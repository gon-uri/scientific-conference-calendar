from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_site import _conference_rows, _deadline_group_rows, _icore_cell
from validate import (
    load_acceptance_rates,
    load_ccf_rankings,
    load_conferences,
    load_icore_rankings,
    validate_icore_rankings,
)


class IcoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conferences = load_conferences()
        cls.data = load_icore_rankings()
        cls.rankings = cls.data["rankings"]
        cls.ccf_data = load_ccf_rankings()
        cls.rates = load_acceptance_rates()["rates"]

    def test_rankings_match_tracked_main_track_series(self) -> None:
        self.assertEqual(validate_icore_rankings(self.conferences, self.data), [])
        self.assertGreaterEqual(len(self.rankings), 30)
        for series in ("FMTS @ NeurIPS", "TS4H", "AALTD", "IJCAI-ECAI"):
            self.assertNotIn(series, self.rankings)

    def test_rank_and_missing_state(self) -> None:
        neurips = next(item for item in self.conferences if item["id"] == "neurips-2026")
        fmts = next(item for item in self.conferences if item["id"] == "fmts-neurips-2026")
        self.assertIn('href="https://portal.core.edu.au/conf-ranks/98/"', _icore_cell(neurips, self.rankings))
        self.assertIn("A*", _icore_cell(neurips, self.rankings))
        self.assertIn("&mdash;", _icore_cell(fmts, self.rankings))

    def test_new_columns_appear_in_both_tables(self) -> None:
        neurips = next(item for item in self.conferences if item["id"] == "neurips-2026")
        for rendered in (
            _conference_rows([neurips], self.rankings, self.ccf_data["rankings"], self.ccf_data["source_url"], self.rates),
            _deadline_group_rows([neurips], self.rankings, self.ccf_data["rankings"], self.ccf_data["source_url"], self.rates),
        ):
            self.assertLess(rendered.index('data-label="Topics"'), rendered.index('data-label="Acceptance rate"'))
            self.assertLess(rendered.index('data-label="Acceptance rate"'), rendered.index('data-label="ICORE / CCF"'))
            self.assertNotIn('data-label="Difficulty"', rendered)

    def test_validator_rejects_workshop_inheritance(self) -> None:
        data = deepcopy(self.data)
        data["rankings"]["FMTS @ NeurIPS"] = {"rank": "A*", "portal_id": 999999}
        errors = validate_icore_rankings(self.conferences, data)
        self.assertTrue(any("workshops must not inherit" in error for error in errors))

    def test_validator_reports_malformed_rank(self) -> None:
        data = deepcopy(self.data)
        data["rankings"]["NeurIPS"]["rank"] = ["A*"]
        errors = validate_icore_rankings(self.conferences, data)
        self.assertTrue(any("NeurIPS: rank must" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
