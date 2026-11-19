# main.py — news-image-20261119 entry program.
# Draws "The World in One Day", a 1024x1024 front page summing up
# Thursday 19 November 2026 in 36 verified stories (1 hero, 5 leads,
# 30 briefs), with a world map and a markets panel.
# Python 3.13 standard library only, no network, no clock, no random:
# running it twice writes identical bytes.
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import data
import draw
import layout
from png import Canvas


def main():
    total = data.validate()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")

    canvas = Canvas(layout.W, layout.H, layout.PAPER)
    plan = layout.plan(canvas)
    draw.render(canvas, plan)
    blob = canvas.png_bytes()

    assert blob[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    assert len(blob) <= 1048576, "entry.png over 1 MiB: %d" % len(blob)
    with open(out_path, "wb") as f:
        f.write(blob)
    digest = hashlib.sha256(blob).hexdigest()
    print("stories: %d" % total)
    print("entry.png: %d bytes -> %s" % (len(blob), out_path))
    print("sha256: %s" % digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
