import 'dart:math';

import '../db/local_exercise_store.dart';

/// Chooses the next exercise to show from a local candidate pool. Purely a
/// function of local state — network/offline status is not a special case,
/// it's just whatever the pool happens to contain. Swap the implementation
/// (e.g. difficulty-weighted picking) without touching callers.
abstract class ExercisePickingStrategy {
  ExerciseCandidate? pick(
    List<ExerciseCandidate> candidates,
    DateTime now,
    Random rng,
  );
}
