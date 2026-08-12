import 'dart:convert';

import 'package:http/http.dart' as http;

import 'auth/auth_state.dart';
import 'auth/token_store.dart';

const String apiBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://127.0.0.1:8000/api',
);

class ApiException implements Exception {
  final int? statusCode;
  final String message;

  ApiException(this.message, {this.statusCode});

  @override
  String toString() => message;
}

class ApiClient {
  final AuthTokenStore _tokenStore;

  const ApiClient({this._tokenStore = const AuthTokenStore()});

  Future<dynamic> get(String path, {Map<String, String>? query}) async {
    final uri = Uri.parse('$apiBaseUrl$path').replace(queryParameters: query);
    final response = await _sendWithRetry(
      (headers) => http.get(uri, headers: headers),
    );
    return _decode(response);
  }

  Future<dynamic> post(String path, Map<String, dynamic> body) async {
    final uri = Uri.parse('$apiBaseUrl$path');
    final response = await _sendWithRetry(
      (headers) => http.post(
        uri,
        headers: {...headers, 'Content-Type': 'application/json'},
        body: jsonEncode(body),
      ),
    );
    return _decode(response);
  }

  /// Sends a request with the current access token attached (if any). On a
  /// 401, attempts one silent token refresh and retries once; if the refresh
  /// also fails, the stored tokens are cleared and [authState] moves to
  /// loggedOut — sync just stops silently, no forced UI interruption.
  Future<http.Response> _sendWithRetry(
    Future<http.Response> Function(Map<String, String> headers) send,
  ) async {
    http.Response response;
    try {
      response = await send(await _authHeaders());
    } catch (e) {
      throw ApiException('Could not reach the server: $e');
    }

    if (response.statusCode == 401) {
      if (await _refreshAccessToken()) {
        try {
          response = await send(await _authHeaders());
        } catch (e) {
          throw ApiException('Could not reach the server: $e');
        }
      } else {
        await _tokenStore.clear();
        authState.setLoggedOut();
      }
    }
    return response;
  }

  Future<Map<String, String>> _authHeaders() async {
    final access = await _tokenStore.accessToken;
    return access == null ? {} : {'Authorization': 'Bearer $access'};
  }

  Future<bool> _refreshAccessToken() async {
    final refresh = await _tokenStore.refreshToken;
    if (refresh == null) return false;
    try {
      final response = await http.post(
        Uri.parse('$apiBaseUrl/auth/token/refresh/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'refresh': refresh}),
      );
      if (response.statusCode != 200) return false;
      final access = (jsonDecode(response.body) as Map)['access'] as String;
      await _tokenStore.saveAccessToken(access);
      return true;
    } catch (_) {
      return false;
    }
  }

  dynamic _decode(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return jsonDecode(response.body);
    }

    String detail = response.body;
    try {
      final decoded = jsonDecode(response.body);
      if (decoded is Map && decoded['detail'] != null) {
        detail = decoded['detail'].toString();
      }
    } catch (_) {
      // body wasn't JSON, keep raw text
    }
    throw ApiException(detail, statusCode: response.statusCode);
  }
}
