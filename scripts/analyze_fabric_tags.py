from __future__ import annotations

import colorsys
import json
import re
from collections import Counter
from pathlib import Path

from PIL import Image, ImageStat


PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = PROJECT_DIR / "images"
OUTPUT_FILE = PROJECT_DIR / "fabric-tags.json"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"}


def natural_key(path: Path) -> tuple[str, int, str]:
    match = re.match(r"^([A-Za-z]+)-(\d+)", path.stem)
    if not match:
        return (path.stem, 0, path.suffix.lower())
    prefix, number = match.groups()
    return (prefix.upper(), int(number), path.suffix.lower())


def color_bucket(rgb: tuple[int, int, int]) -> str:
    red, green, blue = [value / 255 for value in rgb]
    hue, saturation, value = colorsys.rgb_to_hsv(red, green, blue)
    hue *= 360

    if value < 0.18:
        return "black"
    if saturation < 0.13:
        if value > 0.82:
            return "white"
        if value > 0.55:
            return "grey"
        return "charcoal"
    if saturation < 0.26 and value > 0.70:
        if 25 <= hue <= 65:
            return "cream"
        return "light"
    if 18 <= hue < 48 and value > 0.45 and saturation < 0.62:
        return "beige"
    if 12 <= hue < 42 and value < 0.55:
        return "brown"
    if hue < 12 or hue >= 345:
        if value < 0.45:
            return "maroon"
        return "red"
    if 12 <= hue < 28:
        return "orange"
    if 28 <= hue < 65:
        return "yellow" if saturation > 0.45 else "cream"
    if 65 <= hue < 155:
        return "green"
    if 155 <= hue < 205:
        return "teal"
    if 205 <= hue < 250:
        return "navy" if value < 0.43 else "blue"
    if 250 <= hue < 290:
        return "purple"
    if 290 <= hue < 345:
        return "pink" if value > 0.55 else "maroon"
    return "mixed"


def sample_pixels(image: Image.Image) -> list[tuple[int, int, int]]:
    image = image.convert("RGB")
    width, height = image.size
    crop = image.crop(
        (
            int(width * 0.18),
            int(height * 0.36),
            int(width * 0.82),
            int(height * 0.90),
        )
    )
    crop.thumbnail((120, 120), Image.Resampling.LANCZOS)
    if hasattr(crop, "get_flattened_data"):
        return list(crop.get_flattened_data())
    return list(crop.getdata())


def dominant_colors(image: Image.Image) -> list[str]:
    buckets = Counter(color_bucket(pixel) for pixel in sample_pixels(image))
    total = sum(buckets.values()) or 1

    neutral_total = sum(buckets.get(name, 0) for name in ("white", "grey", "cream", "light"))
    colorful = {
        name: count
        for name, count in buckets.items()
        if name not in {"white", "grey", "cream", "light"} and count / total >= 0.035
    }
    if colorful and neutral_total / total > 0.48:
        for name, count in colorful.items():
            buckets[name] += int(count * 1.8)
        total = sum(buckets.values()) or 1

    ranked = [
        (name, count)
        for name, count in buckets.most_common()
        if count / total >= 0.06 and name not in {"light"}
    ]
    colors = [name for name, _count in ranked[:3]]
    if not colors:
        colors = [buckets.most_common(1)[0][0]]

    # White/cream fabrics often sit on white paper. Keep them searchable.
    if buckets.get("white", 0) / total > 0.50 and "white" not in colors:
        colors.insert(0, "white")
    if buckets.get("cream", 0) / total > 0.22 and "cream" not in colors:
        colors.append("cream")

    return colors[:3]


def pattern_tags(image: Image.Image, colors: list[str]) -> list[str]:
    image = image.convert("L")
    width, height = image.size
    crop = image.crop(
        (
            int(width * 0.14),
            int(height * 0.22),
            int(width * 0.86),
            int(height * 0.90),
        )
    )
    crop = crop.resize((72, 72), Image.Resampling.LANCZOS)
    pixels = crop.load()

    horizontal_edges = []
    vertical_edges = []
    high_edge_pixels = 0
    for y in range(1, 71):
        row_total = 0
        for x in range(1, 71):
            dx = abs(pixels[x, y] - pixels[x - 1, y])
            dy = abs(pixels[x, y] - pixels[x, y - 1])
            row_total += dx
            if dx + dy > 34:
                high_edge_pixels += 1
        horizontal_edges.append(row_total / 70)
    for x in range(1, 71):
        col_total = 0
        for y in range(1, 71):
            col_total += abs(pixels[x, y] - pixels[x, y - 1])
        vertical_edges.append(col_total / 70)

    stat = ImageStat.Stat(crop)
    contrast = stat.stddev[0]
    h_strength = sum(1 for value in horizontal_edges if value > 10) / len(horizontal_edges)
    v_strength = sum(1 for value in vertical_edges if value > 10) / len(vertical_edges)
    edge_density = high_edge_pixels / (70 * 70)
    color_count = len([color for color in colors if color not in {"white", "cream", "grey"}])

    if contrast < 12 and edge_density < 0.10:
        return ["solid"]
    if h_strength > 0.28 and v_strength > 0.28:
        return ["checks"]
    if h_strength > 0.24 or v_strength > 0.24:
        return ["stripes"]
    if edge_density > 0.30 and color_count <= 1:
        return ["texture"]
    if edge_density > 0.18:
        return ["printed"]
    if contrast < 22:
        return ["solid"]
    return ["texture"]


def style_tags(code: str, colors: list[str], patterns: list[str]) -> list[str]:
    styles = ["shirt"]
    if code.startswith("PI-"):
        styles.append("premium")
    if any(pattern in patterns for pattern in ["solid", "stripes", "checks"]):
        styles.append("formal")
    if any(pattern in patterns for pattern in ["printed", "texture"]):
        styles.append("casual")
    if any(color in colors for color in ["white", "cream", "beige", "grey"]):
        styles.append("light")
    if any(color in colors for color in ["black", "charcoal", "navy", "maroon", "brown"]):
        styles.append("dark")
    return list(dict.fromkeys(styles))


def analyze_image(path: Path) -> dict[str, list[str] | str]:
    with Image.open(path) as image:
        colors = dominant_colors(image)
        patterns = pattern_tags(image, colors)
    styles = style_tags(path.stem, colors, patterns)
    tags = list(dict.fromkeys([*colors, *patterns, *styles]))
    return {
        "colors": colors,
        "patterns": patterns,
        "uses": ["shirt"],
        "styles": styles,
        "tags": tags,
        "source": "auto",
    }


def main() -> None:
    existing = {}
    if OUTPUT_FILE.exists():
        existing = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))

    records = {}
    for image_path in sorted(
        [path for path in IMAGE_DIR.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS],
        key=natural_key,
    ):
        current = existing.get(image_path.stem)
        if current and current.get("source") == "manual":
            records[image_path.stem] = current
        else:
            records[image_path.stem] = analyze_image(image_path)

    OUTPUT_FILE.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT_FILE.name} for {len(records)} fabrics.")


if __name__ == "__main__":
    main()
