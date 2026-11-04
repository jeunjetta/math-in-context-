# Video status log

## 4 November 2026 · v7 package identity and claim audit

**State:** corrected draft handoffs and tested packaging; v7 video unchanged.

Fresh main `c9fdf98729379dd404afce99daad1a6aa042156e`, unmerged pilot PR #1
`7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`, open video PR #2 source
`b902ecec4099e84aca458715665aeb88d55e0611` inspected. Read main README,
pilot AGENTS/ROADMAP, source/concept registries and actual FFT lesson; video
README/status, REVIEW, Substack/thumbnail handoffs, model/render/tests.
No PR #2 discussion feedback. Fresh detached worktree preserves unrelated work.

Found and corrected concrete drift: Substack editorial notes referenced v5's
old hash; REVIEW's final instruction said v6; THUMBNAIL's final v5 note was
not clearly historical. All now identify the current v7 pairing. Article body
and thumbnail pixels are unchanged. Candidate title now explicitly scopes
the gain: “2× faster FFT—but only 10 ms saved?” No engagement claim.

Added fft-latency/review-version.json (identity, title template, three credited
URLs and false approval snapshot), PACKAGE_AUDIT_V7.md (claim/evidence ledger,
source/destination distinctions and limits) and test_package.py (four narrow
guards). Updated README, REVIEW, SUBSTACK_DRAFT and THUMBNAIL handoffs.
No renderer, lesson JSON, VTT, timing, arithmetic, dependency, lockfile,
notebook, research, audio, MP4 or thumbnail-asset changes.

Actual validation:

- Current v7 MP4 rehashed; matches
  `1d3050b3094f1a090954cb9c2e6ed10e90d438169e86bd2cfbc2a7f13ed74036`.
  No new render or complete decode run; prior results remain in FOCUS_V7.
- Inspected existing encoded 75 s end/source frame and committed 320×180
  thumbnail. Credits match the three URLs in the description/article/README;
  the end-card repo path still is not a verified live exercise destination.
- FFTW accuracy notes and 3Blue1Brown Fourier page retrieved 4 November;
  roles remain implementation context and inspiration, not timing evidence.
- `uv run --locked python -m unittest test_video test_qa test_thumbnail
  test_small_screen test_package -v`: 36 tests pass in 26.571 s, including
  3,840 frame-fit checks, four new packaging guards and prior numerical tests.
  Whitespace check passes. Snapshot/strings are not OCR, semantic certification,
  URL usability tests, human review or publishing permission.

Exact blockers remain tablet/full-playback/pacing and editorial approval,
audio decision (retiming if recorded), authorized lesson deployment/verified
URL and corresponding final CTA/description/source links. All release boxes
remain unchecked; no video upload, Substack/social publication, merge, account
change, purchase, new automation or assumed Open Notebook deployment.

Next bounded work: respond to v7 review if available; otherwise prepare one
source-checked comparison storyboard for the already-proposed later candidate
“Same-looking curves, different physics,” with no private research claims.
Do not use recurring runs to infer approval or keep cosmetically retiming v7.

## 4 November 2026 · v7 focus-first visual candidate

**State:** encoded silent review candidate; no publication approval.

Fresh main `c9fdf98729379dd404afce99daad1a6aa042156e`, open/unmerged pilot
PR #1 `7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`, video PR #2 source
`ad0d35aced7ff2a5e33cc08f128896b0b7604e57` inspected. Read main README,
pilot AGENTS/ROADMAP and source/concept registries, video README/status,
REVIEW/storyboard, renderer/model/tests. No PR #2 discussion feedback.
Fresh detached worktree preserves prior staged/unrelated work.

Addressed SMALL_SCREEN's proposed focus-first candidate: four category titles
remain as context; only the active description appears in an enlarged panel.
Added reusable focus_cards() to render.py, updated border-pixel tests and a
new active-description-only/font-size/cue-edge test. Updated README, REVIEW,
storyboard; added FOCUS_V7.md and one encoded 640-wide comparison PNG.
No lesson JSON, VTT, arithmetic, timing, dependencies, lockfile, notebook,
thumbnail, Substack copy or research changes. Duration stays 80 seconds.

Actual validation:

- `uv run --locked python -m unittest test_video test_qa test_thumbnail
  test_small_screen -v`: 32 tests pass in 25.500 s, including 3,840 frame-fit
  checks across both fixtures and each active description at incoming/last
  outgoing frames. Whitespace check passes.
