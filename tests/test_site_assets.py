from __future__ import annotations

import base64
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_site import ASSETS_DIR, build_site


class SiteAssetTests(unittest.TestCase):
    def test_title_font_is_embedded_with_its_original_license(self) -> None:
        font = (ASSETS_DIR / "vendor" / "audiowide-latin.woff2").read_bytes()
        self.assertEqual(font[:4], b"wOF2")
        with TemporaryDirectory() as directory:
            html = build_site(docs_dir=Path(directory)).read_text(encoding="utf-8")
        self.assertIn("data:font/woff2;base64," + base64.b64encode(font).decode("ascii"), html)
        self.assertIn('with Reserved Font Names "Audiowide"', html)
        self.assertIn("SIL OPEN FONT LICENSE Version 1.1", html)
        self.assertNotIn("fonts.googleapis.com", html)
        self.assertNotIn("fonts.gstatic.com", html)


if __name__ == "__main__":
    unittest.main()
