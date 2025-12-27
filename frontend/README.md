# Frontend - Unipath

## Overview

Unipath Frontend is a Flutter mobile and web application for the university course selection system. It provides:

- User authentication (Student, Admin, Professor, HOD)
- Curriculum visualization (Course Chart)
- Course recommendation engine interface
- Weekly schedule planning
- Student progress tracking
- Profile management

## Tech Stack

- **Framework:** Flutter 3.x
- **Language:** Dart
- **Platforms:** iOS, Android, Web
- **State Management:** Provider / Riverpod (to be configured)
- **UI:** Material Design 3 + RTL Support

## Project Structure

```
frontend/unipath/
├── lib/
│   ├── main.dart                 # App entry point
│   ├── models/                   # Data models
│   │   ├── user.dart
│   │   ├── course.dart
│   │   └── chart.dart
│   ├── screens/                  # UI screens
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── chart/
│   │   ├── schedule/
│   │   └── profile/
│   ├── services/                 # API services
│   │   ├── auth_service.dart
│   │   ├── course_service.dart
│   │   └── api_client.dart
│   ├── widgets/                  # Reusable widgets
│   └── utils/                    # Utilities
├── test/                         # Unit & widget tests
├── pubspec.yaml                  # Dependencies
└── README.md
```

## Setup Instructions

### 1. Prerequisites

- Flutter SDK 3.x installed ([Download](https://flutter.dev/docs/get-started/install))
- Dart 3.x
- IDE: Android Studio, VS Code, or Xcode

### 2. Verify Flutter Setup

```bash
flutter doctor
```

### 3. Get Dependencies

Navigate to the `unipath` folder:

```bash
cd unipath
flutter pub get
```

### 4. Environment Configuration

Create `lib/config/environment.dart`:

```dart
class Environment {
  static const String apiBaseUrl = 'http://localhost:8000/api';
  static const String appName = 'Unipath';
  static const bool isDebug = true;
}
```

### 5. Run Application

#### Android

```bash
flutter run -d emulator-5554
```

#### iOS (macOS only)

```bash
flutter run -d all
```

#### Web

```bash
flutter run -d chrome
```

## Dependencies

Key packages in `pubspec.yaml`:

- **http** - HTTP client
- **provider** - State management (optional)
- **flutter_localizations** - RTL support for Persian
- **intl** - Internationalization

## Code Structure

### Models
Define data structures for User, Course, Chart, etc.

### Screens
Organize screens by feature:
- **Auth:** Login, Registration
- **Dashboard:** Home, Recommendations
- **Chart:** Visual curriculum tree
- **Schedule:** Weekly timetable
- **Profile:** User profile, settings

### Services
API communication layer with backend.

### Widgets
Reusable UI components.

## Features Checklist

- [ ] Authentication (Login/Registration)
- [ ] Dashboard with student info
- [ ] Curriculum Chart visualization
- [ ] Course recommendations
- [ ] Weekly schedule builder
- [ ] Profile management
- [ ] RTL support for Persian
- [ ] Dark mode support
- [ ] Offline capability (local cache)

## Testing

Run unit tests:

```bash
flutter test
```

## Build for Production

### Android APK

```bash
flutter build apk --release
```

### iOS IPA

```bash
flutter build ios --release
```

### Web

```bash
flutter build web --release
```

## Troubleshooting

### Flutter not found
Ensure Flutter SDK is in your PATH:
```bash
flutter --version
```

### Dependencies issues
Clean and reinstall:
```bash
flutter clean
flutter pub get
```

### Android build issues
```bash
flutter clean
cd android
./gradlew clean
```

## Documentation

- [Flutter Docs](https://flutter.dev/docs)
- [Dart API](https://api.dart.dev)
- [Material Design 3](https://m3.material.io/)

## Contributing

Follow Dart style guide and Flutter best practices.
