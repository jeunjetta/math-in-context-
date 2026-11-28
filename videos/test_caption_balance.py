import json
from pathlib import Path
import tempfile
import unittest
from PIL import ImageChops
import caption_balance as b
import caption_layout as base
import render


class BalanceTests(unittest.TestCase):
    def test_all_120_frames_change_only_caption_and_keep_words(self):
        for n in range(1680,1800):
            diff=ImageChops.difference(base.frame(n),b.frame(n)).getbbox()
            self.assertTrue(80<=diff[0]<diff[2]<=1200)
            self.assertTrue(590<=diff[1]<diff[3]<=682)
        ledger=b.balanced(render.cue_at(70)[1])
        self.assertEqual(' '.join(ledger['lines']),render.cue_at(70)[1])
        self.assertTrue(all(len(line.split())>=2 for line in ledger['lines']))
        self.assertLess(ledger['ink_width_difference_px'],100)
        self.assertEqual(base.layout(render.cue_at(70)[1])['lines'][-1],'lesson.')
        for box in ledger['ink_bounds']:
            self.assertTrue(80<=box[0]<box[2]<=1200)
            self.assertTrue(590<=box[1]<box[3]<=682)

    def test_rejects_outside_scope(self):
        for n in (1679,1800,True,1680.0):
            with self.assertRaises(ValueError): b.frame(n)
        for value in ('short line','one\ntwo','x'*100):
            with self.assertRaises(ValueError): b.balanced(value)

    def test_reproduction_and_no_overwrite(self):
        folder=render.ROOT/'fft-latency/caption-balance'
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'new'
            self.assertEqual(b.export(out),json.loads((folder/'report.json').read_text()))
            self.assertEqual((out/'comparison-640.png').read_bytes(),(folder/'comparison-640.png').read_bytes())
            with self.assertRaises(FileExistsError): b.export(out)


if __name__=='__main__': unittest.main()
