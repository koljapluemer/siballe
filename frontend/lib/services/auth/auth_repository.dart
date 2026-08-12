import '../api_client.dart';
import 'auth_state.dart';
import 'token_store.dart';

class AuthRepository {
  final ApiClient _client;
  final AuthTokenStore _tokenStore;

  const AuthRepository({
    this._client = const ApiClient(),
    this._tokenStore = const AuthTokenStore(),
  });

  Future<void> register({
    required String username,
    required String email,
    required String password,
  }) async {
    final data = await _client.post('/auth/register/', {
      'username': username,
      'email': email,
      'password': password,
      'password_confirm': password,
    });
    await _saveTokens(data as Map<String, dynamic>);
    await _loadMe();
  }

  Future<void> login({required String username, required String password}) async {
    final data = await _client.post('/auth/token/', {
      'username': username,
      'password': password,
    });
    await _saveTokens(data as Map<String, dynamic>);
    await _loadMe();
  }

  Future<void> logout() async {
    await _tokenStore.clear();
    authState.setLoggedOut();
  }

  /// Restores login state from stored tokens at app start.
  Future<void> restoreSession() async {
    if (await _tokenStore.accessToken == null) {
      authState.setLoggedOut();
      return;
    }
    try {
      await _loadMe();
    } on ApiException {
      // ApiClient already attempts one silent refresh internally, so a
      // failure here means the session is genuinely dead.
      await _tokenStore.clear();
      authState.setLoggedOut();
    }
  }

  Future<void> _saveTokens(Map<String, dynamic> data) => _tokenStore.save(
    accessToken: data['access'] as String,
    refreshToken: data['refresh'] as String,
  );

  Future<void> _loadMe() async {
    final data = await _client.get('/auth/me/') as Map<String, dynamic>;
    authState.setLoggedIn(data['username'] as String);
  }
}
