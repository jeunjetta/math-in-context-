import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from PIL import Image
import encoded_caption_audit as audit


class EncodedCaptionTests(unittest.TestCase):
    def test_exact_solid_cores_and_eroded_edge(self):
        im = Image.new('RGB',(20,10),(10,17,28))
        for y in range(2,8):
            for x in range(2,8): im.putpixel((x,y),(244,247,252))
        result = audit.measure(im,im)
        self.assertEqual(result['foreground_core_pixels'],16)
        self.assertAlmostEqual(result['conservative_core_ratio'],
                               audit.colors.ratio('#f4f7fc','#0a111c'))

    def test_missing_thin_core_and_bad_geometry_fail(self):
        im = Image.new('RGB',(10,10),(10,17,28))
        for y in range(10): im.putpixel((5,y),(244,247,252))
        with self.assertRaises(ValueError): audit.measure(im,im)
        with self.assertRaises(ValueError): audit.measure(im,im.convert('L'))
        with self.assertRaises(ValueError): audit.measure(im,im.resize((5,5)))

    def test_decoded_not_source_colors_drive_result(self):
        ref = Image.new('RGB',(20,10),(10,17,28))
        for y in range(2,8):
            for x in range(2,8): ref.putpixel((x,y),(244,247,252))
        decoded = ref.copy()
        for y in range(2,8):
            for x in range(2,8): decoded.putpixel((x,y),(100,100,100))
        self.assertLess(audit.measure(ref,decoded)['conservative_core_ratio'],
                        audit.measure(ref,ref)['conservative_core_ratio'])

    def test_wrong_movie_rejected_before_decode_or_output(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'wrong.mp4'; path.write_bytes(b'wrong')
            out = Path(temp)/'out'
            with patch.object(audit.subprocess,'run') as run:
                with self.assertRaises(ValueError): audit.audit(path,out)
                run.assert_not_called()
            self.assertFalse(out.exists())


if __name__ == '__main__': unittest.main()
