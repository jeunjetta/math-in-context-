import ast
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContentTests(unittest.TestCase):
    def test_latency_example(self):
        self.assertAlmostEqual(100 * (0.8 + 0.2 / 2), 90)
        self.assertAlmostEqual(1 / (0.8 + 0.2 / 2), 10 / 9)
        self.assertAlmostEqual(1 / 0.8, 1.25)

    def test_connections(self):
        data = json.loads((ROOT / "content/connections.json").read_text())
        ids = {node["id"] for node in data["nodes"]}
        self.assertEqual(len(ids), len(data["nodes"]))
        for edge in data["edges"]:
            self.assertIn(edge["from"], ids)
            self.assertIn(edge["to"], ids)

    def test_sources(self):
        sources = json.loads((ROOT / "content/sources.json").read_text())["sources"]
        self.assertEqual(len({s["id"] for s in sources}), len(sources))
        for source in sources:
            self.assertTrue(source["url"].startswith("https://"))
            self.assertTrue(source["role"])

    def test_notebook_syntax(self):
        ast.parse((ROOT / "apps/fft_and_latency.py").read_text())


if __name__ == "__main__":
    unittest.main()
