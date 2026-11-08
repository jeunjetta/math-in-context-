"""Narrow companion drift/arithmetic guards; no editorial or release approval."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import unittest

from curves_models import square_map, potential, electric_field

ROOT=Path(__file__).resolve().parent/'same-looking-curves'


class CompanionTests(unittest.TestCase):
    def test_frozen_identity_and_draft_destinations(self):
        data=json.loads((ROOT/'companion.json').read_text())
        candidate=json.loads((ROOT/'review-candidate.json').read_text())
        self.assertEqual(data['candidate'],candidate['candidate'])
        self.assertEqual(data['media_sha256'],candidate['sha256'])
        self.assertEqual(hashlib.sha256((ROOT/'episode.json').read_bytes()).hexdigest(),data['lesson_sha256'])
        self.assertFalse(data['publication_approved'])
        self.assertIsNone(data['public_video_url'])
        self.assertIsNone(data['interactive_lesson_url'])
        self.assertEqual(data['status'],'unpublished editorial draft')
        self.assertTrue((ROOT/data['article_path']).is_file())

    def test_public_copy_sources_scope_and_no_private_destinations(self):
        draft=(ROOT/'SUBSTACK_DRAFT.md').read_text()
        begin='<!-- PUBLIC_DRAFT_BEGIN -->';end='<!-- PUBLIC_DRAFT_END -->'
        self.assertEqual(draft.count(begin),1);self.assertEqual(draft.count(end),1)
        public=draft.split(begin)[1].split(end)[0]
        episode=json.loads((ROOT/'episode.json').read_text())
        self.assertIn('# '+episode['title'],public)
        self.assertTrue(350<=len(public.split())<=750)  # editorial size budget, not reading-time evidence
        package=json.loads((ROOT/'package.json').read_text())
        for source in package['primary_sources']+package['inspirations']:
            self.assertIn(source['url'],public)
        for token in ('not stereographic','normalized models','At the origin E=0','modelling',
                      'not theorem validation','No proof of the Riemann hypothesis'):
            self.assertIn(token,public)
        for token in ('chatgpt.com/library','libfile_','youtu.be','youtube.com','<iframe','watch now'):
            self.assertNotIn(token,public)
        self.assertNotIn('- [x]',draft)
        self.assertFalse(re.search(r'\]\((?!https://)[^)]+\)',public))

    def test_reproduced_map_and_gradient_arithmetic(self):
        self.assertEqual(square_map(F(1),F(1)),(F(0),F(2)))
        for x in [F(-2),F(-1,3),F(0),F(1),F(3,2)]:
            for y in [F(-1),F(0),F(1,2),F(2)]:
                u,v=square_map(x,y)
                self.assertEqual(u,potential(x,y))
                ex,ey=electric_field(x,y)
                self.assertEqual(2*x*ex-2*y*ey,-4*(x*x+y*y))
                self.assertEqual(y*ex+x*ey,0)
                if x==1:self.assertEqual(u,1-v*v/4)


if __name__=='__main__':unittest.main()
