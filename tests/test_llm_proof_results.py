from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from sync_llm_proof_results import collect_known_resolutions  # noqa: E402


class LlmProofResultTests(unittest.TestCase):
    def test_checked_in_results_are_known_literature_resolutions(self):
        payload = json.loads((ROOT / "data" / "llm_proof_results.json").read_text())
        self.assertEqual(len(payload["results"]), 25)
        self.assertEqual(
            {status: sum(r["site_status"] == status for r in payload["results"])
             for status in ("solved", "disproved")},
            {"solved": 19, "disproved": 6},
        )
        self.assertTrue(all(r["article_title"] and r["article_url"]
                            for r in payload["results"]))

    def test_source_import_matches_checked_in_data(self):
        source = ROOT.parent / "Graph-Theory-LLM-Proofs"
        if not source.is_dir():
            self.skipTest("sibling Graph-Theory-LLM-Proofs checkout not available")
        expected = collect_known_resolutions(source)
        checked_in = json.loads((ROOT / "data" / "llm_proof_results.json").read_text())
        self.assertEqual(checked_in, expected)


if __name__ == "__main__":
    unittest.main()
