from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import unittest
from map_study import (DATA,validate,cue_at,parameter_at,mapping_points,map_pixel,
                       potential_paths,frame,vtt)
from curves_models import potential,electric_field


class MapStudyTests(unittest.TestCase):
    def test_map_correspondence_and_bounds(self):
        for i in range(241):
            y=F(-3,2)+F(i,80)
            a,b=mapping_points(y)
            self.assertEqual(b,(1-y*y,2*y))
            self.assertEqual(b[0],1-b[1]**2/4)
            for p,output,box in ((a,False,(40,190,610,495)),(b,True,(650,190,1240,495))):
                x,yy=map_pixel(p,output)
                self.assertTrue(box[0]+15<x<box[2]-15)
                self.assertTrue(box[1]+48<yy<box[3]-15)

    def test_contours_field_lines_and_direction(self):
        contours,lines=potential_paths()
        for path in contours:
            for x,y in path:
                self.assertAlmostEqual(abs(potential(x,y)),1,places=12)
        for path in lines:
            for x,y in path:
                self.assertAlmostEqual(abs(x*y),.6,places=12)
                ex,ey=electric_field(x,y)
                self.assertAlmostEqual(y*ex+x*ey,0,places=12)
            x,y=path[120];dx=path[105][0]-x;dy=path[105][1]-y
            ex,ey=electric_field(x,y)
            self.assertGreater(ex*dx+ey*dy,0)

    def test_cues_and_parameter(self):
        validate(DATA)
        for c in DATA["cues"]:
            self.assertIs(cue_at(c["start"]),c)
            self.assertIs(cue_at(c["end"]-1/24),c)
        self.assertEqual(parameter_at(6),-1.5)
        self.assertEqual(parameter_at(10),0)
        self.assertEqual(parameter_at(14),1.5)
        self.assertEqual(vtt(),(Path(__file__).parent/"same-looking-curves/map-study.vtt").read_text())
        for t in (-1,32,float("nan")):
            with self.assertRaises(ValueError):cue_at(t)
        data=deepcopy(DATA);data["motion_end"]=13
        with self.assertRaises(ValueError):validate(data)

    def test_all_frames_fit(self):
        for n in range(768):
            self.assertEqual(frame(n/24).size,(1280,720))
