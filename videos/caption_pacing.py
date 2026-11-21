"""Source-copy audit of full-pilot reading cues; not visual or audio certification."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from lesson_model import load_lesson
from render import caption_cues

ROOT=Path(__file__).resolve().parent
FOLDER=ROOT/'fft-latency'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def measure(start,end,text):
    a,b=Fraction(str(start)),Fraction(str(end))
    if b<=a or not text.strip():raise ValueError('Nonempty cue and positive duration required')
    duration=b-a
    return dict(start=float(a),end=float(b),text=text,characters=len(text),
                whitespace_tokens=len(text.split()),duration_exact=str(duration),
                cps_exact=str(Fraction(len(text))/duration),
                tokens_per_second_exact=str(Fraction(len(text.split()))/duration))


def report():
    lesson=load_lesson(FOLDER/'lesson.json')
    identity=json.loads((FOLDER/'review-version.json').read_text())
    copy=json.loads((FOLDER/'caption-proposals.json').read_text())
    if (copy['status']!='unadopted category-caption copy proposals'
            or copy['publication_approved'] is not False
            or copy['video_sha256']!=identity['video_sha256']):
        raise ValueError('Unadopted copy bound to frozen movie required')
    rows=[dict(index=i,**measure(a,b,t)) for i,(a,b,t) in enumerate(caption_cues(lesson))]
    if len(rows)!=19 or rows[0]['start']!=0 or rows[-1]['end']!=80:
        raise ValueError('Review changed pilot duration or cue structure')
    proposals=[]
    if len(copy['proposals'])!=4:raise ValueError('Exactly four category proposals required')
    for i,p in enumerate(copy['proposals']):
        expected=lesson['scenes'][5]['cards'][i]['title']
        if (p['category']!=expected or (p['start'],p['end'])!=(49+3*i,52+3*i)):
            raise ValueError('Proposal category/window mismatch')
        old=next(r for r in rows if (r['start'],r['end'])==(p['start'],p['end']))
        new=measure(p['start'],p['end'],p['text'])
        if new['characters']>=old['characters']:raise ValueError('Expected shorter copy proposal')
        proposals.append(dict(category=p['category'],original=old,proposed=new,
                              characters_removed=old['characters']-new['characters']))
    ranking=sorted(rows,key=lambda r:(-Fraction(r['cps_exact']),r['index']))
    return dict(source_commit=copy['source_commit'],video_sha256=copy['video_sha256'],
                publication_approved=False,status='source-copy audit; proposals unadopted',
                cue_count=len(rows),total_characters=sum(r['characters'] for r in rows),
                total_whitespace_tokens=sum(r['whitespace_tokens'] for r in rows),
                rows=rows,ranked_indices=[r['index'] for r in ranking],proposals=proposals,
                source_hashes={p:sha(ROOT/p) for p in ('caption_pacing.py','render.py','lesson_model.py',
                    'fft-latency/lesson.json','fft-latency/review-version.json','fft-latency/caption-proposals.json')},
                limitations='Unicode code-point and whitespace-token arithmetic only. No total '
                'screen-reading load, OCR, visual/layout review, normative rate threshold, '
                'speech synchronization, comprehension, accessibility or adoption approval.')


def markdown(r):
    lines=['# Full FFT pilot · caption-copy pacing audit','',
           '15 November 2026. **Source-copy audit; shorter proposals UNADOPTED.**', '',
           'Same frozen 80-second silent v7 movie; no render, retiming or canonical caption change.',
           'The 49–61 s category scene has the four highest caption character rates. This ranks review',
           'attention, not comprehension difficulty or failure against an accessibility threshold.', '',
           '## Four concrete copy proposals', '',
           '| Seconds | Current caption | Unadopted shorter caption | Characters before → after | CPS before → after |',
           '|---|---|---|---|---|']
    for p in r['proposals']:
        a,b=p['original'],p['proposed']
        lines.append(f"| {a['start']:g}–{a['end']:g} | {a['text']} | {b['text']} | {a['characters']} → {b['characters']} | {float(Fraction(a['cps_exact'])):.2f} → {float(Fraction(b['cps_exact'])):.2f} |")
    lines+=['','The proposals preserve four distinct questions, including the numerical qualifier on',
            'stability. They do not replace mathematical/editorial review, reduce the font-size concern',
            'or prove that three seconds is enough. Do not add them to the frozen movie/VTT/package',
            'without a controlled candidate update and new encoded/device review.', '',
            '## All current reading cues', '',
            '| Seconds | Caption text | Code points | Whitespace tokens | Code points/s |',
            '|---|---|---|---|---|']
    for c in r['rows']:
        lines.append(f"| {c['start']:g}–{c['end']:g} | {c['text']} | {c['characters']} | {c['whitespace_tokens']} | {float(Fraction(c['cps_exact'])):.2f} |")
    lines+=['',f"Total across cues: {r['total_characters']} code points; {r['total_whitespace_tokens']} whitespace tokens.",
            'These are cumulative cue-text counts, not unique words or all text on screen.', '',
            '## Measurement boundary and next review', '',
            '`len(text)` counts Unicode code points, including spaces and punctuation, before raster',
            'wrapping. `text.split()` counts whitespace tokens: numbers, symbols and hyphenated text',
            'can each be one token. Fractions preserve exact source durations/rates in the JSON report.',
            'There is no imported WPM/CPS pass threshold. Equations, unfamiliar concepts, bars, motion,',
            'persistent labels, source credits, repeated text and visual search are NOT included in',
            'this caption-only measure. Lower CPS does not establish lower cognitive load.', '',
            'Next: review the existing 49–61 s scene on the intended device, particularly whether',
            'the current title, active description and caption compete. If shorter copy is chosen,',
            'update lesson/captions/review/package together and rerender only that controlled candidate.',
            'No new layout or timing alternative is selected by this audit.', '',
            'The optional narration script is NOT an audio source. Its word-count budget cannot',
            'certify caption timing. [W3C SC 1.2.2 guidance](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html)',
            'addresses synchronized text for prerecorded audio; this silent reading-track count is',
            'not a WCAG compliance assessment. If authorized narration is recorded, captions must',
            'reflect its actual audio and timing, including meaningful non-speech sound where relevant.', '',
            '## Reproduce and provenance', '',
            f"Source baseline: `{r['source_commit']}`. Movie SHA256: `{r['video_sha256']}`.",
            '[Exact machine-readable audit and source hashes](caption-pacing-report.json);',
            '[editable unadopted proposals](caption-proposals.json). Original project copy only;',
            'no footage, music, voice, private data or research-agent conclusion added.', '',
            'From videos/:', '', '```sh',
            'uv run --locked python caption_pacing.py --check',
            'uv run --locked python -m unittest test_caption_pacing -v',
            '# Regenerate this derived audit after a deliberate source/proposal change:',
            'uv run --locked python caption_pacing.py --write', '```','',
            'Existing renderer/dependencies/lockfile retained. Official [Fraction docs](https://docs.python.org/3.12/library/fractions.html)',
            'and [Python licence](https://docs.python.org/3.12/license.html) checked 15 November;',
            'no new renderer, binary bundle, paid service or commercial/codec-rights clearance.',
            'Actual tests and next gates are in [STATUS.md](../STATUS.md). Earlier visual evidence',
            'remains dated evidence; no new decoded-frame, clipping, equation-legibility, device,',
            'full-playback or audio-sync review occurred. Frozen media/lesson/captions, narration',
            'choice, ending/live-lesson release gate, research, account settings and publication',
            'status remain unchanged. No guessed Open Notebook deployment or new automation.', '']
    return '\n'.join(lines)


def generated():
    r=report()
    return {'CAPTION_PACING.md':markdown(r),'caption-pacing-report.json':json.dumps(r,indent=2)+'\n'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--check',action='store_true');group.add_argument('--write',action='store_true')
    args=p.parse_args()
    for name,value in generated().items():
        path=FOLDER/name
        if args.check:
            if path.read_text()!=value:raise SystemExit('Derived audit drift: '+name)
        else:path.write_text(value)
    print('Source-copy audit matches; no reading-speed, accessibility or adoption approval implied.')
