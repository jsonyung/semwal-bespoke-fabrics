# Out Of Stock Fabric Archive

Move fabric images here when they should be hidden from the live website and PDF catalog, but you still want to keep the photo.

Normal office command:

```bash
./mark-out-of-stock.sh I-440
```

That command moves the file here and runs the catalog updater.

Manual example:

```text
images/I-440.jpg -> archive/out-of-stock/I-440.jpg
```

If moving manually, then run:

```bash
./update-catalog.sh
```

To bring it back, run:

```bash
./restore-fabric.sh I-440
```
