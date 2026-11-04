"""Narrow packaging drift guards, not a semantic or publication certifier."""
import json
import re
import unittest
from unittest.mock import patch

import render
import thumbnail
from lesson_model import context
from render import LESSON, ROOT


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.identity = json.loads((ROOT / "fft-latency/review-version.json").read_text())
        self.review = (ROOT / "fft-latency/REVIEW.md").read_text()
        self.article = (ROOT / "fft-latency/SUBSTACK_DRAFT.md").read_text()

    def test_current_handoffs_identify_same_candidate(self):
        identity = self.identity
        self.assertRegex(identity["renderer_source_commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(identity["video_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(identity["duration_seconds"], LESSON["duration"])
        self.assertEqual(identity["audio"], "silent")
        for document in (self.review, self.article):
            for key in ("label", "renderer_source_commit", "video_sha256"):
                self.assertIn(identity[key], document)
        # Historical logs/audits intentionally retain older hashes and labels.
        footer = self.review.split("## Release blockers / approval checklist", 1)[1]
        self.assertNotIn("Keep the v6 draft", footer)
        notes = self.article.split("## Editorial handoff", 1)[1]
        self.assertNotIn("existing v5 video", notes)

    def test_title_is_model_derived_and_explicit_about_fft(self):
        title = self.identity["title_template"].format_map(context(LESSON))
        actual = re.search(r"\*\*Candidate title:\*\* ([^\n]+)", self.review).group(1)
        self.assertEqual(actual, title)
        self.assertEqual(title, "2× faster FFT—but only 10 ms saved?")
        self.assertTrue(title.endswith("?"))
        copy = thumbnail.resolved_copy(LESSON)
        self.assertEqual(copy["hook"], "2× FASTER FFT.")
        self.assertTrue(copy["question"].endswith("?"))
        self.assertIn("Synthetic", copy["qualifier"])

    def test_description_article_and_source_card_credit_same_sources(self):
        readme = (ROOT / "README.md").read_text()
        self.assertEqual(len(self.identity["sources"]), 3)
        for source in self.identity["sources"]:
            self.assertTrue(source["role"])
            for document in (self.review, self.article, readme):
                self.assertIn(source["url"], document)
        # Actual renderer strings, not OCR or full semantic verification.
        with patch.object(render, "text", wraps=render.text) as drawn:
            render.render_frame(75)
        visible = "\n".join(call.args[2] for call in drawn.call_args_list)
        for name in ("FFTW accuracy notes", "linked Marimo derivation", "3Blue1Brown"):
            self.assertIn(name, visible)
        self.assertIn("videos/README.md", visible)

    def test_snapshot_does_not_clear_release_gates(self):
        self.assertIs(self.identity["publication_approved"], False)
        self.assertIn("NOT APPROVED FOR PUBLICATION", self.article)
        self.assertIn("not approved for publication", self.review)
        for document in (self.review, self.article):
            self.assertIn("ADD_VERIFIED_LESSON_URL_BEFORE_PUBLICATION", document)
            self.assertNotIn("- [x]", document)
        self.assertIn("ADD_APPROVED_VIDEO_URL_BEFORE_PUBLICATION", self.article)
        self.assertIn("not evidence for the invented timing numbers", self.review)


if __name__ == "__main__":
    unittest.main()
