# Roadmap

Last synchronized: 2026-10-06

## Venue Radar Redesign

- Completed: refined calendar/radar identity, simple README, MIT/CC BY licensing,
  author/social links, five normalized sizes, seven hierarchical topic families,
  offline city map plus conference tables, eight new conference series, and
  synchronized catalog workbook with repeatable maintenance tooling.
- Completed community setup: Giscus prerequisites verified through its official
  checker; the live comments widget, Discussions, and request form are ready.
- Deferred: user accounts, live scraping, custom backend, and map tile services
  are deliberately outside the static architecture.

## Milestones

### Baseline Static Calendar

- Goal: Maintain a public static conference calendar with committed HTML and ICS outputs.
- Priority: High
- Dependencies: Valid conference YAML data, Python build scripts, GitHub Pages configuration.
- Estimated complexity: Medium
- Completion status: Completed

### Data Quality and Freshness

- Goal: Compare all provisional meeting and submission dates with current organizer schedules about monthly, preserving uncertainty until evidence is published.
- Priority: High
- Dependencies: `data/conferences.yml`, official conference pages, validation rules.
- Estimated complexity: Ongoing
- Completion status: In Progress

### Topic Coverage

- Goal: Maintain seven broad families and central subtopics covering ML/AI, data/time series, signals/vision, neuroscience/neurotechnology, healthcare/biomedical AI, dynamics/complex systems/control, and responsible/trustworthy AI.
- Priority: Medium
- Dependencies: `data/topics.yml`, validation, per-topic ICS generation.
- Estimated complexity: Low
- Completion status: In Progress

### Website Usability

- Goal: Keep the static site easy to scan, search, filter, and subscribe to.
- Priority: Medium
- Dependencies: `scripts/build_site.py`, generated `docs/index.html`, committed ICS feeds.
- Estimated complexity: Medium
- Completion status: Completed for current scope

### Conference Ranking Column

- Goal: Show independent sourced ICORE and CCF rankings without implying that workshops or unlisted venues inherit a parent conference's rank.
- Priority: Medium
- Dependencies: ICORE 2026 portal export, official CCF 2026 catalog; series-level mapping, source/year metadata, and a blank state for uncovered venues.
- Estimated complexity: Medium
- Completion status: Completed with ICORE and CCF 2026; refresh when either publisher releases a new list.

### Submission Opportunities And Acceptance Evidence

- Goal: Show whether a new paper can still be submitted, with prerequisite gates, an opportunities filter that includes future and estimated routes, historical acceptance bands, and a source-linked percentage when available.
- Priority: High
- Dependencies: `gate_for` deadline metadata, historical rate evidence, site generation, validation, browser checks.
- Estimated complexity: Medium
- Completion status: Completed for current catalog; rate coverage expands only as reliable sources are found.

### Repeatable Data Refresh

- Goal: Keep an actionable monthly source-linked queue for edition reviews and historical acceptance evidence, plus cadence-aware next-edition projections that never imply official confirmation.
- Priority: High
- Dependencies: `scripts/maintenance_report.py`, `scripts/rollover_editions.py`, official organizer pages, documented review procedure.
- Estimated complexity: Ongoing
- Completion status: Completed tooling and procedure; reviews remain recurring work.

### Calendar Feed Reliability

- Goal: Preserve deterministic calendar UIDs, stable sorting, standards-compliant escaping, and useful feed variants.
- Priority: High
- Dependencies: `scripts/build_ics.py`, `scripts/validate.py`, data schema.
- Estimated complexity: Medium
- Completion status: Completed for current scope

### Regression Testing Improvements

- Goal: Add targeted tests or checks for ICS formatting, generated-output drift, and static site behavior.
- Priority: Medium
- Dependencies: Existing build scripts, selected test framework or script conventions.
- Estimated complexity: Medium
- Completion status: In Progress; targeted metadata/ICS tests and repeatable browser smoke checks cover the redesign. Screenshot-baseline comparisons remain future work.

### Persistent Project State Documentation

- Goal: Make the repository self-documenting for future Codex sessions without relying on conversation history.
- Priority: High
- Dependencies: `project_docs/implementation_status.md`, `project_docs/roadmap.md`, `project_docs/architecture.md`, `project_docs/decisions.md`, `project_docs/session_log.md`
- Estimated complexity: Low
- Completion status: Completed
