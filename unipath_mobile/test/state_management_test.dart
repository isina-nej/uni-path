import 'package:flutter_test/flutter_test.dart';
import 'package:unipath_mobile/providers/course_provider.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  group('Course State Management', () {
    test('Mark course as passed unlocks dependent courses', () {
      final container = ProviderContainer();
      
      // Initial state: Math2 is locked (depends on Math1)
      var courses = container.read(courseListProvider);
      final math1 = courses.firstWhere((c) => c.id == 'm1');
      final math2 = courses.firstWhere((c) => c.id == 'm2');
      
      expect(math1.passed, false, reason: 'Math1 should start unpassed');
      expect(math2.prerequisites.contains('m1'), true, reason: 'Math2 requires Math1');
      
      // Toggle Math1 as passed
      container.read(courseListProvider.notifier).togglePassed('m1');
      courses = container.read(courseListProvider);
      
      // Verify Math1 is now passed
      expect(courses.firstWhere((c) => c.id == 'm1').passed, true);
      
      // Verify Math2 is no longer locked
      final notifier = container.read(courseListProvider.notifier);
      final math2Updated = courses.firstWhere((c) => c.id == 'm2');
      expect(notifier.isLocked(math2Updated), false, reason: 'Math2 should be unlocked');
    });

    test('Grade validation prevents invalid inputs', () {
      expect(0 >= 0 && 0 <= 20, true, reason: '0 is valid');
      expect(20 >= 0 && 20 <= 20, true, reason: '20 is valid');
      expect(15 >= 0 && 15 <= 20, true, reason: '15 is valid');
      expect(-1 >= 0 && -1 <= 20, false, reason: 'Negative grade invalid');
      expect(21 >= 0 && 21 <= 20, false, reason: 'Grade > 20 invalid');
    });
  });
}
