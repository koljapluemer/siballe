import 'package:drift/drift.dart';

/// Cached exercise content, keyed by the backend's stable node id. Refreshed
/// from the pool endpoint; never touched when a review is graded.
@DataClassName('ExerciseRow')
class Exercises extends Table {
  IntColumn get id => integer()();
  TextColumn get kind => text()();
  TextColumn get front => text()();
  TextColumn get back => text()();
  TextColumn get credits => text()();
  DateTimeColumn get contentUpdatedAt => dateTime()();

  @override
  Set<Column> get primaryKey => {id};
}

/// Many-to-many: which situations each exercise is eligible under.
@DataClassName('ExerciseSituationRow')
class ExerciseSituations extends Table {
  IntColumn get exerciseId => integer()();
  IntColumn get situationId => integer()();

  @override
  Set<Column> get primaryKey => {exerciseId, situationId};
}

/// FSRS review state for an exercise. Absence of a row for an exercise id
/// means "new/never reviewed" — see DefaultExercisePickingStrategy.
@DataClassName('ReviewCardRow')
class ReviewCards extends Table {
  IntColumn get exerciseId => integer()();
  TextColumn get cardJson => text()(); // fsrs Card.toMap(), jsonEncoded
  DateTimeColumn get due => dateTime()();
  DateTimeColumn get updatedAt => dateTime()(); // local grading time; LWW comparator
  BoolColumn get dirty => boolean().withDefault(const Constant(true))();

  @override
  Set<Column> get primaryKey => {exerciseId};
}
