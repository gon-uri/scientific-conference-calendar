# Implementation Status

Last synchronized: 2026-10-06

## Feature Checklist

### Conference Data Source

- Current status: Completed
- Brief description: `data/conferences.yml` is the canonical source of truth for one edition per item, with dates, prerequisites, topics, sources, confidence, and review metadata. The catalog now has 83 editions across 63 series. Eighteen cadence-based next editions were added as estimates; 11 of those meeting dates were subsequently verified from organizer pages. IJCAI and ECAI 2027 were added as distinct officially announced successors to the joint 2026 event, and the former LOD series was corrected to AIS 2026 with a provisional AIS 2027 successor. IDA, ACPR, and IEEE NER have separately marked estimated submission dates based on earlier calls. The former subjective Difficulty field remains removed.
- Files modified: `data/conferences.yml`, `data/metadata.yml`, `data/core_conferences_normalized_tags.xlsx`
- Tests implemented: Covered by `scripts/validate.py` and the GitHub Actions build workflow.
- Remaining work: Continue adding and refreshing conferences as organizers publish dates.
- Known issues: Many future editions are intentionally marked `estimated`; they need periodic review and source confirmation.

### ICORE Rankings

- Current status: Completed
- Brief description: `data/icore_rankings.yml` holds 34 verified ICORE 2026 A*/A/B/C ranks at the conference-series level, with official portal IDs and export provenance. Unlisted venues, satellite workshops, and the joint IJCAI-ECAI record intentionally have no inferred rank; standalone IJCAI and ECAI 2027 have their direct mappings. The synchronized workbook carries the rank and its direct ICORE source link.
- Files modified: `data/icore_rankings.yml`, `data/core_conferences_normalized_tags.xlsx`, `scripts/validate.py`, `scripts/build_site.py`, `tests/test_icore.py`
- Tests implemented: Rank schema and workshop exclusion in validation; targeted rendering and validation tests in `tests/test_icore.py`.
- Remaining work: Re-audit against the next ICORE release when published.
- Known issues: ICORE ranks selected computing conferences and main-track full papers, not every venue type in this calendar.

### CCF Rankings And Historical Acceptance

- Current status: Completed for sourced coverage
- Brief description: `data/ccf_rankings.yml` maps 27 directly matched main-track series to the official CCF 2026 seventh-edition catalog, adding ICASSP coverage beyond ICORE and separate B mappings for IJCAI and ECAI. `data/acceptance_rates.yml` now covers 22 series with historical percentages or source-grounded qualitative-only estimates; the site derives five bands and shows Unknown where evidence is absent. The catalog workbook mirrors the rankings, bands, historical percentages, tracks, and source links.
- Files modified: `data/ccf_rankings.yml`, `data/acceptance_rates.yml`, `data/core_conferences_normalized_tags.xlsx`, `scripts/validate.py`, `scripts/build_site.py`
- Tests implemented: Mapping/schema checks in validation and rendering tests; workbook sample inspection and visual preview.
- Remaining work: Add reliable rate evidence as organizers publish statistics; revisit rankings only on new releases.
- Known issues: Historical rates describe specific tracks and editions, not a predicted chance of acceptance.

### Data Validation

- Current status: Completed
- Brief description: Validation checks required fields, IDs, date formats, topic taxonomy membership, edition- and deadline-level confidence, optional submission-opening evidence, source URLs, prerequisite deadline links, duplicate deadline UID keys, both ranking releases and workshop exclusions, and historical acceptance evidence.
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
- Brief description: Generates `docs/index.html` with one compact expandable row per edition ordered by the next chronological milestone, including conference start. Submission status distinguishes verified open, upcoming, estimated, closed, and unannounced routes; the opportunities checkbox includes open, upcoming, and estimated submission routes. The Confidence column is removed; date uncertainty appears in the status and milestone. Upcoming conferences are separated from ongoing/past editions. The result count sits beside the checkbox, and both tables use `Accept. rate` with sourced bands/percentages. Rankings, filters, and ICS downloads remain available.
- Files modified: `scripts/build_site.py`, `docs/index.html`
- Tests implemented: `python scripts/build_all.py`; generated as part of CI.
- Remaining work: Add automated browser regression checks before further large UI changes.
- Known issues: The site has no automated visual regression tests.

### Topic Taxonomy and Metadata

- Current status: Completed
- Brief description: `data/topics.yml` defines the controlled topic vocabulary, `data/metadata.yml` provides the site-level `last_updated` date, and the 63-series workbook is a synchronized catalog reference.
- Files modified: `data/topics.yml`, `data/metadata.yml`, `scripts/validate.py`, `scripts/build_site.py`
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
- Brief description: `scripts/maintenance_report.py` defaults to a 30-day review window and flags inferred submission dates even when a meeting date is confirmed. `scripts/rollover_editions.py` provides idempotent cadence-aware projections for selected annual and biennial series. `project_docs/data_maintenance.md` records the monthly source comparison and publication routine.
- Files modified: `scripts/maintenance_report.py`, `scripts/rollover_editions.py`, `tests/test_maintenance.py`, `tests/test_rollover_and_site.py`, `project_docs/data_maintenance.md`, `README.md`
- Tests implemented: Unit tests for queue classification; CLI run against the full catalog.
- Remaining work: Run the report regularly and review organizer sources. It does not automatically scrape or publish unverified updates.
- Known issues: Acceptance evidence remains sparse for workshops and some smaller venues.
