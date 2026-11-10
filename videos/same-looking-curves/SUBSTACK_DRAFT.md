# Companion writing handoff · curves episode

**9 November 2026 · unpublished editorial draft, not approved.**
Video remains the primary format; this is optional supporting reading for
the frozen 86-second silent legibility-v3 candidate, not a new episode.
Source baseline: `1358a273285983ae7a610f2b45b22839591a380e`.
Exact identity and absent public destinations: [companion.json](companion.json).
[Video review](REVIEW.md) · [proposed description](PACKAGE.md) ·
[original cover option and alt text](THUMBNAIL.md).

Only the text between the markers below is proposed article copy.
No Substack API action, scheduled post or account setting is involved.

<!-- PUBLIC_DRAFT_BEGIN -->

# Same-looking curves, different physics

Three definitions that change how you read a plot.

A curved line is not yet an explanation. Before comparing two pictures,
ask what rule produced each line. That question separates three objects
which are easy to confuse: images of points, contours of a scalar function,
and curves that follow a vector field.

## 1. Mapping points does not introduce a force

Write z=x+iy and apply w=z². The output coordinates are
u=x²−y² and v=2xy. Points on the input line x=1 therefore land on
u=1−v²/4: a parabola in the output u,v plane. For example,
z=1+i maps to w=2i, the output point (0,2).

We have moved mathematical points between coordinate planes. No forces
have been introduced. Sweeping a dot along the input line is a parameter
change, not a simulation of something moving through physical time.

## 2. A contour and a field line answer different questions

Return to the original x,y plane. Now choose V=x²−y² as a local,
normalized electric-potential model. Its Laplacian is 2−2=0. This is a
useful harmonic example, but choosing it as a potential is a modelling
decision—not a consequence of drawing the mapped parabola. No real
electrode boundary problem has been solved.

A potential contour keeps V constant. The associated field is
E=−grad V=(-2x,2y). A field line instead has its tangent parallel to E
where E is nonzero. Here its non-axis branches satisfy xy=constant.

Pause and predict: if you follow the direction of E, does V stay constant?

No. Along a parametrization with derivative E, the change is
grad V · E = −|grad V|². Away from the origin this is negative.
Field lines cross regular potential contours normally rather than tracing
them. At the origin E=0, so there is no field direction to assign there.

## 3. A projection changes the view, not the field

Switch to a different model: a normalized ideal magnetic dipole directed
along +z. Its field lines live in three dimensions. Exclude the singular
source; this is not a model inside a real bar magnet.

Looking along y drops that coordinate. Two of the episode's fixed curves
then overlap in their x,z outlines despite having different depths.
Turning only the camera separates their projections without changing the
field or the underlying curves. This is orthographic, not stereographic,
projection. A curve appearing edge-on has not physically collapsed.

## A habit worth carrying into engineering

Before interpreting a plotted arc, check its defining equation, coordinate
plane, units and whether it is a section or a projection. A scalar contour
does not become a trajectory because its shape resembles one. This is an
interpretation habit, not a validated operational tool or a grid-readiness
claim. All examples here are normalized models, not real grid telemetry.

The useful connection is explicit: analytic map → harmonic real part →
chosen potential → gradient field. A separate connection, 3D field →
camera image, loses depth. A modelling choice and a representation step
are not the same kind of link.

Resemblance can suggest a question. Definitions and equations decide what
has actually been established. No proof of the Riemann hypothesis,
Navier–Stokes regularity or shared underlying physics is claimed here.

### Sources and inspiration

- [NIST DLMF §1.9](https://dlmf.nist.gov/1.9): harmonic real and imaginary
  parts of analytic functions, Eq. 1.9.26; the polynomial example is derived above.
- [MIT, Electromagnetic Fields and Energy §4.1](https://web.mit.edu/6.013_book/www/chapter4/4.1.html): potential, negative gradient and field lines.
- [NASA CCMC, Properties of Magnetic Dipoles](https://ccmc.gsfc.nasa.gov/static/files/Dipole.pdf): ideal dipole components and field-line geometry, Eqs. (7)–(9), (15).
- Conceptual inspiration: 3Blue1Brown's [zeta](https://www.3blue1brown.com/lessons/zeta/)
  and [quaternions lesson pages](https://www.3blue1brown.com/lessons/quaternions/).
  No creator footage, artwork or narration is reused; inspiration is not theorem validation.

<!-- PUBLIC_DRAFT_END -->

## Internal editorial checks — not article copy

Primary sources rechecked 9 November 2026. No quotes, clips or transcript
timestamps used. Reuses only public educational definitions and the existing
episode; no private research manuscript, notebook export or operator data.

There is no verified public video or curves lesson destination. Add neither
a guessed URL nor a “watch now” button. This draft has no image/embed:
the original cover option is separate and unselected. If later selected,
upload the approved asset and alt text manually; check the actual Substack
preview. No assumption that arbitrary iframes or LaTeX will render there.
Equations use readable plain text, not an untested publishing integration.

- [ ] Karin/editor reviews voice, length, modelling caveats and usefulness.
- [ ] Independent mathematical/editorial and rights review.
- [ ] Confirm candidate/lesson still match the companion identity.
- [ ] Check mobile layout and equations in an actual Substack draft preview.
- [ ] Resolve cover, audio and video/lesson destinations separately.
- [ ] Explicit approval for exact final copy/media and publishing destination.

Tests in test_curves_companion.py check narrow identity/source/link guards
and exact polynomial/gradient arithmetic; they do not approve the prose,
certify comprehension, validate a real physical model or prove research.
The full run, files, limitations and next action are in [STATUS.md](../STATUS.md).
