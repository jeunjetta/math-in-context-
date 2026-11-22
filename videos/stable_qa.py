"""Opt-in QA on a private movie snapshot; preserve the archived qa.py renderer.

Detect ordinary concurrent input edits, not adversarial filesystem activity.
No output pack is published until decoding and the final identity check pass.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from lesson_model import load_lesson
from qa import review_pack
from render import ROOT


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def stable_review_pack(video, out, data, every_seconds=None):
    video, out = Path(video).resolve(), Path(out).resolve()
    if out.exists():
        raise FileExistsError('Choose a new QA output directory')
    if not video.is_file():
        raise ValueError('Input must be an existing local video file')
    # The archived helper receives a private value, never the caller's dict.
    lesson = copy.deepcopy(data)
    expected = sha(video)
    with tempfile.TemporaryDirectory(prefix='math-video-qa-') as temporary:
        stage = Path(temporary)
        snapshot = stage/'input.mp4'
        shutil.copyfile(video, snapshot)
        if sha(snapshot) != expected or sha(video) != expected:
            raise ValueError('Movie changed while taking the QA snapshot')
        report = review_pack(snapshot, stage/'pack', lesson, every_seconds)
        if sha(video) != expected or sha(snapshot) != expected:
            raise ValueError('Movie changed during QA; no output pack published')
        if report['input_sha256'] != expected:
            raise ValueError('Decoded snapshot identity mismatch')
        report['input_guard'] = dict(
            method='private byte copy; original and snapshot SHA-256 checked before and after QA',
            source_sha256=sha(Path(__file__)),
            limitations='Not a filesystem lock, signature, adversarial race defense or content approval. '
                         'A temporary change restored between checks is not detected. '
                         'Final copying can leave an incomplete directory on I/O failure.')
        (stage/'pack/report.json').write_text(json.dumps(report, indent=2)+'\n')
        # copytree refuses an existing destination, including one created during QA.
        # Keep the success report last so failed artifact copying has no receipt.
        shutil.copytree(stage/'pack', out, ignore=shutil.ignore_patterns('report.json'))
        shutil.copyfile(stage/'pack/report.json', out/'report.json')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--lesson', type=Path, default=ROOT/'fft-latency/lesson.json')
    parser.add_argument('--every-seconds', type=int)
    args = parser.parse_args()
    # A resolved assembly lesson must not be re-formatted as a source template.
    data = json.loads(args.lesson.read_text())
    if args.lesson.resolve() == (ROOT/'fft-latency/lesson.json').resolve():
        data = load_lesson(args.lesson)
    report = stable_review_pack(args.video, args.out, data, args.every_seconds)
    print(f"Snapshot QA: {len(report['samples'])} encoded samples; human review still required.")


if __name__ == '__main__':
    main()
