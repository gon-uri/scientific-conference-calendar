# Scientific Conference Calendar

A public, shareable calendar of scientific conference deadlines and conference dates, focused on machine learning, data science, AI, neuroscience, EEG/MEG, BCI, medical AI, vision, LLMs, time-series analysis, and biomedical signal processing.

The project publishes:

- A human-readable conference database in YAML.
- Calendar feeds in `.ics` format.
- A simple GitHub Pages website.

## Calendar feeds

After GitHub Pages is enabled, the main feeds will be available as:

```text
calendar-all.ics
deadlines.ics
conferences.ics
```

The project may also generate topic-specific feeds such as:

```text
tags/ml.ics
tags/eeg.ics
tags/medical.ics
tags/vision.ics
tags/llms.ics
```

## Data source

The source of truth is:

```text
data/conferences.yml
```

Generated files live in:

```text
docs/
```

Do not manually edit generated files unless absolutely necessary. Instead, edit `data/conferences.yml` and rebuild.

## Local setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Validate the data:

```bash
python scripts/validate.py
```

Build all outputs:

```bash
python scripts/build_all.py
```

## Adding a conference

Add a new entry to:

```text
data/conferences.yml
```

Each conference edition should include:

- Conference name.
- Year.
- Website.
- Conference dates.
- Submission deadlines.
- Topic labels.
- Source URLs.
- Last checked date.
- Confidence level.

Use official sources whenever possible.

## Confidence levels

Use one of:

```text
confirmed
estimated
announced_no_deadlines
not_yet_announced
stale
```

Do not invent exact dates. If a date is inferred from prior years, mark it as `estimated`.

## Topic labels

Suggested topics include:

```text
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
```

## Sharing

The preferred sharing method is the GitHub Pages website plus public `.ics` feeds.

People can subscribe to the `.ics` feeds from Google Calendar, Apple Calendar, Outlook, or other calendar apps.

## Monthly update workflow

Once per month, use ChatGPT or Codex to check the latest official conference pages and propose updates to `data/conferences.yml`.

The update process should be human-reviewed. The agent should not silently overwrite uncertain data.