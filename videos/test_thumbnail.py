import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image
import thumbnail
from lesson_model import load_lesson
from render import LESSON, ROOT


class ThumbnailTests(unittest.TestCase):
    def test_baseline_split_and_labels(self):
        image = thumbnail.render_thumbnail(LESSON)
        self.assertEqual(image.size, (1280, 720))
        cut = thumbnail.split_x(LESSON)
        self.assertEqual(cut, 294)  # rounded 20% of the 1152px baseline bar
        self.assertEqual(image.getpixel((cut-1, 420)), (99, 224, 208))
        self.assertEqual(image.getpixel((cut, 420)), (255, 194, 115))
        copy = thumbnail.resolved_copy(LESSON)
        self.assertEqual(copy["fourier"], "FFT\n20 ms")
        self.assertEqual(copy["other"], "OTHER WORK\n80 ms")
        self.assertIn("100 ms", copy["baseline"])

    def test_prediction_and_safety_labels_are_actually_drawn(self):
        with patch.object(thumbnail, "text", wraps=thumbnail.text) as drawn:
            thumbnail.render_thumbnail(LESSON)
        strings = [call.args[2] for call in drawn.call_args_list]
        self.assertIn("2× FASTER SYSTEM?", strings)
        self.assertIn("DRAFT", strings)
        self.assertIn("Synthetic example", strings)
        visible = "\n".join(strings)
        self.assertNotIn("90 ms", visible)  # prediction, not answer reveal
        self.assertNotIn("grid", visible.lower())
        self.assertIn("not a claim", thumbnail.resolved_copy(LESSON)["alt"])

    def test_alternate_model_no_stale_numbers(self):
        alternate = load_lesson(ROOT / "fft-latency/lesson.json",
                                ROOT / "fft-latency/scenarios/half-share.json")
        thumbnail.render_thumbnail(alternate)  # fail if any label overflows
        self.assertEqual(thumbnail.split_x(alternate), 640)
        copy = thumbnail.resolved_copy(alternate)
        self.assertEqual(copy["hook"], "4× FASTER FFT.")
        self.assertIn("200 ms", copy["baseline"])
        self.assertEqual(copy["other"], "OTHER WORK\n100 ms")

    def test_exports_decode_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "candidate"
            thumbnail.export(out, LESSON)
            for name, size in [("thumbnail.png", (1280,720)), ("thumbnail-320.png", (320,180))]:
                path = out / name
                with Image.open(path) as image:
                    image.load()
                    self.assertEqual(image.size, size)
                    self.assertEqual(image.mode, "RGB")
                self.assertLess(path.stat().st_size, 2_000_000)
            with self.assertRaises(FileExistsError):
                thumbnail.export(out, LESSON)


if __name__ == "__main__":
    unittest.main()
