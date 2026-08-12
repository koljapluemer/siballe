import 'package:flutter/material.dart';
import 'package:fsrs/fsrs.dart';

class FsrsButtonRow extends StatelessWidget {
  final ValueChanged<Rating> onRate;

  const FsrsButtonRow({super.key, required this.onRate});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _button('Wrong', Rating.again),
        _button('Hard', Rating.hard),
        _button('Correct', Rating.good),
        _button('Easy', Rating.easy),
      ],
    );
  }

  Widget _button(String label, Rating rating) {
    return ElevatedButton(onPressed: () => onRate(rating), child: Text(label));
  }
}
