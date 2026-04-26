from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image


PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = PROJECT_DIR / "images"
THUMB_DIR = PROJECT_DIR / "thumbs"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"}


def natural_key(path: Path) -> tuple[str, int, str]:
    match = re.match(r"^([A-Za-z]+)-(\d+)", path.stem)
    if not match:
        return (path.stem, 0, path.suffix.lower())
    prefix, number = match.groups()
    return (prefix.upper(), int(number), path.suffix.lower())


def fabric_type(code: str) -> str:
    if code.startswith("PI-"):
        return "Premium / PI"
    if code.startswith("I-"):
        return "Fabric"
    return "Uncategorized"


def create_thumbnail(source: Path, code: str) -> str:
    THUMB_DIR.mkdir(exist_ok=True)
    output = THUMB_DIR / f"{code}.jpg"
    if output.exists() and output.stat().st_mtime >= source.stat().st_mtime:
        return f"thumbs/{output.name}"

    with Image.open(source) as image:
        image = image.convert("RGB")
        image.thumbnail((420, 420), Image.Resampling.LANCZOS)
        image.save(output, "JPEG", quality=72, optimize=True, progressive=True)
    return f"thumbs/{output.name}"


def build_records() -> list[dict[str, str]]:
    files = [
        path
        for path in IMAGE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    records = []
    for path in sorted(files, key=natural_key):
        code = path.stem
        thumb = create_thumbnail(path, code)
        records.append(
            {
                "code": code,
                "type": fabric_type(code),
                "image": f"images/{path.name}",
                "thumb": thumb,
                "filename": path.name,
            }
        )
    return records


def write_json(records: list[dict[str, str]]) -> None:
    output = PROJECT_DIR / "catalog-data.json"
    output.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")


def write_catalog_md(records: list[dict[str, str]]) -> None:
    lines = [
        "# Semwal Bespoke Fabrics Catalog",
        "",
        f"Total fabrics: **{len(records)}**",
        "",
        "Use `Cmd+F` / `Ctrl+F` to search a fabric code like `I-440` or `PI-531`.",
        "",
        "| Code | Type | Preview | File |",
        "|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            f"| `{record['code']}` | {record['type']} | "
            f"[![{record['code']}]({record['thumb']})]({record['image']}) | "
            f"[{record['filename']}]({record['image']}) |"
        )
    lines.append("")
    (PROJECT_DIR / "CATALOG.md").write_text("\n".join(lines), encoding="utf-8")


def write_readme(records: list[dict[str, str]]) -> None:
    prefixes: dict[str, list[int]] = {}
    for record in records:
        match = re.match(r"^([A-Za-z]+)-(\d+)$", record["code"])
        if match:
            prefix, number = match.groups()
            prefixes.setdefault(prefix.upper(), []).append(int(number))

    summary_lines = []
    for prefix in sorted(prefixes):
        numbers = sorted(prefixes[prefix])
        summary_lines.append(
            f"- `{prefix}` series: {len(numbers)} fabrics, from `{prefix}-{numbers[0]}` to `{prefix}-{numbers[-1]}`"
        )

    lines = [
        "# Semwal Bespoke Fabrics",
        "",
        "A searchable fabric catalog for Semwal Bespoke.",
        "",
        "## What is inside",
        "",
        f"- Total fabric images: **{len(records)}**",
        "- PDF catalog: [semwal-bespoke-fabrics-catalog.pdf](semwal-bespoke-fabrics-catalog.pdf)",
        "- Searchable Markdown catalog: [CATALOG.md](CATALOG.md)",
        "- Browser search catalog: [index.html](index.html)",
        "- Machine-readable data: [catalog-data.json](catalog-data.json)",
        "- Web thumbnails: [thumbs/](thumbs/)",
        "",
        "## Code summary",
        "",
        *summary_lines,
        "",
        "## How to search",
        "",
        "- On GitHub, open `CATALOG.md` and use browser search for a code like `I-440`.",
        "- On GitHub Pages, open `index.html` and use the search box.",
        "",
        "## Adding more fabrics",
        "",
        "1. Add new fabric images into `images/` using code filenames such as `I-463.jpg`.",
        "2. Run `./update-catalog.sh`.",
        "3. Confirm the commit and push when asked.",
        "",
    ]
    (PROJECT_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    records = build_records()
    write_json(records)
    write_catalog_md(records)
    write_readme(records)
    print(f"Generated catalog for {len(records)} fabrics.")


if __name__ == "__main__":
    main()
