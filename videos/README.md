# Math in Context · video workshop

First increment: **80-second silent, captioned visual draft**, not an approved
YouTube release. Original graphics; synthetic numbers; no operational claims.
Video work lives here independently of the Marimo starter PR #1.

## Start with one complete review copy

Review focus: **the full source-only copy**, not a teaser, the older
caption-layout comparison or the frozen v7 reference. This is a review
priority, **not adoption of a release design**. All three copies below are
80-second silent drafts and remain unapproved.

| Copy | Role and limitation | Correct handoff |
|---|---|---|
| `fft-source-only-review.mp4` | Review focus; unadopted source-code-only ending, not a live lesson | [Playback worksheet](fft-latency/SOURCE_PLAYBACK_REVIEW.md) · [Exact identity and draft description](fft-latency/SOURCE_ONLY_REVIEW.md) |
| `fft-caption-layout-review.mp4` | Earlier larger-caption comparison; live-lesson CTA remains unverified | [Older playback worksheet](fft-latency/PLAYBACK_REVIEW.md) · [Render evidence](fft-latency/CAPTION_REVIEW_RENDER.md) |
| `fft-latency-draft.mp4` | Frozen canonical v7 reference; not approved, live-lesson CTA unverified | [v7 editorial handoff](fft-latency/REVIEW.md) · [Canonical identity](fft-latency/review-version.json) |

For the review focus, use the existing separately supplied file:
`fft-source-only-review.mp4`, 732,406 bytes, SHA-256
`790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`.
Private review links are not included here; these repository links do not
grant media access or imply a public video destination.

1. Open the [source-only worksheet](fft-latency/SOURCE_PLAYBACK_REVIEW.md)
   and watch the exact copy once at normal speed in an existing trusted player.
   No installation or code is needed to watch and comment.
2. Use the [descriptive text alternative](fft-latency/DESCRIPTIVE_TRANSCRIPT.md)
   to follow the captions, visual changes and equations in text. It is a draft,
   not recorded narration or an accessibility certification.
3. Return the worksheet's timestamped feedback for that file: keep, one specific
   fix, or cannot assess. A review recommendation does not authorize publication.

Prioritize 49–61 s (the four distinctions) and 70–80 s (the source-only ending).
Choose the release design before reconciling candidate, captions and package;
do not substitute the older worksheet's ending prompts. Full intended-device
playback, human math/editorial/rights, text-equivalence/assistive-tech review,
audio choice/retiming, parent reconciliation and exact-version publication
approval remain open. Source-only adoption does not deploy a live lesson.

For technical reproduction of this exact copy, use the
[fresh-environment rebuild commands](fft-latency/CLEAN_REBUILD.md).
The [contrast audit](fft-latency/CONTRAST_AUDIT.md) checks intended source
colors, not small-text readability. Neither check completes human review.
The [four encoded caption samples](fft-latency/ENCODED_CAPTION_AUDIT.md)
extend that narrow check to decoded solid glyph interiors in 49–61 s;
thin strokes, antialias edges and intended-device readability remain unassessed.
A [caption-cut timing check](fft-latency/CAPTION_CUT_AUDIT.md) compares decoded
pixels on both sides of all 18 cue changes with outgoing/incoming source
templates. It is not OCR, speech synchronization or full-playback approval.
An optional [snapshot-based QA command](fft-latency/STABLE_QA.md) prevents
ordinary concurrent movie edits from misidentifying a newly generated review
pack; the archived renderer and existing manifests remain unchanged.
An equivalent [plain UTF-8 SRT reading track](fft-latency/SRT_SIDECAR.md)
is available for compatible editors/players. It preserves the 19 WebVTT
cues; it is not speech or a readability fix for the burned-in text.

## Retained studies and supporting drafts

The [retained production studies](PRODUCTION_STUDIES.md) preserve the earlier
comparisons, teasers, packaging and later curves work. They are provenance,
not extra prerequisites to reviewing the one complete copy above. No study
has been adopted or release gate cleared by moving these notes.

## Reproduce

