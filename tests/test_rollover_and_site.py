from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_site import _acceptance_cell, _deadline_grid_rows, _milestones
from rollover_editions import rollover_candidates
from validate import load_acceptance_rates, load_conferences


class RolloverAndSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conferences = load_conferences()

    def test_rollover_is_idempotent_for_tracked_next_editions(self) -> None:
        self.assertEqual(rollover_candidates(self.conferences, date(2026, 10, 6)), [])

    def test_respects_biennial_and_omits_irregular_workshops(self) -> None:
        without_future = [
            item for item in self.conferences
            if item["id"] not in {"biomag-2028", "icpr-2028", "s-sspr-2028"}
        ]
        candidates = rollover_candidates(without_future, date(2026, 10, 6))
        self.assertEqual({item["year"] for item in candidates}, {2028})
        self.assertEqual({item["series"] for item in candidates}, {"BIOMAG", "ICPR", "S+SSPR"})
        self.assertTrue(all(item["confidence"] == "estimated" for item in candidates))

    def test_milestones_include_opening_and_conference_start(self) -> None:
        sample = {
            "conference_start": "2027-01-20", "confidence": "confirmed",
            "deadlines": [{
                "type": "full_paper", "label": "Paper deadline",
                "datetime": "2026-12-01T23:59:00Z",
                "opens_at": "2026-11-10T00:00:00Z", "confidence": "estimated",
            }],
        }
        milestones = _milestones(sample)
        self.assertEqual([item["type"] for item in milestones], [
            "full_paper_opens", "full_paper", "conference_start",
        ])
        self.assertEqual([item["estimated"] for item in milestones], [True, True, False])

    def test_qualitative_estimate_is_explicit(self) -> None:
        rates = load_acceptance_rates()["rates"]
        uai = next(item for item in self.conferences if item["series"] == "UAI")
        cell = _acceptance_cell(uai, rates)
        self.assertIn("Low", cell)
        self.assertIn("(estimated)", cell)
        self.assertIn("basis", rates["UAI"])

    def test_date_only_milestone_keeps_tooltip_without_time_estimate_label(self) -> None:
        milestone = {
            "type": "full_paper", "label": "Paper submission",
            "datetime": "2026-11-02T23:59:00-12:00",
            "estimated": False, "approximate_time": True,
        }
        html = _deadline_grid_rows([milestone])
        self.assertNotIn("(time est.)", html)
        self.assertNotIn("(est.)", html)
        self.assertIn('title="Official day; exact hour/timezone unannounced.', html)

    def test_estimated_date_still_has_milestone_label(self) -> None:
        milestone = {
            "type": "full_paper", "label": "Paper submission",
            "datetime": "2026-11-02T23:59:00-12:00",
            "estimated": True, "approximate_time": True,
        }
        html = _deadline_grid_rows([milestone])
        self.assertIn("(est.)", html)
        self.assertNotIn("(time est.)", html)
        self.assertNotIn("Official day", html)


if __name__ == "__main__":
    unittest.main()
