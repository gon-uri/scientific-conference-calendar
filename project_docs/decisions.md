# Architecture Decision Records

Last synchronized: 2026-07-08

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
