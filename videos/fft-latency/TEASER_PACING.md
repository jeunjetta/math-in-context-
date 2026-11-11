# FFT teaser · slower closing comparison

11 November 2026. **Unrendered timing alternative, not a reviewed video.**

The existing 28-second encoded draft and both full candidates are unchanged.
This version keeps 0–22 s identical, then doubles each closing focus from
1.5 to 3 seconds. Total: 34 seconds / 816 frames at 24 fps. It is not
the primary 80-second explainer or a proposed replacement without review.

| Focus | Existing start / hold | Alternative start / hold | Description tokens |
|---|---|---|---|
| Complexity | 22 s / 1.5 s | 22 s / 3 s | 2 |
| Stability | 23.5 s / 1.5 s | 25 s / 3 s | 3 |
| Latency | 25 s / 1.5 s | 28 s / 3 s | 2 |
| Grid readiness | 26.5 s / 1.5 s | 31 s / 3 s | 3 |

## What the measurement means

The closing card has 34 persistent whitespace tokens,
including its 11-token caption, plus 10 description tokens
across four changing focuses. Persistent titles/caption/credits are counted
once over the entire closing scene, not charged again to each focus.
The report separately counts description tokens per focus: doubling the
hold halves that mechanical rate. It does not halve comprehension time.

These are whitespace-token counts, not validated reading-speed thresholds.
Concurrent caption, hierarchy, visual search, revisiting titles, unfamiliar
concepts and credits compete for attention. Symbols and numbers are not
equally difficult words. Longer holds may help, bore or still be inadequate.
Only real playback/comprehension feedback can choose between versions.

## Inspect and reproduce

From videos/:

```sh
uv run --locked python fft_teaser_pacing.py --check
uv run --locked python -m unittest test_fft_teaser_pacing -v
```

[Structured timing](teaser-pacing.json), [audit report](teaser-pacing-report.json),
[alternative silent VTT](teaser-pacing.vtt), [frozen encoded draft](TEASER_RENDER.md).
The Python frame(n) interface maps the alternative timeline onto the
unchanged original renderer, without monkey-patching or editing frozen
helpers. Incoming phases own exact cuts at 22, 25, 28 and 31 seconds.
It returns original source metadata plus explicitly named comparison time.

No new MP4, encoded QA, continuous playback, device test or audio exists
for this alternative. No technical render blocker: the bounded deliverable
is tested timing/source-frame mapping and a storyboard, not another encode.

## Sources, rights and remaining gates

Same synthetic sequential 20+80→10+80=90 ms model, unchanged accuracy,
other-work and overhead assumptions; no real telemetry or readiness claim.
Concept path: Fourier algorithms → component cost → end-to-end latency;
numerical stability and validated grid readiness remain separate questions.
Educational sources remain [the pilot](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py)
and [FFTW accuracy context](https://fftw.org/accuracy/comments.html), not evidence of a new FFT.
No creator footage, music or narration added. Existing pinned Pillow 12.3.0
and external DejaVu fonts retained; no dependency or binary distribution.
[Current official drawing docs](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html)
and [licensing](https://pillow.readthedocs.io/en/stable/about.html#license)
rechecked 11 November; current stable docs describe 13.0.0, not the pinned runtime.
No blanket commercial-rights clearance is implied.

Next: encode this alternative separately and inspect actual cut/end frames
before asking Karin to compare complete tablet playback. Do not overwrite
the frozen draft. Human/editorial/math/rights review, audio and destination
choices, stacked-parent reconciliation and exact-version publication approval
remain open. Nothing published or merged.
