#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ "$#" -ne 1 ]; then
  echo "Usage: ./mark-out-of-stock.sh FABRIC_CODE_OR_FILENAME"
  echo
  echo "Examples:"
  echo "  ./mark-out-of-stock.sh I-440"
  echo "  ./mark-out-of-stock.sh PI-531.jpg"
  exit 1
fi

input="$1"
code="${input%.*}"
archive_dir="archive/out-of-stock"
mkdir -p "$archive_dir"

matches=()
if [ -f "images/$input" ]; then
  matches+=("images/$input")
else
  while IFS= read -r file; do
    matches+=("$file")
  done < <(find images -maxdepth 1 -type f \( -iname "${code}.*" \) | sort)
fi

if [ "${#matches[@]}" -eq 0 ]; then
  echo "Could not find active fabric: $input"
  echo "Check the code and make sure the image is in images/."
  exit 1
fi

if [ "${#matches[@]}" -gt 1 ]; then
  echo "More than one matching image found:"
  printf '  %s\n' "${matches[@]}"
  echo "Use the full filename instead, for example: ./mark-out-of-stock.sh I-440.jpg"
  exit 1
fi

source_file="${matches[0]}"
filename="$(basename "$source_file")"
target_file="$archive_dir/$filename"

if [ -e "$target_file" ]; then
  echo "Archive already has $filename"
  echo "Nothing moved. Check archive/out-of-stock/ before continuing."
  exit 1
fi

mv "$source_file" "$target_file"
echo "Moved $filename to archive/out-of-stock/"
echo "This hides it from the live website and PDF, but keeps the photo safe."
echo
./update-catalog.sh
