# Stock Workflow

Use this file when fabric availability changes.

---

## 1. Hide A Fabric (Out Of Stock)

Use this when a fabric is out of stock, discontinued, or should not show to clients.

```bash
./mark-out-of-stock.sh I-440
```

What happens:
- The photo moves from `images/` to `archive/out-of-stock/`.
- The fabric disappears from the website, PDF, `CATALOG.md`, and search data.
- The original photo is safely kept in the archive.
- The catalog and PDF rebuild automatically.

You can also use the full filename:

```bash
./mark-out-of-stock.sh I-440.jpg
```

---

## 2. Bring A Fabric Back In Stock

Use this when a fabric is available again.

```bash
./restore-fabric.sh I-440
```

What happens:
- The photo moves back from `archive/out-of-stock/` to `images/`.
- The fabric returns to the website, PDF, `CATALOG.md`, and search data.

---

## 3. Set Metres Remaining (Low Stock Warning)

Use this when a fabric is running low but **not yet out of stock**.
Shows a coloured metre bar + "Low Stock" badge on the website card.
The PDF is not affected — metres are website-only.

```bash
./set-meters.sh I-440 4
```

Examples:

```bash
./set-meters.sh I-21 4        # 4 metres left — shows red bar + Low Stock badge
./set-meters.sh I-102 7       # 7 metres left — shows yellow bar
./set-meters.sh I-135 12      # 12 metres left — shows green bar
./set-meters.sh I-21 0        # remove the bar (fabric is restocked)
```

Metre bar colours:
- 🔴 Red + "Low Stock" badge = under 5 mtrs
- 🟡 Yellow/orange = 5–10 mtrs
- 🟢 Green = 10+ mtrs

After setting metres, run:

```bash
./update-catalog.sh
```

---

## 4. Add A New Fabric

1. Put the fabric photo in `images/`.
2. Name it with the fabric code, for example `I-469.jpg`.
3. Run:

```bash
./update-catalog.sh
```

---

## 5. Permanently Remove A Fabric

Only do this when the photo is not needed anymore.

1. Delete the image from `images/`.
2. Run:

```bash
./update-catalog.sh
```

For normal business use, prefer `./mark-out-of-stock.sh CODE` instead of deleting.
That keeps the photo safe for future reference if the fabric comes back.

---

## Quick Reference — All Commands

| Task | Command |
|---|---|
| Hide (out of stock) | `./mark-out-of-stock.sh I-440` |
| Bring back (in stock) | `./restore-fabric.sh I-440` |
| Set metres remaining | `./set-meters.sh I-440 4` |
| Remove metre bar | `./set-meters.sh I-440 0` |
| Add new fabric | Put photo in `images/`, run `./update-catalog.sh` |
| Rebuild website + PDF | `./update-catalog.sh` |
| Fix fabric tags/filters | `./tag-fabric.sh I-440 colors=blue patterns=stripes` |

---

## GitHub Privacy Note

If this repository is on GitHub Free and you make it private, the GitHub Pages website will be unpublished.

Best options:

- Keep this repo public if the website must stay live on GitHub Pages.
- Use GitHub Pro/paid plan if you want private repo support for Pages.
- Use two repos later: a private working repo and a public website-only repo.
