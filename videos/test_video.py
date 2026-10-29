import unittest
from pathlib import Path
import tempfile
from render import LESSON, ROOT, caption_cues, cue_at, render_frame, scene_at, font, write_captions


class VideoTests(unittest.TestCase):
    def test_arithmetic(self):
        b, f, s = (LESSON[k] for k in ("baseline_ms", "fourier_ms", "kernel_speedup"))
        self.assertEqual(b-f+f/s, 90)
        self.assertAlmostEqual(b/(b-f+f/s), 10/9)
        self.assertEqual(b/(b-f), 1.25)

    def test_continuity(self):
        scenes = LESSON["scenes"]
        self.assertEqual(scenes[0]["start"], 0)
        self.assertEqual(scenes[-1]["end"], LESSON["duration"])
        for a,b in zip(scenes, scenes[1:]):
            self.assertEqual(a["end"], b["start"])
        self.assertTrue(60 <= LESSON["duration"] <= 90)
        cues = caption_cues()
        for a,b in zip(cues, cues[1:]):
            self.assertAlmostEqual(a[1], b[0])
        for a,b,c in cues:
            self.assertLessEqual(len(c)/(b-a), 21)  # reading-rate guard, not user review

    def test_every_frame_text_fits(self):
        # Renderer throws on text overflow, including all animated number states.
        for frame in range(LESSON["duration"] * LESSON["fps"]):
            image = render_frame(frame / LESSON["fps"])
            self.assertEqual(image.size, (1280, 720))

    def test_boundaries_and_glyphs(self):
        self.assertEqual(scene_at(18)["id"], "halve")
        with self.assertRaises(ValueError):
            scene_at(80)
        self.assertIsNotNone(font(30).getmask("× ≠ → −"))

    def test_caption_and_focus_sync(self):
        scene = scene_at(49)
        self.assertEqual(len(scene["cards"]), len(scene["captions"]))
        self.assertEqual([c["title"] for c in scene["cards"]],
                         ["Complexity", "Stability", "Latency", "Readiness"])
        for index, start in enumerate((49, 52, 55, 58)):
            self.assertEqual(cue_at(start)[0], index)
            self.assertEqual(cue_at(start + 3 - 1/24)[0], index)
            # Inspect the actual focus-border pixel, not only its timing helper.
            image = render_frame(start)
            for i in range(4):
                x, y = 64 + i % 2 * 588, 242 + i // 2 * 147
                expected = (99,224,208) if i == index else (32,50,73)
                self.assertEqual(image.getpixel((x+100, y+1)), expected)
        for start, end, caption in caption_cues():
            self.assertEqual(cue_at(start)[1], caption)
            self.assertEqual(cue_at(end - 1/24)[1], caption)

    def test_checked_in_vtt_matches(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "captions.vtt"
            write_captions(path)
            self.assertEqual(path.read_bytes(),
                             (ROOT / "fft-latency/captions.vtt").read_bytes())


if __name__ == "__main__":
    unittest.main()
