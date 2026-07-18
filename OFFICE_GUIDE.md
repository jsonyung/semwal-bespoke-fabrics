# Semwal Bespoke Catalog — Office Guide

This is the main guide for daily office use.

---

## What The Project Does

This project makes three things from the fabric photos in `images/`:

- A searchable website catalog (live on GitHub Pages)
- A downloadable PDF catalog
- A GitHub searchable Markdown catalog

**Live website:**
```
https://jsonyung.github.io/semwal-bespoke-fabrics/
```

---

## Daily Workflows

### ▶ Hide A Fabric (Out Of Stock)

When a fabric is out of stock — remove it from the website and PDF.

```bash
./mark-out-of-stock.sh I-440
```

- The photo moves to `archive/out-of-stock/` (kept safe, not deleted).
- The fabric disappears from the website and PDF immediately after pushing.

---

### ▶ Bring A Fabric Back (In Stock Again)

When a fabric is available again — restore it to the website and PDF.

```bash
./restore-fabric.sh I-440
```

- The photo moves back to `images/`.
- The fabric returns to the website and PDF.

---

### ▶ Set Metres Remaining (Low Stock Warning)

When fabric is running low but **not yet fully out of stock** — show a warning bar on the website.

```bash
./set-meters.sh I-440 4
```

This shows a coloured metre bar on the website card:
- 🔴 **Red + "Low Stock" badge** = under 5 mtrs
- 🟡 **Yellow bar** = 5–10 mtrs
- 🟢 **Green bar** = 10+ mtrs

The PDF is **not affected** — metres only show on the website.

To remove the bar when fabric is restocked:

```bash
./set-meters.sh I-440 0
```

After setting metres, always run:

```bash
./update-catalog.sh
```

---

### ▶ Add A New Fabric

1. Put the fabric photo in `images/`
2. Name it with the fabric code, e.g. `I-469.jpg`
3. Run:

```bash
./update-catalog.sh
```

**Photo requirements:**
- Size: 800×1000 px (portrait) recommended
- Format: JPG
- Background: white, clean, no chairs or furniture
- Use ImageMagick to resize: see `HOW_TO_ADD_FABRIC_IMAGES.md`

---

### ▶ Rebuild Website + PDF

After any change, run this to update everything:

```bash
./update-catalog.sh
```

This rebuilds:
- `catalog-data.json` (website data)
- `CATALOG.md` (GitHub searchable list)
- `thumbs/` (website thumbnails)
- `semwal-bespoke-fabrics-catalog.pdf`
- `README.md`

---

## Quick Reference — All Commands

| Task | Command |
|---|---|
| Hide fabric (out of stock) | `./mark-out-of-stock.sh I-440` |
| Restore fabric (back in stock) | `./restore-fabric.sh I-440` |
| Set metres remaining | `./set-meters.sh I-440 4` |
| Remove metre bar | `./set-meters.sh I-440 0` |
| Add new fabric | Put photo in `images/`, run `./update-catalog.sh` |
| Rebuild website + PDF | `./update-catalog.sh` |
| Fix fabric tags/filters | `./tag-fabric.sh I-440 colors=blue patterns=stripes` |
| Review all tags visually | `python3 scripts/generate_tag_review.py` |

---

## Website Filters

The website has:
- **Search box** — type any fabric code like `I-440`
- **Series filter** — `All`, `I`, `PI`
- **Advanced filters:**
  - Pattern: `Solid`, `Checks`, `Stripes`, `Printed`, `Texture`
  - Color: `White`, `Cream`, `Blue`, `Navy`, `Black`, `Grey`, `Beige`, `Maroon`, `Green`
  - Style: `Shirt`, `Formal`, `Casual`, `Premium`, `Light`, `Dark`

---

## Current Catalog Stats (as of Jul 2026)

| Status | Count |
|---|---|
| Active fabrics on website | 270 |
| Archived (out of stock) | 43 |
| Low stock (metre bars) | 28 |

---

## File Map

| File / Folder | Purpose |
|---|---|
| `images/` | Active fabric photos — what's on the website |
| `archive/out-of-stock/` | Hidden fabrics — kept safe, not deleted |
| `thumbs/` | Auto-generated website thumbnails |
| `fabric-tags.json` | Fabric filter tags + metres data |
| `catalog-data.json` | Auto-generated website data |
| `index.html` | The website catalog |
| `semwal-bespoke-fabrics-catalog.pdf` | Auto-generated PDF catalog |
| `CATALOG.md` | GitHub searchable catalog |
| `update-catalog.sh` | Main updater — run after any change |
| `mark-out-of-stock.sh` | Hide a fabric |
| `restore-fabric.sh` | Bring a fabric back |
| `set-meters.sh` | Set metres remaining for low stock |
| `tag-fabric.sh` | Fix fabric filter tags |
| `STOCK_WORKFLOW.md` | Full stock workflow guide |
| `HOW_TO_ADD_FABRIC_IMAGES.md` | Image sizing + ImageMagick guide |
| `FABRIC_TAGGING.md` | Tagging guide |

---

## GitHub Privacy Note

On GitHub Free, making this repository private will stop GitHub Pages from publishing the website.

Best options:
- Keep this repo **public** if the website must stay live.
- Use a **paid GitHub plan** if you need Pages from a private repo.
- Later split into two repos: a private working repo and a public website-only repo.
