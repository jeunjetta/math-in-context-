# What if the faster step adds overhead?

23 November 2026. **Optional draft after-video exercise; not approved for publication.**

Watch the existing 80-second FFT/latency pilot first if available. This text also stands alone; it is not another movie, a live app or a required review step.

## Predict before scrolling to the answer

The synthetic baseline is 100 ms: 20 ms of Fourier work and 80 ms of other work. The Fourier step becomes 2 times as fast.

Now add **8 ms of new overhead**. What is the new end-to-end time? Choose 90 ms, 98 ms, 108 ms.

How much new overhead would exactly erase the time saving?

Change only the no-added-overhead assumption. Work is still sequential; other work and accuracy remain unchanged. Additional sequential time on the improved path only; not a cost already included in the original other work.

## Answer and feedback

**98 ms**: 10 + 80 + 8 = 98 ms.

Choosing 90 ms omits the new overhead. Choosing 108 ms adds overhead but forgets to halve the Fourier step.

The Fourier change saves 10 ms before overhead. Exactly **10 ms of new overhead** consumes that saving. Less gives a net time reduction; more makes this toy workload slower.

| New overhead | New total | Old time / new time | Net result versus baseline |
|---:|---:|---:|---|
| 0 ms | 90 ms | 100 / 90 ≈ 1.11× | faster |
| 8 ms | 98 ms | 100 / 98 ≈ 1.02× | faster |
| 10 ms | 100 ms | 100 / 100 = 1.00× | break-even |
| 12 ms | 102 ms | 100 / 102 ≈ 0.98× | slower |

For fixed extra overhead h, the accounting is T_new = T_old - F + F/s + h. Here F is the original Fourier time and s its speedup. Net improvement requires h < F(1 - 1/s); equality is break-even. All times use the same units. We do not assume overhead stays fixed as input size or s changes.

This is reproduced arithmetic, not benchmark evidence. A speedup factor below one means slower, not a negative runtime. Overlapped or parallel work needs a critical-path model instead of this sequential sum. Same accuracy is assumed, not demonstrated.

Concept placement: Fourier computation → component time saving → overhead budget → end-to-end latency. These are method/application links, not equivalences. The calculation establishes neither arithmetic-complexity improvement, numerical stability nor validated real-time grid readiness. No operational recommendation.

## Sources and reuse

- [Original synthetic notebook source](https://github.com/jeunjetta/math-in-context-/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/apps/fft_and_latency.py): baseline and assumptions; source code, not a deployed lesson.
- [FFTW authors’ accuracy context](https://fftw.org/accuracy/comments.html): separate implementation-error question, not support for these hypothetical times.

No external text, imagery, voice or footage is copied. No learner responses are collected. This is not a validated assessment, accessibility certification or evidence that anyone understood the film.

## Producer notes — not extra movie content

Reference movie SHA-256: `790584a85d73529c882106a0202a26fbdd512018433441d8088f5ad069dbeb5e`. Source baseline: `e880ac860d5240f513e40648355507640a909885`. Movie, captions, description/package and existing notebook stay unchanged. This exercise is not inserted into the film or a publication package.

Edit `overhead-check.json`; the small standard-library generator separates exercise data from Markdown. From `videos/`, run `python3 overhead_check.py` to regenerate, `python3 overhead_check.py --check` to detect drift, and `python3 -m unittest test_overhead_check -v` to test. `evaluate(model, overhead_ms)` returns exact fractions for reuse in a future Marimo cell; no Marimo app/export or deployment was created or tested.

Python [Fraction documentation](https://docs.python.org/3/library/fractions.html) and FFTW context checked 23 November 2026. Existing dependency/renderer licensing is unchanged; no new commercial-use clearance is claimed. Next: editorial review of this check alongside the existing intended-device review, then adopt or discard it separately. All video release gates remain open.
