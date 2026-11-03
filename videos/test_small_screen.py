import copy
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image
from small_screen import PICKS, SIZES, make_pack, sha


class SmallScreenTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.report_path = self.root / "report.json"
        self.out = self.root / "scaled"
        self.report = dict(input_sha256="a" * 64, full_decode_completed=True,
                           media=dict(width=1280, height=720, fps=24, frames=1920,
                                      duration=80, audio_streams=0, timestamps_verified=True),
                           samples=[])
        for seconds, scene in PICKS:
            name = f"{seconds}.png"
            Image.new("RGB", (1280, 720), "navy").save(self.root / name)
            self.report["samples"].append(dict(seconds=seconds, frame=seconds*24,
                                              scene=scene, image=name))

    def run_pack(self, report=None):
        self.report_path.write_text(json.dumps(self.report if report is None else report))
        return make_pack(self.report_path, self.out)

    def test_sizes_provenance_and_no_overwrite(self):
        result = self.run_pack()
        self.assertEqual(len(result["samples"]), 6)
        self.assertFalse(result["publication_approved"])
        self.assertEqual(result["source_report_sha256"], sha(self.report_path))
        self.assertNotIn(str(self.root), json.dumps(result))
        for sample in result["samples"]:
            with Image.open(self.out / sample["image"]) as image:
                self.assertIn(image.size, SIZES)
                self.assertEqual(image.getpixel((0, 0)), (0, 0, 128))
            self.assertEqual(sample["source_image_sha256"], sha(self.root / f"{sample['seconds']}.png"))
            self.assertEqual(sample["image_sha256"], sha(self.out / sample["image"]))
        before = sha(self.out / "manifest.json")
        with self.assertRaises(FileExistsError):
            make_pack(self.report_path, self.out)
        self.assertEqual(before, sha(self.out / "manifest.json"))

    def test_reject_unverified_or_wrong_media(self):
        for change in (lambda r: r.update(full_decode_completed=False),
                       lambda r: r.update(input_sha256="invalid"),
                       lambda r: r["media"].update(audio_streams=1),
                       lambda r: r["media"].update(width=640),
                       lambda r: r["media"].update(timestamps_verified=False)):
            report = copy.deepcopy(self.report)
            change(report)
            with self.assertRaises(ValueError):
                self.run_pack(report)
            self.assertFalse(self.out.exists())

    def test_reject_missing_duplicate_and_wrong_timestamp(self):
        for change in (lambda r: r["samples"].pop(),
                       lambda r: r["samples"].append(r["samples"][0]),
                       lambda r: r["samples"][0].update(frame=839)):
            report = copy.deepcopy(self.report)
            change(report)
            with self.assertRaises(ValueError):
                self.run_pack(report)
            self.assertFalse(self.out.exists())

    def test_reject_path_escape_and_bad_geometry(self):
        report = copy.deepcopy(self.report)
        report["samples"][0]["image"] = "../outside.png"
        with self.assertRaises(ValueError):
            self.run_pack(report)
        Image.new("RGB", (640, 360)).save(self.root / "75.png")
        with self.assertRaises(ValueError):
            self.run_pack()
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
