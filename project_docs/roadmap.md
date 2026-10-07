# Roadmap

Last synchronized: 2026-10-07

## Venue Radar Redesign

- Completed: refined calendar/radar identity, simple README, MIT/CC BY licensing,
  author/social links, five normalized sizes, eight hierarchical topic families,
  offline city map plus conference tables, eight new conference series, and
  synchronized catalog workbook with repeatable maintenance tooling.
- Completed community setup: Giscus prerequisites verified through its official
  checker; the live comments widget, Discussions, and request form are ready.
- Completed usability polish: single collapsible filter panel, narrower topics,
  independent CCF filter, linked rank headings/webpage scores, larger branding,
  header calendar action, more evident tab selection, inline Search, clearer
  topic/subtopic disclosure cues, and an always-visible deadline opportunities
  checkbox outside the filter panel. Larger title/logo and filter-disclosure
  sizing accompany the selected, locally embedded Audiowide title. Ten font
  specimens and the final choice are documented in typography_proposal.md.
- Completed branding refinement: four-color, geometry-preserving logo recolor
  and a full-width white Audiowide/logo banner at the beginning of README.
- Completed filter/sharing polish: always-visible Clear filters aligned with
  the disclosure heading, an eight-family topic viewport, removal of the
  duplicate Time series shortcut, default-selected Show submission options only,
  header X draft/repository-star actions and a simple white radar favicon.
- Completed header/attribution polish: rightmost calendar action with its
  caption below, no redundant map heading, shorter website attribution and
  plain-text README department name. Introduction, tab name and personal-project
  clarification proposals are in site_copy.md, awaiting selection.
- Completed repository migration: gon-uri/venue-radar with updated public
  links, Giscus name, attribution, and Git origin. Preserve all published event
  UIDs and the existing community mapping; old feed subscriptions need new URLs.
- Deferred: user accounts, live scraping, custom backend, and map tile services
  are deliberately outside the static architecture.

## Milestones

### AI Deadlines Coverage

- Completed: the 11 approved additions (AutoML, LoG, CoRL, GECCO, SaTML, ProbML,
  AAMAS, MLSys, CogSci, ICIP, Interspeech), including three focused new subtopics.
- Completed: EuroGP, KR, ICAPS and all 12 vision/imaging/multimedia candidates,
  including both dedicated biometrics venues FG/IJCB. Five additional leaves
  distinguish reasoning, planning, graphics, multimedia, and biometrics;
  recurrence and source limitations are documented in vision_ai_expansion.md.
- Completed: the 13 language/retrieval/web selections plus ICRA, RSS and SMC,
  with five focused new leaves, eight-topic filters, central family identities,
  and curated Time series subtopic matching. Evidence is in nlp_robotics_expansion.md.
- Backlog: [conference_candidates.md](conference_candidates.md) preserves all
  57 originally missing series: 42 added and 15 still untracked, plus future-only
  ICWM separately. Further additions require approval and official-source review.

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

- Goal: Maintain eight broad families: ML & Data Science; NLP, Agents & Retrieval; Vision & Multimedia; RL, Robotics & Control; Complex Systems, Time Series & Signals; Healthcare & Biometrics; Neuroscience & Neurotechnology; Responsible & Trustworthy AI. Central identities keep generic ML methods from overwhelming specialist searches; individual subtopics retain broader sourced scope matching.
- Priority: Medium
- Dependencies: `data/topics.yml`, validation, per-topic ICS generation.
- Estimated complexity: Low
- Completion status: In Progress

### Detailed Conference Scopes

- Goal: Keep useful, curated series profiles beyond the four visible main
  topics, avoiding indiscriminate import of expansive CFP inventories.
- Completed: sourced profile schema, primary/additional matching in search,
  filters and topic feeds, scope evidence in calendar descriptions, a separate
  workbook sheet, and a missing/stale/prior-edition review queue.
- Current coverage: 63 of 113 series, including all 42 AI Deadlines additions.
- Remaining work: curate the 50 missing profiles from official sources and
  review existing profiles about monthly. Prior-edition evidence stays dated.
- Guidance: [conference_scopes.md](conference_scopes.md).

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

- Goal: Show whether a new research contribution can still be submitted, align countdown and collapsed track/action with prerequisite gates, distinguish evidenced opening from confirmed opening-unverified opportunities, and retain historical acceptance bands and source-linked percentages when available.
- Priority: High
- Dependencies: `gate_for` deadline metadata, historical rate evidence, site generation, validation, browser checks.
- Estimated complexity: Medium
- Completion status: Completed for current catalog; rate coverage expands only as reliable sources are found.
- Completed correction: green Open/Scheduled/Submission opportunity states,
  yellow estimates, red closed routes, submission-action countdowns and Closed
  time-left labels. Expanded schedules and chronological closed-row placement
  remain available; AAMAS/MLSys transitions are covered by browser regressions.

### Repeatable Data Refresh

- Goal: Keep actionable monthly source-linked queues for edition reviews, historical acceptance evidence, and curated conference scopes, plus cadence-aware next-edition projections that never imply official confirmation.
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
