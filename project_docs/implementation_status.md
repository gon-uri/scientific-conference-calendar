# Implementation Status

Last synchronized: 2026-10-08

## Repository Rename

- Current repository: `gon-uri/venue-radar`.
- Current website: https://gon-uri.github.io/venue-radar/.
- Completed: updated public links, Giscus repository name, local Git remote,
  attribution, and regression checks. Pages remains main/docs. Giscus's own
  API confirms access to the renamed repository and the same category IDs.
  All 123 feeds are byte-for-byte unchanged after rebuilding, preserving UIDs.
  Existing subscribers must update old feed URLs to the new Pages base.

## Venue Radar Release

- Implemented: Venue Radar branding and refined calendar/radar logo, restrained
  visual styling, compact S/M/L/XL/XXL filters, eight hierarchical topic families,
  and a Conferences & Map tab with an offline world map and date-sorted tables.
- Logo palette: dark blue-gray #263238, unified light blue #38A6B0, muted red
  location dot #C85C62, and white calendar interior. Original symbol edge coverage
  is preserved by direct pixel recoloring; exterior transparency stays intact.
  README begins with a full-width, clickable white Audiowide/logo banner.
- Interface polish: Filters & search starts expanded on desktop and collapsed
  on mobile (up to 760px). The panel contains
  metadata filters, independent ICORE/CCF selections and Search. Clear filters
  is aligned with its heading and remains visible when collapsed; clearing
  removes all restrictions without opening the panel.
  Search is aligned to the right of Acceptance rate on desktop. Topics &
  Subtopics families show disclosure arrows, plus/minus signs, and hover hints.
  Show submission options only starts selected and remains beside the deadline tab
  controls, outside the disclosure, with a larger checkbox/label, and still
  applies only to deadlines. The (time est.) annotation is below the Time left
  countdown, not in Next milestone; official date-only milestones retain
  explanatory date tooltips, and estimated-date labels are unchanged.
  The topic tree fits all eight collapsed families and scrolls after expansion;
  Time series remains inside its family, with the duplicate shortcut removed.
  Match remains below the filter grid.
  Open submission statuses retain bold green styling without a leading dot.
  Submission countdowns now match the collapsed track and required author
  action, using mandatory abstract/registration gates before paper cutoffs.
  Confirmed Open, Scheduled submission and opening-unverified Submission
  opportunity are green; estimated opportunities are yellow, closed routes red,
  and unannounced deadlines grey. Closed rows say Closed in Time left and keep
  chronological schedule placement when showing all. Expanded schedules retain
  organizer proposals, opening dates and production deadlines without treating
  them as fresh-submission countdown targets. See ADR-032.
  Topics are narrower; linked ranking headings and CCF scores open official
  webpages. The larger identity, top-right calendar action, and contrasting
  selected tab make navigation clearer. Header sizing is now 42px title / 82px
  logo on desktop and 34px / 66px on mobile. The filter disclosure has 20px
  text/arrow and an explicit 14px gap. The user selected Audiowide from the ten
  actual-font previews in project_docs/typography_proposal.md. Implementation
  embeds its native 400-weight WOFF2 face for the title only, with optical
  logo/text alignment and no external font request. Body/table fonts stay unchanged.
  Conference-name links in both tables use semibold weight 600 at their existing
  font size and color, including archived editions. Other links are unaffected.
  Mobile cards initially show Conference / Submission status / Time left in
  deadlines and Conference / Dates / Location in Conferences & Map. Independent
  More info / Less info controls reveal all remaining metadata, including past
  editions. Expansion survives filtering, tab changes and resizing; desktop
  tables remain fully visible. Without JavaScript all metadata remains visible.
  Mobile cards now have 13px darker bold field labels, a pale teal Conference
  header, stronger 1px outlines and 14px separation. More info / Less info uses
  a quieter 36px full-width white row; desktop typography/layout are unchanged.
