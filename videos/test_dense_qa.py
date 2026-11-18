import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import dense_qa as d


class DenseTests(unittest.TestCase):
    def test_expression_and_invalid_indices(self):
        self.assertEqual(d.balanced_select([0]), r'eq(n\,0)')
        self.assertEqual(d.balanced_select([0, 2]), r'(eq(n\,0)+eq(n\,2))')
        for values in ([], [-1], [True], [1.0], [2, 1], [1, 1]):
            with self.assertRaises(ValueError): d.balanced_select(values)

    def test_guards_do_not_start_decoding(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(d.subprocess, 'run') as run:
            root=Path(tmp); movie=root/'wrong.mp4'; movie.write_bytes(b'wrong')
            with self.assertRaises(ValueError): d.review(movie, root/'out')
            self.assertFalse((root/'out').exists())
            with self.assertRaises(FileExistsError): d.extract_frames(movie, root, [0])
            self.assertFalse(run.called)

    @unittest.skipUnless(shutil.which('ffmpeg'), 'External FFmpeg required')
    def test_101_selected_frame_timestamps_and_pixels(self):
        indices=list(range(100))+[127]
        common=['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=s=32x32:r=128:d=1']
        def hashes(extra):
            output=subprocess.check_output(common+extra+['-fps_mode','passthrough',
                '-threads','1','-f','framemd5','-'], text=True)
            rows=[line.split(',') for line in output.splitlines() if not line.startswith('#')]
            return [(int(row[2]),row[-1].strip()) for row in rows]
        complete=hashes([])
        selected=hashes(['-vf','select='+d.balanced_select(indices)])
        self.assertEqual(selected,[complete[n] for n in indices])
        self.assertEqual(len(selected),101)

    def test_failed_extraction_writes_no_success_report(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(d.subprocess,'run') as run:
            run.side_effect=subprocess.CalledProcessError(1,'ffmpeg')
            with self.assertRaises(subprocess.CalledProcessError):
                d.extract_frames('fixture.mp4',Path(tmp)/'frames',[0,1])
            self.assertFalse((Path(tmp)/'report.json').exists())


if __name__ == '__main__': unittest.main()
