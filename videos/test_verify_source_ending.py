import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import verify_source_ending as v


class VerifySourceEndingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.movie = self.root/'fixture.mp4'
        self.caption = self.root/'fixture.vtt'
        # Deliberately not real media: unit fixtures must never reach a decoder.
        self.movie.write_bytes(b'fixture movie')
        self.caption.write_bytes(b'fixture captions')
        (self.root/'source.py').write_bytes(b'fixture source')
        self.report = json.loads((v.FOLDER/'render-report.json').read_text())
        self.report.update(sha256=v.sha(self.movie),captions_sha256=v.sha(self.caption),
                           source_hashes={'source.py':v.sha(self.root/'source.py')})

    def check(self,report=None):
        v.verify_inputs(self.movie,self.caption,report or self.report,self.root)

    def test_matching_input_bytes(self):
        self.check()

    def test_reject_wrong_movie_and_caption(self):
        for field in ('sha256','captions_sha256'):
            report=copy.deepcopy(self.report);report[field]='0'*64
            with self.subTest(field=field),self.assertRaises(ValueError):self.check(report)

    def test_reject_source_drift_or_escape(self):
        for sources in ({},{'source.py':'0'*64},{'../outside.py':'0'*64}):
            report=copy.deepcopy(self.report);report['source_hashes']=sources
            with self.subTest(sources=sources),self.assertRaises(ValueError):self.check(report)

    def test_reject_approval_audio_or_timeline_drift(self):
        for field,value in [('publication_approved',True),('audio',True),('duration',80),
                            ('excerpt_cue_windows',[[70,75],[75,80]])]:
            report=copy.deepcopy(self.report);report[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.check(report)

    def test_wrong_file_rejected_before_decoder(self):
        with patch.object(v.subprocess,'check_output') as decode:
            with self.assertRaises(ValueError):v.verify(self.movie,self.caption)
            decode.assert_not_called()

    def test_no_overwrite_before_verification(self):
        out=self.root/'prior.json';out.write_text('prior')
        with patch('sys.argv',['verify_source_ending.py',str(self.movie),'--out',str(out)]),\
             patch.object(v,'verify') as verify:
            with self.assertRaises(SystemExit) as error:v.main()
            self.assertEqual(error.exception.code,2);verify.assert_not_called()
        self.assertEqual(out.read_text(),'prior')


if __name__ == '__main__':
    unittest.main()
