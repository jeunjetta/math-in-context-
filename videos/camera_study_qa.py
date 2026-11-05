"""Decode sampled frames of this exact camera-study format; not release approval."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from PIL import Image
from camera_study import DATA, cue_at


def inspect(movie,out):
    movie,out=Path(movie),Path(out)
    facts=json.loads(subprocess.check_output(
        ["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(movie)]))
    if len(facts["streams"])!=1:
        raise ValueError("Silent single-stream study only")
    s=facts["streams"][0]
    if (s["codec_type"],s["width"],s["height"],s["r_frame_rate"],int(s["nb_frames"])) != (
            "video",1280,720,"24/1",768):
        raise ValueError("Wrong camera-study media geometry")
    if abs(float(facts["format"]["duration"])-32)>0.001:
        raise ValueError("Wrong duration")
    indices={0,767,14*24}
    for cue in DATA["cues"]:
        start=cue["start"]*24
        indices.add(start)
        if start:
            indices.add(start-1)
    indices.update(range(0,768,48))
    indices=sorted(indices)
    out.mkdir(parents=True,exist_ok=False)
    rows=[]
    for n in indices:
        raw=subprocess.check_output(["ffmpeg","-v","error","-i",str(movie),
              "-vf",f"select=eq(n\\,{n})","-frames:v","1","-f","rawvideo",
              "-pix_fmt","rgb24","pipe:1"])
        if len(raw)!=1280*720*3:
            raise ValueError("Missing decoded sample")
        image=Image.frombytes("RGB",(1280,720),raw)
        image.save(out/f"frame-{n:04}.png")
        image.resize((640,360),Image.Resampling.LANCZOS).save(out/f"frame-{n:04}-640.png")
        rows.append({"frame":n,"time_seconds":n/24,
                     "expected_caption":cue_at(n/24)["caption"]})
    report={"input_sha256":hashlib.sha256(movie.read_bytes()).hexdigest(),
            "samples":rows,"publication_approved":False,
            "note":"Expected captions are source metadata, not OCR; inspect decoded pixels."}
    (out/"samples.json").write_text(json.dumps(report,indent=2)+"\n")
    return report


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("movie",type=Path)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    result=inspect(args.movie,args.out)
    print(len(result["samples"]),"encoded samples exported; not publication approval.")
