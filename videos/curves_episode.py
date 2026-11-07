"""Integrated silent rough cut; no physical equivalence implied by transitions."""
import argparse
from copy import deepcopy
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw
import map_study
from camera_study import geometry
from curves_keyframes import stroke, arrow, MASK
from render import text, smooth, BG, FG, MUTED, PANEL, CYAN, AMBER
from study_media import render_study

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'same-looking-curves/episode.json').read_text())
BASELINE='e30ea2a1c6e640c9de87aae2e833d4e47542b557'


def validate(data):
    prior=0
    expected=['intro','input','map','potential','potential','orientation',
              'camera','camera','camera','question','sources']
    if [c['view'] for c in data['cues']]!=expected:
        raise ValueError('Authored object/transition order changed')
    for c in data['cues']:
        if c['start']!=prior or c['end']<=prior:
            raise ValueError('Noncontiguous reading track')
        if len(c['caption'].split())/(c['end']-c['start'])>3:
            raise ValueError('Reading budget exceeded')
        prior=c['end']
    if not 60<=prior<=90 or prior!=data['duration'] or data['fps']!=24:
        raise ValueError('Episode duration/frame-rate mismatch')
    if data['map_motion']!=[data['cues'][2]['start'],data['cues'][2]['end']]:
        raise ValueError('Map sweep must match its cue')
    if data['camera_motion']!=[data['cues'][7]['start'],data['cues'][7]['end']]:
        raise ValueError('Camera turn must match its cue')
    return data


validate(DATA)


def cue_at(t,data=DATA):
    if not 0<=t<data['duration']:
        raise ValueError('Outside episode')
    return next(c for c in data['cues'] if c['start']<=t<c['end'])


def view_angles(t,data=DATA):
    cue=cue_at(t,data)
    if cue['view']=='orientation':
        return math.pi/9,math.pi/9
    a,b=data['camera_motion']
    return math.pi/6*smooth((t-a)/(b-a)),0


def project3(p,alpha,beta):
    # Two orthonormal camera rows. Beta=0 recovers the earlier x/z camera.
    x,y,z=p
    return (x*math.cos(alpha)+y*math.sin(alpha),
            z*math.cos(beta)+(-x*math.sin(alpha)+y*math.cos(alpha))*math.sin(beta))


def map_frame(t,cue,data):
    # Fresh configuration; never mutate either study's lesson/reading track.
    config=deepcopy(map_study.DATA)
    config.update(title=data['title'],status=data['status'],duration=data['duration'],
                  motion_start=data['map_motion'][0],motion_end=data['map_motion'][1],
                  cues=[dict(cue,start=0,end=data['duration'])])
    return map_study.frame(t,config)


def orientation_key(t,data=DATA):
    alpha,beta=view_angles(t,data)
    layout=data['dipole_layout'];origin=tuple(layout['axis_origin'])
    result=[]
    for label,p,offset in [('x',(1,0,0),(8,0)),('y',(0,1,0),(-24,18)),('z',(0,0,1),(8,-8))]:
        h,v=project3(p,alpha,beta)
        end=(origin[0]+layout['axis_length']*h,origin[1]-layout['axis_length']*v)
        box=(end[0]+offset[0],end[1]+offset[1],45,41)
        result.append((label,origin,end,box,abs(h)+abs(v)<1e-10))
    return result


def draw_dipole(d,t,data):
    alpha,beta=view_angles(t,data)
    d.rounded_rectangle((40,190,1240,490),radius=12,fill=PANEL)
    cx,cy,scale=460,340,230
    project=lambda p:(cx+scale*p[0],cy-scale*p[1])
    for j,(_,runs) in enumerate(geometry()):
        color=CYAN if j==0 else AMBER
        for run in runs:
            ps=[project(project3(p,alpha,beta)) for p in run]
            stroke(d,ps,color,4,j==1)
            k=len(ps)//3;arrow(d,ps[k],ps[k+8],color)
    rad=scale*MASK
    d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),fill=BG,outline=FG,width=2)
    # A separate orientation key shows projected +axis directions, not field B.
    for label,origin,end,box,collapsed in orientation_key(t,data):
        if collapsed:
            d.ellipse((origin[0]-4,origin[1]-4,origin[0]+4,origin[1]+4),outline=MUTED)
        else:
            arrow(d,origin,end,MUTED)
        text(d,box,label,data['dipole_layout']['axis_font'],MUTED)
    for i,label in enumerate(data['dipole_labels'][:2]):
        text(d,(760,210+50*i,450,44),label,data['dipole_layout']['label_font'],FG)
    note=data['projection_notes'][0 if beta else (1 if alpha==0 else 2)]
    text(d,(70,500,1140,43),data['dipole_labels'][2]+' · '+data['dipole_labels'][3],28)
    text(d,(70,548,1140,55),note+' · '+data['projection_kind'],27,MUTED)


def frame(t,data=DATA):
    cue=cue_at(t,data)
    if cue['view'] in ('input','map','potential'):
        return map_frame(t,cue,data)
    im=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(im)
    text(d,(40,18,1200,58),data['title'],36,bold=True)
    text(d,(40,78,1200,32),data['status'],19,MUTED)
    text(d,(40,123,1200,50),cue['heading'],32,bold=True)
    if cue['view'] in ('orientation','camera'):
        draw_dipole(d,t,data)
    elif cue['view']=='sources':
        for i,line in enumerate(data['sources']):
            text(d,(60,215+70*i,1160,55),line,28,FG if i<3 else MUTED)
    else:
        for i,line in enumerate(data['intro_labels']):
            y=215+105*i
            d.rounded_rectangle((40,y,1240,y+80),radius=12,fill=PANEL)
            text(d,(70,y+15,1140,58),line,32)
    text(d,(40,615,1200,85),cue['caption'],28,bold=True)
    return im


def vtt(data=DATA):
    return map_study.vtt(data)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    sources=['curves_episode.py','map_study.py','camera_study.py','curves_models.py',
             'curves_keyframes.py','render.py','lesson_model.py','study_media.py',
             'same-looking-curves/episode.json','same-looking-curves/map-study.json',
             'same-looking-curves/camera-study.json','fft-latency/lesson.json']
    print(json.dumps(render_study(DATA,frame,vtt(),args.out,'curves-episode',sources,BASELINE),indent=2))
