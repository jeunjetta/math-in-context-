# Encoded caption-cut timing

25 November 2026, evening. PR #4 baseline
`9d0280cfc7e914359b9bd7f0571bf61e4a390e8e`.
The SAME unadopted 80-second silent source-only copy is unchanged.
This is a relative pixel-template diagnostic, not OCR, speech sync or approval.

## Result and exact scope

All **18 interior cue cuts / 36 sampled frames** favor their expected
caption-region template over the adjacent cue. Samples are frame `n-1`
and frame `n` for each cue-start frame `n` on the existing 24fps timeline.
The 44.5-second cut is frame 1068; the two ending transitions are frames
1680 and 1800. No one-frame early/late caption switch was detected at these
sampled boundaries. First/last movie frames and every held frame are not
part of this test; prior decode/timestamp evidence remains separately dated.

Across the 36 comparisons, expected-template mean absolute RGB errors are
about 1.87–2.59 levels per 8-bit channel; adjacent-cue errors are about
165.04–199.07. Minimum separation is 162.60. These are diagnostic distances,
not a readability score, perceptual threshold, probability or exact pixel match.
The [full result](caption-cut-report.json) records both scores, selected-pixel
counts, captions, frames, commands and movie/source/font/tool identities.

The checker validates the movie's existing SHA-256
`790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`
and 732,406 bytes, plus twelve archived render sources and the resolved
lesson/VTT identities. It hashes and decodes the SAME in-memory movie bytes.
FFmpeg selects samples in three small batches, then crops x=0..1279,
y=590..691. Only positions containing exact foreground `#f4f7fc` in EITHER
source template contribute to the error: changing dark backgrounds cannot
dominate the comparison. Source templates are the outgoing/incoming frames
from the existing renderer, not newly authored text or a second clock.
Comparison uses mean absolute channel error and a strict `expected < other`
decision; identical/empty templates fail rather than asserting a result.

This does not independently validate the renderer's words, all glyphs,
card highlights outside the crop, equation regions, clipping, smooth motion,
all held frames, color-managed display, stream transcodes or comprehension.
It detects which of TWO source states these samples resemble; a different
error could still resemble the expected state more closely. Controlled
one-frame-shift fixtures are tests, not claims that this movie had a defect.
There is no speech, so speech/caption synchronization is not applicable.
No new full human/device playback or visual-inspection result is claimed.

## Reproduce without changing the movie

From `videos/`, with the pinned environment and external FFmpeg:

```sh
uv sync --locked
uv run --locked python -m unittest test_caption_cut_audit test_encoded_caption_audit test_contrast_audit -v
uv run --locked python caption_cut_audit.py /path/to/fft-source-only-review.mp4 --out out/new-cut-audit
```

Choose a NEW output directory. A mismatch writes a report with
`all_expected_closer: false` and exits nonzero; publication approval remains
false either way. Input/source/decoder failure does not create that report.
The tool never encodes a movie or edits captions. Four new tests cover all
cut indices (including 44.5s), correct/swapped early-late fixtures, ambiguous/
invalid crops and wrong movie rejection before decoding/output. Existing
reports are not regenerated or relabelled by this tool.

Official [FFmpeg select/crop documentation](https://ffmpeg.org/ffmpeg-filters.html),
[legal notes](https://ffmpeg.org/legal.html),
[Pillow channel operations](https://pillow.readthedocs.io/en/stable/reference/ImageChops.html)
and [licence](https://pillow.readthedocs.io/en/stable/about.html) checked today.
Retained Pillow 12.3.0/uv.lock, system FFmpeg 7.1.5 and external DejaVu;
no dependency upgrade, bundled binaries/fonts or blanket commercial clearance.

Next remains one complete intended-device pass using the existing
[worksheet](SOURCE_PLAYBACK_REVIEW.md), then one observed issue or a release-
design recommendation. Human math/editorial/rights, accessible playback,
audio choice/retiming, source-only adoption, parent reconciliation and
exact-version publication approval remain open. No research/operational
claims, new voice, paid service, publishing, merge or account/sharing changes.
