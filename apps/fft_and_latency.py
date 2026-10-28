# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo==0.25.2"]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A faster FFT is not automatically a faster control room

    **5-minute experiment · synthetic numbers · no live grid connection**

    A Fourier transform separates a signal into frequency components. An FFT
    computes the discrete transform efficiently. But accelerating one step
    does not accelerate everything around it.

    **Predict:** a 100 ms pipeline spends 20 ms in Fourier computation.
    If that step becomes twice as fast, does the whole pipeline become 2× faster?
    """)
    return


@app.cell
def _(mo):
    fraction = mo.ui.slider(0, 100, value=20, step=1, label="FFT share of baseline runtime (%)")
    kernel_gain = mo.ui.slider(1, 20, value=2, step=1, label="FFT speedup factor")
    baseline = mo.ui.slider(10, 1000, value=100, step=10, label="Baseline total (ms)")
    mo.vstack([fraction, kernel_gain, baseline])
    return baseline, fraction, kernel_gain


@app.cell(hide_code=True)
def _(baseline, fraction, kernel_gain, mo):
    f = fraction.value / 100
    s = kernel_gain.value
    remaining = (1 - f) + f / s
    total = baseline.value * remaining
    gain = 1 / remaining
    ceiling = "unbounded in this toy model" if f == 1 else f"{1/(1-f):.2f}×"
    mo.md(f"""
    ## Your result

    **{total:.1f} ms total · {gain:.2f}× overall speedup**

    Other work: **{baseline.value*(1-f):.1f} ms**.
    Fourier work after improvement: **{baseline.value*f/s:.1f} ms**.

    Even an infinitely fast Fourier step has a speedup ceiling of **{ceiling}**.

    $$S = \\frac{{1}}{{(1-f)+f/s}}.$$

    Here $f$ is the fraction improved; $s$ is that step's speedup.
    Assumptions: sequential work, unchanged accuracy and no extra overhead.
    Real parallel pipelines can behave differently.
    """)
    return


@app.cell
def _(mo):
    answer = mo.ui.radio(
        ["2×", "About 1.11×", "1.5×"],
        label="For the ORIGINAL 20% share and 2× FFT improvement, what is the total speedup?",
    )
    mo.vstack([mo.md("## Check your prediction"), answer])
    return (answer,)


@app.cell(hide_code=True)
def _(answer, mo):
    feedback = (
        "Choose an answer to reveal feedback."
        if answer.value is None
        else "Correct: 1/(0.8+0.2/2) = 1/0.9, about 1.11×."
        if answer.value == "About 1.11×"
        else "Try again: only the 20 ms step is halved; the other 80 ms remains."
    )
    mo.md(feedback)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## What this tells us—and what it does not

    PMUs report time-aligned estimates including magnitude, phase, frequency
    and rate of change of frequency, not every raw-waveform detail.
    [NIST's dynamic PMU work](https://www.nist.gov/publications/dynamic-phasor-measurement-unit-test-system)
    gives historical measurement context, not current compliance requirements.

    **Engineering question:** which step limits the workload, and what happens
    to numerical error, alignment, communication and worst-case latency?

    A theorem about exact arithmetic is not automatically a stable float64
    implementation. This does not validate a new FFT, promise real-time EMT,
    or advise an operational change.

    **Explore next:** [3Blue1Brown's Fourier explanation](https://www.3blue1brown.com/lessons/fourier-transforms/).
    This exercise is original; the linked lesson is inspiration.
    """)
    return


if __name__ == "__main__":
    app.run()
