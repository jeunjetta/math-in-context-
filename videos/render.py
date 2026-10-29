"""Original data-driven silent animatic. Pillow frames -> local FFmpeg.

No downloaded images, audio, browser, model API or network calls during render.
All coordinates use a 1280 x 720 design canvas. Text refuses to clip silently.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont
from lesson_model import compact, context, load_lesson, metrics, quotient

ROOT = Path(__file__).resolve().parent
LESSON = load_lesson(ROOT / "fft-latency/lesson.json")
BG, FG, MUTED = "#101c2c", "#f4f7fc", "#b5c4d7"
CYAN, AMBER, PANEL = "#63e0d0", "#ffc273", "#203249"


@lru_cache
def font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(name, size)


@lru_cache(maxsize=4096)
def measure(value, size, bold):
    return font(size, bold).getlength(value)


def text(draw, box, value, size=30, fill=FG, bold=False, center=False):
    """Wrap by actual glyph measurements and fail on overflow."""
    x, y, width, height = box
    face = font(size, bold)
    lines = []
    for paragraph in value.split("\n"):
        line = ""
        for word in paragraph.split():
            candidate = f"{line} {word}".strip()
            if measure(candidate, size, bold) > width:
                if not line:
                    raise ValueError(f"Word too wide: {word}")
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    line_height = size * 1.35
    if len(lines) * line_height > height:
        raise ValueError(f"Text clips: {value}")
    for i, line in enumerate(lines):
        dx = (width - measure(line, size, bold)) / 2 if center else 0
        draw.text((x + dx, y + i * line_height), line, font=face, fill=fill)


def smooth(t):
    t = max(0, min(1, t))
    return t * t * (3 - 2 * t)


def scene_at(t, data=LESSON):
    if not 0 <= t < data["duration"]:
        raise ValueError("Frame outside lesson")
    return next(s for s in data["scenes"] if s["start"] <= t < s["end"])


def caption_cues(data=LESSON):
    cues = []
    for s in data["scenes"]:
        step = (s["end"] - s["start"]) / len(s["captions"])
        for i, caption in enumerate(s["captions"]):
            cues.append((s["start"] + i * step, s["start"] + (i + 1) * step, caption))
    return cues


def cue_at(t, data=LESSON):
    """One timing source for burned captions, VTT and visual attention cues.

    Intervals are half-open: a cut belongs to its incoming cue, never both.
    """
    s = scene_at(t, data)
    step = (s["end"] - s["start"]) / len(s["captions"])
    # Match the same explicit boundaries used by caption_cues, avoiding a
    # floating-point floor at fractional boundaries such as 65.5 seconds.
    index = next(i for i in range(len(s["captions"]))
                 if s["start"] + i*step <= t < s["start"] + (i+1)*step)
    return index, s["captions"][index]


def bar(draw, y, fourier, label, data=LESSON):
    other = data["baseline_ms"] - data["fourier_ms"]
    x, scale, h = 96, 850 / data["baseline_ms"], 72
    draw.rounded_rectangle((x, y, x + 850, y + h), radius=8, fill=PANEL)
    fw = fourier * scale
    if fw > 0:
        draw.rectangle((x, y, x + fw, y + h), fill=CYAN)
    draw.rectangle((x + fw, y, x + fw + other * scale, y + h), fill=AMBER)
    text(draw, (x, y - 43, 850, 42), label, 25, MUTED)
    label_text = f"{compact(fourier + other)} ms"
    label_size = 34 if measure(label_text, 34, True) <= 200 else 28
    text(draw, (990, y + 13, 200, 50), label_text, label_size, bold=True)


def render_frame(t, data=LESSON):
    s = scene_at(t, data)
    image = Image.new("RGB", (data["width"], data["height"]), BG)
    d = ImageDraw.Draw(image)
    text(d, (64, 28, 900, 35), s["eyebrow"], 20, CYAN, True)
    text(d, (1030, 28, 190, 35), "VISUAL DRAFT", 18, MUTED)
    text(d, (64, 90, 1152, 145), s["heading"], 44, bold=True)
    sid = s["id"]
    baseline, fourier, gain = data["baseline_ms"], data["fourier_ms"], data["kernel_speedup"]
    other = baseline - fourier
    values = metrics(data)
    labels = context(data)
    if sid == "hook":
        text(d, (80, 260, 1120, 115), f"{labels['kernel_gain']}× faster FFT. How much faster overall?", 46, CYAN, True, True)
        text(d, (80, 410, 1120, 65), "Predict first. Then follow the time.", 32, MUTED, center=True)
    elif sid in {"baseline", "halve"}:
        text(d, (96, 208, 500, 30), "TEAL: FOURIER COMPUTATION", 18, CYAN)
        text(d, (620, 208, 580, 30), "AMBER: OTHER WORK", 18, AMBER)
        bar(d, 282, fourier, "BEFORE", data)
        if sid == "halve":
            remaining = fourier * (1 - (1 - 1 / gain) * smooth((t - s["start"]) / 3))
            bar(d, 427, remaining, "AFTER · same time scale", data)
        else:
            text(d, (96, 400, 1050, 70), f"Fourier: {fourier:g} ms       Other work: {other:g} ms", 32)
        text(d, (96, 524, 1050, 38), "Sequential · same accuracy · no added overhead", 23, MUTED)
    elif sid == "formula":
        text(d, (80, 250, 1120, 100), quotient(values["baseline"], values["new_total"]), 68, CYAN, True, True)
        text(d, (80, 370, 1120, 75), "S = 1 / [(1 − f) + f/s]", 42, center=True)
        text(d, (80, 460, 1120, 85), f"f = {labels['fraction']} of baseline time\ns = {labels['kernel_gain']} kernel speedup", 26, MUTED, center=True)
    elif sid == "ceiling":
        remaining = (fourier / gain) * (1 - smooth((t-s["start"]) / 3))
        bar(d, 290, remaining, "IDEAL LIMIT · Fourier time tends to zero", data)
        text(d, (80, 420, 1120, 100), quotient(values["baseline"], values["other"])+" maximum", 48, CYAN, True, True)
    elif sid == "distinctions":
        active, _ = cue_at(t, data)
        for i, card in enumerate(s["cards"]):
            x, y = 64 + (i % 2) * 588, 242 + (i // 2) * 147
            selected = i == active
            d.rounded_rectangle((x, y, x+560, y+130), 12, fill=PANEL,
                                outline=CYAN if selected else PANEL, width=3)
            text(d, (x+22, y+12, 516, 44), card["title"], 30,
                 CYAN if selected else MUTED, True)
            text(d, (x+22, y+62, 516, 60), card["description"], 24,
                 FG if selected else MUTED)
        text(d, (64, 537, 1152, 34), f"FOCUS {active+1}/4 · {s['cards'][active]['title']}",
             20, CYAN)
    elif sid == "readiness":
        for i, line in enumerate(["Accuracy and numerical error", "Data movement and alignment", "Worst-case deadlines and validation"]):
            text(d, (96, 250 + 85*i, 1080, 65), f"0{i+1}   {line}", 32, CYAN if i == 0 else FG)
        text(d, (96, 512, 1080, 44), "Synthetic arithmetic. Not operational evidence.", 25, AMBER)
    else:
        text(d, (80, 242, 1120, 62), "Fourier methods  →  FFT algorithms  →  latency", 32, CYAN, True, True)
        text(d, (80, 325, 1120, 65), "Try: apps/fft_and_latency.py  ·  pilot PR #1", 27, center=True)
        text(d, (80, 404, 1120, 90), "Sources: FFTW accuracy notes · linked Marimo derivation\nInspiration: 3Blue1Brown's Fourier lesson", 24, MUTED, center=True)
        text(d, (80, 506, 1120, 40), "Full URLs, assumptions and credits in videos/README.md", 22, MUTED, center=True)
    _, caption = cue_at(t, data)
    d.rectangle((0, 580, 1280, 720), fill="#0a111c")
    text(d, (80, 590, 1120, 80), caption, 26, center=True)
    text(d, (64, 684, 1152, 28), "MATH IN CONTEXT   /   SYNTHETIC EXAMPLE   /   NO GRID TELEMETRY", 16, MUTED)
    d.rectangle((0, 716, int(1280*t/data["duration"]), 719), fill=CYAN)
    return image


def timestamp(seconds):
    ms = round(seconds * 1000)
    return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}"


def write_captions(path, data=LESSON):
    cues = [f"{timestamp(a)} --> {timestamp(b)}\n{c}\n" for a,b,c in caption_cues(data)]
    path.write_text("WEBVTT\n\n" + "\n".join(cues))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=ROOT/"out")
    p.add_argument("--stills-only", action="store_true")
    p.add_argument("--scenario", type=Path, help="JSON override with exactly the three timing parameters")
    args = p.parse_args()
    data = load_lesson(ROOT/"fft-latency/lesson.json", args.scenario)
    args.out.mkdir(parents=True, exist_ok=True)
    write_captions(args.out/"captions.vtt", data)
    for s in data["scenes"]:
        render_frame((s["start"]+s["end"])/2, data).save(args.out/f"{s['id']}.png")
    if args.stills_only:
        return
    fps = data["fps"]
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-f", "rawvideo",
               "-pix_fmt", "rgb24", "-s", "1280x720", "-r", str(fps), "-i", "pipe:0",
               "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "20",
               "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(args.out/"fft-latency-draft.mp4")]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
        try:
            for i in range(data["duration"] * fps):
                process.stdin.write(render_frame(i/fps, data).tobytes())
        finally:
            process.stdin.close()
        if process.wait():
            raise RuntimeError("FFmpeg render failed")


if __name__ == "__main__":
    main()
