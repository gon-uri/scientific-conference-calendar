# AGENTS.md

## Project

This repository maintains a public scientific conference calendar for machine
learning, data science, AI, neuroscience, EEG/MEG, BCI, medical AI, vision,
LLMs, time-series analysis, and biomedical signal processing.

The project is intentionally static:

- no backend server
- no database
- no paid hosting
- no OpenAI API usage

The canonical source of truth is:

```text
data/conferences.yml
```

Generated website and calendar files go in:

```text
docs/
```

## Initial Structure

```text
data/
  conferences.yml
scripts/
  validate.py
  build_ics.py
  build_site.py
  build_all.py
docs/
.github/
  workflows/
    build.yml
```

## Data Rules

Each item in `data/conferences.yml` represents one edition of one conference.

Required fields:

- `id`
- `series`
- `year`
- `title`
- `short_title`
- `website`
- `conference_start`
- `conference_end`
- `topics`
- `deadlines`
- `last_checked`
- `confidence`

Allowed confidence values:

- `confirmed`
- `estimated`
- `announced_no_deadlines`
- `not_yet_announced`
- `stale`

Allowed relevance values:

- `high`
- `medium`
- `low`
- `watch`

Use `estimated` for inferred or placeholder dates. Do not make uncertain data
look confirmed.

## Generated Outputs

The first version generates:

- `docs/calendar-all.ics`
- `docs/deadlines.ics`
- `docs/conferences.ics`
- `docs/tags/*.ics`
- `docs/index.html`

Calendar event UIDs must be deterministic and stable. Derive UIDs from the
conference `id` and the event type, for example:

```text
neurips-2027-deadline-full-paper@scientific-conference-calendar
neurips-2027-conference@scientific-conference-calendar
```

Never use random values for calendar UIDs.

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

## Agent Notes

Keep changes small and reviewable. Prefer boring Python and standard library
code. Do not introduce a framework, database, deployment service, or external
API dependency unless the project owner explicitly asks for it.
