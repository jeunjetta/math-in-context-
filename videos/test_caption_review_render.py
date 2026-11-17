from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import ImageChops
import caption_review_render as c


class CaptionReviewTests(unittest.TestCase):
    def test_router_boundaries_and_invalid_inputs(self):
        with patch.object(c.layout,'frame',return_value='layout') as ordinary, \
             patch.object(c.balance,'frame',return_value='balanced') as balanced:
            for n in (0,1679,1800,1919):
                self.assertEqual(c.frame(n),'layout');ordinary.assert_called_with(n)
            for n in (1680,1799):
                self.assertEqual(c.frame(n),'balanced');balanced.assert_called_with(n)
            for n in (-1,1920,True,24.0):
                with self.assertRaises(ValueError): c.frame(n)

    def test_pixels_reuse_the_tested_adapters(self):
        for n in (0,840,1248,1572,1679,1680,1799,1800,1919):
            expected=c.balance.frame(n) if 1680<=n<1800 else c.layout.frame(n)
            self.assertIsNone(ImageChops.difference(c.frame(n),expected).getbbox())

    def test_existing_directory_is_not_modified(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(c.subprocess,'Popen') as encoder:
            out=Path(tmp)
            with self.assertRaises(FileExistsError): c.encode(out)
            encoder.assert_not_called()
            self.assertEqual(list(out.iterdir()),[])


if __name__=='__main__': unittest.main()
