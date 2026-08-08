class Situation {
  final int id;
  final String description;
  final String language;

  const Situation({
    required this.id,
    required this.description,
    required this.language,
  });

  factory Situation.fromJson(Map<String, dynamic> json, String language) {
    return Situation(
      id: json['id'] as int,
      description: json['description'] as String,
      language: language,
    );
  }
}

class LanguageGroup {
  final String language;
  final List<Situation> situations;

  const LanguageGroup({required this.language, required this.situations});

  factory LanguageGroup.fromJson(Map<String, dynamic> json) {
    final language = json['language'] as String;
    final situations = (json['situations'] as List)
        .map((s) => Situation.fromJson(s as Map<String, dynamic>, language))
        .toList();
    return LanguageGroup(language: language, situations: situations);
  }
}
