import 'package:flutter/material.dart';

import '../services/node_repository.dart';
import 'smart_field.dart';

class _TranslationRowControllers {
  final TextEditingController content = TextEditingController();
  final TextEditingController note = TextEditingController();

  bool get isEmpty => content.text.trim().isEmpty;

  void dispose() {
    content.dispose();
    note.dispose();
  }
}

/// Owns the list of translation-row text controllers so the parent form can
/// read the current values on submit without the field needing a form-wide
/// key. Always keeps exactly one trailing empty row (auto-grow).
class TranslationRowsController extends ChangeNotifier {
  final List<_TranslationRowControllers> _rows = [_TranslationRowControllers()];

  void ensureTrailingEmptyRow() {
    if (_rows.isEmpty || !_rows.last.isEmpty) {
      _rows.add(_TranslationRowControllers());
      notifyListeners();
    }
  }

  void removeAt(int index) {
    if (_rows.length <= 1) return;
    _rows[index].dispose();
    _rows.removeAt(index);
    notifyListeners();
  }

  List<TranslationInput> get nonEmptyTranslations => _rows
      .where((row) => !row.isEmpty)
      .map(
        (row) => TranslationInput(content: row.content.text.trim(), note: row.note.text.trim()),
      )
      .toList();

  @override
  void dispose() {
    for (final row in _rows) {
      row.dispose();
    }
    super.dispose();
  }
}

class TranslationRowsField extends StatefulWidget {
  final TranslationRowsController controller;
  final String kind;
  final NodeRepository nodeRepository;

  const TranslationRowsField({
    super.key,
    required this.controller,
    required this.kind,
    this.nodeRepository = const NodeRepository(),
  });

  @override
  State<TranslationRowsField> createState() => _TranslationRowsFieldState();
}

class _TranslationRowsFieldState extends State<TranslationRowsField> {
  @override
  void initState() {
    super.initState();
    widget.controller.addListener(_rebuild);
  }

  @override
  void dispose() {
    widget.controller.removeListener(_rebuild);
    super.dispose();
  }

  void _rebuild() => setState(() {});

  @override
  Widget build(BuildContext context) {
    final rows = widget.controller._rows;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text('Translations', style: Theme.of(context).textTheme.labelLarge),
        const SizedBox(height: 8),
        for (var i = 0; i < rows.length; i++)
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      SmartField<String>(
                        controller: rows[i].content,
                        labelText: 'English',
                        suggestionsBuilder: (query) => widget.nodeRepository.search(
                          kind: widget.kind,
                          language: 'eng',
                          query: query,
                        ),
                        displayStringForOption: (option) => option,
                        onChanged: (_) => widget.controller.ensureTrailingEmptyRow(),
                      ),
                      const SizedBox(height: 4),
                      TextField(
                        controller: rows[i].note,
                        decoration: const InputDecoration(
                          labelText: 'Note (optional)',
                          border: OutlineInputBorder(),
                          isDense: true,
                        ),
                      ),
                    ],
                  ),
                ),
                if (rows.length > 1)
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => widget.controller.removeAt(i),
                  ),
              ],
            ),
          ),
      ],
    );
  }
}