- Sharing: Share on X and Star the repo sit beside the header calendar action,
  with matching pinned Lucide icons. X opens a prefilled draft with the approved
  introduction, rankings/rates, search/filtering and website link; visitors
  decide whether to post. No third-party social widget or automatic star is
  added. The browser tab uses a simple radar-only SVG on white; main logo and
  README artwork remain unchanged. Copy alternatives are in sharing.md.
  Actions now appear Share on X, Star the repo, All events (.ics), with
  Download calendar below the rightmost action and top-aligned desktop buttons.
  The map retains its confirmed-edition/city count without the On the map heading.
  Website author attribution no longer includes the university affiliation;
  README keeps it as plain text without a department link. Conferences & Map
  is the approved tab label; the approved personal-project disclaimer ends the
  README's final paragraph. The selected introduction starts Find your next
  conference in machine learning and AI and highlights related neuroscience,
  healthcare, complex systems and control opportunities. The exact sentence
  and alternatives are in site_copy.md; no copy decision remains pending.
  The X draft now explicitly names ML, AI and neuroscience, with the rest of
  the approved sharing text and website link unchanged.
- Catalog: 166 edition records across 129 series; 43 controlled subtopics. Added
  L4DC, IFAC SYSID, IEEE CDC, ACC, NOLTA, SIAM DS, CCS, and NetSci from official
  sources. Unpublished submission dates remain explicitly estimated.
  The 11 approved AI Deadlines additions are AutoML, LoG, CoRL, GECCO, SaTML,
  ProbML, AAMAS, MLSys, CogSci, ICIP, and Interspeech. Three focused new leaves
  cover evolutionary computation, cognition, and ML systems. The full original
  57-series gap is preserved in conference_candidates.md: 42 added, 15 remain
  untracked, with future-only ICWM separate and the missing 2024 history noted.
  The second batch adds EuroGP, KR, ICAPS, all 12 Vision/Imaging/Multimedia
  candidates, and therefore both dedicated biometrics candidates (FG, IJCB).
  Five focused leaves cover reasoning, planning, graphics, multimedia, and
  biometrics. Evidence and review priorities are in vision_ai_expansion.md.
  The third batch adds ACL, EMNLP, NAACL, COLING, CoNLL, LREC, IJCNLP, SIGIR,
  ECIR, RecSys, WWW, COLM, ISWC, ICRA, RSS and SMC (22 editions). Reviewed scope
  profiles also cover existing CIKM/WSDM. See nlp_robotics_expansion.md for
  provisional dates, ARR/RSS gates, recurrence exceptions, and monthly priorities.
  The fourth batch adds 16 complex-systems/neuroscience series (22 editions),
  including all five regional Dynamics Days branches, AREADNE and SfN.
  Publication/abstract-only caveats are documented without changing the public
  layout or submission semantics. See dynamics_neuroscience_expansion.md.
  The public build contains 212 ICS feeds; old UIDs and timing remain stable.
- Community: structured conference-request form, star/X links, author profile,
  and live Giscus comments. The official configuration checker confirms the
  repository/app/Discussions prerequisites, and the live widget renders correctly.
  README invites conference requests through the existing form and error
  reports/feature requests through a general GitHub issue link, alongside comments.
- Licensing: MIT code; CC BY 4.0 original content and artwork; separate vendor
  notices. Both licenses permit commercial reuse with their required notices.
- Maintenance: YAML remains canonical. Topic and city registries are validated;
  reusable export/workbook synchronization scripts preserve native workbook
  tables. Detailed commands live in project_docs, not README.
- Verification: data validation, Python tests, full build, workbook rendering
  and value checks, plus desktop/mobile browser interaction and overflow checks.
  The current catalog expansion passes all 81 Python tests and full browser
  smoke at six widths. All 187 prior feeds retain identical existing events;
  repeated builds are byte-identical. Release 8b351a3 is published: Build
  37794093622 and Pages 37794090302 passed, live HTML and all 28 aggregate/new
  feeds match the local output, and full live browser smoke passes at six
  widths. The earlier catalog release d869465 also verified all 30
  aggregate/new-series/new-topic feeds.

## Feature Checklist

### Curated Conference Scope Profiles

- Current status: Completed tooling; initial reviewed coverage.
- Coverage: 79 of 129 series, including all 42 AI Deadlines additions and
  the 16 complex-systems/neuroscience additions.
  The 50 remaining profiles are explicitly queued, not filled with guesses.
