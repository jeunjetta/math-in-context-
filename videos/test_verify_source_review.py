import copy
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import verify_source_review as v


class SourceCopyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.video = self.root/'fixture.mp4'
        self.captions = self.root/'fixture.vtt'
        # Fake bytes are used only with mocked subprocesses, never a decoder.
        self.video.write_bytes(b'fixture movie')
        self.captions.write_bytes(b'fixture captions')
        (self.root/'source.py').write_bytes(b'fixture source')
        self.resolved = self.root/'fft-latency/source-only-review/resolved-lesson.json'
        self.resolved.parent.mkdir(parents=True)
        self.resolved.write_bytes(b'fixture lesson')
        self.report = v.load_report()
        self.report.update(sha256=v.sha(self.video),size_bytes=self.video.stat().st_size,
            captions_sha256=v.sha(self.captions),resolved_lesson_sha256=v.sha(self.resolved),
            source_hashes={'source.py':v.sha(self.root/'source.py')})

    def check(self, report=None):
        v.verify_inputs(self.video,self.captions,report or self.report,self.root)

    def test_matching_input_and_wrong_bytes(self):
        self.check()
        for field in ('sha256','captions_sha256','resolved_lesson_sha256','size_bytes'):
            r=copy.deepcopy(self.report);r[field]=0 if field=='size_bytes' else '0'*64
            with self.subTest(field=field),self.assertRaises(ValueError):self.check(r)

    def test_render_evidence_drift_escape_or_missing(self):
        for sources in ({},{'source.py':'bad'},{'../outside.py':'bad'}):
            r=copy.deepcopy(self.report);r['source_hashes']=sources
            with self.subTest(sources=sources),self.assertRaises(ValueError):self.check(r)

    def test_wrong_scope(self):
        for field,value in [('publication_approved',True),('status','adopted'),('filename','old.mp4')]:
            r=copy.deepcopy(self.report);r[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.check(r)
        for field,value in [('duration',10),('audio_streams',1),('frames',240)]:
            r=copy.deepcopy(self.report);r['media'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.check(r)

    def test_manifest_pin_and_predecode_rejection(self):
        with patch.object(v,'sha',return_value='bad'):
            with self.assertRaises(ValueError):v.load_report()
        with patch.object(v.subprocess,'check_output') as decoder:
            with self.assertRaises(ValueError):v.verify(self.video,self.captions)
            decoder.assert_not_called()

    def probe(self):
        return dict(streams=[dict(codec_type='video',codec_name='h264',width=1280,
            height=720,avg_frame_rate='24/1',r_frame_rate='24/1')],
            frames=[dict(best_effort_timestamp_time=str(n/24)) for n in range(1920)],
            format=dict(duration='80.000'))

    def run_mocked(self, probe=None, failure=None):
        outputs=[json.dumps(probe or self.probe()).encode(),'ffmpeg fixture','ffprobe fixture']
        with patch.object(v,'load_report',return_value=self.report), \
             patch.object(v,'verify_inputs') as inputs, \
             patch.object(v.subprocess,'check_output',side_effect=outputs), \
             patch.object(v.subprocess,'run',side_effect=failure) as decode:
            result=v.verify(self.video,self.captions)
            self.assertEqual(inputs.call_count,2)
            decode.assert_called_once()
            self.assertTrue(decode.call_args.kwargs['check'])
            return result

    def test_probe_decode_and_final_inputs_checked(self):
        result=self.run_mocked()
        self.assertFalse(result['publication_approved'])
        self.assertEqual(result['media']['frames'],1920)
        self.assertEqual(result['sha256'],v.sha(self.video))

    def test_extra_stream_bad_timestamps_and_decode_failure(self):
        probe=self.probe();probe['streams'].append(dict(codec_type='audio'))
        with self.assertRaises(ValueError):self.run_mocked(probe)
        probe=self.probe();probe['frames'][-1]['best_effort_timestamp_time']='80'
        with self.assertRaises(ValueError):self.run_mocked(probe)
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_mocked(failure=subprocess.CalledProcessError(1,['ffmpeg']))

    def test_changed_input_after_decode_rejected(self):
        with patch.object(v,'load_report',return_value=self.report), \
             patch.object(v,'verify_inputs',side_effect=[None,ValueError('changed')]), \
             patch.object(v.subprocess,'check_output',return_value=json.dumps(self.probe()).encode()), \
             patch.object(v.subprocess,'run'):
            with self.assertRaisesRegex(ValueError,'changed'):v.verify(self.video,self.captions)

    def test_no_overwrite_before_verification(self):
        out=self.root/'prior.json';out.write_text('prior')
        with patch('sys.argv',['verify_source_review.py',str(self.video),'--out',str(out)]), \
             patch.object(v,'verify') as verify:
            with self.assertRaises(SystemExit) as error:v.main()
            self.assertEqual(error.exception.code,2);verify.assert_not_called()
        self.assertEqual(out.read_text(),'prior')

    def test_worksheet_identity_and_windows(self):
        text=(v.ROOT/'fft-latency/SOURCE_PLAYBACK_REVIEW.md').read_text()
        report=v.load_report()
        self.assertIn(report['sha256'],text)
        self.assertIn(report['filename'],text)
        self.assertIn(f"{report['size_bytes']:,}",text)
        lesson=json.loads((v.FOLDER/'resolved-lesson.json').read_text())
        windows=[(s['start'],s['end']) for s in lesson['scenes'][:-1]]+[(70,75),(75,80)]
        actual=[tuple(map(int,m)) for m in re.findall(r'^\| (\d+)–(\d+) s \|',text,re.M)]
        self.assertEqual(actual,windows)
        self.assertIn(lesson['scenes'][-1]['captions'][-1],text)
        self.assertIn('linked in the description.',text)


if __name__ == '__main__':
    unittest.main()
