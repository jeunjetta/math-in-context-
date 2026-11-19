"""Full silent source-only review assembly; never replaces an adopted candidate."""
import argparse
import copy
import json
from functools import cache
from pathlib import Path
import subprocess
from PIL import ImageDraw

import caption_layout
import fft_source_endcard as ending
import qa
import render

BASELINE = '0a083c1274f3792f0385c526e01d3488285ccd22'
NAME = 'fft-source-only-review'
CONFIG = json.loads((render.ROOT/'fft-latency/source-only-review.json').read_text())


def lesson():
    data = copy.deepcopy(render.LESSON)
    proposal = ending.load()
    if (' '.join(CONFIG['first_ending_caption_lines']) != proposal['cues'][0]['caption']
            or CONFIG['publication_approved'] is not False):
        raise ValueError('Only word-preserving caption wrapping in this unadopted assembly')
    data['scenes'][-1]['heading'] = proposal['heading']
    data['scenes'][-1]['captions'] = [c['caption'] for c in proposal['cues']]
    if [(a,b) for a,b,_ in render.caption_cues(data)][-2:] != [(70,75),(75,80)]:
        raise ValueError('Ending must retain the two original cue windows')
    return data


@cache
def ending_frame(index):
    image=ending.image(index)[0]
    if index == 0:
        lesson()  # validate word identity before drawing
        draw=ImageDraw.Draw(image)
        draw.rectangle((64,595,1215,692),fill=render.BG)
        for row,line in enumerate(CONFIG['first_ending_caption_lines']):
            face=render.font(32,True)
            left,top,right,bottom=draw.textbbox((0,0),line,font=face)
            y=595+row*round(32*1.3)
            if right-left>1152 or y+bottom-top>693:
                raise ValueError('Ending caption clips')
            draw.text((64-left,y-top),line,font=face,fill=render.FG)
    return image


def frame(n):
    if type(n) is not int or not 0 <= n < 1920:
        raise ValueError('Expected full-pilot frame 0..1919')
    if n < 1680:
        return caption_layout.frame(n)
    return ending_frame(ending.phase(n-1680)).copy()


def encode(out):
    out = Path(out)
    if out.exists():
        raise FileExistsError('Choose a new source-only review directory')
    data = lesson()
    out.mkdir(parents=True)
    render.write_captions(out/(NAME+'.vtt'), data)
    (out/'resolved-lesson.json').write_text(json.dumps(data,indent=2)+'\n')
    movie = out/(NAME+'.mp4')
    command=['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24',
             '-s','1280x720','-r','24','-i','pipe:0','-an','-c:v','libx264',
             '-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)]
    process = subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for n in range(1920):
            process.stdin.write(frame(n).tobytes())
    except BaseException:
        process.kill()
        raise
    finally:
        process.stdin.close()
        process.wait()
    if process.returncode:
        raise RuntimeError('Encode failed; no successful render report')
    checked = qa.review_pack(movie,out/'qa',data)
    paths=('source_only_review.py','caption_layout.py','fft_source_endcard.py',
           'fft-latency/source-only-review.json',
           'fft-latency/source-endcard.json','fft-latency/caption-layout.json',
           'fft-latency/lesson.json','fft-latency/review-version.json',
           'render.py','lesson_model.py','qa.py','uv.lock')
    report=dict(source_commit=BASELINE,status='unadopted full source-only review',
                publication_approved=False,filename=movie.name,sha256=ending.sha(movie),
                size_bytes=movie.stat().st_size,media=checked['media'],
                full_decode_completed=checked['full_decode_completed'],
                sample_count=len(checked['samples']),tools=checked['tools'],
                captions_sha256=ending.sha(out/(NAME+'.vtt')),
                resolved_lesson_sha256=ending.sha(out/'resolved-lesson.json'),
                source_hashes={p:ending.sha(render.ROOT/p) for p in paths},
                fonts={str(render.font(32,b).path):ending.sha(render.font(32,b).path) for b in (False,True)},
                encoder_options=command[1:-1],
                changes='First 70s source pixels match larger-caption review. Final 10s reuse source-only proposal with word-preserving first-cue line break.',
                limitations='Separate silent unadopted full review. Source link is not a live lesson. '
                'No complete human/device playback, speech sync, accessibility, layout/release-design '
                'adoption, rights or publication approval. Frozen v7 and earlier review untouched.')
    (out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    result=encode(parser.parse_args().out)
    print(f"Source-only review encoded: {result['sha256']}; no approval implied.")
