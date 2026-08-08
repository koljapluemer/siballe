import 'package:flutter/material.dart';

import '../models/situation.dart';

class SituationListItem extends StatelessWidget {
  final Situation situation;
  final bool interested;
  final ValueChanged<bool> onChanged;

  const SituationListItem({
    super.key,
    required this.situation,
    required this.interested,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return CheckboxListTile(
      title: Text(situation.description),
      value: interested,
      onChanged: (value) => onChanged(value ?? false),
    );
  }
}
