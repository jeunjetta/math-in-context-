"""Local silent-study encoding and decoded QA, independent of lesson geometry."""
import hashlib
import json
from pathlib import Path
import subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parent


def render_study(data,frame_fn,captions,out,name,source_paths,baseline):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    movie=out/(name+"-draft.mp4")
    fps,duration=data["fps"],data["duration"];count=fps*duration
    process=subprocess.Popen(["ffmpeg","-v","error","-n","-f","rawvideo",
        "-pix_fmt","rgb24","-s","1280x720","-r",str(fps),"-i","pipe:0","-an",
        "-c:v","libx264","-preset","fast","-crf","21","-pix_fmt","yuv420p",
        "-movflags","+faststart",str(movie)],stdin=subprocess.PIPE)
    try:
        for n in range(count):
            process.stdin.write(frame_fn(n/fps).tobytes())
    except BaseException:
        process.kill()
        raise
    finally:
        process.stdin.close();process.wait()
    if process.returncode:
        raise RuntimeError("Encode failed; partial output is not reviewed")
    subprocess.run(["ffmpeg","-v","error","-i",str(movie),"-f","null","-"],check=True)
    facts=json.loads(subprocess.check_output(["ffprobe","-v","error",
        "-show_streams","-show_format","-of","json",str(movie)]))
    streams=facts["streams"]
    if len(streams)!=1 or streams[0]["codec_type"]!="video":
        raise ValueError("Only silent single-video studies supported")
    s=streams[0]
    if (s["width"],s["height"],s["r_frame_rate"],int(s["nb_frames"]))!=(
            1280,720,f"{fps}/1",count):
        raise ValueError("Unexpected media shape/timing")
    if abs(float(facts["format"]["duration"])-duration)>.001:
        raise ValueError("Unexpected duration")
    (out/(name+".vtt")).write_text(captions)
    indices={0,count-1}
    for cue in data["cues"]:
        start=cue["start"]*fps;indices.add(start)
        if start:indices.add(start-1)
        indices.add(round((cue["start"]+cue["end"])*fps/2))
    indices.update(range(0,count,2*fps))
    previews=out/"encoded";previews.mkdir()
    samples=[]
    for n in sorted(indices):
        raw=subprocess.check_output(["ffmpeg","-v","error","-i",str(movie),
             "-vf",f"select=eq(n\\,{n})","-frames:v","1","-f","rawvideo",
             "-pix_fmt","rgb24","pipe:1"])
        if len(raw)!=1280*720*3:raise ValueError("Missing decoded frame")
        im=Image.frombytes("RGB",(1280,720),raw)
        im.save(previews/f"frame-{n:04}.png")
        im.resize((640,360),Image.Resampling.LANCZOS).save(previews/f"frame-{n:04}-640.png")
        samples.append({"frame":n,"time_seconds":n/fps})
    report={"source_commit":baseline,"sha256":hashlib.sha256(movie.read_bytes()).hexdigest(),
            "duration":duration,"fps":fps,"frames":count,"audio":False,
            "complete_decode":True,"publication_approved":False,"samples":samples,
            "source_hashes":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_paths},
            "ffmpeg":subprocess.check_output(["ffmpeg","-version"]).decode().splitlines()[0]}
    (out/"render-report.json").write_text(json.dumps(report,indent=2)+"\n")
    return report
