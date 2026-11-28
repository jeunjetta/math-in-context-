# Source-only copy · one complete playback review

20 November 2026, evening. Baseline PR #4
`5abf3cca6f3544938eec16f5e5d2b08b32ed887b`.
**Use this sheet for the source-only copy, not the older CTA movie.**
The [older playback worksheet](PLAYBACK_REVIEW.md) remains valid only for
its own earlier movie; its final-caption prompts do not describe this copy.

## Identify and watch

File: **fft-source-only-review.mp4**, 732,406 bytes, 80 seconds,
1280×720, 24 fps, silent. SHA-256:
`790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`.
The review file was supplied separately. No public video link, download,
new sharing grant or installation is provided by this sheet.
Use the existing file in a trusted local player at your normal viewing size.
Watch once at normal speed without pausing/seeking; then revisit trouble spots.
If the player cannot display it at a useful size, mark **cannot assess**.

| Window | Check on THIS copy | Record if missed |
|---|---|---|
| 0–8 s | Time to predict before the result? | Hook rushed/unclear |
| 8–18 s | 20 ms Fourier + 80 ms other work; sequential, same accuracy, no added overhead? | Number/assumption unreadable |
| 18–30 s | Only Fourier work shrinks, settling at 10 + 80 = 90 ms? | Motion/labels confusing |
| 30–40 s | 100/90 ≈ 1.11× overall, not 2×? | Equation needs replay |
| 40–49 s | Even zero Fourier time leaves 80 ms: 1.25× ceiling? | Ceiling unclear |
| 49–61 s | Complexity, stability, latency and readiness remain distinct? | Name the rushed card |
| 61–70 s | Synthetic arithmetic is not operational grid evidence? | Scope warning missed |
| 70–75 s | “Inspect the synthetic notebook source, / linked in the description.” Read naturally across both lines? | Break/density/cut problem |
| 75–80 s | “No live lesson or real-grid benchmark is claimed.” Remains readable through the ending? | Final disclosure missed |

Without replay, explain why the total is 90 ms and name one thing the
arithmetic does not establish. This is a review prompt, not a scored study.
The [matching unpublished description/source link](SOURCE_ONLY_REVIEW.md#matching-unpublished-description)
points to public notebook source, **not** a deployed interactive lesson.

Copy this public-safe response format; do not include operator data:

> Exact filename/hash: …
> Entire 0–80 s watched at normal speed: yes/no
> Device/player and approximate viewing width (or unknown): …
> Window/timestamp: … / observed issue: … / effect on understanding: …
> Layout recommendation: keep / one specific fix / cannot assess
> Source-only release route recommendation: adopt / retain for revision / cannot assess

Recommendations do not authorize publication or silently adopt a candidate.
No speech exists: speech/caption synchronization is **not applicable**, not
passed. Color contrast passing does not establish small-text readability.
Prior native import observations concern the older movie, not this copy.

## Optional exact-copy check for a technical reviewer

No code is needed just to watch and comment. With the existing pinned video
environment and external FFmpeg/FFprobe, from `videos/`:

```sh
uv sync --locked
uv run --locked python verify_source_review.py /absolute/path/fft-source-only-review.mp4
# Optional: save evidence to a NEW file; existing files are never replaced.
uv run --locked python verify_source_review.py /absolute/path/fft-source-only-review.mp4 --out out/source-copy-check-new.json
```

The output directory must already exist. `--captions` optionally checks a
downloaded VTT; otherwise the checked-in matching VTT is used. Input filename
alone is not trusted: movie/VTT bytes, size, pinned render manifest, resolved
lesson and all twelve archived render sources must match before decoding.
The script then probes all 1,920 timestamps and streams, checks geometry,
duration/rates/codec/no audio, fully decodes, and rechecks inputs afterward.
It does not render, upload or inspect pixels. Trusted repository hashes are
identity evidence, not a cryptographic signature or independent content audit.

The [dated technical verification result](source-only-review/copy-check.json)
records an actual run on the existing movie; it is not evidence of this
worksheet being completed. Official [FFprobe documentation](https://ffmpeg.org/ffprobe.html)
and [FFmpeg legal guidance](https://ffmpeg.org/legal.html) checked 20 November.
Existing external-build/codec/font licensing caveats remain; no bundled
binary, paid service, new asset, voice or dependency.

Next: collect one complete intended-device pass using this identity, choose
the release design, then reconcile candidate/captions/package together.
Human maths/editorial/rights, accessible playback, audio choice/retiming,
parent-branch reconciliation, authorized review route and exact-version
publication approval remain open. Frozen v7, earlier copies and gates unchanged.
