# Descriptive text: sampled encoded-frame comparison

27 November 2026. **Assistant visual comparison, not independent human review,
full playback or accessibility approval.** No movie or text revision.

Source: PR #4 head `d3206c2b0ac6ae97035704645b47c77917626e15`.
Compared [the existing descriptive text](DESCRIPTIVE_TRANSCRIPT.md) against
16 freshly decoded native-size PNGs from the exact source-only review focus.
No substantive contradiction was found in the sampled visual assertions.
This is narrower than saying the full text and movie are equivalent.

## Exact scope

- Movie: `fft-source-only-review.mp4`, 732,406 bytes, SHA-256
  `790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`.
- Text SHA-256:
  `b648f3b1fc32f5507f7f6f7cb0d8a3de01fbb07be40d4c438a7f42f613d96ecc`.
- Editable description JSON SHA-256:
  `b1888ed06c515e7e2f331e4b6f12b1ba26c3ab68ac27e97dcf24cd5218adb23b`.
- The existing exact-copy verifier passed again: twelve render-source hashes,
  matching VTT, all 1,920 timestamps and complete decode; 80 s, 24 fps,
  1280×720 H.264, no audio. This is not a new render.
- PNGs 01–16 were each viewed at native 1280×720 output size. They are local
  ignored QA, not bundled assets or another review movie.

Frame numbers are zero-based, time = frame / 24. The table describes what
was inspected, not unseen frames or a claim to have watched motion.

| Text section | Encoded frames (seconds) / PNGs | Observed visual agreement |
|---|---|---|
| Prediction, 0–8 s | 96 (4 s) / 01 | Question and prediction invitation; no numerical answer. |
| Baseline, 8–18 s | 312 (13 s) / 02 | Teal 20 ms plus amber 80 ms; 100 ms total; model assumptions visible. |
| Halving, 18–30 s | 456, 504, 624 (19, 21, 26 s) / 03–05 | Intermediate teal width with endpoint arrow, then settled 90 ms; amber length unchanged between these samples; final caption states 10 + 80 and 10 saved. |
| Quotient, 30–40 s | 840 (35 s) / 06 | 100 / 90 ≈ 1.11×; general S formula and f = 0.20, s = 2 agree. |
| Ceiling, 40–49 s | 984, 1032, 1068 (41, 43, 44.5 s) / 07–09 | Intermediate bar with → 80 endpoint; settled amber-only 80 ms; then exact 100 / 80 = 1.25× maximum. Background remainder is not extra work. |
| Four questions, 49–61 s | 1176, 1248, 1320, 1392 (49, 52, 55, 58 s) / 10–13 | All four active titles/descriptions agree with text and corresponding captions, in the stated order. Labels and focus numbering accompany color. |
| Engineering limits, 61–70 s | 1572 (65.5 s) / 14 | Three numbered items and synthetic/not-operational warning agree; no real-grid capability asserted. |
| Source-only ending, 70–80 s | 1680, 1919 (70, 79.9583… s) / 15–16 | Concept path, source-code-only/not-live-app disclosure, readiness inequality and model/accuracy credits agree; both final caption states inspected. |

No clipping or illegible equation symbols were observed in these native-size
samples. That is **not** evidence of comfortable three-second reading,
intended-device legibility or comprehension. The descriptions' exact
transition durations are consistent with the selected states and source
data, but this still-frame check cannot verify every intervening frame or
prove continuous animation timing. Nor does it check all 19 caption holds.

## Reproduce the same sample selection

From `videos/`, use the existing exact movie and a NEW local output directory:

```sh
python3 verify_source_review.py /path/to/fft-source-only-review.mp4 --captions /path/to/fft-source-only-review.vtt
mkdir -p out/text-visual-check-new
ffmpeg -v error -n -i /path/to/fft-source-only-review.mp4 -vf "select='eq(n,96)+eq(n,312)+eq(n,456)+eq(n,504)+eq(n,624)+eq(n,840)+eq(n,984)+eq(n,1032)+eq(n,1068)+eq(n,1176)+eq(n,1248)+eq(n,1320)+eq(n,1392)+eq(n,1572)+eq(n,1680)+eq(n,1919)'" -fps_mode vfr out/text-visual-check-new/%02d.png
python3 descriptive_transcript.py --check
```

Actual extraction used system FFmpeg 7.1.5-0+deb13u1. The `-n` guard refuses
to overwrite existing PNGs. Viewer output was used for the observations
above, not an OCR or similarity-score acceptance test.

## Decision and remaining gap

Keep the existing text unchanged on this evidence; do not generate a new
movie solely because this comparison found no sampled mismatch. Retain the
generator's explicit warning that structural checks do not verify semantic
equivalence. This report is not a conformance determination or Karin's signoff.

Next: use the [complete playback worksheet](SOURCE_PLAYBACK_REVIEW.md) on the
intended device, including normal-speed 49–61 s concurrent text and final
70–80 s source-only disclosure. Obtain human text-equivalence/editorial
feedback and assistive-technology testing; revise one observed problem if
found. Full math/rights review, audio choice and retiming if recorded,
source-only adoption, parent reconciliation, authorized review route and
exact-version publication approval remain open. Speech sync is not
applicable to this silent file, not passed.

Current [W3C WAI transcript guidance](https://www.w3.org/WAI/media/av/transcripts/)
was checked for the distinction between captions and important visual
information; it does not validate this report or certify this text.
Official [FFmpeg select documentation](https://ffmpeg.org/ffmpeg-filters.html#select_002c-aselect)
and [licensing notes](https://ffmpeg.org/legal.html) were checked on this date.
Existing external-build/font/codec caveats remain; no tool migration,
dependency change, bundled binary/font or blanket commercial clearance.
