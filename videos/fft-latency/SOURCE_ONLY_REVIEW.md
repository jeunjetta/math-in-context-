# Full FFT pilot · source-only review copy

19 November 2026 · second video increment. Baseline:
`0a083c1274f3792f0385c526e01d3488285ccd22`, draft PR #4.
**Separate unadopted 80-second review, not the frozen v7 candidate.**
This puts the existing source-only ending into full lesson context so the
design decision can be reviewed. It does not adopt that release route,
replace the earlier movies or silently clear their live-lesson release gate.

## Exact copy and bounded changes

File: `fft-source-only-review.mp4` · 732,406 bytes · silent H.264 ·
1280×720 · 24 fps · 1,920 frames · 80.0 s.
SHA-256: `790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`.
The private review file is supplied separately; no public destination or
access grant is embedded here. [Render evidence](source-only-review/render-report.json).

The first 70 seconds route through the same 34px caption-layout source as
the previous full review. Arithmetic, assumptions, bar timing and four claim
distinctions are unchanged. This is SOURCE-pixel reuse, not a claim that
separately encoded streams have byte-identical first 70 seconds.
Only the final 10 seconds use the [source-only proposal](SOURCE_ENDCARD.md).

| Window | Reading caption |
|---|---|
| 70–75 s | Inspect the synthetic notebook source, linked in the description. |
| 75–80 s | No live lesson or real-grid benchmark is claimed. |

The card explicitly says “Source code only · not a live interactive app.”
Its concept path remains Fourier methods → component costs → end-to-end
latency; faster computation is distinguished from validated grid readiness.
This is one response to a specific unresolved CTA defect, not a new topic
or another timing/copy alternative. The 19 cue windows stay unchanged.

![Decoded first source-only ending cue, with a word-preserving two-line caption](source-only-review/ending.png)

The first assembly exposed an orphan “description.” on line two. The final
assembly changes ONLY that caption's line break to:

> Inspect the synthetic notebook source,
> linked in the description.

Exact words and 70–75 s timing are retained. The archive's proposal code,
JSON, stills and ten-second excerpt are not edited. The small assembly
override is separated in [source-only-review.json](source-only-review.json).
Typography is 34px in the earlier captions and the existing 32px bold
ending caption; persistent ending labels go down to 28px. Density and small
secondary credits still need device/editorial review, not inferred approval.

## Matching unpublished description

Draft copy for THIS review identity only; not posted or approved:

> Halving a 20 ms Fourier step in a sequential 100 ms workload gives
> 10 + 80 = 90 ms overall—about 1.11× faster, not 2×. We assume unchanged
> other work, unchanged accuracy and no added overhead. These are synthetic
> numbers, not a benchmark or evidence of real-grid readiness.

- [Inspect the public Python/Marimo notebook source](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py). Source code only; not a hosted interactive lesson. Local execution needs a suitable Python/Marimo environment.
- [FFTW authors' numerical-accuracy context](https://fftw.org/accuracy/comments.html), not evidence for a new FFT or these hypothetical timings.
- Educational inspiration: [3Blue1Brown's Fourier lesson](https://www.3blue1brown.com/lessons/fourier-transforms/). All visuals here are original; no clips or distinctive assets reused.

Notebook source fetched fresh on 19 November at the immutable commit above;
Git blob identity matches `bf6eb0d52cb3bb20f0ec2747a0648612eb1af09a`.
PR #1 remains unmerged and main remains the template. No live URL verified.
The available public-fetch route rejected the deployments endpoint as
unsupported; this does not establish account/deployment state. No account
settings inspected/changed, guessed Pages address or Open Notebook deployment.

## Reproduction and actual validation

Content stays in the existing lesson/end-card JSON, with a small wrapping
override; [resolved lesson](source-only-review/resolved-lesson.json) and
[matching full-length VTT](source-only-review/fft-source-only-review.vtt)
identify this assembly without modifying the canonical frozen files.
From `videos/`, use a NEW output directory:

```sh
uv run --locked python -m unittest test_source_only_review -v
uv run --locked python source_only_review.py --out out/source-only-new
```

Full decode and all 1,920 timestamps pass. The 39 cut/midpoint samples and
seven contact sheets are reproducible under ignored `out/`. Inspected decoded
frames 840, 1679, 1680, 1799, 1800 and 1919 at full size and final contact
sheet 07 at reduced size: equation legible, old caption ends before the 70 s
cut, both ending cues switch correctly, no clipping seen in these samples,
orphan removed. This is not full human/normal-speed/device playback or audio
synchronization; no audio exists. No native/browser restriction was retried.

Five focused tests pass in 0.358 s: old cue/assumption preservation, scoped
frame routing, selected component-pixel identity, caption-only changed pixels
and word sequence, invalid inputs and no-overwrite. Final suite:
**144 pass in 166.463 s**. Review HTML, caption-pacing/narration copy and
whitespace checks pass. Hashes bind source, resolved content, VTT, fonts and
movie. The superseded first assembly stays ignored and was not distributed.

Existing Python/Pillow 12.3.0 and lockfile retained. Official
[Pillow licence](https://pillow.readthedocs.io/en/stable/about.html),
[FFmpeg commands](https://ffmpeg.org/ffmpeg.html) and
[FFmpeg legal notes](https://ffmpeg.org/legal.html) checked 19 November.
External DejaVu and GPL-enabled libx264 encoder are not bundled. No new
dependency, paid service, fabricated voice or blanket commercial/codec clearance.

Next: review THIS full copy on the intended device, especially the 70 s cut,
reading load and 49–61 s cards. Decide whether to adopt the source-only route;
only then reconcile canonical candidate/captions/publication package together.
Until then frozen v7, previous larger-caption review and original release gates
stay intact. Human math/editorial/rights, accessible full playback, audio choice
and retiming if needed, parent reconciliation, authorized review route and exact-
version publication approval remain open. Nothing uploaded to YouTube, posted,
merged, deployed or newly automated. No research conclusions changed.
