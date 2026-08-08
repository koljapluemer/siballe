import 'package:flutter/material.dart';

class FsrsButtonRow extends StatelessWidget {
  final VoidCallback onAnswer;

  const FsrsButtonRow({super.key, required this.onAnswer});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _button('Wrong'),
        _button('Hard'),
        _button('Correct'),
        _button('Easy'),
      ],
    );
  }

  Widget _button(String label) {
    return ElevatedButton(onPressed: onAnswer, child: Text(label));
  }
}
