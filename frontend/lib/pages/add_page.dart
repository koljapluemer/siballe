import 'package:flutter/material.dart';

import 'add_content_form_page.dart';

class AddPage extends StatelessWidget {
  const AddPage({super.key});

  void _open(BuildContext context, String kind) {
    Navigator.of(
      context,
    ).push(MaterialPageRoute(builder: (_) => AddContentFormPage(kind: kind)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Add')),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 480),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                ElevatedButton(
                  onPressed: () => _open(context, 'SENTENCE'),
                  child: const Text('Add Sentence'),
                ),
                const SizedBox(height: 12),
                ElevatedButton(
                  onPressed: () => _open(context, 'VOCAB'),
                  child: const Text('Add Vocab'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
