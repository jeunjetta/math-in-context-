from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from PIL import ImageChops
import caption_fit as p


class CaptionFitTests(unittest.TestCase):
    def test_isolated_change_and_ink(self):
        original,proposed=p.data_pair();restored=deepcopy(proposed)
        restored['scenes'][5]['captions'][1]=original['scenes'][5]['captions'][1]
        self.assertEqual(original,restored)
        self.assertNotEqual(original,proposed)
        for data in (original,proposed):
            r=p.caption_ink(data);self.assertEqual(r['lines'],1)
            self.assertEqual(r['font_px'],26);self.assertEqual(r['nominal_font_px_at_640'],13)
        self.assertEqual([len(d['scenes'][5]['captions'][1]) for d in (original,proposed)],[55,46])

    def test_every_cue_frame_and_only_caption_pixels(self):
        original,proposed=p.data_pair()
        for n in range(1248,1320):
            a,b=(p.render_frame(n/24,d) for d in (original,proposed))
            self.assertIsNone(ImageChops.difference(a.crop((0,0,1280,580)),b.crop((0,0,1280,580))).getbbox())
            self.assertIsNone(ImageChops.difference(a.crop((0,680,1280,720)),b.crop((0,680,1280,720))).getbbox())
            self.assertIsNotNone(ImageChops.difference(a,b).getbbox())
            self.assertEqual(p.cue_at(n/24,proposed)[0],1)
        for n in (-1,1247,1320,True,52.0):
            with self.assertRaises(ValueError):p.frame(n,True)

    def test_reproducible_stills_and_committed_evidence(self):
        folder=p.FOLDER/'caption-fit';record=json.loads((folder/'report.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            fresh=p.export(Path(tmp)/'new')
            self.assertEqual(fresh,record)
        for name in ('current-640.png','proposed-640.png'):
            self.assertEqual(p.sha(folder/name),record['images'][name])
        for path,digest in record['source_hashes'].items():self.assertEqual(p.sha(p.ROOT/path),digest)
        self.assertFalse(record['publication_approved'])

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):p.export(tmp)


if __name__=='__main__':unittest.main()
