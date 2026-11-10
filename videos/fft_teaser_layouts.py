"""Complete source-frame layouts. No encoder, movie, audio or publishing path."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, __version__ as pillow_version
from fft_teaser import resolved
from fft_vertical_keyframes import image as previous_image, checked_text, SIZE, SAFE
from lesson_model import context
from render import BG, FG, MUTED, CYAN, AMBER, PANEL, font

ROOT=Path(__file__).resolve().parent
FOLDER=ROOT/'fft-latency'


def load():
    data=json.loads((FOLDER/'teaser-layouts.json').read_text())
    if data['publication_approved'] is not False or data['status']!='source-frame layouts, no teaser movie':
        raise ValueError('Only unapproved source-frame layouts supported')
    if len(data['scope'])!=4 or len(data['assumptions'])!=4 or len(data['credits'])!=2:
        raise ValueError('Re-review layout before changing structure')
    return data


def cue_at(t):
    teaser=resolved()
    if not 0<=t<teaser['duration']: raise ValueError('Time outside teaser')
    return next(c for c in teaser['cues'] if c['start']<=t<c['end'])


def scope_index(t):
    cue=cue_at(t)
    if cue['id']!='scope': return None
    # Incoming phase owns the exact boundary; this scene is six seconds.
    return next(i for i in range(4) if cue['start']+1.5*i<=t<cue['start']+1.5*(i+1))


def render_frame(t, data=None):
    data=load() if data is None else data
    if data['publication_approved'] is not False: raise ValueError('Unapproved only')
    cue=cue_at(t);kind=cue['id']
    if kind in ('baseline','result'):
        im,report=previous_image(kind)
        report.update(cue=kind,scope_focus=None)
        return im,report
    values=context(json.loads((FOLDER/'lesson.json').read_text()))
    im=Image.new('RGB',SIZE,BG);draw=ImageDraw.Draw(im);records=[]
    def text(box,value,size,color=FG,bold=False):
        checked_text(draw,box,value.format_map(values),size,records,color,bold)
    text((100,180,790,50),resolved()['persistent_label'],34,CYAN,True)
    for i,line in enumerate(data['headlines'][kind]):
        text((100,290+94*i,790,88),line,64,FG,True)
    focus=None
    if kind=='question':
        q=data['question']
        text((100,560,790,65),q['label'],48,CYAN,True)
        text((100,670,790,180),q['value'],160,FG,True)
        text((100,955,790,95),q['prompt'],66,AMBER,True)
        text((100,1110,790,80),q['instruction'],44,MUTED)
    elif kind=='component':
        for i,card in enumerate(data['component']):
            y=535+i*300
            draw.rounded_rectangle((100,y,880,y+245),18,fill=PANEL)
            text((125,y+28,730,65),card['label'],48,CYAN if i==0 else AMBER,True)
            text((125,y+133,730,85),card['value'],64,FG,True)
    elif kind=='assumptions':
        for i,label in enumerate(data['assumptions']):
            y=535+i*170
            draw.rounded_rectangle((100,y,880,y+140),18,fill=PANEL)
            text((125,y+38,730,70),label,48,FG,True)
    elif kind=='scope':
        focus=scope_index(t)
        for i,card in enumerate(data['scope']):
            y=520+i*84
            draw.rounded_rectangle((100,y,880,y+72),12,fill=PANEL,
                                   outline=CYAN if i==focus else PANEL,width=3)
            text((120,y+14,740,52),card['title'],40,CYAN if i==focus else MUTED,True)
        text((100,930,790,150),data['scope'][focus]['description'],50,FG,True)
        for i,label in enumerate(data['credits']):
            text((100,1110+i*48,790,44),label,30,MUTED)
    else: raise ValueError('Unsupported scene')
    # Scope's longer caption needs four lines; keep size, lift the band.
    caption_box=(100,1240,790,300) if kind=='scope' else (100,1330,790,190)
    text(caption_box,cue['caption'],46,FG,True)
    return im,{'cue':kind,'scope_focus':focus,'caption':cue['caption'],
               'proposed_cue_seconds':[cue['start'],cue['end']],
               'text':records,'safe_region':SAFE}


def frame_index(n):
    data=resolved()
    if type(n) is not int or not 0<=n<data['duration']*data['fps']:
        raise ValueError('Frame index outside teaser')
    return render_frame(n/data['fps'])


def export(out):
    out=Path(out)
    if out.exists(): raise FileExistsError('Choose a new output directory')
    # Stage/validate everything in memory before creating the destination.
    times=(2,10,19.5,22.75,24.25,25.75,27.25)
    frames=[render_frame(t) for t in times]
    out.mkdir(parents=True)
    images={};reports=[]
    for t,(im,record) in zip(times,frames):
        key=record['cue']+(f"-{record['scope_focus']}" if record['scope_focus'] is not None else '')
        for width in ((1080,360) if record['scope_focus'] in (None,0) else (360,)):
            name=f'{key}-{width}.png'
            im.resize((width,width*16//9),Image.Resampling.LANCZOS).save(out/name)
            images[name]=hashlib.sha256((out/name).read_bytes()).hexdigest()
        reports.append(dict(time=t,**record))
    sources=('fft_teaser_layouts.py','fft_vertical_keyframes.py','fft_teaser.py','lesson_model.py','render.py',
             'fft-latency/teaser-layouts.json','fft-latency/vertical-keyframes.json',
             'fft-latency/teaser.json','fft-latency/lesson.json','fft-latency/review-version.json')
    report={'status':'source-frame layouts, no teaser movie','publication_approved':False,
            'audio':False,'canvas':SIZE,'proposed_duration':28,'fps':24,
            'pillow':pillow_version,'images':images,'frames':reports,
            'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
            'font_sha256':{str(font(46,b).path):hashlib.sha256(Path(font(46,b).path).read_bytes()).hexdigest()
                           for b in (False,True)}}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True,type=Path)
    export(p.parse_args().out)
