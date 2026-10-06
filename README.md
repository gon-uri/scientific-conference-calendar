# Scientific Conference Calendar

[Published website](https://gon-uri.github.io/scientific-conference-calendar/)

A public, static calendar of scientific conferences relevant to machine
learning, data science, AI, neuroscience, EEG/MEG, BCI, medical AI, vision,
LLMs, time-series analysis, and biomedical signal processing.

The source of truth is `data/conferences.yml`. Generated website and calendar
files are written to `docs/` for GitHub Pages.

Maintained project-state documentation lives in `project_docs/`. The `docs/`
folder is reserved for generated public site and calendar files.

## Outputs

The build creates:

- `docs/index.html`
- `docs/calendar-all.ics`
- `docs/deadlines.ics`
- `docs/conferences.ics`
- `docs/conferences/*.ics`
- `docs/tags/*.ics`

## Local Setup

```bash
pip install -r requirements.txt
python scripts/build_all.py
```

Run validation only:

```bash
python scripts/validate.py
```

## Data

Edit conference data in:

```text
data/conferences.yml
```

Each conference entry includes normalized topics, size, submission type, and
source-backed dates. Confirmed dates should include official source URLs; proxy
dates should remain marked as `estimated` with a note. A prerequisite such as
abstract registration uses `gate_for` to name the later paper deadline it gates.
Submission deadlines can have their own `confidence` when the meeting dates
are official but the submission schedule is inferred. The site's
`Show submission opportunities` checkbox includes confirmed upcoming and
estimated future paper routes, not only portals open today; a green status
marker identifies a verified open-now portal.

`data/icore_rankings.yml` and `data/ccf_rankings.yml` contain independent
series-level ranks, shown together on the website. A blank rank means no direct
match was verified; workshops do not inherit parent-conference ranks.
`data/acceptance_rates.yml` contains sourced rates for named historical tracks
and editions. The qualitative band is derived from the percentage, and absent
evidence appears as Unknown, not as a guessed numeric rate. A sourced
qualitative-only estimate is explicitly marked `(estimated)`. The workbook in
`data/` mirrors these values for catalog review.

To review upcoming editions and rate-evidence gaps:

```bash
python scripts/maintenance_report.py --max-age-days 30
python scripts/rollover_editions.py --as-of YYYY-MM-DD
```

See [data maintenance](project_docs/data_maintenance.md) for the source-check,
validation, workbook-sync, and publication procedure.

## GitHub Pages

After pushing the repository to GitHub:

1. Open the repository settings.
2. Go to **Pages**.
3. Set the source to **Deploy from a branch**.
4. Select the `main` branch and the `/docs` folder.
5. Save.

The site will publish `docs/index.html`, and the `.ics` files in `docs/` can be
used as public calendar subscription feeds.
