# Architecture Decision Records

Last synchronized: 2026-10-06

## ADR-001: Keep the Project Static

- Date: 2026-07-08
- Context: The calendar needs to be public, cheap to host, easy to inspect, and maintainable without operational infrastructure.
- Decision: Use a static repository with YAML data, Python generation scripts, committed `docs/` outputs, and GitHub Pages hosting.
- Alternatives considered: Backend service with a database; scheduled hosted job; external calendar API integration.
- Consequences: Hosting and operations stay simple. Generated files must be rebuilt and committed when data changes.

## ADR-002: Use YAML as the Canonical Data Source

- Date: 2026-07-08
- Context: Conference metadata needs to be human-editable and reviewable in pull requests.
- Decision: Treat `data/conferences.yml` as the canonical source of truth, with `data/topics.yml` as the controlled topic vocabulary and `data/metadata.yml` for site-level metadata.
- Alternatives considered: CSV spreadsheet only; JSON; SQLite; remote database.
- Consequences: YAML supports nested deadline records and source URLs cleanly. Validation is required to prevent schema drift.

## ADR-003: Validate Before Generating Outputs

- Date: 2026-07-08
- Context: Published calendar feeds and the website should not be regenerated from malformed or misleading data.
- Decision: Run `scripts/validate.py` before `scripts/build_ics.py` and `scripts/build_site.py`; CI also validates before building.
- Alternatives considered: Let builders fail ad hoc; rely on manual review only.
- Consequences: Data errors fail early with specific messages. Builders can assume required fields and normalized topics exist.

## ADR-004: Use Deterministic Calendar UIDs

- Date: 2026-07-08
- Context: Calendar subscribers need stable events across rebuilds.
- Decision: Derive UIDs from conference `id` and event type using the `scientific-conference-calendar` UID domain.
- Alternatives considered: Random UUIDs; timestamp-based UIDs; generated hash values.
- Consequences: Rebuilds do not create duplicate calendar events. Conference IDs and deadline types must remain stable once published.

## ADR-005: Commit Generated Public Outputs

- Date: 2026-07-08
- Context: GitHub Pages can serve static files directly from the `docs/` folder.
- Decision: Write and commit generated `.html` and `.ics` files under `docs/`.
- Alternatives considered: Generate during deployment; serve from a separate build artifact branch.
- Consequences: The published site does not need a runtime build step. Maintainers must regenerate outputs after source data changes.

## ADR-006: Maintain Persistent Project-State Documentation

- Date: 2026-07-08
- Context: Codex chat context may expire, but future sessions must be able to continue from repository state alone.
- Decision: Maintain `project_docs/implementation_status.md`, `project_docs/roadmap.md`, `project_docs/architecture.md`, `project_docs/decisions.md`, and `project_docs/session_log.md` as required project-state files.
- Alternatives considered: Rely on chat history; keep notes outside the repo; use only `README.md`.
- Consequences: Every coding session must read these docs first, update affected docs after changes, and append a session log entry before ending.

## ADR-007: Separate Project-State Docs from Public Generated Outputs

- Date: 2026-07-08
- Context: The `docs/` directory is both the GitHub Pages publishing root and the generated output target for HTML and ICS files. Keeping maintained project-state Markdown files there makes the directory harder to reason about.
- Decision: Move maintained project-state files to `project_docs/` and reserve `docs/` for generated public site and calendar artifacts.
- Alternatives considered: Keep the Markdown files in `docs/`; move generated site outputs to another folder; store project-state docs in hidden metadata directories.
- Consequences: `docs/` has one clear meaning as public generated output. `project_docs/` has one clear meaning as maintained project memory. Existing GitHub Pages publishing can remain configured to serve `/docs`.

## ADR-008: Keep AGENTS.md as a Lightweight Entrypoint

- Date: 2026-07-08
- Context: `AGENTS.md` is useful because coding agents discover it automatically, but the previous version duplicated details now maintained in `project_docs/`.
- Decision: Keep `AGENTS.md`, reduce it to concise onboarding instructions, and point agents to `project_docs/` for durable status, roadmap, architecture, decisions, and session history.
- Alternatives considered: Delete `AGENTS.md`; keep the full duplicated project specification in `AGENTS.md`.
- Consequences: Future agents still get immediate repository-specific guidance, while long-lived project knowledge has a single maintained home in `project_docs/`.

## ADR-009: Represent Joint Conference Editions Once

- Date: 2026-08-20
- Context: IJCAI and ECAI are holding a joint 2026 event. Separate records would create duplicate public site and calendar entries for the same dates and venue.
- Decision: Model the edition as one `ijcai-ecai-2026` conference record, retaining both organizations in its name, sources, topics, and search coverage.
- Alternatives considered: Duplicate the joint event as individual IJCAI and ECAI records; omit one conference from the catalog.
- Consequences: Subscribers receive one accurate event. Future editions can use individual records when the conferences resume separate schedules.

