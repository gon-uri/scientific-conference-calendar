# Scientific Conference Calendar

A public, static calendar of scientific conferences relevant to machine
learning, data science, AI, neuroscience, EEG/MEG, BCI, medical AI, vision,
LLMs, time-series analysis, and biomedical signal processing.

The source of truth is `data/conferences.yml`. Generated website and calendar
files are written to `docs/` for GitHub Pages.

## Outputs

The build creates:

- `docs/index.html`
- `docs/calendar-all.ics`
- `docs/deadlines.ics`
- `docs/conferences.ics`
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

The seed dataset contains estimated placeholder dates for an initial project
skeleton. Treat these as examples until they are checked against official
conference pages.

## GitHub Pages

After pushing the repository to GitHub:

1. Open the repository settings.
2. Go to **Pages**.
3. Set the source to **Deploy from a branch**.
4. Select the `main` branch and the `/docs` folder.
5. Save.

The site will publish `docs/index.html`, and the `.ics` files in `docs/` can be
used as public calendar subscription feeds.
