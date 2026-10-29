# Video status log

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
