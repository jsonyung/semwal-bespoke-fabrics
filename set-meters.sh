#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ "$#" -lt 2 ]; then
  echo "Usage: ./set-meters.sh FABRIC_CODE METERS"
  echo
  echo "Examples:"
  echo "  ./set-meters.sh I-21 4        # sets 4 metres remaining"
  echo "  ./set-meters.sh I-102 2.5     # decimals are fine"
  echo "  ./set-meters.sh I-21 0        # clears stock (use mark-out-of-stock.sh instead if fully gone)"
  echo
  echo "To set multiple at once:"
  echo "  for code in I-21 I-102 I-129; do ./set-meters.sh \"\$code\" 4; done"
  exit 1
fi

python3 - "$1" "$2" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

code = sys.argv[1].strip().removesuffix(".jpg").removesuffix(".jpeg").removesuffix(".png")
try:
    meters = float(sys.argv[2])
except ValueError:
    raise SystemExit(f"Invalid metres value: {sys.argv[2]}. Use a number like 4 or 2.5")

if meters < 0:
    raise SystemExit("Metres cannot be negative.")

project = Path.cwd()
image_exists = any(
    (project / "images" / f"{code}{suffix}").exists()
    for suffix in [".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"]
)
if not image_exists:
    raise SystemExit(f"Could not find {code} in images/. Check the fabric code.")

tags_path = project / "fabric-tags.json"
tags = json.loads(tags_path.read_text(encoding="utf-8")) if tags_path.exists() else {}
record = tags.get(code, {})

if meters == 0:
    record.pop("meters", None)
    print(f"Cleared metres for {code}.")
else:
    record["meters"] = meters
    print(f"Set {code} → {meters} metres remaining.")

tags[code] = record
tags_path.write_text(json.dumps(dict(sorted(tags.items())), indent=2) + "\n", encoding="utf-8")
print("Now run ./update-catalog.sh to rebuild the website.")
PY
