import copy
import json
from pathlib import Path
import tempfile
import unittest

from qa import validate_media
import fft_teaser_media as m


class MediaTests(unittest.TestCase):
    def test_vtt_and_cut_selection(self):
        text=m.vtt()
        self.assertNotIn('No matching',text)
        self.assertIn('not aligned to speech',text)
        for cue in m.resolved()['cues']: self.assertIn(cue['caption'],text)
        self.assertIn('00:00:22.000 --> 00:00:28.000',text)
        indices=m.selection()
        self.assertEqual(indices,sorted(set(indices)))
        self.assertTrue(all(0<=n<672 for n in indices))
        for n in (96,192,288,408,528,564,600,636):
            self.assertIn(n,indices);self.assertIn(n-1,indices)
        self.assertIn(0,indices);self.assertIn(671,indices)

    def test_vertical_media_validation(self):
        probe=dict(streams=[dict(codec_type='video',codec_name='h264',width=1080,height=1920,
                                avg_frame_rate='24/1',r_frame_rate='24/1')],
                   frames=[{'best_effort_timestamp_time':str(n/24)} for n in range(672)],
                   format={'duration':'28.000'})
        data=dict(width=1080,height=1920,fps=24,duration=28)
        self.assertEqual(validate_media(probe,data)['frames'],672)
        bad=copy.deepcopy(probe);bad['streams'][0]['width']=1280
        with self.assertRaises(ValueError):validate_media(bad,data)
        bad=copy.deepcopy(probe);bad['frames'][400]['best_effort_timestamp_time']='0'
        with self.assertRaises(ValueError):validate_media(bad,data)

    def test_no_overwrite_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):m.render(tmp)
            with self.assertRaises(ValueError):m.inspect(Path(tmp)/'missing.mp4',Path(tmp)/'out')
            fake=Path(tmp)/'fake.mp4';fake.touch()
            with self.assertRaises(FileExistsError):m.inspect(fake,tmp)

    def test_frozen_render_report_identity(self):
        folder=m.ROOT/'fft-latency/teaser-render'
        r=json.loads((folder/'render-report.json').read_text())
        candidate=json.loads((folder/'candidate.json').read_text())
        self.assertEqual(candidate['sha256'],r['sha256'])
        self.assertEqual(candidate['source_baseline'],r['source_commit'])
        self.assertFalse(candidate['publication_approved'])
        self.assertIsNone(candidate['public_video_url'])
        self.assertIsNone(candidate['interactive_lesson_url'])
        self.assertFalse(r['publication_approved']);self.assertFalse(r['audio'])
        self.assertTrue(r['complete_decode']);self.assertEqual(r['media']['frames'],672)
        self.assertEqual(m.sha(folder/'fft-latency-teaser.vtt'),r['captions_sha256'])
        self.assertEqual((folder/'fft-latency-teaser.vtt').read_text(),m.vtt())
        for p,sha in r['source_hashes'].items():self.assertEqual(m.sha(m.ROOT/p),sha,p)
        self.assertEqual([row['frame'] for row in r['samples']],m.selection())
        for row in r['samples']:
            self.assertEqual(row['expected_caption'],m.cue_at(row['seconds'])['caption'])
            self.assertEqual(row['scope_focus'],m.scope_index(row['seconds']))


if __name__=='__main__':unittest.main()
