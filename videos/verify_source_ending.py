"""Verify a local copy of the unadopted source-ending excerpt; never approve it."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from qa import validate_media

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT/'fft-latency/source-ending-excerpt'


def sha(path):
    with Path(path).open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def verify_inputs(video, captions, report, root=ROOT):
    """Fail closed before invoking any decoder. Report is trusted repo evidence."""
    if (report['publication_approved'] is not False or report['audio'] is not False
            or report['status'] != 'unadopted source-only ending technical excerpt'
            or report['original_pilot_window'] != [70,80]
            or report['excerpt_cue_windows'] != [[0,5],[5,10]]
            or (report['duration'],report['fps'],report['frames']) != (10,24,240)):
        raise ValueError('Expected the unadopted silent ten-second excerpt report')
    if not Path(video).is_file() or sha(video) != report['sha256']:
        raise ValueError('Movie bytes do not match the recorded excerpt')
    if not Path(captions).is_file() or sha(captions) != report['captions_sha256']:
        raise ValueError('Caption bytes do not match the recorded excerpt')
    if not report['source_hashes']:
        raise ValueError('Missing source evidence')
    for relative, digest in report['source_hashes'].items():
        source = (root/relative).resolve()
        if not source.is_relative_to(root.resolve()):
            raise ValueError('Source evidence must stay inside videos/')
        if not source.is_file() or sha(source) != digest:
            raise ValueError('Source identity mismatch: '+relative)


def verify(video, captions=None):
    video = Path(video).resolve()
    captions = Path(captions or FOLDER/'fft-source-ending-excerpt.vtt').resolve()
    report = json.loads((FOLDER/'render-report.json').read_text())
    verify_inputs(video,captions,report)
    probe = json.loads(subprocess.check_output([
        'ffprobe','-v','error','-show_frames','-show_streams','-show_format',
        '-of','json',str(video)]))
    if len(probe['streams']) != 1:
        raise ValueError('Expected exactly one video stream and no other streams')
    media = validate_media(probe,dict(width=1280,height=720,fps=24,duration=10))
    if media['codec'] != 'h264':
        raise ValueError('Unexpected codec')
    # ffprobe facts are not a substitute for consuming the complete stream.
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),
                    '-map','0:v:0','-f','null','-'],check=True)
    return dict(status='exact excerpt bytes and technical media checks passed',
                source_commit=report['source_commit'],sha256=sha(video),
                captions_sha256=sha(captions),
                render_report_sha256=sha(FOLDER/'render-report.json'),
                verifier_sha256=sha(Path(__file__)),media=media,
                full_decode_completed=True,source_files_checked=len(report['source_hashes']),
                tools={name:subprocess.check_output([name,'-version'],text=True).splitlines()[0]
                       for name in ('ffmpeg','ffprobe')},
                publication_approved=False,
                limitations='Trusted repository report, not a digital signature or independent '
                'content audit. No OCR, fresh visual inspection, continuous human playback, '
                'audio sync, device comprehension, rights clearance or adoption approval.')


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
