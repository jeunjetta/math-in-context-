import json
import tempfile
import unittest

import fft_source_endcard_media as p
from fft_source_endcard import phase, sha


class SourceEndingMediaTests(unittest.TestCase):
    def test_exact_excerpt_mapping(self):
        data = p.timeline()
        self.assertEqual((data['fps'], data['duration']), (24, 10))
        self.assertEqual([(c['start'],c['end']) for c in data['cues']], [(0,5),(5,10)])
        for n in range(240):
            self.assertEqual(phase(round((n/24)*24)), 0 if n < 120 else 1)
            self.assertEqual(data['cues'][phase(n)]['text'], p.load()['cues'][phase(n)]['caption'])

    def test_matching_excerpt_captions(self):
        folder = p.ROOT/'fft-latency/source-ending-excerpt'
        self.assertEqual((folder/(p.NAME+'.vtt')).read_text(), p.captions())
        self.assertIn('00:00:05.000 --> 00:00:10.000', p.captions())
        self.assertNotIn('00:01:', p.captions())

    def test_encoded_evidence_identity(self):
        folder = p.ROOT/'fft-latency/source-ending-excerpt'
        r = json.loads((folder/'render-report.json').read_text())
        self.assertEqual(r['source_commit'], p.BASELINE)
        self.assertEqual(r['source_video_sha256'], p.load()['source_video_sha256'])
        self.assertEqual(r['media']['frames'], 240)
        self.assertTrue(r['media']['timestamps_verified'])
        self.assertEqual(r['media']['duration'], 10)
        self.assertFalse(r['publication_approved'])
        self.assertFalse(r['audio'])
        self.assertEqual(r['captions_sha256'], sha(folder/(p.NAME+'.vtt')))
        for path, digest in r['source_hashes'].items():
            self.assertEqual(sha(p.ROOT/path), digest)
        self.assertTrue({0,119,120,239}.issubset({s['frame'] for s in r['samples']}))

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):
                p.render(tmp)


if __name__ == '__main__':
    unittest.main()
