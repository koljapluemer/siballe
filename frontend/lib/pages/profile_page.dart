import 'package:flutter/material.dart';

import '../services/secure_api_key_store.dart';

class ProfilePage extends StatefulWidget {
  final SecureApiKeyStore apiKeyStore;

  const ProfilePage({super.key, this.apiKeyStore = const SecureApiKeyStore()});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  final _controller = TextEditingController();
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    widget.apiKeyStore.read().then((value) {
      if (!mounted) return;
      setState(() {
        _controller.text = value ?? '';
        _loaded = true;
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    final value = _controller.text.trim();
    if (value.isEmpty) {
      await widget.apiKeyStore.delete();
    } else {
      await widget.apiKeyStore.write(value);
    }
    if (!mounted) return;
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Saved.')));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: !_loaded
          ? const Center(child: CircularProgressIndicator())
          : Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 480),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      TextField(
                        controller: _controller,
                        obscureText: true,
                        decoration: const InputDecoration(
                          labelText: 'OpenAI API Key',
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _save,
                        child: const Text('Save'),
                      ),
                    ],
                  ),
                ),
              ),
            ),
    );
  }
}
