import 'dart:math';

import '../db/local_exercise_store.dart';
import 'exercise_picking_strategy.dart';

/// If anything is due: 5/6 of the time show a due exercise, 1/6 of the time
/// show a random new (never-reviewed) one instead. If nothing is due, prefer
/// a new exercise. If there's neither (or the pool is otherwise empty of
/// options), fall back to whatever is due least far in the future.
class DefaultExercisePickingStrategy implements ExercisePickingStrategy {
  const DefaultExercisePickingStrategy();

  @override
  ExerciseCandidate? pick(
    List<ExerciseCandidate> candidates,
    DateTime now,
    Random rng,
  ) {
    final due = candidates
        .where((c) => c.card != null && !c.card!.due.isAfter(now))
        .toList();
    final fresh = candidates.where((c) => c.card == null).toList();

    if (due.isNotEmpty) {
      if (fresh.isNotEmpty && rng.nextInt(6) == 0) {
        return fresh[rng.nextInt(fresh.length)];
      }
      return due[rng.nextInt(due.length)];
    }
    if (fresh.isNotEmpty) {
      return fresh[rng.nextInt(fresh.length)];
    }
    if (candidates.isEmpty) return null;
    return candidates.reduce(
      (a, b) => a.card!.due.isBefore(b.card!.due) ? a : b,
    );
  }
}
