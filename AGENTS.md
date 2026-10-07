# AGENTS.md

This is the lightweight entrypoint for coding agents. The detailed source of
truth lives in the repository, not in chat history.

## Before Making Changes

Read these files first:

- `project_docs/implementation_status.md`
- `project_docs/roadmap.md`
- `project_docs/architecture.md`
- `project_docs/decisions.md`
- `project_docs/session_log.md`

Then reconstruct the current project state from the repository. If the docs and
code disagree, update the docs before implementing new work.

## Project Constraints

- The calendar is intentionally static: no backend server, database, paid
  hosting, or OpenAI API dependency.
- `data/conferences.yml` is the canonical conference data source.
- `data/conference_scopes.yml` holds complementary, sourced series profiles.
  Read `project_docs/conference_scopes.md` before editing them. Keep extra topics
  characteristic and curated; never import an exhaustive CFP topics list.
- `data/conference_families.yml` assigns every tracked series one to three
  central identities in the eight-family taxonomy. Broad family filters use
  these identities; individual subtopics use the curated topic union.
  Consult `project_docs/topic_audit.md` when adding or retagging a series.
- `docs/` is reserved for generated GitHub Pages outputs: `index.html` and
  `.ics` feeds.
- `project_docs/` contains maintained project-state documentation.
- `project_docs/conference_candidates.md` preserves the dated AI Deadlines
  comparison and untracked candidate backlog. Consult it before expanding the
  catalog; candidates are not approved additions or confirmed calendar data.
- Use `estimated` for inferred or placeholder dates. Do not make uncertain data
  look confirmed.
- Calendar event UIDs must be deterministic and stable. Never use random values
  for calendar UIDs.

## Local Commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Validate data:

```bash
python scripts/validate.py
```

Build all generated outputs:

```bash
python scripts/build_all.py
```

## After Changes

- Update affected files in `project_docs/`.
- Record important technical decisions in `project_docs/decisions.md`.
- Append a session entry to `project_docs/session_log.md`.
- Keep changes small and reviewable.
