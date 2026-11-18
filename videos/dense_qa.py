"""Dense samples of the existing caption review, without editing archived QA."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import qa
import render

BASELINE = '62e288b77e1524c08d38a4e81e2c8a2df380801a'
IDENTITY = render.ROOT/'fft-latency/caption-review/render-report.json'


def sha(path):
    with Path(path).open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def balanced_select(indices):
    indices = list(indices)
    if (not indices or any(type(n) is not int or n < 0 for n in indices)
            or indices != sorted(set(indices))):
        raise ValueError('Expected nonempty sorted unique nonnegative integer frames')
    def tree(items):
        if len(items) == 1:
            return f'eq(n\\,{items[0]})'
        middle = len(items)//2
        return '('+tree(items[:middle])+'+'+tree(items[middle:])+')'
    return tree(indices)


def extract_frames(video, out, indices):
    expression = balanced_select(indices)
    out = Path(out)
    if out.exists():
        raise FileExistsError('Choose a new dense-frame directory')
    out.mkdir(parents=True)
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-xerror', '-n',
                    '-i', str(video), '-map', '0:v:0', '-vf', 'select='+expression,
                    '-vsync', '0', '-threads', '1', str(out/'%04d.png')], check=True)
    paths = sorted(out.glob('*.png'))
    if len(paths) != len(indices):
        raise ValueError('Incomplete dense export; no successful report')
    return paths, expression


def review(video, out):
    video, out = Path(video).resolve(), Path(out).resolve()
    identity = json.loads(IDENTITY.read_text())
    if not video.is_file() or sha(video) != identity['sha256']:
        raise ValueError('Expected the exact unadopted full caption-review movie')
    if out.exists():
        raise FileExistsError('Choose a new review directory')
    # Reuse the frozen probe/all-timestamp/full-decode checks, without monkeypatching.
    checked = qa.review_pack(video, out/'cuts', render.LESSON)
    indices = qa.sample_frames(render.LESSON, every_seconds=1)
    paths, expression = extract_frames(video, out/'frames', indices)
    records = [dict(frame=n, seconds=n/render.LESSON['fps'],
                    scene=render.scene_at(n/render.LESSON['fps'], render.LESSON)['id'],
                    expected_caption=render.cue_at(n/render.LESSON['fps'], render.LESSON)[1],
                    image='frames/'+p.name, image_sha256=sha(p))
               for n, p in zip(indices, paths)]
    sheets = qa.contact_sheets(paths, records, out)
    if sha(video) != checked['input_sha256']:
        raise ValueError('Input changed during review; no successful report')
    report = dict(source_commit=BASELINE, input_sha256=sha(video),
                  identity_report_sha256=sha(IDENTITY), media=checked['media'],
                  source_hashes={p:sha(render.ROOT/p) for p in
                                 ('dense_qa.py', 'qa.py', 'render.py', 'lesson_model.py', 'uv.lock')},
                  tools=checked['tools'], full_decode_completed=True, decode_passes=2,
                  baseline_qa='cuts/report.json', every_seconds=1,
                  selection_expression=expression, samples=records, contact_sheets=sheets,
                  publication_approved=False,
                  limitations='Expected captions are metadata, not OCR. Dense samples are not '
                  'full playback, motion/pacing/device/accessibility/audio-sync or adoption approval.')
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = review(args.video, args.out)
    print(f"Dense QA: {len(result['samples'])} samples; no movie edit or approval.")
