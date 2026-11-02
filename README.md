# Offline File Converter

Offline File Converter is a privacy-first conversion toolkit with a zero-dependency browser app, a reusable Python engine, a PyQt6 desktop client, and a Flutter mobile client. Source files are processed locally and are never uploaded.

## Features

- Browser conversion for text-family and image-family formats
- Python conversion engine for PDF, images, documents, spreadsheets, and text
- PyQt6 desktop dashboard with drag-and-drop, progress, history, themes, and safe output selection
- Flutter mobile project for local file selection, image/PDF workflows, sharing, and history
- Unit tests, CI, packaging scripts, and deployment documentation

## Supported formats

The browser app supports TXT, Markdown, CSV, JSON, PNG, JPEG, and WebP. The Python engine additionally supports BMP, TIFF, PDF, DOCX, XLSX, and HTML workflows. See `docs/CONVERSION_SUPPORT.md` for optional dependencies and limitations.

## Run

### Browser

```sh
python3 -m http.server 8080
```

Open `http://localhost:8080`.

### Desktop

```sh
./scripts/setup.sh
python -m desktop.frontend.main
```

On Windows, use `scripts/setup.bat` and `python -m desktop.frontend.main`.

### Mobile

Install Flutter, then:

```sh
cd mobile/converter_mobile
flutter pub get
flutter run
```

## Test and build

```sh
python -m pytest -q
npm test
npm run check
```

Use `scripts/build_desktop.sh` or `.bat` for PyInstaller packaging and `scripts/build_mobile.sh` for Android APK/AAB builds. iOS requires macOS and Xcode.

## Offline and security model

No cloud conversion APIs are used. Applications do not execute input files, preserve source files, reject unsupported encrypted PDFs, avoid silent overwrites, and cleanly report missing optional tooling. See `docs/SECURITY.md`.

## Known limitations

Flutter and platform packaging require their native SDKs. High-fidelity DOCX/PDF and OCR workflows depend on optional local tools. iOS artifacts cannot be produced on Linux.
