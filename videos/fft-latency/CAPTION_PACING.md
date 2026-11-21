# Full FFT pilot · caption-copy pacing audit

15 November 2026. **Source-copy audit; shorter proposals UNADOPTED.**

Same frozen 80-second silent v7 movie; no render, retiming or canonical caption change.
The 49–61 s category scene has the four highest caption character rates. This ranks review
attention, not comprehension difficulty or failure against an accessibility threshold.

## Four concrete copy proposals

| Seconds | Current caption | Unadopted shorter caption | Characters before → after | CPS before → after |
|---|---|---|---|---|
| 49–52 | Arithmetic complexity asks how operation counts grow. | Complexity: how operation counts grow. | 53 → 38 | 17.67 → 12.67 |
| 52–55 | Numerical stability asks how computation errors behave. | Numerical stability: computation error growth. | 55 → 46 | 18.33 → 15.33 |
| 55–58 | Latency measures elapsed time for the whole workload. | Latency: elapsed time for the whole job. | 53 → 40 | 17.67 → 13.33 |
| 58–61 | Readiness needs validation against system deadlines. | Readiness: validated system and deadlines. | 52 → 42 | 17.33 → 14.00 |

The proposals preserve four distinct questions, including the numerical qualifier on
stability. They do not replace mathematical/editorial review, reduce the font-size concern
or prove that three seconds is enough. Do not add them to the frozen movie/VTT/package
without a controlled candidate update and new encoded/device review.

## All current reading cues

| Seconds | Caption text | Code points | Whitespace tokens | Code points/s |
|---|---|---|---|---|
| 0–4 | Suppose Fourier computation becomes 2× as fast. | 47 | 7 | 11.75 |
| 4–8 | Does the whole system become 2× as fast? Pause and predict. | 59 | 11 | 14.75 |
| 8–13 | Imagine sequential work taking 100 milliseconds. | 48 | 6 | 9.60 |
| 13–18 | Fourier work takes 20 ms. Everything else takes 80 ms. | 54 | 10 | 10.80 |
| 18–22 | Divide Fourier time by 2: 20 ms becomes 10 ms. | 46 | 10 | 11.50 |
| 22–26 | The other 80 milliseconds stays unchanged. | 42 | 6 | 10.50 |
| 26–30 | 10 + 80 = 90 ms. We saved 10 milliseconds. | 42 | 10 | 10.50 |
| 30–35 | Overall speedup is old time divided by new time. | 48 | 9 | 9.60 |
| 35–40 | 100 divided by 90 is about 1.11×, not 2×. | 41 | 9 | 8.20 |
| 40–44.5 | Even zero Fourier time leaves 80 milliseconds. | 46 | 7 | 10.22 |
| 44.5–49 | In this model, the speedup limit is about 1.25×. | 48 | 9 | 10.67 |
| 49–52 | Arithmetic complexity asks how operation counts grow. | 53 | 7 | 17.67 |
| 52–55 | Numerical stability asks how computation errors behave. | 55 | 7 | 18.33 |
| 55–58 | Latency measures elapsed time for the whole workload. | 53 | 8 | 17.67 |
| 58–61 | Readiness needs validation against system deadlines. | 52 | 6 | 17.33 |
| 61–65.5 | Check accuracy, data movement, and worst-case deadlines. | 56 | 7 | 12.44 |
| 65.5–70 | This toy arithmetic proves no new FFT or real-time grid capability. | 67 | 11 | 14.89 |
| 70–75 | Explore the fraction improved and its speedup in our Marimo lesson. | 67 | 11 | 13.40 |
| 75–80 | Fourier methods connect algorithms to latency—not automatically to readiness. | 77 | 9 | 15.40 |

Total across cues: 1001 code points; 160 whitespace tokens.
These are cumulative cue-text counts, not unique words or all text on screen.

## Measurement boundary and next review

`len(text)` counts Unicode code points, including spaces and punctuation, before raster
wrapping. `text.split()` counts whitespace tokens: numbers, symbols and hyphenated text
can each be one token. Fractions preserve exact source durations/rates in the JSON report.
There is no imported WPM/CPS pass threshold. Equations, unfamiliar concepts, bars, motion,
persistent labels, source credits, repeated text and visual search are NOT included in
this caption-only measure. Lower CPS does not establish lower cognitive load.

Next: review the existing 49–61 s scene on the intended device, particularly whether
the current title, active description and caption compete. If shorter copy is chosen,
update lesson/captions/review/package together and rerender only that controlled candidate.
No new layout or timing alternative is selected by this audit.

The optional narration script is NOT an audio source. Its word-count budget cannot
certify caption timing. [W3C SC 1.2.2 guidance](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html)
addresses synchronized text for prerecorded audio; this silent reading-track count is
not a WCAG compliance assessment. If authorized narration is recorded, captions must
reflect its actual audio and timing, including meaningful non-speech sound where relevant.

## Reproduce and provenance

Source baseline: `85f1868ea816a52c581ed64cbde3d21b567a40c4`. Movie SHA256: `1d3050b3094f1a090954cb9c2e6ed10e90d438169e86bd2cfbc2a7f13ed74036`.
[Exact machine-readable audit and source hashes](caption-pacing-report.json);
[editable unadopted proposals](caption-proposals.json). Original project copy only;
no footage, music, voice, private data or research-agent conclusion added.

From videos/:

```sh
uv run --locked python caption_pacing.py --check
uv run --locked python -m unittest test_caption_pacing -v
# Regenerate this derived audit after a deliberate source/proposal change:
uv run --locked python caption_pacing.py --write
```

Existing renderer/dependencies/lockfile retained. Official [Fraction docs](https://docs.python.org/3.12/library/fractions.html)
and [Python licence](https://docs.python.org/3.12/license.html) checked 15 November;
no new renderer, binary bundle, paid service or commercial/codec-rights clearance.
Actual tests and next gates are in [STATUS.md](../STATUS.md). Earlier visual evidence
remains dated evidence; no new decoded-frame, clipping, equation-legibility, device,
full-playback or audio-sync review occurred. Frozen media/lesson/captions, narration
choice, ending/live-lesson release gate, research, account settings and publication
status remain unchanged. No guessed Open Notebook deployment or new automation.
