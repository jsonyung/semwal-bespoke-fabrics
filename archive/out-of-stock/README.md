# Out Of Stock Fabric Archive

Move fabric images here when they should be hidden from the live website and PDF catalog, but you still want to keep the photo.

Example:

```text
images/I-440.jpg -> archive/out-of-stock/I-440.jpg
```

Then run:

```bash
./update-catalog.sh
```

To bring it back, move the image back into `images/` and run the updater again.
