import json
from pathlib import Path
import tempfile
import unittest

import fft_teaser_slow_media as m


class SlowerMediaTests(unittest.TestCase):
    def test_34_second_media_not_28_second(self):
        probe=dict(streams=[dict(codec_type='video',codec_name='h264',width=1080,height=1920,
            avg_frame_rate='24/1',r_frame_rate='24/1')],
            frames=[{'best_effort_timestamp_time':str(n/24)} for n in range(816)],
            format={'duration':'34.000'})
        self.assertEqual(m.validate_media(probe,dict(width=1080,height=1920,fps=24,duration=34))['frames'],816)
        with self.assertRaises(ValueError):m.validate_media(probe,dict(width=1080,height=1920,fps=24,duration=28))
        probe['frames'][600]['best_effort_timestamp_time']='0'
        with self.assertRaises(ValueError):m.validate_media(probe,dict(width=1080,height=1920,fps=24,duration=34))

    def test_caption_and_incoming_focus_cuts(self):
        self.assertIn('00:00:22.000 --> 00:00:34.000',m.vtt())
        self.assertNotIn('Unrendered',m.vtt())
        self.assertIn('not aligned to speech',m.vtt())
        samples=m.selection()
        for n in (96,192,288,408,528,600,672,744):
            self.assertIn(n,samples);self.assertIn(n-1,samples)
        self.assertEqual(samples,sorted(set(samples)));self.assertEqual(samples[-1],815)

    def test_no_overwrite_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):m.render(tmp)
            with self.assertRaises(ValueError):m.inspect(Path(tmp)/'missing.mp4',Path(tmp)/'new')
            f=Path(tmp)/'fake.mp4';f.touch()
            with self.assertRaises(FileExistsError):m.inspect(f,tmp)

    def test_frozen_slow_candidate(self):
        folder=m.ROOT/'fft-latency/teaser-slower-render'
        r=json.loads((folder/'render-report.json').read_text())
        c=json.loads((folder/'candidate.json').read_text())
        self.assertEqual(c['sha256'],r['sha256']);self.assertFalse(c['publication_approved'])
        self.assertFalse(r['audio']);self.assertTrue(r['complete_decode'])
        self.assertEqual(r['media']['frames'],816);self.assertEqual(r['samples'][-1]['frame'],815)
        self.assertEqual([x['frame'] for x in r['samples']],m.selection())
        self.assertEqual((folder/'fft-latency-teaser-slower.vtt').read_text(),m.vtt())
        self.assertEqual(m.original.sha(folder/'fft-latency-teaser-slower.vtt'),r['captions_sha256'])
        for p,h in r['source_hashes'].items():self.assertEqual(m.original.sha(m.ROOT/p),h,p)
        for x in r['samples']:
            src=m.pacing.source_time(x['seconds'])
            self.assertEqual(x['expected_caption'],m.cue_at(src)['caption'])
            self.assertEqual(x['scope_focus'],m.scope_index(src))


if __name__=='__main__':unittest.main()
