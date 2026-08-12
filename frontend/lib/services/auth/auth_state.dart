import 'package:flutter/foundation.dart';

enum AuthStatus { unknown, loggedOut, loggedIn }

/// Current login status, shared by ApiClient (to know whether/when to clear
/// tokens on a failed refresh) and the Profile tab (to render login state).
class AuthState extends ChangeNotifier {
  AuthStatus status = AuthStatus.unknown;
  String? username;

  void setLoggedIn(String username) {
    this.username = username;
    status = AuthStatus.loggedIn;
    notifyListeners();
  }

  void setLoggedOut() {
    if (status == AuthStatus.loggedOut) return;
    username = null;
    status = AuthStatus.loggedOut;
    notifyListeners();
  }
}

/// This app has no dependency-injection framework; auth state is needed by
/// both ApiClient and the Profile tab, so it's a single shared instance.
final authState = AuthState();
