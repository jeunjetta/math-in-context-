import copy
import json
from pathlib import Path
import tempfile
import unittest
import fft_source_endcard as p


class SourceEndcardTests(unittest.TestCase):
    def test_coverage_and_actual_ink(self):
        self.assertEqual([p.phase(n) for n in range(240)].count(0),120)
        self.assertEqual(p.phase(120),1)
        for n in (-1,240,True,1.2):
            with self.assertRaises(ValueError):p.phase(n)
        for i in (0,1):
            im,r=p.image(i);self.assertEqual(im.size,(1280,720))
            self.assertTrue(all(x['size']>=28 for x in r['text']))
            self.assertEqual(r['caption'],p.load()['cues'][i]['caption'])

    def test_source_only_and_frozen_identity(self):
        d=p.load();self.assertFalse(d['publication_approved']);self.assertFalse(d['audio'])
        self.assertIn('not a live interactive app',d['disclosure'])
        self.assertIn('/blob/7905dc2b30ad9c05436f4db4a03d9cfe34224ffc/',d['notebook']['url'])
        self.assertEqual(d['notebook']['blob_sha'],'bf6eb0d52cb3bb20f0ec2747a0648612eb1af09a')
        self.assertEqual(d['source_video_sha256'],json.loads((p.FOLDER/'review-version.json').read_text())['video_sha256'])

    def test_frozen_proposal_report(self):
        folder=p.FOLDER/'source-endcard'
        r=json.loads((folder/'report.json').read_text())
        for path,h in r['images'].items():self.assertEqual(p.sha(folder/path),h)
        for path,h in r['source_hashes'].items():self.assertEqual(p.sha(p.ROOT/path),h)
        self.assertEqual(len(r['frames']),2);self.assertFalse(r['publication_approved'])

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):p.export(tmp)


if __name__=='__main__':unittest.main()
