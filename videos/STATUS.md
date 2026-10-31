# Video status log

## 31 October 2026 · reproducible encoded-video QA

**State:** tested local QA increment; existing silent v4 MP4 unchanged.

Fresh remote main `c9fdf98729379dd404afce99daad1a6aa042156e`; open pilot
PR #1 `7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`; draft video PR #2
`e066989c54c789836a7ff377eed4725d8b21cf2f` before this increment. Read
current main/pilot README, AGENTS/ROADMAP, source/concept registries and video
README/status/render/model/storyboard. No PR #2 comments. Local editable
inputs matched remote Git blob hashes. Changes remain only under `videos/`.

Added `qa.py` and `test_qa.py`; updated README commands/limitations and this
log. No lesson, renderer, caption, math conclusion, dependency or audio change.
QA reads a local encoded file, verifies dimensions/duration/frame count/rate
and each presentation timestamp, then fully decodes it with error-stop enabled.
Samples both sides of caption cuts plus scene midpoints and first/last frames;
exports full-resolution PNGs, labelled contact sheets and JSON provenance.
The report includes file/tool/lesson hashes and encoder/prober versions, not
private paths or arbitrary source metadata. It never grants release approval.
Unexpected audio requires a separate sync review. Existing packs are protected
from overwrite; incomplete packs after failure are not successful reports.

Validation: complete suite `uv run --locked python -m unittest test_video
test_qa -v` passed all 16 tests in 38.590 seconds, including all 3,840 existing
layout frames and four new QA tests. New coverage includes cue-cut selection,
wrong geometry/rate/count/timestamps/duration/audio rejection, a real local
synthetic H.264 fixture, report/sample output and no-overwrite behavior.
After adding tool-version metadata, the four QA tests were rerun successfully.
No notebook was modified; its check/export is not newly claimed here.

Actual command on the unchanged v4 MP4:
`uv run --locked python qa.py out/v4/fft-latency-draft.mp4 --out
out/qa-v4-20261031-final` (one line). Result: 39 samples, seven sheets;
H.264, 1280x720, 24 fps, 1,920 frames, 80.000 s, zero audio streams;
all presentation timestamps verified and complete decode succeeded.
Input SHA256 remains
`2035c73833e041e6eee7317705139660cfdc2c68c11907c435b4d14ec39abd37`.
Outputs stay in ignored `out/`; no new MP4 render or review-copy upload.
Inspected contact sheets 04, 06 and 07 covering formula/ceiling, question/
readiness cuts and end-card transitions; no visible clipping in those samples.
Full-resolution frames remain available for closer reading. This is sampled
QA, not full human playback or actual-tablet accessibility certification.

Official FFprobe/filter pages initially timed out; their official indexed
documentation and upstream FFmpeg source documentation were retrieved for
the frame/JSON/select options. Existing FFmpeg/Pillow license caveats remain;
no packaged binaries, external assets, paid services or new dependencies.

Next bounded editorial/code increment: clarify the ceiling transition's
moving total versus final limit. At 40.000 s the bar still shows 90 ms while
the 1.25x ideal-limit formula is already present; it reaches 80 ms by 43 s.
This is a review point, not wrong final arithmetic. Consider distinct labels
or delaying the final formula until the animation finishes, with a boundary
regression test and encoded-frame review. Do not change the final 80 ms limit.
The report's expected caption metadata is not OCR or proof that a supplied
video matches a lesson; inspect pixels and verify the intended input hash.
Release blockers remain human/tablet review, audio decision, an authorized
lesson deployment/verified URL, final CTA and exact-version publication
approval. Open Notebook deployment is not assumed. No merge, publishing,
settings change, workflow rerun, private data or research claims included.

## 31 October 2026 · live-lesson release-dependency audit

**State:** concrete deployment blocker identified; silent v4 remains unapproved.

Fresh source: main `c9fdf98729379dd404afce99daad1a6aa042156e`, open pilot
PR #1 `7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`, draft video PR #2
`c15591adcaa07b97467afbec10e862e9bb76fc21`. Read remote main/pilot README,
pilot AGENTS/ROADMAP, source/concept registries, notebook and deployment
workflow; current video README/status/review, lesson data and renderer.
No PR #2 feedback. Editable local files matched the remote Git blob hashes.