- `render.py --out out/v7-focus`, then `qa.py
  out/v7-focus/fft-latency-draft.mp4 --out out/qa-v7-focus --every-seconds 1`:
  full decode succeeds, H.264 1280×720, 24 fps, 1,920 verified timestamps,
  80.000 s, zero audio, 101 encoded samples.
- Inspected encoded 49/52/55/58 s full frames, contact sheets 09–14 and
  640-wide v6/v7 stability frames. No visible clipping in inspected samples;
  active description nominally 12→19 px at 640, but inactive titles shrink
  to 13 px. Larger current copy/fewer descriptions is observed, not proof
  of better comprehension, normal-speed readability or accessibility.
- MP4: 669,380 bytes; SHA256
  `1d3050b3094f1a090954cb9c2e6ed10e90d438169e86bd2cfbc2a7f13ed74036`.
  Existing private review-copy identity updated, older versions retained.
  Full output/QA stays ignored; one preview and provenance are in FOCUS_V7.
- Official Pillow drawing/license pages rechecked 4 November; pinned 12.3.0
  and external FFmpeg/font licensing caveats retained. No new assets/audio.

No publishing, YouTube upload, merge, account change, paid service or new
automation. Open Notebook deployment is not assumed. No private research notes,
chat logs, credentials or operator data added to the public branch.

Next bounded step: normal-speed review of v7, especially the three-second
category cues. Absent feedback, audit final packaging/source-card/description
consistency against this exact render, without default retiming or narration.
Exact release blockers remain actual-tablet/full-playback/editorial approval,
audio decision and retiming if needed, authorized lesson deployment/verified
URL and corresponding final CTA/description/source links.

## 3 November 2026 · v6 smaller-view evidence and density findings

**State:** inspectable review assets and a tested exporter; same silent v6
video, not a new render or an approved release.

Fresh main `c9fdf98729379dd404afce99daad1a6aa042156e`, unmerged pilot PR #1
`7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`, open video PR #2 source
`7997d44991a32f20d9365d6d3f3ad9b99cc73bb0` inspected. Read current main
README, pilot AGENTS/ROADMAP and source/concept registries, then video
README/status/REVIEW/storyboard, renderer and QA/tests. No PR #2 discussion
feedback. Fresh detached worktree; previous staged work remains untouched.

Added `small_screen.py`, `test_small_screen.py`, `fft-latency/SMALL_SCREEN.md`
and `fft-latency/small-screen-v6/` (six PNGs and a provenance manifest).
README and REVIEW link the audit. No renderer, lesson, VTT, timing, dependency,
lockfile, thumbnail, Substack, notebook or research changes.

Actual validation:

- Rechecked existing v6 MP4 SHA256
  `2d3a2b0976951c88292229eaebbc6e6a92c4322c2714e09463055f82bead14c9`.
- Fresh `qa.py PATH_TO_V6.mp4 --out out/qa-small-screen --every-seconds 1`:
  complete decode, H.264 1280×720, 24 fps, 1,920 verified timestamps,
  80.000 seconds, zero audio, 101 decoded samples. No new video render.
- `small_screen.py out/qa-small-screen/report.json --out
  fft-latency/small-screen-v6`: six LANCZOS previews from exact encoded
  35/52/75 s samples, at 640×360 and 960×540. All six visually inspected.
- No clipping found in those samples. Main numerical equation stays distinct;
  640-wide card descriptions/source credits are nominally 12 px and the
  README pointer 11 px. Competing card/caption copy is the highest-priority
  density concern, not a measured comprehension failure. Full observations
  and a font-scale table are in SMALL_SCREEN.md.
- `uv run --locked python -m unittest test_video test_qa test_thumbnail
  test_small_screen -v`: final rerun passes 31 tests in 25.986 s, including 3,840 frame-fit
  checks and four new pack tests. Whitespace checks pass.
- Pillow resize documentation/license rechecked; pinned 12.3.0 retained.
  Manifest has hashes and relative image names, no local paths/private data.

Raster dimensions are not CSS/device measurements; stills do not establish
normal-speed readability, pacing, audio sync, accessibility or approval.
No public video upload, publication, merge, paid service, account change,
new automation or assumed Open Notebook deployment.

