import json
import unittest
import fft_review_player as p


class ReviewPlayerTests(unittest.TestCase):
    def test_generated_identity(self):
        self.assertEqual((p.ROOT/'review-player.html').read_text(),p.html())
        for id,folder in [('a','teaser-render'),('b','teaser-slower-render')]:
            d=json.loads((p.ROOT/folder/'candidate.json').read_text())
            self.assertEqual(p.candidates()[id]['sha256'],d['sha256'])

    def test_no_network_or_auto_approval(self):
        h=p.html()
        for banned in ['fetch(', 'XMLHttpRequest', 'localStorage', 'sessionStorage', 'https://', 'http://', 'autoplay']:
            self.assertNotIn(banned,h)
        self.assertIn("connect-src 'none'",h)
        self.assertIn('publication_approved:false',h)
        self.assertIn("'draft human feedback, not approval'",h)
        self.assertIn('crypto.subtle.digest',h)

    def test_safe_text_and_user_controls(self):
        h=p.html()
        self.assertNotIn('.innerHTML',h)
        self.assertIn('movie.currentTime=22',h)
        self.assertIn('movie.pause()',h)
        self.assertIn('URL.revokeObjectURL',h)
        self.assertIn('maxlength="2000"',h)
        self.assertIn('aria-live="polite"',h)


if __name__=='__main__':unittest.main()
