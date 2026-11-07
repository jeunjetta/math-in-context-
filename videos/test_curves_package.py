from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from curves_package import ROOT, PRIMARY, INSPIRATIONS, load, markdown, validate


class PackageTests(unittest.TestCase):
    def test_generated_copy_and_separated_source_roles(self):
        data = load()
        text = markdown(data)
        self.assertEqual(text, (ROOT / 'PACKAGE.md').read_text(encoding='utf-8'))
        public = text.split('## Proposed public description\n\n')[1].split('## Internal source-role ledger')[0]
        for url in list(PRIMARY.values()) + list(INSPIRATIONS):
            self.assertIn(url, public)
        self.assertIn(data['candidate']['sha256'], text)
        self.assertNotIn('chatgpt.com/library', text)
        self.assertNotIn('- [x]', text)
        self.assertNotIn('https://youtu', public)

    def test_identity_and_approval_drift_rejected(self):
        for key, value in [('sha256', '0' * 64), ('audio', True),
                           ('duration', 90), ('publication_approved', True)]:
            with self.subTest(key=key):
                bad = deepcopy(load()); bad['candidate'][key] = value
                with self.assertRaises(ValueError): validate(bad)
        for key, value in [('title', 'New title'), ('status', 'published'),
                           ('publication_approved', True),
                           ('public_video_url', 'https://example.org/movie'),
                           ('interactive_lesson_url', 'https://example.org/lesson')]:
            with self.subTest(key=key):
                bad = deepcopy(load()); bad[key] = value
                with self.assertRaises(ValueError): validate(bad)

    def test_lesson_and_source_drift_rejected(self):
        for name in ('episode.json', 'episode.vtt'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                for source in ('episode.json', 'episode.vtt', 'episode-render.json', 'review-candidate.json'):
                    (root / source).write_bytes((ROOT / source).read_bytes())
                # Whitespace preserves JSON semantics but changes the reviewed source identity.
                with (root / name).open('a', encoding='utf-8') as handle: handle.write('\n')
                with self.assertRaises(ValueError): validate(load(), root=root)
        bad = deepcopy(load()); bad['primary_sources'][0]['url'] = 'https://example.org'
        with self.assertRaises(ValueError): validate(bad)
        bad = deepcopy(load()); bad['inspirations'][0]['role'] = 'Theorem validation'
        with self.assertRaises(ValueError): validate(bad)


if __name__ == '__main__':
    unittest.main()
