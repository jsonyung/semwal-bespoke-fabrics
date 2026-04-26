from __future__ import annotations

import json
import tempfile
from datetime import date
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / "catalog-data.json"
OUTPUT_FILE = PROJECT_DIR / "semwal-bespoke-fabrics-catalog.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 15 * mm
MARGIN_TOP = 18 * mm
MARGIN_BOTTOM = 15 * mm
BRAND = "Semwal Bespoke Fabrics"
ACCENT = colors.HexColor("#166F67")
WARM = colors.HexColor("#8C3F2F")
INK = colors.HexColor("#181716")
MUTED = colors.HexColor("#6B655F")
LINE = colors.HexColor("#DED8D0")
PAPER = colors.HexColor("#FBFAF7")


def load_records() -> list[dict[str, str]]:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def draw_page_background(pdf: canvas.Canvas) -> None:
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)


def draw_cover(pdf: canvas.Canvas, records: list[dict[str, str]], temp_dir: Path) -> None:
    draw_page_background(pdf)
    pdf.setFillColor(ACCENT)
    pdf.rect(0, PAGE_HEIGHT - 76 * mm, PAGE_WIDTH, 76 * mm, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 36 * mm, "Semwal Bespoke")
    pdf.setFont("Helvetica", 22)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 49 * mm, "Fabrics Catalog")

    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 98 * mm, f"{len(records)} searchable fabric swatches")
    pdf.setFont("Helvetica", 11)
    pdf.setFillColor(MUTED)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 108 * mm, "Use fabric codes to find images in the PDF, GitHub catalog, or web search page.")

    samples = records[:6]
    start_x = MARGIN_X
    start_y = PAGE_HEIGHT - 186 * mm
    box = 27 * mm
    gap = 5 * mm
    for index, record in enumerate(samples):
        x = start_x + index * (box + gap)
        draw_image_box(pdf, PROJECT_DIR / record["image"], temp_dir, x, start_y, box, box)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.setFillColor(INK)
        pdf.drawCentredString(x + box / 2, start_y - 5 * mm, record["code"])

    pdf.setFillColor(WARM)
    pdf.rect(MARGIN_X, 42 * mm, 54 * mm, 1.2 * mm, stroke=0, fill=1)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(MARGIN_X, 31 * mm, f"Generated {date.today().isoformat()}")
    pdf.drawString(MARGIN_X, 25 * mm, "Catalog source: image code filenames")
    pdf.showPage()


def draw_header(pdf: canvas.Canvas, title: str, page_label: str) -> None:
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 12 * mm, title)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 12 * mm, page_label)
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.5)
    pdf.line(MARGIN_X, PAGE_HEIGHT - 16 * mm, PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 16 * mm)


def prepared_image(image_path: Path, temp_dir: Path, max_px: int = 900) -> Path:
    output_path = temp_dir / f"{image_path.stem}.jpg"
    if output_path.exists():
        return output_path

    with Image.open(image_path) as image:
        image = image.convert("RGB")
        image.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
        image.save(output_path, "JPEG", quality=78, optimize=True)
    return output_path


def draw_image_box(
    pdf: canvas.Canvas,
    image_path: Path,
    temp_dir: Path,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    pdf.setFillColor(colors.white)
    pdf.roundRect(x, y, width, height, 4, stroke=0, fill=1)
    pdf.setStrokeColor(LINE)
    pdf.roundRect(x, y, width, height, 4, stroke=1, fill=0)

    preview_path = prepared_image(image_path, temp_dir)
    with Image.open(preview_path) as image:
        image_width, image_height = image.size
    scale = min((width - 3 * mm) / image_width, (height - 3 * mm) / image_height)
    draw_width = image_width * scale
    draw_height = image_height * scale
    draw_x = x + (width - draw_width) / 2
    draw_y = y + (height - draw_height) / 2
    pdf.drawImage(
        str(preview_path),
        draw_x,
        draw_y,
        width=draw_width,
        height=draw_height,
        preserveAspectRatio=True,
        mask="auto",
    )


def draw_catalog_pages(pdf: canvas.Canvas, records: list[dict[str, str]], temp_dir: Path) -> None:
    columns = 3
    rows = 3
    gap_x = 7 * mm
    gap_y = 11 * mm
    card_w = (PAGE_WIDTH - 2 * MARGIN_X - gap_x * (columns - 1)) / columns
    card_h = 72 * mm
    image_h = 58 * mm
    start_y = PAGE_HEIGHT - MARGIN_TOP - 16 * mm - card_h

    for page_index, offset in enumerate(range(0, len(records), columns * rows), start=1):
        draw_page_background(pdf)
        draw_header(pdf, BRAND, f"Catalog page {page_index}")
        page_records = records[offset : offset + columns * rows]
        for item_index, record in enumerate(page_records):
            row = item_index // columns
            col = item_index % columns
            x = MARGIN_X + col * (card_w + gap_x)
            y = start_y - row * (card_h + gap_y)
            draw_image_box(pdf, PROJECT_DIR / record["image"], temp_dir, x, y + 11 * mm, card_w, image_h)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(x, y + 4 * mm, record["code"])
            pdf.setFillColor(MUTED)
            pdf.setFont("Helvetica", 7)
            pdf.drawRightString(x + card_w, y + 4.2 * mm, record["type"])
        pdf.showPage()


def draw_index(pdf: canvas.Canvas, records: list[dict[str, str]]) -> None:
    draw_page_background(pdf)
    draw_header(pdf, "Fabric Code Index", "Search reference")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 25 * mm, "All codes included in this PDF catalog.")

    columns = 5
    col_w = (PAGE_WIDTH - 2 * MARGIN_X) / columns
    x_positions = [MARGIN_X + col_w * index for index in range(columns)]
    y = PAGE_HEIGHT - 38 * mm
    line_h = 5.2 * mm
    per_col = int((PAGE_HEIGHT - 54 * mm) // line_h)
    pdf.setFont("Helvetica", 8)
    pdf.setFillColor(INK)
    for index, record in enumerate(records):
        col = index // per_col
        if col >= columns:
            break
        row = index % per_col
        pdf.drawString(x_positions[col], y - row * line_h, record["code"])
    pdf.showPage()


def main() -> None:
    records = load_records()
    with tempfile.TemporaryDirectory() as temp:
        temp_dir = Path(temp)
        pdf = canvas.Canvas(str(OUTPUT_FILE), pagesize=A4)
        pdf.setTitle(BRAND)
        pdf.setAuthor("Semwal Bespoke")
        draw_cover(pdf, records, temp_dir)
        draw_catalog_pages(pdf, records, temp_dir)
        draw_index(pdf, records)
        pdf.save()
    print(f"Generated {OUTPUT_FILE.name} with {len(records)} fabrics.")


if __name__ == "__main__":
    main()
