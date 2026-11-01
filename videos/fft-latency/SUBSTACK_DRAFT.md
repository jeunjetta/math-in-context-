# FFT/latency companion · DRAFT FOR KARIN'S REVIEW

**NOT APPROVED FOR PUBLICATION.** Prepared 1 November 2026 against video
source baseline `d911032ab6edccde549cb07a4c5a7202d0c94594` and the same
synthetic lesson. No post has been created or published on Substack.

The marked article below is the proposed reader-facing copy. Editorial notes
after it are not part of the post. Links are intentionally unresolved until
the video and interactive lesson have separately cleared their release gates.

<!-- BEGIN ARTICLE -->
# A faster FFT is not automatically a faster system

*A small prediction about a big engineering habit: measure the whole journey.*

Suppose the Fourier computation in a software pipeline becomes twice as fast.
Does the entire pipeline become twice as fast?

Make a prediction before reading on. The key question is not only how much
faster the computation becomes, but how much of the original workload it took.

An FFT computes a discrete Fourier transform efficiently. It can be an
important stage in signal processing, but it is still a stage—not the whole
process of moving data, computing a result and delivering it.

## Follow the time

Here is an invented, sequential example. These are not benchmark measurements,
sampling intervals or operational deadlines. Assume unchanged accuracy,
unchanged other work and no added overhead.

<!-- BEGIN MODEL CHECKED EXAMPLE -->
| Work | Before | After |
|---|---:|---:|
| Fourier computation | 20 ms | 10 ms |
| Other work | 80 ms | 80 ms |
| End-to-end total | 100 ms | 90 ms |

Halving the Fourier step saves **10 ms**, or **10% less elapsed time**.
Overall speedup is **100 / 90 ≈ 1.11×**, not **2×**.

Even zero Fourier time would leave **80 ms** of other work.
The maximum overall speedup in this model is **100 / 80 = 1.25×**.
<!-- END MODEL CHECKED EXAMPLE -->

The unchanged work sets the ceiling. This is not a reason to dismiss a faster
FFT; it tells us what that improvement can and cannot do for this workload.

More generally, let `f` be the improved step's fraction of baseline time and
`s` its speedup. The remaining time fraction is `(1-f)+f/s`; overall speedup
is its reciprocal. With overlapping or parallel stages, we need a model of
the critical path rather than blindly adding every stage's runtime.

## Four claims worth keeping separate

| Question | What it asks |
|---|---|
| Arithmetic complexity | How do operation counts grow as input size increases? |
| Numerical stability | How does the algorithm behave in the presence of computation errors? |
| End-to-end latency | How long does the whole workload take? |
| Real-time readiness | Has the complete system been validated against its deadlines and requirements? |

Fewer operations do not by themselves prove lower elapsed time on a particular
machine. Lower latency does not by itself prove numerical reliability.
Neither establishes readiness for a control room. FFTW's authors discuss
implementation-dependent floating-point behavior in their accuracy notes below;
that is a separate question from our invented runtime accounting.

For engineers and builders, a useful next question in a test environment is:
**which part of the complete workload actually limits the result?** Measure
the whole path as well as the component, while checking accuracy and overhead.
This example establishes no new FFT algorithm, AI mathematics breakthrough,
real-time grid capability or operational recommendation.

## Take the next small step

Watch the companion video: **[ADD_APPROVED_VIDEO_URL_BEFORE_PUBLICATION]**.

Try the interactive lesson: **[ADD_VERIFIED_LESSON_URL_BEFORE_PUBLICATION]**.
Change the improved fraction while holding its speedup fixed. Predict the
direction of the total-time change, then check it. Which is more valuable
in your chosen example: a faster step, or a larger fraction worth improving?
These sliders compare hypothetical workloads; a larger fraction is not an
instruction to add computation to a real pipeline.

In our concept map, this bite sits along **Fourier decomposition → FFT
algorithms → a pipeline component → end-to-end latency**. These are method
and application links, not mathematical equivalences or proof of readiness.

### Sources and further exploration

- Our [worked example and Python source](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py): the synthetic calculation and its assumptions. This commit link is source code, not the hosted exercise.
- [FFTW authors' accuracy notes](https://fftw.org/accuracy/comments.html): primary implementation/accuracy context, not evidence for the timing numbers above.
- [3Blue1Brown's Fourier explanation](https://www.3blue1brown.com/lessons/fourier-transforms/): credited inspiration and a deeper visual explanation. No footage, audio, screenshots or distinctive assets have been reused.
<!-- END ARTICLE -->

## Editorial handoff — not reader-facing copy

The post supports the existing v5 video, not a separate lesson or an update
about newly solved mathematics. Its numerical block is regression-checked
against `lesson_model.py` and canonical `lesson.json`. If that model changes,
review the entire post, not just its checked block. No automatic post generator,
new dependency, footage, narration or mathematical research claim was added.

Video review version: 80 seconds, silent, SHA256
`d2a0365545602c55af3ee6018944045a5804a125b0dd5af80d7585c85efe12d4`.
See [REVIEW.md](REVIEW.md) for script/approval gates and
[LESSON_LINK.md](LESSON_LINK.md) for the dated deployment audit. Do not infer a
live lesson address or Open Notebook deployment. Source URLs were retrieved
on 1 November 2026; no direct quotes or podcast clips are used.

Suggested illustration, only after review: an original encoded before/after
bar frame from the matching video export. Alt text should convey the whole
comparison: Fourier work halves, other work stays fixed, and total time falls
from 100 ms to 90 ms. Do not substitute a borrowed creator screenshot.

- [ ] Karin approves wording, mathematical scope and the exact article revision.
- [ ] Video has its separate human/tablet, audio-format and publication approval.
- [ ] Replace the video placeholder with the approved published destination.
- [ ] Replace the lesson placeholder with the verified usable exercise URL.
- [ ] Preview the table, formula, symbols, image/alt text and links on a tablet.
- [ ] Confirm source/asset credits and obtain explicit permission to publish this post.

Use a direct lesson link; arbitrary iframe or equation rendering in Substack
is not assumed. The plain-text formula works without a mathematical widget.
Do not paste these editorial notes or unresolved placeholders into a release.
