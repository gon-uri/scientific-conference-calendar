# Implementation Status

Last synchronized: 2026-07-08

## Feature Checklist

### Conference Data Source

- Current status: Completed
- Brief description: `data/conferences.yml` is the canonical source of truth for one edition of one conference per item. It includes conference dates, deadlines, topics, source URLs, confidence, relevance, and review metadata.
- Files modified: `data/conferences.yml`, `data/metadata.yml`, `data/topics.yml`
- Tests implemented: Covered by `scripts/validate.py` and the GitHub Actions build workflow.
- Remaining work: Continue adding and refreshing conferences as organizers publish dates.
- Known issues: Many future editions are intentionally marked `estimated`; they need periodic review and source confirmation.

### Data Validation

- Current status: Completed
- Brief description: Validation checks required fields, IDs, date formats, topic taxonomy membership, confidence and relevance values, source URL requirements for confirmed data, and duplicate deadline UID keys.
- Files modified: `scripts/validate.py`
- Tests implemented: `python scripts/validate.py`; also run in `.github/workflows/build.yml`.
- Remaining work: Add automated checks for stale `last_checked` values if freshness enforcement becomes necessary.
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
- Brief description: Generates `docs/index.html`, a static GitHub Pages site with searchable/filterable deadline and conference tables, confidence labels, per-conference ICS downloads, and client-side countdowns.
- Files modified: `scripts/build_site.py`, `docs/index.html`
- Tests implemented: `python scripts/build_all.py`; generated as part of CI.
- Remaining work: Add browser or HTML regression checks before large UI changes.
- Known issues: The site has no automated visual regression tests.

### Topic Taxonomy and Metadata

- Current status: Completed
- Brief description: `data/topics.yml` defines the controlled topic vocabulary, and `data/metadata.yml` provides the site-level `last_updated` date.
- Files modified: `data/topics.yml`, `data/metadata.yml`, `scripts/validate.py`, `scripts/build_site.py`
- Tests implemented: Topic membership is checked by `scripts/validate.py`.
- Remaining work: Expand the taxonomy only when needed for real conference coverage.
- Known issues: Topic changes require regenerating the tag calendar feeds.

### CI Build

- Current status: Completed
- Brief description: GitHub Actions installs Python dependencies, validates data, and runs the full build on pushes and pull requests.
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
