from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image


PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = PROJECT_DIR / "images"
ARCHIVE_DIR = PROJECT_DIR / "archive" / "out-of-stock"
THUMB_DIR = PROJECT_DIR / "thumbs"
ARCHIVE_THUMB_DIR = THUMB_DIR / "archive"
TAGS_FILE = PROJECT_DIR / "fabric-tags.json"
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


def create_thumbnail(source: Path, code: str, target_dir: Path = THUMB_DIR, rel_prefix: str = "thumbs") -> str:
    target_dir.mkdir(parents=True, exist_ok=True)
    output = target_dir / f"{code}.jpg"
    if output.exists() and output.stat().st_mtime >= source.stat().st_mtime:
        return f"{rel_prefix}/{output.name}"

    with Image.open(source) as image:
        image = image.convert("RGB")
        image.thumbnail((420, 420), Image.Resampling.LANCZOS)
        image.save(output, "JPEG", quality=72, optimize=True, progressive=True)
    return f"{rel_prefix}/{output.name}"


def load_fabric_tags() -> dict[str, dict[str, list[str]]]:
    if not TAGS_FILE.exists():
        return {}
    return json.loads(TAGS_FILE.read_text(encoding="utf-8"))


def default_tags(code: str) -> dict[str, list[str]]:
    styles = ["shirt", "formal"]
    if code.startswith("PI-"):
        styles.append("premium")
    return {
        "colors": [],
        "patterns": [],
        "uses": ["shirt"],
        "styles": styles,
        "tags": styles,
    }


