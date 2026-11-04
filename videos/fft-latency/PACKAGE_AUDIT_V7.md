# v7 · packaging and claim audit

4 November 2026. **Draft consistency audit, not release approval.**
Inspected source `b902ecec4099e84aca458715665aeb88d55e0611` on open PR #2;
pilot PR #1 remains unmerged. No new MP4, audio, thumbnail artwork or article
body was produced. Open Notebook is not assumed deployed.

## Corrected handoff drift

- Substack editorial notes still named v5 and its old hash. They now identify
  the current v7 candidate and exact MP4; reader-facing article copy is unchanged.
- REVIEW's final instruction still said to keep a v6 label. It now says v7.
- THUMBNAIL's closing note referred to an unchanged v5 video without making
  that historical context clear. The note now records the current pairing.
- Candidate title now explicitly names the accelerated component:
  **2× faster FFT—but only 10 ms saved?** The old “Twice as fast…” title
  could leave that component ambiguous outside the video. This is editorial
  clarification, not a tested engagement/CTR improvement.

The [review identity snapshot](review-version.json) records the exact renderer
commit, MP4 hash, silent format, model-derived title template and three credited
sources. It is a review snapshot, not a trusted approval registry or upload gate.
Its false publication flag does not substitute for Karin's explicit approval.

## Claim-to-evidence ledger

| Claim or packaging element | Grounding | Required limitation |
|---|---|---|
| “2× faster FFT” in title/thumbnail | Hypothetical component gain s=2 in lesson.json | Not a newly implemented algorithm or measured benchmark |
| 100 ms baseline = 20 + 80 | Invented sequential workload; canonical model and pilot source agree | Not a PMU interval, operational deadline or grid telemetry |
| 90 ms after improvement | 20/2 + 80 = 90 | Same accuracy, unchanged other work, no added overhead |
| 10 ms saved; 10% less elapsed time | 100−90=10; 10/100=0.1 | Not a 10% speedup-ratio calculation |
| About 1.11× overall speedup | 100/90=10/9, rounded | Approximation, not equality to 1.11 |
| 1.25× ceiling | 100/80=1.25 as Fourier time tends to zero | Limit of this toy sequential model; parallel critical paths can differ |
| Four category cards | Separate operation count, numerical error, elapsed time and validated deadlines | Improvement in one does not certify another |
| Thumbnail's “2× FASTER SYSTEM?” | Prediction question; baseline blocks show 20/80 | Preserve question mark and synthetic qualifier; not an achieved gain |
| Fourier → FFT → latency | Method/application context | Not an equivalence, readiness result or research proof |

The numerical identities are reproduced elementary accounting, not research
novelty. The existing Substack model-block tests and video-model tests remain
the numerical guards; this audit does not certify arbitrary prose semantics.

## Credits and destination check

The encoded 75 s source card names FFTW accuracy notes, the linked Marimo
derivation and 3Blue1Brown's Fourier lesson, and points to videos/README.md
for full URLs. The README, draft YouTube description and Substack article all
carry the same three URLs recorded in review-version.json.

- [Pinned Marimo source](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py): read from the current PR #1 source; supports the invented calculation and assumptions. A GitHub source page is **not a deployed exercise**.
- [FFTW authors' accuracy notes](https://fftw.org/accuracy/comments.html): retrieved 4 November; supports keeping implementation-dependent floating-point behavior distinct from runtime. Its historical comparisons are not evidence for our invented timings or a current fastest FFT.
- [3Blue1Brown Fourier lesson](https://www.3blue1brown.com/lessons/fourier-transforms/): retrieved 4 November; educational inspiration only. No footage, distinctive assets, quotes or narration are used.

The source card's repo path remains a **public-release blocker**, not a usable
learner CTA. The lesson/video destination placeholders are deliberately retained.
No Pages deployment, account eligibility, end-to-end link journey or new hosting
status is inferred. This audit does not repeat the deployment investigation.
No podcast statement or private Navier–Stokes checkpoint validates this lesson.

## Exact candidate and validation

MP4 SHA256:
`1d3050b3094f1a090954cb9c2e6ed10e90d438169e86bd2cfbc2a7f13ed74036`.
The existing local v7 file was rehashed and matches. Its previous complete
decode/render checks are in [FOCUS_V7.md](FOCUS_V7.md), not rerun here.
Inspected the existing encoded 75 s frame and committed 320×180 thumbnail;
no credit clipping visible in those samples. This is not normal-speed playback,
actual-tablet testing, audio alignment, accessibility or editorial approval.

Four new tests check current handoff identities, model-derived title/thumbnail
question scope, shared credited URLs/actual renderer source-card strings and
retained release gates. They do not OCR the MP4, prove its source identity,
retrieve URLs, certify their meanings or inspect every unsupported claim.
Historical status/audit documents intentionally retain earlier version labels.

```sh
# From videos/
uv run --locked python -m unittest test_package -v
uv run --locked python -m unittest test_video test_qa test_thumbnail test_small_screen test_package -v
```

Actual full run: **36 tests pass in 26.571 s**, including the existing 3,840
frame-fit checks across both synthetic scenarios. No dependency, lockfile,
license, renderer, caption, timing or source-registry change. Draft text changes
need editorial approval even when their numerical checks pass.

Next: obtain exact-version/tablet/pacing and audio-format decisions for v7;
then resolve the verified lesson destination and matching final CTA/description.
Absent feedback, the next bounded production task can be one source-checked
comparison storyboard for “Same-looking curves, different physics,” not another
cosmetic v7 revision or an unapproved public research claim. Publishing remains
blocked; no upload, merge, account change, purchase or automation was performed.
