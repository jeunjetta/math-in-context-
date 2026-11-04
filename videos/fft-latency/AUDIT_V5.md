# v5 chronological encoded-sample audit

**2 November 2026 · agent inspection, not human playback or release approval.**

Historical audit of v5, retained unchanged below. Revision v6 (3 November)
addresses Refinement A by replacing moving decimal totals with endpoint arrows;
see [STATUS.md](../STATUS.md) for its new encoded validation. This does not
retroactively change the v5 observations or clear any human review gate.

Video source inspected at PR #2 commit
`2fdc751d517e79451b774634107d6366a95c0187`; renderer/lesson are unchanged
from the existing v5 render. Encoded input SHA256:
`d2a0365545602c55af3ee6018944045a5804a125b0dd5af80d7585c85efe12d4`.
Match this hash before treating observations as applying to another copy.
No new video render, audio track or performance claim is introduced here.

## What was actually inspected

Complete FFmpeg decode and FFprobe timestamps verified the 80.000-second,
1280×720, 24 fps H.264 file: 1,920 frames, no audio. The expanded QA selection
contains 101 frames: each whole second, both sides of caption cuts, scene
midpoints and the final frame at 79.958 s. All 17 contact sheets were inspected
in order. This spans all scenes, but it is NOT continuous normal-speed
playback, all-frame visual inspection, an actual-tablet test or a listening
test. Caption labels in report.json are expected metadata, not OCR evidence.

## Timestamped observations

| Time | Encoded samples observed | Disposition |
|---|---|---|
| 0–8 s | Prediction question remains on screen; no 90 ms answer revealed. Caption changes at 4 s. | No sampled mismatch found. Eight-second opening still needs human pacing feedback. |
| 8–18 s | Labelled 20/80 split totals 100 ms; same-accuracy/no-overhead assumptions are visible. | No sampled clipping or arithmetic mismatch found. |
| 18–21 s | Shared-scale before/after bars contract only the Fourier segment. Total reads 97.41 ms at 19 s, 92.59 ms at 20 s, then 90 ms at 21 s. | **Refinement A:** decimal totals are products of illustrative easing, not observations or extra lesson results. They draw attention away from the endpoint. Label this beat as a transition and show an endpoint cue during motion rather than an apparently precise intermediate result. |
| 21–30 s | The result holds at 90 ms through the unchanged-work and 10+80 captions; baseline remains 100 ms. | No sampled mismatch found; result has a substantial reading hold. |
| 30–40 s | 100/90≈1.11×, general formula, f=0.20 and s=2 are visible through the two captions. | No sampled glyph/clipping mismatch found. Whether the equation can be absorbed alongside the caption needs normal-speed tablet review. |
| 40–49 s | Transition is labelled; intermediate totals 87.41/82.59 at 41/42 s. It holds at 80 ms from 43 s. Formula absent at 44.458 s, appears with the new cue at 44.5 s. | Prior ceiling timing fix remains visible. **Refinement A** also applies to decorative decimal totals here; do not change the hold/reveal boundary. |
| 49–61 s | Complexity, stability, latency and readiness outlines match their captions at 49, 52, 55 and 58 s and immediately preceding frames. | No sampled mismatch found. Three seconds per card remains a human comprehension/pacing question, not a test-certified duration. |
| 61–70 s | Engineering checklist and explicit “not operational evidence” text persist; no-new-FFT/no-grid-capability caption appears at 65.5 s. | Scope remains appropriate in inspected samples. No operational data or recommendation. |
| 70–80 s | Concept chain, Marimo source path, source credits and final contextual caption persist through the last frame. | **Existing release blocker:** source path/PR pointer is not a learner-ready live URL. No deployment verified by this audit. |

No sampled blank frame, missing scene, swapped focus card, clipped equation
or incorrect final timing value was found. This is a bounded observation,
not a clean bill of health for frames or motion not inspected. Refinement A
is an editorial clarity finding, not an assertion that the arithmetic is wrong
or the file represents measured telemetry. Keep the synthetic/draft labels.

## Reproduce the same coverage

From `videos/`, using the existing pinned dependencies and external FFmpeg:

```sh
uv run --locked python qa.py PATH_TO_MATCHING_V5.mp4 --out out/audit-v5 --every-seconds 1
uv run --locked python -m unittest test_video test_qa test_thumbnail -v
```

Choose a new output folder if one already exists. Inspect contact-01.png through
contact-17.png in order, then inspect full-resolution frames for any concern.
Do not mistake a successful decode for the visual audit itself. The sample
report records its input hash, source/lesson hashes, tool versions and interval.
Generated evidence stays in ignored `out/`; the MP4 and decoded frames are not
new public assets. No binary/font distribution, dependency upgrade or paid tool.
Official [FFmpeg select documentation](https://ffmpeg.org/ffmpeg-filters.html#select_002c-aselect)
and [license/build notes](https://ffmpeg.org/legal.html) were rechecked on
2 November 2026; existing external-tool licensing caveats remain applicable.

## Next action and unchanged gates

Next bounded render change: address Refinement A in the two moving-bar beats,
test motion/hold/caption boundaries, then render and inspect a new draft.
Do not retime or rewrite unrelated scenes solely because they were audited.
Keep the current MP4 unchanged until a new render is actually validated.

Karin's full normal-speed/tablet review, audio decision, final editorial/rights
review, authorized lesson deployment with verified URL and exact-version
publication approval remain outstanding. No checklist is marked complete by
this audit. See [REVIEW.md](REVIEW.md) for the full gates and feedback template.
