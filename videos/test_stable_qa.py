import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from stable_qa import stable_review_pack


class StableQATests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.movie = self.root/'input.mp4'
        self.movie.write_bytes(b'fixture bytes; never a decoder input')
        self.out = self.root/'qa'
        self.data = dict(scenes=[dict(id='fixture')])
        self.snapshot = None

    def fake_review(self, movie, out, data, every_seconds):
        self.snapshot = movie
        self.assertNotEqual(movie, self.movie)
        self.assertEqual(movie.read_bytes(), self.movie.read_bytes())
        out.mkdir()
        (out/'sample.png').write_bytes(b'fixture sample')
        data['scenes'][0]['id'] = 'private mutation'
        return dict(input_sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),
                    publication_approved=False, samples=[], full_decode_completed=True)

    def test_stable_copy_and_private_lesson(self):
        original = copy.deepcopy(self.data)
        with patch('stable_qa.review_pack', side_effect=self.fake_review):
            report = stable_review_pack(self.movie, self.out, self.data)
        self.assertEqual(self.data, original)
        self.assertFalse(self.snapshot.exists())
        self.assertEqual(json.loads((self.out/'report.json').read_text()), report)
        self.assertTrue((self.out/'sample.png').is_file())
        self.assertFalse(report['publication_approved'])

    def test_changed_during_qa_never_publishes(self):
        def mutate(*args):
            report = self.fake_review(*args)
            self.movie.write_bytes(b'new movie')
            return report
        with patch('stable_qa.review_pack', side_effect=mutate):
            with self.assertRaisesRegex(ValueError, 'changed during QA'):
                stable_review_pack(self.movie, self.out, self.data)
        self.assertFalse(self.out.exists())
        self.assertFalse(self.snapshot.exists())

    def test_changed_during_copy_rejected_before_decoder(self):
        real_copy = __import__('shutil').copyfile
        def mutate(source, target):
            real_copy(source, target)
            self.movie.write_bytes(b'changed while copying')
        with patch('stable_qa.shutil.copyfile', side_effect=mutate), \
             patch('stable_qa.review_pack') as decoder:
            with self.assertRaisesRegex(ValueError, 'taking the QA snapshot'):
                stable_review_pack(self.movie, self.out, self.data)
            decoder.assert_not_called()
        self.assertFalse(self.out.exists())

    def test_existing_output_or_decode_failure(self):
        self.out.mkdir()
        with patch('stable_qa.review_pack') as decoder:
            with self.assertRaises(FileExistsError):
                stable_review_pack(self.movie, self.out, self.data)
            decoder.assert_not_called()
        other = self.root/'other'
        with patch('stable_qa.review_pack', side_effect=RuntimeError('decode failed')):
            with self.assertRaisesRegex(RuntimeError, 'decode failed'):
                stable_review_pack(self.movie, other, self.data)
        self.assertFalse(other.exists())

    def test_destination_created_during_qa_not_overwritten(self):
        def collision(*args):
            report = self.fake_review(*args)
            self.out.mkdir()
            (self.out/'owner.txt').write_text('keep')
            return report
        with patch('stable_qa.review_pack', side_effect=collision):
            with self.assertRaises(FileExistsError):
                stable_review_pack(self.movie, self.out, self.data)
        self.assertEqual((self.out/'owner.txt').read_text(), 'keep')
        self.assertFalse((self.out/'report.json').exists())


if __name__ == '__main__':
    unittest.main()
