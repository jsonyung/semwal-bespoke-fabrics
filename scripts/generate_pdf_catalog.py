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
LOGO_FILE = PROJECT_DIR / "assets" / "semwal-logo.png"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 15 * mm
MARGIN_TOP = 18 * mm
MARGIN_BOTTOM = 15 * mm
BRAND = "Semwal Bespoke Fabrics"
ACCENT = colors.HexColor("#3F51B5")
WARM = colors.HexColor("#1E88E5")
INK = colors.HexColor("#1B1E28")
MUTED = colors.HexColor("#5A6072")
LINE = colors.HexColor("#D8DCE8")
PAPER = colors.HexColor("#F6F7FB")
PANEL = colors.white


def load_records() -> list[dict[str, str]]:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def draw_page_background(pdf: canvas.Canvas) -> None:
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)


def draw_cover(pdf: canvas.Canvas, records: list[dict[str, str]], temp_dir: Path) -> None:
    draw_page_background(pdf)
    pdf.setFillColor(ACCENT)
    pdf.rect(0, PAGE_HEIGHT - 90 * mm, PAGE_WIDTH, 90 * mm, stroke=0, fill=1)
    if LOGO_FILE.exists():
        logo_size = 34 * mm
        pdf.drawImage(
            str(LOGO_FILE),
            PAGE_WIDTH - MARGIN_X - logo_size,
            PAGE_HEIGHT - 53 * mm,
            width=logo_size,
            height=logo_size,
            preserveAspectRatio=True,
            mask="auto",
        )
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 31)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 34 * mm, "Semwal Bespoke")
    pdf.setFont("Helvetica", 23)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 48 * mm, "Premium Fabrics Catalog")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 61 * mm, "Curated fabric swatches for bespoke tailoring selection")

    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 112 * mm, f"{len(records)} fabric swatches")
    pdf.setFont("Helvetica", 11)
    pdf.setFillColor(MUTED)
    pdf.drawString(MARGIN_X, PAGE_HEIGHT - 122 * mm, "Search by fabric code in the PDF or online catalog.")

    pdf.setFillColor(colors.white)
    pdf.roundRect(MARGIN_X, PAGE_HEIGHT - 157 * mm, PAGE_WIDTH - 2 * MARGIN_X, 20 * mm, 4, stroke=0, fill=1)
    pdf.setStrokeColor(LINE)
    pdf.roundRect(MARGIN_X, PAGE_HEIGHT - 157 * mm, PAGE_WIDTH - 2 * MARGIN_X, 20 * mm, 4, stroke=1, fill=0)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(MARGIN_X + 6 * mm, PAGE_HEIGHT - 146 * mm, "Online catalog")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(MARGIN_X + 42 * mm, PAGE_HEIGHT - 146 * mm, "https://jsonyung.github.io/semwal-bespoke-fabrics/")

    samples = records[:8]
    start_x = MARGIN_X
    start_y = PAGE_HEIGHT - 210 * mm
    box = 21 * mm
    gap = 4 * mm
    for index, record in enumerate(samples):
        x = start_x + index * (box + gap)
        draw_image_box(pdf, PROJECT_DIR / record["image"], temp_dir, x, start_y, box, box)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.setFillColor(INK)
        pdf.drawCentredString(x + box / 2, start_y - 5 * mm, record["code"])

    pdf.setFillColor(ACCENT)
    pdf.rect(MARGIN_X, 41 * mm, 58 * mm, 1.2 * mm, stroke=0, fill=1)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(MARGIN_X, 30 * mm, f"Updated {date.today().isoformat()}")
    pdf.drawString(MARGIN_X, 24 * mm, "Semwal Bespoke Fabrics | Fabric code reference catalog")
    pdf.showPage()


def draw_header(pdf: canvas.Canvas, title: str, page_label: str) -> None:
    if LOGO_FILE.exists():
        logo_size = 9 * mm
        pdf.drawImage(
            str(LOGO_FILE),
            MARGIN_X,
            PAGE_HEIGHT - 15 * mm,
            width=logo_size,
            height=logo_size,
            preserveAspectRatio=True,
            mask="auto",
        )
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(MARGIN_X + 12 * mm, PAGE_HEIGHT - 12 * mm, title)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 12 * mm, page_label)
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.5)
    pdf.line(MARGIN_X, PAGE_HEIGHT - 18 * mm, PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 18 * mm)


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
    pdf.setFillColor(PANEL)
    pdf.roundRect(x, y, width, height, 3, stroke=0, fill=1)
    pdf.setStrokeColor(LINE)
    pdf.roundRect(x, y, width, height, 3, stroke=1, fill=0)

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
    start_y = PAGE_HEIGHT - MARGIN_TOP - 18 * mm - card_h

    for page_index, offset in enumerate(range(0, len(records), columns * rows), start=1):
        draw_page_background(pdf)
        draw_header(pdf, BRAND, f"Catalog page {page_index}")
        page_records = records[offset : offset + columns * rows]
        for item_index, record in enumerate(page_records):
            row = item_index // columns
            col = item_index % columns
            x = MARGIN_X + col * (card_w + gap_x)
            y = start_y - row * (card_h + gap_y)
            pdf.setFillColor(PANEL)
            pdf.roundRect(x - 2 * mm, y, card_w + 4 * mm, card_h, 4, stroke=0, fill=1)
            pdf.setStrokeColor(LINE)
            pdf.roundRect(x - 2 * mm, y, card_w + 4 * mm, card_h, 4, stroke=1, fill=0)
            draw_image_box(pdf, PROJECT_DIR / record["image"], temp_dir, x, y + 12 * mm, card_w, image_h - 1 * mm)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(x, y + 5 * mm, record["code"])
            pdf.setFillColor(MUTED)
            pdf.setFont("Helvetica", 7)
            pdf.drawRightString(x + card_w, y + 5.4 * mm, record["type"])
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
