"""Encode/review one silent vertical draft locally. No upload or approval path."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image, __version__ as pillow_version
from fft_teaser import resolved, timestamp
from fft_teaser_layouts import frame_index, cue_at, scope_index
from qa import validate_media
from render import font

ROOT=Path(__file__).resolve().parent
BASELINE='61f11c05c8c47011eb93645bd074075272b9da32'
SOURCES=('fft_teaser_media.py','fft_teaser_layouts.py','fft_vertical_keyframes.py',
         'fft_teaser.py','lesson_model.py','render.py','qa.py',
         'fft-latency/teaser-layouts.json','fft-latency/vertical-keyframes.json',
         'fft-latency/teaser.json','fft-latency/lesson.json','fft-latency/review-version.json')


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def vtt():
    lines=['WEBVTT','','NOTE Silent draft reading track. No audio; not aligned to speech.','']
    for cue in resolved()['cues']:
        lines += [f"{timestamp(cue['start'])} --> {timestamp(cue['end'])}",cue['caption'],'']
    return '\n'.join(lines)


def selection():
    data=resolved();fps=data['fps'];count=fps*data['duration']
    indices={0,count-1}
    for cue in data['cues']:
        n=cue['start']*fps
        indices.update((max(0,n-1),n,round((cue['start']+cue['end'])*fps/2)))
    for n in (528,564,600,636): indices.update((n-1,n))
    indices.update(range(0,count,48))
    return sorted(indices)


def inspect(movie,out):
    movie,out=Path(movie).resolve(),Path(out)
    if not movie.is_file(): raise ValueError('Expected an existing local movie')
    if out.exists(): raise FileExistsError('Choose a new review directory')
    probe=json.loads(subprocess.check_output([
        'ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries',
        'frame=best_effort_timestamp_time:stream=codec_type,codec_name,width,height,avg_frame_rate,r_frame_rate:format=duration',
        '-of','json',str(movie)]))
    streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
                    'stream=codec_type','-of','json',str(movie)]))['streams']
    if len(streams)!=1 or streams[0]['codec_type']!='video':
        raise ValueError('Silent, one-video-stream draft only; no audio sync certification')
    facts=validate_media(probe,dict(width=1080,height=1920,fps=24,duration=28))
    if facts['codec']!='h264': raise ValueError('Expected H.264 test output')
    out.mkdir(parents=True);folder=out/'encoded';folder.mkdir()
    indices=selection()
    select='+'.join(f'eq(n\\,{n})' for n in indices)
    # Read the entire stream, not only the first requested frames.
    subprocess.run(['ffmpeg','-v','error','-xerror','-n','-i',str(movie),'-map','0:v:0',
                    '-vf','select='+select,'-fps_mode','vfr','-threads','1',
                    str(folder/'%04d.png')],check=True)
    paths=sorted(folder.glob('*.png'))
    if len(paths)!=len(indices): raise ValueError('Missing decoded samples; incomplete pack')
    samples=[]
    for n,path in zip(indices,paths):
        small=folder/(path.stem+'-360.png')
        with Image.open(path) as im:
            im.resize((360,640),Image.Resampling.LANCZOS).save(small)
        samples.append(dict(frame=n,seconds=n/24,cue=cue_at(n/24)['id'],
                            scope_focus=scope_index(n/24),expected_caption=cue_at(n/24)['caption'],
                            image='encoded/'+path.name,small='encoded/'+small.name))
    caption_path=out/'fft-latency-teaser.vtt';caption_path.write_text(vtt())
    report=dict(source_commit=BASELINE,movie=movie.name,sha256=sha(movie),media=facts,
                complete_decode=True,audio=False,publication_approved=False,samples=samples,
                captions_sha256=sha(caption_path),pillow=pillow_version,
                source_hashes={p:sha(ROOT/p) for p in SOURCES},
                fonts={str(font(46,b).path):sha(font(46,b).path) for b in (False,True)},
                tools={p:subprocess.check_output([p,'-version'],text=True).splitlines()[0]
                       for p in ('ffmpeg','ffprobe')},
                limitations='Expected captions are source metadata, not OCR. Sampled inspection is not full playback, accessibility, comprehension, audio sync or publishing approval.')
    (out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def render(out):
    out=Path(out)
    if out.exists(): raise FileExistsError('Choose a new render directory')
    # Validate source identity and all distinct layouts before opening the encoder.
    for n in (0,96,192,288,408,528,564,600,636): frame_index(n)
    out.mkdir(parents=True)
    movie=out/'fft-latency-teaser-draft.mp4'
    command=['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24',
             '-s','1080x1920','-r','24','-i','pipe:0','-an','-c:v','libx264',
             '-threads','2','-preset','fast','-crf','21','-pix_fmt','yuv420p',
             '-movflags','+faststart',str(movie)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for n in range(672): process.stdin.write(frame_index(n)[0].tobytes())
    except BaseException:
        process.kill()
        raise
    finally:
        process.stdin.close();process.wait()
    if process.returncode: raise RuntimeError('Encode failed; partial output is not reviewed')
    return inspect(movie,out/'review')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--video',type=Path,help='Review an existing matching movie instead of rendering')
    a=p.parse_args();r=inspect(a.video,a.out) if a.video else render(a.out)
    print(r['sha256'],len(r['samples']),'decoded samples; silent draft, not approved.')
