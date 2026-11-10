from copy import deepcopy
from fractions import Fraction as F
import json
import unittest

from fft_teaser import ROOT,resolved,vtt
from lesson_model import metrics


class FFTTeaserTests(unittest.TestCase):
    def test_exact_public_arithmetic_and_vtt(self):
        m=metrics(json.loads((ROOT/'lesson.json').read_text()))
        self.assertEqual((m['baseline'],m['fourier'],m['other'],m['new_fourier'],m['new_total']),
                         (100,20,80,10,90))
        self.assertEqual(m['overall_gain'],F(10,9))
        self.assertEqual(vtt(),(ROOT/'teaser.vtt').read_text())
        cues=resolved()['cues']
        self.assertNotIn('90',cues[0]['caption'])
        self.assertIn('90 ms total',cues[3]['caption'])
        self.assertEqual(cues[-1]['end']*resolved()['fps'],672) # proposed frames only

    def test_identity_timeline_and_draft_guards(self):
        original=json.loads((ROOT/'teaser.json').read_text())
        for key,value in [('source_lesson_sha256','0'*64),('source_video_sha256','0'*64),
                          ('publication_approved',True),('audio',True),('duration',80),
                          ('public_video_url','https://example.org'),('interactive_lesson_url','https://example.org')]:
            bad=deepcopy(original);bad[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):resolved(bad)
        for key,value in [('start',1),('end',0),('source_scene','missing')]:
            bad=deepcopy(original);bad['cues'][0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):resolved(bad)
        bad=deepcopy(original);bad['cues'][0]['caption']='word '*40
        with self.assertRaises(ValueError):resolved(bad)

    def test_script_scope_and_storyboard(self):
        data=resolved();script=' '.join(c['caption'] for c in data['cues'])
        for phrase in ['Sequential work','Same accuracy','No added overhead','Other work unchanged',
                       'complexity','numerical stability','grid readiness']:
            self.assertIn(phrase,script)
        guide=(ROOT/'TEASER.md').read_text()
        for c in data['cues']:self.assertIn(c['caption'],guide)
        self.assertIn('not a crop',guide)
        self.assertNotIn('- [x]',guide)


if __name__=='__main__':unittest.main()
