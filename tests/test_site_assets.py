from __future__ import annotations

import base64
import struct
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_site import ASSETS_DIR, build_site


class SiteAssetTests(unittest.TestCase):
    def test_branding_asset_dimensions_and_readme_placement(self) -> None:
        for name, dimensions in (
            ("venue-radar.png", (256, 256)),
            ("branding/venue-radar-source.png", (256, 256)),
            ("branding/venue-radar-banner.png", (1400, 175)),
        ):
            png = (ASSETS_DIR / name).read_bytes()
            self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">II", png[16:24]), dimensions)
        readme = (ASSETS_DIR.parent / "README.md").read_text(encoding="utf-8")
        self.assertTrue(readme.startswith('<a href="https://gon-uri.github.io/venue-radar/">'))
        self.assertLess(readme.index("assets/branding/venue-radar-banner.png"), readme.index("# [Open Venue Radar]"))
        self.assertNotIn('src="assets/venue-radar.png"', readme)

    def test_renamed_repository_links_and_stable_comment_mapping(self) -> None:
        with TemporaryDirectory() as directory:
            html = build_site(docs_dir=Path(directory)).read_text(encoding="utf-8")
        repo = "https://github.com/gon-uri/venue-radar"
        for suffix in (
            "", "/issues/new?template=conference-request.yml", "/discussions",
            "/blob/main/LICENSE", "/blob/main/CONTENT-LICENSE.md",
        ):
            self.assertIn(f'href="{repo}{suffix}"', html)
        self.assertIn("repo: 'gon-uri/venue-radar'", html)
        self.assertIn("'repo-id': 'R_kgDOTQKmZg'", html)
        self.assertIn("'category-id': 'DIC_kwDOTQKmZs4DHLTi'", html)
        self.assertIn("mapping: 'specific', term: 'Venue Radar community'", html)
        self.assertIn('href="calendar-all.ics" download', html)
        texts = [html]
        texts.extend((ASSETS_DIR.parent / name).read_text(encoding="utf-8")
                     for name in ("README.md", "CONTENT-LICENSE.md"))
        for text in texts:
            self.assertNotIn("gon-uri/scientific-conference-calendar", text)
            self.assertNotIn("gon-uri.github.io/scientific-conference-calendar", text)

    def test_current_logo_is_embedded_in_the_site(self) -> None:
        with TemporaryDirectory() as directory:
            html = build_site(docs_dir=Path(directory)).read_text(encoding="utf-8")
        logo = base64.b64encode((ASSETS_DIR / "venue-radar.png").read_bytes()).decode("ascii")
        self.assertIn(f'src="data:image/png;base64,{logo}" alt=""', html)
        self.assertIn(f'<link rel="icon" href="data:image/png;base64,{logo}">', html)

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
