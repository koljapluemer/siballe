import '../models/language.dart';
import 'api_client.dart';

class LanguageRepository {
  final ApiClient _client;

  const LanguageRepository({this._client = const ApiClient()});

  static List<Language>? _cache;

  Future<List<Language>> list() async {
    final cached = _cache;
    if (cached != null) return cached;
    final data = await _client.get('/languages/');
    final languages = (data as List)
        .map((l) => Language.fromJson(l as Map<String, dynamic>))
        .toList();
    _cache = languages;
    return languages;
  }
}
