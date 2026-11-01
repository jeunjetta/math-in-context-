"""Original thumbnail for the synthetic latency lesson; never uploads anything."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw
from lesson_model import context, load_lesson, metrics
from render import ROOT, BG, FG, MUTED, CYAN, AMBER, text

COPY_PATH = ROOT / "fft-latency/thumbnail.json"


def resolved_copy(data):
    copy = json.loads(COPY_PATH.read_text())
    return {key: value.format_map(context(data)) for key, value in copy.items()}


def split_x(data):
    """Baseline geometry only: the thumbnail does not reveal the answer."""
    values = metrics(data)
    return 64 + round(1152 * values["fourier"] / values["baseline"])


def render_thumbnail(data):
    copy = resolved_copy(data)
    image = Image.new("RGB", (1280, 720), BG)
    d = ImageDraw.Draw(image)
    text(d, (64, 30, 900, 45), copy["brand"], 28, MUTED, True)
    text(d, (1040, 30, 176, 45), copy["status"], 28, MUTED, True)
    text(d, (64, 98, 1152, 110), copy["hook"], 78, CYAN, True)
    text(d, (64, 208, 1152, 100), copy["question"], 64, FG, True)
    text(d, (64, 334, 1152, 65), copy["baseline"], 36, MUTED)
    cut = split_x(data)
    d.rectangle((64, 418, cut-1, 560), fill=CYAN)
    d.rectangle((cut, 418, 1215, 560), fill=AMBER)
    # Labels are inside their own proportional blocks; text() rejects overflow.
    text(d, (76, 429, cut-88, 120), copy["fourier"], 38, BG, True, True)
    text(d, (cut+12, 429, 1192-cut, 120), copy["other"], 38, BG, True, True)
    # Bottom right reserved for platform duration overlays; qualifier stays left.
    text(d, (64, 610, 900, 70), copy["qualifier"], 42, FG, True)
    return image


def export(out, data):
    # Refuse to replace an existing review package.
    out.mkdir(parents=True, exist_ok=False)
    image = render_thumbnail(data)
    image.save(out / "thumbnail.png", optimize=True)
    image.resize((320, 180), Image.Resampling.LANCZOS).save(out / "thumbnail-320.png", optimize=True)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scenario", type=Path)
    args = parser.parse_args()
    data = load_lesson(ROOT / "fft-latency/lesson.json", args.scenario)
    print(export(args.out, data))


if __name__ == "__main__":
    main()
