"""Original staged map/potential excerpt. No morph implies physical equivalence."""
import argparse
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw
from curves_models import square_map
from curves_keyframes import stroke, arrow
from render import text, smooth, BG, FG, MUTED, PANEL, CYAN, AMBER

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"same-looking-curves/map-study.json").read_text())


def validate(data):
    prior=0
    for c in data["cues"]:
        if c["start"]!=prior or c["end"]<=c["start"]:
            raise ValueError("Require contiguous positive cue intervals")
        if len(c["caption"].split())/(c["end"]-c["start"])>3:
            raise ValueError("Caption reading budget exceeded")
        if c["view"] not in ("input","map","potential","sources"):
            raise ValueError("Unknown view")
        prior=c["end"]
    if prior!=data["duration"] or data["fps"]!=24:
        raise ValueError("Study timing mismatch")
    mapping=next(c for c in data["cues"] if c["view"]=="map")
    if (data["motion_start"],data["motion_end"])!=(mapping["start"],mapping["end"]):
        raise ValueError("Parameter sweep must match map cue")
    return data


validate(DATA)


def cue_at(t,data=DATA):
    if not 0<=t<data["duration"]:
        raise ValueError("Outside study")
    return next(c for c in data["cues"] if c["start"]<=t<c["end"])


def parameter_at(t,data=DATA):
    cue_at(t,data)
    return -1.5+3*smooth((t-data["motion_start"])/(data["motion_end"]-data["motion_start"]))


def mapping_points(y):
    return (1,y),square_map(1,y)


def map_pixel(p,output=False):
    cx,scale=(940,35) if output else (325,72)
    return cx+scale*p[0],350-scale*p[1]


def potential_paths():
    # Each path is one branch, never joined across a singular parameter.
    contours=[];lines=[]
    for sign in (-1,1):
        ys=[-1.7+3.4*i/180 for i in range(181)]
        contours += [[(sign*math.sqrt(1+y*y),y) for y in ys],
                     [(y,sign*math.sqrt(1+y*y)) for y in ys]]
        for k in (-.6,.6):
            xs=[sign*(.3+1.7*i/180) for i in range(181)]
            lines.append([(x,k/x) for x in xs])
    return contours,lines


def axes(d,box,center,labels):
    d.rounded_rectangle(box,radius=12,fill=PANEL)
    x0,y0,x1,y1=box;cx,cy=center
    d.line((x0+16,cy,x1-16,cy),fill=MUTED)
    d.line((cx,y0+48,cx,y1-15),fill=MUTED)
    text(d,(x1-48,cy+8,40,40),labels[0],24,MUTED)
    text(d,(cx+10,y0+48,40,40),labels[1],24,MUTED)


def dot(d,p):
    d.ellipse((p[0]-7,p[1]-7,p[0]+7,p[1]+7),fill=AMBER,outline=FG,width=2)


def frame(t,data=DATA):
    cue=cue_at(t,data)
    image=Image.new("RGB",(1280,720),BG);d=ImageDraw.Draw(image)
    text(d,(40,18,1200,58),data["title"],36,bold=True)
    text(d,(40,78,1200,32),data["status"],19,MUTED)
    text(d,(40,123,1200,50),cue["heading"],32,bold=True)
    view=cue["view"]
    if view in ("input","map"):
        axes(d,(40,190,610,495),(325,350),("x","y"))
        text(d,(60,200,510,40),data["input_title"],26,bold=True)
        pts=[(1,-1.5+3*i/180) for i in range(181)]
        stroke(d,[map_pixel(p) for p in pts],CYAN,4)
        a,b=mapping_points(parameter_at(t,data))
        dot(d,map_pixel(a))
        text(d,(60,510,510,48),data["input_formula"],30)
        if view=="map":
            axes(d,(650,190,1240,495),(940,350),("u","v"))
            text(d,(670,200,520,40),data["output_title"],26,bold=True)
            stroke(d,[map_pixel(square_map(*p),True) for p in pts],CYAN,4)
            dot(d,map_pixel(b,True))
            text(d,(670,510,520,48),data["map_formula"],30)
        else:
            text(d,(680,270,510,55),"w = z²",38,bold=True)
            text(d,(680,345,510,48),data["hidden_title"],28,MUTED)
        text(d,(40,567,1200,38),data["scale_label"],23,MUTED)
    elif view=="potential":
        axes(d,(40,190,690,495),(360,350),("x",""))
        text(d,(350,198,40,42),"y",24,MUTED)
        text(d,(60,200,600,42),data["domain_title"],26,bold=True)
        project=lambda p:(360+60*p[0],350-60*p[1])
        contours,lines=potential_paths()
        for path in contours:
            stroke(d,[project(p) for p in path],AMBER,3,True)
        for path in lines:
            ps=[project(p) for p in path]
            stroke(d,ps,CYAN,3)
            arrow(d,ps[120],ps[105],CYAN)
        d.ellipse((354,344,366,356),fill=BG,outline=FG,width=2)
        text(d,(515,365,160,36),"E = 0",23,MUTED)
        for i,label in enumerate(data["potential_labels"]):
            text(d,(735,220+65*i,500,54),label,27,AMBER if i==2 else FG)
        text(d,(40,535,1200,50),data["potential_note"],25,MUTED)
    else:
        for i,line in enumerate(data["sources"]):
            text(d,(60,220+65*i,1160,54),line,27,FG if i<3 else MUTED)
    text(d,(40,615,1200,85),cue["caption"],28,bold=True)
    return image


def timestamp(seconds):
    ms=round(seconds*1000)
    return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}"


def vtt(data=DATA):
    return "WEBVTT\n\n"+"\n\n".join(
        f'{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["caption"]}'
        for c in data["cues"])+"\n"


if __name__=="__main__":
    from study_media import render_study
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(render_study(DATA,frame,vtt(),args.out,"map-study",
          ["map_study.py","study_media.py","curves_models.py","curves_keyframes.py",
           "render.py","same-looking-curves/map-study.json"],
          "fe359523a6c6c65c40c6f070bd7f4e1042816293"),indent=2))
