# Curves episode · draft publication package

**Review copy only. Not published, scheduled or approved.**
FFT/latency v7 remains the first release milestone. This later-candidate
package does not clear any video, mathematics, rights or publishing gate.

## Frozen candidate

- Candidate: `curves-legibility-v3` · 86 seconds · 24 fps · 2,064 frames · silent.
- MP4 SHA256: `f252ab6d34b79c8011c9a4bd71cb8547ceb42bd3797aa675e07e13325d65bc10`.
- Package repo baseline: `29a2a1256105d38f809b1f6475e5266dee7b5a4e` (not a new render).
- Render source baseline: `e30ea2a1c6e640c9de87aae2e833d4e47542b557`; actual source hashes are in [episode-render.json](episode-render.json).
- [Exact-version review](REVIEW.md) · [lesson and assumptions](EPISODE.md) · [structured copy](package.json).
- No public video or interactive-lesson destination has been verified. None is inserted below.

## Proposed public title

Same-looking curves, different physics

## Proposed public description

What defines this curve? This 86-second silent explainer separates images of points under w = z², contours of a chosen local 2D potential, and field lines of an ideal 3D magnetic dipole. Then only the camera turns.

The potential V = x² − y² is a modelling choice, not a claim that a mapped grid is a force field. The camera uses orthographic projection, not stereographic projection: depth is lost even though the field stays fixed.

Normalized educational models; the dipole source is excluded. No real grid telemetry, operational-readiness claim, proof of the Riemann hypothesis or Navier–Stokes regularity, or inference of shared physics. Original code-generated visuals and on-screen text; no audio.

Before comparing two plots, ask: what defines each curve?

Mathematical sources:

- [NIST DLMF §1.9](https://dlmf.nist.gov/1.9)
- [MIT, Electromagnetic Fields and Energy §4.1](https://web.mit.edu/6.013_book/www/chapter4/4.1.html)
- [NASA CCMC, Properties of Magnetic Dipoles](https://ccmc.gsfc.nasa.gov/static/files/Dipole.pdf)

Conceptual inspiration (no borrowed footage, artwork or narration; not theorem validation):

- [3Blue1Brown: zeta lesson](https://www.3blue1brown.com/lessons/zeta/)
- [3Blue1Brown: quaternions lesson page](https://www.3blue1brown.com/lessons/quaternions/)

## Internal source-role ledger — not additional public copy

Primary sources rechecked 2026-11-07 UTC. No clips or transcript offsets are used.

- **NIST DLMF §1.9:** Analytic real and imaginary parts are harmonic (Eq. 1.9.26). Our z² map is derived directly; this source does not identify a mapped grid as a physical field.
- **MIT, Electromagnetic Fields and Energy §4.1:** E = −grad V and the distinction between potential contours and field lines. Our polynomial potential is a chosen local normalized model, not an engineered boundary-value solution.
- **NASA CCMC, Properties of Magnetic Dipoles:** Cartesian dipole components, Eqs. (7)–(9), and r = L sin²θ, Eq. (15), printed pages 2 and 4. Source excluded; not the interior of a real magnet.
- **3Blue1Brown: zeta lesson:** Conceptual inspiration only; no footage, artwork or narration reused; not theorem validation.
- **3Blue1Brown: quaternions lesson page:** Conceptual inspiration only; no footage, artwork or narration reused; not theorem validation. No unseen transcript content is inferred.

## Place in the concept/application graph

| Connection | What is and is not claimed |
|---|---|
| Analytic map → harmonic real part | Mathematical relation; does not assign physical meaning automatically |
| Chosen potential → gradient → field lines | Modelling choice plus definitions; contours and field lines are different objects |
| 3D dipole → orthographic camera | Representation loses depth; rotating the camera does not change the field |
| Reading engineering field plots | Transferable interpretation habit, not a validated operational tool or speedup |

## Timestamped reviewer prompts

These are editorial prompts, not new proofs or completed checks. Reply on [draft PR #3](https://github.com/jeunjetta/math-in-context-/pull/3).

- At 12–22 s, can you distinguish the input x,y plane from the output u,v plane and read the matching-point equation? The sweep is a parameter, not physical time.
- At 22–38 s, is the return to the original domain and choice of potential explicit? Are dashed regular potential contours distinct from solid directed field lines, with no field direction claimed at E = 0?
- At 38–48 s, can you read the +z orientation, source exclusion and normalized-model labels on an actual tablet? The long formula still needs device feedback.
- At 48–70 s, do the labelled cut, lost depth and camera-only turn make sense? The field and underlying 3D curves do not change or collapse.
- At 70–86 s, can you answer the definition question before the answer appears and read the source card? Report timestamp, device and any text that needs more time.

## Unchanged release gates

- [ ] Actual-device full playback and reading pace for this exact media hash.
- [ ] Independent mathematical and editorial review of the model choices and equations.
- [ ] Audio decision; this candidate has no audio and no audio-sync claim.
- [ ] Rights/provenance review, parent-branch reconciliation and exact-version publication approval.
- [ ] Verify real public destinations before adding any video/lesson call to action.

No automatic chapters, uploads, platform settings or scheduled posts are created.
Review prompts use episode times, not a promise of platform chapter support.

## Reproduce the copy check

From `videos/` (Python standard library only):

```sh
python curves_package.py --check
python curves_package.py --stdout
python -m unittest test_curves_package -v
```

Edit package.json, inspect --stdout, update this generated Markdown and run --check.
Identity/hash guards detect narrow drift, not correctness, readability, rights or approval.
Any media/lesson change requires a newly reviewed package; do not transfer approval by filename.