Next bounded increment, absent feedback: prototype a focus-first four-card
candidate with only the active description enlarged, retaining all four
category titles and existing cue semantics; compare encoded 640-wide frames
and timing against v6 before promoting it. Actual-tablet/full-playback and
editorial approval remain pending. Other exact blockers: audio-format decision,
retiming if human narration chosen, authorized lesson deployment/verified URL
and corresponding final CTA/description/source links.

## 3 November 2026 · v6 removes decorative moving totals

**State:** newly rendered silent review draft, not a finished approved video.

Fresh main `c9fdf98729379dd404afce99daad1a6aa042156e`, unmerged pilot PR #1
`7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`, open video PR #2 source
`049c08ab42bc585ab0fb56b09c2ea5a89629e30c` inspected. Read main/pilot
README, pilot AGENTS/ROADMAP and source/concept registries, then video status,
README, REVIEW, storyboard, audit, lesson/model/renderer and relevant tests.
No PR #2 discussion feedback. A fresh detached worktree preserves earlier
staged work; only videos/ changes are added to the dedicated video branch.

Addressed AUDIT_V5 Finding A, without changing caption cues, scene duration,
example arithmetic, numerical assumptions, source registry or research claims.
Both moving bars now use model-derived endpoint arrows instead of showing
precise-looking easing totals: →90 ms during 18–21 s, →80 ms during 40–43 s.
The first beat is explicitly labelled “TRANSITION · Fourier time ÷ 2” (the
alternate fixture correctly uses ÷4). Exact totals are restored only once
the bars settle. The 43 s limit hold and 44.5 s formula reveal are unchanged.
Data owns the text/timing; bar() accepts an optional total-label override.
Both transition durations are validated to finish within their first cue.

Changed render.py, lesson_model.py, lesson.json, test_video.py, README,
REVIEW, storyboard and a dated note on the historical AUDIT_V5, plus this log.
No dependency, lockfile, audio, font, notebook, thumbnail or Substack changes.

Actual validation on final inputs:

- `uv run --locked python -m unittest test_video test_qa test_thumbnail -v`:
  27 tests pass in 31.691 s, including all 3,840 frame text-fit checks across
  both scenarios, new transition/endpoint text and boundary assertions,
  invalid halve-timing guards, existing ceiling-hold/reveal pixel checks,
  canonical VTT/transcript freshness and encoded QA fixture tests.
- Final render: `uv run --locked python render.py --out out/v6-final`.
- Encoded check: `uv run --locked python qa.py
  out/v6-final/fft-latency-draft.mp4 --out out/qa-v6-final --every-seconds 1`
  (one line). Complete decode succeeds; H.264, 1280x720, 24 fps, 1,920 frames,
  all timestamps verified, 80.000 s, zero audio streams. 101 samples exported.
- Inspected encoded contact sheets 04,05,09,10 covering changed beats and
  cuts; full-size 19 s and 42 s frames inspected for arrow/transition label
  legibility. The 90/80 ms settled labels and 44.5 s formula remain legible
  with no clipping in these samples. This is targeted sampled QA, not full
  playback, an actual-tablet test or comprehension/accessibility approval.
- Final output: 668,634 bytes, SHA256
  `2d3a2b0976951c88292229eaebbc6e6a92c4322c2714e09463055f82bead14c9`.
  An earlier unreviewed local v6 render used a longer transition label; it
  was superseded before delivery. Only the v6-final hash identifies this draft.
- Existing private review-copy identity replaced, retaining previous versions;
  no public video upload. Generated MP4/QA evidence stays ignored in git.
- Official Pillow drawing/license and FFmpeg legal pages rechecked 3 November
  2026. Existing pinned Pillow 12.3.0 retained (current docs are 13.0.0);
  external encoder/font and build-dependent licensing caveats unchanged.

Whitespace validation passes. This does not approve a title/thumbnail/video
combination or clear the learner-link blocker. No publishing, merging, account
changes, paid service, new automation or assumed Open Notebook deployment.

Next bounded increment, if no editorial feedback: inspect v6 at tablet-sized
viewports for the dense formula/four-card/source scenes and record specific
readability findings before proposing any unrelated retiming. Actual-device
normal-speed review still belongs to Karin; scaled stills cannot replace it.
Remaining release gates: full/tablet/editorial review and exact-version
approval, audio-format decision and retiming if narration chosen, authorized
lesson deployment/verified URL and matching final CTA/description/source links.

## 2 November 2026 · chronological v5 encoded-sample audit

