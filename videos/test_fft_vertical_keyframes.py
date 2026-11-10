import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image
import fft_vertical_keyframes as k


class VerticalTests(unittest.TestCase):
    def test_checked_in_preview_identity(self):
        folder=k.FOLDER/'vertical-keyframes'
        report=json.loads((folder/'report.json').read_text())
        for name,sha in report['source_sha256'].items():
            self.assertEqual(hashlib.sha256((k.ROOT/name).read_bytes()).hexdigest(),sha,name)
        for name,sha in report['images'].items():
            self.assertEqual(hashlib.sha256((folder/name).read_bytes()).hexdigest(),sha,name)
        for record in report['frames']:
            _,fresh=k.image(record['kind'])
            self.assertEqual(json.loads(json.dumps(fresh)),record)

    def test_fit_captions_and_common_scale(self):
        for kind in ('baseline','result'):
            im,r=k.image(kind)
            self.assertEqual(im.size,(1080,1920))
            self.assertTrue(r['caption'])
            for t in r['text']:
                x,y,right,bottom=t['bounds']
                self.assertTrue(90<=x<=right<=900 and 170<=y<=bottom<=1550)
            for b in r['bars']:
                fourier,other=b['segments']
                self.assertAlmostEqual(other[2]-other[0],624)
                self.assertAlmostEqual(fourier[2]-fourier[0],156 if b['id']=='baseline' else 78)
                for rect,color in zip(b['segments'],('#63e0d0','#ffc273')):
                    x=int((rect[0]+rect[2])/2);y=int((rect[1]+rect[3])/2)
                    self.assertEqual(im.getpixel((x,y)),Image.new('RGB',(1,1),color).getpixel((0,0)))
            if kind=='baseline': self.assertNotIn('90',r['caption'])
            else: self.assertIn('90',r['caption'])

    def test_overflow_and_approval_fail_closed(self):
        d=copy.deepcopy(k.copy_data());d['headlines']['baseline'][0]='X'*200
        with self.assertRaises(ValueError): k.image('baseline',d)
        d=k.copy_data();d['publication_approved']=True
        with self.assertRaises(ValueError): k.image('baseline',d)
        with self.assertRaises(ValueError): k.image('question')

    def test_export_provenance_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'new';k.export(out)
            r=json.loads((out/'report.json').read_text())
            self.assertFalse(r['publication_approved'])
            self.assertFalse(r['audio'])
            self.assertEqual(len(r['images']),6)
            for name in r['images']:
                with Image.open(out/name) as im:
                    width=int(name.split('-')[1].split('.')[0])
                    self.assertEqual(im.size,(width,width*16//9))
            with self.assertRaises(FileExistsError): k.export(out)


if __name__=='__main__': unittest.main()
