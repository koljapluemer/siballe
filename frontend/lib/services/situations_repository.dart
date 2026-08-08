import '../models/situation.dart';
import 'api_client.dart';

class SituationsRepository {
  final ApiClient _client;

  const SituationsRepository({this._client = const ApiClient()});

  Future<List<LanguageGroup>> fetchGrouped() async {
    final data = await _client.get('/situations/');
    return (data as List)
        .map((g) => LanguageGroup.fromJson(g as Map<String, dynamic>))
        .toList();
  }

  Future<List<Situation>> listForLanguage(String languageCode) async {
    final data = await _client.get('/situations/', query: {'language': languageCode});
    final groups = (data as List)
        .map((g) => LanguageGroup.fromJson(g as Map<String, dynamic>))
        .toList();
    return groups.isEmpty ? [] : groups.first.situations;
  }
}
