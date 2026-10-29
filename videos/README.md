# Math in Context · video workshop

First increment: **80-second silent, captioned visual draft**, not an approved
YouTube release. Original graphics; synthetic numbers; no operational claims.
Video work lives here independently of the Marimo starter PR #1.

Latest revision: **v3** preserves the prediction question without revealing
the answer, and synchronizes a labelled visual focus with each of the four
complexity/stability/latency/readiness captions. Duration remains 80 seconds.

## Reproduce

From `videos/`, with Python 3.11–3.13, uv, FFmpeg (libx264 enabled) and
DejaVu Sans installed:

```sh
uv sync --locked
uv run --locked python -m unittest test_video -v
uv run --locked python render.py --stills-only
uv run --locked python render.py --out out/full
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames -show_entries format=duration -of json out/full/fft-latency-draft.mp4
```

The renderer refuses to overwrite an existing MP4. Choose a new `--out` folder
for each render. `out/` is ignored: do not commit large generated videos.
Pillow is exactly pinned and resolved in `uv.lock`. Tested external encoder:
FFmpeg 6.1.1-3ubuntu5, libx264; exact encoder/font versions can change pixels.
No FFmpeg binary or font is bundled. Install these through your system package
manager; do not assume byte-for-byte output on every machine.

## Content and extension points

- `fft-latency/lesson.json`: scene times, captions/script, question cards and lesson parameters.
- `render.py`: reusable text-fitting, bar, timing and caption components.
- `fft-latency/storyboard.md`: editorial and visual direction.
- `fft-latency/captions.vtt`: generated from the lesson, also burned into frames.
- `test_video.py`: arithmetic, cue coverage/reading-rate, frame layout, focus-pixel
  synchronization and checked-in VTT freshness checks.
- `STATUS.md`: provenance, actual validation and next bounded task.

The script is the ordered caption text in `lesson.json` (also readable in VTT).
In the four-question scene, each card corresponds to one caption in order;
`cue_at()` drives both the highlighted card and burned caption. Boundaries
belong to the incoming cue. Keep the card/caption counts aligned when editing.
No separate narration has been recorded. The current captions are a silent
reading track, not a claim of alignment to speech. Record an authorized human
voice only after editorial review; then retime the cues to that recording.
Numbers in the baseline label are editorial text: when changing the example,
update labels/captions and tests together, not just the numeric parameters.

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

## Review gates

- [ ] Karin reviews pacing, message and tablet legibility.
- [ ] Verify visual continuity in full playback; inspect the encoded result.
- [ ] Decide silent-explainer versus human narration; if narration, retime captions.
- [ ] Link the verified published interactive lesson (not a guessed URL).
- [ ] Mathematical/editorial and rights approval before upload/publication.

No automatic publishing, account changes, paid service or merge is included.
