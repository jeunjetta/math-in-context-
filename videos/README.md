# Math in Context · video workshop

First increment: **80-second silent, captioned visual draft**, not an approved
YouTube release. Original graphics; synthetic numbers; no operational claims.
Video work lives here independently of the Marimo starter PR #1.

**Review without installing anything:** open the
[tablet-friendly editorial handoff](fft-latency/REVIEW.md) for the exact
current script, scene checklist and draft title/description/source links.
It is a review page, not a release approval or live interactive lesson.

The [v7 packaging audit](fft-latency/PACKAGE_AUDIT_V7.md) reconciles current
video/blog handoff identities, the component-specific title and source credits.
Its shared snapshot and regression tests detect narrow drift, not release approval.

Later candidate: [Same-looking curves, different physics](same-looking-curves/STORYBOARD.md)
has an original 82-second unrecorded script, primary-source ledger and tested
geometry helpers. Two [original comparison keyframes](same-looking-curves/KEYFRAMES.md)
now include full/640-pixel previews, source masking and reproducible code.
A [32-second silent camera-study excerpt](same-looking-curves/CAMERA_STUDY.md)
now tests fixed dipole curves under a turning camera, with captions and encoded QA.
A [32-second silent map/potential excerpt](same-looking-curves/MAP_STUDY.md)
now stages matching input/output points, then explicitly returns to the domain
for a chosen potential model. An [86-second integrated silent rough cut](same-looking-curves/EPISODE.md)
now adds 3D orientation, labelled camera cuts and one closing question/source card.
The [exact-version review handoff](same-looking-curves/REVIEW.md) now includes
larger orientation labels, before/after samples and an unchecked reviewer checklist.
The [candidate-bound publication package](same-looking-curves/PACKAGE.md) separates
proposed title/description and primary-source links from internal review prompts.
Its offline copy checks reject lesson/media identity drift; they grant no approval.
One [original curves thumbnail option](same-looking-curves/THUMBNAIL.md) now has
full/640/320-pixel previews, reproducible geometry and candidate-bound hashes.
The [unpublished curves companion](same-looking-curves/SUBSTACK_DRAFT.md) adds
a worked point map and contour-versus-field-line prediction, with primary sources.
It remains unapproved; the FFT pilot remains the first release milestone.
No RH or private NS research claims.

The [v6 smaller-view review pack](fft-latency/SMALL_SCREEN.md) includes three
encoded moments at 640×360 and 960×540, timestamped findings and a reproducible
export command. It flags dense secondary text; it is not an actual-tablet test.

The [Substack companion draft](fft-latency/SUBSTACK_DRAFT.md) supports this
same pilot with a prediction, worked example and source links. It is not
posted or approved; video/lesson destinations remain explicit placeholders.

The [original thumbnail candidate](fft-latency/THUMBNAIL.md) includes full-size
and small previews, a prediction-first hook and model-driven reproduction
commands. It is draft packaging for review, not a performance announcement.

The [live-lesson handoff](fft-latency/LESSON_LINK.md) records the read-only
Pages/Actions audit, current deployment blocker and approval-dependent CTA
verification steps. Passing pilot tests does not establish a deployed lesson.

Latest revision: **v7 focus-first candidate** enlarges the active category's
description while retaining the four titles as context. See the
[encoded v6/v7 comparison and review limits](fft-latency/FOCUS_V7.md).
It has not passed actual-tablet playback or editorial approval.

Retained from v6: moving bars replace animation-generated decimal totals with
endpoint arrows during the two moving-bar beats (18–21 s and 40–43 s).
Exact totals appear only once settled: 90 ms at 21 s and 80 ms at 43 s;
the 1.25× formula still appears with its caption at 44.5 s. The validated
timing model, public 100 → 90 ms example, prediction-first opening and
synchronized question cards are retained; duration remains 80 seconds.

## Reproduce

From `videos/`, with Python 3.11–3.13, uv, FFmpeg (libx264 enabled) and
DejaVu Sans installed:

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
