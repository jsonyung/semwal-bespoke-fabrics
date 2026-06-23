# How To Add New Fabric Images — Full Step-by-Step Guide

This guide explains **everything** from taking the photo to seeing it live on the website.
Anyone can follow this — no technical knowledge needed for the basic steps.

---

## Quick Summary (for people who already know the workflow)

```bash
# 1. Put raw photo in "new fabric/" folder
# 2. Run the ImageMagick process command (see Part 3)
# 3. Image auto-saves to semwal-bespoke-fabrics/images/
# 4. Run ./update-catalog.sh → type y → done
```

---

## Part 1 — Taking The Photo (Best Practices)

Good photos = better catalog. Follow these tips when taking fabric photos:

| ✅ DO | ❌ DON'T |
|-------|----------|
| Place fabric swatch on plain **white paper** | Use colourful backgrounds |
| Shoot in **portrait / vertical** orientation | Shoot landscape if you can avoid it |
| Keep swatch **centred** on the paper | Put swatch in corners |
| Use **good natural light** or white LED | Use yellow indoor bulbs |
| Put the **ID label** (e.g. I-467) visible in the photo | Forget to include the label |
| Hold phone **directly above**, looking straight down | Shoot at an angle |

> **Tip:** Portrait photos (phone held tall) give the best results — they need less cropping.

---

## Part 2 — Naming and Placing the File

When someone gives you new fabric photos, put them in:

```
/Users/sbtailor/StudioProjects/aa/new fabric/
```

Name each file using its fabric code:

```
I-463.jpg
I-464.jpg
PI-532.jpg
```

**Rules for filenames:**
- Use the fabric code exactly (e.g. `I-463`, not `i463` or `fabric-463`)
- Keep the `.jpg` extension (lowercase)
- No spaces in the filename
- If there are extra/duplicate photos of the same fabric (e.g. `I-466_Extra.jpg`), **skip them** — only process one photo per fabric

---

## Part 3 — Process the Images with ImageMagick

This step reduces file size and crops out wasted background — without losing quality.

### Check if ImageMagick is installed

Open Terminal and run:

```bash
magick --version
```

You should see something like `ImageMagick 7.x.x`. If not, install it:

```bash
brew install imagemagick
```

---

### Step 3A — Check if photo is Portrait or Landscape

Run this to check dimensions:

```bash
magick identify -format "%wx%h\n" "new fabric/I-467.jpg"
```

- If **width < height** (e.g. `2304x4096`) — it is **Portrait** — use Portrait command below
- If **width > height** (e.g. `4096x2304`) — it is **Landscape** — use Landscape command below

---

### Portrait Photos (phone held tall — most common)

```bash
magick "new fabric/I-464.jpg" \
  -auto-orient \
  -fuzz 8% -trim +repage \
  -resize "900x1600>" \
  -quality 82 \
  "semwal-bespoke-fabrics/images/I-464.jpg"
```

**What each part does:**

| Part | What it does |
|------|-------------|
| `-auto-orient` | Fixes rotation if phone was held at an angle |
| `-fuzz 8% -trim` | Removes background borders (8% tolerance for near-white) |
| `+repage` | Cleans up the canvas after trimming |
| `-resize "900x1600>"` | Shrinks to max 900x1600px — never upscales |
| `-quality 82` | Compresses to ~80-250 KB without visible quality loss |

---

### Landscape Photos (phone held sideways — avoid if possible)

```bash
magick "new fabric/I-467.jpg" \
  -auto-orient \
  -gravity center -crop 65%x65%+0+0 +repage \
  -fuzz 12% -trim +repage \
  -resize "900x1600>" \
  -quality 82 \
  "semwal-bespoke-fabrics/images/I-467.jpg"
```

**Extra steps for landscape:**

| Part | What it does |
|------|-------------|
| `-gravity center -crop 65%x65%` | Crops to the centre 65% — removes dark edges and table corners |
| `-fuzz 12%` | Higher tolerance because landscape backgrounds are messier |

---

### Batch — Process Multiple Files At Once

Run this from the `aa/` folder.

**Portrait batch:**

```bash
cd /Users/sbtailor/StudioProjects/aa

for f in "new fabric/I-464.jpg" "new fabric/I-465.jpg"; do
  CODE=$(basename "$f")
  magick "$f" \
    -auto-orient \
    -fuzz 8% -trim +repage \
    -resize "900x1600>" \
    -quality 82 \
    "semwal-bespoke-fabrics/images/$CODE"
  echo "Done: $CODE"
done
```

**Landscape batch:**

```bash
cd /Users/sbtailor/StudioProjects/aa

for f in "new fabric/I-463.jpg" "new fabric/I-467.jpg"; do
  CODE=$(basename "$f")
  magick "$f" \
    -auto-orient \
    -gravity center -crop 65%x65%+0+0 +repage \
    -fuzz 12% -trim +repage \
    -resize "900x1600>" \
    -quality 82 \
    "semwal-bespoke-fabrics/images/$CODE"
  echo "Done: $CODE"
done
```

---

### Step 3B — Verify the Result Before Going Live

Always check the output:

```bash
magick identify -format "%f: %wx%h, %b bytes\n" "semwal-bespoke-fabrics/images/I-467.jpg"
```

Expected output:
```
I-467.jpg: 765x1123, 144550B bytes
```

- Width should be under 900px
- Height should be under 1600px
- File size should be between **20 KB and 500 KB** (not 4 MB like the raw photo)

You can also open the file in Finder/Preview to visually check it looks correct.

