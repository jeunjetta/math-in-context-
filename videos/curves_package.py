"""Offline draft-package checks; no publishing or approval capability.

Edit package.json, inspect --stdout, update PACKAGE.md with that output,
then run --check. Data and generated copy stay separate from rendering.
These guards detect identity/copy drift, not truth, readability or rights.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "same-looking-curves"
PRIMARY = {
    "harmonic": "https://dlmf.nist.gov/1.9",
    "potential": "https://web.mit.edu/6.013_book/www/chapter4/4.1.html",
    "dipole": "https://ccmc.gsfc.nasa.gov/static/files/Dipole.pdf",
}
INSPIRATIONS = {
    "https://www.3blue1brown.com/lessons/zeta/",
    "https://www.3blue1brown.com/lessons/quaternions/",
}


def load():
    return json.loads((ROOT / "package.json").read_text(encoding="utf-8"))


def validate(data, root=ROOT):
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    episode = json.loads((root / "episode.json").read_text(encoding="utf-8"))
    candidate = json.loads((root / "review-candidate.json").read_text(encoding="utf-8"))
    report = json.loads((root / "episode-render.json").read_text(encoding="utf-8"))
    require(data["schema_version"] == 1, "Unknown package schema")
    require(data["status"] == "draft" and data["publication_approved"] is False,
            "This workflow is draft-only; it cannot grant publication approval")
    require(data["candidate"] == candidate, "Package does not match frozen candidate")
    require(candidate["publication_approved"] is False and candidate["audio"] is False,
            "This package is for an unapproved silent draft")
    for key in ("sha256", "duration", "fps", "frames", "audio", "publication_approved"):
        require(candidate[key] == report[key], "Candidate/render mismatch: " + key)
    require(candidate["source_baseline"] == report["source_commit"], "Source baseline drift")
    require(data["title"] == episode["title"], "Title differs from frozen lesson")
    require(candidate["duration"] == episode["duration"] and
            candidate["fps"] == episode["fps"] and
            candidate["frames"] == episode["duration"] * episode["fps"], "Timing drift")
    require(set(data["lesson_hashes"]) == {"episode.json", "episode.vtt"}, "Lesson hash set")
    for name, digest in data["lesson_hashes"].items():
        require(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest,
                "Lesson changed; re-review package: " + name)
    require(len(data["repo_baseline"]) == 40 and
            all(c in "0123456789abcdef" for c in data["repo_baseline"]), "Baseline commit")
    require(data["public_video_url"] is None and data["interactive_lesson_url"] is None,
            "No public destinations verified; a separate release review is required")
    require({s["id"]: s["url"] for s in data["primary_sources"]} == PRIMARY and
            len(data["primary_sources"]) == len(PRIMARY), "Primary-source ledger drift")
    require({s["url"] for s in data["inspirations"]} == INSPIRATIONS and
            len(data["inspirations"]) == len(INSPIRATIONS), "Inspiration ledger drift")
    for source in data["inspirations"]:
        require("not theorem validation" in source["role"], "Inspiration role missing")
    require(len(data["description"]) == 4 and len(data["review_questions"]) == 5,
            "Review the package structure explicitly before changing it")
    require(all(isinstance(s, str) and s.strip() for s in
                data["description"] + data["review_questions"]), "Empty copy")
    require("chatgpt.com/library" not in json.dumps(data) and
            "libfile_" not in json.dumps(data), "Private review locator in public copy")


def markdown(data):
    validate(data)
    c = data["candidate"]
    lines = [
        "# Curves episode · draft publication package", "",
        "**Review copy only. Not published, scheduled or approved.**",
        "FFT/latency v7 remains the first release milestone. This later-candidate",
        "package does not clear any video, mathematics, rights or publishing gate.", "",
        "## Frozen candidate", "",
        f"- Candidate: `{c['candidate']}` · {c['duration']} seconds · {c['fps']} fps · {c['frames']:,} frames · silent.",
        f"- MP4 SHA256: `{c['sha256']}`.",
        f"- Package repo baseline: `{data['repo_baseline']}` (not a new render).",
        f"- Render source baseline: `{c['source_baseline']}`; actual source hashes are in [episode-render.json](episode-render.json).",
        "- [Exact-version review](REVIEW.md) · [lesson and assumptions](EPISODE.md) · [structured copy](package.json).",
        "- No public video or interactive-lesson destination has been verified. None is inserted below.", "",
        "## Proposed public title", "", data["title"], "",
        "## Proposed public description", "",
    ]
    for paragraph in data["description"]:
        lines += [paragraph, ""]
    lines += ["Mathematical sources:", ""]
    for source in data["primary_sources"]:
        lines += [f"- [{source['label']}]({source['url']})"]
    lines += ["", "Conceptual inspiration (no borrowed footage, artwork or narration; not theorem validation):", ""]
    for source in data["inspirations"]:
        lines += [f"- [{source['label']}]({source['url']})"]
    lines += ["", "## Internal source-role ledger — not additional public copy", "",
              f"Primary sources rechecked {data['sources_checked_utc']} UTC. No clips or transcript offsets are used.", ""]
    for source in data["primary_sources"] + data["inspirations"]:
        lines += [f"- **{source['label']}:** {source['role']}"]
    lines += ["", "## Place in the concept/application graph", "",
              "| Connection | What is and is not claimed |", "|---|---|",
              "| Analytic map → harmonic real part | Mathematical relation; does not assign physical meaning automatically |",
              "| Chosen potential → gradient → field lines | Modelling choice plus definitions; contours and field lines are different objects |",
              "| 3D dipole → orthographic camera | Representation loses depth; rotating the camera does not change the field |",
              "| Reading engineering field plots | Transferable interpretation habit, not a validated operational tool or speedup |", "",
              "## Timestamped reviewer prompts", "",
              "These are editorial prompts, not new proofs or completed checks. Reply on [draft PR #3](https://github.com/jeunjetta/math-in-context-/pull/3).", ""]
    for question in data["review_questions"]:
        lines += [f"- {question}"]
    lines += ["", "## Unchanged release gates", "",
              "- [ ] Actual-device full playback and reading pace for this exact media hash.",
              "- [ ] Independent mathematical and editorial review of the model choices and equations.",
              "- [ ] Audio decision; this candidate has no audio and no audio-sync claim.",
              "- [ ] Rights/provenance review, parent-branch reconciliation and exact-version publication approval.",
              "- [ ] Verify real public destinations before adding any video/lesson call to action.", "",
              "No automatic chapters, uploads, platform settings or scheduled posts are created.",
              "Review prompts use episode times, not a promise of platform chapter support.", "",
              "## Reproduce the copy check", "", "From `videos/` (Python standard library only):", "",
              "```sh", "python curves_package.py --check",
              "python curves_package.py --stdout",
              "python -m unittest test_curves_package -v", "```", "",
              "Edit package.json, inspect --stdout, update this generated Markdown and run --check.",
              "Identity/hash guards detect narrow drift, not correctness, readability, rights or approval.",
              "Any media/lesson change requires a newly reviewed package; do not transfer approval by filename."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true")
    group.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    text = markdown(load())
    if args.stdout:
        print(text, end="")
    elif (ROOT / "PACKAGE.md").read_text(encoding="utf-8") != text:
        raise SystemExit("PACKAGE.md differs from reviewed data; inspect --stdout")
    else:
        print("Draft package and frozen candidate agree; no approval granted.")


if __name__ == "__main__":
    main()
