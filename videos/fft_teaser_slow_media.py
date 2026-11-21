"""Separate silent 34-second comparison encoder; frozen 28-second draft untouched."""
import argparse
import json
from pathlib import Path
import subprocess

from PIL import Image, __version__ as pillow_version
import fft_teaser_pacing as pacing
import fft_teaser_media as original
from fft_teaser import timestamp
from fft_teaser_layouts import cue_at, scope_index
from qa import validate_media
from render import font

ROOT=Path(__file__).resolve().parent
BASELINE='c1a0bf873111dbd73b161bcb17815fa6cf2aba29'
SOURCES=original.SOURCES+('fft_teaser_slow_media.py','fft_teaser_pacing.py',
                        'fft-latency/teaser-pacing.json','fft-latency/teaser-render/candidate.json')


def vtt():
    lines=['WEBVTT','','NOTE Silent slower comparison reading track; no audio, not aligned to speech.','']
    for c in pacing.cues():
        lines += [f"{timestamp(c['start'])} --> {timestamp(c['end'])}",c['caption'],'']
    return '\n'.join(lines)


def selection():
    cuts={c['start']*24 for c in pacing.cues()} | {528,600,672,744}
    return sorted({0,815,*range(0,816,48),*cuts,*(n-1 for n in cuts if n)})


def inspect(movie,out):
    pacing.load()
    movie,out=Path(movie).resolve(),Path(out)
    if not movie.is_file():raise ValueError('Expected existing local comparison movie')
    if out.exists():raise FileExistsError('Choose a new review directory')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_frames','-show_entries',
        'frame=best_effort_timestamp_time:stream=codec_type,codec_name,width,height,avg_frame_rate,r_frame_rate:format=duration',
        '-of','json',str(movie)]))
    if len(probe['streams'])!=1 or probe['streams'][0]['codec_type']!='video':
        raise ValueError('One silent video stream required')
    facts=validate_media(probe,dict(width=1080,height=1920,fps=24,duration=34))
    if facts['codec']!='h264':raise ValueError('Expected H.264 test')
    out.mkdir(parents=True);folder=out/'encoded';folder.mkdir()
    indices=selection();select='+'.join(f'eq(n\\,{n})' for n in indices)
    subprocess.run(['ffmpeg','-v','error','-xerror','-n','-i',str(movie),'-map','0:v:0',
        '-vf','select='+select,'-fps_mode','vfr','-threads','1',str(folder/'%04d.png')],check=True)
    paths=sorted(folder.glob('*.png'))
    if len(paths)!=len(indices):raise ValueError('Incomplete decoded sample pack')
    samples=[]
    for n,path in zip(indices,paths):
        source=pacing.source_time(n/24);small=folder/(path.stem+'-360.png')
        with Image.open(path) as im:im.resize((360,640),Image.Resampling.LANCZOS).save(small)
        samples.append(dict(frame=n,seconds=n/24,source_seconds=source,
            cue=cue_at(source)['id'],scope_focus=scope_index(source),
            expected_caption=cue_at(source)['caption'],image='encoded/'+path.name,small='encoded/'+small.name))
    caption_path=out/'fft-latency-teaser-slower.vtt';caption_path.write_text(vtt())
    report=dict(source_commit=BASELINE,movie=movie.name,sha256=original.sha(movie),media=facts,
        complete_decode=True,audio=False,publication_approved=False,samples=samples,
        compared_to_sha256=pacing.load()['frozen_video_sha256'],
        captions_sha256=original.sha(caption_path),pillow=pillow_version,
        source_hashes={p:original.sha(ROOT/p) for p in SOURCES},
        fonts={str(font(46,b).path):original.sha(font(46,b).path) for b in (False,True)},
        tools={p:subprocess.check_output([p,'-version'],text=True).splitlines()[0] for p in ('ffmpeg','ffprobe')},
        limitations='Expected captions are mapped source metadata, not OCR. Decode and sampled QA are not full playback, comprehension, accessibility, audio sync or approval.')
    (out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def render(out):
    out=Path(out)
    if out.exists():raise FileExistsError('Choose a new render directory')
    # Validate each distinct layout before the encoder; no stale success report on failure.
    for n in (0,96,192,288,408,528,600,672,744):pacing.frame(n)
    out.mkdir(parents=True);movie=out/'fft-latency-teaser-slower-draft.mp4'
    process=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24',
        '-s','1080x1920','-r','24','-i','pipe:0','-an','-c:v','libx264','-threads','2',
        '-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],stdin=subprocess.PIPE)
    try:
        for n in range(816):process.stdin.write(pacing.frame(n)[0].tobytes())
    except BaseException:
        process.kill();raise
    finally:
        process.stdin.close();process.wait()
    if process.returncode:raise RuntimeError('Encode failed; partial output is not reviewed')
    return inspect(movie,out/'review')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True,type=Path)
    p.add_argument('--video',type=Path);a=p.parse_args()
    r=inspect(a.video,a.out) if a.video else render(a.out)
    print(r['sha256'],len(r['samples']),'decoded samples; silent unapproved comparison.')
