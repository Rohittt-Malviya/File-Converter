# Converter Mobile

Flutter companion app for Local Convert. It supports local conversion between
TXT, Markdown, CSV, JSON, PNG, JPEG, and WebP files. Converted files are
written to the device temporary directory and opened with the native share
sheet; file contents are never uploaded.

## Run

Install Flutter, then run:

```sh
flutter pub get
flutter test
flutter run
```

This repository includes the app source and platform entry/configuration files.
The remaining generated Flutter wrapper files can be regenerated with
`flutter create .` from this directory when Flutter is available.
