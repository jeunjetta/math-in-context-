# Same-looking curves, different physics

**Preproduction draft · 5 November 2026 · not approved or rendered.**
One idea: identify the mathematical object before comparing its shape.
Audience: university-level maths basics, engineers and curious builders.
This is a later candidate, not a replacement for the FFT/latency pilot.

Source baseline: `97c8aea386535f8eca8ffd00478f36b56adc364e` on draft PR #2.
Work branch: `codex/video-curves-storyboard`, stacked on
`codex/video-fft-latency` so the later candidate does not alter PR #2.
The complete proposed spoken script, scene times, labels and visual directions
are editable in [script.json](script.json). It is **unrecorded narration**,
not a fabricated voiceover or an audio-aligned caption track. There is no new
MP4, VTT, image export, human playback review or actual-device test.

## 82-second cut

157 whitespace-delimited words. Provisional scene durations are reading-budget
checks, not measured narration timings. If an authorized human records it,
listen and retime before producing final captions. No voice or music selected.

| Time | Spoken idea | Original visual and required distinction |
|---|---|---|
| 0–8 s | What does each curve represent? | Three labeled previews, never an equivalence-implying morph |
| 8–22 s | A grid line is mapped into another plane, not turned into a force | Separate input x,y and output u,v panels; highlight x=1 under w=z² |
| 22–38 s | The real part can serve as a local potential; contours differ from field lines | Return explicitly to domain x,y; dashed equipotentials, solid field lines, direction arrows |
| 38–56 s | An ideal dipole supplies actual field-line geometry in three dimensions | z-aligned normalized dipole, 3D axes, two azimuthal planes; masked source |
| 56–70 s | A camera can hide depth without changing the field | Two curves overlap looking along y; rotate only the camera, then see separation |
| 70–82 s | Check definitions, dimensions and equations before resemblance | Three object definitions, primary source card, prediction question |

Closing prediction: **Which of the three objects is defined by a tangent
parallel to its field?** Answer: the field line. A potential contour is normal
to its nonzero gradient; a mapped grid line is defined by a point map.
This question is preproduction copy, not a hosted interactive quiz.

## Mathematical and visual specification

### 1. Image of a grid line — output plane

Choose F(z)=z², z=x+iy, w=u+iv. Then u=x²−y² and v=2xy.
The input line x=1 maps to u=1−v²/4, a parabola in the **u,v plane**.
It is not a field line or an equipotential merely because it is curved.
Label both planes persistently; do not reuse x,y labels for output coordinates.
F is two-to-one globally, and F'(0)=0: mark the origin as a critical point,
not an example of angle preservation. No zeta function is plotted in this bite.

### 2. Potential and field — input/domain plane

There is a real mathematical bridge, not only a visual analogy:
Re F=x²−y² is harmonic, with Laplacian 2−2=0. Choose the **local normalized
2D electrostatic model** V=Re F and E=−grad V=(−2x,2y). This choice is a
modeling assumption; no global electrode boundary problem is being solved.
Potential contours V=c are hyperbolas (degenerate at c=0), while E's
non-axis field-line branches satisfy xy=constant. In particular,
E·grad(xy)=0 and E is perpendicular to a regular V-contour, away from (0,0).
The origin has E=0 and no defined field direction. Distinguish domain contours
from the previous image of a grid, even though the same polynomial appears.

Suggested finite plotting window: x,y in [-2,2], with nonzero V levels
{-1,-0.5,0.5,1} and xy levels {-0.75,-0.25,0.25,0.75}. Use separate legends
and dash styles, not color alone. Arrows show direction; do not imply their
uniform length or chosen curve density measures field strength.

### 3. Ideal 3D magnetic dipole — source excluded

Use positive normalized M=1, moment along +z, with r²=x²+y²+z²:
B=(3xz,3yz,3z²−r²)/r⁵ for r>0. These are normalized geometry, not SI
measurements, operator telemetry or a model inside a real bar magnet.
Dipole lines have r=L sin²(theta), fixed azimuth phi, where theta is
colatitude from +z and L is the equatorial crossing radius. This field-line
formula is not an equipotential equation. The model is singular at r=0.

Use L=1 and phi=±pi/3 for the two main curves. For a future render, exclude
a sphere r<0.15: split/mask each polyline there, never join its endpoints
through the source or close a line across the gap. The math helper excludes
the poles but does not implement the renderer's source mask; that is remaining
work. The mathematical tangent check includes the equator, avoiding division
by a radial component that vanishes there.

