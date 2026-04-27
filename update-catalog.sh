#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PYTHON_BIN="${PYTHON_BIN:-python3}"
LOCAL_BUNDLED_PYTHON="/Users/sbtailor/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
if [ -x "$LOCAL_BUNDLED_PYTHON" ]; then
  PYTHON_BIN="$LOCAL_BUNDLED_PYTHON"
fi

echo "Semwal Bespoke Fabrics catalog updater"
echo

image_count="$(find images -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' -o -iname '*.heic' -o -iname '*.tif' -o -iname '*.tiff' \) | wc -l | tr -d ' ')"
echo "Found ${image_count} fabric images in images/"
if [ -d "archive/out-of-stock" ]; then
  archived_count="$(find archive/out-of-stock -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' -o -iname '*.heic' -o -iname '*.tif' -o -iname '*.tiff' \) | wc -l | tr -d ' ')"
  echo "Found ${archived_count} archived out-of-stock images."
fi
echo

echo "Analyzing fabric colors and patterns..."
"$PYTHON_BIN" scripts/analyze_fabric_tags.py

echo "Regenerating searchable catalog files..."
"$PYTHON_BIN" scripts/generate_catalog.py

echo "Regenerating PDF catalog..."
"$PYTHON_BIN" scripts/generate_pdf_catalog.py

echo
echo "Current changes:"
git status --short
echo

if git diff --quiet && git diff --cached --quiet; then
  echo "No catalog changes to commit."
  exit 0
fi

if [ ! -t 0 ]; then
  echo "Changes were generated but not committed or pushed because this is not an interactive terminal."
  echo "Run ./update-catalog.sh in Terminal to approve commit and push, or commit manually."
  exit 0
fi

read -r -p "Commit and push these catalog changes now? [y/N] " answer
case "$answer" in
  y|Y|yes|YES)
    git add .
    git commit -m "Update fabric catalog"
    git push
    echo
    echo "Catalog updated and pushed to GitHub."
    ;;
  *)
    echo "Changes were generated but not committed or pushed."
    ;;
esac
