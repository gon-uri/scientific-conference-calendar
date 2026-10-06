# Session Log

## 2026-10-07 (four-color logo and README banner)

- Objective: Change only the logo colors and place a full-width white
  logo/Audiowide banner at the top of README.
- Method: two built-in image-editor trials were discarded because they
  introduced subtle edge/shading changes. The user explicitly approved direct
  pixel processing instead. Preserved the existing 256px source under
  assets/branding/venue-radar-source.png and left the original 1254px generation
  untouched. No foreground position, stroke shape, size, or alpha was changed.
- Completed: exact four-color logo (#263238, #38A6B0, #C85C62, #FFFFFF),
  opaque white calendar interior/header, and transparent exterior. The same
  active asset is embedded as website mark/favicon. README starts with a
  clickable 1400x175 white banner rendered with the real Audiowide face;
  the prominent text link follows it and the separate small logo was removed.
- Maintenance: added recolor_logo.mjs and build_readme_banner.mjs as optional
  Sharp/Playwright maintainer tools. Documented commands, palette, source
  provenance, and geometry guarantees in the project documents.
- Verification: recolor assertions confirm four nontransparent RGB values
  and unchanged foreground alpha at every original pixel. All 93 records
  validate, 32 Python tests and the full build pass, and browser checks pass
  at 1440/1051/1050/768/390/320px. Final banner and mobile page were inspected.
- Publication: source assets, README, maintained docs, and generated HTML
  are committed together. Canonical data, ranks, dates, and all ICS feeds
  are unchanged.

## 2026-10-07 (Audiowide selection and publication)

- Objective: Apply the user's chosen Audiowide title and publish the approved
  larger identity and filter-disclosure styling.
- Completed: embedded the native 400-weight Latin WOFF2 for the title only,
  disabled synthetic styling, and preserved the original OFL notice in the
  vendor directory and generated HTML. No external font request is required;
  body/table fonts, conference data, rankings, and all 123 ICS feeds are unchanged.
- Layout: retained 42px/82px desktop and 34px/66px mobile title/logo dimensions.
  Optical text shifts are 2px/1.5px; narrow titles wrap cleanly between words.
  Mobile brand padding contains the taller text bounds. Filters & search
  retains the approved 20px label/triangle, 14px gap, and native keyboard behavior.
- Documentation: synchronized status, architecture, roadmap, decision record,
  typography selection, and third-party attribution; retained both preview PNGs
  as review artifacts, not public runtime assets.
- Verification: 93 records validate, all 30 Python tests pass, and the full
  build succeeds. Browser tests pass at 1440/1051/1050/768/390/320px, checking
  loaded Audiowide, no network font requests, unchanged body fonts, visible-pixel
  logo/title centering, text fit, disclosure keyboard controls, filters, and map.
  Desktop and narrow-mobile screenshots were inspected.
- Publication: source, selected font/license, documentation, and generated HTML
  are committed together for the existing main/docs GitHub Pages workflow.

## 2026-10-07 (distinctive fonts and visible-centre alignment)

- Objective: Offer five more unusual title fonts and align the logo and text
  vertically in the new preview set.
- Completed: sourced and rendered Syne ExtraBold, Unbounded Black, Audiowide,
  Righteous, and Orbitron Black as options 6-10. Each uses an actual official
  font file, the same 42px title/82px logo, and unchanged brand colors.
- Alignment: measured visible pixel bounds in browser screenshots and applied
  font-specific text offsets. All five visible vertical centres agree within
  0.1px; finished PNG was visually inspected. No synthetic bold, missing fonts,
  blank logo images, clipped text, or JavaScript errors were detected.
- Documentation: expanded typography_proposal.md with sources, weights, and
  alignment details. User font selection remains pending. No production code,
  canonical data, or calendar feeds changed in this proposal; prior local UI
  edits remain intact and unpushed.

## 2026-10-07 (header sizing and five typography options)

- Objective: Double the filter arrow/text spacing, enlarge its label/indicator,
  enlarge the title more than the logo, and show five bolder title-font options.
- Completed locally: desktop title/logo are 42px/82px; mobile 34px/66px. Filters
  & search uses a 20px label/triangle and 14px gap. Its native disclosure and
  keyboard semantics remain intact. No public font family change was made.
- Proposal: rendered Space Grotesk Bold, Sora ExtraBold, Archivo Black,
  Bricolage Grotesque ExtraBold, and Oxanium Bold from actual official font
  files at identical size/color/logo dimensions. Verified all five fonts loaded.
  Preview and source/implementation notes are in assets/branding and
  project_docs/typography_proposal.md. User selection is pending.
- Verification: all 93 records validate; 29 Python tests and the full build
  pass. Browser checks cover disclosure spacing/rotation, brand fit, filters,
  map behavior, and overflow at 1440/1051/1050/768/390/320px. Previews inspected.
- Publication: local working changes, not yet committed or pushed. Conference
  facts, ranking data, and ICS feeds are unchanged.

## 2026-10-06 (time-estimate placement and opportunities sizing)

- Objective: Move `(time est.)` from Next milestone into Time left, and slightly
  enlarge the Show only submission opportunities checkbox and label. Align
  Clear filters vertically with the Match selector.
- Completed: the annotation appears beneath the selected countdown and updates
  with the next milestone. Expanded date-only entries retain explanatory
  tooltips; `(est.)` date labels are unchanged. The opportunities control uses
  .94rem text and a fixed 19px checkbox while preserving responsive placement.
  Match and Clear filters share a compact, vertically centered footer row.
- Verification: all 93 editions validate; 29 Python tests and the full build
  pass. Browser checks cover annotation placement, collapsed/expanded rows,
  transition to a non-time-estimated milestone, checkbox size, Match/Clear
  alignment, existing filters and map interactions, and overflow at
  1440/1051/1050/768/390/320px.
- Publication: source and generated HTML use the existing main/docs Pages
  configuration. Conference data, rankings, and all ICS feeds are unchanged.

## 2026-10-06 (inline search and topic discovery)

- Objective: Refine filter placement and make the topic hierarchy easier to
  discover without changing filtering semantics.
- Completed: Search follows Acceptance rate in the shared grid with aligned
  desktop headings; the disclosure is larger and named Filters & search.
  Show only submission opportunities sits outside beside the tabs and stays
  usable with the panel collapsed. Topics & Subtopics replaces the filter
  legend; native disclosure arrows and hover hints supplement plus/minus signs.
  Narrow screens stack the controls without changing their order or meaning.
  Corrected tablet-width table-header crowding with wrapping and compact padding.
- Verification: all 93 editions validate; 27 Python tests and the full build
  pass. Browser checks cover collapsed-panel opportunities, Search alignment,
  topic expansion/selection, both rank filters, map interactions, header overlap, and overflow
  at 1440/1051/1050/768/390/320px. Desktop/mobile previews were inspected.
- Publication: source and generated HTML use the existing main/docs Pages
  configuration. Conference records, rankings, and ICS feeds are unchanged.

## 2026-10-06 (filter and navigation corrections)

- Objective: Apply requested compact filtering, CCF navigation/filtering, header
  and tab refinements; propose an alternative title font separately.
- Completed: one initially collapsed filter panel containing search, all
  options, and Clear filters; narrower Topics; independent CCF filter; linked
  ICORE Rank/CCF Rank headings; CCF scores link to the official seventh-edition
  webpage while PDF/page evidence remains intact. Increased title/logo sizes,
  moved the labelled calendar download to the header's right edge, and made
  selected/unselected tabs more distinct. No conference dates or ranks changed.
- Typography: proposed Space Grotesk SemiBold (600), with the current body font
  retained; awaiting user approval before applying a title-font change.
- Verification: all 93 editions validate; 27 Python tests and the full build
  pass. Browser checks pass at 1440/768/390/320px, covering filter containment,
  collapsed state, rank links, independent/combined CCF selections, Unranked,
  both tables/map, existing interactions, and horizontal overflow. Inspected
  desktop and narrow-mobile screenshots; no calendar feed changes.
- Publication: these UI corrections use the existing main/docs GitHub Pages
  configuration; source and generated HTML are published together.

## 2026-10-06 (Venue Radar implementation)

- Objective: Implement the approved redesign, conference expansion, topic
  hierarchy, community support, and refined sector-sweep calendar/radar logo.
- Completed: normalized five sizes; seven families/27 subtopics; source-reviewed
  tags; offline confirmed-city map and Conferences tables; restrained responsive
  styling; eight new series/ten editions (93 editions, 71 series); date-only
  deadline precision; MIT/CC BY licenses and vendor notices; simple README,
  author/social links, structured request form, and configured lazy Giscus.
- Maintenance: added validated city/family registries and repeatable latest-series
  export/workbook sync. Updated the native-table workbook and project documents.
- Verification: 24 Python tests pass; all 93 records validate; repeated builds
  are byte-identical. All 123 ICS feeds have CRLF, <=75-byte physical lines,
  and balanced events; all 226 pre-existing event UIDs are retained. Re-imported
  workbook values match every series/subtopic and show no formula errors.
  Browser smoke checks pass at 1440/768/390/320px, including expanded mobile
  filters, partial family selection, ANY/ALL matching, closed-route exclusions,
  grouped map popups, keyboard/hover access, empty results, and world-view reset.
  Popup auto-pan and city-link zoom races found during testing were corrected.
- Publication: pushed release commit 4d70ec0 to main. Build and Pages deployment
  succeeded; the live page shows the new identity, catalog, families, and map.
  Giscus's official checker confirms all repository/app/Discussions prerequisites;
  the live widget renders its editor and GitHub sign-in without configuration
  errors. No test comment or reaction was posted.
- Remaining work: community moderation and monthly official-source review,
  especially estimated deadlines and unknown acceptance statistics.

## 2026-10-06 (Conference Radar branding proposal)

- Objective: Explore the approved public name and requested logo candidates,
  and evaluate responsible-AI coverage before redesign implementation.
- Tasks completed: Created three transparent PNG logo candidates; recorded the
  resolved design, license, conference-addition, hierarchy, author, and social
  choices in `project_docs/branding_proposal.md`. Checked current tag coverage
  and official FAccT, AIES, ACML, KDD, and ICLR sources.
- Verification: All candidate PNGs have an alpha channel; no canonical data,
  live website, README, license, or generated-output changes were made.
- User selection at proposal time: Option 2 (calendar radar), with Venue Radar
  preferred over Conference Radar. Later feedback requested a refined sector
  sweep; the implementation session above records the final artwork.
- Follow-up: The user approved implementation and the seventh Responsible &
  Trustworthy AI family; federated learning remains an ML subtopic.

## 2026-10-06 (milestone ordering and recurring editions)

- Objective: Make the submission calendar chronological without confusing post-acceptance steps with paper opportunities, refresh future editions, and establish a monthly estimate-review workflow.
- Tasks completed:
  - Reworked the deadline table around each edition's next milestone, including conference start; moved ongoing/past meetings to a separate table. Submission status now distinguishes verified open, upcoming, estimated, closed, and unannounced routes independently of sorting. The opportunities checkbox includes upcoming and estimated routes, not only portals open now.
  - Removed the Confidence columns, widened Next milestone, changed the heading to `Accept. rate`, placed the result count beside the checkbox, and made mobile filters collapsible. A green marker identifies verified open-now submissions.
  - Added a cadence-aware, idempotent rollover tool and 18 projected next editions. Replaced 11 projected meeting dates with official announcements and added sourced, explicitly estimated deadlines for IDA, ACPR, and IEEE NER.
  - Added official IJCAI and ECAI 2027 as separate editions, with direct ICORE/CCF mappings and a sourced IJCAI 2024 acceptance rate. Corrected LOD 2026 to its organizer-announced AIS name, dates, and location; added a provisional AIS 2027 successor.
  - Expanded sourced acceptance-rate coverage to 22 series, including clearly marked qualitative-only estimates, and synchronized the 63-series catalog workbook.
  - Changed maintenance review to a 30-day default, documented monthly source comparison, and added focused tests for projections, status, and review queues.
- Tests run: YAML validation, Python unit tests, full HTML/ICS build, workbook preview/error check, and desktop/mobile Chrome interaction and overflow checks.
- Remaining tasks: Keep provisional editions and qualitative estimates under monthly review; add automated browser/ICS snapshot checks if interface or feed complexity grows.

## 2026-10-06 (submission opportunities and acceptance)

- Objective: Make the calendar reliable for finding the next real paper-submission opportunity, add complementary CCF ranks and sourced acceptance evidence, and make routine data refreshes repeatable.
- Tasks completed:
  - Removed subjective Difficulty from canonical data and ICS descriptions. Added mandatory `gate_for` links to 19 abstract/registration steps.
  - Added 25 direct CCF 2026 ranks and 13 source-backed historical acceptance rates; synchronized the catalog workbook with bands, percentages, tracks, editions, and source links.
  - Added submission status, actionable countdown, compact expandable deadlines, muted passed milestones, open-only filtering, clearer column order, result count, and compact filters to both website tabs.
  - Added an edition/evidence maintenance report and documented the editorial update and publication routine.
- Tests run: YAML validation, Python unit tests, full HTML/ICS build, workbook render and formula-error scan, and desktop/mobile Chrome interaction and overflow checks.
- Remaining tasks: Expand historical rate coverage only where trustworthy sources exist; continue reviewing provisional next editions. Add automated browser/ICS regression checks.

## 2026-10-06

- Objective: Publish ICORE 2026 conference ranks in both calendar table tabs.
- Tasks completed:
  - Audited the official ICORE 2026 export against all 61 tracked series and recorded 32 verified main-track ranks with direct source links. Left unmatched, joint-event, and workshop ranks blank rather than inferring them.
  - Added the ICORE column after Difficulty in both Upcoming Deadlines and Upcoming Conferences, including a clear missing-rank state and scope note.
  - Synchronized the series workbook, added ranking validation and focused tests, and rebuilt the generated page.
- Tests run: Data validation, unit tests, static build, official-export cross-check, workbook inspection, and desktop/mobile visual checks.
- Remaining tasks: Recheck the ranking source when ICORE publishes a new release; continue the existing review of provisional conference dates.

## 2026-10-05

- Objective: Add IDA, AIME, and FMTS editions; refresh the conference calendar; research ranking sources for a possible website column.
- Tasks completed:
  - Added official IDA 2026, AIME 2027, and FMTS @ NeurIPS 2026 records with source URLs, topics, metadata, and submission deadlines.
  - Corrected PAKDD 2027 dates, venue, submission and camera-ready deadlines from its official site; updated ITISE 2027 with its announced dates and a date-only submission deadline whose hour remains estimated.
  - Rechecked the incomplete upcoming COLT, OHBM, IEEE NER, IDA 2027, ACPR, and TS4H entries. The first five remain incomplete; the TS4H 2026 record was replaced with the documented 2025 edition because no 2026 workshop was announced.
  - Synchronized the series-level workbook, updated site metadata, and researched ICORE, CCF, and Google Scholar Metrics. Recommended ICORE 2026 for a future column, pending user selection.
- Tests run: `python3 -B scripts/validate.py` and `python3 -B scripts/build_all.py`; checked generated site and ICS outputs and workbook rendering.
- Remaining tasks: Recheck FMTS's exact workshop day, IDA 2027's exact dates, and the provisional upcoming deadlines as organizers publish them. Add a ranking column only after the user selects a source.


## 2026-09-14

- Objective: Refresh canonical upcoming-edition data from official organizer sources and publish the rebuilt static calendar.
- Tasks completed:
  - Rechecked all 17 records that were previously marked provisional against their official event or series pages.
  - Promoted AISTATS 2027, COSYNE 2027, IEEE BigData 2026, ICPR 2026, S+SSPR 2026, and AALTD 2026 to `confirmed` after organizers published their schedules and submission milestones.
  - Corrected dates, locations, CFP URLs, source URLs, and deadlines where official material superseded prior-cycle estimates.
  - Preserved 11 entries as `estimated`, `announced_no_deadlines`, or `not_yet_announced` where organizers still have not published sufficient future information, while updating their `last_checked` review metadata.
- Files modified:
  - `data/conferences.yml`
  - `data/metadata.yml`
  - `project_docs/implementation_status.md`
  - `project_docs/roadmap.md`
  - `project_docs/architecture.md`
  - `project_docs/session_log.md`
- Tests run:
  - `python3 -B scripts/validate.py` passed and validated 59 conferences before output generation.
  - `python3 -B scripts/build_all.py` passed and regenerated `docs/index.html` plus all aggregate, topic, and per-conference ICS feeds.
  - An integrity check confirmed the six newly verified records are `confirmed` and all 11 remaining provisional records were reviewed on 2026-09-14.
- Remaining tasks:
  - Continue periodic reviews of the 11 intentionally provisional future editions.
- Suggested next step: Continue periodic official-source reviews for the 11 intentionally provisional entries.

## 2026-08-31

- Objective: Verify the IJCAI-ECAI and EACL catalog coverage and refresh incomplete upcoming-edition information from organizer sources.
- Tasks completed:
  - Confirmed that IJCAI-ECAI 2026 was already represented as one joint record and added its official main-track CFP dates.
  - Added EACL 2027 in Athens with its official ARR submission and EACL commitment dates, conference metadata, and per-conference calendar identity.
  - Added the controlled `Natural Language Processing & LLMs` topic and synchronized it to the workbook vocabulary sheet.
  - Refreshed available facts for incomplete records, including corrected CCN 2026 dates and location, CIKM 2026 dates and CFP, CNS* and Bernstein deadlines, ESANN 2027, IDEAL 2026, IEEE NER 2027, IEEE SSP 2027, and ICPR 2026 dates.
  - Rechecked every remaining provisional record against its official series or event page and preserved `estimated`, `announced_no_deadlines`, or `not_yet_announced` where organizers still have not published sufficient future information.
  - Synchronized `data/core_conferences_normalized_tags.xlsx` with all 59 canonical records and visually verified the conference and vocabulary sheets.
- Files modified:
  - `data/conferences.yml`
  - `data/topics.yml`
  - `data/metadata.yml`
  - `data/core_conferences_normalized_tags.xlsx`
  - `project_docs/implementation_status.md`
  - `project_docs/roadmap.md`
  - `project_docs/architecture.md`
  - `project_docs/decisions.md`
  - `project_docs/session_log.md`
- Tests run:
  - `python3 -B scripts/validate.py` passed and validated 59 conferences before output generation.
  - `python3 -B scripts/build_all.py` passed and regenerated `docs/index.html` plus aggregate, topic, and per-conference ICS feeds.
- Remaining tasks:
  - Continue periodic reviews of the intentionally provisional future editions.
- Suggested next step: Recheck the intentionally provisional future editions as their organizers publish official calls.

## 2026-08-20

- Objective: Expand and refresh the conference catalog requested for ML/AI, data mining, pattern recognition, signal processing, and time-series research.
- Tasks completed:
  - Audited the requested 39 conference labels against the canonical YAML catalog and synchronized spreadsheet, expanding the catalog from 34 to 58 records.
  - Added 24 missing records with normalized topics, difficulty, size, relevance, source URLs, confirmation states, review notes, and deterministic calendar IDs.
  - Recorded the joint IJCAI-ECAI 2026 edition once so the public site and calendar feeds do not duplicate the shared event.
  - Reviewed official organizer sites and refreshed newly published upcoming-edition details for existing and added conferences, including ICLR, ECML PKDD, MICCAI, ISBI, WSDM, ACML, ICANN, ICONIP, EUSIPCO, and IEEE conference series.
  - Kept entries marked `estimated` or `not_yet_announced` whenever an official future date or deadline was unavailable.
  - Synchronized `data/core_conferences_normalized_tags.xlsx` with the canonical 58-record catalog while preserving its table formatting.
- Files modified:
  - `data/conferences.yml`
  - `data/core_conferences_normalized_tags.xlsx`
  - `data/metadata.yml`
  - `project_docs/implementation_status.md`
  - `project_docs/roadmap.md`
  - `project_docs/architecture.md`
  - `project_docs/decisions.md`
  - `project_docs/session_log.md`
- Tests run:
  - `python3 -B scripts/validate.py` passed and validated 58 conferences.
  - `python3 -B scripts/build_all.py` passed, regenerated `docs/index.html`, and regenerated aggregate, topic, and per-conference ICS feeds.
  - YAML integrity checks confirmed unique IDs, fresh review dates, and coverage of every requested label; IJCAI and ECAI resolve to the joint 2026 record.
- Remaining tasks:
  - Continue reviewing intentionally non-confirmed entries as organizers publish official details.
- Suggested next step: Continue periodic official-source reviews for entries intentionally awaiting organizer announcements.

## 2026-07-08

- Objective: Establish persistent project-state documentation so future Codex sessions can recover current state from the repository.
- Tasks completed:
  - Inspected repository structure, source data files, build scripts, README, generated docs outputs, and CI workflow.
  - Created initial implementation status, roadmap, architecture, ADR, and session log documentation.
  - Documented the current static YAML-to-HTML/ICS architecture and generated-output workflow.
  - Installed the declared `PyYAML` dependency into the local Python 3 environment after validation showed it was missing.
  - Verified validation and full build commands.
- Files modified:
  - `project_docs/implementation_status.md`
  - `project_docs/roadmap.md`
  - `project_docs/architecture.md`
  - `project_docs/decisions.md`
  - `project_docs/session_log.md`
- Tests run:
  - `python scripts/validate.py` could not run because `python` is not available on PATH in this local environment.
  - `python3 scripts/validate.py` initially failed because `PyYAML` was missing.
  - `python3 -m pip install -r requirements.txt` completed successfully.
  - `python3 scripts/validate.py` passed and validated 34 conferences.
  - `python3 scripts/build_all.py` passed, validated 34 conferences, and regenerated the expected HTML and ICS outputs.
- Remaining tasks:
  - Keep these documentation files synchronized with future code, data, and architecture changes.
- Suggested next step: Keep the documentation files synchronized whenever conference data, build behavior, or architecture changes.

## 2026-07-08

- Objective: Clarify the documentation architecture and review whether `AGENTS.md` should remain.
- Tasks completed:
  - Moved maintained project-state documentation from `docs/` to `project_docs/`.
  - Reserved `docs/` for generated GitHub Pages outputs only.
  - Kept `AGENTS.md` as a useful lightweight agent entrypoint and reduced duplicated project details.
  - Updated README, architecture, roadmap, implementation status, and ADRs to reflect the new documentation layout.
- Files modified:
  - `AGENTS.md`
  - `README.md`
  - `project_docs/implementation_status.md`
  - `project_docs/roadmap.md`
  - `project_docs/architecture.md`
  - `project_docs/decisions.md`
  - `project_docs/session_log.md`
- Tests run:
  - `python3 -B scripts/validate.py` passed and validated 34 conferences.
  - `python3 -B scripts/build_all.py` passed, validated 34 conferences, and regenerated the expected HTML and ICS outputs.
- Remaining tasks:
  - None for the documentation layout cleanup.
- Suggested next step: Keep `AGENTS.md` short and use `project_docs/` for durable project state.

## 2026-07-08

- Objective: Refresh the core conference database and tune the public webpage presentation for sharing.
- Tasks completed:
  - Reviewed the 34-entry core conference list from `data/core_conferences_normalized_tags.xlsx` against official conference websites.
  - Updated `data/conferences.yml` with refreshed official dates, deadlines, source URLs, confidence states, notes, and `last_checked` metadata.
  - Changed the TS4H size label from `S/focused` to `S`.
  - Adjusted the Upcoming Conferences table so the Confidence header has more room.
  - Reworded the estimated-entry explanation in the generated page footer and confidence tooltip.
  - Regenerated the GitHub Pages HTML and all committed ICS feeds.
- Files modified:
  - `data/conferences.yml`
  - `data/metadata.yml`
  - `scripts/build_site.py`
  - `docs/index.html`
  - `docs/*.ics`
  - `docs/conferences/*.ics`
  - `docs/tags/*.ics`
  - `project_docs/implementation_status.md`
  - `project_docs/session_log.md`
- Tests run:
  - `python3 scripts/validate.py` passed and validated 34 conferences.
  - `python3 scripts/build_all.py` passed, validated 34 conferences, and regenerated the expected HTML and ICS outputs.
  - A YAML sanity check confirmed all 34 entries have `last_checked: 2026-07-08` and no remaining `S/focused` labels.
- Remaining tasks:
  - Continue periodic review for entries that remain intentionally marked `estimated`.
- Suggested next step: Share the updated GitHub Pages calendar after the pushed commit is published.
