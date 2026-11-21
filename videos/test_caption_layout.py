import json
from pathlib import Path
import tempfile
import unittest

from PIL import ImageChops
import caption_layout as c
import render


class CaptionLayoutTests(unittest.TestCase):
    def test_every_frame_and_unchanged_noncaption_pixels(self):
        for n in range(1920):
            original=render.render_frame(n/24)
            proposed=c.frame(n)
            bounds=ImageChops.difference(original,proposed).getbbox()
            self.assertTrue(80 <= bounds[0] < bounds[2] <= 1200)
            self.assertTrue(590 <= bounds[1] < bounds[3] <= 682)

    def test_original_copy_timing_and_ink(self):
        cues=render.caption_cues()
        self.assertEqual(len(cues),19)
        self.assertIs(c.CONFIG['publication_approved'],False)
        self.assertEqual(c.CONFIG['font_px'],34)
        # Advance-centering put this negative-bearing glyph 0.5px outside.
        tight=c.layout(render.cue_at(65.5)[1])
        self.assertEqual(tight['ink_bounds'][0][0],80)
        self.assertEqual(tight['ink_bounds'][0][2],1200)
        self.assertEqual(tight['origins'][0][0],81)
        for a,b,text in cues:
            ledger=c.layout(text)
            self.assertEqual(' '.join(ledger['lines']),text)
            self.assertLessEqual(len(ledger['lines']),2)
            for box in ledger['ink_bounds']:
                self.assertLessEqual(box[3],682)
            for n in (int(a*24),int(b*24)-1):
                c.frame(n)
        for n in (-1,1920,True,24.0):
            with self.assertRaises(ValueError): c.frame(n)
        with self.assertRaises(ValueError): c.layout('x'*100)
        with self.assertRaises(ValueError): c.layout(('long words '*100))

    def test_reproducible_sheet_report_and_no_overwrite(self):
        folder=render.ROOT/'fft-latency/caption-layout'
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'new'
            self.assertEqual(c.export(out),json.loads((folder/'report.json').read_text()))
            self.assertEqual((out/'comparison-640.png').read_bytes(),(folder/'comparison-640.png').read_bytes())
            with self.assertRaises(FileExistsError): c.export(out)


if __name__=='__main__': unittest.main()
