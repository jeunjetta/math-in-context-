# FFT/latency pilot · editorial handoff

**DRAFT FOR KARIN'S REVIEW · not approved for publication.**

Prepared 30 October 2026 from video source commit
`448987cc64d01e6162614eedfc831b9c3172e981`.
This handoff describes the existing **v4, 80-second silent captioned draft**;
it does not introduce a new render, voice or mathematical claim.
Read this page on GitHub without installing anything. Open the review video
from the accompanying ChatGPT message; it is not a public YouTube upload.

## Three decisions, when convenient

- [ ] Message and pacing: keep as-is, or note the first confusing timestamp.
- [ ] Audio format: keep silent, record an authorized human narrator, or retain both versions.
- [ ] Release readiness: approve only after the blockers below are resolved.

These boxes deliberately remain unchecked. Test results are not Karin's approval.

## The one idea

Improving one component does not improve the entire workload by the same
factor. Our synthetic sequential example is 20 ms of Fourier computation
plus 80 ms of other work. Halving the Fourier time gives 10 + 80 = 90 ms:
10% less elapsed time, or about **1.11× overall speedup**, not 2×.
Those two ways of stating the improvement are not interchangeable percentages.

Assumptions: sequential work, unchanged accuracy, no added overhead, and
unchanged other work. The 1.25× ceiling is a mathematical limit of this
toy model, not predicted performance of an engineering system.

Concept placement: Fourier decomposition → FFT computation → a pipeline
component → end-to-end latency. It connects a method to an application;
it does not equate fast computation with operational readiness.

## Shot-level review

