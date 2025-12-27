import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:unipath_mobile/main.dart';

void main() {
  testWidgets('App loads without crashing', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(child: UnipathApp()),
    );
    expect(find.byType(UnipathApp), findsOneWidget);
  });
}
