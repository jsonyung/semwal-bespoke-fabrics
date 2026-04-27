# Semwal Bespoke Fabrics

A searchable fabric catalog for Semwal Bespoke.

## Open Catalog

- Live searchable website: [https://jsonyung.github.io/semwal-bespoke-fabrics/](https://jsonyung.github.io/semwal-bespoke-fabrics/)
- PDF catalog: [semwal-bespoke-fabrics-catalog.pdf](semwal-bespoke-fabrics-catalog.pdf)
- GitHub searchable catalog: [CATALOG.md](CATALOG.md)
- Complete office guide: [OFFICE_GUIDE.md](OFFICE_GUIDE.md)
- Stock workflow guide: [STOCK_WORKFLOW.md](STOCK_WORKFLOW.md)
- Fabric tagging guide: [FABRIC_TAGGING.md](FABRIC_TAGGING.md)

## What is inside

- Total fabric images: **307**
- PDF catalog: [semwal-bespoke-fabrics-catalog.pdf](semwal-bespoke-fabrics-catalog.pdf)
- Searchable Markdown catalog: [CATALOG.md](CATALOG.md)
- Browser search catalog: [index.html](index.html)
- Machine-readable data: [catalog-data.json](catalog-data.json)
- Web thumbnails: [thumbs/](thumbs/)
- Editable fabric tags: [fabric-tags.json](fabric-tags.json)
- Tag helper command: [tag-fabric.sh](tag-fabric.sh)
- Fabric tag review board: [fabric-tag-review.html](fabric-tag-review.html)

## Code summary

- `I` series: 292 fabrics, from `I-18` to `I-462`
- `PI` series: 15 fabrics, from `PI-502` to `PI-531`

## How to search

- Best option: open the live website and type a fabric code like `I-440`.
- Use website filter buttons for color, pattern, and style.
- On GitHub, open `CATALOG.md` and use browser search with `Ctrl+F` or `Cmd+F`.
- In the PDF, use PDF search with `Ctrl+F` or `Cmd+F`.

## Website Filters

The website supports filters for:

- Series: `I`, `PI`
- Pattern: `Solid`, `Checks`, `Stripes`, `Printed`, `Texture`
- Color: `White`, `Blue`, `Black`, `Grey`, `Cream`, `Beige`, `Navy`, and more
- Style: `Formal`, `Casual`, `Premium`, `Light`, `Dark`

Filter data comes from `fabric-tags.json`. It is auto-generated first, then can be corrected by hand when someone reviews fabrics.

To correct tags for one fabric, run:

```bash
./tag-fabric.sh I-440 colors=white,blue patterns=stripes styles=formal,light
```

Then run `./update-catalog.sh`. Manual tags are preserved by future auto-analysis. See [FABRIC_TAGGING.md](FABRIC_TAGGING.md).

To review all fabrics visually, run:

```bash
python3 scripts/generate_tag_review.py
```

Then open `fabric-tag-review.html`.

## Easy Update For New Fabrics

Use this when a new fabric photo needs to be added.

### 1. Add The Image

Put the new fabric image inside the `images/` folder.

Name the file with the fabric code:

```text
I-463.jpg
I-464.jpg
PI-532.jpg
```

Rules:

- Use the fabric code as the filename.
- Keep the extension like `.jpg` or `.png`.
- Do not use spaces in the filename.
- Do not rename old files unless the fabric code is wrong.

### 2. Run One Command

Open Terminal inside this project folder and run:

```bash
./update-catalog.sh
```

The updater will:

- Count all active fabric images.
- Count archived out-of-stock images.
- Update `CATALOG.md`.
- Update `catalog-data.json`.
- Merge tags from `fabric-tags.json` into the website.
- Update website thumbnails in `thumbs/` and remove unused thumbnails.
- Regenerate the PDF catalog.
- Show what changed.
- Ask before committing and pushing to GitHub.

When it asks:

```text
Commit and push these catalog changes now? [y/N]
```

Type `y`, then press Enter.

### 3. What Updates Online

After pushing, GitHub updates:

- Live website search
- GitHub catalog
- PDF catalog
- Image thumbnails

GitHub Pages can take a few minutes to refresh. If the website looks old, do a hard refresh with `Cmd+Shift+R` on Mac or `Ctrl+Shift+R` on Windows.

## Out Of Stock Or Removed Fabrics

Use this when a fabric should disappear from the live website and PDF catalog.

### Temporarily Out Of Stock

Run:

```bash
./mark-out-of-stock.sh I-440
```

Use the real fabric code. You can also use the full filename:

```bash
./mark-out-of-stock.sh I-440.jpg
```

That fabric will be removed from the website, PDF, `CATALOG.md`, and `catalog-data.json`, but the photo is safely kept in the archive.

### Back In Stock

Run:

```bash
./restore-fabric.sh I-440
```

That fabric will return to the website, PDF, `CATALOG.md`, and `catalog-data.json`.

### Permanently Remove

Delete the fabric image from `images/`, then run `./update-catalog.sh`.

The updater also removes old unused thumbnails.

For normal office use, prefer `./mark-out-of-stock.sh CODE` instead of deleting. The full step-by-step guide is in [STOCK_WORKFLOW.md](STOCK_WORKFLOW.md).

## GitHub Private Repository Note

If this repository is on GitHub Free and you make it private, the GitHub Pages website will be unpublished.

Best options:

- Keep this repo public if the website must stay live on GitHub Pages.
- Use GitHub Pro/paid plan if you want Pages from a private repo.
- Later, split into two repos: one private working repo and one public website-only repo.

## PDF Generation

The PDF is generated automatically by:

```bash
python3 scripts/generate_pdf_catalog.py
```

Normally, do not run this alone. Use:

```bash
./update-catalog.sh
```

That updates the PDF plus the website/catalog files together.

## Moving Or Sharing This Project

Move the whole `semwal-bespoke-fabrics` folder together. The website needs these files to stay together:

- `index.html`
- `catalog-data.json`
- `images/`
- `thumbs/`
- `assets/`

For another office computer, download the repository ZIP from GitHub, unzip it, and keep the folder together.
