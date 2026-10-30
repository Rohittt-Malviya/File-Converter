# Build report

Generated during project validation. This report records commands that were actually run; unavailable toolchains are explicitly marked as blocked.

## Repository

- Branch: `feat/offline-file-converter`
- Python: 3.12.3 available
- Node tests and syntax checks: passed before this expansion
- Flutter: not installed in the execution environment
- Pandoc and Tesseract: not detected in the base environment
- PyInstaller: installed in `.venv`

## Build status

| Target | Status |
|---|---|
| Browser app | Available as static files |
| Python conversion engine | Source and tests added |
| PyQt6 desktop | Linux build completed; Qt/X11 runtime libraries may be needed on target systems |
| Android APK/AAB | Blocked: Flutter SDK unavailable |
| iOS | Blocked: requires macOS and Xcode |

Run `scripts/setup.sh` for Python dependencies, then `scripts/run_tests.sh`.
