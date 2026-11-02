#!/usr/bin/env bash
set -euo pipefail
. .venv/bin/activate
pyinstaller --noconfirm --clean --name LocalConvert --windowed --paths . desktop/frontend/main.py
mkdir -p deploy/desktop/"$(uname -s | tr '[:upper:]' '[:lower:]')"
cp -r dist/LocalConvert* deploy/desktop/"$(uname -s | tr '[:upper:]' '[:lower:]')"/
