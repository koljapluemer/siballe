import 'package:flutter/material.dart';

class FsrsButtonRow extends StatelessWidget {
  final VoidCallback onAnswer;

  const FsrsButtonRow({super.key, required this.onAnswer});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _button(context, 'Wrong', Colors.red),
        _button(context, 'Hard', Colors.orange),
        _button(context, 'Correct', Colors.green),
        _button(context, 'Easy', Colors.blue),
      ],
    );
  }

  Widget _button(BuildContext context, String label, Color color) {
    return ElevatedButton(
      onPressed: onAnswer,
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        foregroundColor: Colors.white,
      ),
      child: Text(label),
    );
  }
}
