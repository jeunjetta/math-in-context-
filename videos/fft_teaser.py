"""Offline preproduction script/VTT checks, not a renderer or publishing tool."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from lesson_model import context

ROOT=Path(__file__).resolve().parent/'fft-latency'


def resolved(data=None):
    data=deepcopy(data if data is not None else json.loads((ROOT/'teaser.json').read_text()))
    lesson=json.loads((ROOT/'lesson.json').read_text())
    identity=json.loads((ROOT/'review-version.json').read_text())
    if data['source_lesson_sha256']!=hashlib.sha256((ROOT/'lesson.json').read_bytes()).hexdigest():
        raise ValueError('Source lesson changed; re-review teaser')
    if data['source_video_sha256']!=identity['video_sha256']:
        raise ValueError('Source video changed; re-review teaser')
    if (data['publication_approved'] is not False or data['audio'] is not False or
        data['status']!='unrendered storyboard' or data['public_video_url'] is not None or
        data['interactive_lesson_url'] is not None):
        raise ValueError('This workflow is unrendered, silent and draft-only')
    if data['duration']!=28 or data['fps']!=24 or data['proposed_canvas']!=[1080,1920]:
        raise ValueError('Review proposed timeline/layout before changing format')
    values=context(lesson);expected=0;ids=set()
    scenes={s['id'] for s in lesson['scenes']}
    for cue in data['cues']:
        if (type(cue['start']) is not int or type(cue['end']) is not int or
            cue['start']!=expected or cue['end']<=cue['start'] or
            cue['id'] in ids or cue['source_scene'] not in scenes):
            raise ValueError('Invalid teaser cue/source mapping')
        cue['caption']=cue['caption'].format_map(values)
        if len(cue['caption'].split())/(cue['end']-cue['start'])>3:
            raise ValueError('Provisional reading budget exceeded; not a comprehension test')
        expected=cue['end'];ids.add(cue['id'])
    if expected!=data['duration'] or len(data['cues'])!=6:
        raise ValueError('Six cues must cover the proposed teaser')
    return data


def timestamp(seconds):
    return f'00:{seconds//60:02}:{seconds%60:02}.000'


def vtt(data=None):
    data=resolved(data)
    lines=['WEBVTT','','NOTE Provisional silent reading track. No matching teaser movie or audio exists.','']
    for cue in data['cues']:
        lines += [f"{timestamp(cue['start'])} --> {timestamp(cue['end'])}",cue['caption'],'']
    return '\n'.join(lines)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--vtt',action='store_true')
    group.add_argument('--script',action='store_true')
    group.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.vtt:print(vtt(),end='')
    elif args.script:
        for cue in resolved()['cues']:
            print(f"{cue['start']:02}–{cue['end']:02} s: {cue['caption']}")
    elif (ROOT/'teaser.vtt').read_text()!=vtt():
        raise SystemExit('Provisional VTT differs; inspect --vtt')
    else:print('Teaser script/VTT/source agree. No render or approval implied.')
