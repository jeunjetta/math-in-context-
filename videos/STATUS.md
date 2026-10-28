# Video status log

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
