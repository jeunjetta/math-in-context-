"""Word-preserving line-balance study for the unadopted 70–75s caption."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw
import caption_layout as base
import render

BASELINE='3f7a74537ec0299a290deaaa9ab27292b59ad4b2'


def balanced(value):
    if len(base.layout(value)['lines']) != 2 or '\n' in value:
        raise ValueError('Study expects one paragraph requiring two lines')
    words=value.split()
    candidates=[]
    for split in range(2,len(words)-1):
        lines=[' '.join(words[:split]),' '.join(words[split:])]
        try: parts=[base.layout(line) for line in lines]
        except ValueError: continue
        if any(len(part['lines'])!=1 for part in parts): continue
        widths=[part['ink_bounds'][0][2]-part['ink_bounds'][0][0] for part in parts]
        candidates.append(((abs(widths[0]-widths[1]),max(widths),split),parts,lines))
    if not candidates: raise ValueError('No fitting split with at least two words per line')
    score,parts,lines=min(candidates,key=lambda row:row[0])
    origins=[];bounds=[]
    for i,part in enumerate(parts):
        shift=i*base.CONFIG['font_px']*1.35
        x,y=part['origins'][0];left,top,right,bottom=part['ink_bounds'][0]
        origins.append([x,y+shift]);bounds.append([left,top+shift,right,bottom+shift])
        if bottom+shift>682: raise ValueError('Balanced ink clips vertically')
    return dict(lines=lines,origins=origins,ink_bounds=bounds,
                ink_width_difference_px=score[0],split_word_index=score[2])


def frame(n):
    if type(n) is not int or not 1680<=n<1800:
        raise ValueError('Only frames 1680..1799 (70–75s) supported')
    ledger=balanced(render.cue_at(n/24)[1])
    image=base.frame(n);draw=ImageDraw.Draw(image)
    draw.rectangle((80,590,1199,681),fill='#0a111c')
    for line,origin in zip(ledger['lines'],ledger['origins']):
        draw.text(origin,line,font=render.font(base.CONFIG['font_px']),fill=render.FG)
    return image


def export(out):
    out=Path(out)
    if out.exists(): raise FileExistsError('Choose a new study directory')
    out.mkdir(parents=True)
    sheet=Image.new('RGB',(1280,408),render.BG);draw=ImageDraw.Draw(sheet)
    images={}
    for col,(name,im) in enumerate((('greedy',base.frame(1680)),('balanced',frame(1680)))):
        draw.text((col*640+16,12),name.upper()+' · UNADOPTED 34px STUDY',font=render.font(24),fill=render.FG)
        for width in (1280,640):
            path=out/f'{name}-{width}.png'
            im.resize((width,width*9//16),Image.Resampling.LANCZOS).save(path)
            images[path.name]=base.sha(path)
        sheet.paste(im.resize((640,360),Image.Resampling.LANCZOS),(col*640,48))
    sheet.save(out/'comparison-640.png');images['comparison-640.png']=base.sha(out/'comparison-640.png')
    text=render.cue_at(70)[1]
    paths=('caption_balance.py','caption_layout.py','fft-latency/caption-layout.json',
           'render.py','lesson_model.py','fft-latency/lesson.json',
           'fft-latency/captions.vtt','fft-latency/review-version.json','uv.lock')
    report=dict(source_commit=BASELINE,publication_approved=False,
                status='unadopted two-line balance study',window=[70,75],fps=24,
                text=text,greedy=base.layout(text),balanced=balanced(text),
                font_px=34,box=base.CONFIG['box'],images=images,
                source_hashes={p:base.sha(render.ROOT/p) for p in paths},
                font_sha256=base.sha(render.font(34).path),
                limitations='Line-break geometry only, not production adoption, encoded playback, '
                'speech sync, reading-speed or device approval. Existing live-Marimo CTA unverified.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    print(json.dumps(export(p.parse_args().out),indent=2))
