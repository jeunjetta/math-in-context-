# Full-pilot caption layout · encoded review

18 November 2026 (Australia/Sydney). **One provisional, unadopted 80-second
silent review copy**, not a replacement for frozen v7 or a publication approval.
Source baseline: `1dfb4f7aeba73ac6d244ec5db9383cc0e58f58f4`, draft PR #4.

This integrates the already-tested [34px ink-centered layout](CAPTION_LAYOUT.md)
and [balanced 70–75 s line break](CAPTION_BALANCE.md) into one complete movie.
It makes the proposed treatment reviewable in sequence instead of adding another
copy/layout alternative. All ordered caption words, cue times, lesson data,
mathematics, scene graphics, graph and source cards remain unchanged. The original
Marimo CTA is still **unverified**; rendering it does not establish a live lesson.
The source-only ending proposal is not included. The existing 26px v7 file,
`review-version.json`, release package and earlier evidence remain unchanged.

## Exact review artifact and technical checks

File: `fft-caption-layout-review.mp4`, 724,266 bytes.
SHA-256: `d0b22d6291d0b8d9205bd5e47d7d27cbd8892f63df4a1957a7d3d5decc605142`.
Delivered separately for private review; no public destination or access grant.
The [render manifest](caption-review/render-report.json) records source/font/media
hashes, tool versions and encoder options, not reviewer acceptance.

H.264, 1280×720, 24 fps, 1,920 frames, 80.0 s, no audio. Full-stream decode
completed with error checking; all 1,920 presentation timestamps verified against
frame/24. Matching VTT is byte-identical to the canonical captions, SHA-256
`7713ab432a953f757757d25126bed96fed66b4e381967ddd608367282b0a2a9d`.
FFmpeg/ffprobe: `7.1.5-0+deb13u1`. Technical validation is not speech sync.

Inspected all 39 decoded cut/midpoint samples in contact sheets 01–07, plus
full-resolution equation frame 840, balanced-ending frame 1680 and final-caption
frame 1800. No caption/footer overlap or clipping seen in these samples; the
100/90 ≈ 1.11× equation and unchanged assumptions are legible at native size.
The final two captions fit on two lines. This is sampled visual inspection,
not complete normal-speed playback, actual-device readability or accessibility
approval. The 49–61 s distinction cards still change every three seconds.

The first encode completed, but a 101-sample FFmpeg select expression failed
with `Cannot allocate memory` during QA filter parsing. No successful QA report
was written for that attempt. A NEW output directory was used for the successful
retry with the existing 39 cut/midpoint samples; full decode and all timestamp
checks were retained. The exact resource/parser cause was not independently
diagnosed. No frozen QA implementation or archived evidence was modified.

## Reproduce and extend

The new adapter routes frames 1680..1799 through the balanced-ending adapter and
all other frames through the whole-pilot layout adapter. It refuses an existing
output directory and writes its successful manifest only after QA completes.
Content remains in the canonical JSON/VTT; no duplicate script or dependency.
From `videos/`, with external FFmpeg/ffprobe installed, use a NEW directory:

```sh
uv run --locked python -m unittest test_caption_review_render -v
uv run --locked python -m unittest discover -p 'test_*.py'
uv run --locked python caption_review_render.py --out out/caption-layout-review
```

Three new tests check routing boundaries/invalid inputs, pixel identity with the
tested adapters at nine frames and no-overwrite behavior. Full suite: **135 pass
in 91.167 s**. Review HTML, caption-pacing and narration source-copy checks pass.
Generated MP4/VTT/39 PNGs/seven sheets/full QA report stay under ignored `out/`;
the compact manifest is committed. No rendering output is an adopted candidate.

Original geometry/text; no third-party footage, music, speech or cloned voice.
Retain pinned Pillow 12.3.0 / `uv.lock` and external DejaVu Sans. Official
[FFmpeg commands](https://ffmpeg.org/ffmpeg.html),
[FFmpeg licensing](https://ffmpeg.org/legal.html) and
[Pillow licence](https://pillow.readthedocs.io/en/stable/about.html) checked
18 November 2026. This uses the existing Python/Pillow renderer and external
GPL-enabled libx264 encoder; no encoder/font is redistributed. No blanket
commercial-use or codec-patent clearance is claimed. Remotion was not newly
selected; no paid service, new dependency or purchase.

## Next decision and exact blockers

Review this ONE copy at normal speed on the intended device, particularly
49–61 s and both ending cues at 70–80 s. Record timestamped feedback before
adopting a production layout or changing candidate identity. Do not add variants
without a specific observed defect. This encoding is provisional review evidence,
not the production-selection step called for in the prior study.

Still open: human mathematics/editorial/rights review; full device playback and
accessibility; audio choice and any resulting retiming/speech synchronization;
live-Marimo CTA/destination verification or explicit fallback adoption;
public-review-route authorization; stacked-parent reconciliation; exact-version
publication approval. Open Notebook deployment is not assumed. No upload to
YouTube, Substack/social publication, sharing change, merge or automation.