**State:** concrete timestamped audit and denser QA coverage, not full human
playback, an updated video or release approval.

Fresh main `c9fdf98729379dd404afce99daad1a6aa042156e`, open pilot PR #1
`7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`, video PR #2 source
`2fdc751d517e79451b774634107d6366a95c0187` inspected. Read main and pilot
README, pilot AGENTS/ROADMAP (absent on main/video), source/concept registries;
video README/status/REVIEW/storyboard/captions/model/renderer and QA/tests.
PR #2 discussion timeline has no feedback. Used a fresh detached worktree;
older staged checkouts and all non-video work remain untouched.

Added optional `qa.py --every-seconds N` (positive whole seconds). It retains
the existing 39 cue/scene/edge samples and adds regular chronological frames.
Omission preserves existing behavior. Selection is validated before creating
an output directory; report records the interval. Updated `test_qa.py` and
README; new `fft-latency/AUDIT_V5.md` contains timestamped findings and limits.
No lesson, renderer, caption, thumbnail, Substack or research changes.

Actual validation:

- Complete decode of the matching existing silent v5 MP4 succeeds. Input
  SHA256 `d2a0365545602c55af3ee6018944045a5804a125b0dd5af80d7585c85efe12d4`;
  H.264, 1280x720, 24 fps, 1,920 timestamps verified, 80.000 seconds, no audio.
- Ran `uv run --locked python qa.py PATH_TO_MATCHING_V5.mp4 --out
  out/audit-v5 --every-seconds 1` (one line). 101 frames, 17 contact sheets;
  inspected all sheets in chronological order and full-resolution 19 s,
  35 s and 49 s samples. New QA source SHA256 in the generated report:
  `45ae6c25baf9f54564c8cf4cf95ee2e8590ed988fc5e732e9cf96fc21094d9b9`.
- `uv run --locked python -m unittest test_video test_qa test_thumbnail -v`:
  25 tests pass in 25.144 s, including all 3,840 rendered-frame fit checks,
  encoded fixture/report checks and the new regular-sampling test. The latter
  checks default 39 coverage, whole seconds, preserved cuts, sorted unique
  selection, final frame and invalid intervals. No dependency/lock change.
- Whitespace check passes. Official FFmpeg select and license/build pages
  rechecked 2 November 2026; existing external build/font caveats retained.

Finding A (editorial clarity, not wrong endpoint math): 18–21 s and 40–43 s
show precise-looking intermediate totals produced by easing (e.g. 97.41 ms
at 19 s). They are not measured timing results and add unnecessary reading
load. Recommend transition/endpoint cues during motion, exact endpoint labels
once settled, while preserving the 43 s hold and 44.5 s ceiling-formula reveal.
The complete timestamp table distinguishes sampled checks from human pacing
questions. No sampled clipping/missing scene/wrong final value was found.
No full normal-speed/tablet review, all-frame visual check, audio listening,
comprehension or publication approval is claimed. Do not clear those gates.

Render status: video unchanged; no new MP4 render or review-copy replacement.
Generated QA evidence stays ignored under out/ and can be reproduced; no new
public binary assets. No publishing, merging, account changes, purchases,
automation creation or assumed Open Notebook deployment. Existing source-path
CTA is still not a verified live learner URL; PR #1 remains unmerged.

Next bounded increment: address Finding A in the two animation beats with
targeted boundary tests, render a new draft and inspect its encoded result.
Do not change unrelated scenes or mark release approved. Remaining blockers:
Karin's full/tablet/editorial review and exact-version approval; audio decision
and retiming if narration; authorized lesson deployment/verified URL and matching
final CTA/description. This audit is not evidence those conditions are met.

## 2 November 2026 · original prediction-first thumbnail candidate

**State:** reviewable video packaging, not an approved thumbnail or release.

Fresh remote main `c9fdf98729379dd404afce99daad1a6aa042156e`, open pilot PR #1
`7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`, and open video PR #2 source
`88a935885bc1492c472239b4817b867a1568f9e2` inspected before this increment.
Main/video have no AGENTS or ROADMAP; read both from current pilot PR #1,
along with its README, source/concept registries and complete lesson notebook.
Read video README, status, review, lesson/model/renderer and relevant tests.
PR #2 has no comments/reviews in the retrieved discussion timeline. A fresh
detached worktree avoids the older checkout's staged changes; those are untouched.
All changes remain under `videos/` on the dedicated video branch/PR.

