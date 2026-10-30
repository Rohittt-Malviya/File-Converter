#!/usr/bin/env bash
set -euo pipefail
python3 -m pytest -q
npm test
if command -v flutter >/dev/null 2>&1; then
  (cd mobile/converter_mobile && flutter test && flutter analyze)
else
  echo "Flutter not installed; Flutter tests/analyzer not run." >&2
fi
