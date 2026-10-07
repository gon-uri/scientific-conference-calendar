from __future__ import annotations

import base64
import struct
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import parse_qs, urlparse
from xml.etree import ElementTree


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_site import ASSETS_DIR, SHARE_TEXT, SITE_URL, build_site


class PageElements(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs) -> None:
        self.elements.append((tag, dict(attrs)))


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
        favicon = base64.b64encode((ASSETS_DIR / "favicon.svg").read_bytes()).decode("ascii")
        self.assertIn(f'<link rel="icon" type="image/svg+xml" sizes="any" href="data:image/svg+xml;base64,{favicon}">', html)
        svg = ElementTree.parse(ASSETS_DIR / "favicon.svg").getroot()
        self.assertEqual(svg.attrib["viewBox"], "0 0 64 64")
        background = svg.find("{http://www.w3.org/2000/svg}rect")
        self.assertEqual(background.attrib, {"width": "64", "height": "64", "fill": "#ffffff"})

    def test_sharing_links_are_prefilled_and_do_not_post_automatically(self) -> None:
        with TemporaryDirectory() as directory:
            html = build_site(docs_dir=Path(directory)).read_text(encoding="utf-8")
        page = PageElements()
        page.feed(html)
        actions = {attrs["class"]: attrs for tag, attrs in page.elements
                   if tag == "a" and "header-button" in attrs.get("class", "")}
        share = actions["header-button share-button"]
        url = urlparse(share["href"])
        self.assertEqual((url.scheme, url.netloc, url.path), ("https", "x.com", "/intent/tweet"))
        self.assertEqual(parse_qs(url.query), {"text": [SHARE_TEXT], "url": [SITE_URL]})
        self.assertIn("for ML, AI, neuroscience, and related fields.", SHARE_TEXT)
        self.assertLessEqual(len(SHARE_TEXT) + 24, 280)
        self.assertEqual(actions["header-button star-button"]["href"], "https://github.com/gon-uri/venue-radar")
        for attrs in actions.values():
            self.assertEqual(attrs["target"], "_blank")
            self.assertEqual(attrs["rel"], "noopener noreferrer")
        self.assertNotIn("platform.twitter.com/widgets.js", html)

    def test_submission_options_start_selected_and_shortcut_is_removed(self) -> None:
        with TemporaryDirectory() as directory:
            html = build_site(docs_dir=Path(directory)).read_text(encoding="utf-8")
        page = PageElements()
        page.feed(html)
        inputs = {attrs.get("id"): attrs for tag, attrs in page.elements if tag == "input"}
        self.assertIn("checked", inputs["open-only"])
        self.assertNotIn("time-series-shortcut", inputs)
        self.assertIn('value="time-series-sequential-data"', html)

    def test_public_attribution_and_header_action_order(self) -> None:
        with TemporaryDirectory() as directory:
            html = build_site(docs_dir=Path(directory)).read_text(encoding="utf-8")
        page = PageElements()
        page.feed(html)
        self.assertEqual(
            [attrs["class"] for tag, attrs in page.elements
             if tag == "a" and attrs.get("class") in {
                 "header-button share-button", "header-button star-button", "calendar-button",
             }],
            ["header-button share-button", "header-button star-button", "calendar-button"],
        )
        self.assertLess(html.index('class="calendar-button"'), html.index('class="calendar-caption"'))
        self.assertNotIn("On the map", html)
        self.assertIn('tabindex="-1">Conferences &amp; Map</button>', html)
        self.assertIn(
            '<p class="subhead">Find your next conference in machine learning and AI, '
            'or explore related opportunities in neuroscience, healthcare, '
            'complex systems, and control.</p>', html,
        )
        self.assertIn('aria-label="Confirmed upcoming conference locations"', html)
        self.assertIn('Created and maintained by <strong>Gonzalo Uribarri</strong>.', html)
        self.assertNotIn("Assistant Professor", html)
        self.assertIn('href="https://www.su.se/profiles/g/gour8957"', html)
        readme = (ASSETS_DIR.parent / "README.md").read_text(encoding="utf-8")
        self.assertIn("Assistant Professor at the\nDepartment of Computer and Systems Sciences,", readme)
        self.assertNotIn("https://www.su.se/english/divisions/", readme)
        self.assertIn("[University profile](https://www.su.se/profiles/g/gour8957)", readme)
        final_paragraph = readme.strip().split("\n\n")[-1].replace("\n", " ")
        self.assertTrue(final_paragraph.startswith("Code is available under"))
        self.assertTrue(final_paragraph.endswith(
            "Venue Radar is a personal project by Gonzalo Uribarri, "
            "not an official Stockholm University service."
        ))

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