The [fresh-environment source-only rebuild](fft-latency/CLEAN_REBUILD.md)
reproduces the existing MP4, manifest, captions and lesson byte-for-byte on
the same host. It checks a new local environment, not cross-machine output
or release approval; no new version of the movie is distributed.

From `videos/`, with Python 3.11–3.13, uv, FFmpeg (libx264 enabled) and
DejaVu Sans installed:

### Current review focus: full source-only copy

These commands build the copy named in the review instructions above, not
frozen v7. Choose a NEW output directory; the renderer refuses an existing
one. The test command runs the full video workshop suite, including retained
studies. It does not complete human review or authorize publication.

```sh
uv sync --locked
uv run --locked python -m unittest discover -p 'test_*.py'
uv run --locked python source_only_review.py --out out/review-copy-new
uv run --locked python verify_source_review.py out/review-copy-new/fft-source-only-review.mp4 --captions out/review-copy-new/fft-source-only-review.vtt
```

The verifier requires the existing exact movie/caption/source identity before
checking all timestamps and fully decoding. A different host/toolchain may
produce different bytes: investigate a mismatch, do not overwrite archived
evidence or silently adopt the new output. The
[fresh-environment receipt](fft-latency/CLEAN_REBUILD.md) records the earlier
same-host result and its limits. Rebuilding does not distribute a new copy.

### Frozen v7 and alternate fixture: reference commands only

The default `render.py` commands below are NOT the source-only review focus.
`--scenario` is a separate synthetic reuse fixture, not another public episode.

```sh
uv sync --locked
uv run --locked python -m unittest test_video test_qa test_thumbnail test_small_screen test_package -v
uv run --locked python render.py --stills-only
uv run --locked python render.py --out out/full
uv run --locked python render.py --scenario fft-latency/scenarios/half-share.json --stills-only --out out/alternate
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames -show_entries format=duration -of json out/full/fft-latency-draft.mp4
uv run --locked python qa.py out/full/fft-latency-draft.mp4 --out out/review-full
uv run --locked python qa.py out/full/fft-latency-draft.mp4 --out out/review-chronological --every-seconds 1
```

The renderer refuses to overwrite an existing MP4. Choose a new `--out` folder
for each render. `out/` is ignored: do not commit large generated videos.
Pillow is exactly pinned and resolved in `uv.lock`. Tested external encoder:
FFmpeg 6.1.1-3ubuntu5, libx264; exact encoder/font versions can change pixels.
No FFmpeg binary or font is bundled. Install these through your system package
manager; do not assume byte-for-byte output on every machine.

## Content and extension points

- `fft-latency/lesson.json`: scene times, captions/script, question cards and lesson parameters.
- `lesson_model.py`: exact rational timing arithmetic, validation and template expansion.
- `fft-latency/scenarios/half-share.json`: synthetic reuse test, not a replacement public episode.
- `render.py`: reusable text-fitting, bar, timing and caption components.
- `fft-latency/storyboard.md`: editorial and visual direction.
- `fft-latency/captions.vtt`: generated from the lesson, also burned into frames.
- `test_video.py`: arithmetic, cue coverage/reading-rate, frame layout, focus-pixel
  synchronization and checked-in VTT freshness checks.
- `small_screen.py` / `test_small_screen.py`: scaled encoded-sample review packs,
  provenance hashes and input/no-overwrite guards; no device approval.
- `fft-latency/review-version.json` / `test_package.py`: current candidate
  identity, title template and credited-source consistency; no publishing authority.
- `STATUS.md`: provenance, actual validation and next bounded task.

