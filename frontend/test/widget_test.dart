import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:frontend/app.dart';

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  testWidgets('bottom nav shows Learn/Add/Situations and switches tabs', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const App());
    await tester.pump();

    expect(find.text('Learn'), findsWidgets);
    expect(find.text('Add'), findsWidgets);
    expect(find.text('Situations'), findsWidgets);

    await tester.tap(find.text('Add'));
    await tester.pump();
    expect(find.text('Coming soon.'), findsOneWidget);
  });
}
