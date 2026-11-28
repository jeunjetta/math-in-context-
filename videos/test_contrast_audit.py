import json
import unittest
from unittest.mock import patch

import contrast_audit as c


class ContrastTests(unittest.TestCase):
    def test_extremes_and_symmetry(self):
        self.assertEqual(c.luminance('#000000'), 0)
        self.assertEqual(c.luminance('#ffffff'), 1)
        self.assertEqual(c.ratio('#000000', '#ffffff'), 21)
        self.assertEqual(c.ratio('#101c2c', '#101c2c'), 1)
        self.assertEqual(c.ratio('#aAbBcC', '#123456'), c.ratio('#123456', '#aabbcc'))

    def test_srgb_piecewise_and_weights(self):
        self.assertAlmostEqual(c.luminance('#0a0a0a'), (10/255)/12.92)
        self.assertAlmostEqual(c.luminance('#0b0b0b'), ((11/255+0.055)/1.055)**2.4)
        for color, expected in (('#ff0000', .2126), ('#00ff00', .7152), ('#0000ff', .0722)):
            self.assertAlmostEqual(c.luminance(color), expected)

    def test_invalid_or_nonopaque_colors(self):
        for color in (None, 123, '#fff', '#ffffffff', 'red', '#gg0000', ' #000000'):
            with self.assertRaises(ValueError): c.luminance(color)

    def test_threshold_is_not_rounded(self):
        self.assertFalse(c.meets(4.499999))
        self.assertTrue(c.meets(4.5))

    def test_palette_is_literal_without_execution(self):
        source = "raise RuntimeError('must not execute')\nBG,FG,MUTED='#000000','#ffffff','#aaaaaa'\nCYAN,AMBER,PANEL='#00ffff','#ffff00','#111111'"
        self.assertEqual(c.palette(source)['FG'], '#ffffff')

    def test_checked_in_result_and_scope(self):
        result = c.audit()
        self.assertEqual(result, json.loads(c.REPORT.read_text()))
        self.assertEqual(len(result['pairs']), 10)
        self.assertTrue(result['all_pairs_pass'])
        self.assertFalse(result['publication_approved'])
        self.assertEqual(len({(p['foreground'], p['background']) for p in result['pairs']}), 10)

    def test_manifest_and_render_source_drift_fail_closed(self):
        actual = c.sha
        manifest = c.ROOT/'fft-latency/source-only-review/render-report.json'
        for changed in (manifest, c.ROOT/'render.py', c.ROOT/'caption_layout.py',
                        manifest.parent/'fft-source-only-review.vtt', manifest.parent/'resolved-lesson.json'):
            with self.subTest(path=changed), patch.object(c, 'sha', side_effect=lambda path: 'bad' if path == changed else actual(path)):
                with self.assertRaises(ValueError): c.audit()


if __name__ == '__main__':
    unittest.main()