The script is the ordered caption text in `lesson.json`, after expanding its
numeric placeholders (also readable in generated VTT). `load_lesson()` is the
supported construction route for rendering data; do not mutate a loaded
dictionary's numbers without regenerating its captions.
In the four-question scene, each card corresponds to one caption in order;
`cue_at()` drives both the highlighted card and burned caption. Boundaries
belong to the incoming cue. Keep the card/caption counts aligned when editing.
`focus_cards()` draws a persistent four-title strip and only the active
description in a larger panel; copy remains in `lesson.json`. No separate
animation clock or duplicated caption timing is introduced.
Both bar scenes' transition labels, endpoint arrows and `transition_seconds`
live in lesson data. Each transition must finish within its first cue; the ceiling
quotient appears only with its second cue, never beside an intermediate moving total.
An endpoint arrow during a labelled transition means “toward this result,”
not an instantaneous measured total. Settled labels use the exact model value.
No separate narration has been recorded. The current captions are a silent
reading track, not a claim of alignment to speech. Record an authorized human
voice only after editorial review; then retime the cues to that recording.
An [optional human-recording brief and 154-word rehearsal script](fft-latency/NARRATION_BRIEF.md)
now prepares that choice; target timing is tested, but no speech or sync is claimed.
Its neutral ending does not resolve the frozen visual CTA or adopt a release route.
Change the three timing parameters through a scenario file; numeric captions,
equations, variables and bar scales then follow automatically. The script's
qualitative assumptions still need editorial review. This lesson deliberately
requires `0 < fourier_ms < baseline_ms` and `kernel_speedup > 1`: zero-work,
all-Fourier and no-speedup edge cases need a different script. Nonfinite values,
booleans and scenarios with extra keys are rejected. Displayed timings and
kernel speedup must be exactly representable to at most two decimal places;
otherwise validation rejects them instead of printing an incorrect equality.
Nonterminating time fractions such as 1/3 retain rational notation in the
variable definition. Quotients use `≈` when their two-decimal result is rounded.
Very large labels can still fail layout checks; validation is not a substitute
for rendering and editorial review of a new scenario.

The alternate fixture is 200 ms baseline, 100 ms Fourier time, 4× kernel gain:
25+100=125 ms, 1.60× total gain and a 2.00× ideal ceiling. It exercises a
different Fourier share and bar scale, not operational telemetry. Both fixtures
are rendered at every frame in tests; only the original pilot is delivered as
the review video. No dependency change or extra service is needed.

1280×720 landscape, 24 fps. Minimum main caption size 26 px; high contrast;
text labels accompany colors. No flashing or rapid cuts. Review on a real
tablet is still required; automated fit checks cannot certify accessibility.

## Mathematical claim and scope

For sequential work, let `f` be the baseline time fraction improved and `s` the
speedup of that part. Assume unchanged other work, same accuracy and no added
overhead. Then `Tnew/Told = (1-f)+f/s` and overall speedup is its reciprocal.
Here `f=.2, s=2`: `Tnew=80+20/2=90 ms`, `S=100/90≈1.11`.
As `s` tends to infinity the ceiling is `1/.8=1.25`.
This is a reproduced elementary derivation, not a benchmark or new result.
Parallel/overlapped work can require a different latency model.

Complexity counts operations as input grows; numerical stability concerns
computation error; end-to-end latency is elapsed time for the whole workload;
real-time readiness additionally needs deadlines, validation and a system
context. None follows automatically from improvement in another.

Concept placement: Fourier decomposition → efficient discrete computation
(FFT) → a component in a pipeline → end-to-end latency. This is a method/
application link, not an equivalence or proof of grid readiness.

## Sources and provenance

Checked 29 October 2026. All graphics, text layout and bars are original code.
No third-party clips, screenshots, logos, music, voices or research manuscripts.

