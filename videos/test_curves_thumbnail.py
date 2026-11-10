from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import tempfile
import unittest

from PIL import Image
from curves_thumbnail import DATA,FOLDER,geometry,plot_points,image,export,validate
from curves_models import potential


class CurvesThumbnailTests(unittest.TestCase):
    def test_checked_in_preview_provenance(self):
        folder=FOLDER/'thumbnail-previews-v2'
        report=json.loads((folder/'report.json').read_text())
        self.assertEqual(report['media_sha256'],DATA['media_sha256'])
        self.assertFalse(report['publication_approved'])
        for name,digest in report['source_sha256'].items():
            self.assertEqual(hashlib.sha256((FOLDER.parent/name).read_bytes()).hexdigest(),digest)
        for name,digest in report['images'].items():
            self.assertEqual(hashlib.sha256((folder/name).read_bytes()).hexdigest(),digest)

    def test_copy_fit_identity_and_bounds(self):
        self.assertEqual(image().size,(1280,720))
        bad=deepcopy(DATA);bad['media_sha256']='0'*64
        with self.assertRaises(ValueError):validate(bad)
        bad=deepcopy(DATA);bad['publication_approved']=True
        with self.assertRaises(ValueError):validate(bad)
        bad=deepcopy(DATA);bad['headline'][0]='M'*100
        with self.assertRaises(ValueError):image(bad)
        first,second,third=plot_points()
        for bounds,points in [((68,400,396,536),first),((476,400,804,536),second)]+[
                ((884,400,1212,536),points) for _,points in third]:
            l,t,r,b=bounds
            self.assertTrue(all(l<=x<=r and t<=y<=b for x,y in points))

    def test_geometric_meaning_and_source_exclusion(self):
        mapped,contour,dipole=geometry()
        for u,v in mapped:self.assertAlmostEqual(u,1-v*v/4)
        for x,y in contour:self.assertAlmostEqual(potential(x,y),1)
        for _,run in dipole:
            for p in run:self.assertGreaterEqual(math.sqrt(sum(x*x for x in p)),.15)
        self.assertEqual(DATA['notes'],['point image','constant V','3D projection'])

    def test_exports_decode_hashes_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'new';export(out)
            report=json.loads((out/'report.json').read_text())
            self.assertFalse(report['publication_approved'])
            for width in (1280,640,320):
                p=out/f'thumbnail-{width}.png'
                with Image.open(p) as im:
                    im.load();self.assertEqual(im.size,(width,width*9//16))
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),report['images'][p.name])
            with self.assertRaises(FileExistsError):export(out)


if __name__=='__main__':unittest.main()