## ADR-010: Add a Dedicated NLP and LLM Topic

- Date: 2026-08-31
- Context: EACL is a core computational-linguistics venue. The controlled vocabulary had no topic that could accurately represent NLP and language-model research.
- Decision: Add `Natural Language Processing & LLMs` to `data/topics.yml` and the synchronized workbook vocabulary, then tag EACL with it alongside its relevant ML and responsible-AI topics.
- Alternatives considered: Tag EACL only as generic machine learning; add an EACL-specific tag; defer EACL until a later taxonomy revision.
- Consequences: The public site and generated ICS feeds gain a focused NLP/LLM subscription filter while retaining reusable, controlled taxonomy terms.

## ADR-011: Do Not Publish Unverified Workshop Editions as Current Events

- Date: 2026-10-05
- Context: The TS4H site still documents its 2025 workshop, and the official NeurIPS 2026 workshop list does not include TS4H. FMTS 2026 is on that list but its one-day slot is still either Dec 11 or Dec 12.
- Decision: Keep TS4H as a documented 2025 edition instead of a fabricated 2026 event. Track FMTS 2026 using Dec 11 as an explicitly estimated one-day calendar placeholder until NeurIPS assigns the exact day.
- Alternatives considered: Retain the unsupported TS4H 2026 dates; represent FMTS as a two-day event even though it lasts one day.
- Consequences: Calendar subscribers are not shown a false TS4H 2026 workshop. FMTS remains discoverable with visible date uncertainty and must be revisited when the day is announced.

## ADR-012: Source ICORE Ranks by Conference Series

- Date: 2026-10-06
- Context: The user selected ICORE for a webpage rank column. The official ICORE 2026 export provides ranks for selected computing venues but does not assign a rank to every tracked series or to satellite workshops.
- Decision: Keep a separate, validated series-level mapping of A*/A/B/C ranks and ICORE portal IDs in `data/icore_rankings.yml`. Show linked ranks in both website tables; use a dash when no direct rank is mapped. Do not transfer constituent ranks to the joint IJCAI-ECAI edition or a parent rank to a workshop.
- Alternatives considered: Duplicate ranks in every edition record; infer ranks from acronym similarities; treat unlisted venues as C or Unranked.
- Consequences: Rank provenance is auditable, edition data remains canonical for conference facts, and missing ranks do not imply low quality. The mapping and workbook require review when ICORE releases new rankings.

## ADR-013: Determine Open Submissions From Actionable Paper Routes

- Date: 2026-10-06
- Context: A future camera-ready, workshop-proposal, or commitment deadline can make a conference appear open even when a new paper can no longer be submitted. A past mandatory abstract or registration gate can also close a paper route ahead of its paper deadline.
- Decision: Keep one compact expandable deadline row per edition, but derive submission status and countdown from future paper/abstract/poster routes. Link mandatory earlier steps to their target with `gate_for`. Show only confirmed routes under the open-only filter; estimated and unannounced dates remain distinct. Retain passed milestones in the expanded list with muted red-grey styling.
- Alternatives considered: Show every milestone as a separate top-level row; use the chronologically next milestone as the countdown; hide all passed milestones.
- Consequences: Users can quickly identify where a paper can still go. Maintainers must record mandatory gates accurately, and unknown/estimated routes never masquerade as confirmed openings.

## ADR-014: Keep Rankings And Historical Rates As Separate Evidence Maps

- Date: 2026-10-06
- Context: Subjective Difficulty labels were opaque, while ICORE does not cover every tracked computing venue. CCF provides complementary direct coverage, and acceptance rates must not be invented from a rank or a subjective label.
- Decision: Add an independently sourced CCF 2026 map beside ICORE 2026. Replace Difficulty with sourced historical acceptance rates and five fixed percentage-derived bands. Store year, track, URL, and approximation flag in `data/acceptance_rates.yml`; show Unknown when evidence is insufficient. The ICORE filter remains separate and simple.
- Alternatives considered: Blend ICORE and CCF into one score; inherit ranks from parent conferences; convert old Difficulty labels into unsourced percentages; show a numeric estimate for every venue.
- Consequences: The page gains useful coverage and clearer selectivity context without implying precision it does not have. Historical figures must be refreshed and read in their edition/track context.

## ADR-015: Use An Editorial Review Queue, Not Automatic Scraping

- Date: 2026-10-06
- Context: Organizer pages change format and publish provisional schedules, so unattended scraping could silently turn a placeholder into a misleading confirmed deadline.
- Decision: Add `scripts/maintenance_report.py` with distinct edition and acceptance-evidence queues, plus `project_docs/data_maintenance.md`. A maintainer checks official sources, edits YAML, validates, rebuilds, reviews, and commits.
- Alternatives considered: Live browser scraping on page load; a backend database; automatic scheduled mutations.
- Consequences: The static architecture and reviewable provenance remain intact. Regular manual review is still required.
