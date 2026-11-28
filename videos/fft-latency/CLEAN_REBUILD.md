# Source-only review · fresh-environment rebuild

21 November 2026, evening. Source commit
`17a066de120ddced5400229dcafab07cb6d9c128`, PR #4.
**Same content, reproduced on the same host—not a new candidate.**

A fresh worktree had no virtual environment or generated outputs. Running
`uv sync --locked` created its own `videos/.venv` and installed exactly
Pillow 12.3.0. Import paths were checked: the renderer came from this
worktree, and Pillow from this new environment, not an earlier project's
environment. Python 3.12.14, uv 0.13.9 and system FFmpeg/FFprobe 7.1.5
were used. uv reported a harmless hardlink-to-copy fallback; installation
completed. No dependency, lockfile, source code or scene data changed.
All 166 tests pass in this environment (110.470 seconds).

The full source-only review was rebuilt using its existing command. The
new MP4 equals the original review file byte-for-byte (direct `cmp` as
well as SHA-256). Its size remains 732,406 bytes and SHA-256 remains
`790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`.
The render manifest, matching VTT and resolved lesson are also byte-identical
to the checked-in originals. The manifest includes all twelve render-source
hashes, both font hashes, encoder options and tool/media facts. Its retained
`source_commit` is the original renderer baseline, not today's repo head;
the [rebuild receipt](source-only-review/rebuild-check.json) records both.

The rebuild's own QA passes full decode and all 1,920 frame timestamps:
80 seconds, 24 fps, 1280×720, H.264, no audio. It exports 39 decoded samples
and seven contact sheets under ignored `out/`. Inspected fresh native frames
840, 1068, 1680 and 1919: equations, settled ceiling, source-only disclosure
and final caption agree with the known review; no clipping seen there.
This is sampled inspection, not complete human playback or device approval.

## Repeat from `videos/`

Use a fresh checkout/worktree of the source commit above and the documented
system prerequisites. Do not delete another environment to simulate a fresh
one. Choose a NEW output directory each time:

```sh
uv sync --locked
uv run --locked python -m unittest discover -p 'test_*.py'
uv run --locked python source_only_review.py --out out/rebuild-new
uv run --locked python verify_source_review.py out/rebuild-new/fft-source-only-review.mp4 --captions out/rebuild-new/fft-source-only-review.vtt
cmp fft-latency/source-only-review/render-report.json out/rebuild-new/render-report.json
cmp fft-latency/source-only-review/resolved-lesson.json out/rebuild-new/resolved-lesson.json
```

The verifier checks the recorded movie identity before probing/decoding;
it fails if a different host/toolchain produces different bytes. Such a
failure requires investigation, not automatic replacement of the old
manifest or a claim that the new pixels are wrong. The exact font/encoder
versions and build options matter. Existing evidence is never overwritten.

## Limits and next action

This checks independence from previous worktree environments, **not** a
new machine, container, cold cache, platform-portable binary, or independent
audit. The system interpreter, encoders, fonts and possible package cache
remain shared. No binaries or fonts are bundled. Official
[Pillow licence](https://pillow.readthedocs.io/en/stable/about.html),
[FFmpeg commands](https://ffmpeg.org/ffmpeg.html) and
[FFmpeg legal guidance](https://ffmpeg.org/legal.html) were rechecked;
existing external-build/codec/distribution caveats remain. No purchase,
new service, asset or voice. No blanket commercial clearance is implied.

The rebuilt file stays ignored and is not separately distributed: use the
already supplied exact review copy and its [playback sheet](SOURCE_PLAYBACK_REVIEW.md).
Next is still a complete intended-device pass, text-equivalence/assistive-
technology review and the source-only adoption decision. Human math/editorial/
rights, audio choice/retiming, parent reconciliation, authorized review route
and exact-version publication approval remain open. Reproducible technical
rendering is not a finished reviewed video or a verified live lesson.