def clean_tag_list(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    cleaned = []
    for value in values:
        if isinstance(value, str) and value.strip():
            cleaned.append(value.strip().lower())
    return list(dict.fromkeys(cleaned))


def tags_for_code(code: str, fabric_tags: dict[str, dict[str, list[str]]]) -> dict[str, list[str]]:
    raw = fabric_tags.get(code, {})
    merged = default_tags(code)
    for key in ("colors", "patterns", "uses", "styles"):
        values = clean_tag_list(raw.get(key))
        if values:
            merged[key] = values
    merged["tags"] = list(dict.fromkeys([*merged["colors"], *merged["patterns"], *merged["uses"], *merged["styles"]]))
    # Pass through metres-remaining if set
    if "meters" in raw:
        try:
            merged["meters"] = float(raw["meters"])
        except (TypeError, ValueError):
            pass
    return merged


def build_records() -> list[dict[str, object]]:
    fabric_tags = load_fabric_tags()
    files = [
        path
        for path in IMAGE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    records = []
    for path in sorted(files, key=natural_key):
        code = path.stem
        thumb = create_thumbnail(path, code)
        tags = tags_for_code(code, fabric_tags)
        records.append(
            {
                "code": code,
                "type": fabric_type(code),
                "image": f"images/{path.name}",
                "thumb": thumb,
                "filename": path.name,
                **tags,
            }
        )
    return records


def build_archive_records() -> list[dict[str, object]]:
    if not ARCHIVE_DIR.exists():
        return []
    fabric_tags = load_fabric_tags()
    files = [
        path
        for path in ARCHIVE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    records = []
    for path in sorted(files, key=natural_key):
        code = path.stem
        thumb = create_thumbnail(path, code, target_dir=ARCHIVE_THUMB_DIR, rel_prefix="thumbs/archive")
        tags = tags_for_code(code, fabric_tags)
        records.append(
            {
                "code": code,
                "type": fabric_type(code),
                "image": f"archive/out-of-stock/{path.name}",
                "thumb": thumb,
                "filename": path.name,
                "status": "out-of-stock",
                **tags,
            }
        )
    return records


def cleanup_thumbnails(records: list[dict[str, object]], archive_records: list[dict[str, object]] | None = None) -> None:
    if THUMB_DIR.exists():
        active = {Path(record["thumb"]).name for record in records}
        for thumb in THUMB_DIR.glob("*.jpg"):
            if thumb.name not in active:
                thumb.unlink()

    if ARCHIVE_THUMB_DIR.exists() and archive_records is not None:
        active_arch = {Path(record["thumb"]).name for record in archive_records}
        for thumb in ARCHIVE_THUMB_DIR.glob("*.jpg"):
            if thumb.name not in active_arch:
                thumb.unlink()


def write_json(records: list[dict[str, object]]) -> None:
    output = PROJECT_DIR / "catalog-data.json"
    output.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")


def write_archive_json(records: list[dict[str, object]]) -> None:
    output = PROJECT_DIR / "archive-data.json"
    output.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")


def display_tags(record: dict[str, object]) -> str:
    tags = []
    for key in ("colors", "patterns", "styles"):
        values = record.get(key, [])
        if isinstance(values, list):
            tags.extend(str(value).title() for value in values[:3])
    return ", ".join(list(dict.fromkeys(tags)))


def write_catalog_md(records: list[dict[str, object]]) -> None:
    lines = [
        "# Semwal Bespoke Fabrics Catalog",
        "",
        f"Total fabrics: **{len(records)}**",
        "",
        "Use `Cmd+F` / `Ctrl+F` to search a fabric code like `I-440` or `PI-531`.",
        "",
        "| Code | Type | Tags | Preview | File |",
        "|---|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            f"| `{record['code']}` | {record['type']} | "
            f"{display_tags(record)} | "
            f"[![{record['code']}]({record['thumb']})]({record['image']}) | "
            f"[{record['filename']}]({record['image']}) |"
        )
    lines.append("")
    (PROJECT_DIR / "CATALOG.md").write_text("\n".join(lines), encoding="utf-8")


def write_readme(records: list[dict[str, object]]) -> None:
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
        "- Website stock guide: [stock-guide.html](stock-guide.html)",
        "- PDF catalog: [semwal-bespoke-fabrics-catalog.pdf](semwal-bespoke-fabrics-catalog.pdf)",
        "- GitHub searchable catalog: [CATALOG.md](CATALOG.md)",
        "- Complete office guide: [OFFICE_GUIDE.md](OFFICE_GUIDE.md)",
        "- Stock workflow guide: [STOCK_WORKFLOW.md](STOCK_WORKFLOW.md)",
        "- Fabric tagging guide: [FABRIC_TAGGING.md](FABRIC_TAGGING.md)",
        "",
        "## What is inside",
        "",
        f"- Total fabric images: **{len(records)}**",
        "- PDF catalog: [semwal-bespoke-fabrics-catalog.pdf](semwal-bespoke-fabrics-catalog.pdf)",
        "- Searchable Markdown catalog: [CATALOG.md](CATALOG.md)",
        "- Browser search catalog: [index.html](index.html)",
        "- Website stock guide: [stock-guide.html](stock-guide.html)",
        "- Machine-readable data: [catalog-data.json](catalog-data.json)",
        "- Web thumbnails: [thumbs/](thumbs/)",
        "- Editable fabric tags: [fabric-tags.json](fabric-tags.json)",
        "- Tag helper command: [tag-fabric.sh](tag-fabric.sh)",
        "- Fabric tag review board: [fabric-tag-review.html](fabric-tag-review.html)",
        "",
        "## Code summary",
        "",
        *summary_lines,
        "",
        "## How to search",
        "",
        "- Best option: open the live website and type a fabric code like `I-440`.",
        "- Use website filter buttons for color, pattern, and style.",
        "- On GitHub, open `CATALOG.md` and use browser search with `Ctrl+F` or `Cmd+F`.",
        "- In the PDF, use PDF search with `Ctrl+F` or `Cmd+F`.",
        "",
        "## Website Filters",
        "",
        "The website supports filters for:",
        "",
        "- Series: `I`, `PI`",
        "- Pattern: `Solid`, `Checks`, `Stripes`, `Printed`, `Texture`",
        "- Color: `White`, `Blue`, `Black`, `Grey`, `Cream`, `Beige`, `Navy`, and more",
        "- Style: `Formal`, `Casual`, `Premium`, `Light`, `Dark`",
        "",
        "Filter data comes from `fabric-tags.json`. It is auto-generated first, then can be corrected by hand when someone reviews fabrics.",
        "",
        "To correct tags for one fabric, run:",
        "",
        "```bash",
        "./tag-fabric.sh I-440 colors=white,blue patterns=stripes styles=formal,light",
        "```",
        "",
        "Then run `./update-catalog.sh`. Manual tags are preserved by future auto-analysis. See [FABRIC_TAGGING.md](FABRIC_TAGGING.md).",
        "",
        "To review all fabrics visually, run:",
        "",
        "```bash",
        "python3 scripts/generate_tag_review.py",
        "```",
        "",
        "Then open `fabric-tag-review.html`.",
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
        "- Merge tags from `fabric-tags.json` into the website.",
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
        "Run:",
        "",
        "```bash",
        "./mark-out-of-stock.sh I-440",
        "```",
        "",
        "Use the real fabric code. You can also use the full filename:",
        "",
        "```bash",
        "./mark-out-of-stock.sh I-440.jpg",
        "```",
        "",
        "That fabric will be removed from the website, PDF, `CATALOG.md`, and `catalog-data.json`, but the photo is safely kept in the archive.",
        "",
        "### Back In Stock",
        "",
        "Run:",
        "",
        "```bash",
        "./restore-fabric.sh I-440",
        "```",
        "",
        "That fabric will return to the website, PDF, `CATALOG.md`, and `catalog-data.json`.",
        "",
        "### Permanently Remove",
        "",
        "Delete the fabric image from `images/`, then run `./update-catalog.sh`.",
        "",
        "The updater also removes old unused thumbnails.",
        "",
        "For normal office use, prefer `./mark-out-of-stock.sh CODE` instead of deleting. The full step-by-step guide is in [STOCK_WORKFLOW.md](STOCK_WORKFLOW.md).",
        "",
        "## GitHub Private Repository Note",
        "",
        "If this repository is on GitHub Free and you make it private, the GitHub Pages website will be unpublished.",
        "",
        "Best options:",
        "",
        "- Keep this repo public if the website must stay live on GitHub Pages.",
        "- Use GitHub Pro/paid plan if you want Pages from a private repo.",
        "- Later, split into two repos: one private working repo and one public website-only repo.",
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
    archive_records = build_archive_records()
    cleanup_thumbnails(records, archive_records)
    write_json(records)
    write_archive_json(archive_records)
    write_catalog_md(records)
    write_readme(records)
    print(f"Generated catalog for {len(records)} active fabrics and {len(archive_records)} archived fabrics.")


if __name__ == "__main__":
    main()
