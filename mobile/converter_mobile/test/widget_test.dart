import 'package:converter_mobile/main.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('shows the local converter home screen', (tester) async {
    await tester.pumpWidget(const ConverterApp());
    expect(find.text('Local Convert'), findsOneWidget);
    expect(find.text('Choose files'), findsOneWidget);
    expect(find.text('Private file conversion'), findsOneWidget);
  });
}