- Brief description: `data/conference_scopes.yml` stores zero to six curated
  additional topics, a detailed scope summary, official evidence URLs/year,
  and an independent review date by exact series. Broad CFP lists are reduced
  to characteristic areas; incidental applications do not become blanket tags.
- Public behavior: tables retain their up-to-four main topics. Family checkboxes
  use curated central identities; individual subtopics, including Time series,
  use the primary/additional union. Search also matches scope prose. Topic
  feeds use the same union; descriptions include scope evidence without changing
  event UIDs, dates, or submission status. Unprofiled venues retain their main
  topic matching. The workbook adds a separate Conference Scope sheet.
- Maintenance: the report now has edition, acceptance, and scope queues. Scope
  checks flag missing, stale, and prior-edition profiles. Editorial guidance is
  in `project_docs/conference_scopes.md`.
- Tests: schema, curation limits, fallback behavior, unchanged main tags,
  summary/extra-topic search, feed union/UID stability, queue classification,
  workbook export, and browser filtering across both tabs and the map.
- Remaining work: review the 50 missing profiles gradually from official
  sources and refresh existing profiles about monthly. Several profiles use
  the last published CFP and retain its actual year.

### Conference Data Source

- Current status: Completed
- Brief description: `data/conferences.yml` is canonical, with 166 editions across 129 series. Cadence-based estimates are distinguished from official meeting dates and deadline evidence. Joint editions and renamed series preserve their stable identities. All 42 AI Deadlines additions have official source links, explicit recurrence, central subtopics, size notes, and independent submission routes where required. ECCV and ICCV are biennial; WACV's two rounds have independent gates. Subjective Difficulty remains removed.
- Files modified: `data/conferences.yml`, `data/metadata.yml`, `data/core_conferences_normalized_tags.xlsx`
- Tests implemented: Covered by `scripts/validate.py` and the GitHub Actions build workflow.
- Remaining work: Continue adding and refreshing conferences as organizers publish dates.
- Known issues: Many future editions are intentionally marked `estimated`; they need periodic review and source confirmation.

### ICORE Rankings

- Current status: Completed
- Brief description: `data/icore_rankings.yml` holds 66 verified ICORE 2026 A*/A/B/C ranks at the conference-series level, with official portal IDs and export provenance. The second batch has 13 direct matches; 3DV and EUVIP have no ICORE entry. CoRL is explicitly Unranked in the portal. Unlisted venues, satellite workshops, and the joint IJCAI-ECAI record intentionally have no inferred rank; standalone IJCAI and ECAI 2027 have their direct mappings. The synchronized workbook carries the rank and its direct ICORE source link.
- Files modified: `data/icore_rankings.yml`, `data/core_conferences_normalized_tags.xlsx`, `scripts/validate.py`, `scripts/build_site.py`, `tests/test_icore.py`
- Tests implemented: Rank schema and workshop exclusion in validation; targeted rendering and validation tests in `tests/test_icore.py`.
- Remaining work: Re-audit against the next ICORE release when published.
- Known issues: ICORE ranks selected computing conferences and main-track full papers, not every venue type in this calendar.

### CCF Rankings And Historical Acceptance

- Current status: Completed for sourced coverage
- Brief description: `data/ccf_rankings.yml` maps 55 directly matched main-track series to the official CCF 2026 seventh-edition catalog. ICASSP and 3DV add coverage beyond ICORE; IJCAI/ECAI retain separate B mappings. PDF-page evidence remains stored, while `page_url` supplies the official webpage for public navigation and is validated separately. `data/acceptance_rates.yml` covers 34 series with historical percentages or source-grounded qualitative-only estimates, adding CVPR, ECCV, ICAPS, ICCV, and WACV evidence; the site derives five bands and shows Unknown where evidence is absent. The catalog workbook mirrors the rankings, bands, historical percentages, tracks, and source links.
- Files modified: `data/ccf_rankings.yml`, `data/acceptance_rates.yml`, `data/core_conferences_normalized_tags.xlsx`, `scripts/validate.py`, `scripts/build_site.py`
- Tests implemented: Mapping/schema checks in validation and rendering tests; workbook sample inspection and visual preview.
- Remaining work: Add reliable rate evidence as organizers publish statistics; revisit rankings only on new releases.
- Known issues: Historical rates describe specific tracks and editions, not a predicted chance of acceptance.

