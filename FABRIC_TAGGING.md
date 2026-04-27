# Fabric Tagging Guide

Every fabric can have tags for client-friendly filtering on the website.

The main tag file is:

```text
fabric-tags.json
```

Normally, do not edit the big JSON file by hand. Use the helper command.

## Correct One Fabric

Example:

```bash
./tag-fabric.sh I-440 colors=white,blue patterns=stripes styles=formal,light
```

Then rebuild everything:

```bash
./update-catalog.sh
```

## Common Tag Values

Colors:

```text
white, cream, beige, grey, charcoal, black, blue, navy, teal, green, pink, red, maroon, brown, purple
```

Patterns:

```text
solid, checks, stripes, printed, texture
```

Uses:

```text
shirt
```

Styles:

```text
formal, casual, premium, light, dark
```

## What Source Means

`"source": "auto"` means the tag was generated from image analysis.

`"source": "manual"` means someone corrected it. Manual tags are preserved when `./update-catalog.sh` runs again.

## Good Tagging Examples

White solid office fabric:

```bash
./tag-fabric.sh I-18 colors=white patterns=solid styles=formal,light
```

Blue checks fabric:

```bash
./tag-fabric.sh I-24 colors=blue,navy patterns=checks styles=formal,dark
```

Printed casual fabric:

```bash
./tag-fabric.sh I-180 colors=blue,white patterns=printed styles=casual,light
```

Premium fabric:

```bash
./tag-fabric.sh PI-531 colors=navy patterns=checks styles=premium,formal,dark
```
