#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ "$#" -lt 2 ]; then
  echo "Usage: ./tag-fabric.sh FABRIC_CODE key=value key=value"
  echo
  echo "Examples:"
  echo "  ./tag-fabric.sh I-440 colors=white,blue patterns=stripes styles=formal,light"
  echo "  ./tag-fabric.sh PI-531 colors=navy patterns=checks styles=premium,formal,dark"
  echo
  echo "Allowed keys: colors, patterns, uses, styles"
  exit 1
fi

python3 - "$@" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

allowed = {"colors", "patterns", "uses", "styles"}
code = sys.argv[1].strip().removesuffix(".jpg").removesuffix(".jpeg").removesuffix(".png")
updates: dict[str, list[str]] = {}

for arg in sys.argv[2:]:
    if "=" not in arg:
        raise SystemExit(f"Invalid tag argument: {arg}")
    key, value = arg.split("=", 1)
    key = key.strip().lower()
    if key not in allowed:
        raise SystemExit(f"Invalid key: {key}. Allowed keys: {', '.join(sorted(allowed))}")
    values = [item.strip().lower() for item in value.split(",") if item.strip()]
    if not values:
        raise SystemExit(f"No values provided for {key}")
    updates[key] = list(dict.fromkeys(values))

project = Path.cwd()
image_exists = any((project / "images" / f"{code}{suffix}").exists() for suffix in [".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"])
if not image_exists:
    raise SystemExit(f"Could not find {code} in images/. Check the fabric code.")

tags_path = project / "fabric-tags.json"
tags = json.loads(tags_path.read_text(encoding="utf-8")) if tags_path.exists() else {}
record = tags.get(code, {})
for key in allowed:
    record.setdefault(key, [])
record.update(updates)
record["tags"] = list(dict.fromkeys([*record["colors"], *record["patterns"], *record["uses"], *record["styles"]]))
record["source"] = "manual"
tags[code] = record
tags_path.write_text(json.dumps(dict(sorted(tags.items())), indent=2) + "\n", encoding="utf-8")
print(f"Updated tags for {code}: {', '.join(record['tags'])}")
print("Now run ./update-catalog.sh to rebuild the website and PDF.")
PY
