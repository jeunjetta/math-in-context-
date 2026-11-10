from copy import deepcopy
import math
from pathlib import Path
import unittest
from camera_study import DATA, validate, cue_at, angle_at, geometry, frame, vtt
from curves_models import camera


class CameraStudyTests(unittest.TestCase):
    def test_cues_and_caption_file(self):
        validate(DATA)
        self.assertEqual(vtt(),(Path(__file__).parent/"same-looking-curves/camera-study.vtt").read_text())
        for cue in DATA["cues"]:
            self.assertIs(cue_at(cue["start"]),cue)
            self.assertIs(cue_at(cue["end"]-1/24),cue)
        for t in (-1,32,float("nan")):
            with self.assertRaises(ValueError):
                cue_at(t)

    def test_angle_continuity_and_fixed_geometry(self):
        before=geometry()
        self.assertEqual(angle_at(0),0)
        self.assertEqual(angle_at(10),0)
        self.assertAlmostEqual(angle_at(14),math.pi/12)
        self.assertAlmostEqual(angle_at(18),math.pi/6)
        angles=[angle_at(i/24) for i in range(768)]
        self.assertEqual(angles,sorted(angles))
        self.assertIs(before,geometry())
        a=before[0][1][0];b=before[1][1][0]
        for p,q in zip(a,b):
            self.assertEqual(camera(p,0),camera(q,0))
            self.assertAlmostEqual(camera(q,math.pi/6)[0],0,places=14)
            self.assertGreaterEqual(sum(x*x for x in p),.15**2)

    def test_all_frames_fit(self):
        for i in range(768):
            self.assertEqual(frame(i/24).size,(1280,720))

    def test_bad_timing_rejected(self):
        for key,value in (("rotation_end",9),("duration",31),("max_angle_degrees",60)):
            data=deepcopy(DATA);data[key]=value
            with self.assertRaises(ValueError):
                validate(data)
