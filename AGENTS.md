AGENTS.md

Project overview

This repository maintains a public, shareable scientific conference calendar focused on machine learning, data science, artificial intelligence, neuroscience, computational neuroscience, biomedical signal processing, EEG/MEG, BCI, vision, time-series analysis, and medical AI.

The project has three main outputs:

1. A structured conference database stored in YAML.
2. Generated .ics calendar feeds that people can subscribe to.
3. A simple static website published with GitHub Pages.

The calendar should include both:

* Submission-related deadlines, such as abstract, full paper, workshop, poster, camera-ready, rebuttal, notification, and early registration deadlines.
* The actual conference dates.

The source of truth must be the YAML data files, not generated HTML or generated .ics files.

Main design goals

Prioritize:

1. Simplicity.
2. Transparency.
3. Easy manual review.
4. Stable calendar event IDs to avoid duplicates.
5. No paid API dependency.
6. No OpenAI API usage.
7. Good compatibility with GitHub Pages and common calendar apps.

Avoid:

1. Complex backend services.
2. Databases.
3. Authentication systems.
4. Server-side rendering.
5. Hidden automated calendar edits.
6. Silent overwriting of manually curated data.
7. Any dependency that requires paid hosting.

Expected repository structure

Use this structure unless there is a strong reason to change it:

scientific-conference-calendar/
  AGENTS.md
  README.md
  requirements.txt
  data/
    conferences.yml
  scripts/
    validate.py
    build_ics.py
    build_site.py
    build_all.py
  docs/
    index.html
    calendar-all.ics
    deadlines.ics
    conferences.ics
    tags/
      ml.ics
      neuroscience.ics
      eeg.ics
      medical.ics
      vision.ics
      llms.ics
      time-series.ics
  .github/
    workflows/
      build.yml

The docs/ directory is the GitHub Pages output directory.

Data model

The canonical conference data should live in:

data/conferences.yml

Each entry should represent one edition of one conference.

Use this schema:

- id: neurips-2027
  series: NeurIPS
  year: 2027
  title: Conference on Neural Information Processing Systems
  short_title: NeurIPS 2027
  website: https://example.org
  cfp_url: https://example.org/cfp
  source_urls:
    - https://example.org/dates
  location: San Diego, USA
  mode: in-person
  conference_start: 2027-12-05
  conference_end: 2027-12-11
  timezone: America/Los_Angeles
  topics:
    - ML
    - LLMs
  relevance: high
  deadlines:
    - type: abstract
      label: Abstract submission deadline
      datetime: 2027-05-11T23:59:00-12:00
      source_url: https://example.org/dates
    - type: full_paper
      label: Full paper submission deadline
      datetime: 2027-05-15T23:59:00-12:00
      source_url: https://example.org/dates
  last_checked: 2026-07-07
  confidence: confirmed
  notes: ""

Required fields:

* id
* series
* year
* title
* short_title
* website
* conference_start
* conference_end
* topics
* deadlines
* last_checked
* confidence

Recommended fields:

* cfp_url
* source_urls
* location
* mode
* timezone
* relevance
* notes

Allowed confidence values:

confirmed
estimated
announced_no_deadlines
not_yet_announced
stale

Allowed relevance values:

high
medium
low
watch

Allowed topic examples:

ML
AI
Data Science
Neuroscience
Computational Neuroscience
EEG
MEG
BCI
Medical
Vision
LLMs
NLP
Time Series
Signal Processing
Healthcare
Robotics
Statistics
Explainable AI

Do not over-normalize topics at the beginning. Keep them human-readable.

Calendar generation rules

Generate at least three calendar files:

docs/calendar-all.ics
docs/deadlines.ics
docs/conferences.ics

Also generate topic-specific calendars when possible:

docs/tags/eeg.ics
docs/tags/medical.ics
docs/tags/ml.ics

Calendar event title format:

For deadlines:

[Topic1][Topic2] ShortTitle — Deadline label

Example:

