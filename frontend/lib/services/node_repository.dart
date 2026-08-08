import 'api_client.dart';
import 'secure_api_key_store.dart';

class TranslationInput {
  final String content;
  final String note;

  const TranslationInput({required this.content, this.note = ''});

  Map<String, dynamic> toJson() => {'content': content, 'note': note};
}

class AddContentResult {
  final int? nodeId;
  final int situationId;
  final String? generationError;

  const AddContentResult({required this.nodeId, required this.situationId, this.generationError});

  factory AddContentResult.fromJson(Map<String, dynamic> json) {
    return AddContentResult(
      nodeId: json['node_id'] as int?,
      situationId: json['situation_id'] as int,
      generationError: json['generation_error'] as String?,
    );
  }
}

class NodeRepository {
  final ApiClient _client;
  final SecureApiKeyStore _apiKeyStore;

  const NodeRepository({
    this._client = const ApiClient(),
    this._apiKeyStore = const SecureApiKeyStore(),
  });

  Future<List<String>> search({
    required String kind,
    required String language,
    required String query,
  }) async {
    if (query.trim().isEmpty) return [];
    final data = await _client.get(
      '/nodes/search/',
      query: {'kind': kind, 'language': language, 'q': query},
    );
    return (data as List).map((row) => row['content'] as String).toList();
  }

  Future<AddContentResult> addContent({
    required String kind,
    required String language,
    required String situationDescription,
    required String content,
    required List<TranslationInput> translations,
  }) async {
    final apiKey = await _apiKeyStore.read();
    final body = {
      'kind': kind,
      'language': language,
      'situation_description': situationDescription,
      'content': content,
      'translations': translations.map((t) => t.toJson()).toList(),
      if (apiKey != null && apiKey.isNotEmpty) 'openai_api_key': apiKey,
    };
    final data = await _client.post('/nodes/add-content/', body);
    return AddContentResult.fromJson(data as Map<String, dynamic>);
  }
}
