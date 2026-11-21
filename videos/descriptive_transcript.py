"""Generate a draft visual text alternative, not speech or an approved release."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT/'fft-latency'
OUTPUT = FOLDER/'DESCRIPTIVE_TRANSCRIPT.md'
MANIFEST_SHA = '2456b23798529acc23853d5bdb5ac521b0ef5d3fdf08160bc51e7ee122a5e13a'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(root=ROOT):
    folder=Path(root)/'fft-latency'
    path=folder/'source-only-review/render-report.json'
    if sha(path)!=MANIFEST_SHA:
        raise ValueError('Source-only render manifest changed; re-review text scope')
    report=json.loads(path.read_text())
    for relative,digest in report['source_hashes'].items():
        if sha(Path(root)/relative)!=digest:
            raise ValueError('Rendering source drift: '+relative)
    for name,key in (('resolved-lesson.json','resolved_lesson_sha256'),
                     ('fft-source-only-review.vtt','captions_sha256')):
        if sha(path.parent/name)!=report[key]:
            raise ValueError('Resolved content drift: '+name)
    lesson=json.loads((path.parent/'resolved-lesson.json').read_text())
    spec=json.loads((folder/'descriptive-transcript.json').read_text())
    validate(spec,lesson,report)
    ending=json.loads((folder/'source-endcard.json').read_text())
    return spec,lesson,report,ending


def validate(spec,lesson,report):
    if (spec['publication_approved'] is not False or report['publication_approved'] is not False
            or spec['status']!='unadopted descriptive text alternative'
            or spec['movie_sha256']!=report['sha256'] or report['media']['audio_streams']!=0):
        raise ValueError('Only this unadopted silent review is in scope')
    if [s['id'] for s in spec['scenes']]!=[s['id'] for s in lesson['scenes']]:
        raise ValueError('Visual descriptions must cover every scene once, in order')
    if any(not isinstance(s['visual_description'],str) or not s['visual_description'].strip()
           for s in spec['scenes']):
        raise ValueError('Each scene needs a visual description')


def cues(scene):
    step=(scene['end']-scene['start'])/len(scene['captions'])
    return [(scene['start']+i*step,scene['start']+(i+1)*step,text)
            for i,text in enumerate(scene['captions'])]


def document(spec,lesson,report,ending):
    lines=['# FFT and whole-workload latency · descriptive text alternative','',
        '21 November 2026. **Draft for the unadopted source-only review, not an approved release.**','',
        'This video has no audio. The text below combines its on-screen caption track with '
        'descriptions of the important visual information. It is not a speech transcript, '
        'an audio-description recording, a new cut or an accessibility certification. '
        'Time windows locate content; they do not pace or limit reading.','',
        f"Reference file: `{report['filename']}` · 80 seconds. SHA-256: `{report['sha256']}`.",'',
        f"Source baseline: `{spec['source_commit']}`. Movie and existing captions are unchanged.",'',
        '## Assumptions and persistent labels','',
        '; '.join(lesson['assumptions'])+'. All times are synthetic milliseconds, not grid telemetry. '
        'The early scenes carry a VISUAL DRAFT marker and a synthetic/no-telemetry footer. '
        'An advancing bottom line indicates elapsed video progress, not measured workload latency. '
        'The ending instead labels the example SYNTHETIC · NOT A BENCHMARK.','']
    for visual,scene in zip(spec['scenes'],lesson['scenes']):
        lines += [f"## {scene['start']:g}–{scene['end']:g} seconds · {scene['heading']}",'',
                  'Visual description: '+visual['visual_description'],'',
                  'On-screen caption track (not speech):','']
        for i,(start,end,text) in enumerate(cues(scene)):
            lines += [f'- {start:g}–{end:g} s: {text}']
            if 'cards' in scene:
                card=scene['cards'][i]
                lines += [f"  Active panel: {card['title']} — {card['description']}."]
        lines += ['']
    lines += ['## Sources and review limits','',
        f"- [Synthetic notebook source]({ending['notebook']['url']}): public Python/Marimo code, not a deployed lesson.",
        f"- [FFTW authors’ numerical-accuracy context]({ending['accuracy_context_url']}): not validation of the hypothetical timings.",
        '- [3Blue1Brown Fourier lesson](https://www.3blue1brown.com/lessons/fourier-transforms/): educational inspiration, no reused visuals or clips.','',
        'The separate [playback worksheet](SOURCE_PLAYBACK_REVIEW.md) identifies this exact copy. '
        'Human equivalence/editorial review and assistive-technology testing remain open, alongside '
        'device playback, source-only adoption, rights/audio decisions and publication approval. '
        'No accessibility gate is automatically cleared.','',
        'Production note: visual copy is editable in `descriptive-transcript.json`; '
        'headings, 19 caption cues, four active panels and source links are derived from pinned '
        'review data. Regenerate with `python3 descriptive_transcript.py`; check freshness with '
        '`python3 descriptive_transcript.py --check`. No rendering dependency is needed.','',
        'Method informed by current [W3C WAI transcript guidance](https://www.w3.org/WAI/media/av/transcripts/) '
        'and [video-only alternatives guidance](https://www.w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html), '
        'checked 21 November 2026. These distinguish visual description from caption text; '
        'this draft is not a conformance determination.','']
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    expected=document(*load())
    if args.check:
        if OUTPUT.read_text()!=expected:
            raise SystemExit('Stale descriptive text alternative')
    else:
        OUTPUT.write_text(expected)
    print('Eight visual descriptions and 19 on-screen cues match this draft; no approval implied.')


if __name__=='__main__':
    main()
