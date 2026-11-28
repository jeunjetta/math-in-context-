# Four encoded caption samples

25 November 2026 (Sydney), source baseline
`053c1cacd2a9a0de25626ce41d7543fef59c35ef`, PR #4.
One narrow diagnostic of the unchanged source-only review copy, not another
movie or a readability/accessibility approval.

## What was measured

The movie snapshot is checked against SHA-256
`790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`
and 732,406 bytes before decoding. The exact same in-memory bytes feed
FFmpeg, avoiding a hash/path replacement race. The existing source-color
audit also checks all twelve archived rendering-source hashes and the
resolved lesson/caption identities. Existing render evidence stays immutable.

Decode frames 1212, 1284, 1356 and 1428 (24 fps) to RGB with system FFmpeg
7.1.5. For each matching original source frame, crop only x=80..1199,
y=590..681. Make masks of exact source foreground `#f4f7fc` and caption
background `#0a111c`, then erode each with a 3x3 minimum filter. At those
source-defined locations measure the DECODED pixels, not the source colors.
Apply the existing sRGB luminance function; divide minimum foreground
luminance + .05 by maximum background luminance + .05. These independent
extrema form a conservative diagnostic of the selected cores, not adjacent
pixel pairs, a complete stroke measurement or a normative conformance test.

| Time | Focus | Selected foreground pixels | Core ratio |
|---|---|---:|---:|
| 50.5 s | Complexity | 108 | 15.883:1 |
| 53.5 s | Stability | 121 | 14.978:1 |
| 56.5 s | Latency | 120 | 14.898:1 |
| 59.5 s | Readiness | 121 | 15.828:1 |

The intended solid source pair is 17.621:1. Compression changes decoded
values, but this sample does not indicate a solid-core contrast defect
warranting a color change. Only 108–121 foreground pixels survive the mask
per frame: **do not extrapolate this result to every glyph or thin stroke**.
Antialias edges and glyphs without 3x3 solid interiors are excluded.
The [machine-readable result](encoded-caption-report.json) records counts,
extrema, decoded RGB hashes, source/script/font identity and decoder command.

Inspected the four-row 640-wide decoded sheet and full-size 53.5 s stability
frame. No caption clipping or wrong highlighted category was observed in
those samples. Footer remains small; concurrent heading/card/caption load
still requires intended-device normal-speed review. This section contains
no equations; no new equation-scene review is claimed. No full playback,
new movie, audio or speech synchronization was performed.

## Reproduce

From `videos/`, using an existing exact movie at your own local path:

```sh
uv sync --locked
uv run --locked python -m unittest test_encoded_caption_audit test_contrast_audit -v
uv run --locked python encoded_caption_audit.py /path/to/fft-source-only-review.mp4 --out out/new-caption-audit
```

The output directory must not already exist. It receives four full PNGs,
a 640-wide four-row sheet and report.json. PNGs remain local/ignored, not
additional media copies for release. Decoder/build differences may alter
RGB values: compare the recorded tool version rather than assuming byte
identity on another host. Unit tests cover eroded cores, source-versus-decoded
measurement, missing thin cores/geometry and wrong-file rejection before
decode/output. The first extraction attempt failed because filter commas
were not escaped; corrected before accepting any report. Pillow's getdata
deprecation warning remains non-fatal under the retained 12.3.0 pin.

Official [Pillow drawing docs](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html),
[licence](https://pillow.readthedocs.io/en/stable/about.html),
[FFmpeg select docs](https://ffmpeg.org/ffmpeg-filters.html#select_002c-aselect)
and [build-dependent legal notes](https://ffmpeg.org/legal.html) checked today.
No dependency/lock changes or bundled fonts/encoder; existing system DejaVu
and external FFmpeg terms remain. No blanket commercial/codec clearance.
The [earlier source-color audit](CONTRAST_AUDIT.md) retains its W3C method
references; this diagnostic treats decoded RGB as sRGB, without color-managed
display validation. Streaming transcodes, other text regions, other frames,
reading comprehension and full WCAG conformance are outside scope.

Next: complete intended-device playback and record one specific observed
issue or release-design recommendation. Source-only adoption, independent
math/editorial/rights review, accessible playback, audio decision/retiming,
parent reconciliation and exact-version publication approval remain open.
No candidate/caption/package adoption, research changes or publishing.
