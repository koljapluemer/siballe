class Language {
  final String code;
  final String name;

  const Language({required this.code, required this.name});

  factory Language.fromJson(Map<String, dynamic> json) {
    return Language(code: json['code'] as String, name: json['name'] as String);
  }

  @override
  String toString() => name;
}
