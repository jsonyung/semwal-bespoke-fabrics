from __future__ import annotations

import csv
import html
import json
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / "catalog-data.json"
HTML_FILE = PROJECT_DIR / "fabric-tag-review.html"
CSV_FILE = PROJECT_DIR / "fabric-tag-review.csv"


def joined(record: dict[str, object], key: str) -> str:
    values = record.get(key, [])
    if not isinstance(values, list):
        return ""
    return ", ".join(str(value) for value in values)


def main() -> None:
    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    with CSV_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["code", "filename", "colors", "patterns", "uses", "styles", "image"])
        for record in records:
            writer.writerow(
                [
                    record["code"],
                    record["filename"],
                    joined(record, "colors"),
                    joined(record, "patterns"),
                    joined(record, "uses"),
                    joined(record, "styles"),
                    record["image"],
                ]
            )

    cards = []
    for record in records:
        code = html.escape(str(record["code"]))
        image = html.escape(str(record["image"]))
        thumb = html.escape(str(record.get("thumb") or record["image"]))
        colors = html.escape(joined(record, "colors"))
        patterns = html.escape(joined(record, "patterns"))
        styles = html.escape(joined(record, "styles"))
        command = html.escape(
            f"./tag-fabric.sh {record['code']} colors={joined(record, 'colors').replace(', ', ',')} "
            f"patterns={joined(record, 'patterns').replace(', ', ',')} "
            f"styles={joined(record, 'styles').replace(', ', ',')}"
        )
        cards.append(
            f"""
            <article class="card">
              <a href="{image}" target="_blank" rel="noreferrer"><img src="{thumb}" alt="{code}"></a>
              <div class="meta">
                <h2>{code}</h2>
                <p><strong>Color</strong> {colors}</p>
                <p><strong>Pattern</strong> {patterns}</p>
                <p><strong>Style</strong> {styles}</p>
                <code>{command}</code>
              </div>
            </article>
            """
        )

    HTML_FILE.write_text(
        f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Semwal Fabric Tag Review</title>
    <style>
      body {{ margin: 0; background: #f6f7fb; color: #1b1e28; font-family: Inter, system-ui, sans-serif; }}
      header {{ position: sticky; top: 0; z-index: 1; border-bottom: 1px solid #d8dce8; background: #fff; }}
      .wrap {{ width: min(1280px, calc(100% - 32px)); margin: 0 auto; }}
      .mast {{ padding: 18px 0; }}
      h1 {{ margin: 0; font-size: 30px; }}
      p {{ color: #5a6072; }}
      .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px; padding: 20px 0 44px; }}
      .card {{ overflow: hidden; border: 1px solid #d8dce8; border-radius: 8px; background: #fff; box-shadow: 0 14px 34px rgba(27, 30, 40, 0.08); }}
      img {{ display: block; width: 100%; aspect-ratio: 1; object-fit: cover; background: #edeff6; }}
      .meta {{ display: grid; gap: 6px; padding: 12px; }}
      h2 {{ margin: 0; font-size: 18px; }}
      .meta p {{ margin: 0; font-size: 13px; }}
      strong {{ display: inline-block; min-width: 56px; color: #1b1e28; }}
      code {{ display: block; overflow-x: auto; border-radius: 6px; padding: 8px; background: #edeff6; color: #1b1e28; font-size: 11px; white-space: nowrap; }}
    </style>
  </head>
  <body>
    <header>
      <div class="wrap mast">
        <h1>Fabric Tag Review</h1>
        <p>Check every fabric visually. Copy the command on any card, edit tags if needed, then run it in Terminal.</p>
      </div>
    </header>
    <main class="wrap grid">
      {''.join(cards)}
    </main>
  </body>
</html>
""",
        encoding="utf-8",
    )
    print(f"Generated {HTML_FILE.name} and {CSV_FILE.name} for {len(records)} fabrics.")


if __name__ == "__main__":
    main()
