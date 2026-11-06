from copy import deepcopy
import math
from pathlib import Path
import unittest
from curves_episode import DATA,validate,cue_at,view_angles,project3,frame,vtt
from curves_models import camera
from camera_study import geometry
import map_study


class EpisodeTests(unittest.TestCase):
    def test_timeline_guards(self):
        validate(DATA)
        for c in DATA['cues']:
            self.assertIs(cue_at(c['start']),c)
            self.assertIs(cue_at(c['end']-1/24),c)
        for t in (-1,86,float('nan')):
            with self.assertRaises(ValueError):cue_at(t)
        for key in ('map_motion','camera_motion'):
            bad=deepcopy(DATA);bad[key][1]-=1
            with self.assertRaises(ValueError):validate(bad)
        self.assertEqual(vtt(),(Path(__file__).parent/'same-looking-curves/episode.vtt').read_text())

    def test_projection_and_camera_only_motion(self):
        before=geometry()
        for a in (0,.2,math.pi/6):
            for b in (0,math.pi/9):
                basis=[project3(p,a,b) for p in ((1,0,0),(0,1,0),(0,0,1))]
                self.assertAlmostEqual(sum(p[0]**2 for p in basis),1)
                self.assertAlmostEqual(sum(p[1]**2 for p in basis),1)
                self.assertAlmostEqual(sum(p[0]*p[1] for p in basis),0)
            for p in ((1,2,3),(-.2,.4,.9)):
                self.assertEqual(project3(p,a,0),camera(p,a))
        self.assertEqual(view_angles(48),(0,0))
        self.assertAlmostEqual(view_angles(64)[0],math.pi/6)
        self.assertNotEqual(view_angles(47)[1],0)
        self.assertEqual(geometry(),before)

    def test_no_study_mutation(self):
        original=deepcopy(map_study.DATA)
        for t in (6,12,22,30):frame(t)
        self.assertEqual(map_study.DATA,original)

    def test_dipole_stays_in_plot(self):
        for t in [38,47]+[48+i/4 for i in range(88)]:
            a,b=view_angles(t)
            for _,runs in geometry():
                for run in runs:
                    for p in run:
                        h,v=project3(p,a,b);x,y=460+230*h,340-230*v
                        self.assertTrue(60<x<735)
                        self.assertTrue(200<y<480)

    def test_all_frames_fit(self):
        for n in range(DATA['duration']*DATA['fps']):
            self.assertEqual(frame(n/24).size,(1280,720))
