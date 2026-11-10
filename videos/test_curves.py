from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path
import unittest

from curves_models import (square_map, potential, electric_field, dipole_field,
                           dipole_line, dipole_line_tangent, camera)


class CurvesTests(unittest.TestCase):
    def test_map_and_potential_are_different_objects(self):
        for x,y in product([F(-2),F(-1,2),F(0),F(1),F(3,2)],repeat=2):
            u,v = square_map(x,y)
            self.assertEqual(u, potential(x,y))
            # Central differences are exact for these quadratic polynomials.
            h=F(1,7)
            ux=(square_map(x+h,y)[0]-square_map(x-h,y)[0])/(2*h)
            uy=(square_map(x,y+h)[0]-square_map(x,y-h)[0])/(2*h)
            vx=(square_map(x+h,y)[1]-square_map(x-h,y)[1])/(2*h)
            vy=(square_map(x,y+h)[1]-square_map(x,y-h)[1])/(2*h)
            self.assertEqual(ux,vy)
            self.assertEqual(uy,-vx)
            lap=(potential(x+h,y)+potential(x-h,y)+potential(x,y+h)
                 +potential(x,y-h)-4*potential(x,y))/(h*h)
            self.assertEqual(lap,0)
            grad_v=((potential(x+h,y)-potential(x-h,y))/(2*h),
                    (potential(x,y+h)-potential(x,y-h))/(2*h))
            tangent_v_level = (2*y,2*x)
            field = electric_field(x,y)
            self.assertEqual(sum(a*b for a,b in zip(field,tangent_v_level)),0)
            self.assertEqual(field, tuple(-v for v in grad_v))
            # xy is constant along E; do not confuse its curves with V=constant.
            self.assertEqual(y*field[0]+x*field[1],0)
        for y in [F(-2),F(-1),F(0),F(1,2),F(2)]:
            u,v = square_map(F(1),y)
            self.assertEqual(u,1-v*v/4)

    def test_dipole_curves_are_tangent_to_field(self):
        for theta,phi,L in product((0.4,0.9,math.pi/2,2.1,2.7), (0,math.pi/3,-math.pi/3), (0.8,1.5)):
            point = dipole_line(theta,phi,L)
            b = dipole_field(*point)
            tangent = dipole_line_tangent(theta,phi,L)
            cross = tuple(tangent[(i+1)%3]*b[(i+2)%3]-tangent[(i+2)%3]*b[(i+1)%3] for i in range(3))
            norm = math.sqrt(sum(v*v for v in tangent)*sum(v*v for v in b))
            self.assertLess(math.sqrt(sum(v*v for v in cross))/norm,1e-12)
            self.assertGreater(sum(a*b for a,b in zip(tangent,b)),0)
        self.assertEqual(dipole_field(0,0,1),(0,0,2))
        self.assertEqual(dipole_field(1,0,0),(0,0,-1))

    def test_camera_can_hide_depth_without_changing_curves(self):
        for theta in (0.5,1,math.pi/2,2,2.5):
            a = dipole_line(theta,math.pi/3)
            b = dipole_line(theta,-math.pi/3)
            self.assertNotEqual(a[1],b[1])
            self.assertEqual(camera(a),camera(b))
            self.assertGreater(abs(camera(a,math.pi/6)[0]-camera(b,math.pi/6)[0]),0.01)

    def test_singular_source_and_invalid_curve_inputs_rejected(self):
        for point in ((0,0,0),(math.inf,0,0),(math.nan,0,1)):
            with self.assertRaises(ValueError):
                dipole_field(*point)
        for theta,phi,L in ((0,0,1),(math.pi,0,1),(1,0,0),(1,math.nan,1)):
            with self.assertRaises(ValueError):
                dipole_line(theta,phi,L)

    def test_story_has_one_contiguous_unrecorded_bite(self):
        path=Path(__file__).parent / "same-looking-curves/script.json"
        data=json.loads(path.read_text())
        self.assertEqual(data["duration_seconds"],82)
        self.assertIn("UNRECORDED",data["status"])
        prior=0
        for scene in data["scenes"]:
            self.assertEqual(scene["start"],prior)
            self.assertGreater(scene["end"],scene["start"])
            self.assertLessEqual(len(scene["script"].split())/(scene["end"]-scene["start"]),3)
            self.assertTrue(scene["labels"] and scene["visual"])
            prior=scene["end"]
        self.assertEqual(prior,82)


if __name__ == "__main__":
    unittest.main()
