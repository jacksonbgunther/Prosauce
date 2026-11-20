#!/usr/bin/env bash
# Rebuild index.html and privacy.html from tools/gen_site.py.
# Usage (from repo root):  bash tools/build.sh
set -euo pipefail
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"
python3 tools/gen_site.py "$TMP"
python3 -W ignore tools/build_html.py "$TMP" .
rm -rf "$TMP"
python3 tools/build_theme.py
