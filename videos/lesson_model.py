"""Validated, exact synthetic timing model shared by captions and graphics."""
from fractions import Fraction
import json
import math
from pathlib import Path

SCENARIO_KEYS = {"baseline_ms", "fourier_ms", "kernel_speedup"}


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Timing parameters must be finite JSON numbers")
    if not math.isfinite(value):
        raise ValueError("Timing parameters must be finite JSON numbers")
    return Fraction(str(value))


def metrics(data):
    baseline, fourier, gain = (number(data[k]) for k in
                              ("baseline_ms", "fourier_ms", "kernel_speedup"))
    if not 0 < fourier < baseline or gain <= 1:
        raise ValueError("This lesson requires 0 < Fourier time < total and speedup > 1")
    other = baseline - fourier
    new_fourier = fourier / gain
    new_total = other + new_fourier
    return dict(baseline=baseline, fourier=fourier, other=other,
                kernel_gain=gain, new_fourier=new_fourier, new_total=new_total,
                saved=baseline-new_total, fraction=fourier/baseline,
                overall_gain=baseline/new_total, ceiling_gain=baseline/other)


def compact(value):
    return f"{float(value):.2f}".rstrip("0").rstrip(".")


def context(data):
    values = metrics(data)
    # Captions include exact sums. Refuse examples that would silently round
    # their millisecond operands before displaying an equals sign.
    for key in ("baseline", "fourier", "other", "new_fourier", "new_total", "saved", "kernel_gain"):
        if Fraction(compact(values[key])) != values[key]:
            raise ValueError("Displayed timings and kernel speedup must be exact to at most two decimals")
    result = {k: compact(v) for k, v in values.items()}
    for key in ("overall_gain", "ceiling_gain"):
        result[key] = f"{float(values[key]):.2f}"
    fraction = f"{float(values['fraction']):.2f}"
    result["fraction"] = fraction if Fraction(fraction) == values["fraction"] else str(values["fraction"])
    return result


def quotient(numerator, denominator):
    """Never put exact equality in front of a rounded quotient."""
    value = numerator / denominator
    rounded = f"{float(value):.2f}"
    relation = "=" if Fraction(rounded) == value else "≈"
    return f"{compact(numerator)} / {compact(denominator)} {relation} {rounded}×"


def load_lesson(path, scenario=None):
    data = json.loads(Path(path).read_text())
    if scenario is not None:
        patch = json.loads(Path(scenario).read_text())
        if not isinstance(patch, dict) or set(patch) != SCENARIO_KEYS:
            raise ValueError("A scenario must supply exactly the three timing parameters")
        data.update(patch)
    values = context(data)  # validate before formatting or drawing
    if (data["width"], data["height"]) != (1280, 720):
        raise ValueError("Renderer currently supports only the 1280×720 design canvas")
    if type(data["fps"]) is not int or data["fps"] <= 0:
        raise ValueError("fps must be a positive integer")
    if type(data["duration"]) is not int or not 60 <= data["duration"] <= 90:
        raise ValueError("Lesson must be 60–90 whole seconds")
    expected = 0
    for scene in data["scenes"]:
        if scene["start"] != expected or scene["end"] <= scene["start"]:
            raise ValueError("Scene timeline must be positive, ordered and contiguous")
        if not scene["captions"]:
            raise ValueError("Every scene needs captions")
        if "cards" in scene and len(scene["cards"]) != len(scene["captions"]):
            raise ValueError("Each question card needs exactly one caption")
        expected = scene["end"]
    if expected != data["duration"]:
        raise ValueError("Scenes must cover the full duration")

    def substitute(item):
        if isinstance(item, str):
            return item.format_map(values)
        if isinstance(item, list):
            return [substitute(v) for v in item]
        if isinstance(item, dict):
            return {k: substitute(v) for k, v in item.items()}
        return item
    return substitute(data)
