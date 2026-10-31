"""Local encoded-video review pack. No publishing or approval decisions."""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw
from lesson_model import load_lesson
from render import ROOT, caption_cues, cue_at, font, scene_at


def sample_frames(data):
    """Both sides of every cue cut, scene midpoints, first and last frames."""
    fps, count = data["fps"], data["fps"] * data["duration"]
    frames = {0, count - 1}
    for start, _, _ in caption_cues(data):
        incoming = math.ceil(start * fps)
        frames.update((max(0, incoming - 1), incoming))
    for scene in data["scenes"]:
        frames.add(math.floor((scene["start"] + scene["end"]) * fps / 2))
    return sorted(frames)


def validate_media(probe, data):
    streams = probe["streams"]
    videos = [s for s in streams if s["codec_type"] == "video"]
    if len(videos) != 1 or any(s["codec_type"] == "audio" for s in streams):
        raise ValueError("QA currently requires one video stream and no audio; narration needs separate sync review")
    video = videos[0]
    if (video["width"], video["height"]) != (data["width"], data["height"]):
        raise ValueError("Encoded dimensions do not match lesson")
    fps = data["fps"]
    if any(Fraction(video[k]) != fps for k in ("avg_frame_rate", "r_frame_rate")):
        raise ValueError("Encoded frame rates do not match lesson")
    times = [float(f["best_effort_timestamp_time"]) for f in probe["frames"]]
    if len(times) != fps * data["duration"]:
        raise ValueError("Decoded frame count does not match lesson")
    if any(not math.isfinite(t) or abs(t - i / fps) > 0.00001
           for i, t in enumerate(times)):
        raise ValueError("Frame timestamps are not the expected zero-based constant-rate timeline")
    duration = float(probe["format"]["duration"])
    if not math.isfinite(duration) or abs(duration - data["duration"]) > 0.001:
        raise ValueError("Encoded duration does not match lesson")
    return dict(codec=video["codec_name"], width=video["width"],
                height=video["height"], fps=fps, frames=len(times),
                duration=duration, audio_streams=0, timestamps_verified=True)


def contact_sheets(paths, records, out):
    sheets = []
    for offset in range(0, len(paths), 6):
        sheet = Image.new("RGB", (1280, 1248), "#101c2c")
        draw = ImageDraw.Draw(sheet)
        draw.text((16, 8), "ENCODED SAMPLES / HUMAN REVIEW REQUIRED", font=font(22), fill="white")
        for slot, path in enumerate(paths[offset:offset + 6]):
            record = records[offset + slot]
            x, y = slot % 2 * 640, 48 + slot // 2 * 400
            with Image.open(path) as frame:
                frame = frame.convert("RGB")
                frame.thumbnail((624, 351))
                sheet.paste(frame, (x + 8, y))
            label = f"frame {record['frame']:04d} / {record['seconds']:.3f}s / {record['scene']}"
            draw.text((x + 8, y + 355), label, font=font(19), fill="white")
        name = f"contact-{offset // 6 + 1:02d}.png"
        sheet.save(out / name)
        sheets.append(name)
    return sheets


def review_pack(video, out, data):
    video, out = Path(video).resolve(), Path(out).resolve()
    if not video.is_file():
        raise ValueError("Input must be an existing local video file")
    # Never overwrite a prior review pack or its evidence.
    if out.exists():
        raise FileExistsError("Choose a new QA output directory")
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames",
        "-show_entries", "frame=best_effort_timestamp_time:stream=codec_type,codec_name,width,height,avg_frame_rate,r_frame_rate:format=duration",
        "-of", "json", str(video)]))
    # Probe all streams separately: -select_streams above otherwise hides audio.
    all_streams = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
        "-of", "json", str(video)]))["streams"]
    if any(s["codec_type"] == "audio" for s in all_streams):
        raise ValueError("Audio found: this silent-draft QA cannot certify audio/caption sync")
    if sum(s["codec_type"] == "video" for s in all_streams) != 1:
        raise ValueError("Expected exactly one video stream")
    facts = validate_media(probe, data)
    out.mkdir(parents=True)
    frames_dir = out / "frames"
    frames_dir.mkdir()
    indices = sample_frames(data)
    select = "+".join(f"eq(n\\,{i})" for i in indices)
    # Consume the entire stream, including its last frame; -xerror stops on errors.
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-xerror", "-n",
                    "-i", str(video), "-map", "0:v:0", "-vf", f"select={select}",
                    "-vsync", "0", "-threads", "1", str(frames_dir / "%04d.png")], check=True)
    paths = sorted(frames_dir.glob("*.png"))
    if len(paths) != len(indices):
        raise ValueError("Decoded sample count does not match selection; incomplete pack")
    records = [dict(frame=i, seconds=i / data["fps"], scene=scene_at(i / data["fps"], data)["id"],
                    expected_caption=cue_at(i / data["fps"], data)[1],
                    image=f"frames/{path.name}") for i, path in zip(indices, paths)]
    sheets = contact_sheets(paths, records, out)
    def sha(path):
        with path.open("rb") as source:
            return hashlib.file_digest(source, "sha256").hexdigest()
    report = dict(input_sha256=sha(video), qa_source_sha256=sha(Path(__file__)),
                  lesson_sha256=hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest(),
                  tools={name: subprocess.check_output([name, "-version"], text=True).splitlines()[0]
                         for name in ("ffmpeg", "ffprobe")},
                  media=facts, full_decode_completed=True, samples=records, contact_sheets=sheets,
                  limitations="Expected captions come from supplied lesson, not OCR. Sampling does not establish content/source identity, accessibility, comprehension, audio sync or approval.",
                  publication_approved=False)
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scenario", type=Path)
    args = parser.parse_args()
    data = load_lesson(ROOT / "fft-latency/lesson.json", args.scenario)
    report = review_pack(args.video, args.out, data)
    print(f"QA pack: {len(report['samples'])} encoded samples; human review still required.")


if __name__ == "__main__":
    main()
