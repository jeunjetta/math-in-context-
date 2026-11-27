"""Optional after-video arithmetic; does not change any rendering data.

Pure evaluate() is reusable from a future Marimo cell without Marimo imports.
This file does not compute an FFT, measure runtime or test numerical stability.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path

from lesson_model import compact, metrics, number, quotient

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT/'fft-latency'
OUTPUT = FOLDER/'OVERHEAD_CHECK.md'


def evaluate(model, overhead_ms):
    """Same sequential toy workload, plus nonnegative NEW time on new path."""
    h = number(overhead_ms)
    if h < 0:
        raise ValueError('Added overhead must be nonnegative')
    m = metrics(model)
    total = m['new_total'] + h
    return dict(overhead=h, total=total, saved=m['baseline']-total,
                speedup=m['baseline']/total, break_even=m['saved'],
                outcome='faster' if total < m['baseline'] else
                        'break-even' if total == m['baseline'] else 'slower')


def load():
    spec = json.loads((FOLDER/'overhead-check.json').read_text())
    report = json.loads((FOLDER/'source-only-review/render-report.json').read_text())
    lesson = json.loads((FOLDER/'source-only-review/resolved-lesson.json').read_text())
    if (spec['status'] != 'unadopted optional after-video exercise'
            or spec['publication_approved'] is not False
            or report['publication_approved'] is not False
            or spec['movie_sha256'] != report['sha256']
            or spec['changed_assumption'] != 'No added overhead'
            or spec['changed_assumption'] not in lesson['assumptions']):
        raise ValueError('Exercise scope or reference changed; review before regeneration')
    for h in spec['overheads_ms']:
        row = evaluate(lesson, h)
        if any(Fraction(compact(row[k])) != row[k] for k in ('overhead', 'total')):
            raise ValueError('Displayed times must be exact to at most two decimals')
    probe = evaluate(lesson, spec['prediction_overhead_ms'])
    m = metrics(lesson)
    choices = [number(c) for c in spec['prediction_choices_ms']]
    if (probe['overhead'] not in [number(h) for h in spec['overheads_ms']]
            or len(choices) != 3 or len(set(choices)) != 3
            or set(choices) != {m['new_total'], probe['total'], m['baseline']+probe['overhead']}):
        raise ValueError('Prediction must have exactly one matching answer')
    return spec, lesson


def document(spec, lesson):
    m = metrics(lesson)
    probe = evaluate(lesson, spec['prediction_overhead_ms'])
    lines = [
        '# What if the faster step adds overhead?', '',
        '23 November 2026. **Optional draft after-video exercise; not approved for publication.**', '',
        'Watch the existing 80-second FFT/latency pilot first if available. '
        'This text also stands alone; it is not another movie, a live app or a required review step.', '',
        '## Predict before scrolling to the answer', '',
        f"The synthetic baseline is {compact(m['baseline'])} ms: {compact(m['fourier'])} ms "
        f"of Fourier work and {compact(m['other'])} ms of other work. "
        f"The Fourier step becomes {compact(m['kernel_gain'])} times as fast.", '',
        f"Now add **{compact(probe['overhead'])} ms of new overhead**. "
        'What is the new end-to-end time? Choose '
        + ', '.join(compact(number(c))+' ms' for c in spec['prediction_choices_ms'])+'.', '',
        'How much new overhead would exactly erase the time saving?', '',
        'Change only the no-added-overhead assumption. Work is still sequential; '
        'other work and accuracy remain unchanged. '+spec['overhead_definition'], '',
        '## Answer and feedback', '',
        f"**{compact(probe['total'])} ms**: {compact(m['new_fourier'])} + "
        f"{compact(m['other'])} + {compact(probe['overhead'])} = {compact(probe['total'])} ms.", '',
        f"Choosing {compact(m['new_total'])} ms omits the new overhead. "
        f"Choosing {compact(m['baseline']+probe['overhead'])} ms adds overhead but forgets to "
        f"divide Fourier time by {compact(m['kernel_gain'])}.", '',
        f"The Fourier change saves {compact(m['saved'])} ms before overhead. "
        f"Exactly **{compact(m['saved'])} ms of new overhead** consumes that saving. "
        'Less gives a net time reduction; more makes this toy workload slower.', '',
        '| New overhead | New total | Old time / new time | Net result versus baseline |',
        '|---:|---:|---:|---|'
    ]
    for h in spec['overheads_ms']:
        row = evaluate(lesson, h)
        lines.append(f"| {compact(row['overhead'])} ms | {compact(row['total'])} ms | "
                     f"{quotient(m['baseline'], row['total'])} | {row['outcome']} |")
    lines += ['',
        'For fixed extra overhead h, the accounting is T_new = T_old - F + F/s + h. '
        'Here F is the original Fourier time and s its speedup. '
        'Net improvement requires h < F(1 - 1/s); equality is break-even. '
        'All times use the same units. We do not assume overhead stays fixed as input size or s changes.', '',
        'This is reproduced arithmetic, not benchmark evidence. A speedup factor below one '
        'means slower, not a negative runtime. Overlapped or parallel work needs a critical-path '
        'model instead of this sequential sum. Same accuracy is assumed, not demonstrated.', '',
        'Concept placement: Fourier computation → component time saving → overhead budget → '
        'end-to-end latency. These are method/application links, not equivalences. '
        'The calculation establishes neither arithmetic-complexity improvement, numerical '
        'stability nor validated real-time grid readiness. No operational recommendation.', '',
        '## Sources and reuse', '',
        '- [Original synthetic notebook source](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py): '
        'baseline and assumptions; source code, not a deployed lesson.',
        '- [FFTW authors’ accuracy context](https://fftw.org/accuracy/comments.html): '
        'separate implementation-error question, not support for these hypothetical times.', '',
        'No external text, imagery, voice or footage is copied. No learner responses are collected. '
        'This is not a validated assessment, accessibility certification or evidence that anyone understood the film.', '',
        '## Producer notes — not extra movie content', '',
        f"Reference movie SHA-256: `{spec['movie_sha256']}`. "
        f"Source baseline: `{spec['source_commit']}`. "
        'Movie, captions, description/package and existing notebook stay unchanged. '
        'This exercise is not inserted into the film or a publication package.', '',
        'Edit `overhead-check.json`; the small standard-library generator separates exercise data '
        'from Markdown. From `videos/`, run `python3 overhead_check.py` to regenerate, '
        '`python3 overhead_check.py --check` to detect drift, and '
        '`python3 -m unittest test_overhead_check -v` to test. '
        '`evaluate(model, overhead_ms)` returns exact fractions for reuse in a future Marimo cell; '
        'no Marimo app/export or deployment was created or tested.', '',
        'Python [Fraction documentation](https://docs.python.org/3/library/fractions.html) '
        'and FFTW context checked 23 November 2026. Existing dependency/renderer licensing is unchanged; '
        'no new commercial-use clearance is claimed. Next: editorial review of this check alongside '
        'the existing intended-device review, then adopt or discard it separately. '
        'All video release gates remain open.', ''
    ]
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = document(*load())
    if args.check:
        if OUTPUT.read_text() != text:
            raise SystemExit('Overhead exercise is stale')
    else:
        OUTPUT.write_text(text)
    print('Overhead exercise matches the toy model; no learner or release approval implied.')


if __name__ == '__main__':
    main()
