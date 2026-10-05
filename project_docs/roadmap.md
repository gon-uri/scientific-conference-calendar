# Roadmap

Last synchronized: 2026-10-05

## Milestones

### Baseline Static Calendar

- Goal: Maintain a public static conference calendar with committed HTML and ICS outputs.
- Priority: High
- Dependencies: Valid conference YAML data, Python build scripts, GitHub Pages configuration.
- Estimated complexity: Medium
- Completion status: Completed

### Data Quality and Freshness

- Goal: Keep conference dates, deadlines, confidence labels, and source URLs accurate as organizers update schedules.
- Priority: High
- Dependencies: `data/conferences.yml`, official conference pages, validation rules.
- Estimated complexity: Ongoing
- Completion status: In Progress

### Topic Coverage

- Goal: Maintain useful topic tags for ML, AI, NLP and LLMs, data mining, pattern recognition, signal processing, neuroscience, EEG/MEG, BCI, medical AI, vision, time-series analysis, and biomedical signal processing.
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

- Goal: Show a sourced conference-series ranking after Difficulty without implying that workshops or unlisted venues inherit a parent conference's rank.
- Priority: Medium
- Dependencies: User selection of a ranking source; series-level mapping, source/year metadata, and a blank state for uncovered venues.
- Estimated complexity: Medium
- Completion status: Proposed; ICORE 2026 recommended, awaiting user decision.

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
- Completion status: Not Started

### Persistent Project State Documentation

- Goal: Make the repository self-documenting for future Codex sessions without relying on conversation history.
- Priority: High
- Dependencies: `project_docs/implementation_status.md`, `project_docs/roadmap.md`, `project_docs/architecture.md`, `project_docs/decisions.md`, `project_docs/session_log.md`
- Estimated complexity: Low
- Completion status: Completed
