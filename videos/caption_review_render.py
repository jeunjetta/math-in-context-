"""Encode one full, unadopted caption-layout review; never replaces frozen v7."""
import argparse
import json
from pathlib import Path
import subprocess

import caption_balance as balance
import caption_layout as layout
import qa
import render

BASELINE='1dfb4f7aeba73ac6d244ec5db9383cc0e58f58f4'
NAME='fft-caption-layout-review.mp4'


def frame(n):
    if type(n) is not int or not 0<=n<1920:
        raise ValueError('Only frozen 80-second lesson frames 0..1919')
    return balance.frame(n) if 1680<=n<1800 else layout.frame(n)


def encode(out):
    out=Path(out)
    if out.exists(): raise FileExistsError('Choose a new review-render directory')
    out.mkdir(parents=True)
    render.write_captions(out/'captions.vtt')
    movie=out/NAME
    command=['ffmpeg','-hide_banner','-loglevel','error','-n','-f','rawvideo',
             '-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0',
             '-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt',
             'yuv420p','-movflags','+faststart',str(movie)]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as process:
        try:
            for n in range(1920): process.stdin.write(frame(n).tobytes())
        finally: process.stdin.close()
        if process.wait(): raise RuntimeError('Encoder failed; no successful review report')
    # Use the established cut/midpoint selection. The 101-term chronological
    # select expression exceeds this external FFmpeg build's parser budget.
    checked=qa.review_pack(movie,out/'qa',render.LESSON)
    paths=('caption_review_render.py','caption_balance.py','caption_layout.py',
           'fft-latency/caption-layout.json','render.py','lesson_model.py','qa.py',
           'fft-latency/lesson.json','fft-latency/captions.vtt',
           'fft-latency/review-version.json','uv.lock')
    record=dict(source_commit=BASELINE,publication_approved=False,
                status='unadopted full caption-layout encoded review',
                filename=NAME,sha256=layout.sha(movie),size_bytes=movie.stat().st_size,
                media=checked['media'],full_decode_completed=checked['full_decode_completed'],
                sample_count=len(checked['samples']),tools=checked['tools'],
                captions_sha256=layout.sha(out/'captions.vtt'),
                source_hashes={p:layout.sha(render.ROOT/p) for p in paths},
                font_sha256=layout.sha(render.font(34).path),
                encoder_options=command[1:-1],
                changes='34px ink-centered captions in 92px box; balanced line break only at 70–75s.',
                limitations='Technical decode/timestamp checks and sampled QA, not full human playback, '
                'actual-device readability, speech sync, accessibility, adoption or publication approval. '
                'No audio. Original live-Marimo CTA unverified. Frozen v7 remains unchanged.')
    (out/'render-report.json').write_text(json.dumps(record,indent=2)+'\n')
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    print(json.dumps(encode(p.parse_args().out),indent=2))