Read-only public Actions history returned five runs. Pilot content tests
succeeded at its current head (run 40734730180), but the sole Pages run
40723050432 failed on 28 October at main's original template commit.
Its build/export and artifact upload succeeded; deploy failed with HTTP 404.
The failure annotation advises checking whether Pages is enabled. Public
Pages metadata also returned 404; authenticated settings were not inspected.
This identifies a deployment gate, not a definitive settings diagnosis or an
FFT/render failure. No successful Pages run or actual lesson URL was found.
The main build did not include the unmerged FFT lesson. Official GitHub Pages
custom-workflow docs were checked; no setting, workflow or deployment changed.

Added `fft-latency/LESSON_LINK.md`: dated evidence table, current end-card
inventory, ordered approval-dependent handoff and pending verification fields.
Linked from README and REVIEW. Added an offline regression test checking the
actual drawn draft end-card pointer and the handoff's pending status. The
description placeholder stays intact; no guessed Pages address or Open
Notebook deployment is substituted. All changes remain under `videos/`.

Render status: unchanged v4, no rerender or new playback approval claimed.
Validation: all 12 locked-environment unittest tests pass in 45.828 seconds,
including all 3,840 frame text-fit checks across both synthetic scenarios,
canonical VTT/transcript checks and the new drawn end-card/handoff test.
Complete handoff Markdown inspected; staged whitespace check is clean.
SHA256 rechecked:
`2035c73833e041e6eee7317705139660cfdc2c68c11907c435b4d14ec39abd37`.
The existing review MP4 is unchanged; no replacement upload is needed.

Next bounded code increment, absent editorial feedback: a reusable local QA
command to extract encoded scene/caption-boundary contact sheets and media
facts, making future human reviews reproducible without publishing anything.
Release still needs an authorized PR #1 merge/publishing-source decision,
successful deployment containing the lesson, actual tablet interaction check,
matching final CTA/description, audio decision and exact-version publication
approval. These release gates do not block continued local QA work.
No merge, settings change, workflow rerun, paid service, public upload, private
data or research conclusion was included. No new automation was created.

## 30 October 2026 · editorial handoff for v4

**State:** review materials ready; video remains the same unapproved silent v4.

Fresh retrieval: main `c9fdf98729379dd404afce99daad1a6aa042156e`, open
pilot PR #1 `7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`, video PR #2
`448987cc64d01e6162614eedfc831b9c3172e981`. Read current main/pilot README,
AGENTS, ROADMAP, source/concept registries; current video README/status,
lesson data, storyboard and VTT. No new video PR comments. Relevant local
handoff inputs matched the freshly inspected remote source before edits.

Added `fft-latency/REVIEW.md`: tablet-readable exact caption transcript,
eight-shot review table, assumptions and arithmetic, draft title/description,
source/credit links, feedback template and deliberately unchecked release gates.
Linked it from `videos/README.md`. Added two regression tests to `test_video.py`
for transcript/timing freshness and draft/gate preservation. No renderer,
lesson, numerical model, dependency or audio was changed.

Validation: 11 tests pass in 55.787 seconds, including all 3,840 frame checks
across the two existing scenarios. After removing Markdown hard-break trailing
spaces, the two handoff-specific tests were rerun and pass. Manually inspected
the complete Markdown handoff for script, timing, arithmetic and draft labels.
FFTW's primary accuracy notes and the original 3Blue1Brown Fourier lesson
were retrieved on 30 October 2026 for source/credit verification. No quotes,
third-party footage, music or voices are used. No research conclusions added.

Render status: no new render needed or claimed; this handoff describes v4,
80.000 seconds, silent, SHA256
`2035c73833e041e6eee7317705139660cfdc2c68c11907c435b4d14ec39abd37`.
The existing review MP4 is not republished or replaced for a documentation change.
No full human playback or actual-tablet accessibility review is marked complete.

Next bounded step: perform a read-only publication-readiness check of the
pilot's Pages/Actions state and the end-card call-to-action; if not live, keep
the explicit placeholder and record the exact missing gate. Do not enable
Pages or alter settings without approval. Incorporate any Karin feedback
before producing another cosmetic render. Full review, audio choice, live
lesson URL and explicit publication approval remain release blockers, not
technical-render blockers. No merge, public upload, purchase, account change
or new automation performed. Other agents' files remain untouched.

## 30 October 2026 · FFT/latency visual draft v4

**State:** reusable-model/code increment with rerendered original review pilot;
not a new episode or approved public release.

### Retrieved state and files

