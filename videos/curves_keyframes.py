"""Original preproduction stills; no source artwork, model API or telemetry."""
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw
from curves_models import square_map, dipole_line, camera
from render import text, BG, FG, MUTED, CYAN, AMBER, PANEL

ROOT = Path(__file__).resolve().parent
COPY = json.loads((ROOT / "same-looking-curves/keyframes.json").read_text())
SIZE = (1280, 720)
MASK = 0.15
OUTPUT_SCALE = 30


def dipole_segments(phi, extent=1, mask=MASK, samples=401):
    """Split before projection: never join through the excluded source sphere."""
    if not (0 < mask < extent and samples >= 3):
        raise ValueError("Require 0 < mask < extent and samples >= 3")
    segments, run = [], []
    for i in range(1, samples):
        theta = math.pi*i/samples
        p = dipole_line(theta, phi, extent)
        if math.sqrt(sum(v*v for v in p)) >= mask:
            run.append(p)
        elif run:
            segments.append(run)
            run = []
    if run:
        segments.append(run)
    return segments


def stroke(draw, points, color, width=3, dashed=False):
    for i in range(len(points)-1):
        if not dashed or i % 12 < 6:
            draw.line((points[i], points[i+1]), fill=color, width=width)


def arrow(draw, p, q, color):
    draw.line((p, q), fill=color, width=3)
    angle = math.atan2(q[1]-p[1], q[0]-p[0])
    wing = [(q[0]-11*math.cos(angle+a), q[1]-11*math.sin(angle+a))
            for a in (-0.5, 0.5)]
    draw.polygon([q, *wing], fill=color)


def canvas():
    image = Image.new("RGB", SIZE, BG)
    d = ImageDraw.Draw(image)
    text(d, (36, 18, 1210, 60), COPY["title"], 38, bold=True)
    text(d, (36, 78, 1210, 35), COPY["draft"], 19, MUTED)
    return image, d


def plot(draw, box, coords, scale, labels):
    x, y, w, h = box
    draw.rounded_rectangle(box, radius=12, fill=PANEL)
    cx, cy = coords
    draw.line((x+18, cy, w-18, cy), fill=MUTED, width=1)
    draw.line((cx, y+18, cx, h-18), fill=MUTED, width=1)
    text(draw, (w-48, cy+5, 42, 34), labels[0], 22, MUTED)
    text(draw, (cx+8, y+5, 40, 34), labels[1], 22, MUTED)
    return lambda a,b: (cx+scale*a, cy-scale*b)


def mapping():
    image, d = canvas()
    centers = (225, 640, 1055)
    for i,cx in enumerate(centers):
        text(d, (cx-190, 125, 380, 38), COPY["mapping_titles"][i], 26, bold=True)
    a = plot(d, (36, 180, 414, 460), (225, 320), 57, ("x","y"))
    b = plot(d, (451, 180, 829, 460), (640, 320), OUTPUT_SCALE, ("u","v"))
    c = plot(d, (866, 180, 1244, 460), (1055, 320), 57, ("x","y"))
    line = [(1, -2+4*i/200) for i in range(201)]
    stroke(d, [a(*p) for p in line], CYAN, 4)
    stroke(d, [b(*square_map(*p)) for p in line], CYAN, 4)
    for i in (40,140):
        arrow(d, a(*line[i]), a(*line[i+10]), CYAN)
        arrow(d, b(*square_map(*line[i])), b(*square_map(*line[i+10])), CYAN)
    # E-field integral curves xy=k: direction E=(-2x,2y), so x decreases if x>0.
    for k in (-0.6, 0.6):
        for sign in (-1,1):
            xs = [sign*(0.3+1.7*i/180) for i in range(181)]
            ps = [c(x,k/x) for x in xs]
            stroke(d, ps, CYAN, 3)
            # direction along decreasing x for x>0, increasing x for x<0
            arrow(d, ps[120], ps[105], CYAN)
    # V-contours x²-y²=±1, away from the zero-gradient origin.
    for sign in (-1,1):
        ys = [-1.7+3.4*i/180 for i in range(181)]
        stroke(d, [c(sign*math.sqrt(1+y*y), y) for y in ys], AMBER, 3, True)
        stroke(d, [c(y, sign*math.sqrt(1+y*y)) for y in ys], AMBER, 3, True)
    for project in (a,c):
        p = project(0,0)
        d.ellipse((p[0]-5,p[1]-5,p[0]+5,p[1]+5), fill=FG)
    for i,cx in enumerate(centers):
        text(d, (cx-190, 477, 380, 90), COPY["mapping_notes"][i], 24)
    text(d, (451, 548, 378, 30), "Plot scales differ.", 19, MUTED)
    text(d, (36, 580, 1200, 46), COPY["mapping_footer"], 32, bold=True)
    text(d, (36, 628, 1200, 72),
         "Right: dashed = V contours; solid + arrows = E field lines.\nAt origin: map derivative = 0; E = 0. Shapes do not establish common physics.",
         23, MUTED)
    return image


def dipole():
    image, d = canvas()
    for i,alpha in enumerate((0,math.pi/6)):
        cx = 330+620*i
        text(d, (cx-275, 125, 550, 40), COPY["dipole_titles"][i], 27, bold=True)
        p = plot(d, (cx-275,180,cx+275,465), (cx,325), 230, ("h","z"))
        for phi,color,dashed in ((math.pi/3,CYAN,False),(-math.pi/3,AMBER,True)):
            for segment in dipole_segments(phi):
                pixels = [p(*camera(point,alpha)) for point in segment]
                stroke(d,pixels,color,4,dashed)
                # B points along increasing colatitude on these chosen lines.
                j=len(pixels)//3
                arrow(d,pixels[j],pixels[j+8],color)
        # Conservative projected source disc, not a physical solid magnet.
        radius=230*MASK
        d.ellipse((cx-radius,325-radius,cx+radius,325+radius),fill=BG,outline=FG,width=2)
        text(d,(cx-275,477,550,42),COPY["dipole_notes"][i],24)
    text(d,(36,540,1200,42),COPY["dipole_footer"],30,bold=True)
    text(d,(36,594,1200,105),
         "Solid: φ = +60°; dashed: φ = −60° (edge-on at right). r = sin²θ.\nIdeal +z dipole. Source r < 0.15 masked; no line joins through it.\nOrthographic, NOT stereographic. h = horizontal screen coordinate.",
         23,MUTED)
    return image


def export(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    for name, image in (("mapping",mapping()),("dipole",dipole())):
        image.save(out / (name+".png"))
        image.resize((640,360),Image.Resampling.LANCZOS).save(out / (name+"-640.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    export(parser.parse_args().out)
