import 'package:flutter/material.dart';
import 'package:flutter_markdown_plus/flutter_markdown_plus.dart';

class Flashcard extends StatelessWidget {
  final String front;
  final String? back;
  final String? credits;

  const Flashcard({super.key, required this.front, this.back, this.credits});

  @override
  Widget build(BuildContext context) {
    final revealed = back != null;
    return Card(
      margin: const EdgeInsets.all(16),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            MarkdownBody(data: front, shrinkWrap: true),
            if (revealed) ...[
              const Divider(height: 32),
              MarkdownBody(data: back!, shrinkWrap: true),
            ],
            if (revealed && credits != null && credits!.isNotEmpty) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surfaceContainerHighest,
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(
                  credits!,
                  style: Theme.of(context).textTheme.labelSmall,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