Added `thumbnail.py`, `test_thumbnail.py`, `fft-latency/thumbnail.json`,
`fft-latency/THUMBNAIL.md` and two small PNGs under
`fft-latency/thumbnail-candidate/`; README and REVIEW link the candidate.
The hook asks “2× faster FFT. 2× faster system?” rather than asserts a total
gain. The canonical model drives the proportional baseline 20/80 ms bar and
text, including alternate-scenario checks. Original code-drawn graphics only,
with explicit synthetic/draft labels, question mark, text alongside color,
alt text and a bottom-right overlay reserve. No answer reveal in the thumbnail.
No screenshots, third-party visual assets, private data, audio or generated voice.

Actual validation:

- `uv run --locked python -m unittest test_video test_qa test_thumbnail -v`:
  24 tests pass in 49.995 s, including all 3,840 frame text-fit checks,
  VTT/transcript, encoded-fixture QA and four new thumbnail tests.
- New tests check model values, proportional boundary pixels, actually drawn
  hook/qualifier/draft text, alternate 200 ms/100 ms/4× rendering, decoded PNG
  sizes/mode/file size and refusal to overwrite existing output folders.
- Exported with `uv run --locked python thumbnail.py --out
  fft-latency/thumbnail-candidate` (one line), then inspected both 1280×720
  and 320×180 images for text clipping, question mark, labels and balance.
  This is desktop visual inspection, not actual-tablet testing or CTR evidence.
- Full PNG: 43,371 bytes, SHA256
  `ea7f5e46f2d6f188ed1fb651c38d99d2e6a3d5160de9f7d93f3d5bdb929cf58d`.
  Small preview: 24,269 bytes, SHA256
  `3c829f164872cb3321e02c0a5c71387b57b731b5e1d3df9d7fe5965d02252578`.
- Whitespace check passes. Official Pillow drawing/license docs and YouTube
  thumbnail help rechecked on 2 November 2026; links and provenance in
  THUMBNAIL.md. Locked Pillow 12.3.0 retained; current docs are 13.0.0.
  No dependency, lockfile, font binary or renderer-tool choice change.

Render status: existing 80-second silent v5 MP4 unchanged, no new video render
or review-copy replacement. Captions, lesson arithmetic, Substack article,
research conclusions, source registry and Marimo pilot are unchanged. No new
automation, purchase, public video/social/blog posting, merge, account change
or assumed Open Notebook deployment. The committed PNGs are draft PR assets,
not a YouTube upload. Publication approval remains absent.

Next bounded increment if no feedback: audit the complete silent v5 playback
in chronological segments, record timestamped issues rather than another
packaging draft, and fix only any specific pacing/continuity defect found.
Remaining release blockers: Karin's full/tablet/editorial review and exact-
revision approval; audio-format decision (and retiming if narration chosen);
authorized lesson deployment/verified learner URL and final matching links.
The target dates in unmerged PR #1 are not evidence that these gates passed.

## 1 November 2026 · Substack companion draft for the pilot

**State:** reviewable supporting copy, not a published post or video approval.

Fresh remote main `c9fdf98729379dd404afce99daad1a6aa042156e`; open pilot
PR #1 `7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`; draft video PR #2
source `d911032ab6edccde549cb07a4c5a7202d0c94594` before this increment.
Read current README/main and pilot, AGENTS/ROADMAP, source/concept registries,
pilot notebook and video README/status/REVIEW/model/tests. No PR #2 feedback.
Local editable inputs matched remote Git blob hashes. Work remains under
`videos/` on the existing dedicated branch.

Added `fft-latency/SUBSTACK_DRAFT.md` with reader-facing copy separated from
editorial notes: a prediction, worked before/after table, percent-versus-ratio
distinction, ideal ceiling, explicit assumptions, the four claim categories,
concept placement and sources. Video and lesson URLs remain placeholders.
The slider prompt explicitly compares hypothetical workloads rather than
prescribing extra computation. No operational data or research claims.
README links the draft; two regression tests check its numerical block against
the canonical timing model and retain draft labels/unresolved links/gates.

Verification: 20 tests pass in 43.128 seconds, including all 3,840 frame checks,
VTT/transcript, encoded-fixture QA and both new draft checks. After one wording
clarification outside the checked block, both draft tests were rerun and pass.
Complete Markdown was manually inspected for calculation, claim scope, links,
table/heading structure and separation of editorial material. Whitespace check
passes. Substack rendering and actual-tablet preview are not claimed tested.
FFTW's primary accuracy notes and the original 3Blue1Brown Fourier lesson were
retrieved on 1 November 2026; no quoted prose or third-party assets reused.

