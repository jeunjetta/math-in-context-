import copy
import io
from contextlib import redirect_stdout
from pathlib import Path
import unittest
from unittest.mock import patch

import descriptive_transcript as d


class DescriptiveTranscriptTests(unittest.TestCase):
    def setUp(self):
        self.spec,self.lesson,self.report,self.ending=d.load()

    def test_complete_caption_timeline_and_visual_scene_coverage(self):
        cues=[cue for scene in self.lesson['scenes'] for cue in d.cues(scene)]
        self.assertEqual(len(cues),19)
        self.assertEqual(cues[0][0],0)
        self.assertEqual(cues[-1][1],80)
        self.assertTrue(all(a[1]==b[0] for a,b in zip(cues,cues[1:])))
        self.assertEqual(len(self.spec['scenes']),8)
        text=d.document(self.spec,self.lesson,self.report,self.ending)
        for _,_,caption in cues:
            self.assertIn(caption,text)
        self.assertEqual(text.count('Visual description:'),8)
        self.assertEqual(text.count('Active panel:'),4)
        for card in self.lesson['scenes'][5]['cards']:
            self.assertIn(f"{card['title']} — {card['description']}",text)

    def test_generated_document_fresh(self):
        self.assertEqual(d.OUTPUT.read_text(),d.document(*d.load()))

    def test_wrong_movie_approval_or_missing_visual_rejected(self):
        for key,value in [('movie_sha256','wrong'),('publication_approved',True),('status','approved')]:
            spec=copy.deepcopy(self.spec);spec[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):d.validate(spec,self.lesson,self.report)
        for operation in ('omit','reorder','blank'):
            spec=copy.deepcopy(self.spec)
            if operation=='omit':spec['scenes'].pop()
            elif operation=='reorder':spec['scenes'].reverse()
            else:spec['scenes'][0]['visual_description']=' '
            with self.subTest(operation=operation),self.assertRaises(ValueError):d.validate(spec,self.lesson,self.report)

    def test_manifest_source_lesson_and_caption_drift_rejected(self):
        actual=d.sha
        for suffix in ('render-report.json','render.py','resolved-lesson.json','fft-source-only-review.vtt'):
            with self.subTest(suffix=suffix),patch.object(d,'sha',side_effect=lambda path: 'bad' if Path(path).name==suffix else actual(path)):
                with self.assertRaises(ValueError):d.load()

    def test_equation_assumptions_and_endpoint_descriptions(self):
        text=d.document(*d.load())
        for phrase in ('Sequential work','Same accuracy','No added overhead','Other work unchanged',
                       'S = 1 / [(1 - f) + f/s]','f = 0.20','approximately 1.11',
                       'equals 1.25','From 18 to 21','From 40 to 43','At 44.5',
                       'endpoint, not an instantaneous measured total',
                       'not a live interactive app','not grid telemetry','not a speech transcript'):
            self.assertIn(phrase,text)
        self.assertIn(self.report['sha256'],text)
        self.assertIn(self.ending['notebook']['url'],text)

    def test_check_mode_never_writes(self):
        with patch('sys.argv',['descriptive_transcript.py','--check']), \
             patch.object(Path,'write_text') as write:
            d.main();write.assert_not_called()
        with patch('sys.argv',['descriptive_transcript.py','--check']), \
             patch.object(Path,'read_text',return_value='stale'), \
             patch.object(d,'load',return_value=(self.spec,self.lesson,self.report,self.ending)), \
             patch.object(Path,'write_text') as write:
            with self.assertRaises(SystemExit):d.main()
            write.assert_not_called()

    def test_cli_success_labels_only_what_it_checks(self):
        for checking in (False,True):
            argv=['descriptive_transcript.py']+(['--check'] if checking else [])
            stream=io.StringIO()
            with patch('sys.argv',argv),patch.object(Path,'write_text') as write,redirect_stdout(stream):
                d.main()
            message=stream.getvalue()
            self.assertIn('freshness checked' if checking else 'generated',message)
            self.assertIn('structure and pinned-source identity checked',message)
            self.assertIn('Visual equivalence and accessibility remain unverified',message)
            self.assertNotIn('match this draft',message)
            self.assertEqual(write.call_count,0 if checking else 1)

    def test_structure_validation_is_not_semantic_equivalence(self):
        # Deliberately false wording in an in-memory fixture ONLY. No file write.
        original=d.OUTPUT.read_bytes()
        spec=copy.deepcopy(self.spec)
        spec['scenes'][1]['visual_description']='Negative-control fixture: a purple 700 ms bar.'
        d.validate(spec,self.lesson,self.report)  # schema cannot detect this semantic error
        rendered=d.document(spec,self.lesson,self.report,self.ending)
        self.assertIn('purple 700 ms bar',rendered)
        self.assertFalse(spec['publication_approved'])
        self.assertEqual(d.OUTPUT.read_bytes(),original)


if __name__=='__main__':
    unittest.main()
