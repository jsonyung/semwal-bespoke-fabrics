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


def cleanup_thumbnails(records: list[dict[str, str]]) -> None:
    if not THUMB_DIR.exists():
        return
    active = {Path(record["thumb"]).name for record in records}
    for thumb in THUMB_DIR.glob("*.jpg"):
        if thumb.name not in active:
            thumb.unlink()


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
        "## Open Catalog",
        "",
        "- Live searchable website: [https://jsonyung.github.io/semwal-bespoke-fabrics/](https://jsonyung.github.io/semwal-bespoke-fabrics/)",
        "- PDF catalog: [semwal-bespoke-fabrics-catalog.pdf](semwal-bespoke-fabrics-catalog.pdf)",
        "- GitHub searchable catalog: [CATALOG.md](CATALOG.md)",
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
        "- Best option: open the live website and type a fabric code like `I-440`.",
        "- On GitHub, open `CATALOG.md` and use browser search with `Ctrl+F` or `Cmd+F`.",
        "- In the PDF, use PDF search with `Ctrl+F` or `Cmd+F`.",
        "",
        "## Easy Update For New Fabrics",
        "",
        "Use this when a new fabric photo needs to be added.",
        "",
        "### 1. Add The Image",
        "",
        "Put the new fabric image inside the `images/` folder.",
        "",
        "Name the file with the fabric code:",
        "",
        "```text",
        "I-463.jpg",
        "I-464.jpg",
        "PI-532.jpg",
        "```",
        "",
        "Rules:",
        "",
        "- Use the fabric code as the filename.",
        "- Keep the extension like `.jpg` or `.png`.",
        "- Do not use spaces in the filename.",
        "- Do not rename old files unless the fabric code is wrong.",
        "",
        "### 2. Run One Command",
        "",
        "Open Terminal inside this project folder and run:",
        "",
        "```bash",
        "./update-catalog.sh",
        "```",
        "",
        "The updater will:",
        "",
        "- Count all active fabric images.",
        "- Count archived out-of-stock images.",
        "- Update `CATALOG.md`.",
        "- Update `catalog-data.json`.",
        "- Update website thumbnails in `thumbs/` and remove unused thumbnails.",
        "- Regenerate the PDF catalog.",
        "- Show what changed.",
        "- Ask before committing and pushing to GitHub.",
        "",
        "When it asks:",
        "",
        "```text",
        "Commit and push these catalog changes now? [y/N]",
        "```",
        "",
        "Type `y`, then press Enter.",
        "",
        "### 3. What Updates Online",
        "",
        "After pushing, GitHub updates:",
        "",
        "- Live website search",
        "- GitHub catalog",
        "- PDF catalog",
        "- Image thumbnails",
        "",
        "GitHub Pages can take a few minutes to refresh. If the website looks old, do a hard refresh with `Cmd+Shift+R` on Mac or `Ctrl+Shift+R` on Windows.",
        "",
        "## Out Of Stock Or Removed Fabrics",
        "",
        "Use this when a fabric should disappear from the live website and PDF catalog.",
        "",
        "### Temporarily Out Of Stock",
        "",
        "1. Move the fabric image from `images/` to `archive/out-of-stock/`.",
        "2. Keep the same filename, for example `I-440.jpg`.",
        "3. Run `./update-catalog.sh`.",
        "4. Type `y` when asked to commit and push.",
        "",
        "That fabric will be removed from the website, PDF, `CATALOG.md`, and `catalog-data.json`, but the photo is safely kept in the archive.",
        "",
        "### Back In Stock",
        "",
        "1. Move the image from `archive/out-of-stock/` back to `images/`.",
        "2. Run `./update-catalog.sh`.",
        "3. Type `y` when asked to commit and push.",
        "",
        "### Permanently Remove",
        "",
        "Delete the fabric image from `images/`, then run `./update-catalog.sh`.",
        "",
        "The updater also removes old unused thumbnails.",
        "",
        "## PDF Generation",
        "",
        "The PDF is generated automatically by:",
        "",
        "```bash",
        "python3 scripts/generate_pdf_catalog.py",
        "```",
        "",
        "Normally, do not run this alone. Use:",
        "",
        "```bash",
        "./update-catalog.sh",
        "```",
        "",
        "That updates the PDF plus the website/catalog files together.",
        "",
        "## Moving Or Sharing This Project",
        "",
        "Move the whole `semwal-bespoke-fabrics` folder together. The website needs these files to stay together:",
        "",
        "- `index.html`",
        "- `catalog-data.json`",
        "- `images/`",
        "- `thumbs/`",
        "- `assets/`",
        "",
        "For another office computer, download the repository ZIP from GitHub, unzip it, and keep the folder together.",
        "",
    ]
    (PROJECT_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    records = build_records()
    cleanup_thumbnails(records)
    write_json(records)
    write_catalog_md(records)
    write_readme(records)
    print(f"Generated catalog for {len(records)} fabrics.")


if __name__ == "__main__":
    main()
