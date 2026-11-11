import unittest
import fft_teaser_pacing as p
import fft_teaser_layouts as original


class PacingTests(unittest.TestCase):
    def test_timeline_and_incoming_cuts(self):
        for n in range(816):
            t=n/24; mapped=p.source_time(t)
            self.assertTrue(0<=mapped<28)
            if t<22: self.assertEqual(t,mapped)
            else: self.assertEqual(original.scope_index(mapped),int((t-22)//3))
        for t in (-1,34):
            with self.assertRaises(ValueError):p.source_time(t)
        for n in (-1,816,True,1.5):
            with self.assertRaises(ValueError):p.frame(n)

    def test_sample_pixels_preserve_visuals_and_fit(self):
        for n in (0,287,288,527,528,599,600,671,672,743,744,815):
            im, rec=p.frame(n)
            old, prior=original.render_frame(p.source_time(n/24))
            self.assertEqual(im.tobytes(),old.tobytes())
            self.assertEqual(rec['cue'],prior['cue'])
            self.assertEqual(rec['comparison_seconds'],n/24)

    def test_rates_and_caption_coverage(self):
        r=p.report()
        self.assertEqual(r['comparison_frames'],816)
        for row in r['rows']:
            self.assertEqual(row['baseline_description_tokens_per_second'],
                             2*row['comparison_description_tokens_per_second'])
        rows=p.cues(); self.assertEqual(rows[0]['start'],0)
        self.assertEqual(rows[-1]['end'],34)
        for a,b in zip(rows,rows[1:]):self.assertEqual(a['end'],b['start'])
        self.assertIn('00:00:22.000 --> 00:00:34.000',p.vtt())
        self.assertIn('not aligned to speech',p.vtt())

    def test_generated_artifacts_and_draft_identity(self):
        for name,content in p.generated().items():
            self.assertEqual((p.FOLDER/name).read_text(),content,name)
        self.assertFalse(p.report()['publication_approved'])
        self.assertFalse(p.report()['audio'])
        self.assertIn('not validated reading-speed thresholds',p.markdown())


if __name__=='__main__':unittest.main()
