# Source-only review · intended-color contrast

20 November 2026 (Sydney). Source commit
`68668c1dbd54fcd2996e3042e32481c3733fc8ef`, PR #4.
**A source-color audit, not another cut or accessibility certification.**

## Exact scope

The [80-second source-only review](SOURCE_ONLY_REVIEW.md) is unchanged:
`fft-source-only-review.mp4`, SHA-256
`790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`.
Its [render manifest](source-only-review/render-report.json) is pinned by hash.
The audit checks all 12 recorded rendering-source hashes and the resolved
lesson/VTT hashes before calculating. It does not reopen the movie, re-decode
it, or claim a new pixel inspection. Existing render evidence remains separate.

The inventory follows the actual drawing roles in `render.py` (0–70 s),
`caption_layout.py` and `fft_source_endcard.py`/`source_only_review.py` (70–80 s).
It covers ten unique opaque text/background combinations. Scene headings,
equations, inactive and active category titles, captions, source prompt,
disclosure, credits and footer are represented. The role inventory is manual,
not automated discovery of every text call. No text is drawn on the moving
teal/amber bars. Bar/border/progress contrast and color-only distinctions are
not assessed by this text audit.

## Method and result

Use the current W3C [sRGB relative-luminance definition](https://www.w3.org/WAI/WCAG22/Understanding/relative-luminance.html):
linearize each normalized channel using the 0.04045 breakpoint, then
`L = 0.2126 R + 0.7152 G + 0.0722 B`. Contrast is
`(lighter L + 0.05) / (darker L + 0.05)`.
The [contrast-minimum explanation](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
uses 4.5:1 for ordinary text and 3:1 for large text, without rounding the
threshold comparison. This project audit conservatively uses **4.5:1 for
all ten pairs**, without inferring a large-text exemption from video pixels.
Underlying solid source colors are used, not antialias-edge samples.
These W3C web-text criteria inform this narrow production check; they do
not certify the complete video or viewing environment.

| Text role/color | Background | Ratio (display rounded) | Target |
|---|---|---:|---|
| Primary `#f4f7fc` | Canvas `#101c2c` | 15.971:1 | Pass |
| Secondary `#b5c4d7` | Canvas `#101c2c` | 9.671:1 | Pass |
| Teal `#63e0d0` | Canvas `#101c2c` | 10.701:1 | Pass |
| Amber `#ffc273` | Canvas `#101c2c` | 10.793:1 | Pass |
| Primary `#f4f7fc` | Panel `#203249` | 12.118:1 | Pass |
| Secondary `#b5c4d7` | Panel `#203249` | **7.338:1** | Pass |
| Teal `#63e0d0` | Panel `#203249` | 8.119:1 | Pass |
| Amber `#ffc273` | Panel `#203249` | 8.189:1 | Pass |
| Primary `#f4f7fc` | Caption `#0a111c` | 17.621:1 | Pass |
| Secondary `#b5c4d7` | Caption `#0a111c` | 10.670:1 | Pass |

Full-precision results and role descriptions live in
[contrast-report.json](contrast-report.json); editable audit scope is separate
in [contrast-spec.json](contrast-spec.json). Palette values are parsed from
literal renderer assignments without importing Pillow or running rendering
code. The caption background literal is checked in both relevant sources.
No color adjustment is justified by this result alone.

## Reproduce and limitations

From `videos/`, with Python 3.11–3.13 (standard library only for this audit):

```sh
python3 contrast_audit.py --check
python3 -m unittest test_contrast_audit -v
```

After intentionally reviewing a changed scope/source identity, update the
specification and run `python3 contrast_audit.py` to regenerate the report.
The `--check` path makes no writes and rejects stale results. Source drift
fails closed rather than silently applying this review to a different movie.
Seven tests cover luminance endpoints, channel weights/linearization,
symmetry, invalid/nonopaque colors, unrounded thresholds, non-executing
palette parsing, exact checked-in results and provenance drift rejection.

Passing intended-color contrast does **not** establish encoded/streaming
pixel contrast, color-management fidelity, antialias legibility, typography,
reading speed, comprehension or complete WCAG conformance. The unchanged
pre-70 s footer is 16 px on the 1280-wide canvas: nominally 8 px at 640-wide.
Earlier captions are 34 px (17 at half-size); closing captions are 32 px bold
(16 at half-size), with secondary closing labels down to 28 px (14 at half-size).
Those are geometric scale calculations, not a device-observed pass.

Next concrete step: one complete intended-device playback of THIS exact
source-only copy, prioritizing the 49–61 s distinctions and 70–80 s ending.
Judge reading load and secondary text; choose source-only adoption before
reconciling the canonical candidate/package. Full human math/editorial/rights,
audio choice (and retiming if narrated), accessible playback, parent-branch
reconciliation and exact-version publication approval remain outstanding.
No audio exists, so speech/caption synchronization is not claimed. No new
movie, render, assets, dependencies, notebook edits or research claims.