Fresh main `c9fdf98729379dd404afce99daad1a6aa042156e`; open pilot PR #1
at `7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`; video PR #2 at
`0aaa36497a78ccdd03306dada72c324f9507e04d` before this increment. Read
remote main/pilot README, AGENTS, ROADMAP, sources, concept links and pilot
notebook; then video README/status/render/tests/data. No new PR #2 comments.
Local editable video sources matched the remote head before edits.
All modifications remain under `videos/` on `codex/video-fft-latency`.

Added `lesson_model.py` and `fft-latency/scenarios/half-share.json`; changed
lesson templates, renderer, tests, generated VTT, README and this log.
Numeric captions/labels now share exact rational calculations; bar lengths
scale against the baseline, rather than a fixed 100 ms assumption.
Added input/precision guards and exact-versus-rounded quotient notation.
The public pilot stays 100 → 90 ms; alternate 200 → 125 ms is only a reuse test.

### Verification

- Initial new text-capture test sampled the second result cue rather than its
  sum cue, so its expectation failed. Corrected test sample to 28 s; no
  production change was needed for that failure.
- Final locked run from `videos/`: 9 tests pass in 23.461 seconds,
  including arithmetic/text assertions and bar-color pixel
  checks for the alternate scenario; VTT freshness; cue/focus synchronization;
  invalid/rounded-input guards; all 3,840 frames across both scenarios fit.
- A verification invocation from the repo root failed to import `test_video`;
  rerunning from the documented `videos/` directory passed. No dependency fix
  or project-wide environment change was needed. Whitespace checks pass.
- Full original pilot render `out/v4/fft-latency-draft.mp4`: H.264, 720p,
  24 fps, 1,920 frames, 80.000 s, 694,441 bytes, deliberately no audio.
- Full encoded-file decode succeeds; extracted original result frame at 28 s.
  Original formula and alternate formula/bar/ceiling stills inspected, with
  correct 125 ms / 1.60× / 2.00× alternate results and no visible clipping.
- Alternate CLI still export succeeds; no alternate full MP4 is claimed.
- Original MP4 SHA256:
  `2035c73833e041e6eee7317705139660cfdc2c68c11907c435b4d14ec39abd37`.
- Python's official Fraction docs and FFmpeg legal page checked on 30 October
  2026. Existing Python/Pillow/FFmpeg tool choice and dependency lock retained;
  no paid service, new package, downloaded asset or redistributed binary.
- No notebook, source registry, research conclusion, public upload or merge
  changed. Open Notebook deployment and Pages availability remain unverified.

### Next bounded step / exact remaining gates

Before adding another topic, prepare an editorial handoff for this pilot:
plain script, shot-level review checklist and draft description/source links,
all explicitly marked for Karin's approval. These can be reviewed on a tablet
without running the renderer. Publication still needs full human/tablet playback,
audio-format decision and verified live Marimo link. No technical render blocker.

## 29 October 2026 · FFT/latency visual draft v3

**State:** updated rendered review draft; no publication approval claimed.

### Retrieved state

- Fresh main remains `c9fdf98729379dd404afce99daad1a6aa042156e`.
- Open PR #1 remains at `7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`;
  video PR #2 at `e1aba4305ab5cc7e031b1e47e870db80f757dbfc` before this increment.
- Read current remote README, pilot AGENTS/ROADMAP/source and concept registries,
  video README/status/render/data/tests. PR #2 has no review comments.
- Editable local source files matched the inspected remote head before edits.
  Continuing the same dedicated branch; no changes outside `videos/`.

### Bounded changes

- Opening now asks the question instead of displaying a not-equal answer during
  the prediction pause. The mathematical conclusion is unchanged.
- Four distinct 3-second captions now each have one outlined, labelled focus
  card. Card content moved into lesson data; muted cards remain legible.
- Added shared `cue_at()` timing for captions and attention cues, pixel-level
  focus tests at incoming/outgoing boundaries and VTT freshness regression test.
- Updated lesson JSON, renderer, tests, regenerated VTT, storyboard, README and
  this status log. No new external assets/dependencies or narration.

### Validation actually completed

- Same pinned Pillow 12.3.0/uv lock; 6 unittest tests pass in 12.759 seconds,
  including all 1,920 frame text-fit checks and caption reading-rate guard.
- Full render: `uv run --locked python render.py --out out/v3` succeeds.
- FFprobe: H.264, 1280×720, 24 fps, 1,920 frames, 80.000 seconds,
  672,514 bytes, deliberately no audio.
