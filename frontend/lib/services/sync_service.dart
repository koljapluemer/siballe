import 'api_client.dart';
import 'auth/auth_state.dart';
import 'db/local_exercise_store.dart';
import 'exercise_repository.dart';

/// Best-effort background sync: refreshes the local exercise pool for the
/// given situations, and — if logged in — pushes locally graded reviews and
/// merges the server's authoritative progress back in. Failures (offline,
/// server error, not logged in) are swallowed; the UI already has everything
/// it needs from local storage regardless of sync outcome.
class SyncService {
  final ExerciseRepository _exerciseRepository;
  final ApiClient _client;
  final LocalExerciseStore _store;

  SyncService({
    this._exerciseRepository = const ExerciseRepository(),
    this._client = const ApiClient(),
    LocalExerciseStore? store,
  }) : _store = store ?? localExerciseStore;

  Future<void> syncAll({required Set<int> interestedSituationIds}) async {
    await _refreshPool(interestedSituationIds);
    await _syncProgress();
  }

  Future<void> _refreshPool(Set<int> situationIds) async {
    if (situationIds.isEmpty) return;
    try {
      final entries = await _exerciseRepository.pool(situationIds);
      await _store.upsertPool(entries);
    } on ApiException {
      // Offline or server error — keep using whatever is already cached.
    }
  }

  Future<void> _syncProgress() async {
    if (authState.status != AuthStatus.loggedIn) return;
    try {
      final dirty = await _store.dirtyCards();
      final response = await _client.post('/sync/exercise-progress/', {
        'progress': dirty.map((d) => d.toJson()).toList(),
      });
      final entries = ((response as Map<String, dynamic>)['progress'] as List)
          .map((e) => ServerProgressEntry.fromJson(e as Map<String, dynamic>))
          .toList();
      await _store.applyServerState(entries);
    } on ApiException {
      // Offline, unauthenticated, or server error — try again next sync.
    }
  }
}
