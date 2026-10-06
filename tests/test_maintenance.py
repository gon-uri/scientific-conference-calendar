from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from maintenance_report import acceptance_queue, review_queue


class MaintenanceTests(unittest.TestCase):
    def test_flags_estimated_stale_and_missing_deadline(self) -> None:
        item = {
            "id": "sample-2027", "short_title": "Sample 2027", "series": "Sample", "year": 2027,
            "last_checked": "2026-01-01", "confidence": "estimated",
            "conference_end": "2027-05-01", "deadlines": [],
            "website": "https://example.org", "source_urls": ["https://example.org/dates"],
        }
        result = review_queue([item], date(2026, 10, 6), 60)
        self.assertEqual(len(result), 1)
        self.assertIn("estimated", result[0][2])
        self.assertIn("no submission deadline", result[0][2])
        self.assertEqual(result[0][3], "https://example.org/dates")
        self.assertEqual(acceptance_queue([item], {}, date(2026, 10, 6)), ["Sample: no sourced rate"])

    def test_confirmed_fresh_complete_record_is_not_queued(self) -> None:
        item = {
            "id": "sample-2027", "short_title": "Sample 2027", "series": "Sample", "year": 2027,
            "last_checked": "2026-10-01", "confidence": "confirmed",
            "conference_end": "2027-05-01", "deadlines": [{"type": "full_paper"}],
            "website": "https://example.org",
        }
        self.assertEqual(review_queue([item], date(2026, 10, 6), 60), [])


if __name__ == "__main__":
    unittest.main()
