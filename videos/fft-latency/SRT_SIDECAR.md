# Source-only pilot · equivalent SubRip reading track

24 November 2026. Source baseline: `c60940d5c6b5e1ae56100057f6604216ae23024f`.
**Optional draft sidecar, not an adopted candidate or publication approval.**

The full source-only copy now has a plain UTF-8
[SRT sidecar](source-only-review/fft-source-only-review.srt), converted from
its existing [WebVTT](source-only-review/fft-source-only-review.vtt).
All 19 cue texts and start/end times are unchanged. Only the container syntax
changes: sequential cue numbers and comma-separated milliseconds. No style
tags, visual assets, narration, new words or timing changes are added.

This supports editors/players that accept basic SubRip. YouTube's official
[supported-file guidance](https://support.google.com/youtube/answer/2734698?hl=en)
lists basic UTF-8 SRT without styling. That is format guidance, **not** evidence
of this file being imported into YouTube, or permission to publish it. No
platform session, upload, setting or account operation was performed.

## Exact identities

| Item | SHA-256 |
|---|---|
| Existing `fft-source-only-review.mp4` | `790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e` |
| Existing WebVTT | `3418c98bbc7fe171544ffe4298eacaa46c0297342960e76a3c69dd2f421f164e` |
| New SRT | `f11544880886b3b233fbb67e7ae37246f06fb6988b3bb0882da9a2c3381a62e4` |

These identify the unadopted 80-second silent full copy, not frozen v7 or
the teaser. The existing render manifest pins the original VTT; it was NOT
rewritten to pretend the new sidecar was part of the earlier render.
No new movie is distributed and no private review link is added.

## Reproduce and validate from `videos/`

Use the existing external FFmpeg and a NEW destination; `-n` refuses overwrite:

```sh
mkdir -p out
ffmpeg -v error -n -i fft-latency/source-only-review/fft-source-only-review.vtt -map 0:s:0 -c:s srt out/fft-source-only-review-new.srt
cmp fft-latency/source-only-review/fft-source-only-review.srt out/fft-source-only-review-new.srt
python3 -m unittest test_source_srt -v
```

Actual conversion used system FFmpeg 7.1.5-0+deb13u1.
The converter's final blank cue separator is retained verbatim; Git's
blank-at-EOF warning is intentionally excepted for this SRT only.
Three focused tests pass: all texts/times equal the hash-verified VTT;
cue numbers/contiguous 0–80s
coverage and all 24fps frame boundaries agree; independently reading SRT with
FFmpeg and writing WebVTT back preserves every text and timestamp. The final
two cues remain 70–75s and 75–80s; the exclusive end is frame 1,920. Unicode
`×` survives. FFmpeg emits shorter valid minute/second VTT timestamps on the
round-trip; the test compares integer milliseconds, not cosmetic spelling.
The test parser handles only this archive's plain-text profile, not general
SRT/WebVTT syntax. The conversion test is skipped when FFmpeg is unavailable.

No video was encoded/decoded by this increment. Subtitle format conversion
does not inspect encoded pixels, clipping, equations or native playback, and
does not establish speech synchronization. No speech exists: this is the
same silent **reading track**, not a fabricated speech transcript. It is not
the [descriptive text alternative](DESCRIPTIVE_TRANSCRIPT.md), which also
describes informative visuals.

## Playback limits and next action

The movie already has burned-in text. A player may auto-load a same-stem SRT
and display a duplicate overlay; do not mistake that for a changed movie.
Use the existing review worksheet and record whether a sidecar is enabled.
This file cannot remove or resize burned-in captions. Player wrapping and
positioning are not preserved by plain SRT; the renderer's word-preserving
two-line ending is not a promise about a player's line layout. Intended-device
and assistive-technology testing remain open; no accessibility certification.

The official [FFmpeg command documentation](https://ffmpeg.org/ffmpeg.html)
and [licensing guidance](https://ffmpeg.org/legal.html) were checked today.
The existing external build is reused, not bundled; no dependency/lock/font
change, purchase or blanket commercial/codec rights clearance is claimed.

Next: optional local-player import of this sidecar when reviewing the exact
copy; compare wrapping and avoid duplicate overlay. Full intended-device
movie review, mathematical/editorial/rights approval, audio choice/retiming,
source-only adoption, parent reconciliation, authorized review route and
exact-version publication approval remain open. No live lesson or Open
Notebook deployment is assumed; no research conclusions change.