### Data Validation

- Current status: Completed
- Brief description: Validation checks required fields, stable IDs, date formats and precision, five size labels, up to four unique main topics, family membership, city aliases/coordinates, confidence, opening evidence, source URLs, deadline gates, duplicate UID keys, both ranking releases, and historical acceptance evidence. Scope profiles require up to six distinct controlled additional topics, bounded prose, official-source URL syntax, review date, and evidence year.
- Files modified: `scripts/validate.py`
- Tests implemented: `python scripts/validate.py`; also run in `.github/workflows/build.yml`.
- Remaining work: Consider enforcing freshness in CI if review cadence becomes a hard publication requirement; the maintenance report currently flags stale checks without blocking builds.
- Known issues: Validation confirms structure and source presence, but does not verify that external URLs are still reachable or current.

### Calendar Feed Generation

- Current status: Completed
- Brief description: Builds aggregate, deadline-only, conference-only, per-topic, and per-conference `.ics` files with deterministic UIDs and stable ordering.
- Files modified: `scripts/build_ics.py`, `docs/calendar-all.ics`, `docs/deadlines.ics`, `docs/conferences.ics`, `docs/tags/*.ics`, `docs/conferences/*.ics`
- Tests implemented: `python scripts/build_all.py`; CI runs validation before build generation.
- Remaining work: Add unit tests for ICS escaping, folding, sorting, and UID stability if the generator grows.
- Known issues: Calendar generation rewrites output files but does not currently include a snapshot test.

### Static Website Generation

- Current status: Completed
- Brief description: Generates standalone Venue Radar HTML with an expandable, submission-action-ordered milestone table (chronological schedule fallback for closed/unannounced rows) and a Conferences & Map tab with an offline city-grouped map. Submission opportunities include open, scheduled, confirmed opening-unverified, and estimated routes but not post-acceptance-only steps. Shared hierarchical topics, search, sizes, independent ICORE/CCF ranks, and acceptance filters affect both tables and the map. Metadata options and inline Search live in Filters & search, initially expanded on desktop and collapsed on mobile; Clear filters remains aligned with its heading and always visible. Show submission options only starts checked, sits beside the tabs and wraps below on mobile. The topic tree fits eight collapsed families and uses native disclosure arrows and plus/minus cues; the duplicate Time series shortcut is removed, not the subtopic. Mobile cards show their first three fields and independently reveal the rest through More info / Less info; desktop tables stay complete. Confirmed future cities appear on the map; estimates stay in the table and past editions are separate. Per-row ICS downloads remain only in Conferences & Map; aggregate download, X sharing and repository-star links are grouped at the header's right edge. A white radar-only SVG supplies the favicon. Tabs clearly contrast the selected and selectable views.
- Files modified: `scripts/build_site.py`, `docs/index.html`
- Tests implemented: `python scripts/build_all.py`; generated as part of CI. The 81 Python tests and browser smoke script cover renamed repository navigation, stable Giscus mapping and calendar UID namespace, relative download paths, embedded branding/font/licensing, README banner placement, ranking metadata/links, independent CCF filtering, disclosure containment, inline Search alignment, enlarged opportunities controls outside the collapsed panel, open abstract/paper statuses without decorative dots, time-estimate placement and milestone transitions, navigation, map interactions, optical brand alignment, and overflow at 1440/1051/1050/768/390/320px. The additions also cover annual/biennial rollover, sourced confidence, all-day deadlines, new subtopic filtering, AAMAS/MLSys/Interspeech/WACV track transitions, current FG/IJCB evidence, and curated scope matching without expanding table labels. Current polish checks default opportunity membership, collapsed clearing/focus, heading alignment, all-eight-family visibility, internal expanded scrolling, retained Time series matching, semibold conference names/inherited size/cell bounds, header action order/top alignment, caption placement, map/author wording, README attribution links and favicon pixels at 32px. mobile_cards.mjs adds 760/761px boundary checks, independent disclosure/keyboard behavior, resize/filter/tab persistence, nested milestones, archived cards and a no-JavaScript fallback.
- Remaining work: Keep desktop/mobile interaction coverage current and moderate community requests through GitHub.
- Known issues: Giscus requires GitHub sign-in and the optional external service. No screenshot-baseline comparison is currently enforced in CI.
- Submission regression checks: `tests/submission_behavior.mjs`, called by the
  browser smoke, verifies AAMAS/MLSys countdown/status transitions, mandatory
  gates, organizer versus workshop-paper relevance, estimated evidence,
  retained schedule details, Closed time-left labels and interleaved row ordering.

