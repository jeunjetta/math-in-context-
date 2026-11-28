# FFT and whole-workload latency · descriptive text alternative

21 November 2026. **Draft for the unadopted source-only review, not an approved release.**

This video has no audio. The text below combines its on-screen caption track with descriptions of the important visual information. It is not a speech transcript, an audio-description recording, a new cut or an accessibility certification. Time windows locate content; they do not pace or limit reading.

Reference file: `fft-source-only-review.mp4` · 80 seconds. SHA-256: `790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`.

Source baseline: `4b3a4a2ef4194801480cc7aa14041932c75b44ec`. Movie and existing captions are unchanged.

## Assumptions and persistent labels

Sequential work; Same accuracy; No added overhead; Other work unchanged. All times are synthetic milliseconds, not grid telemetry. The early scenes carry a VISUAL DRAFT marker and a synthetic/no-telemetry footer. An advancing bottom line indicates elapsed video progress, not measured workload latency. The ending instead labels the example SYNTHETIC · NOT A BENCHMARK.

## 0–8 seconds · A faster FFT. A faster system?

Visual description: On a dark canvas, the prediction question asks: 2 times faster FFT; how much faster overall? A second line invites a prediction before following the time. No numerical answer is shown yet.

On-screen caption track (not speech):

- 0–4 s: Suppose Fourier computation becomes 2× as fast.
- 4–8 s: Does the whole system become 2× as fast? Pause and predict.

## 8–18 seconds · First, measure the whole journey.

Visual description: A horizontal bar labelled BEFORE represents 100 milliseconds. Its first fifth is teal, labelled Fourier computation, 20 milliseconds; the remaining four fifths are amber, labelled other work, 80 milliseconds. Text states sequential work, same accuracy and no added overhead. These are assumptions of the synthetic model, not measured guarantees.

On-screen caption track (not speech):

- 8–13 s: Imagine sequential work taking 100 milliseconds.
- 13–18 s: Fourier work takes 20 ms. Everything else takes 80 ms.

## 18–30 seconds · Only the Fourier block shrinks.

Visual description: The original 100-millisecond bar stays above a second bar drawn on the same time scale. From 18 to 21 seconds only the second bar's teal Fourier segment shrinks from 20 to 10 milliseconds; the amber 80-millisecond segment keeps its length. During movement an arrow points toward 90 milliseconds: it labels the endpoint, not an instantaneous measured total. From 21 seconds the second bar is settled at 90 milliseconds. The captions state the resulting 10-millisecond saving.

On-screen caption track (not speech):

- 18–22 s: Divide Fourier time by 2: 20 ms becomes 10 ms.
- 22–26 s: The other 80 milliseconds stays unchanged.
- 26–30 s: 10 + 80 = 90 ms. We saved 10 milliseconds.

## 30–40 seconds · Kernel speed is not system speed.

Visual description: The large equation reads: 100 divided by 90 is approximately 1.11 times. Below it, S = 1 / [(1 - f) + f/s]. In words, overall speedup equals one divided by the sum of the unchanged time fraction and the improved time fraction divided by its component speedup. Here f = 0.20 of baseline time and s = 2 for the Fourier component. The approximation sign matters: 100/90 is not exactly 1.11.

On-screen caption track (not speech):

- 30–35 s: Overall speedup is old time divided by new time.
- 35–40 s: 100 divided by 90 is about 1.11×, not 2×.

## 40–49 seconds · Even an instant FFT has a ceiling.

Visual description: From 40 to 43 seconds the remaining teal segment shrinks toward zero. An arrow points toward the 80-millisecond endpoint, while the amber other-work segment remains unchanged. After 43 seconds the settled bar contains only that 80 milliseconds. The dark remainder is only the comparison bar's background; it does not add to the new duration. At 44.5 seconds the equation appears: 100 divided by 80 equals 1.25 times maximum. This ceiling belongs only to the stated model.

On-screen caption track (not speech):

- 40–44.5 s: Even zero Fourier time leaves 80 milliseconds.
- 44.5–49 s: In this model, the speedup limit is about 1.25×.

## 49–61 seconds · Four questions. Four different tests.

Visual description: Four category titles remain visible in a horizontal strip. Every three seconds, a teal outline and a larger explanation panel move the focus to the next category, in the order below. The titles and words, not color alone, distinguish the questions.

On-screen caption track (not speech):

- 49–52 s: Arithmetic complexity asks how operation counts grow.
  Active panel: Complexity — Operation count as input grows.
- 52–55 s: Numerical stability asks how computation errors behave.
  Active panel: Stability — Roundoff and error growth.
- 55–58 s: Latency measures elapsed time for the whole workload.
  Active panel: Latency — Elapsed end-to-end time.
- 58–61 s: Readiness needs validation against system deadlines.
  Active panel: Readiness — Validated system + deadlines.

## 61–70 seconds · Faster is useful. Readiness is more.

Visual description: A numbered checklist shows: accuracy and numerical error; data movement and alignment; worst-case deadlines and validation. An amber warning reads: Synthetic arithmetic. Not operational evidence. The footer continues to identify a synthetic example with no grid telemetry.

On-screen caption track (not speech):

- 61–65.5 s: Check accuracy, data movement, and worst-case deadlines.
- 65.5–70 s: This toy arithmetic proves no new FFT or real-time grid capability.

## 70–80 seconds · Measure the whole job.

Visual description: The source-only card says Measure the whole job and Synthetic - not a benchmark. Its concept path connects Fourier methods to component costs to end-to-end latency; these arrows locate the lesson, not an equivalence or readiness proof. A panel offers a public Python / Marimo notebook and explicitly labels it Source code only - not a live interactive app. Another line states Faster computation is not equal to validated grid readiness. Credits identify the model as synthetic and the accuracy context as the FFTW authors. The two final captions below point to source code and deny any live-lesson or real-grid benchmark claim.

On-screen caption track (not speech):

- 70–75 s: Inspect the synthetic notebook source, linked in the description.
- 75–80 s: No live lesson or real-grid benchmark is claimed.

## Sources and review limits

- [Synthetic notebook source](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py): public Python/Marimo code, not a deployed lesson.
- [FFTW authors’ numerical-accuracy context](https://fftw.org/accuracy/comments.html): not validation of the hypothetical timings.
- [3Blue1Brown Fourier lesson](https://www.3blue1brown.com/lessons/fourier-transforms/): educational inspiration, no reused visuals or clips.

The separate [playback worksheet](SOURCE_PLAYBACK_REVIEW.md) identifies this exact copy. Human equivalence/editorial review and assistive-technology testing remain open, alongside device playback, source-only adoption, rights/audio decisions and publication approval. No accessibility gate is automatically cleared.

Production note: visual copy is editable in `descriptive-transcript.json`; headings, 19 caption cues, four active panels and source links are derived from pinned review data. Regenerate with `python3 descriptive_transcript.py`; check freshness with `python3 descriptive_transcript.py --check`. No rendering dependency is needed.

Method informed by current [W3C WAI transcript guidance](https://www.w3.org/WAI/media/av/transcripts/) and [video-only alternatives guidance](https://www.w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html), checked 21 November 2026. These distinguish visual description from caption text; this draft is not a conformance determination.
