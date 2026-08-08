import '../models/exercise.dart';
import 'api_client.dart';

class ExerciseRepository {
  final ApiClient _client;

  const ExerciseRepository({this._client = const ApiClient()});

  Future<Exercise> generate(int situationId) async {
    final data = await _client.get(
      '/exercises/generate/',
      query: {'situation_id': situationId.toString()},
    );
    return Exercise.fromJson(data as Map<String, dynamic>);
  }
}
