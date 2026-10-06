# Data Maintenance

Last synchronized: 2026-10-06

## Monthly Edition Review

Run `python scripts/maintenance_report.py --max-age-days 30`. The edition
queue lists provisional upcoming events, unannounced deadlines, old source
checks, and series whose most recent tracked edition has passed. Each row
includes a source page to start the review. The separate acceptance queue
lists series with no sourced rate or a rate more than two edition years old.
The report is advisory; it never scrapes, silently overwrites, or promotes a
date to confirmed. Review projected dates against current official pages about
once a month, even when a conference has an apparently plausible estimate.

Run `python scripts/rollover_editions.py --as-of YYYY-MM-DD` to preview
missing next editions for supported annual and biennial series. After
checking the series cadence and current organizer pages, run the same command
with `--write` to add any still-missing records. The command is idempotent:
existing edition IDs are never replaced. It projects the prior edition's
meeting and submission timing by cadence, marks all projected dates estimated,
sets location to unannounced, and does not carry over observed portal-open status.
Other series require individual editorial review; a missing edition is not
automatically proof of an annual recurrence.

For each edition, check the organizer's official dates/CFP page and update
`data/conferences.yml`: date, time zone, location, milestones, source URLs,
`last_checked`, confidence, and a short note explaining uncertainty. Preserve
the edition `id` and deadline `type` when correcting a date so subscribed
calendar UIDs stay stable. Add `gate_for: "full_paper"` (or another exact
deadline type) when an earlier abstract/registration deadline is mandatory
for that paper route. A past gate closes that route even if the paper date
is still ahead. Workshop proposals, camera-ready files, commitments, and
supplementary materials are not new-paper opportunities. A workshop *paper*
deadline is an opportunity. If a new edition is not officially announced,
do not invent a confirmed date; use `estimated` with a source and note, or
leave the missing deadline absent.

Use edition-level `confidence` for meeting dates and deadline-level
`confidence: "estimated"` when only a submission date is inferred. Set
`opens_at` only when a source publishes an opening time. Use
`open_observed_on: "YYYY-MM-DD"` only after checking a live submission portal;
review it again as part of the next monthly pass. Without either signal the
site says Upcoming, not Open, even when the deadline is in the future.
The submission-opportunities checkbox includes confirmed upcoming and
estimated future routes, but excludes editions closed to new submissions.
The next milestone includes the conference start; after that date an edition
moves to the separate ongoing/past table. For each estimate replaced by an
official date, update the source URL, `last_checked`, confidence, and notes,
then inspect the generated site and feeds before publishing.

## Rankings And Acceptance

ICORE 2026 ranks live in `data/icore_rankings.yml`; CCF 2026 ranks live in
`data/ccf_rankings.yml`. Match an exact main-track conference series against
the official release. Do not transfer a rank to a satellite workshop or the
joint IJCAI-ECAI edition. A missing mapping is displayed as a dash, not C.
Re-audit the maps only when the corresponding publisher releases a new list.

Record a historical acceptance rate in `data/acceptance_rates.yml` only when
the organizer or proceedings supplies a defensible numerator/denominator or
published percentage. Keep the edition year, population/track, direct source
URL, and `approximate: true` for rough published counts. A single
track-specific historical rate is not a forecast for the next edition.
The website derives five qualitative bands from the percentage:

| Band | Historical rate |
| --- | --- |
| Very low | under 20% |
| Low | 20% to under 30% |
| Moderate | 30% to under 40% |
| High | 40% to under 60% |
| Very high | 60% or above |

If reliable evidence is absent, leave the series out and let the site show
Unknown. A qualitative-only estimate may be added when official historical
statistics or proceedings support a defensible band but not a current-edition
percentage; label it `(estimated)` and keep the direct source. Do not convert
the former subjective Difficulty label or rank into a rate.

## Publish

1. Synchronize the catalog workbook in `data/` when series ranks, rates, or
   tags change. YAML remains canonical.
2. Run `python scripts/validate.py`, `python -m unittest discover -s tests -v`,
   and `python scripts/build_all.py`.
3. Inspect the changed HTML and ICS outputs, especially the status of gated
   deadlines, confidence labels, links, and stable UIDs. For interface work,
   check desktop and mobile in a browser.
4. Update `data/metadata.yml` when the published dataset has been reviewed,
   update relevant `project_docs/` files, commit the generated `docs/`
   outputs with their source changes, and push.

The public site is static. It never fetches organizer pages at runtime; every
published fact must be reviewed and committed.
