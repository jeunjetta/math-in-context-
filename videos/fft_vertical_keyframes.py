"""Two original vertical layout prototypes; no timeline, encoder or publication."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, __version__ as pillow_version
from fft_teaser import resolved
from lesson_model import context, metrics
from render import BG, FG, MUTED, CYAN, AMBER, PANEL, font

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT / 'fft-latency'
SIZE = (1080, 1920)
# Design-only reserve: right-side controls and bottom metadata can vary by app.
SAFE = (90, 170, 900, 1550)


def copy_data():
    data = json.loads((FOLDER/'vertical-keyframes.json').read_text())
    if data['publication_approved'] is not False:
        raise ValueError('Still prototypes cannot grant publication approval')
    return data


def checked_text(draw, box, value, size, records, color=FG, bold=False):
    """Wrap using actual ink boxes, optically align, reject every overflow."""
    x,y,w,h = box
    face = font(size,bold)
    lines=[]
    for paragraph in value.split('\n'):
        line=''
        for word in paragraph.split():
            candidate=(line+' '+word).strip()
            b=draw.textbbox((0,0),candidate,font=face)
            if b[2]-b[0]>w:
                if not line: raise ValueError('Word clips: '+word)
                lines.append(line);line=word
            else: line=candidate
        lines.append(line)
    pitch=round(size*1.3)
    for i,line in enumerate(lines):
        l,t,r,b=draw.textbbox((0,0),line,font=face)
        actual=(x,y+i*pitch,x+r-l,y+i*pitch+b-t)
        if actual[2]>x+w or actual[3]>y+h:
            raise ValueError('Text clips: '+value)
        if not (SAFE[0]<=actual[0]<=actual[2]<=SAFE[2] and
                SAFE[1]<=actual[1]<=actual[3]<=SAFE[3]):
            raise ValueError('Text leaves design safe region: '+value)
        draw.text((x-l,y+i*pitch-t),line,font=face,fill=color)
        records.append({'text':line,'bounds':actual,'size':size,'color':color})


def bar_geometry(fourier, other, baseline, y):
    scale=780/float(baseline)
    split=100+float(fourier)*scale
    end=split+float(other)*scale
    return [(100,y,split,y+82),(split,y,end,y+82)]


def image(kind, data=None):
    if kind not in ('baseline','result'): raise ValueError('Only two prototypes exist')
    data=copy_data() if data is None else data
    if data['publication_approved'] is not False: raise ValueError('Unapproved only')
    teaser=resolved()
    lesson=json.loads((FOLDER/'lesson.json').read_text())
    values=context(lesson);m=metrics(lesson)
    cue=next(c for c in teaser['cues'] if c['id']==kind)
    im=Image.new('RGB',SIZE,BG);draw=ImageDraw.Draw(im);records=[]
    def text(box,value,size,color=FG,bold=False):
        checked_text(draw,box,value,size,records,color,bold)
    text((100,180,790,50),teaser['persistent_label'],34,CYAN,True)
    for i,line in enumerate(data['headlines'][kind]):
        text((100,290+94*i,790,88),line,70,FG,True)
    current=m['fourier'] if kind=='baseline' else m['new_fourier']
    for i,(label,amount,color) in enumerate(zip(data['component_labels'],
                                             (current,m['other']),(CYAN,AMBER))):
        x=100+i*400
        draw.rounded_rectangle((x,535,x+380,740),18,fill=PANEL)
        text((x+20,558,340,65),label,46,color,True)
        text((x+20,647,340,66),f'{amount} ms',56,FG,True)
    # Always keep the original bar: the changed width has a fixed reference.
    bars=[]
    for name,y,fw in [('baseline',870,m['fourier'])]+(
            [('result',1060,m['new_fourier'])] if kind=='result' else []):
        text((100,y-60,780,48),data[name+'_label'].format_map(values),36,MUTED,True)
        draw.rectangle((100,y,880,y+82),fill=PANEL)
        segments=bar_geometry(fw,m['other'],m['baseline'],y)
        for box,color in zip(segments,(CYAN,AMBER)): draw.rectangle(box,fill=color)
        bars.append({'id':name,'segments':segments})
    total_y=1000 if kind=='baseline' else 1190
    text((100,total_y,790,84),data[kind+'_sum'].format_map(values),64,FG,True)
    if kind=='baseline':
        text((100,1130,790,65),data['baseline_note'],44,MUTED)
    text((100,1330,790,190),cue['caption'],46,FG,True)
    # No heading, baseline result, or secondary claims are added to this caption.
    return im,{'kind':kind,'proposed_cue_seconds':[cue['start'],cue['end']],
               'caption':cue['caption'],'text':records,'bars':bars,'safe_region':SAFE}


def export(out):
    out=Path(out)
    if out.exists(): raise FileExistsError('Choose a new output directory')
    frames=[image(k) for k in ('baseline','result')]  # Validate all before writing.
    out.mkdir(parents=True)
    reports=[];files={}
    for im,report in frames:
        reports.append(report)
        for width in (1080,540,360):
            name=f"{report['kind']}-{width}.png"
            im.resize((width,width*16//9),Image.Resampling.LANCZOS).save(out/name)
            files[name]=hashlib.sha256((out/name).read_bytes()).hexdigest()
    sources=('fft_vertical_keyframes.py','fft_teaser.py','lesson_model.py','render.py',
             'fft-latency/vertical-keyframes.json','fft-latency/teaser.json',
             'fft-latency/lesson.json','fft-latency/review-version.json')
    report={'status':'two still prototypes, not a rendered teaser',
            'publication_approved':False,'audio':False,'pillow':pillow_version,
            'canvas':SIZE,'images':files,'frames':reports,
            'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
            'font_sha256':{str(font(46,b).path):hashlib.sha256(Path(font(46,b).path).read_bytes()).hexdigest()
                           for b in (False,True)}}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True,type=Path)
    export(p.parse_args().out)
