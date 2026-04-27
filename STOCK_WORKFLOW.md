# Stock Workflow

Use this file when fabric availability changes.

## Hide A Fabric From The Website

Use this when a fabric is out of stock, discontinued for now, or should not show to clients.

```bash
./mark-out-of-stock.sh I-440
```

What happens:

- The photo moves from `images/` to `archive/out-of-stock/`.
- The fabric disappears from the website, PDF, `CATALOG.md`, and search data.
- The original photo is still saved in the archive.
- The updater asks whether to commit and push the change to GitHub.

You can also use the full filename:

```bash
./mark-out-of-stock.sh I-440.jpg
```

## Bring A Fabric Back

Use this when the fabric is available again.

```bash
./restore-fabric.sh I-440
```

What happens:

- The photo moves back from `archive/out-of-stock/` to `images/`.
- The fabric returns to the website, PDF, `CATALOG.md`, and search data.
- The updater asks whether to commit and push the change to GitHub.

## Add A New Fabric

1. Put the image in `images/`.
2. Name it with the fabric code, for example `I-463.jpg`.
3. Run:

```bash
./update-catalog.sh
```

## Permanently Remove A Fabric

Only do this when the photo is not needed anymore.

1. Delete the image from `images/`.
2. Run:

```bash
./update-catalog.sh
```

For normal business use, prefer `./mark-out-of-stock.sh CODE` instead of deleting. That keeps the photo safe for future reference.

## GitHub Privacy Note

If this repository is on GitHub Free and you make it private, the GitHub Pages website will be unpublished.

Best options:

- Keep this repo public if the website must stay live on GitHub Pages.
- Use GitHub Pro/paid plan if you want private repo support for Pages.
- Use two repos later: a private working repo and a public website-only repo.
