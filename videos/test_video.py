import unittest
from pathlib import Path
import tempfile
import json
from fractions import Fraction
from unittest.mock import patch
import render
from lesson_model import context, load_lesson, metrics, quotient
from render import LESSON, ROOT, caption_cues, cue_at, render_frame, scene_at, font, write_captions, timestamp


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
        alternate = load_lesson(ROOT/"fft-latency/lesson.json",
                                ROOT/"fft-latency/scenarios/half-share.json")
        for data in (LESSON, alternate):
            for frame in range(data["duration"] * data["fps"]):
                image = render_frame(frame / data["fps"], data)
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

    def test_editorial_handoff_script_matches(self):
        review = (ROOT / "fft-latency/REVIEW.md").read_text()
        actual = review.split("<!-- BEGIN CANONICAL CAPTIONS -->\n", 1)[1].split(
            "\n<!-- END CANONICAL CAPTIONS -->", 1)[0]
        def short(t):
            return timestamp(t)[3:].removesuffix(".000")
        expected = "\n\n".join(
            f"**{short(a)}–{short(b)}**\n{caption}"
            for a, b, caption in caption_cues())
        self.assertEqual(actual, expected)

    def test_editorial_handoff_keeps_release_gates(self):
        review = (ROOT / "fft-latency/REVIEW.md").read_text()
        self.assertIn("DRAFT FOR KARIN'S REVIEW", review)
        self.assertIn("ADD_VERIFIED_LESSON_URL_BEFORE_PUBLICATION", review)
        self.assertNotIn("- [x]", review)
        self.assertIn("10% less elapsed time", review)
        self.assertIn("1.11× overall speedup", review)
        self.assertIn("https://fftw.org/accuracy/comments.html", review)

    def test_draft_cta_handoff_is_explicit(self):
        handoff = (ROOT / "fft-latency/LESSON_LINK.md").read_text()
        self.assertIn("BLOCKED FOR PUBLIC RELEASE", handoff)
        self.assertIn("40723050432", handoff)
        self.assertIn("40734730180", handoff)
        self.assertIn("ADD_VERIFIED_LESSON_URL_BEFORE_PUBLICATION", handoff)
        self.assertNotIn("- [x]", handoff)
        # Audit the actual drawn end-card pointer, not only the script.
        with patch.object(render, "text", wraps=render.text) as draw_text:
            render_frame(75)
            visible = "\n".join(str(call.args[2]) for call in draw_text.call_args_list)
        self.assertIn("VISUAL DRAFT", visible)
        self.assertIn("Try: apps/fft_and_latency.py", visible)
        self.assertNotIn("https://", visible)
        self.assertIn("[dated live-lesson handoff](LESSON_LINK.md)",
                      (ROOT / "fft-latency/REVIEW.md").read_text())

    def test_alternate_scenario_text_and_math(self):
        data = load_lesson(ROOT/"fft-latency/lesson.json",
                           ROOT/"fft-latency/scenarios/half-share.json")
        values = metrics(data)
        self.assertEqual(values["new_total"], 125)
        self.assertEqual(values["overall_gain"], Fraction(8,5))
        self.assertEqual(values["ceiling_gain"], 2)
        self.assertEqual(quotient(values["baseline"], values["new_total"]), "200 / 125 = 1.60×")
        self.assertEqual(quotient(Fraction(100), Fraction(90)), "100 / 90 ≈ 1.11×")
        with patch.object(render, "text", wraps=render.text) as draw_text:
            for t in (4, 13, 24, 28, 35, 45):
                render_frame(t, data)
            visible = "\n".join(str(call.args[2]) for call in draw_text.call_args_list)
        for required in ("4× faster FFT", "25 + 100 = 125", "200 / 125 = 1.60×",
                         "f = 0.50", "s = 4", "200 / 100 = 2.00×"):
            self.assertIn(required, visible)
        self.assertNotIn("0.20", visible)
        self.assertNotIn("90 ms", visible)
        for start, end, caption in caption_cues(data):
            self.assertNotIn("{", caption)
            self.assertLessEqual(len(caption)/(end-start), 21)

    def test_bar_uses_baseline_relative_scale(self):
        data = load_lesson(ROOT/"fft-latency/lesson.json",
                           ROOT/"fft-latency/scenarios/half-share.json")
        before = render_frame(13, data)
        self.assertEqual(before.getpixel((500, 310)), (99,224,208))
        self.assertEqual(before.getpixel((600, 310)), (255,194,115))
        after = render_frame(24, data)
        self.assertEqual(after.getpixel((620, 460)), (255,194,115))
        self.assertEqual(after.getpixel((640, 460)), (32,50,73))

    def test_invalid_or_rounded_example_fails_early(self):
        thirds = dict(LESSON, baseline_ms=3, fourier_ms=1, kernel_speedup=2)
        self.assertEqual(context(thirds)["fraction"], "1/3")
        for key, value in (("baseline_ms", 0), ("fourier_ms", 100),
                           ("kernel_speedup", 1), ("kernel_speedup", True),
                           ("kernel_speedup", float("nan")), ("kernel_speedup", 3)):
            data = dict(LESSON)
            data[key] = value
            with self.assertRaises(ValueError):
                context(data)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"scenario.json"
            path.write_text(json.dumps({"baseline_ms":200,"fourier_ms":100,
                                        "kernel_speedup":4,"caption":"stale"}))
            with self.assertRaises(ValueError):
                load_lesson(ROOT/"fft-latency/lesson.json", path)


if __name__ == "__main__":
    unittest.main()
