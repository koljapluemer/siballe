class Exercise {
  final String kind;
  final String front;
  final String back;
  final String credits;

  const Exercise({
    required this.kind,
    required this.front,
    required this.back,
    required this.credits,
  });

  factory Exercise.fromJson(Map<String, dynamic> json) {
    return Exercise(
      kind: json['kind'] as String,
      front: json['front'] as String,
      back: json['back'] as String,
      credits: json['credits'] as String,
    );
  }
}
