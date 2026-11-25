from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import caption_cut_audit as audit


class CaptionCutTests(unittest.TestCase):
    def templates(self):
        a,b = (Image.new('RGB',(10,10),(10,17,28)) for _ in range(2))
        for y in range(2,8):
            a.putpixel((2,y),(244,247,252))
            b.putpixel((7,y),(244,247,252))
        return a,b

    def test_all_cuts_include_fractional_second(self):
        cuts = audit.cuts()
        self.assertEqual(len(cuts),18)
        self.assertIn(1068,[r['frame'] for r in cuts])  # 44.5 seconds
        self.assertEqual(cuts[-1]['frame'],1800)
        self.assertEqual(len({k for r in cuts for k in (r['frame']-1,r['frame'])}),36)

    def test_correct_and_one_frame_shift_fixtures(self):
        a,b = self.templates()
        self.assertTrue(audit.compare(a,a,b)['expected_is_closer'])
        self.assertTrue(audit.compare(b,b,a)['expected_is_closer'])
        self.assertFalse(audit.compare(b,a,b)['expected_is_closer'])
        self.assertFalse(audit.compare(a,b,a)['expected_is_closer'])

    def test_invalid_or_ambiguous_templates(self):
        a,b = self.templates()
        with self.assertRaises(ValueError): audit.compare(a,a,a)
        with self.assertRaises(ValueError): audit.compare(a,a,b.convert('L'))
        with self.assertRaises(ValueError): audit.compare(a,a,b.resize((5,5)))
        blank = Image.new('RGB',(10,10))
        with self.assertRaises(ValueError): audit.compare(blank,blank,Image.new('RGB',(10,10),'red'))

    def test_wrong_file_before_decode_or_output(self):
        with tempfile.TemporaryDirectory() as temp:
            movie = Path(temp)/'wrong.mp4'; movie.write_bytes(b'wrong')
            with patch.object(audit.subprocess,'run') as run:
                with self.assertRaises(ValueError): audit.audit(movie,Path(temp)/'out')
                run.assert_not_called()
            self.assertFalse((Path(temp)/'out').exists())


if __name__ == '__main__': unittest.main()
