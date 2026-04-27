# Semwal Bespoke Catalog Office Guide

This is the main guide for normal office use.

## What The Project Does

This project makes three things from the fabric photos in `images/`:

- A searchable website catalog.
- A downloadable PDF catalog.
- A GitHub searchable Markdown catalog.

The live website is:

```text
https://jsonyung.github.io/semwal-bespoke-fabrics/
```

## Daily Workflows

### Add New Fabric

1. Put the fabric photo inside `images/`.
2. Rename it to the fabric code, for example `I-463.jpg`.
3. Run:

```bash
./update-catalog.sh
```

4. When asked to commit and push, type `y`.

### Hide Out-Of-Stock Fabric

Use this when the fabric is temporarily unavailable or should not show to clients.

```bash
./mark-out-of-stock.sh I-440
```

The photo moves to `archive/out-of-stock/`, but it is not deleted.

### Bring Fabric Back In Stock

```bash
./restore-fabric.sh I-440
```

The photo moves back to `images/` and returns to the website/PDF.

### Correct Fabric Tags

Use this when a fabric should show under better filters.

```bash
./tag-fabric.sh I-440 colors=white,blue patterns=stripes styles=formal,light
```

Then run:

```bash
./update-catalog.sh
```

## Website Filters

The website shows simple filters first:

- Search box
- Series: `All`, `I`, `PI`

Extra filters are inside **Advanced filters**:

- Pattern: `Solid`, `Checks`, `Stripes`, `Printed`, `Texture`
- Color: `White`, `Cream`, `Blue`, `Navy`, `Black`, `Grey`, `Beige`, `Maroon`, `Green`
- Style: `Shirt`, `Formal`, `Casual`, `Premium`, `Light`, `Dark`

## Review Every Fabric

Run this to create a visual review board:

```bash
python3 scripts/generate_tag_review.py
```

Then open:

```text
fabric-tag-review.html
```

Use that page to check each image and decide whether its tags are correct. If a fabric needs correction, use `./tag-fabric.sh`.

## PDF Generation

Normally use:

```bash
./update-catalog.sh
```

That regenerates the PDF automatically.

Only run the PDF script directly if you know the catalog data is already updated:

```bash
python3 scripts/generate_pdf_catalog.py
```

## GitHub Privacy

On GitHub Free, making this repository private will stop GitHub Pages from publishing the website.

Best options:

- Keep this repo public if the website must stay live.
- Use a paid GitHub plan if you need Pages from a private repo.
- Later split the setup into a private working repo and a public website-only repo.

## File Map

- `images/`: active fabric photos.
- `archive/out-of-stock/`: hidden fabrics kept safely.
- `thumbs/`: generated website thumbnails.
- `fabric-tags.json`: editable fabric filter tags.
- `catalog-data.json`: generated website data.
- `index.html`: website catalog.
- `semwal-bespoke-fabrics-catalog.pdf`: generated PDF catalog.
- `CATALOG.md`: GitHub searchable catalog.
- `update-catalog.sh`: main updater.
- `tag-fabric.sh`: correct tags for one fabric.
- `mark-out-of-stock.sh`: hide a fabric.
- `restore-fabric.sh`: bring back a fabric.
