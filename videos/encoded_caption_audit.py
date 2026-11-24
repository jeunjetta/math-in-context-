"""Four encoded caption samples: solid-core diagnostic, not readability approval."""
import argparse
from functools import cache
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageFilter, __version__ as pillow_version
import contrast_audit as colors
import source_only_review as source

FRAMES = (1212, 1284, 1356, 1428)  # 50.5, 53.5, 56.5, 59.5 seconds
BOX = (80, 590, 1200, 682)  # exclusive right/bottom; captions only


def digest(data):
    return hashlib.sha256(data).hexdigest()


@cache
def light(rgb):
    return colors.luminance('#' + ''.join(f'{v:02x}' for v in rgb))


def core_mask(image, rgb):
    """Only exact source colors with a same-color 3x3 neighbourhood."""
    mask = Image.new('L', image.size)
    mask.putdata([255 if p == rgb else 0 for p in image.getdata()])
    return mask.filter(ImageFilter.MinFilter(3))


def measure(reference, decoded):
    if reference.mode != 'RGB' or decoded.mode != 'RGB' or reference.size != decoded.size:
        raise ValueError('Matching RGB images required')
    values = []
    for rgb in ((244, 247, 252), (10, 17, 28)):
        mask = core_mask(reference, rgb)
        samples = [light(pixel) for pixel, selected in zip(decoded.getdata(), mask.getdata()) if selected]
        if not samples:
            raise ValueError('No solid source core; do not extrapolate to thin glyphs')
        values.append(samples)
    foreground, background = values
    # Separate worst extrema are deliberately conservative, not adjacent pairs.
    return dict(foreground_core_pixels=len(foreground), background_core_pixels=len(background),
                minimum_foreground_luminance=min(foreground),
                maximum_background_luminance=max(background),
                conservative_core_ratio=(min(foreground)+.05)/(max(background)+.05))


def audit(movie, out):
    colors.audit()  # all twelve archived render-source hashes and caption/content identity
    manifest = json.loads((colors.ROOT/'fft-latency/source-only-review/render-report.json').read_text())
    data = Path(movie).read_bytes()  # immutable in-memory snapshot for hash AND decoder
    if digest(data) != manifest['sha256'] or len(data) != manifest['size_bytes']:
        raise ValueError('Not the exact source-only movie')
    out = Path(out)
    if out.exists():
        raise FileExistsError('Choose a new output directory')
    expression = '+'.join(f'eq(n\\,{n})' for n in FRAMES)
    command = ['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-vf', 'select='+expression,
               '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1']
    decoded = subprocess.run(command, input=data, capture_output=True, check=True).stdout
    stride = 1280*720*3
    if len(decoded) != len(FRAMES)*stride:
        raise ValueError('Wrong decoded sample count/geometry')
    out.mkdir(parents=True)
    rows = []
    sheet = Image.new('RGB', (640, 4*360))
    for i, n in enumerate(FRAMES):
        image = Image.frombytes('RGB', (1280,720), decoded[i*stride:(i+1)*stride])
        ref = source.frame(n)
        row = dict(frame=n, seconds=n/24, caption=source.render.cue_at(n/24)[1],
                   decoded_rgb_sha256=digest(image.tobytes()),
                   **measure(ref.crop(BOX), image.crop(BOX)))
        rows.append(row)
        image.save(out/f'frame-{n}.png')
        sheet.paste(image.resize((640,360), Image.Resampling.LANCZOS), (0,i*360))
    sheet.save(out/'samples-640.png')
    report = dict(source_commit='053c1cacd2a9a0de25626ce41d7543fef59c35ef',
                  movie_sha256=digest(data), movie_bytes=len(data),
                  script_sha256=colors.sha(__file__), pillow=pillow_version,
                  font_sha256=colors.sha(source.render.font(34).path),
                  ffmpeg=subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
                  decoder_command=command, crop_box_exclusive=BOX,
                  method='Exact RGB source masks eroded with a 3x3 minimum filter; decoded RGB extrema at those locations.',
                  samples=rows, publication_approved=False,
                  limitations='Four midpoint caption cores only. Antialias edges, thin strokes without cores, '
                  'hero/cards/footer, other frames, streaming transcodes, color-managed/device display, '
                  'reading pace, comprehension and WCAG conformance not assessed. Not speech sync or full playback.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('movie', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.movie,args.out)
    print('Four caption core ratios:', [round(r['conservative_core_ratio'],3) for r in result['samples']])
