#!/usr/bin/env bash
set -euo pipefail
cd mobile/converter_mobile
flutter pub get
flutter build apk --release
flutter build appbundle --release
mkdir -p ../../deploy/android/apk ../../deploy/android/appbundle
cp build/app/outputs/flutter-apk/app-release.apk ../../deploy/android/apk/
cp build/app/outputs/bundle/release/app-release.aab ../../deploy/android/appbundle/
