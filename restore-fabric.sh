#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ "$#" -ne 1 ]; then
  echo "Usage: ./restore-fabric.sh FABRIC_CODE_OR_FILENAME"
  echo
  echo "Examples:"
  echo "  ./restore-fabric.sh I-440"
  echo "  ./restore-fabric.sh PI-531.jpg"
  exit 1
fi

input="$1"
code="${input%.*}"
archive_dir="archive/out-of-stock"

matches=()
if [ -f "$archive_dir/$input" ]; then
  matches+=("$archive_dir/$input")
else
  while IFS= read -r file; do
    matches+=("$file")
  done < <(find "$archive_dir" -maxdepth 1 -type f \( -iname "${code}.*" \) | sort)
fi

if [ "${#matches[@]}" -eq 0 ]; then
  echo "Could not find archived fabric: $input"
  echo "Check the code and make sure the image is in archive/out-of-stock/."
  exit 1
fi

if [ "${#matches[@]}" -gt 1 ]; then
  echo "More than one matching archived image found:"
  printf '  %s\n' "${matches[@]}"
  echo "Use the full filename instead, for example: ./restore-fabric.sh I-440.jpg"
  exit 1
fi

source_file="${matches[0]}"
filename="$(basename "$source_file")"
target_file="images/$filename"

if [ -e "$target_file" ]; then
  echo "images/ already has $filename"
  echo "Nothing moved. Check images/ before continuing."
  exit 1
fi

mv "$source_file" "$target_file"
echo "Moved $filename back to images/"
echo "This makes it active again on the live website and PDF."

# Clear metres remaining — fabric is back in stock, start fresh
python3 - "$code" <<'PY'
import json, sys
from pathlib import Path
code = sys.argv[1]
tags_path = Path("fabric-tags.json")
if tags_path.exists():
    tags = json.loads(tags_path.read_text(encoding="utf-8"))
    if code in tags and "meters" in tags[code]:
        del tags[code]["meters"]
        tags_path.write_text(json.dumps(dict(sorted(tags.items())), indent=2) + "\n", encoding="utf-8")
        print(f"Cleared metres entry for {code} — fabric is back in stock.")
PY

echo
./update-catalog.sh
