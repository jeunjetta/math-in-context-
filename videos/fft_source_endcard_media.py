"""Encode the unadopted source-only ending as a separate silent ten-second test."""
import argparse
import json
from pathlib import Path
import subprocess

from fft_source_endcard import ROOT, load, image, phase, sha
from qa import validate_media
from render import font
from study_media import render_study

BASELINE = '879cf7b13eb9a4cb4af3889803e41da26d31e869'
NAME = 'fft-source-ending-excerpt'
SOURCES = ('fft_source_endcard_media.py', 'fft_source_endcard.py', 'study_media.py',
           'qa.py', 'render.py', 'fft-latency/source-endcard.json',
           'fft-latency/review-version.json', 'uv.lock')


def timeline():
    proposal = load()
    return dict(width=1280, height=720, fps=proposal['fps'], duration=10,
                cues=[dict(start=c['start']-70, end=c['end']-70, text=c['caption'])
                      for c in proposal['cues']])


def captions():
    cues = timeline()['cues']
    return ('WEBVTT\n\nNOTE Silent unadopted excerpt; original pilot offsets 70–80 s.\n\n'
            + '\n\n'.join(f"00:00:{c['start']:02}.000 --> 00:00:{c['end']:02}.000\n{c['text']}"
                           for c in cues) + '\n')


def render(out):
    data = timeline()
    states = [image(i)[0] for i in (0, 1)]
    report = render_study(data, lambda t: states[phase(round(t*data['fps']))],
                          captions(), out, NAME, SOURCES, BASELINE)
    movie = Path(out)/(NAME+'-draft.mp4')
    # Inspect every decoded frame timestamp, not just the container duration.
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_frames', '-show_streams', '-show_format',
        '-of', 'json', str(movie)]))
    report['media'] = validate_media(probe, data)
    report.update(status='unadopted source-only ending technical excerpt',
                  original_pilot_window=[70, 80],
                  source_video_sha256=load()['source_video_sha256'],
                  captions_sha256=sha(Path(out)/(NAME+'.vtt')),
                  original_cue_windows=[[70, 75], [75, 80]],
                  excerpt_cue_windows=[[0, 5], [5, 10]],
                  fonts={str(font(32,b).path): sha(font(32,b).path) for b in (False, True)},
                  limitations='Separate silent technical excerpt, not an adopted full pilot. '
                    'Expected captions are not OCR. No speech sync, continuous human playback, '
                    'device readability, comprehension, rights clearance or publication approval.')
    (Path(out)/'render-report.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    print(json.dumps(render(parser.parse_args().out), indent=2))
