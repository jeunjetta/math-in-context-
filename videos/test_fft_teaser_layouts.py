import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import fft_teaser_layouts as layouts


class LayoutTests(unittest.TestCase):
    def test_all_frames_and_incoming_cuts(self):
        counts={};focus=set()
        for n in range(672):
            im,r=layouts.frame_index(n)
            self.assertEqual(im.size,(1080,1920))
            self.assertEqual(r['caption'],layouts.cue_at(n/24)['caption'])
            counts[r['cue']]=counts.get(r['cue'],0)+1
            if r['scope_focus'] is not None: focus.add(r['scope_focus'])
        self.assertEqual(counts,dict(question=96,baseline=96,component=96,result=120,assumptions=120,scope=144))
        self.assertEqual(focus,{0,1,2,3})
        for n in (96,192,288,408,528):
            self.assertNotEqual(layouts.frame_index(n-1)[1]['cue'],layouts.frame_index(n)[1]['cue'])
        for n,i in ((528,0),(564,1),(600,2),(636,3)):
            self.assertEqual(layouts.frame_index(n)[1]['scope_focus'],i)
            if i: self.assertEqual(layouts.frame_index(n-1)[1]['scope_focus'],i-1)

    def test_no_spoiler_assumptions_and_scope(self):
        for t in (2,10):
            _,r=layouts.render_frame(t)
            words=' '.join(x['text'] for x in r['text'])
            self.assertNotIn('90',words)
            self.assertNotIn('1.11',words)
        _,r=layouts.render_frame(19)
        words=' '.join(x['text'] for x in r['text'])
        for label in layouts.load()['assumptions']: self.assertIn(label,words)
        for t,i in ((22.75,0),(24.25,1),(25.75,2),(27.25,3)):
            _,r=layouts.render_frame(t)
            words=' '.join(x['text'] for x in r['text'])
            self.assertIn(layouts.load()['scope'][i]['description'],words)
            self.assertIn('FFTW authors',words)

    def test_guards_and_export(self):
        for n in (-1,672,True,1.5):
            with self.assertRaises(ValueError): layouts.frame_index(n)
        for t in (-1,28,float('nan')):
            with self.assertRaises(ValueError): layouts.render_frame(t)
        d=copy.deepcopy(layouts.load());d['headlines']['question'][0]='X'*200
        with self.assertRaises(ValueError): layouts.render_frame(2,d)
        d=layouts.load();d['publication_approved']=True
        with self.assertRaises(ValueError): layouts.render_frame(2,d)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'new';layouts.export(out)
            r=json.loads((out/'report.json').read_text())
            self.assertEqual(len(r['images']),11)
            self.assertFalse(r['publication_approved']);self.assertFalse(r['audio'])
            with self.assertRaises(FileExistsError): layouts.export(out)

    def test_preview_source_and_image_identity(self):
        folder=layouts.FOLDER/'teaser-layouts'
        r=json.loads((folder/'report.json').read_text())
        for name,sha in r['source_sha256'].items():
            self.assertEqual(hashlib.sha256((layouts.ROOT/name).read_bytes()).hexdigest(),sha,name)
        for name,sha in r['images'].items():
            self.assertEqual(hashlib.sha256((folder/name).read_bytes()).hexdigest(),sha,name)
        for record in r['frames']:
            _,fresh=layouts.render_frame(record['time'])
            self.assertEqual(json.loads(json.dumps(fresh)),{k:v for k,v in record.items() if k!='time'})


if __name__=='__main__': unittest.main()