- [Marimo lesson at inspected source commit](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py): exact local accounting and assumptions. PR #1 is unmerged; no live Pages link is claimed.
- [FFTW authors' accuracy notes](https://fftw.org/accuracy/comments.html): supports separating algorithm runtime from floating-point behavior; this video does not reproduce their benchmark or claim a new FFT.
- [3Blue1Brown Fourier lesson](https://www.3blue1brown.com/lessons/fourier-transforms/): credited educational inspiration only; no reused assets.
- [Lex Fridman episode page](https://lexfridman.com/math-ai-crisis/) and [official transcript](https://lexfridman.com/math-ai-crisis-transcript/): discussion context only, not mathematical verification. No quotes or clips used; timestamp offsets therefore not needed in this draft.

Tool choice: inspected current [Remotion composition](https://www.remotion.dev/docs/composition),
[rendering](https://www.remotion.dev/docs/render), [pricing](https://www.remotion.dev/docs/license/pricing)
and [license FAQ](https://www.remotion.dev/docs/license/faq). Remotion offers a
free tier subject to eligibility (including individuals, teams up to three and
noncommercial evaluation); larger commercial use is not automatically free.
We chose a small Python renderer for this flat-graphic animatic because it
matches the repo and installed tools, and avoids browser setup. No conclusion
about Remotion's suitability or a paid license purchase is implied.

[Pillow ImageDraw docs](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html)
and [license](https://pillow.readthedocs.io/en/stable/about.html): MIT-CMU.
[FFmpeg docs](https://ffmpeg.org/ffmpeg.html) and [legal page](https://ffmpeg.org/legal.html):
licensing depends on build options; the tested GPL-enabled system build stays
external, not redistributed here. DejaVu Sans is a system font; see its
installed copyright/license notice (e.g. `/usr/share/doc/fonts-dejavu-core/copyright`).
No claim that all codec patent/distribution obligations disappear. Recheck
applicable terms before distributing a packaged renderer.

## Encoded-file QA pack

The [dated v5 chronological sample audit](fft-latency/AUDIT_V5.md) records
observations across all eight scenes, the inspected encoded file's hash,
one animation-label refinement and the limits of sampled review. It does
not mark full playback, actual-tablet usability or publication approved.

`qa.py` reads an existing local MP4; it does not rerender, upload or approve it.
Use a **new** output directory on each run. It produces `report.json`, full-size
decoded PNG samples in `frames/`, and six-sample contact sheets. All are ignored
under `out/`. It samples the first/last frames, both sides of each caption cut,
and scene midpoints. The current 80-second lesson yields 39 distinct frames.

Optional `--every-seconds 1` adds each whole-second frame while retaining
all those cut/midpoint/first/last checks: 101 samples and 17 contact sheets
for the current pilot. It accepts positive whole seconds only. Omitting
the option preserves the original selection. The report records the interval;
even dense samples cannot certify unseen frames, smooth motion or pacing.

For the existing larger-caption review, the flat dense selection fails in
the inspected FFmpeg 7.1.5 build. The opt-in [balanced dense export](fft-latency/DENSE_QA.md)
recovers all 101 intended frames without editing archived QA or the movie.
Its actual frame-selection/pixel checks pass; it is not full playback approval.

The report records input SHA256, QA source hash, resolved lesson hash, external
FFmpeg/FFprobe versions, dimensions, duration, frame count/rate and every
frame's constant-rate timestamp check. A complete FFmpeg decode must succeed.
It rejects wrong media geometry/timing and audio-bearing files: narration
requires a separate listening/alignment review, not these silent-draft checks.
Incomplete packs may remain after a decoder failure; no successful report is
written in that case. Existing output directories are never overwritten.

For an alternate rendered scenario, pass the **same** `--scenario` file to QA.
The reported captions and scene names are expected lesson metadata, **not OCR**
or an assertion that the encoded pixels match that scenario. Check the input
hash against the intended render and inspect full-resolution frames; contact
sheets are overview aids, not a substitute for tablet playback, mathematical
review, accessibility checks or publication approval. `publication_approved`
is always false. No voice, external assets, dependencies or binary distributions
were added. See official [FFprobe documentation](https://ffmpeg.org/ffprobe.html)
and [select filter documentation](https://ffmpeg.org/ffmpeg-filters.html#select_002c-aselect).

## Review gates

- [ ] Karin reviews pacing, message and tablet legibility.
- [ ] Verify visual continuity in full playback; inspect the encoded result.
- [ ] Decide silent-explainer versus human narration; if narration, retime captions.
- [ ] Link the verified published interactive lesson (not a guessed URL).
- [ ] Mathematical/editorial and rights approval before upload/publication.

No automatic publishing, account changes, paid service or merge is included.
