"""Whole-pilot larger-caption feasibility test, not an adopted renderer."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, __version__ as pillow_version
import render

BASELINE = '920dd609b068146e00c7f7827fc927a756e828c9'
CONFIG = json.loads((render.ROOT/'fft-latency/caption-layout.json').read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def layout(value):
    x, y, width, height = CONFIG['box']
    size = CONFIG['font_px']
    lines = []
    for paragraph in value.split('\n'):
        line = ''
        for word in paragraph.split():
            candidate = f'{line} {word}'.strip()
            if render.measure(candidate, size, False) > width:
                if not line: raise ValueError('Word too wide')
                lines.append(line)
                line = word
            else: line = candidate
        lines.append(line)
    if len(lines) > CONFIG['max_lines'] or len(lines)*size*1.35 > height:
        raise ValueError('Caption exceeds proposed box')
    draw = ImageDraw.Draw(Image.new('RGB', (1280,720)))
    bounds, origins = [], []
    for i, line in enumerate(lines):
        raw = draw.textbbox((0,0),line,font=render.font(size))
        ink_width = raw[2]-raw[0]
        if ink_width > width: raise ValueError('Actual caption ink too wide')
        # Center the ink, not merely its advance. Negative left bearings matter.
        origin = [x+(width-ink_width)/2-raw[0], y+i*size*1.35]
        box = draw.textbbox(origin,line,font=render.font(size))
        if not (x <= box[0] < box[2] <= x+width and y <= box[1] < box[3] <= y+height):
            raise ValueError('Actual caption ink clips')
        bounds.append(list(box))
        origins.append(origin)
    return dict(lines=lines, ink_bounds=bounds, origins=origins)


def frame(n):
    if type(n) is not int or not 0 <= n < 1920:
        raise ValueError('Only frozen-pilot frames 0..1919')
    t = n/24
    caption = render.cue_at(t)[1]
    ledger = layout(caption)
    image = render.render_frame(t)
    draw = ImageDraw.Draw(image)
    x,y,w,h = CONFIG['box']
    draw.rectangle((x,y,x+w-1,y+h-1), fill='#0a111c')
    for origin,line in zip(ledger['origins'],ledger['lines']):
        draw.text(origin,line,font=render.font(CONFIG['font_px']),fill=render.FG)
    return image


def export(out):
    out = Path(out)
    if out.exists(): raise FileExistsError('Choose a new output directory')
    out.mkdir(parents=True)
    sheet = Image.new('RGB',(1280,1488), render.BG)
    draw = ImageDraw.Draw(sheet)
    draw.text((16,12),'CURRENT · 26px / 80px box',font=render.font(24),fill=render.FG)
    draw.text((656,12),'UNADOPTED · 34px / 92px box',font=render.font(24),fill=render.FG)
    images = {}
    for row,t in enumerate(CONFIG['sample_seconds']):
        for col,im in enumerate((render.render_frame(t),frame(int(t*24)))):
            name=f'{t}s-{col}-1280.png'
            im.save(out/name)
            images[name]=sha(out/name)
            sheet.paste(im.resize((640,360),Image.Resampling.LANCZOS),(col*640,48+row*360))
    sheet.save(out/'comparison-640.png')
    images['comparison-640.png']=sha(out/'comparison-640.png')
    sources=('caption_layout.py','fft-latency/caption-layout.json','render.py',
             'lesson_model.py','fft-latency/lesson.json','fft-latency/captions.vtt',
             'fft-latency/review-version.json','uv.lock')
    report=dict(source_commit=BASELINE,config=CONFIG,pillow=pillow_version,
                cues=[dict(start=a,end=b,text=c,**layout(c)) for a,b,c in render.caption_cues()],
                images=images,source_hashes={p:sha(render.ROOT/p) for p in sources},
                font_sha256=sha(render.font(CONFIG['font_px']).path),
                limitations='Source-frame layout only, not encoded, adopted, speech-synchronized, '
                'device-tested or approved. Copy/timing/hero/footer unchanged; live CTA still unverified.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    print(json.dumps(export(p.parse_args().out),indent=2))