- Full encoded video decodes without reported errors. Inspected opening and
  card stills plus four encoded samples from 49–61 seconds: focus progresses
  complexity, stability, latency, readiness with its matching caption; no
  visible clipping. These are sampled checks, not full human playback review.
- New MP4 SHA256:
  `478ac6d896bb557dad694c1cd1e8ff4de90d76fc10e3c080fbb937a96b40cebd`.
- Output remains ignored, not committed. Updating the existing review-copy
  identity preserves the prior version. Nothing uploaded to a public platform.
- Pillow drawing/docs/license rechecked; no renderer change or paid service.
  The FFmpeg legal page timed out on recheck; the prior build/license caveat in
  README remains unchanged. No binaries/fonts are redistributed.
- No notebook modified; pilot/tablet/Pages validation is not reclassified as
  complete. No research material or conclusions changed.

### Next action and blockers

Next code increment, if editorial feedback is not yet available: remove the
remaining hard-coded numerical labels/scales and add a second synthetic
parameter set to test reuse without caption/graphics contradictions.
Release still requires full human/tablet playback review, the silent-versus-
authorized-human-narration decision, a verified live lesson link and publication
approval. Technical rendering is not blocked. PR #1 is still unmerged.

## 29 October 2026 · FFT/latency visual draft v2

**State:** rendered technical preview, not editorially approved or published.

### Retrieved state and provenance

- Fresh remote `main`: `c9fdf98729379dd404afce99daad1a6aa042156e`.
- Only open PR at retrieval: #1, head
  `7905dc2b30ad9c05436f4db4a03d9cfe34224ffc` (unmerged).
- Read main README and PR-head README, AGENTS, ROADMAP, source/concept registries
  and `apps/fft_and_latency.py`. No prior video status/branch existed.
- Dedicated branch `codex/video-fft-latency` starts from main; all changes
  confined to `videos/`. PR #1 and research conclusions are untouched.
- No Open Notebook deployment assumed. No private notes, telemetry or credentials.

### Delivered files

Python renderer/reusable components; lesson/scene data; script in caption data;
storyboard; WebVTT captions; README with commands, provenance and license notes;
exact Pillow dependency + uv lock; tests; this log.
Generated MP4 and eight review stills live in ignored `videos/out/v2/` locally,
not as binary files in the source PR. A review copy is delivered separately.

### Validation actually completed

- `uv lock`, `uv sync --locked`: successful. Pillow 12.3.0, Python 3.12.14.
- `uv run --locked python -m unittest test_video -v`: 4 tests pass (22.817 s).
  Includes 1,920 frame render/text-fit checks, arithmetic, scene/caption coverage,
  <=21 caption characters/second and boundary/glyph smoke checks.
- First test caught overflowing intermediate decimal labels; display rounding
  repaired. Visual inspection caught exact-equals on a rounded quotient; changed
  to approximation sign, separated variable definitions and rerendered v2.
- `uv run --locked python render.py --out out/v2`: successful.
- FFprobe: H.264, 1280×720, 24 fps, 1,920 frames, 80.000 s, 650,856 bytes,
  no audio stream (deliberate).
- Full encoded-file FFmpeg decode to null: successful, no reported errors.
- Inspected all eight scene midpoint stills (across v1/v2) and v2 encoded frame
  at 35 s: text/notation/bars readable, no visible clipping. This is sampled
  visual QA, not a complete human playback review or accessibility certification.
- MP4 SHA256:
  `222507bf0c654a8d120688a9580ef5f8fdeea3a64182cd61e34224609f906646`.
- Captions burned in from canonical cue data; separate VTT from the same data.
  No speech exists, so audio synchronization is not yet applicable.
- `git diff --check`: clean. No Marimo notebook modified; notebook integration
  still depends on unmerged PR #1 and unverified Pages/tablet checks.

### Next bounded increment / exact remaining gates

1. Review complete playback and scene transitions at tablet size; improve pace
   and the four-question card if comprehension needs more breathing room.
2. Karin chooses silent version or an authorized human narration; record and
   retime captions if narration is chosen. No fabricated/cloned voice.
3. Replace repository-path call to action with a verified published Marimo URL
   once the separate pilot clears its gates.

No technical render blocker remains. Outstanding release gates: human editorial/
mathematical review, real tablet usability, final audio decision, verified lesson
link and explicit publication approval. No uploads, merges, paid services,
account changes or new automations performed.
