"""Narrow plain-text sidecar checks, not general SRT/WebVTT validation."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT/'fft-latency/source-only-review'
VTT = FOLDER/'fft-source-only-review.vtt'
SRT = FOLDER/'fft-source-only-review.srt'


def cues(text, subrip=False):
    blocks = text.strip().split('\n\n')
    if not subrip:
        if blocks.pop(0) != 'WEBVTT':
            raise ValueError('Expected plain WebVTT header')
    result = []
    separator = ',' if subrip else '.'
    hours = r'(\d{2}):' if subrip else r'(?:(\d{2}):)?'
    stamp = hours + r'([0-5]\d):([0-5]\d)' + re.escape(separator) + r'(\d{3})'
    for n, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if subrip:
            if lines.pop(0) != str(n):
                raise ValueError('Expected sequential SubRip cue numbers')
        # This archive has exactly one plain text line per cue, no style tags.
        if len(lines) != 2 or any(c in lines[1] for c in '<>'):
            raise ValueError('Outside this plain-text fixture profile')
        match = re.fullmatch(stamp+r' --> '+stamp, lines[0])
        if not match:
            raise ValueError('Unexpected timestamp profile')
        values = [int(v or 0) for v in match.groups()]
        def ms(v):
            h,m,s,f = v
            return ((h*60+m)*60+s)*1000+f
        start,end = ms(values[:4]),ms(values[4:])
        if start >= end:
            raise ValueError('Nonpositive cue duration')
        result.append((start,end,lines[1]))
    return result


class SourceSRTTests(unittest.TestCase):
    def test_all_text_and_times_match_pinned_vtt(self):
        report = json.loads((FOLDER/'render-report.json').read_text())
        self.assertEqual(hashlib.sha256(VTT.read_bytes()).hexdigest(), report['captions_sha256'])
        self.assertEqual(hashlib.sha256(SRT.read_bytes()).hexdigest(),
                         'f11544880886b3b233fbb67e7ae37246f06fb6988b3bb0882da9a2c3381a62e4')
        self.assertEqual(cues(VTT.read_text()), cues(SRT.read_text(), True))
        self.assertIn('2×', SRT.read_text(encoding='utf-8'))
        self.assertFalse(SRT.read_bytes().startswith(b'\xef\xbb\xbf'))
        self.assertFalse(report['publication_approved'])

    def test_cue_coverage_frame_edges_and_source_ending(self):
        rows = cues(SRT.read_text(encoding='utf-8'), True)
        self.assertEqual(len(rows), 19)
        self.assertEqual((rows[0][0],rows[-1][1]), (0,80000))
        for i,(start,end,_) in enumerate(rows):
            self.assertEqual(start*24 % 1000,0)
            self.assertEqual(end*24 % 1000,0)
            if i: self.assertEqual(rows[i-1][1],start)
        self.assertEqual([r[:2] for r in rows[-2:]], [(70000,75000),(75000,80000)])
        self.assertEqual(rows[-1][2], 'No live lesson or real-grid benchmark is claimed.')
        self.assertEqual(rows[-1][1]*24//1000,1920)  # exclusive end frame

    @unittest.skipUnless(shutil.which('ffmpeg'), 'External FFmpeg needed for semantic round-trip')
    def test_independent_ffmpeg_srt_to_vtt_roundtrip(self):
        text = subprocess.check_output(['ffmpeg','-v','error','-i',str(SRT),
            '-map','0:s:0','-c:s','webvtt','-f','webvtt','pipe:1'], text=True, encoding='utf-8')
        self.assertEqual(cues(text), cues(VTT.read_text(encoding='utf-8')))


if __name__ == '__main__':
    unittest.main()