### Topic Taxonomy and Metadata

- Current status: Completed
- Brief description: `data/topics.yml` defines 43 leaves within eight unchanged families. `data/conference_families.yml` assigns every series one to three central family IDs, separately from generic method tags. Family selection uses these identities; individual subtopics, including Time series, use the curated primary/additional union. Dynamics includes complex systems, graphs, time series and signals; control is separate, and biometrics sits with healthcare. The long dynamics label remains one line. Tables retain four main topics. The workbook mirrors 129 catalog series, 43 leaves and 79 scope profiles. Three added leaves cover artificial life, neuromorphic computing and systems/experimental neuroscience.
- Files modified: `data/topics.yml`, `data/topic_families.yml`, `data/cities.yml`, `scripts/catalog_metadata.py`, `scripts/export_catalog.py`, `scripts/sync_workbook.mjs`, `scripts/build_site.py`
- Tests implemented: Topic membership is checked by `scripts/validate.py`.
- Remaining work: Expand the taxonomy only when needed for real conference coverage.
- Known issues: Topic changes require regenerating the tag calendar feeds.

### CI Build

- Current status: Completed
- Brief description: GitHub Actions installs Python dependencies, validates data, tests ranking integration, and runs the full build on pushes and pull requests.
- Files modified: `.github/workflows/build.yml`, `requirements.txt`
- Tests implemented: Workflow runs `python scripts/validate.py` and `python scripts/build_all.py`.
- Remaining work: Consider checking for uncommitted generated-output drift in CI if generated files are expected to stay committed.
- Known issues: CI does not deploy directly; publishing depends on GitHub Pages serving the `docs/` folder from the configured branch.

### Persistent Project Documentation

- Current status: Completed
- Brief description: Repository-level status, roadmap, architecture, decision, and session log documents live in `project_docs/` so future Codex sessions can recover state by reading the repository while `docs/` remains reserved for generated public outputs.
- Files modified: `project_docs/implementation_status.md`, `project_docs/roadmap.md`, `project_docs/architecture.md`, `project_docs/decisions.md`, `project_docs/session_log.md`, `AGENTS.md`, `README.md`
- Tests implemented: Documentation synchronization is manual. This session verified the repository with `python3 scripts/validate.py` and `python3 scripts/build_all.py`.
- Remaining work: Keep these documents updated after each feature or architecture change.
- Known issues: None for the initial documentation setup.

### Regular Data Maintenance

- Current status: Completed tooling; ongoing editorial review
- Brief description: The 30-day maintenance queue flags inferred dates even when the meeting is confirmed. Separate acceptance and scope queues flag missing/stale evidence, with scope profiles also requiring current-edition CFP checks. Idempotent rollover respects annual, biennial, and IFAC SYSID's triennial cadence. Topic/city checks and a repeatable workbook export/sync workflow accompany monthly official-source review.
- Files modified: `scripts/maintenance_report.py`, `scripts/rollover_editions.py`, `tests/test_maintenance.py`, `tests/test_rollover_and_site.py`, `project_docs/data_maintenance.md`, `README.md`
- Tests implemented: Unit tests for queue classification; CLI run against the full catalog.
- Remaining work: Run the report regularly and review organizer sources. It does not automatically scrape or publish unverified updates.
- Known issues: Acceptance evidence remains sparse for workshops and some smaller venues.
