# Session Log

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
