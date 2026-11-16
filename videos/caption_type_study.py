"""Unadopted 26/34px category-caption comparison; frozen renderer untouched."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, __version__ as pillow_version
import render

BASELINE = '1538d57e3128d75767af52c2a7e022023b2c03ea'
TIMES = (49, 52, 55, 58)
BOX = (80, 590, 1120, 80)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ink(t, size):
    value = render.cue_at(t)[1]
    advance = render.measure(value, size, False)
    if advance > BOX[2]:
        raise ValueError('Study requires one line; do not silently wrap')
    x = BOX[0] + (BOX[2] - advance) / 2
    bounds = ImageDraw.Draw(Image.new('RGB', (1280, 720))).textbbox(
        (x, BOX[1]), value, font=render.font(size))
    if not (80 <= bounds[0] < bounds[2] <= 1200 and
            590 <= bounds[1] < bounds[3] < 670):
        raise ValueError('Actual caption ink leaves the fixed box')
    return dict(text=value, font_px=size, nominal_font_px_at_640=size / 2,
                advance_px=advance, ink_bounds=list(bounds), lines=1)


def frame(n, size=34):
    if type(n) is not int or not 49 * 24 <= n < 61 * 24:
        raise ValueError('Only source frames 1176..1463 are in this study')
    if type(size) is not int or size not in (26, 34):
        raise ValueError('Only current 26px / study 34px supported')
    t = n / 24
    ink(t, size)
    image = render.render_frame(t)
    if size == 34:
        draw = ImageDraw.Draw(image)
        # Erase only the existing caption box, not the footer or progress bar.
        draw.rectangle((80, 590, 1199, 669), fill='#0a111c')
        render.text(draw, BOX, render.cue_at(t)[1], size, center=True)
    return image


def export(out):
    out = Path(out)
    if out.exists():
        raise FileExistsError('Choose a new study directory')
    out.mkdir(parents=True)
    sheet = Image.new('RGB', (1280, 1488), render.BG)
    draw = ImageDraw.Draw(sheet)
    for x, label in ((16, 'CURRENT · 26px source / 13px at 640'),
                     (656, 'UNADOPTED · 34px source / 17px at 640')):
        draw.text((x, 12), label, font=render.font(24), fill=render.FG)
    images = {}
    for row, t in enumerate(TIMES):
        for col, size in enumerate((26, 34)):
            im = frame(t * 24, size)
            path = out / f'{t}s-{size}px-1280.png'
            im.save(path)
            images[path.name] = sha(path)
            sheet.paste(im.resize((640, 360), Image.Resampling.LANCZOS),
                        (col * 640, 48 + row * 360))
    path = out / 'comparison-640.png'
    sheet.save(path)
    images[path.name] = sha(path)
    sources = ('caption_type_study.py', 'render.py', 'lesson_model.py',
               'fft-latency/lesson.json', 'fft-latency/review-version.json', 'uv.lock')
    report = dict(source_commit=BASELINE, publication_approved=False,
                  status='unadopted original-copy category-caption type study',
                  pillow=pillow_version, fps=24, window=[49, 61],
                  source_video_sha256=json.loads((render.ROOT / 'fft-latency/review-version.json').read_text())['video_sha256'],
                  cues=[dict(start=t, end=t+3, current=ink(t, 26), proposed=ink(t, 34)) for t in TIMES],
                  source_hashes={p: sha(render.ROOT / p) for p in sources},
                  font_sha256=sha(render.font(34).path), images=images,
                  limitations='Source stills, not encoded media or adoption. No copy/timing change; '
                  'no proof of device readability, comprehension, accessibility or speech sync. '
                  'Footer and inactive category labels remain small. Other scenes not tested at 34px.')
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    print(json.dumps(export(parser.parse_args().out), indent=2))
