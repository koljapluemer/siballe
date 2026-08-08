import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// On-device-only storage for the user's OpenAI API key. Never sent to or
/// stored by our backend - only included, per-request, when the user submits
/// the Add-content form.
class SecureApiKeyStore {
  static const _key = 'openai_api_key';

  final FlutterSecureStorage _storage;

  const SecureApiKeyStore({this._storage = const FlutterSecureStorage()});

  Future<String?> read() => _storage.read(key: _key);

  Future<void> write(String apiKey) => _storage.write(key: _key, value: apiKey);

  Future<void> delete() => _storage.delete(key: _key);
}