---

## Part 4 — Update The Catalog

Once images are in `semwal-bespoke-fabrics/images/`, run:

```bash
cd /Users/sbtailor/StudioProjects/aa/semwal-bespoke-fabrics
./update-catalog.sh
```

This automatically:
- Counts all fabric images
- Analyzes colours and patterns (for website filters)
- Regenerates `CATALOG.md`
- Regenerates `catalog-data.json` (website data)
- Regenerates the PDF catalog
- Creates web thumbnails in `thumbs/` folder
- Shows you what changed

When it asks:

```
Commit and push these catalog changes now? [y/N]
```

Type **`y`** and press **Enter**.

After **2-5 minutes**, the live website will update automatically.

---

## Part 5 — Replacing An Old Fabric Photo

If a fabric already exists (e.g. `I-107`) and you have a better photo:

1. Process the new photo the same way as Part 3 above
2. Save it to `semwal-bespoke-fabrics/images/I-107.jpg` — **it will overwrite the old one automatically**
3. Run `./update-catalog.sh` and type `y`

> **Backup tip:** If you want to keep the old photo, copy it somewhere safe before overwriting.

---

## Part 6 — File Size Reference

| Situation | File Size | What to do |
|-----------|-----------|-----------|
| Raw phone photo | 3-7 MB | **Must process with ImageMagick** |
| Processed — perfect | 50-300 KB | Ready to use |
| Processed — still fine | 300-500 KB | OK, use it |
| Processed — very small | Under 20 KB | May look blurry — inspect the image |
| Still too large after processing | Over 500 KB | Change `-quality 82` to `-quality 75` |

---

## Part 7 — Troubleshooting

### "Too much white space around the swatch"

The `-fuzz 8%` trim is not aggressive enough. Try increasing it:

```bash
-fuzz 15% -trim +repage
```

Or for very stubborn cases, use the landscape method (65% center crop) even on portrait shots.

---

### "Part of the swatch got cut off at the edges"

The trim was too aggressive. Reduce fuzz:

```bash
-fuzz 4% -trim +repage
```

---

### "Image is still rotated sideways after processing"

Force the rotation manually:

```bash
# Rotate 90 degrees clockwise
magick input.jpg -rotate 90 output.jpg

# Rotate 90 degrees counter-clockwise
magick input.jpg -rotate -90 output.jpg
```

---

### "I accidentally saved the wrong image / want to undo"

Restore from git:

```bash
cd /Users/sbtailor/StudioProjects/aa/semwal-bespoke-fabrics
git checkout images/I-107.jpg
```

---

### "update-catalog.sh says permission denied"

```bash
chmod +x /Users/sbtailor/StudioProjects/aa/semwal-bespoke-fabrics/update-catalog.sh
```

---

## Part 8 — Full Workflow Checklist

Use this checklist every time you add a new fabric:

```
[ ] Got the raw photo from phone/camera
[ ] Named it correctly (e.g. I-468.jpg — fabric code, no spaces)
[ ] Placed raw photo in "new fabric/" folder
[ ] Checked if it is portrait or landscape (magick identify)
[ ] Ran the correct ImageMagick command (portrait or landscape)
[ ] Verified output: dimensions under 900x1600, file size 20-500 KB
[ ] Visually checked the image in Finder — looks good
[ ] Image is saved to semwal-bespoke-fabrics/images/
[ ] Ran ./update-catalog.sh
[ ] Typed y to commit and push
[ ] Waited 2-5 minutes
[ ] Checked live website — fabric appears in search
```

Live website: **https://jsonyung.github.io/semwal-bespoke-fabrics/**

---

## Part 9 — Fabric Code Naming System

| Series | Example codes | Used for |
|--------|---------------|---------|
| `I-` | I-101, I-463, I-468 | Main fabric collection |
| `PI-` | PI-502, PI-531 | Premium Indian fabrics |

Always use the code from the **physical label** on the fabric swatch.

---

## Quick Reference Card (Print This)

```
+----------------------------------------------------------+
|          ADDING NEW FABRIC — QUICK STEPS                 |
+----------------------------------------------------------+
|                                                          |
|  1. Put raw photo in:  aa/new fabric/I-XXX.jpg           |
|                                                          |
|  2a. PORTRAIT command (phone held tall):                 |
|      magick "new fabric/I-XXX.jpg"                       |
|        -auto-orient                                      |
|        -fuzz 8% -trim +repage                            |
|        -resize "900x1600>"                               |
|        -quality 82                                       |
|        "semwal-bespoke-fabrics/images/I-XXX.jpg"         |
|                                                          |
|  2b. LANDSCAPE command (phone held sideways):            |
|      magick "new fabric/I-XXX.jpg"                       |
|        -auto-orient                                      |
|        -gravity center -crop 65%x65%+0+0 +repage        |
|        -fuzz 12% -trim +repage                           |
|        -resize "900x1600>"                               |
|        -quality 82                                       |
|        "semwal-bespoke-fabrics/images/I-XXX.jpg"         |
|                                                          |
|  3. cd semwal-bespoke-fabrics && ./update-catalog.sh     |
|     -> Type y -> press Enter                             |
|                                                          |
|  4. Wait 2-5 min -> check live website                   |
|     https://jsonyung.github.io/semwal-bespoke-fabrics/  |
+----------------------------------------------------------+
```

---

*This guide is for the Semwal Bespoke Fabrics catalog project.*
*Live website: https://jsonyung.github.io/semwal-bespoke-fabrics/*
