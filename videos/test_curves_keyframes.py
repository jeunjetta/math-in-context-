import math
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from curves_keyframes import dipole_segments, mapping, dipole, export, MASK, OUTPUT_SCALE
from curves_models import camera, square_map


class KeyframeTests(unittest.TestCase):
    def test_mapped_curve_inside_plot(self):
        for i in range(201):
            u,v=square_map(1,-2+4*i/200)
            x,y=640+OUTPUT_SCALE*u,320-OUTPUT_SCALE*v
            self.assertTrue(451+18 <= x <= 829-18)
            self.assertTrue(180+18 <= y <= 460-18)

    def test_source_split_and_domains(self):
        for phi in (math.pi/3,-math.pi/3):
            runs = dipole_segments(phi)
            self.assertEqual(len(runs),1)
            for p in runs[0]:
                self.assertGreaterEqual(sum(v*v for v in p),MASK**2)
            self.assertGreater(runs[0][0][2],0)
            self.assertLess(runs[0][-1][2],0)
        for mask in (0,1,2):
            with self.assertRaises(ValueError):
                dipole_segments(0,mask=mask)

    def test_same_geometry_different_camera(self):
        a=dipole_segments(math.pi/3)[0]
        b=dipole_segments(-math.pi/3)[0]
        for p,q in zip(a,b):
            self.assertEqual(camera(p),camera(q))
        self.assertTrue(any(abs(camera(p,math.pi/6)[0]-camera(q,math.pi/6)[0])>.1
                            for p,q in zip(a,b)))

    def test_layout_and_export_guards(self):
        for fn in (mapping,dipole):
            self.assertEqual(fn().size,(1280,720))  # text() rejects overflow
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"frames"
            export(out)
            for name in ("mapping","dipole"):
                with Image.open(out/(name+"-640.png")) as im:
                    self.assertEqual(im.size,(640,360))
            with self.assertRaises(FileExistsError):
                export(out)
