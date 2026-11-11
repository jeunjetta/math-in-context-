"""Timing-only alternative. No encode, publication or audio-alignment claim."""
import argparse
import hashlib
import json
from pathlib import Path

from fft_teaser import resolved, timestamp
import fft_teaser_layouts as layouts

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT / 'fft-latency'


def load():
    d = json.loads((FOLDER / 'teaser-pacing.json').read_text())
    candidate = json.loads((FOLDER / 'teaser-render/candidate.json').read_text())
    if (d['status'] != 'unrendered timing comparison' or d['publication_approved'] is not False
            or d['audio'] is not False or d['frozen_video_sha256'] != candidate['sha256']):
        raise ValueError('Draft-only comparison; frozen candidate identity required')
    if (d['scope_start'], d['focus_seconds'], d['duration'], d['fps']) != (22, 3, 34, 24):
        raise ValueError('Re-review mapping before changing timing')
    return d


def source_time(t):
    d = load()
    if not 0 <= t < d['duration']:
        raise ValueError('Outside comparison')
    return t if t < 22 else 22 + (t - 22) / 2


def frame(n):
    d = load()
    if type(n) is not int or not 0 <= n < d['duration'] * d['fps']:
        raise ValueError('Outside comparison frames')
    im, record = layouts.render_frame(source_time(n / d['fps']))
    return im, dict(record, comparison_frame=n, comparison_seconds=n/d['fps'],
                   source_seconds=source_time(n/d['fps']))


def cues():
    rows = resolved()['cues']
    rows[-1]['end'] = load()['duration']
    return rows


def vtt():
    lines = ['WEBVTT', '', 'NOTE Unrendered 34-second silent timing comparison; not aligned to speech.', '']
    for c in cues():
        lines += [f"{timestamp(c['start'])} --> {timestamp(c['end'])}", c['caption'], '']
    return '\n'.join(lines)


def report():
    d = load(); data = layouts.load(); old = resolved()
    # Whitespace-token counts are reproducible descriptors, not reading-time predictions.
    count = lambda s: len(s.split())
    persistent = [old['persistent_label'], *data['headlines']['scope'],
                  *(c['title'] for c in data['scope']), *data['credits'], old['cues'][-1]['caption']]
    rows = []
    for i, card in enumerate(data['scope']):
        words = count(card['description'])
        rows.append(dict(title=card['title'], description=card['description'],
                         description_tokens=words, baseline_start=22+1.5*i,
                         comparison_start=22+3*i, baseline_hold=1.5, comparison_hold=3,
                         baseline_description_tokens_per_second=words/1.5,
                         comparison_description_tokens_per_second=words/3))
    sources = ['fft_teaser_pacing.py', 'fft-latency/teaser-pacing.json',
               'fft_teaser_layouts.py', 'fft-latency/teaser-layouts.json',
               'fft_teaser.py', 'fft-latency/teaser.json', 'fft-latency/lesson.json',
               'fft-latency/teaser-render/candidate.json']
    return dict(status=d['status'], publication_approved=False, audio=False,
                source_commit=d['source_commit'], frozen_video_sha256=d['frozen_video_sha256'],
                baseline_duration=28, comparison_duration=34, comparison_frames=816,
                scope_persistent_tokens=sum(map(count, persistent)),
                scope_description_tokens=sum(r['description_tokens'] for r in rows),
                closing_caption_tokens=count(old['cues'][-1]['caption']), rows=rows,
                source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources})


