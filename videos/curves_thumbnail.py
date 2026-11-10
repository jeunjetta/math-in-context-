"""Original scientific thumbnail, not a movie frame or publication action."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, __version__ as pillow_version
from curves_models import square_map, camera
from curves_keyframes import dipole_segments, stroke
from render import BG, FG, CYAN, AMBER, PANEL, font

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT / 'same-looking-curves'
DATA = json.loads((FOLDER / 'thumbnail.json').read_text())
SIZE = (1280, 720)


def validate(data=DATA):
    candidate = json.loads((FOLDER / 'review-candidate.json').read_text())
    if (data['candidate'] != candidate['candidate'] or
            data['media_sha256'] != candidate['sha256'] or
            data['publication_approved'] is not False):
        raise ValueError('Thumbnail must identify the unapproved frozen candidate')
    if len(data['headline']) != 2 or len(data['labels']) != 3 or len(data['notes']) != 3:
        raise ValueError('Review layout before changing copy structure')


def label(draw, box, value, size, color=FG):
    """Single line, optical top alignment; actual glyph bounds must fit."""
    x,y,w,h = box
    face = font(size, True)
    left,top,right,bottom = draw.textbbox((0,0),value,font=face)
    if right-left > w or bottom-top > h:
        raise ValueError('Thumbnail text clips: '+value)
    draw.text((x-left,y-top),value,font=face,fill=color)
    return (x,y,x+right-left,y+bottom-top)


def geometry():
    """Panel-local coordinates, derived from the retained episode models."""
    mapped = [square_map(1,-1.3+2.6*i/200) for i in range(201)]
    # Regular V=1 contour: x=sqrt(1+y²); no field direction arrow.
    contour = [(math.sqrt(1+y*y),y) for y in [-1.1+2.2*i/200 for i in range(201)]]
    dipole = [(phi,run) for phi in (math.pi/3,-math.pi/3)
              for run in dipole_segments(phi)]
    return mapped,contour,dipole


def plot_points():
    mapped,contour,dipole = geometry()
    first = [(222+72*u,468-24*v) for u,v in mapped]
    second = [(575+60*x,468-58*y) for x,y in contour]
    third = [(phi,[(1060+135*h,468-135*z) for h,z in
                   [camera(p,math.pi/9) for p in run]]) for phi,run in dipole]
    return first,second,third


def image(data=DATA):
    validate(data)
    im = Image.new('RGB',SIZE,BG);draw = ImageDraw.Draw(im)
    label(draw,(48,25,1184,40),data['eyebrow'],30)
    label(draw,(48,92,1184,110),data['headline'][0],104)
    label(draw,(48,214,1184,84),data['headline'][1],78,CYAN)
    for i,x in enumerate((48,456,864)):
        draw.rounded_rectangle((x,326,x+368,618),radius=18,fill=PANEL)
        label(draw,(x+20,347,328,44),data['labels'][i],36)
        label(draw,(x+20,557,328,44),data['notes'][i],34)
    first,second,third = plot_points()
    stroke(draw,first,CYAN,8)
    for p in (first[35],first[155]):
        draw.ellipse((p[0]-8,p[1]-8,p[0]+8,p[1]+8),fill=FG)
    stroke(draw,second,AMBER,8,True)
    for phi,points in third:
        stroke(draw,points,CYAN if phi>0 else AMBER,8,phi<0)
    # The physical r<0.15 exclusion was applied in geometry before projection.
    # This screen disc also conservatively occludes retained points; not a magnet.
    draw.ellipse((1039.75,447.75,1080.25,488.25),fill=BG,outline=FG,width=2)
    label(draw,(48,658,1184,38),data['footer'],28)
    return im


def export(out):
    out=Path(out)
    if out.exists(): raise FileExistsError('Use a new output directory')
    im=image()  # Validate/render before creating output; no partial copy on fit failure.
    out.mkdir(parents=True)
    files={}
    for width in (1280,640,320):
        target=out/f'thumbnail-{width}.png'
        im.resize((width,width*9//16),Image.Resampling.LANCZOS).save(target)
        files[target.name]=hashlib.sha256(target.read_bytes()).hexdigest()
    report={'candidate':DATA['candidate'],'media_sha256':DATA['media_sha256'],
            'publication_approved':False,'pillow':pillow_version,'images':files,
            'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                for name in ('curves_thumbnail.py','curves_models.py','curves_keyframes.py','render.py',
                             'same-looking-curves/thumbnail.json')},
            'font':str(font(36,True).path),
            'font_sha256':hashlib.sha256(Path(font(36,True).path).read_bytes()).hexdigest()}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    export(parser.parse_args().out)
