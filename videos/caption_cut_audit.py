"""Two-template encoded caption-region check; not OCR, speech sync or approval."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageChops, ImageStat, __version__ as pillow_version
import contrast_audit as colors
import encoded_caption_audit as identity
import source_only_review as source

BOX = (0, 590, 1280, 692)


def cuts():
    cues = source.render.caption_cues(source.lesson())
    result = []
    for i, (start, _, text) in enumerate(cues[1:], 1):
        frame = Fraction(str(start))*24
        if frame.denominator != 1:
            raise ValueError('Cue cut is not on this 24fps timeline')
        result.append(dict(frame=int(frame), seconds=float(start),
                           outgoing=cues[i-1][2], incoming=text))
    return result


def compare(decoded, expected, other):
    if any(im.mode != 'RGB' or im.size != decoded.size for im in (decoded, expected, other)):
        raise ValueError('Matching RGB crops required')
    # Restrict to exact foreground pixels in either template, not changing backgrounds.
    ep, op = expected.load(), other.load()
    mask = Image.new('L', decoded.size)
    mp = mask.load()
    count = 0
    for y in range(decoded.height):
        for x in range(decoded.width):
            if ep[x,y] == (244,247,252) or op[x,y] == (244,247,252):
                mp[x,y] = 255
                count += 1
    if not count or expected.tobytes() == other.tobytes():
        raise ValueError('Templates cannot distinguish the cut')
    def error(template):
        delta = ImageChops.difference(decoded, template)
        masked = Image.composite(delta, Image.new('RGB',delta.size),mask)
        return sum(ImageStat.Stat(masked).sum)/(3*count)
    correct, wrong = error(expected), error(other)
    return dict(mask_pixels=count, expected_mae=correct, other_mae=wrong,
                margin=wrong-correct, expected_is_closer=correct<wrong)


def audit(movie, out):
    colors.audit()  # pins twelve render sources, resolved lesson and VTT
    manifest = json.loads((colors.ROOT/'fft-latency/source-only-review/render-report.json').read_text())
    data = Path(movie).read_bytes()
    if identity.digest(data) != manifest['sha256'] or len(data) != manifest['size_bytes']:
        raise ValueError('Not the exact source-only movie')
    out = Path(out)
    if out.exists(): raise FileExistsError('Choose a new output directory')
    boundaries = cuts()
    numbers = sorted({n for cut in boundaries for n in (cut['frame']-1,cut['frame'])})
    stride = (BOX[2]-BOX[0])*(BOX[3]-BOX[1])*3
    frames, commands = {}, []
    # Small batches avoid deep select expressions in external FFmpeg builds.
    for offset in range(0,len(numbers),12):
        batch = numbers[offset:offset+12]
        expression = '+'.join(f'eq(n\\,{n})' for n in batch)
        command = ['ffmpeg','-v','error','-i','pipe:0','-vf',
                   f'select={expression},crop=1280:102:0:590',
                   '-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','pipe:1']
        raw = subprocess.run(command,input=data,capture_output=True,check=True).stdout
        if len(raw) != len(batch)*stride: raise ValueError('Wrong decoded crop count/geometry')
        commands.append(command)
        for i,n in enumerate(batch):
            frames[n] = Image.frombytes('RGB',(1280,102),raw[i*stride:(i+1)*stride])
    rows = []
    for cut in boundaries:
        n = cut['frame']
        before, after = (source.frame(k).crop(BOX) for k in (n-1,n))
        rows.append(dict(**cut, before=compare(frames[n-1],before,after),
                         after=compare(frames[n],after,before)))
    result = dict(source_commit='9d0280cfc7e914359b9bd7f0571bf61e4a390e8e',
                  movie_sha256=identity.digest(data), movie_bytes=len(data),
                  audit_source_sha256=colors.sha(__file__), pillow=pillow_version,
                  font_sha256=colors.sha(source.render.font(34).path),
                  ffmpeg=subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
                  crop_box_exclusive=BOX, decoder_commands=commands, boundaries=rows,
                  all_expected_closer=all(r[side]['expected_is_closer'] for r in rows for side in ('before','after')),
                  publication_approved=False,
                  limitations='36 caption-region samples at 18 cuts only. Source-defined foreground-union '
                  'mask and two-template relative pixel error, not OCR or semantic proof, exact pixel identity, '
                  'all-frame QA, full playback, device readability, speech synchronization or release approval.')
    out.mkdir(parents=True)
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('movie',type=Path)
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    result = audit(args.movie,args.out)
    print('18 caption cuts / 36 samples:',result['all_expected_closer'])
    if not result['all_expected_closer']: raise SystemExit('Inspect a caption cut mismatch')
