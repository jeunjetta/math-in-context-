from fractions import Fraction
import json
import unittest
import caption_pacing as p


class CaptionPacingTests(unittest.TestCase):
    def test_measurement_definition(self):
        r=p.measure(0,4,'10 + 80 = 90 ms.')
        self.assertEqual(r['characters'],16)
        self.assertEqual(r['whitespace_tokens'],6)
        self.assertEqual(Fraction(r['cps_exact']),Fraction(16,4))
        self.assertEqual(Fraction(p.measure(40,44.5,'abc')['cps_exact']),Fraction(2,3))
        self.assertEqual(p.measure(0,1,'≈ 1.11×')['characters'],7)
        with self.assertRaises(ValueError):p.measure(1,1,'text')

    def test_full_coverage_and_top_review_region(self):
        r=p.report();rows=r['rows']
        self.assertEqual(len(rows),19)
        self.assertEqual(sum(Fraction(c['duration_exact']) for c in rows),80)
        self.assertTrue(all(a['end']==b['start'] for a,b in zip(rows,rows[1:])))
        top=[rows[i]['start'] for i in r['ranked_indices'][:4]]
        self.assertEqual(set(top),{49,52,55,58})
        self.assertEqual(rows[r['ranked_indices'][0]]['start'],52)

    def test_shorter_proposals_are_not_adopted(self):
        r=p.report();self.assertFalse(r['publication_approved'])
        self.assertEqual(len(r['proposals']),4)
        for c in r['proposals']:
            self.assertGreater(c['characters_removed'],0)
            self.assertEqual(c['original']['duration_exact'],c['proposed']['duration_exact'])
        self.assertIn('Numerical stability',r['proposals'][1]['proposed']['text'])

    def test_generated_reports_and_source_identity(self):
        for name,value in p.generated().items():self.assertEqual((p.FOLDER/name).read_text(),value)
        r=json.loads((p.FOLDER/'caption-pacing-report.json').read_text())
        for path,digest in r['source_hashes'].items():self.assertEqual(p.sha(p.ROOT/path),digest)
        self.assertIn('not a WCAG compliance assessment',p.markdown(r))


if __name__=='__main__':unittest.main()
