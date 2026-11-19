from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image, ImageChops

import source_only_review as s
import render


class SourceReviewTests(unittest.TestCase):
    def test_copy_and_timeline_are_scoped(self):
        data=s.lesson(); old=render.caption_cues(); new=render.caption_cues(data)
        self.assertEqual(new[:-2],old[:-2])
        self.assertEqual([(a,b) for a,b,_ in new],[(a,b) for a,b,_ in old])
        self.assertEqual(new[-2:],[(70,75,'Inspect the synthetic notebook source, linked in the description.'),
                                  (75,80,'No live lesson or real-grid benchmark is claimed.')])
        self.assertIn('our Marimo lesson',render.LESSON['scenes'][-1]['captions'][0])
        for key in ('baseline_ms','fourier_ms','kernel_speedup','assumptions'):
            self.assertEqual(data[key],render.LESSON[key])

    def test_router_and_invalid_inputs(self):
        with patch.object(s.caption_layout,'frame',return_value='earlier') as old, \
             patch.object(s,'ending_frame',return_value=Image.new('RGB',(1,1))) as end:
            for n in (0,839,1679):
                self.assertEqual(s.frame(n),'earlier'); old.assert_called_with(n)
            for n,index in ((1680,0),(1799,0),(1800,1),(1919,1)):
                s.frame(n);end.assert_called_with(index)
            for n in (-1,1920,True,24.0):
                with self.assertRaises(ValueError): s.frame(n)

    def test_selected_pixels_reuse_components(self):
        for n in (0,432,840,1248,1679,1800,1919):
            expected=s.caption_layout.frame(n) if n<1680 else s.ending.image(0 if n<1800 else 1)[0]
            self.assertIsNone(ImageChops.difference(s.frame(n),expected).getbbox())

    def test_first_ending_caption_only_rewraps_words(self):
        self.assertEqual(' '.join(s.CONFIG['first_ending_caption_lines']),s.ending.load()['cues'][0]['caption'])
        self.assertTrue(all(len(line.split())>=2 for line in s.CONFIG['first_ending_caption_lines']))
        before=s.ending.image(0)[0]
        after=s.frame(1680)
        box=ImageChops.difference(before,after).getbbox()
        self.assertIsNotNone(box)
        self.assertTrue(64<=box[0]<box[2]<=1216 and 595<=box[1]<box[3]<=693)
        self.assertIsNone(ImageChops.difference(after,s.frame(1799)).getbbox())

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(s.subprocess,'Popen') as encoder:
            with self.assertRaises(FileExistsError): s.encode(Path(tmp))
            encoder.assert_not_called()
            self.assertEqual(list(Path(tmp).iterdir()),[])


if __name__=='__main__':unittest.main()
