# Semwal Bespoke Fabrics

A searchable fabric catalog for Semwal Bespoke.

## Open Catalog

- Live searchable website: [https://jsonyung.github.io/semwal-bespoke-fabrics/](https://jsonyung.github.io/semwal-bespoke-fabrics/)
- PDF catalog: [semwal-bespoke-fabrics-catalog.pdf](semwal-bespoke-fabrics-catalog.pdf)
- GitHub searchable catalog: [CATALOG.md](CATALOG.md)

## What is inside

- Total fabric images: **307**
- PDF catalog: [semwal-bespoke-fabrics-catalog.pdf](semwal-bespoke-fabrics-catalog.pdf)
- Searchable Markdown catalog: [CATALOG.md](CATALOG.md)
- Browser search catalog: [index.html](index.html)
- Machine-readable data: [catalog-data.json](catalog-data.json)
- Web thumbnails: [thumbs/](thumbs/)

## Code summary

- `I` series: 292 fabrics, from `I-18` to `I-462`
- `PI` series: 15 fabrics, from `PI-502` to `PI-531`

## How to search

- Best option: open the live website and type a fabric code like `I-440`.
- On GitHub, open `CATALOG.md` and use browser search with `Ctrl+F` or `Cmd+F`.
- In the PDF, use PDF search with `Ctrl+F` or `Cmd+F`.

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

- Count all fabric images.
- Update `CATALOG.md`.
- Update `catalog-data.json`.
- Update website thumbnails in `thumbs/`.
- Regenerate the PDF catalog.
- Show what changed.
- Ask before committing and pushing to GitHub.

When it asks:

```text
Commit and push these catalog changes now? [y/N]
```

Type:

```text
y
```

Then press Enter.

### 3. What Updates Online

After pushing, GitHub updates:

- Live website search
- GitHub catalog
- PDF catalog
- Image thumbnails

GitHub Pages can take a few minutes to refresh. If the website looks old, do a hard refresh with `Cmd+Shift+R` on Mac or `Ctrl+Shift+R` on Windows.

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

For another office computer, download the repository ZIP from GitHub, unzip it, and keep the folder together.
