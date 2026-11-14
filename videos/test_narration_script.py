import copy
import json
import unittest
import narration_script as n


class NarrationScriptTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((n.FOLDER/'narration.json').read_text())

    def test_exact_windows_pauses_and_budget(self):
        rows=n.validate(self.data)
        self.assertEqual(len(rows),19)
        self.assertEqual(sum(c['pause_seconds'] for c in rows),2)
        self.assertTrue(all(c['mechanical_wpm']<=160 for c in rows))
        self.assertEqual(n.words("model's real-time"),["model's","real","time"])

    def test_reject_timing_identity_or_approval_drift(self):
        for field,value in [('duration',90),('publication_approved',True),('audio_recorded',True),
                            ('source_video_sha256','0'*64),('source_lesson_sha256','0'*64)]:
            data=copy.deepcopy(self.data);data[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):n.validate(data)

    def test_reject_cue_pause_and_rate_errors(self):
        for field,value in [('start',1),('pause_seconds',True),('pause_seconds',float('nan')),
                            ('pause_seconds',4),('speech','word '*50)]:
            data=copy.deepcopy(self.data);data['cues'][0][field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):n.validate(data)

    def test_generated_script_and_honest_status(self):
        self.assertEqual((n.FOLDER/'NARRATION_SCRIPT.md').read_text(),n.script(self.data))
        self.assertFalse(self.data['audio_recorded']);self.assertFalse(self.data['publication_approved'])
        text=' '.join(c['speech'] for c in self.data['cues'])
        for phrase in ('sequential','same accuracy','no added overhead','other work fixed',
                       'synthetic','does not establish real-time grid readiness'):
            self.assertIn(phrase,text)


if __name__=='__main__':unittest.main()
