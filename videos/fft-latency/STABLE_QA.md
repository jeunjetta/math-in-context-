# Snapshot-based encoded review packs

22 November 2026, evening. Source: PR #4 head
`b591022707584010e70a9188965ba4fab5ac81c4`.
This is an optional technical QA improvement, not a new movie or release design.

## Why a separate wrapper

The existing `qa.py` hashes the input only after probing, decoding and making
contact sheets. If a person or another render replaces that path during the
run, the final hash could describe different bytes from the decoded samples.
No existing review pack is known to have suffered this problem. The issue is
reproduced as controlled mutation in tests, not asserted retrospectively.

`stable_qa.py` hashes the original, makes a private temporary movie copy,
checks both hashes, and runs the existing helper on that copy and a deep copy
of the lesson data. It checks the original and copy again before exporting
the pack. Mutation or decode failure discards temporary evidence without
creating the requested output pack. An existing destination is never reused;
a destination created during QA is also refused. Successful evidence includes
the guard's source hash. Snapshot storage needs additional space for the movie
and temporary pack; temporary files are cleaned on ordinary completion/errors.

The old helper is deliberately unchanged: twelve-source render manifests and
existing exact-copy checks pin its bytes. No historical manifests are rewritten.
Existing rendering/verification commands keep their original behaviour.

## Use from `videos/`

For the full source-only review, first verify the separately supplied movie's
exact recorded identity using the existing verifier. Then choose a new output:

```sh
uv run --locked python verify_source_review.py /path/to/fft-source-only-review.mp4
uv run --locked python stable_qa.py /path/to/fft-source-only-review.mp4 --lesson fft-latency/source-only-review/resolved-lesson.json --out out/source-snapshot-new
uv run --locked python -m unittest test_stable_qa test_qa -v
```

`--lesson` accepts an already resolved lesson JSON; omit it only for the
canonical pilot. Optional `--every-seconds 1` adds chronological samples while
keeping cue cuts. This wrapper does not identify a supplied lesson as the movie's
actual source: use the exact-copy verifier first. Expected captions are lesson
metadata, not OCR. The wrapper does not validate arbitrary lesson schemas or
replace the renderer's source-model validation.

## Actual validation

Five regression tests cover stable input/private lesson data, mutation during
copy, mutation during QA, existing output/decode failure and a late destination
collision. Fixtures are not passed to a decoder. The existing real encoded
integration test also passes.

The wrapper separately processed the existing exact full source-only movie:
SHA-256 `790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`,
732,406 bytes, H.264, 1280×720, 24 fps, 1,920 frames, 80 seconds, no audio.
Complete decode and all timestamps passed; 39 samples/seven sheets generated.
The existing verifier also passed all twelve archived source hashes. New native
samples at frames 840, 1320 and 1919 were inspected: equation, latency focus
and source-only ending agree; no clipping observed there. This is not an
every-frame visual audit, complete human/device playback or audio-sync check.
Output stays ignored under `out/`; no replacement movie is distributed.

## Limits and next action

Before/after hashes are not a lock, digital signature or defense against an
adversary who restores bytes between checks. The private decoded copy is the
evidence source; checks detect ordinary concurrent edits to the original.
Final copying can leave an incomplete destination on I/O failure; the report is
copied last. Do not treat a directory without its completed report as success.
No accessibility, comprehension, mathematical review or publication approval
is inferred. No new runtime dependency, encoder, font, voice or rights clearance.

Official [FFprobe documentation](https://ffmpeg.org/ffprobe.html),
[FFmpeg licensing](https://ffmpeg.org/legal.html) and
[Python hashlib](https://docs.python.org/3/library/hashlib.html) checked today.
Existing external FFmpeg build/codec/font terms remain; nothing is bundled and
no blanket commercial-use permission is claimed.

Next editorial step is unchanged: complete intended-device playback of the
one review focus, return one specific issue and decide the source-only route
before candidate/package migration. All existing release gates remain open.
