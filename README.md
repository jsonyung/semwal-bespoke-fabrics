# Semwal Bespoke Fabrics

A searchable fabric catalog for Semwal Bespoke.

## What is inside

- Total fabric images: **307**
- PDF catalog: [semwal-bespoke-fabrics-catalog.pdf](semwal-bespoke-fabrics-catalog.pdf)
- Searchable Markdown catalog: [CATALOG.md](CATALOG.md)
- Browser search catalog: [index.html](index.html)
- Machine-readable data: [catalog-data.json](catalog-data.json)

## Code summary

- `I` series: 292 fabrics, from `I-18` to `I-462`
- `PI` series: 15 fabrics, from `PI-502` to `PI-531`

## How to search

- On GitHub, open `CATALOG.md` and use browser search for a code like `I-440`.
- On GitHub Pages, open `index.html` and use the search box.

## Adding more fabrics

1. Add new fabric images into `images/` using code filenames such as `I-463.jpg`.
2. Run `python3 scripts/generate_catalog.py`.
3. Commit and push the updated files.
