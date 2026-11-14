"""Prepare an optional recording script, not audio or speech-aligned captions."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

from lesson_model import load_lesson
from render import caption_cues

ROOT=Path(__file__).resolve().parent
FOLDER=ROOT/'fft-latency'


def words(text):
    # Hyphens split spoken words; internal apostrophes remain one word.
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?",text)


def validate(data):
    if (data['status']!='unrecorded optional human-narration rehearsal draft'
            or data['publication_approved'] is not False or data['audio_recorded'] is not False):
        raise ValueError('Only unrecorded unapproved rehearsal copy supported')
    lesson=load_lesson(FOLDER/'lesson.json')
    identity=json.loads((FOLDER/'review-version.json').read_text())
    if data['source_video_sha256']!=identity['video_sha256']:
        raise ValueError('Frozen movie identity changed; rereview required')
    if hashlib.sha256((FOLDER/'lesson.json').read_bytes()).hexdigest()!=data['source_lesson_sha256']:
        raise ValueError('Lesson identity changed; rereview required')
    windows=[(start,end) for start,end,_ in caption_cues(lesson)]
    if data['duration']!=80 or [(c['start'],c['end']) for c in data['cues']]!=windows:
        raise ValueError('Rehearsal windows must match the existing pilot')
    rows=[]
    for c in data['cues']:
        pause=c['pause_seconds'];duration=c['end']-c['start']
        if isinstance(pause,bool) or not isinstance(pause,(int,float)) or not math.isfinite(pause) or not 0<=pause<duration:
            raise ValueError('Invalid planned pause')
        count=len(words(c['speech']));rate=60*count/(duration-pause)
        if not count or rate>data['mechanical_wpm_budget']:
            raise ValueError('Mechanical rehearsal budget exceeded')
        rows.append(dict(**c,words=count,mechanical_wpm=round(rate,2)))
    return rows


def script(data):
    rows=validate(data)
    lines=['# FFT pilot · optional human read', '',
           '**UNRECORDED REHEARSAL DRAFT · not audio-aligned captions or an adopted soundtrack.**','',
           'Windows are rehearsal targets, not observed speech timestamps. Pause after the cue text.', '',
           '| Target seconds | Original spoken copy | Planned trailing pause | Words / mechanical wpm |',
           '|---|---|---|---|']
    for c in rows:
        lines.append(f"| {c['start']:g}–{c['end']:g} | {c['speech']} | {c['pause_seconds']:g} s | {c['words']} / {c['mechanical_wpm']:g} |")
    count=sum(c['words'] for c in rows)
    pause=sum(c['pause_seconds'] for c in rows)
    lines+=['',f'Total: {count} mechanically counted words, {pause:g} s planned pauses, '
            f'{60*count/80:.2f} words/minute across the 80 s window.',
            'Counts/rates are planning arithmetic, not a validated speaking pace or a listening test.', '',
            'Read [NARRATION_BRIEF.md](NARRATION_BRIEF.md) before rehearsal. The ending is destination-neutral; '
            'the frozen movie still has an unresolved live-lesson CTA. Do not mix and release as-is.', '']
    return '\n'.join(lines)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    expected=script(json.loads((FOLDER/'narration.json').read_text()))
    if args.check:
        if (FOLDER/'NARRATION_SCRIPT.md').read_text()!=expected:
            raise SystemExit('Generated script differs from lesson-bound narration data')
        print('Rehearsal script matches data; no recording, synchronization or approval implied.')
    else:
        (FOLDER/'NARRATION_SCRIPT.md').write_text(expected)
