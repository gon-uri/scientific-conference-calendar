# Data Maintenance

Last synchronized: 2026-10-06

## Weekly Edition Review

Run `python scripts/maintenance_report.py --max-age-days 60`. The edition
queue lists provisional upcoming events, unannounced deadlines, old source
checks, and series whose most recent tracked edition has passed. Each row
includes a source page to start the review. The separate acceptance queue
lists series with no sourced rate or a rate more than two edition years old.
The report is advisory; it never scrapes, silently overwrites, or promotes a
date to confirmed.

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
Unknown. Do not convert the former subjective Difficulty label into a rate.

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
