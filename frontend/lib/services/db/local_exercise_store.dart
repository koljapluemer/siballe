import 'dart:convert';

import 'package:drift/drift.dart';
import 'package:fsrs/fsrs.dart' as fsrs;

import '../../models/exercise.dart';
import 'app_database.dart';
import 'tables.dart';

/// An exercise paired with its local FSRS review state, if any. A `null` card
/// means the exercise has never been reviewed on this device ("new").
class ExerciseCandidate {
  final Exercise exercise;
  final fsrs.Card? card;

  const ExerciseCandidate({required this.exercise, this.card});
}

/// A locally-graded review not yet confirmed by the server.
class DirtyReview {
  final int exerciseId;
  final Map<String, dynamic> cardData;
  final DateTime updatedAt;

  const DirtyReview({
    required this.exerciseId,
    required this.cardData,
    required this.updatedAt,
  });

  Map<String, dynamic> toJson() => {
    'node_id': exerciseId,
    'card_data': cardData,
    'updated_at': updatedAt.toIso8601String(),
  };
}

/// One row of the server's authoritative progress state, as returned by
/// POST /sync/exercise-progress/.
class ServerProgressEntry {
  final int nodeId;
  final Map<String, dynamic> cardData;
  final DateTime updatedAt;

  const ServerProgressEntry({
    required this.nodeId,
    required this.cardData,
    required this.updatedAt,
  });

  factory ServerProgressEntry.fromJson(Map<String, dynamic> json) {
    return ServerProgressEntry(
      nodeId: json['node_id'] as int,
      cardData: json['card_data'] as Map<String, dynamic>,
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
}

/// Local cache of exercise content + FSRS review state, backed by drift/sqlite.
class LocalExerciseStore {
  final AppDatabase _db;

  const LocalExerciseStore(this._db);

  /// Refreshes cached exercise content from the pool endpoint. Never touches
  /// [ReviewCards] — content refresh must not reset review progress.
  Future<void> upsertPool(List<ExercisePoolEntry> entries) async {
    final now = DateTime.now().toUtc();
    await _db.batch((batch) {
      for (final entry in entries) {
        batch.insert(
          _db.exercises,
          ExercisesCompanion.insert(
            id: Value(entry.exercise.id),
            kind: entry.exercise.kind,
            front: entry.exercise.front,
            back: entry.exercise.back,
            credits: entry.exercise.credits,
            contentUpdatedAt: now,
          ),
          mode: InsertMode.insertOrReplace,
        );
        for (final situationId in entry.situationIds) {
          batch.insert(
            _db.exerciseSituations,
            ExerciseSituationsCompanion.insert(
              exerciseId: entry.exercise.id,
              situationId: situationId,
            ),
            mode: InsertMode.insertOrIgnore,
          );
        }
      }
    });
  }

  /// Exercises eligible under any of [situationIds], each paired with its
  /// local review state (if any). This is the candidate pool the picking
  /// strategy chooses from — entirely local, no network involved.
  Future<List<ExerciseCandidate>> candidatesForSituations(
    Set<int> situationIds,
  ) async {
    if (situationIds.isEmpty) return [];

    final query = _db.select(_db.exercises).join([
      innerJoin(
        _db.exerciseSituations,
        _db.exerciseSituations.exerciseId.equalsExp(_db.exercises.id),
      ),
      leftOuterJoin(
        _db.reviewCards,
        _db.reviewCards.exerciseId.equalsExp(_db.exercises.id),
      ),
    ])..where(_db.exerciseSituations.situationId.isIn(situationIds));

    final rows = await query.get();

    // A node can match on more than one interested situation; dedupe by id.
    final byExercise = <int, ExerciseCandidate>{};
    for (final row in rows) {
      final exerciseRow = row.readTable(_db.exercises);
      final cardRow = row.readTableOrNull(_db.reviewCards);
      byExercise[exerciseRow.id] = ExerciseCandidate(
        exercise: _toExercise(exerciseRow),
        card: cardRow == null ? null : _toCard(cardRow),
      );
    }
    return byExercise.values.toList();
  }

  /// Records a graded review locally and marks it dirty for the next sync.
  Future<void> saveReview(int exerciseId, fsrs.Card card) async {
    await _db
        .into(_db.reviewCards)
        .insertOnConflictUpdate(
          ReviewCardsCompanion.insert(
            exerciseId: Value(exerciseId),
            cardJson: jsonEncode(card.toMap()),
            due: card.due,
            updatedAt: DateTime.now().toUtc(),
            dirty: const Value(true),
          ),
        );
  }

  Future<List<DirtyReview>> dirtyCards() async {
    final rows = await (_db.select(
      _db.reviewCards,
    )..where((t) => t.dirty.equals(true))).get();
    return rows
        .map(
          (row) => DirtyReview(
            exerciseId: row.exerciseId,
            cardData: jsonDecode(row.cardJson) as Map<String, dynamic>,
            updatedAt: row.updatedAt,
          ),
        )
        .toList();
  }

  /// Merges the server's authoritative progress set back in. The server has
  /// already resolved last-write-wins, so an entry only gets dropped locally
  /// if it's somehow older than what's already here (defensive; shouldn't
  /// happen since a dirty local row is always included in the preceding push).
  Future<void> applyServerState(List<ServerProgressEntry> entries) async {
    await _db.transaction(() async {
      for (final entry in entries) {
        final existing =
            await (_db.select(
              _db.reviewCards,
            )..where((t) => t.exerciseId.equals(entry.nodeId))).getSingleOrNull();
        if (existing != null && existing.updatedAt.isAfter(entry.updatedAt)) {
          continue;
        }
        await _db
            .into(_db.reviewCards)
            .insertOnConflictUpdate(
              ReviewCardsCompanion.insert(
                exerciseId: Value(entry.nodeId),
                cardJson: jsonEncode(entry.cardData),
                due: DateTime.parse(entry.cardData['due'] as String),
                updatedAt: entry.updatedAt,
                dirty: const Value(false),
              ),
            );
      }
    });
  }

  Exercise _toExercise(ExerciseRow row) => Exercise(
    id: row.id,
    kind: row.kind,
    front: row.front,
    back: row.back,
    credits: row.credits,
  );

  fsrs.Card _toCard(ReviewCardRow row) =>
      fsrs.Card.fromMap(jsonDecode(row.cardJson) as Map<String, dynamic>);
}

/// This app has no dependency-injection framework; the store wraps the single
/// shared [appDatabase] connection, so it's a top-level singleton too.
final localExerciseStore = LocalExerciseStore(appDatabase);
