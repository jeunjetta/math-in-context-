import copy
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from qa import review_pack, sample_frames, validate_media
from render import LESSON


def fixture_probe():
    return {"streams": [{"codec_type": "video", "codec_name": "h264",
                         "width": 1280, "height": 720,
                         "avg_frame_rate": "24/1", "r_frame_rate": "24/1"}],
            "format": {"duration": "80.000"},
            "frames": [{"best_effort_timestamp_time": str(i/24)} for i in range(1920)]}


class QATests(unittest.TestCase):
    def test_cut_selection(self):
        frames = sample_frames(LESSON)
        self.assertEqual(frames, sorted(set(frames)))
        self.assertEqual((frames[0], frames[-1]), (0, 1919))
        for seconds in (8, 18, 30, 40, 49, 52, 55, 58, 61, 65.5, 70, 75):
            self.assertIn(round(seconds*24)-1, frames)
            self.assertIn(round(seconds*24), frames)
        self.assertIn(35*24, frames)  # legible equation hold

    def test_media_facts(self):
        facts = validate_media(fixture_probe(), LESSON)
        self.assertEqual(facts["frames"], 1920)
        self.assertTrue(facts["timestamps_verified"])
        self.assertEqual(facts["audio_streams"], 0)

    def test_reject_wrong_media(self):
        for field, value in (("width", 640), ("avg_frame_rate", "30/1")):
            probe = fixture_probe()
            probe["streams"][0][field] = value
            with self.assertRaises(ValueError):
                validate_media(probe, LESSON)
        for mutate in (
            lambda p: p["streams"].append({"codec_type": "audio"}),
            lambda p: p["frames"].pop(),
            lambda p: p["frames"][10].update(best_effort_timestamp_time="0.9"),
            lambda p: p["frames"][0].update(best_effort_timestamp_time="nan"),
            lambda p: p["format"].update(duration="79"),
        ):
            probe = fixture_probe()
            mutate(probe)
            with self.assertRaises(ValueError):
                validate_media(probe, LESSON)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                         "Local FFmpeg/FFprobe required for encoded integration test")
    def test_encoded_pack_and_no_overwrite(self):
        data = dict(fps=4, duration=1, width=1280, height=720,
                    scenes=[dict(id="fixture", start=0, end=1, captions=["Synthetic test frame."])])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            video = root/"fixture.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-n", "-f", "lavfi", "-i",
                            "color=c=navy:s=1280x720:r=4:d=1", "-an", "-c:v",
                            "libx264", "-threads", "1", "-pix_fmt", "yuv420p", str(video)], check=True)
            out = root/"qa"
            report = review_pack(video, out, data)
            self.assertFalse(report["publication_approved"])
            self.assertTrue(report["full_decode_completed"])
            self.assertEqual(report["media"]["frames"], 4)
            self.assertEqual(len(report["input_sha256"]), 64)
            self.assertTrue((out/"report.json").is_file())
            self.assertTrue((out/report["contact_sheets"][0]).is_file())
            for sample in report["samples"]:
                self.assertTrue((out/sample["image"]).is_file())
            with self.assertRaises(FileExistsError):
                review_pack(video, out, data)
            invalid = copy.deepcopy(data)
            invalid["duration"] = 2
            with self.assertRaises(ValueError):
                review_pack(video, root/"bad", invalid)
            self.assertFalse((root/"bad").exists())


if __name__ == "__main__":
    unittest.main()