Watch once without pausing; then revisit only the rows that felt unclear.
Mark feedback in [PR #2](https://github.com/jeunjetta/math-in-context-/pull/2),
for example: “35 s — equation needs another second.”

| Time | What should land | What to check on a tablet |
|---|---|---|
| 00:00–00:08 | A genuine prediction question | Does the opening invite an answer without revealing it? |
| 00:08–00:18 | 20 ms + 80 ms = 100 ms | Can you identify both labelled parts without relying only on color? |
| 00:18–00:30 | Only the Fourier block shrinks; total is 90 ms | Is the unchanged 80 ms visually obvious on the shared time scale? |
| 00:30–00:40 | 100/90 ≈ 1.11×; f=0.20 and s=2 | Is the equation readable before the next cut? |
| 00:40–00:49 | Even an instant Fourier step leaves 80 ms | Is the 1.25× ceiling understood as a model limit? |
| 00:49–01:01 | Complexity, stability, latency and readiness differ | Does each highlighted card match the caption? Are 3 seconds per card enough? |
| 01:01–01:10 | Engineering needs more than a runtime improvement | Is it clear there is no real-grid benchmark or readiness claim? |
| 01:10–01:20 | Context, sources and a next experiment | The live Marimo call-to-action is still a blocker, not a verified link. |

## Exact current script / captions

This is a reading transcript of the canonical caption cues, not a recorded
narration. If a human voice is chosen, adapt pronunciation naturally and then
align captions to the actual audio; do not assume these silent timings fit it.

<!-- BEGIN CANONICAL CAPTIONS -->
**00:00–00:04**
Suppose Fourier computation becomes 2× as fast.

**00:04–00:08**
Does the whole system become 2× as fast? Pause and predict.

**00:08–00:13**
Imagine sequential work taking 100 milliseconds.

**00:13–00:18**
Fourier work takes 20 ms. Everything else takes 80 ms.

**00:18–00:22**
Divide Fourier time by 2: 20 ms becomes 10 ms.

**00:22–00:26**
The other 80 milliseconds stays unchanged.

**00:26–00:30**
10 + 80 = 90 ms. We saved 10 milliseconds.

**00:30–00:35**
Overall speedup is old time divided by new time.

**00:35–00:40**
100 divided by 90 is about 1.11×, not 2×.

**00:40–00:44.500**
Even zero Fourier time leaves 80 milliseconds.

**00:44.500–00:49**
In this model, the speedup limit is about 1.25×.

**00:49–00:52**
Arithmetic complexity asks how operation counts grow.

**00:52–00:55**
Numerical stability asks how computation errors behave.

**00:55–00:58**
Latency measures elapsed time for the whole workload.

**00:58–01:01**
Readiness needs validation against system deadlines.

**01:01–01:05.500**
Check accuracy, data movement, and worst-case deadlines.

**01:05.500–01:10**
This toy arithmetic proves no new FFT or real-time grid capability.

**01:10–01:15**
Explore the fraction improved and its speedup in our Marimo lesson.

**01:15–01:20**
Fourier methods connect algorithms to latency—not automatically to readiness.
<!-- END CANONICAL CAPTIONS -->

## Draft YouTube packaging — NOT FOR PUBLICATION YET

**Candidate title:** Twice as fast… but only 10 ms saved?

**Draft description:**

A 2× faster Fourier step does not automatically make a whole system 2× faster.
In this synthetic example, a 100 ms sequential pipeline spends 20 ms on Fourier
computation and 80 ms elsewhere. Halve the Fourier time and the total becomes
90 ms: about 1.11× overall speedup.

We distinguish operation counts, numerical stability, elapsed latency and
validated real-time readiness. Assumptions: same accuracy, unchanged other
work and no added overhead. This is an arithmetic lesson, not a new FFT
benchmark, a verified AI mathematics breakthrough or a real-grid capability claim.

Interactive lesson: **[ADD_VERIFIED_LESSON_URL_BEFORE_PUBLICATION]**

Further reading and credits:

- Our [worked example and source code](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py) — currently in unmerged PR #1; source code is not a hosted interactive lesson.
- [FFTW authors' accuracy notes](https://fftw.org/accuracy/comments.html) — primary implementation/accuracy context, not evidence for the invented timing numbers.
- [3Blue1Brown's Fourier lesson](https://www.3blue1brown.com/lessons/fourier-transforms/) — educational inspiration; no footage, audio or distinctive assets reused.
- Original synthetic graphics and explanation: Math in Context.

**Timing index for reviewers — not YouTube chapter metadata:**
00:00 Predict · 00:08 Baseline · 00:18 Change one step · 00:30 Overall gain ·
00:40 Ceiling · 00:49 Four different tests · 01:01 Engineering context · 01:10 Explore.

## Source and claim checks

Source URLs above were retrieved on 30 October 2026. Our numerical example is
an exact reproduced calculation, not measured data. FFTW's notes support
keeping floating-point behavior distinct from runtime. The creator lesson is
credited inspiration, not theorem validation. No podcast clips or quotes are
used, so no episode/transcript timestamp conversion is needed for this pilot.
No Navier–Stokes research conclusions enter this public explanation.

The elementary derivation is
`new/old = (1-f)+f/s = 0.8+0.2/2 = 0.9`;
therefore `old/new = 1/0.9 ≈ 1.11`.
With instantaneous Fourier work, `new/old → 0.8`, so gain tends to 1.25×.

## Release blockers / approval checklist

- [ ] Karin has watched full playback on the actual tablet and approved pacing/legibility.
- [ ] Human mathematical/editorial review confirms the assumptions and wording.
- [ ] Silent-versus-human-narration choice is recorded; any added audio has aligned captions.
- [ ] The interactive lesson has a verified, usable live URL; replace the placeholder above.
- [ ] End card and video description point to that same verified lesson.
- [ ] Asset/source credits and final export have received a release review.
- [ ] Karin explicitly approves the exact final version for YouTube/blog/social publication.

No live Pages URL is inferred from the repo name. No publishing, merge,
domain purchase or account change is part of this handoff. Keep the v4 draft
label until final review; passing automated checks does not clear these gates.

## Feedback template

Copy only what is useful into PR #2:

- Timestamp / scene:
- What was confusing or hard to read:
- Suggested wording or visual change:
- Audio preference (silent / authorized human / both):
- Decision (needs changes / ready for another review / approved exact version):
- Reviewer and date:

This template records future feedback; it does not presume an approval.