def markdown():
    r = report()
    lines = ['# FFT teaser · slower closing comparison', '',
        '11 November 2026. **Unrendered timing alternative, not a reviewed video.**', '',
        'The existing 28-second encoded draft and both full candidates are unchanged.',
        'This version keeps 0–22 s identical, then doubles each closing focus from',
        '1.5 to 3 seconds. Total: 34 seconds / 816 frames at 24 fps. It is not',
        'the primary 80-second explainer or a proposed replacement without review.', '',
        '| Focus | Existing start / hold | Alternative start / hold | Description tokens |',
        '|---|---|---|---|']
    for row in r['rows']:
        lines.append(f"| {row['title']} | {row['baseline_start']:g} s / 1.5 s | {row['comparison_start']} s / 3 s | {row['description_tokens']} |")
    lines += ['', '## What the measurement means', '',
        f"The closing card has {r['scope_persistent_tokens']} persistent whitespace tokens,",
        f"including its {r['closing_caption_tokens']}-token caption, plus {r['scope_description_tokens']} description tokens",
        'across four changing focuses. Persistent titles/caption/credits are counted',
        'once over the entire closing scene, not charged again to each focus.',
        'The report separately counts description tokens per focus: doubling the',
        'hold halves that mechanical rate. It does not halve comprehension time.', '',
        'These are whitespace-token counts, not validated reading-speed thresholds.',
        'Concurrent caption, hierarchy, visual search, revisiting titles, unfamiliar',
        'concepts and credits compete for attention. Symbols and numbers are not',
        'equally difficult words. Longer holds may help, bore or still be inadequate.',
        'Only real playback/comprehension feedback can choose between versions.', '',
        '## Inspect and reproduce', '',
        'From videos/:', '', '```sh',
        'uv run --locked python fft_teaser_pacing.py --check',
        'uv run --locked python -m unittest test_fft_teaser_pacing -v',
        '```', '',
        '[Structured timing](teaser-pacing.json), [audit report](teaser-pacing-report.json),',
        '[alternative silent VTT](teaser-pacing.vtt), [frozen encoded draft](TEASER_RENDER.md).',
        'The Python frame(n) interface maps the alternative timeline onto the',
        'unchanged original renderer, without monkey-patching or editing frozen',
        'helpers. Incoming phases own exact cuts at 22, 25, 28 and 31 seconds.',
        'It returns original source metadata plus explicitly named comparison time.', '',
        'No new MP4, encoded QA, continuous playback, device test or audio exists',
        'for this alternative. No technical render blocker: the bounded deliverable',
        'is tested timing/source-frame mapping and a storyboard, not another encode.', '',
        '## Sources, rights and remaining gates', '',
        'Same synthetic sequential 20+80→10+80=90 ms model, unchanged accuracy,',
        'other-work and overhead assumptions; no real telemetry or readiness claim.',
        'Concept path: Fourier algorithms → component cost → end-to-end latency;',
        'numerical stability and validated grid readiness remain separate questions.',
        'Educational sources remain [the pilot](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py)',
        'and [FFTW accuracy context](https://fftw.org/accuracy/comments.html), not evidence of a new FFT.',
        'No creator footage, music or narration added. Existing pinned Pillow 12.3.0',
        'and external DejaVu fonts retained; no dependency or binary distribution.',
        '[Current official drawing docs](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html)',
        'and [licensing](https://pillow.readthedocs.io/en/stable/about.html#license)',
        'rechecked 11 November; current stable docs describe 13.0.0, not the pinned runtime.',
        'No blanket commercial-rights clearance is implied.', '',
        'Next: encode this alternative separately and inspect actual cut/end frames',
        'before asking Karin to compare complete tablet playback. Do not overwrite',
        'the frozen draft. Human/editorial/math/rights review, audio and destination',
        'choices, stacked-parent reconciliation and exact-version publication approval',
        'remain open. Nothing published or merged.']
    return '\n'.join(lines)+'\n'


def generated():
    return {'TEASER_PACING.md':markdown(), 'teaser-pacing-report.json':json.dumps(report(),indent=2)+'\n',
            'teaser-pacing.vtt':vtt()}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true'); p.add_argument('--write', action='store_true')
    args = p.parse_args()
    if args.check == args.write: p.error('Choose --check or --write')
    for name, content in generated().items():
        dest = FOLDER/name
        if args.write: dest.write_text(content)
        elif not dest.exists() or dest.read_text() != content:
            raise SystemExit('Generated comparison drift: '+name)
    print('Timing comparison sources agree; no rendered or editorial approval implied.')