### 4. Camera projection — not new physics

The first orthographic camera uses screen coordinates (x,z), dropping y.
The two fixed-phi curves above have equal x,z but opposite, nonzero y, so
their projected paths overlap. At camera azimuth alpha=pi/6, use screen
coordinates (x cos alpha+y sin alpha,z); they separate. All physical points
and B remain fixed. Keep an orientation triad and “depth lost / projected
shape and angles can distort” label visible. A meridional section is a chosen
plane through the axis, not the projection of every 3D line.

This camera operation is **not stereographic projection**. Stereographic
projection of a sphere and quaternion visualization are later subjects;
do not silently substitute their angle properties for this ordinary camera.

## Place in the concept/application graph

| Connection | Type and limit |
|---|---|
| Analytic function → harmonic real/imaginary parts | Established mathematical relation |
| Harmonic real part → chosen local 2D potential | Modeling construction, not automatic physical identity |
| Potential → gradient field → field lines | Distinct objects linked by differential equations |
| 3D dipole → camera view | Representation with lost depth, not a changed field |
| Zeta-grid inspiration → these comparisons | Motivation only; no claim about zeros, RH or shared physics |

No private NS checkpoint, proof-of-RH claim, common-physics hypothesis or
simulation-of-reality claim is used. Resemblance can motivate a question;
the definitions and equations decide what has actually been established.

## Primary source and inspiration ledger

All below retrieved 5 November 2026; no source imagery, footage, narration or
distinctive creator assets copied. Equations are implemented in original code.

- [NIST DLMF §1.9](https://dlmf.nist.gov/1.9), especially harmonic functions
  §1.9(ii), Eq. 1.9.26, and conformal transformation §1.9(iv): analytic real
  and imaginary parts are harmonic; local angle preservation requires a
  nonzero derivative. Our polynomial example is derived directly above.
- [MIT Electromagnetic Fields and Energy, §4.1](https://web.mit.edu/6.013_book/www/chapter4/4.1.html): E is the negative potential gradient; distinguishes equipotentials, field lines and 2D views. Our normalized polynomial is a chosen local model, not copied artwork or a claimed engineered boundary solution.
- [NASA CCMC, Properties of Magnetic Dipoles](https://ccmc.gsfc.nasa.gov/static/files/Dipole.pdf), pp. 2 and 4, Eqs. (7)–(9) and (15): Cartesian dipole components and r=L sin²(theta). M is a normalized coefficient here, not a charged-particle magnetic moment or real Earth model. Illustrations are not reused.
- [3Blue1Brown zeta lesson](https://www.3blue1brown.com/lessons/zeta/)
  and [quaternions/stereographic lesson page](https://www.3blue1brown.com/lessons/quaternions/): credited conceptual inspiration only. The latter retrieved page is sparse; no unseen transcript or detailed video content is inferred. No clips mean no episode/transcript timestamp-offset assumption.

## Validation and next concrete deliverable

`curves_models.py` separates small geometry functions from script data and any
future renderer. `test_curves.py` has five tests: exact rational polynomial
and gradient checks; 30 floating-point dipole tangent samples (tolerance
1e-12, diagnostic not proof); two-camera depth overlap/separation; singular
input guards; and contiguous 82-second script with a provisional <=3 words/s
budget per scene. These do not prove caption readability or validate a render.

Actual validation: five focused tests pass; the full video suite passes
**41 tests in 46.050 s**, including existing pilot layout/arithmetic/QA guards.
The script contains 157 words; all six proposed scenes stay within the
provisional word budget. Whitespace check passes. These are code and script
checks, not narration synchronization, visual QA or mathematical peer review.

```sh
# From videos/, existing locked environment; no new dependency
uv run --locked python -m unittest test_curves -v
```

Next bounded increment: produce two original code-drawn keyframes (mapping
versus potential, and the two-camera dipole comparison), including the source
mask and persistent coordinate labels. Inspect at full size and tablet-sized
rasters before attempting an animatic. Use existing tools if suitable; recheck
official docs/licensing before choosing any new renderer or distributing assets.

Open work is production, not a technical inability to render: no keyframes,
layout/contrast checks, captions, audio or full render yet. Human mathematical,
editorial and eventual exact-version publication approval are still required.
The v7 FFT pilot remains the first release milestone with its existing gates;
this small preproduction task clears none of them.
