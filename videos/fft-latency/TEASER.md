# FFT/latency · 28-second teaser storyboard

Current follow-on, 11 November: [first silent encoded test](TEASER_RENDER.md)
now exists. The text below is the retained 9–10 November preproduction record;
its “no movie” statements are historical, not current status.

**9 November 2026 · preproduction only · no teaser movie or audio exists.**
This is a separate proposed vertical edit, not a crop of the 80-second pilot.
The 60–90-second first milestone remains the unchanged v7 full explainer.
Nothing is uploaded, posted, scheduled, merged or approved here.

10 November follow-on: two [baseline/result still prototypes](VERTICAL_KEYFRAMES.md)
are now rendered and inspected at three widths. The other four layouts and
the full teaser movie are still not rendered; the storyboard below is retained.

Later 10 November: [all six source-frame layouts](TEASER_LAYOUTS.md) now
exist and are tested, including the four missing scenes. No teaser movie
or audio exists; earlier notes above are dated preproduction snapshots.

Inspected baseline: `a1ae076e794ebc5ccc3c45b65132694e3a8c0af0`;
original FFT work branch/PR #2: `97c8aea386535f8eca8ffd00478f36b56adc364e`.
Frozen source movie SHA256:
`1d3050b3094f1a090954cb9c2e6ed10e90d438169e86bd2cfbc2a7f13ed74036`.
[Full-video review](REVIEW.md) · [teaser data](teaser.json) ·
[provisional VTT](teaser.vtt). Approval never transfers automatically.

## One idea and one prediction

Changing a component changes only its contribution to a sequential total.
The hypothetical example stays 20+80=100 ms, then 10+80=90 ms. Overall
speedup is 100/90=10/9, approximately 1.11×, not 2×. No measured gain or
new FFT is announced. The full fraction formula and 1.25× ceiling stay in
the main video rather than being rushed into this teaser.

Concept placement: Fourier decomposition → FFT computation → pipeline
component → end-to-end latency. This is workload accounting, not a theorem
of numerical stability or evidence of real-time grid readiness.

## Proposed shots and exact resolved reading track

Proposed 1080×1920, 24 fps, 28 seconds / 672 frames **if rendered**.
Original labelled teal Fourier/amber other-work graphics, one common bar
scale and a separate large caption band. Persistent label:
“SYNTHETIC · NOT A BENCHMARK.” Never use color alone for meaning.
Keep a conservative central safe region; overlays/glyph fit need rendered QA.

| Time | Exact proposed caption | Visual direction / source beat |
|---|---|---|
| 0–4 s | Suppose Fourier work is 2× as fast. The whole system too? | Prediction without 90 ms or answer. Source hook, 0–8 s; not a clip in/out point. |
| 4–8 s | 20 ms Fourier + 80 ms other work = 100 ms. | Labelled baseline bar on fixed scale. Source baseline, 8–18 s. |
| 8–12 s | Fourier: 20 → 10 ms. Other work: 80 ms. | Static component change; arrow means old→new, not instantaneous measured time. Withhold new total. Source halve, 18–30 s. |
| 12–17 s | 10 + 80 = 90 ms total—not 2× overall speedup. | Settled before/after bars and large sum; no decorative intermediate totals. Source halve, 18–30 s. |
| 17–22 s | Sequential work. Same accuracy. No added overhead. Other work unchanged. | Four assumptions without a competing equation; inherited lesson assumptions/readiness context. |
| 22–28 s | Timing is not operation-count complexity, numerical stability, or validated grid readiness. | Four concept labels and a different-evidence closing card; synthetic model/FFTW accuracy source credit. No QR, guessed link or “watch now.” Source distinctions, 49–61 s. |

These are freshly proposed times. Source-scene references are semantic
reuse, not an assertion that existing footage fits a vertical crop. Do not
concatenate the original caption cuts blindly. Four seconds of prediction
and <=3 whitespace-words/s are provisional budgets, not comprehension tests.

Canonical teaser script: templates in teaser.json, resolved through unchanged
lesson_model.py. The VTT is an unrecorded silent reading proposal, not aligned
to any movie, speaker or soundtrack; its NOTE says so. No invented/cloned
voice. If authorized human narration is later chosen, listen and retime.

## Claims that must remain distinct

All four assumptions are explicit; parallel/overlapped work can need a
different latency model. The other 80 ms is not identified as communication,
EMT processing or any real control-room workload. No operator data is used.

| Claim | Relevant evidence |
|---|---|
| Arithmetic complexity | How operation counts grow with problem size |
| Numerical stability | Roundoff/error behavior of a specified computation |
| End-to-end latency | Elapsed time of the entire workload |
| Real-time grid readiness | Accuracy, system validation and worst-case deadlines in context |

This table is editorial context, not six seconds of extra on-screen text.
No claim that a mathematical breakthrough makes the grid real-time.

## Sources, provenance and reproduction

Rechecked 9 November 2026:

- [Unmerged Marimo source at inspected commit](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py): synthetic arithmetic/assumptions; not a verified hosted exercise.
- [FFTW authors' accuracy notes](https://fftw.org/accuracy/comments.html): accuracy context, not evidence for the invented timing numbers.
- [3Blue1Brown Fourier lesson](https://www.3blue1brown.com/lessons/fourier-transforms/): conceptual inspiration only; no borrowed footage/audio/distinctive assets.

No quotes, clips or episode/transcript offsets; discussion is not theorem
validation. No private research/notebook material. No new renderer, paid
service, dependency, license purchase or font/binary distribution selected.
Existing pins stay unchanged. Recheck official tool docs and licensing
before implementing/distributing a new render path; no blanket clearance.

From videos/, standard library only:

```sh
python fft_teaser.py --script
python fft_teaser.py --vtt
python fft_teaser.py --check
python -m unittest test_fft_teaser -v
```

The offline checker detects source/caption/timeline drift and excess
provisional reading rate. It does not render, publish or approve. After
deliberate script edits, inspect --vtt before updating teaser.vtt. Never
alter the full lesson to fit the teaser. Results: [STATUS.md](../STATUS.md).

- [ ] Editorial review of hook, arithmetic, scope and proposed pacing.
- [ ] Implement original vertical layouts; render and inspect frames/cuts.
- [ ] Check equation/label clipping and real-device full playback.
- [ ] If audio is added, listen and verify caption synchronization.
- [ ] Verify public destinations before adding any CTA.
- [ ] Rights and explicit exact-version/destination publication approval.

No technical storyboard blocker; rendering is not claimed unavailable.
Layout/render work is the next bounded step, not completed here. Full FFT
pilot and curves video remain unchanged and unapproved.
