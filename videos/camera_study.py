"""Silent camera-study excerpt; fixed 3D geometry, data-driven timing/captions."""
import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw
from curves_models import camera
from curves_keyframes import dipole_segments, stroke, arrow, MASK
from render import text, smooth, BG, FG, MUTED, CYAN, AMBER, PANEL

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT/"same-looking-curves/camera-study.json").read_text())


def validate(data):
    prior=0
    for cue in data["cues"]:
        if cue["start"] != prior or cue["end"] <= cue["start"]:
            raise ValueError("Cues must be contiguous and positive")
        if len(cue["caption"].split())/(cue["end"]-cue["start"]) > 3:
            raise ValueError("Reading budget exceeded")
        if cue["view"] not in ("camera","sources"):
            raise ValueError("Unknown view")
        prior=cue["end"]
    if prior != data["duration"] or data["fps"] != 24:
        raise ValueError("Duration/frame-rate mismatch")
    if not 0 <= data["rotation_start"] < data["rotation_end"] <= data["cues"][-1]["start"]:
        raise ValueError("Rotation must finish before source card")
    if data["max_angle_degrees"] != 30:
        raise ValueError("Copy and geometry are authored for a 30-degree turn")
    return data


validate(DATA)


def cue_at(t,data=DATA):
    if not 0 <= t < data["duration"]:
        raise ValueError("Time outside study")
    return next(c for c in data["cues"] if c["start"] <= t < c["end"])


def angle_at(t,data=DATA):
    cue_at(t,data)
    x=(t-data["rotation_start"])/(data["rotation_end"]-data["rotation_start"])
    return math.radians(data["max_angle_degrees"])*smooth(x)


@lru_cache
def geometry():
    # Immutable 3D positions; never regenerate/rotate the physical curves per frame.
    return tuple((phi,tuple(tuple(run) for run in dipole_segments(phi)))
                 for phi in (math.pi/3,-math.pi/3))


def frame(t,data=DATA):
    cue=cue_at(t,data)
    image=Image.new("RGB",(1280,720),BG)
    d=ImageDraw.Draw(image)
    text(d,(40,18,1200,60),data["title"],36,bold=True)
    text(d,(40,78,1200,34),data["status"],19,MUTED)
    text(d,(40,123,1200,50),cue["heading"],32,bold=True)
    if cue["view"] == "sources":
        for i,line in enumerate(data["source_lines"]):
            text(d,(60,205+57*i,1160,48),line,28,FG if i<3 else MUTED)
    else:
        d.rounded_rectangle((40,185,1240,475),radius=12,fill=PANEL)
        cx,cy,scale=570,325,330
        project=lambda p:(cx+scale*p[0],cy-scale*p[1])
        d.line((70,cy,1200,cy),fill=MUTED)
        d.line((cx,202,cx,458),fill=MUTED)
        text(d,(1170,cy+10,50,42),"h",26,MUTED)
        text(d,(cx+10,199,45,42),"z",26,MUTED)
        text(d,(890,215,320,94),data["axis_note"],22,MUTED)
        alpha=angle_at(t,data)
        for j,(_,runs) in enumerate(geometry()):
            color=CYAN if j==0 else AMBER
            for run in runs:
                points=[project(camera(p,alpha)) for p in run]
                stroke(d,points,color,4,j==1)
                k=len(points)//3
                arrow(d,points[k],points[k+8],color)
        rad=scale*MASK
        d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),fill=BG,outline=FG,width=2)
        text(d,(80,500,1100,45),data["legend"],28)
        text(d,(80,545,1100,42),data["mask_label"]+" · "+data["projection_label"],24,MUTED)
    # One cue source drives the burned reading track and exported VTT.
    text(d,(40,610,1200,90),cue["caption"],28,bold=True)
    return image


def timestamp(seconds):
    millis=round(seconds*1000)
    return f"{millis//3600000:02}:{millis//60000%60:02}:{millis//1000%60:02}.{millis%1000:03}"


def vtt(data=DATA):
    return "WEBVTT\n\n"+"\n\n".join(
        f'{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["caption"]}'
        for c in data["cues"])+"\n"


def render(out):
    out=Path(out)
    out.mkdir(parents=True,exist_ok=False)
    movie=out/"camera-study-draft.mp4"
    command=["ffmpeg","-v","error","-n","-f","rawvideo","-pix_fmt","rgb24",
             "-s","1280x720","-r",str(DATA["fps"]),"-i","pipe:0","-an",
             "-c:v","libx264","-preset","fast","-crf","21","-pix_fmt","yuv420p",
             "-movflags","+faststart",str(movie)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for i in range(DATA["duration"]*DATA["fps"]):
            process.stdin.write(frame(i/DATA["fps"]).tobytes())
    except BaseException:
        process.kill()
        raise
    finally:
        process.stdin.close()
        process.wait()
    if process.returncode:
        raise RuntimeError("FFmpeg encode failed; partial output is not approved")
    (out/"camera-study.vtt").write_text(vtt())
    subprocess.run(["ffmpeg","-v","error","-i",str(movie),"-f","null","-"],check=True)
    facts=json.loads(subprocess.check_output(
        ["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(movie)]))
    streams=facts["streams"]
    if len(streams)!=1 or streams[0]["codec_type"]!="video":
        raise ValueError("Expected one silent video stream")
    stream=streams[0]
    if (stream["width"],stream["height"],stream["r_frame_rate"],int(stream["nb_frames"])) != (
            1280,720,"24/1",DATA["duration"]*DATA["fps"]):
        raise ValueError("Unexpected media geometry/timing")
    if abs(float(facts["format"]["duration"])-DATA["duration"])>0.001:
        raise ValueError("Unexpected media duration")
    report={"source_commit":"12745869662ffd0093ef7e933d428fc4b56cc519",
            "sha256":hashlib.sha256(movie.read_bytes()).hexdigest(),
            "duration":DATA["duration"],"frames":DATA["duration"]*DATA["fps"],"audio":False,
            "complete_decode":True,"publication_approved":False,
            "source_hashes":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
                             for p in ("camera_study.py","curves_models.py",
                                       "curves_keyframes.py","render.py",
                                       "same-looking-curves/camera-study.json")},
            "ffmpeg":subprocess.check_output(["ffmpeg","-version"]).decode().splitlines()[0]}
    (out/"render-report.json").write_text(json.dumps(report,indent=2)+"\n")
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(render(args.out),indent=2))
