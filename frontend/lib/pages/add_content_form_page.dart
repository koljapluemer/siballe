import 'package:flutter/material.dart';

import '../models/language.dart';
import '../services/api_client.dart';
import '../services/language_repository.dart';
import '../services/node_repository.dart';
import '../services/situations_repository.dart';
import '../widgets/smart_field.dart';
import '../widgets/translation_rows_field.dart';

/// Shared form for both "Add Sentence" and "Add Vocab" - `kind` (Node.Kind on
/// the backend: 'SENTENCE' or 'VOCAB') only changes which content is saved.
class AddContentFormPage extends StatefulWidget {
  final String kind;
  final LanguageRepository languageRepository;
  final SituationsRepository situationsRepository;
  final NodeRepository nodeRepository;

  const AddContentFormPage({
    super.key,
    required this.kind,
    this.languageRepository = const LanguageRepository(),
    this.situationsRepository = const SituationsRepository(),
    this.nodeRepository = const NodeRepository(),
  });

  @override
  State<AddContentFormPage> createState() => _AddContentFormPageState();
}

class _AddContentFormPageState extends State<AddContentFormPage> {
  final _languageController = TextEditingController();
  final _situationController = TextEditingController();
  final _contentController = TextEditingController();
  final _translations = TranslationRowsController();

  List<Language> _languages = [];
  Language? _selectedLanguage;
  List<String> _situationsForLanguage = [];
  String? _situationsLoadedForCode;

  bool _submitting = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    widget.languageRepository.list().then((languages) {
      if (mounted) setState(() => _languages = languages);
    });
  }

  @override
  void dispose() {
    _languageController.dispose();
    _situationController.dispose();
    _contentController.dispose();
    _translations.dispose();
    super.dispose();
  }

  Future<List<Language>> _languageSuggestions(String query) async {
    if (query.trim().isEmpty) return [];
    final lower = query.toLowerCase();
    return _languages.where((l) => l.name.toLowerCase().contains(lower)).take(8).toList();
  }

  Future<List<String>> _situationSuggestions(String query) async {
    final language = _selectedLanguage;
    if (language == null) return [];
    if (_situationsLoadedForCode != language.code) {
      _situationsLoadedForCode = language.code;
      final situations = await widget.situationsRepository.listForLanguage(language.code);
      _situationsForLanguage = situations.map((s) => s.description).toList();
    }
    final lower = query.trim().toLowerCase();
    final matches = lower.isEmpty
        ? _situationsForLanguage
        : _situationsForLanguage.where((s) => s.toLowerCase().contains(lower));
    return matches.take(8).toList();
  }

  Future<List<String>> _contentSuggestions(String query) {
    final language = _selectedLanguage;
    if (language == null) return Future.value([]);
    return widget.nodeRepository.search(kind: widget.kind, language: language.code, query: query);
  }

  Language? _resolveLanguage() {
    final typed = _languageController.text.trim().toLowerCase();
    for (final language in _languages) {
      if (language.name.toLowerCase() == typed) return language;
    }
    return null;
  }

  Future<void> _submit() async {
    final language = _resolveLanguage();
    if (language == null) {
      setState(() => _error = 'Select a language from the list.');
      return;
    }
    final content = _contentController.text.trim();
    final translations = _translations.nonEmptyTranslations;
    if (content.isEmpty && translations.isEmpty) {
      setState(() => _error = 'Add the word/sentence or at least one translation.');
      return;
    }

    setState(() {
      _submitting = true;
      _error = null;
    });
    try {
      await widget.nodeRepository.addContent(
        kind: widget.kind,
        language: language.code,
        situationDescription: _situationController.text.trim(),
        content: content,
        translations: translations,
      );
      if (!mounted) return;
      Navigator.of(context).pop();
    } on ApiException catch (e) {
      setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final isSentence = widget.kind == 'SENTENCE';
    return Scaffold(
      appBar: AppBar(title: Text(isSentence ? 'Add Sentence' : 'Add Vocab')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            SmartField<Language>(
              controller: _languageController,
              labelText: 'Language',
              suggestionsBuilder: _languageSuggestions,
              displayStringForOption: (option) => option.name,
              onSelected: (option) => setState(() {
                _selectedLanguage = option;
                _situationsLoadedForCode = null;
              }),
            ),
            const SizedBox(height: 16),
            SmartField<String>(
              controller: _situationController,
              labelText: 'Situation',
              hintText: _selectedLanguage == null ? null : 'General ${_selectedLanguage!.name}',
              suggestionsBuilder: _situationSuggestions,
              displayStringForOption: (option) => option,
            ),
            const SizedBox(height: 16),
            SmartField<String>(
              controller: _contentController,
              labelText: isSentence ? 'Sentence' : 'Word',
              maxLines: isSentence ? 3 : 1,
              suggestionsBuilder: _contentSuggestions,
              displayStringForOption: (option) => option,
            ),
            const SizedBox(height: 16),
            TranslationRowsField(
              controller: _translations,
              kind: widget.kind,
              nodeRepository: widget.nodeRepository,
            ),
            const SizedBox(height: 24),
            if (_error != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Text(
                  _error!,
                  style: TextStyle(color: Theme.of(context).colorScheme.error),
                ),
              ),
            ElevatedButton(
              onPressed: _submitting ? null : _submit,
              child: _submitting
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Text('Save'),
            ),
          ],
        ),
      ),
    );
  }
}
