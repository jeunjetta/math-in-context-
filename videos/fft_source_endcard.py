"""Render a source-only end-card proposal; no mutation of the frozen pilot."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image,ImageDraw,__version__ as pillow_version
from render import font,BG,FG,MUTED,CYAN,AMBER,PANEL

ROOT=Path(__file__).resolve().parent
FOLDER=ROOT/'fft-latency'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load():
    d=json.loads((FOLDER/'source-endcard.json').read_text())
    identity=json.loads((FOLDER/'review-version.json').read_text())
    if (d['source_video_sha256']!=identity['video_sha256'] or d['publication_approved'] is not False
        or d['audio'] is not False or d['status']!='unadopted source-only end-card proposal'):
        raise ValueError('Unadopted silent proposal bound to existing pilot only')
    if (d['start'],d['end'],d['fps'])!=(70,80,24):raise ValueError('Re-review changed timeline')
    if [(c['start'],c['end']) for c in d['cues']]!=[(70,75),(75,80)]:raise ValueError('Two exact cue windows required')
    if d['notebook']['kind']!='public source code, not verified live lesson':raise ValueError('Source-only destination required')
    return d


def phase(n):
    if type(n) is not int or not 0<=n<240:raise ValueError('Expected end-card frame 0..239')
    return 0 if n<120 else 1


def image(index):
    if index not in (0,1):raise ValueError('Two proposal states only')
    d=load();im=Image.new('RGB',(1280,720),BG);draw=ImageDraw.Draw(im);records=[]
    def text(box,value,size,color=FG,bold=False):
        x,y,w,h=box;face=font(size,bold);lines=[]
        for para in value.split('\n'):
            line=''
            for word in para.split():
                proposed=(line+' '+word).strip();l,t,r,b=draw.textbbox((0,0),proposed,font=face)
                if r-l>w:
                    if not line:raise ValueError('Word clips: '+word)
                    lines.append(line);line=word
                else:line=proposed
            lines.append(line)
        for i,line in enumerate(lines):
            l,t,r,b=draw.textbbox((0,0),line,font=face);yy=y+i*round(size*1.3)
            bounds=[x,yy,x+r-l,yy+b-t]
            if bounds[2]>x+w or bounds[3]>y+h or not(48<=x<=bounds[2]<=1232 and 24<=yy<=bounds[3]<=696):
                raise ValueError('Text leaves box/safe region: '+value)
            draw.text((x-l,yy-t),line,font=face,fill=color)
            records.append(dict(text=line,bounds=bounds,size=size))
    text((64,30,1152,40),d['persistent_label'],28,CYAN,True)
    text((64,92,1152,68),d['heading'],48,FG,True)
    text((64,177,1152,54),d['concept_path'],30,MUTED)
    draw.rounded_rectangle((64,244,1216,431),16,fill=PANEL)
    text((88,264,1104,42),d['label'],28,CYAN,True)
    text((88,318,1104,60),d['body'],40,FG,True)
    text((88,382,1104,42),d['disclosure'],28,AMBER,True)
    text((64,462,1152,50),d['limit'],32,FG,True)
    text((64,526,1152,42),d['credit'],28,MUTED)
    text((64,595,1152,98),d['cues'][index]['caption'],32,FG,True)
    return im,dict(phase=index,caption=d['cues'][index]['caption'],text=records)


def export(out):
    out=Path(out)
    if out.exists():raise FileExistsError('Choose a new proposal output directory')
    frames=[image(i) for i in (0,1)]
    out.mkdir(parents=True);images={}
    for i,(im,_) in enumerate(frames):
        for width in (1280,640):
            path=out/f'phase-{i}-{width}.png'
            im.resize((width,width*9//16),Image.Resampling.LANCZOS).save(path);images[path.name]=sha(path)
    sources=('fft_source_endcard.py','fft-latency/source-endcard.json','fft-latency/review-version.json','render.py')
    report=dict(status=load()['status'],source_commit=load()['source_commit'],publication_approved=False,audio=False,
        source_video_sha256=load()['source_video_sha256'],pillow=pillow_version,frames=[r for _,r in frames],images=images,
        source_hashes={p:sha(ROOT/p) for p in sources},
        fonts={str(font(32,b).path):sha(font(32,b).path) for b in (False,True)},
        limitations='Source-frame stills only. Not encoded, adopted, speech-aligned, tablet-reviewed or approved.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True,type=Path);export(p.parse_args().out)
