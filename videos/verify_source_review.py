"""Verify the exact full source-only review copy locally; never approve it."""
import argparse
import json
from pathlib import Path
import subprocess

from qa import validate_media
from verify_source_ending import sha

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT/'fft-latency/source-only-review'
MANIFEST_SHA = '2456b23798529acc23853d5bdb5ac521b0ef5d3fdf08160bc51e7ee122a5e13a'


def load_report():
    path = FOLDER/'render-report.json'
    if sha(path) != MANIFEST_SHA:
        raise ValueError('Render manifest changed; re-review exact-copy scope')
    return json.loads(path.read_text())


def verify_inputs(video, captions, report, root=ROOT):
    """Trusted repository evidence; local input bytes checked before decoding."""
    if (report['publication_approved'] is not False
            or report['status'] != 'unadopted full source-only review'
            or report['filename'] != 'fft-source-only-review.mp4'
            or report['media'] != dict(codec='h264',width=1280,height=720,fps=24,
                frames=1920,duration=80.0,audio_streams=0,timestamps_verified=True)):
        raise ValueError('Expected the unadopted silent full source-only review')
    for path, digest, role in ((video, report['sha256'], 'Movie'),
                               (captions, report['captions_sha256'], 'Captions')):
        if not Path(path).is_file() or sha(path) != digest:
            raise ValueError(role+' bytes do not match the source-only review')
    if Path(video).stat().st_size != report['size_bytes']:
        raise ValueError('Movie size mismatch')
    resolved = root/'fft-latency/source-only-review/resolved-lesson.json'
    if sha(resolved) != report['resolved_lesson_sha256']:
        raise ValueError('Resolved lesson changed')
    if not report['source_hashes']:
        raise ValueError('Missing render source evidence')
    for relative, digest in report['source_hashes'].items():
        source = (root/relative).resolve()
        if not source.is_relative_to(root.resolve()):
            raise ValueError('Source evidence must stay inside videos/')
        if not source.is_file() or sha(source) != digest:
            raise ValueError('Render source drift: '+relative)


def verify(video, captions=None):
    # Resolve to an existing local file before passing anything to FFmpeg.
    video = Path(video).resolve()
    captions = Path(captions or FOLDER/'fft-source-only-review.vtt').resolve()
    report = load_report()
    verify_inputs(video, captions, report)
    probe = json.loads(subprocess.check_output([
        'ffprobe','-v','error','-show_frames','-show_streams','-show_format',
        '-of','json',str(video)]))
    if len(probe['streams']) != 1:
        raise ValueError('Expected exactly one video stream and no other streams')
    media = validate_media(probe, dict(width=1280,height=720,fps=24,duration=80))
    if media['codec'] != 'h264':
        raise ValueError('Unexpected codec')
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),
                    '-map','0:v:0','-f','null','-'],check=True)
    # Do not report success if inputs/evidence changed during the check.
    if load_report() != report:
        raise ValueError('Manifest changed during verification')
    verify_inputs(video, captions, report)
    return dict(status='exact full source-only review bytes and technical checks passed',
        filename=report['filename'],sha256=sha(video),size_bytes=video.stat().st_size,
        captions_sha256=sha(captions),render_source_commit=report['source_commit'],
        render_report_sha256=MANIFEST_SHA,verifier_sha256=sha(Path(__file__)),
        verifier_dependencies={p:sha(ROOT/p) for p in ('qa.py','verify_source_ending.py')},
        media=media,full_decode_completed=True,source_files_checked=len(report['source_hashes']),
        tools={name:subprocess.check_output([name,'-version'],text=True).splitlines()[0]
               for name in ('ffmpeg','ffprobe')},publication_approved=False,
        limitations='Trusted repository identity, not a digital signature. No new render, OCR, '
        'visual inspection, complete human/device playback, speech sync, comprehension, '
        'rights clearance, source-only adoption or publication approval.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video',type=Path)
    parser.add_argument('--captions',type=Path)
    parser.add_argument('--out',type=Path,help='Optional new JSON file; refuses overwrite')
    args = parser.parse_args()
    if args.out and args.out.exists():
        parser.error('Choose a new output file; existing evidence is not overwritten')
    result = json.dumps(verify(args.video,args.captions),indent=2)+'\n'
    if args.out:
        with args.out.open('x') as output:
            output.write(result)
    print(result,end='')


if __name__ == '__main__':
    main()
