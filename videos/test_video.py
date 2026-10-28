import unittest
from render import LESSON, caption_cues, render_frame, scene_at, font


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


if __name__ == "__main__":
    unittest.main()
