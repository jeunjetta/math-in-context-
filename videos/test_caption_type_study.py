import json
from pathlib import Path
import tempfile
import unittest

from PIL import ImageChops
import caption_type_study as study
import render


class CaptionTypeTests(unittest.TestCase):
    def test_all_288_frames_fit_and_changes_stay_inside_caption_box(self):
        for n in range(1176, 1464):
            current = render.render_frame(n/24)
            proposed = study.frame(n)
            bbox = ImageChops.difference(current, proposed).getbbox()
            self.assertIsNotNone(bbox)
            self.assertTrue(80 <= bbox[0] < bbox[2] <= 1200)
            self.assertTrue(590 <= bbox[1] < bbox[3] <= 670)

    def test_cues_and_current_pixels_are_unchanged(self):
        for t in study.TIMES:
            for n in (t*24, (t+3)*24-1):
                self.assertIsNone(ImageChops.difference(
                    study.frame(n, 26), render.render_frame(n/24)).getbbox())
                a, b = study.ink(n/24, 26), study.ink(n/24, 34)
                self.assertEqual(a['text'], b['text'])
                self.assertEqual((a['lines'], b['lines']), (1, 1))
                self.assertEqual(b['nominal_font_px_at_640'], 17)
        for n in (1175, 1464, True, 1248.0):
            with self.assertRaises(ValueError): study.frame(n)
        with self.assertRaises(ValueError): study.frame(1248, 35)

    def test_reproduction_and_no_overwrite(self):
        folder = render.ROOT/'fft-latency/caption-type'
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)/'new'
            report = study.export(out)
            self.assertEqual(report, json.loads((folder/'report.json').read_text()))
            self.assertEqual((out/'comparison-640.png').read_bytes(),
                             (folder/'comparison-640.png').read_bytes())
            with self.assertRaises(FileExistsError): study.export(out)


if __name__ == '__main__':
    unittest.main()
