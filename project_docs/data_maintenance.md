# Data Maintenance

Last synchronized: 2026-10-07

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
missing next editions for explicitly supported recurring series. Annual,
biennial, and IFAC SYSID's triennial patterns are configured separately. After
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

When the official deadline day is known but its cutoff hour/timezone is not,
set `time_precision: date`. Keep an explicitly provisional end-of-day datetime
for ordering and note the assumption; the website marks the time estimate and
the ICS feed emits an all-day event. Do not mark the known day estimated merely
because the hour is unknown. Confirm and remove the date-only precision flag
when the organizer supplies the exact cutoff. If an opening day lacks an hour,
record the day with a note about its provisional midnight time; the portal
still requires source evidence before claiming it is open.

Conference proposal deadlines and restricted invited/tutorial paper routes are
not general submission opportunities. Use descriptive, non-actionable types
for them. SIAM DS, CCS, and NetSci presentation abstracts are not automatically
archival full-paper publications. L4DC's unannounced late-breaking eligibility
does not yet count as an unrestricted route.

## Topics, Sizes, And Map Locations

The AI Deadlines comparison and expansion backlog live in
`project_docs/conference_candidates.md`. It preserves 57 originally missing
series, split into 11 approved additions and 46 remaining candidates, plus
future-only ICWM. It is discovery material, not a second data source.
When approving a candidate, check names/aliases before creating a new series;
AutoML/AUTOMLCONF, LoG/LOG, and SaTML/SATML are the same series, while LoG and
LOD/AIS are different. Confirm the recurrence before configuring rollover.

For the 2026-10-07 additions, prioritize AutoML/ProbML 2027 announcements,
GECCO/CogSci 2027 submission schedules, ICIP/Interspeech exact main-paper
cutoffs, and MLSys's inconsistent homepage/CFP time conversion. AAMAS Blue Sky
Ideas has an independent abstract gate; do not let its opportunity imply the
main track accepts unregistered papers. Do not infer rates from accepted-only
lists or substitute a historical ICORE/CORE rank for the current release.

Assign up to four unique, central leaves from `data/topics.yml`. Prefer the
organizer's core CFP/scope over incidental applications; do not force four.
Parents come from `data/topic_families.yml`, never duplicate them in editions.
Every leaf must have one family and one compact display label. Keep stable
keys/feed slugs when changing presentation labels. Federated learning belongs
to ML & AI; it does not itself prove privacy or ethics coverage. The seventh
family represents responsible/trustworthy AI where it is central to scope.
See `topic_audit.md` for source examples and current family coverage.

Only S, M, L, XL, XXL are allowed, displayed in that order. Prior mixed labels
were mapped S/M to M, M/L to L, and L/XL to XL. Size remains a qualitative
scale, not an attendance claim; revise it only with a documented basis.

For a newly confirmed city, add approximate center coordinates and the exact
`location` string as an alias in `data/cities.yml`. Do not geocode ambiguous
strings, guess an unannounced venue, or claim venue-precise coordinates. The
map includes confirmed/announced meeting dates in mapped cities, in-person or
hybrid, whose start is still in the future. Estimated dates remain in the
table; past/ongoing meetings are separate. Search/topic/rank/rate/size filters
also filter map markers. The submission-opportunities checkbox is deadlines
only, so it cannot hide meetings from the map.

## Catalog Workbook

YAML is authoritative; never import spreadsheet edits silently into it.
`scripts/export_catalog.py --output catalog.json` exports each series' latest
edition and current ranks/rates/topics. `scripts/sync_workbook.mjs` accepts the
workbook, JSON, and preview directory. It preserves native tables, existing row
order/styles, numeric percentages, and vocabulary definitions, appends new
series, validates values, checks formula errors, and renders both sheets.
It refuses unexplained series removal. See development.md for the optional
artifact-tool runtime. Re-import the saved file after editing to verify row
counts and values. No Node or spreadsheet library is needed to build the site.
New submission-type descriptions wrap within their cells, and vocabulary
previews follow the current row count as the controlled taxonomy grows.

## Community Setup

Discussions are enabled for `gon-uri/venue-radar`. Giscus's official API
reconfirmed repository access and category IDs after the rename on 2026-10-07;
the live widget was originally verified on 2026-10-06. For a new fork, its owner must install
[Giscus](https://github.com/apps/giscus) for that repository only.
The embedded client uses its verified repository ID, Announcements category,
and the stable specific term `Venue Radar community`. Verify the rendered
widget on the live page after installation. GitHub sign-in is required to
comment. A direct Discussions link and structured conference-request issue
form are always available even if the optional widget cannot load.

## Repository Rename

The current repository is https://github.com/gon-uri/venue-radar and the website
is https://gon-uri.github.io/venue-radar/. The local Git remote must use the
current repository URL. Pages continues publishing main/docs.

After a future rename, update README, attribution, site navigation, Giscus's
repository name, and corresponding regression checks before rebuilding. Keep
existing Giscus IDs/mapping and the published calendar UID namespace unchanged.
Calendar download paths are relative; subscribers using an old absolute feed
URL must change its base to the new Pages URL. Do not mass-replace the historical
UID namespace, which is not a navigable URL. Verify GitHub's Pages configuration,
the live comment widget, and representative aggregate/topic/edition downloads.

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
