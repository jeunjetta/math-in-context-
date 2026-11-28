import copy
from fractions import Fraction as F
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import overhead_check as o


class OverheadCheckTests(unittest.TestCase):
    def setUp(self):
        self.spec, self.lesson = o.load()

    def test_exact_original_prediction_and_break_even(self):
        for h,total,gain,status in ((0,90,F(10,9),'faster'),
                (8,98,F(50,49),'faster'),(10,100,F(1),'break-even'),
                (12,102,F(50,51),'slower')):
            with self.subTest(h=h):
                r = o.evaluate(self.lesson, h)
                self.assertEqual((r['total'],r['speedup'],r['outcome']), (total,gain,status))
                self.assertEqual(r['break_even'],10)
        for h,status in ((9.99,'faster'),(10.01,'slower')):
            self.assertEqual(o.evaluate(self.lesson,h)['outcome'],status)

    def test_general_model_and_no_mutation(self):
        model = dict(baseline_ms=200, fourier_ms=100, kernel_speedup=4)
        original = copy.deepcopy(model)
        r = o.evaluate(model,75)
        self.assertEqual((r['total'],r['break_even'],r['speedup']), (200,75,1))
        self.assertEqual(model,original)
        with self.assertRaises(ValueError):
            o.evaluate(dict(model, kernel_speedup=1),0)

    def test_invalid_overhead(self):
        for h in (-1,True,'8',None,float('nan'),float('inf')):
            with self.subTest(h=h),self.assertRaises(ValueError):
                o.evaluate(self.lesson,h)

    def test_feedback_uses_actual_speedup_not_always_halving(self):
        for baseline,fourier,gain,new_fourier,total,saving in (
                (200,100,4,25,133,75), (100,20,2.5,8,96,12)):
            with self.subTest(gain=gain):
                model = dict(baseline_ms=baseline, fourier_ms=fourier,
                             kernel_speedup=gain)
                spec = copy.deepcopy(self.spec)
                spec['overheads_ms'] = [0,8,saving,saving+2]
                spec['prediction_choices_ms'] = [total-8,total,baseline+8]
                before = copy.deepcopy((spec,model))
                text = o.document(spec,model)
                self.assertIn(f'forgets to divide Fourier time by {gain:g}.',text)
                self.assertIn(f'**{total} ms**: {new_fourier} + '
                              f'{baseline-fourier} + 8 = {total} ms.',text)
                self.assertIn(f'Exactly **{saving} ms of new overhead**',text)
                self.assertNotIn('forgets to halve',text)
                self.assertEqual((spec,model),before)

    def test_scope_and_misleading_precision_rejected(self):
        actual = Path.read_text
        for key,value in (('publication_approved',True),('movie_sha256','wrong'),
                          ('changed_assumption','Same accuracy'),
                          ('prediction_choices_ms',[90,108]),
                          ('overheads_ms',[0,8,10.001])):
            spec = copy.deepcopy(self.spec); spec[key] = value
            def read(path,*args,**kwargs):
                if path.name=='overhead-check.json': return json.dumps(spec)
                return actual(path,*args,**kwargs)
            with self.subTest(key=key),patch.object(Path,'read_text',read):
                with self.assertRaises(ValueError): o.load()

    def test_display_rejects_rounded_operands_even_when_total_is_exact(self):
        spec = copy.deepcopy(self.spec)
        spec['prediction_choices_ms'] = [80,88,108]
        model = dict(baseline_ms=100, fourier_ms=20.005, kernel_speedup=4001)
        before = copy.deepcopy((spec,model))
        # Exact arithmetic remains reusable; only this two-decimal text is refused.
        self.assertEqual(o.evaluate(model,8)['total'],88)
        with self.assertRaisesRegex(ValueError,'two decimal'):
            o.document(spec,model)
        self.assertEqual((spec,model),before)
        for checking in (False,True):
            argv = ['overhead_check.py']+(['--check'] if checking else [])
            with patch('sys.argv',argv),patch.object(o,'load',return_value=(spec,model)),\
                 patch.object(Path,'write_text') as write:
                with self.assertRaisesRegex(ValueError,'two decimal'): o.main()
                write.assert_not_called()

    def test_direct_document_validates_overhead_precision_and_keeps_exact_cents(self):
        spec = copy.deepcopy(self.spec)
        spec['overheads_ms'] = [0,8.001,10,12]
        spec['prediction_overhead_ms'] = 8.001
        spec['prediction_choices_ms'] = [90,98.001,108.001]
        with self.assertRaisesRegex(ValueError,'two decimal'):
            o.document(spec,self.lesson)
        spec = copy.deepcopy(self.spec)
        spec['prediction_choices_ms'] = [89.99,97.99,108]
        model = dict(baseline_ms=100,fourier_ms=20.02,kernel_speedup=2)
        text = o.document(spec,model)
        self.assertIn('**97.99 ms**: 10.01 + 79.98 + 8 = 97.99 ms.',text)

    def test_document_fresh_and_check_never_writes(self):
        text = o.document(self.spec,self.lesson)
        self.assertEqual(o.OUTPUT.read_text(),text)
        for phrase in ('98 ms','exactly','100 / 98 ≈ 1.02×','100 / 100 = 1.00×',
                       'forgets to divide Fourier time by 2.',
                       '100 / 102 ≈ 0.98×','h < F(1 - 1/s)',
                       'not benchmark evidence','accuracy is assumed','not a deployed lesson'):
            self.assertIn(phrase,text)
        with patch('sys.argv',['overhead_check.py','--check']),patch.object(Path,'write_text') as write:
            o.main();write.assert_not_called()
        with patch('sys.argv',['overhead_check.py','--check']),patch.object(o,'load',return_value=(self.spec,self.lesson)),\
             patch.object(Path,'read_text',return_value='stale'),patch.object(Path,'write_text') as write:
            with self.assertRaises(SystemExit):o.main()
            write.assert_not_called()


if __name__ == '__main__':
    unittest.main()
