class Exercise {
  final int id;
  final String kind;
  final String front;
  final String back;
  final String credits;

  const Exercise({
    required this.id,
    required this.kind,
    required this.front,
    required this.back,
    required this.credits,
  });

  factory Exercise.fromJson(Map<String, dynamic> json) {
    return Exercise(
      id: json['id'] as int,
      kind: json['kind'] as String,
      front: json['front'] as String,
      back: json['back'] as String,
      credits: json['credits'] as String,
    );
  }
}

/// One entry from GET /exercises/pool/ — an Exercise plus the situations it's
/// eligible under, used to populate the local cache.
class ExercisePoolEntry {
  final Exercise exercise;
  final List<int> situationIds;

  const ExercisePoolEntry({required this.exercise, required this.situationIds});

  factory ExercisePoolEntry.fromJson(Map<String, dynamic> json) {
    return ExercisePoolEntry(
      exercise: Exercise.fromJson(json),
      situationIds: (json['situation_ids'] as List).cast<int>(),
    );
  }
}
