import 'package:shared_preferences/shared_preferences.dart';

/// Frontend-only persistence of which situations the user wants to learn.
/// Never synced to the backend — there's no field for it there.
class InterestPrefs {
  static const _key = 'interested_situation_ids';

  const InterestPrefs();

  Future<Set<int>> getInterestedIds() async {
    final prefs = await SharedPreferences.getInstance();
    final stored = prefs.getStringList(_key) ?? const [];
    return stored.map(int.parse).toSet();
  }

  Future<void> setInterested(int situationId, bool interested) async {
    final prefs = await SharedPreferences.getInstance();
    final ids = await getInterestedIds();
    if (interested) {
      ids.add(situationId);
    } else {
      ids.remove(situationId);
    }
    await prefs.setStringList(_key, ids.map((id) => id.toString()).toList());
  }
}
