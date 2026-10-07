# Development And Publication

The public app is static. Python builds committed HTML/ICS; GitHub Pages serves
the main branch's docs directory. No backend, secret, database, paid hosting,
or OpenAI API is needed. README is intentionally nontechnical.

## Required Build

```sh
python -m pip install -r requirements.txt
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build_all.py
```

Open docs/index.html directly for local preview; no development server is
required. Asset sources live in assets and are embedded by build_site.py.
Do not edit generated HTML or ICS manually. Commit source and generated output
together; inspect git diff and preserve deterministic UID keys.

## Optional Browser Smoke

tests/browser_smoke.mjs uses Playwright and a fixed 2026-10-06 reference date.
It checks opportunity filtering outside the collapsed panel, inline Search
alignment, topic disclosure cues, family intersection, map grouping, keyboard
and hover popups, empty results, milestone expansion, and six viewport widths
(including both sides of the 1050px filter-grid breakpoint).
It also checks default-selected opportunity membership, always-visible heading-
aligned clearing without opening the panel, eight collapsed families without
scrolling, internal expanded scrolling and retained Time series leaf matching.
Header sharing/star links are inspected but never used to post or star; favicon
decoding/pixels are checked at 32px and optional 16/32/64px previews are rendered.
Brand checks confirm the embedded Audiowide face is loaded without a network
font request, body/table fonts stay unchanged, and visible logo/title pixel
centers align across single-line and narrow-mobile wrapped titles.
It intentionally does not test Giscus authentication or create comments.
Update catalog-specific expected IDs/counts when the catalog changes.
Scope scenarios check summary-only searches and additional-topic filtering in
both tabs and the map, while confirming tables still show only primary tags.
The imported submission_behavior.mjs suite checks real AAMAS/MLSys transitions
and focused route fixtures: unknown versus scheduled opening, mandatory gates,
estimated evidence, actual contributions versus organizer/production steps,
matching countdown/summary and chronological closed-row placement.
The imported mobile_cards.mjs suite checks compact first-three-field cards in
both tabs, independent expansion, compact 36px full-width controls, 13px labels,
tinted headers, card outlines/spacing, desktop isolation, keyboard/focus, nested
milestones, filter/tab/resize persistence, archived editions and no-JavaScript
fallbacks. Fresh loads verify desktop-expanded/mobile-collapsed filter defaults,
including the 760/761px boundary; resizing never resets a user's disclosure state.

Use the configured bundled Node/dependency runtime when available, discovered
through the Codex workspace-dependencies tool. Alternatively supply a local
Playwright installation. CHROME_BIN can select an existing Chrome executable;
SCREENSHOT_DIR enables screenshots. A temporary tool directory with node_modules
pointing to the configured dependency directory avoids adding app dependencies:

```sh
mkdir -p /tmp/venue-radar-tools
ln -s "$NODE_DEPENDENCIES" /tmp/venue-radar-tools/node_modules
cp tests/browser_smoke.mjs tests/submission_behavior.mjs tests/mobile_cards.mjs /tmp/venue-radar-tools/
CHROME_BIN="$CHROME_BIN" SCREENSHOT_DIR=/tmp/venue-radar-previews "$NODE_BIN" /tmp/venue-radar-tools/browser_smoke.mjs "file://$PWD/docs/index.html"
```

Set the runtime variables to actual discovered paths. Use a URL-encoded file
URL if the checkout path contains spaces. The normal Python CI does not require
Playwright; browser checks are a separate maintainer step for interface changes.

## Optional Branding Assets

The logo palette and README banner are generated from maintained assets.
The original generation and assets/branding/venue-radar-source.png are immutable
references; do not recolor an already recolored/resized output. The recolor
script uses Sharp and verifies the four RGB colors and unchanged foreground
alpha/position. Banner rendering uses Playwright with the real Audiowide font.
Both libraries are optional maintainer dependencies, not website dependencies.

With the same temporary dependency directory prepared above:

```sh
cp scripts/recolor_logo.mjs scripts/build_readme_banner.mjs /tmp/venue-radar-tools/
"$NODE_BIN" /tmp/venue-radar-tools/recolor_logo.mjs "$PWD"
CHROME_BIN="$CHROME_BIN" "$NODE_BIN" /tmp/venue-radar-tools/build_readme_banner.mjs "$PWD"
python scripts/build_all.py
```

Inspect the logo, banner, and desktop/mobile page before committing the assets
and regenerated HTML together. Calendar data/feeds do not change for this work.

## Optional Workbook Synchronization

The checked-in workbook is a review mirror, not a second source of truth.
The editing helper uses the configured @oai/artifact-tool runtime. Follow the
spreadsheet skill's import/render/inspect workflow when using Codex. With the
same temporary dependency directory prepared above:

```sh
python scripts/export_catalog.py --output /tmp/venue-radar-catalog.json
cp scripts/sync_workbook.mjs /tmp/venue-radar-tools/sync_workbook.mjs
"$NODE_BIN" /tmp/venue-radar-tools/sync_workbook.mjs "$PWD/data/core_conferences_normalized_tags.xlsx" /tmp/venue-radar-catalog.json /tmp/venue-radar-workbook-preview
```

Inspect catalog, vocabulary, and scope previews, error output, and re-imported
values before committing.
The helper preserves existing series order and native table formatting, appends
new series, and refuses unexplained removals. It updates latest-edition source
links, ranks, rates, vocabulary, and the separate Conference Scope sheet from
YAML; do not manually infer missing
ratings. Optional runtime dependencies are not required to view/build the site.

## Publish

Update affected project_docs, run validation/tests/build, review the diff, commit,
and push the main branch. Verify the Build workflow, Pages deployment, and live
page. The existing monthly review automation is editorial; it does not justify
publishing unverified scraped dates. Giscus needs its owner-installed GitHub app
and public Discussions; see data_maintenance.md for setup.
