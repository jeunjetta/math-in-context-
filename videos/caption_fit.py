"""Isolated stability-caption source-frame comparison; never modifies the pilot."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from PIL import Image,ImageDraw,__version__ as pillow_version
from lesson_model import load_lesson
from render import ROOT,render_frame,cue_at,font,measure

FOLDER=ROOT/'fft-latency'
BASELINE='c08b87e3f63443a778eb27fc6e1ef1ab632ccb4b'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def data_pair():
    proposal=json.loads((FOLDER/'caption-proposals.json').read_text())
    identity=json.loads((FOLDER/'review-version.json').read_text())
    selected=proposal['proposals'][1]
    if (proposal['publication_approved'] is not False or
            proposal['status']!='unadopted category-caption copy proposals' or
            proposal['video_sha256']!=identity['video_sha256'] or
            (selected['category'],selected['start'],selected['end'])!=('Stability',52,55)):
        raise ValueError('Expected unadopted stability copy bound to the frozen pilot')
    current=load_lesson(FOLDER/'lesson.json');proposed=deepcopy(current)
    proposed['scenes'][5]['captions'][1]=selected['text']
    return current,proposed


def frame(n,proposed=False):
    if type(n) is not int or not 1248<=n<1320:
        raise ValueError('Only stability frames 1248..1319 supported')
    pair=data_pair()
    return render_frame(n/24,pair[1 if proposed else 0])


def caption_ink(data):
    value=cue_at(52,data)[1];advance=measure(value,26,False)
    if advance>1120:raise ValueError('Comparison assumes one caption line')
    x=80+(1120-advance)/2
    bounds=ImageDraw.Draw(Image.new('RGB',(1280,720))).textbbox((x,590),value,font=font(26))
    if not (80<=bounds[0]<bounds[2]<=1200 and 590<=bounds[1]<bounds[3]<=670):
        raise ValueError('Caption ink leaves its source box')
    return dict(text=value,characters=len(value),font_px=26,nominal_font_px_at_640=13,
                lines=1,advance_px=advance,ink_bounds=list(bounds))


def export(out):
    out=Path(out)
    if out.exists():raise FileExistsError('Choose a new still-comparison output directory')
    pair=data_pair();records=[caption_ink(d) for d in pair]
    out.mkdir(parents=True)
    images={}
    for name,data in zip(('current','proposed'),pair):
        im=render_frame(52,data)
        for width in (1280,640):
            path=out/f'{name}-{width}.png'
            im.resize((width,width*9//16),Image.Resampling.LANCZOS).save(path)
            images[path.name]=sha(path)
    paths=('caption_fit.py','render.py','lesson_model.py','fft-latency/lesson.json',
           'fft-latency/caption-proposals.json','fft-latency/review-version.json','uv.lock')
    report=dict(source_commit=BASELINE,source_video_sha256=json.loads((FOLDER/'review-version.json').read_text())['video_sha256'],
                status='unadopted stability-caption source-frame comparison',publication_approved=False,
                frame=1248,seconds=52,window=[52,55],fps=24,pillow=pillow_version,
                captions=records,images=images,source_hashes={p:sha(ROOT/p) for p in paths},
                fonts={str(font(26,b).path):sha(font(26,b).path) for b in (False,True)},
                limitations='Source-frame stills, not encoded media, adoption, device readability, '
                'full playback, speech sync, accessibility or publication approval. '
                'Both captions remain one line at unchanged 26px source / nominal 13px half-size.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    print(json.dumps(export(p.parse_args().out),indent=2))