[ML][LLMs] NeurIPS 2027 — Full paper submission deadline

For conference dates:

[Topic1][Topic2] ShortTitle — Conference

Example:

[Neuroscience][Medical] OHBM 2027 — Conference

Calendar event descriptions should include:

* Full conference title.
* Website.
* CFP URL if available.
* Source URL for the date.
* Location.
* Topics.
* Confidence.
* Last checked date.
* Notes if present.

Use stable event UIDs derived from the conference id and event type.

Examples:

neurips-2027-deadline-abstract@scientific-conference-calendar
neurips-2027-deadline-full-paper@scientific-conference-calendar
neurips-2027-conference@scientific-conference-calendar

Never generate random UIDs because that can create duplicate calendar events for subscribers.

Website requirements

Generate a simple static website in:

docs/index.html

The website should include:

1. A table of upcoming conference deadlines.
2. A table of upcoming conferences.
3. Filters by topic.
4. Filters by relevance.
5. A search box.
6. Links to calendar feeds.
7. A visible “last generated” timestamp.
8. A short explanation of how to subscribe to the .ics feeds.

Keep the website simple. Use plain HTML, CSS, and minimal JavaScript. Do not introduce a frontend framework unless explicitly requested.

Validation requirements

Create a validation script:

scripts/validate.py

It should check:

1. Required fields are present.
2. Conference IDs are unique.
3. Dates are parseable.
4. conference_end is not before conference_start.
5. Each deadline has a type, label, and datetime.
6. Deadlines have stable event UID components.
7. Topics are non-empty.
8. Confidence values are valid.
9. Relevance values are valid when present.

Validation should fail loudly with useful error messages.

Build requirements

Create a single command that validates data and builds all outputs:

python scripts/build_all.py

This command should:

1. Validate the YAML data.
2. Generate .ics calendar files.
3. Generate the static website.
4. Print a short summary of generated outputs.

Dependency rules

Prefer Python standard library when reasonable.

Allowed dependencies:

PyYAML
ics
python-dateutil

Keep requirements.txt minimal.

Do not add heavy dependencies unless necessary.

GitHub Actions

Add a GitHub Actions workflow that runs on push and pull request.

It should:

1. Install Python.
2. Install dependencies.
3. Run validation.
4. Build all generated outputs.

If practical, the workflow may also commit generated files, but the first version can simply check that generated files can be built.

Conference data policy

For every conference date or deadline, include at least one source URL whenever possible.

When information is not yet announced, use:

confidence: not_yet_announced

Do not invent exact dates. If a date is estimated based on prior years, mark it as:

confidence: estimated

and add a note explaining that it is estimated.

When updating conferences, prefer official conference pages over third-party aggregators.

Use third-party sources only as secondary evidence.

Monthly update workflow

The preferred update workflow is human-in-the-loop.

When asked to update conference dates:

1. Search official conference websites first.
2. Look for the latest announced edition.
3. Compare with the current YAML entry.
4. Propose a diff.
5. Add or update source URLs.
6. Update last_checked.
7. Do not silently delete old editions unless requested.
8. Mark uncertain information as estimated, not_yet_announced, or stale.

The agent should produce a summary like:

Updated:
- NeurIPS 2027: added full paper deadline and conference dates.
- ICML 2027: dates not yet announced; marked as not_yet_announced.
- OHBM 2027: conference dates confirmed, submission deadline still missing.
Needs human review:
- MICCAI 2027: found dates on a third-party site only.

Testing expectations

Before declaring work complete, run:

python scripts/validate.py
python scripts/build_all.py

If tests or validation fail, fix the issues before finalizing.

Style expectations

Keep code readable and boring.

Prefer clear function names over clever abstractions.

Add comments only where they explain non-obvious decisions.

Keep generated files deterministic so that diffs are easy to review.

Done definition

A task is done only when:

1. Data validates.
2. Calendar files build.
3. Website builds.
4. Generated files are in docs/.
5. The result can be served by GitHub Pages.
6. The final response explains what changed and how to verify it.