Render status: existing silent v5 unchanged; no new render or review-copy upload.
SHA256 rechecked:
`d2a0365545602c55af3ee6018944045a5804a125b0dd5af80d7585c85efe12d4`.
No renderer, lesson, notebook, dependency, lockfile, audio or source registry
changed. Open Notebook deployment remains unassumed. No purchase, publishing,
merge, account setting change or new automation.

Next bounded video-packaging increment, absent editorial feedback: prepare an
original code-generated thumbnail candidate based on this same synthetic
pipeline, with a readable prediction hook and no new performance claims.
Release still needs Karin's full video/tablet/editorial review, audio decision,
authorized lesson deployment/verified URL, matching final links and explicit
approval for the exact video and article revisions. Do not publish the draft.

## 1 November 2026 · v5 ceiling transition clarified

**State:** updated rendered review draft, not a publication-approved video.

Fresh main `c9fdf98729379dd404afce99daad1a6aa042156e`; open pilot PR #1
`7905dc2b30ad9c05436f4db4a03d9cfe34224ffc`; draft video PR #2 source
baseline `da902ae170f1e39813b8e39c6d273d414289f3c5` before this increment.
Read remote main/pilot README, AGENTS/ROADMAP, source/concept registries;
video status/render/model/data, then current handoff/storyboard/README/tests.
Editable local inputs matched remote Git blob hashes; no PR #2 feedback.
All changes remain on `codex/video-fft-latency`, under `videos/` only.

Changed renderer, lesson data/model, tests, README, storyboard, REVIEW and
this log. No dependency, canonical caption/VTT, duration, example arithmetic,
source registry, notebook or research conclusion changed. The ceiling scene
now labels its 40–43 s moving bar as a transition, holds the final 80 ms value
from 43 s, and reveals the 1.25x formula with its cue at 44.5 s. Text/timing
configuration lives in lesson data; a guard requires the transition to end
before the second cue. The alternate fixture likewise ends at 100 ms/2.00x.

Validation actually completed:

- Full locked suite: 18 tests pass in 23.417 seconds, including all 3,840
  frame text-fit checks across both synthetic scenarios and new transition/
  hold/reveal boundary, amber-only limit bar and invalid-timing checks.
- After editorial documentation updates, both transcript/gate tests pass
  again. Canonical VTT is unchanged. Staged whitespace checks pass.
- Full original render: `uv run --locked python render.py --out out/v5`.
- Encoded QA: `uv run --locked python qa.py out/v5/fft-latency-draft.mp4
  --out out/qa-v5` (one line). Complete decode succeeds; H.264, 1280x720,
  24 fps, 1,920 frames, 80.000 s, zero audio streams; all frame timestamps
  verified. QA exported 39 samples/seven contact sheets. No alternate full
  video is claimed; that scenario is covered by rendered-frame tests.
- Inspected encoded contact sheet 04 (40 s cut, 44.5 s cue reveal, 49 s cut)
  and an additional full-size frame at exactly 43 s. Labels, 80 ms hold and
  equation are readable with no visible clipping in those samples. This is
  sampled QA, not full human playback or an actual-tablet usability review.
- New MP4: 701,569 bytes; SHA256
  `d2a0365545602c55af3ee6018944045a5804a125b0dd5af80d7585c85efe12d4`.
- Existing review-copy identity is used for replacement, preserving earlier
  versions. No new public upload or publishing approval is implied.
- Pillow drawing documentation and FFmpeg's official legal page were checked
  on 1 November 2026. Existing pinned Pillow 12.3.0 remains; no upgrade to
  the newer documentation version or renderer/license change is implied.
  GPL-enabled system encoder stays external; no font/binary redistribution.

Next bounded supporting-content increment, absent review feedback: draft a
short Substack companion for this same pilot with one prediction, the worked
100->90 ms calculation and a learning-link placeholder, not another topic.
Do not post it. Human pacing/tablet review, silent-versus-human-narration
choice, authorized lesson deployment/verified URL, final CTA and exact-version
publication approval remain release gates. Open Notebook is not assumed
deployed. No merges, settings changes, paid service, telemetry, private notes,
public posts or new automation were included.

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
