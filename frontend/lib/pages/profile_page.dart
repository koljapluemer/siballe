import 'package:flutter/material.dart';

import '../services/api_client.dart';
import '../services/auth/auth_repository.dart';
import '../services/auth/auth_state.dart';
import '../services/secure_api_key_store.dart';

class ProfilePage extends StatefulWidget {
  final SecureApiKeyStore apiKeyStore;
  final AuthRepository authRepository;

  const ProfilePage({
    super.key,
    this.apiKeyStore = const SecureApiKeyStore(),
    this.authRepository = const AuthRepository(),
  });

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  final _apiKeyController = TextEditingController();
  bool _apiKeyLoaded = false;

  @override
  void initState() {
    super.initState();
    widget.apiKeyStore.read().then((value) {
      if (!mounted) return;
      setState(() {
        _apiKeyController.text = value ?? '';
        _apiKeyLoaded = true;
      });
    });
  }

  @override
  void dispose() {
    _apiKeyController.dispose();
    super.dispose();
  }

  Future<void> _saveApiKey() async {
    final value = _apiKeyController.text.trim();
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
      body: !_apiKeyLoaded
          ? const Center(child: CircularProgressIndicator())
          : Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 480),
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      _AuthSection(authRepository: widget.authRepository),
                      const SizedBox(height: 32),
                      const Divider(),
                      const SizedBox(height: 16),
                      TextField(
                        controller: _apiKeyController,
                        obscureText: true,
                        decoration: const InputDecoration(
                          labelText: 'OpenAI API Key',
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _saveApiKey,
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

class _AuthSection extends StatefulWidget {
  final AuthRepository authRepository;

  const _AuthSection({required this.authRepository});

  @override
  State<_AuthSection> createState() => _AuthSectionState();
}

class _AuthSectionState extends State<_AuthSection> {
  bool _showSignup = false;
  bool _submitting = false;
  String? _error;

  final _usernameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmController = TextEditingController();

  @override
  void dispose() {
    _usernameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (_showSignup && _passwordController.text != _confirmController.text) {
      setState(() => _error = 'Passwords do not match.');
      return;
    }

    setState(() {
      _submitting = true;
      _error = null;
    });
    try {
      if (_showSignup) {
        await widget.authRepository.register(
          username: _usernameController.text.trim(),
          email: _emailController.text.trim(),
          password: _passwordController.text,
        );
      } else {
        await widget.authRepository.login(
          username: _usernameController.text.trim(),
          password: _passwordController.text,
        );
      }
      _passwordController.clear();
      _confirmController.clear();
    } on ApiException catch (e) {
      if (mounted) setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: authState,
      builder: (context, _) {
        switch (authState.status) {
          case AuthStatus.unknown:
            return const Center(child: CircularProgressIndicator());
          case AuthStatus.loggedIn:
            return Row(
              children: [
                Expanded(child: Text('Logged in as ${authState.username}')),
                TextButton(
                  onPressed: widget.authRepository.logout,
                  child: const Text('Log out'),
                ),
              ],
            );
          case AuthStatus.loggedOut:
            return _buildForm(context);
        }
      },
    );
  }

  Widget _buildForm(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        TextField(
          controller: _usernameController,
          decoration: const InputDecoration(
            labelText: 'Username',
            border: OutlineInputBorder(),
          ),
        ),
        if (_showSignup) ...[
          const SizedBox(height: 8),
          TextField(
            controller: _emailController,
            decoration: const InputDecoration(
              labelText: 'Email',
              border: OutlineInputBorder(),
            ),
          ),
        ],
        const SizedBox(height: 8),
        TextField(
          controller: _passwordController,
          obscureText: true,
          decoration: const InputDecoration(
            labelText: 'Password',
            border: OutlineInputBorder(),
          ),
        ),
        if (_showSignup) ...[
          const SizedBox(height: 8),
          TextField(
            controller: _confirmController,
            obscureText: true,
            decoration: const InputDecoration(
              labelText: 'Confirm password',
              border: OutlineInputBorder(),
            ),
          ),
        ],
        if (_error != null) ...[
          const SizedBox(height: 8),
          Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
        ],
        const SizedBox(height: 16),
        ElevatedButton(
          onPressed: _submitting ? null : _submit,
          child: Text(_showSignup ? 'Create account' : 'Log in'),
        ),
        TextButton(
          onPressed: _submitting
              ? null
              : () => setState(() => _showSignup = !_showSignup),
          child: Text(_showSignup ? 'Log in instead' : 'Create account instead'),
        ),
      ],
    );
  }
}
