import 'dart:async';

import 'package:flutter/material.dart';

/// A text field that suggests completions in a list right below it as the
/// user types, without forcing them to pick one - matching a "smart dropdown"
/// (see spec2.md): free text is always accepted, suggestions are just a
/// shortcut to reuse something that already exists.
class SmartField<T> extends StatefulWidget {
  final TextEditingController controller;
  final String labelText;
  final String? hintText;
  final int maxLines;
  final Future<List<T>> Function(String query) suggestionsBuilder;
  final String Function(T option) displayStringForOption;
  final void Function(T option)? onSelected;
  final void Function(String value)? onChanged;

  const SmartField({
    super.key,
    required this.controller,
    required this.labelText,
    required this.suggestionsBuilder,
    required this.displayStringForOption,
    this.hintText,
    this.maxLines = 1,
    this.onSelected,
    this.onChanged,
  });

  @override
  State<SmartField<T>> createState() => _SmartFieldState<T>();
}

class _SmartFieldState<T> extends State<SmartField<T>> {
  List<T> _suggestions = [];
  Timer? _debounce;
  int _requestId = 0;
  final _focusNode = FocusNode();

  @override
  void dispose() {
    _debounce?.cancel();
    _focusNode.dispose();
    super.dispose();
  }

  void _onTextChanged(String value) {
    widget.onChanged?.call(value);
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 250), () => _fetch(value));
  }

  Future<void> _fetch(String query) async {
    final requestId = ++_requestId;
    final results = await widget.suggestionsBuilder(query);
    if (!mounted || requestId != _requestId || !_focusNode.hasFocus) return;
    setState(() => _suggestions = results);
  }

  void _select(T option) {
    widget.controller.text = widget.displayStringForOption(option);
    widget.onSelected?.call(option);
    setState(() => _suggestions = []);
    _focusNode.unfocus();
  }

  void _dismiss() {
    if (_suggestions.isEmpty) return;
    setState(() => _suggestions = []);
    _focusNode.unfocus();
  }

  @override
  Widget build(BuildContext context) {
    // Suggestions are dismissed via TapRegion rather than a focus-loss
    // listener: tapping a suggestion drops the field's focus before its
    // onTap fires, so clearing suggestions on focus loss would unmount the
    // tile mid-tap and swallow the selection.
    return TapRegion(
      onTapOutside: (_) => _dismiss(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          TextField(
            controller: widget.controller,
            focusNode: _focusNode,
            maxLines: widget.maxLines,
            decoration: InputDecoration(
              labelText: widget.labelText,
              hintText: widget.hintText,
              border: const OutlineInputBorder(),
            ),
            onChanged: _onTextChanged,
          ),
          if (_suggestions.isNotEmpty)
            Card(
              margin: const EdgeInsets.only(top: 2),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  for (final option in _suggestions)
                    ListTile(
                      dense: true,
                      title: Text(widget.displayStringForOption(option)),
                      onTap: () => _select(option),
                    ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
