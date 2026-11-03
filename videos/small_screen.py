"""Downscaled stills from an existing FFT/latency QA pack, not device testing."""
import argparse
import hashlib
import json
from pathlib import Path
import re

from PIL import Image, __version__ as pillow_version


PICKS = ((35, "formula"), (52, "distinctions"), (75, "end"))
SIZES = ((640, 360), (960, 540))
LIMITS = (
    "Raster-size simulations, not CSS/device measurements or normal-speed playback. "
    "Scene/caption labels are QA metadata, not OCR. Hashes record supplied files, "
    "not proof that source PNGs came from the claimed MP4. No accessibility, "
    "comprehension, audio-sync or publication approval."
)


def sha(path):
    with Path(path).open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def make_pack(report_path, out):
    report_path, out = Path(report_path).resolve(), Path(out).resolve()
    if out.exists():
        raise FileExistsError("Choose a new small-screen output directory")
    report = json.loads(report_path.read_text())
    media = report["media"]
    if (report.get("full_decode_completed") is not True
            or media.get("timestamps_verified") is not True
            or (media["width"], media["height"], media["fps"], media["frames"],
                media["duration"], media["audio_streams"]) != (1280, 720, 24, 1920, 80, 0)
            or not re.fullmatch(r"[0-9a-f]{64}", report.get("input_sha256", ""))):
        raise ValueError("Expected a completed silent 1280x720, 24 fps, 80 s pilot QA report")
    # Validate and load every selected source before creating an output directory.
    sources = []
    for seconds, scene in PICKS:
        matches = [s for s in report["samples"]
                   if s["seconds"] == seconds and s["frame"] == seconds * 24
                   and s["scene"] == scene]
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one {seconds} s / {scene} sample")
        sample = matches[0]
        path = (report_path.parent / sample["image"]).resolve()
        if not path.is_relative_to(report_path.parent):
            raise ValueError("Sample must stay inside its QA directory")
        with Image.open(path) as image:
            if image.size != (1280, 720):
                raise ValueError("Source sample must be a full-size 1280x720 frame")
            sources.append((sample, image.convert("RGB"), sha(path)))
    out.mkdir(parents=True)
    records = []
    for sample, image, source_sha in sources:
        for width, height in SIZES:
            name = f"{int(sample['seconds']):02d}s-{sample['scene']}-{width}.png"
            image.resize((width, height), Image.Resampling.LANCZOS).save(out / name)
            records.append(dict(seconds=sample["seconds"], frame=sample["frame"],
                                scene=sample["scene"], width=width, height=height,
                                source_image_sha256=source_sha, image=name,
                                image_sha256=sha(out / name)))
    manifest = dict(input_video_sha256=report["input_sha256"],
                    source_report_sha256=sha(report_path),
                    generator_sha256=sha(Path(__file__)), pillow=pillow_version,
                    resampling="Pillow LANCZOS", samples=records,
                    limitations=LIMITS, publication_approved=False)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qa_report", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = make_pack(args.qa_report, args.out)
    print(f"Exported {len(result['samples'])} scaled stills. Human device/playback review remains required.")


if __name__ == "__main__":
    main()
