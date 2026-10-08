# Session Log

## 2026-10-08 (complex systems and neuroscience expansion)

- Objective: Add the approved 16 series, including AREADNE, SfN and all five
  regional Dynamics Days branches, without changing the eight topic families
  or how the website presents abstract-only opportunities.
- Implemented: 22 sourced edition records, 16 curated scope profiles and central
  family assignments, three focused subtopics and confirmed city identities.
  The catalog now contains 166 editions across 129 series, 43 subtopics and
  79 scope profiles. Canonical YAML and all three workbook tables agree.
- Evidence: Confirmed meeting dates do not confer certainty on proxy submission
  dates; estimates and date-only cutoff precision stay explicit. Biennial
  AREADNE/SAB and regional Dynamics Days recurrence are respected. NODYCON,
  Dynamics Days Asia-Pacific and Dynamics Days CAC have no reliable next
  edition announcement and remain in the existing monthly review queue.
  ICCN's conflicting dates are provisional and excluded from the confirmed map.
- Publication formats: dynamics_neuroscience_expansion.md distinguishes full
  papers, abstract books, archived abstracts and selected journal publication.
  Abstract-only routes use the existing milestone labels and submission status;
  no publication badge, column, filter or new status was added. Renderer,
  JavaScript, CSS, README and the eight family names/order are unchanged.
  No unsupported ICORE/CCF ranks or acceptance percentages were invented.
- Verification: 166 records validate; all 81 Python tests and full browser smoke
  pass at 1440/1051/1050/768/390/320px, including all 26 submission-route fixtures,
  mobile disclosures and the new abstract/estimate/archive/scope/map scenarios.
  Desktop/mobile and workbook previews were inspected. Re-import confirms
  129 catalog rows, 43 vocabulary rows and 79 profiles, with original values
  and native tables preserved. Repeated builds are byte-identical. All 212
  feeds pass CRLF/folding/UID checks; every event in the 187 previous feeds and
  all 144 previous records are unchanged. Non-ICS diff whitespace checks pass;
  legitimate folded ICS content spaces are preserved.

## 2026-10-07 (mobile card hierarchy refinement)

- Objective: Make expansion controls quieter, field labels easier to read,
  and the boundary between successive conference cards clearer.
- Implemented: Mobile-only 36px More info / Less info controls with 4px vertical
  padding and white backgrounds; 13px darker bold field labels; pale teal
  Conference headers; stronger existing 1px outlines; 14px inter-card gaps.
  Both tabs and archived editions share the treatment. Desktop styles, card
  disclosure behavior, filter defaults and all conference data remain unchanged.
- Regression coverage: Existing Python checks cover the embedded mobile rules;
  browser tests verify control dimensions, labels, backgrounds, outlines and
  spacing in both tabs plus desktop isolation at the 760/761px boundary.
- Verification: 144 records validate; 73 Python tests and full browser smoke
  pass at 1440/1051/1050/768/390/320px, including all 26 submission-route fixtures
  and the mobile disclosure/fallback suite. Phone previews were inspected;
  two HTML builds are identical. All 187 feeds, canonical data/workbook, branding,
  README and JavaScript/build logic are unchanged. Git diff checks pass.

## 2026-10-07 (compact mobile cards and collapsed filters)

- Objective: Reduce mobile card height while retaining all conference details,
  and start Filters & search collapsed only on mobile.
- Implemented: At up to 760px, deadline cards show Conference / Submission status
  / Time left; conference and past-edition cards show Conference / Dates /
  Location. More info / Less info reveals the other five fields independently.
  Native keyboard controls, per-row aria-controls IDs, minimum 44px targets and
  a pinned Lucide chevron support accessibility. Desktop tables stay complete.
- State: Expansion survives filtering, sorting, tab changes and resizing; the
  milestone arrow remains independent. Filter defaults depend on initial width,
  not subsequent resizing. Clear filters does not reset disclosure state.
  Without JavaScript all metadata remains accessible and inert buttons are hidden.
- Verification: 144 records validate; all 73 Python tests and full browser smoke
  pass at 1440/1051/1050/768/390/320px, with 26 submission-route fixtures. The new
  mobile suite checks 760/761px boundaries, independent expansion in both tabs,
  keyboard/focus, filter/tab/resize persistence, nested schedules, archived cards
  and no-JavaScript fallback. Collapsed/expanded mobile screenshots were inspected.
  Desktop screenshots retain the original table layout; two HTML builds are
  identical. All 187 calendar feeds, conference data/workbook, branding and
  README are unchanged. Git diff whitespace checks pass.
- Publication: c4e2194 pushed to main. Build 37616467131 and Pages 37616466778
  passed; live HTML matched the tested output and the full live browser suite
  passed, including independent mobile cards and responsive filter defaults.

## 2026-10-07 (semibold conference names)

- Objective: Give the primary scanning anchor more emphasis without increasing
  its size or changing the restrained palette.
- Implemented: One scoped weight-600 CSS rule for conference-name links in
  both tables, including archived editions. Font size, color, other links,
  metadata, filters, data and calendar feeds are unchanged.
- Regression coverage: Python checks the embedded rule has only a weight
  declaration; browser smoke checks computed weight/inherited size for both
  tables and text bounds at all six desktop/mobile widths.
- Verification: 144 records validate; 72 Python tests and full browser smoke
  pass at 1440/1051/1050/768/390/320px, including 26 submission-route fixtures.
  Desktop/mobile screenshots were inspected and two HTML builds are identical.
  All 187 calendar feeds, conference data/workbook, artwork and README remain
  unchanged. Git diff whitespace checks pass.
- Publication: 9fede14 pushed to main. Build 37615023780 and Pages 37615023074
  passed; live HTML matched the tested output and live browser smoke passed
  at all six widths.

## 2026-10-07 (filters expanded by default)

- Objective: Show Filters & search expanded on first load.
- Implemented: Added the native open attribute, retaining keyboard toggling,
  resize-state preservation and Clear filters behavior. The default submission
  opportunities selection and individual topic-family disclosure states are
  unchanged. Current state docs and ADR-025 record the revised default.
- Regression coverage: Python checks the open attribute; browser smoke checks
  default visibility and bounds at six widths before exercising the existing
  collapsed-panel, clearing, keyboard and filtering scenarios.
- Verification: 144 records validate; 71 Python tests and full browser smoke
  pass at 1440/1051/1050/768/390/320px, including 26 submission-route fixtures.
  Default-open desktop/mobile screenshots were inspected; two HTML builds are
  identical. All 187 calendar feeds, canonical data/workbook, artwork and
  README remain unchanged from the preceding release.
- Publication: f6a82ad pushed to main. Build 37613958168 and Pages 37613956917
  passed; live HTML matched the tested output and live browser smoke passed
  at all six widths with the default-expanded filter panel.

## 2026-10-07 (README error and feature invitations)

- Objective: Extend the existing conference-request invitation to welcome
  error reports and feature requests.
- Implemented: Added a concise question and general Open an issue link in the
  same README paragraph, preserving the dedicated conference-request form and
  invitation to website comments. No new issue form, service or website copy
  is introduced. Python checks verify both destinations and the exact invitation.
- Verification: all 71 Python tests pass, including the preserved final
  README disclaimer and both contribution destinations. Generated HTML/ICS,
  canonical data, artwork and build scripts are unchanged in this follow-up.
- Publication: bb6f95c pushed to main. Build 37613440576 and Pages 37613439098
  passed. Remote README and live HTML matched the verified local files;
  live browser smoke passed at all six widths, covering the introduction and
  neuroscience-inclusive X draft from b82823a as well.

## 2026-10-07 (selected introduction and neuroscience sharing)

- Objective: Use the selected Find your next conference sentence exactly,
  and explicitly name ML, AI and neuroscience in the X draft's opening.
- Implemented: Replaced the website subtitle and refined only the sharing
  draft's opening; README's fuller description, remaining X wording and URL
  are unchanged. site_copy.md records the selected option and alternatives;
  sharing.md records the refined draft. State docs and ADR-034 no longer
  describe the introduction as pending.
- Regression coverage: Python and browser checks assert the exact sentence;
  browser smoke also checks subtitle text bounds and separation from the brand
  at all six existing viewport widths. Data, filters, map rules, calendars,
  artwork and typography remain unchanged.
  Sharing checks retain exact decoded draft/URL parameters, the 280-character
  limit and safe new-tab behavior without publishing a post.
- Verification: 144 records validate; all 71 Python tests and the full browser
  smoke pass at 1440/1051/1050/768/390/320px, including all 26 route fixtures.
  Desktop/mobile headers were visually inspected. Two final HTML builds are
  identical; all 187 calendar feeds, canonical data/workbook, artwork, and
  README remain byte-identical to the prior release.
- Publication: b82823a pushed to main. Build 37613193987 and Pages 37613193279
  completed successfully for the selected introduction and refined X draft.

## 2026-10-07 (approved map-tab name and personal-project clarification)

- Objective: Apply Conferences & Map, append the personal-project clarification
  to README's final paragraph and propose five ML/AI-first introductions with
  neuroscience, healthcare, complex systems and control as fields/applications.
- Implemented: Changed only the visible tab label; existing IDs, keyboard
  navigation, filters and map behavior remain. The approved disclaimer follows
  the third-party licensing sentence in the same final README paragraph.
  The website introduction remains unchanged pending selection; site_copy.md
  preserves all five new candidates and the three earlier alternatives.
- Regression coverage: Python verifies the escaped tab label and disclaimer's
  position at the end of the licensing paragraph. Browser smoke checks the
  visible name and existing tab text bounds/interaction at six viewport widths.
  No conference data, calendar feeds, artwork or filter logic is changed.
- Verification: 144 editions validate, 71 Python tests pass, and the full
  browser smoke passes at 1440/1051/1050/768/390/320px with all 26 submission-route
  fixtures. Desktop/mobile views were inspected; the longer tab label fits.
  Two full builds are identical, and all 187 calendar feeds, data/workbook
  and artwork are byte-identical to the previous release.
- Publication: ece1f80 pushed to main. Build 37611875203 and Pages 37611874774
  passed; live HTML matched the tested output and live browser smoke passed
  at all six widths. The working tree was clean after publication.

## 2026-10-07 (header action order and compact attribution)

- Objective: Move the calendar download last/rightmost with its caption below,
  remove the map heading and website affiliation sentence, and remove the
  redundant README department hyperlink. Propose shorter introduction text,
  an explicit map-tab label and a personal-project clarification.
- Implemented: Share on X, Star the repo and All events (.ics) in that order;
  top-aligned desktop buttons and responsive mobile wrapping. The map retains
  its count and accessible label without On the map. Website attribution keeps
  Gonzalo Uribarri and existing profile/license links; README keeps plain-text
  affiliation and the university profile link.
- Choices: Three introduction candidates, recommended Conferences & Map and
  a short README-only personal-project clarification await selection. Current
  introduction and Conferences label remain unchanged. site_copy.md preserves
  proposals and distinguishes them from implemented changes.
- Verification: 144 records validate; 71 Python tests and full browser smoke
  pass at 1440/1051/1050/768/390/320px, including 26 submission-route fixtures.
  New checks verify button order, caption placement, desktop alignment, mobile
  bounds, tab text bounds, retained author profile and accessible map labels,
  removed affiliation/heading and plain-text README department. Desktop/mobile
  header and map screenshots were inspected. All 187 calendar feeds, canonical
  data/workbook and artwork remain unchanged. ADR-034 and state docs are updated.
- Publication: e4583d9 pushed to main. Build 37610525362 and Pages 37610524717
  passed; live HTML matched the verified file and live browser smoke passed
  at all six widths. The working tree was clean after publication.

## 2026-10-07 (filter access, default opportunities and sharing)

- Objective: Remove the duplicate Time series shortcut, keep Clear filters
  accessible when collapsed, fit eight topic families, default to submission
  options, and add header sharing/star links with a simpler browser-tab identity.
- Implemented: Clear filters is outside details and aligned with its heading,
  never opens the panel, and keeps focus on itself when Search is hidden.
  The tree fits all eight collapsed families within its 20rem maximum;
  expanded children scroll internally. Time series stays as a normal subtopic
  with unchanged union matching and feed membership.
- Selected copy: Show submission options only starts checked, preserving all
  four eligible route states. Unchecking or Clear filters reveals all future
  editions, including closed/unannounced ones. The restriction is deadlines-only.
  User selected the first X introduction; both proposals are kept in sharing.md.
- Header: download, Share on X and Star the repo are grouped and responsive.
  Sharing opens an encoded draft with the approved short text and canonical
  website link; no post or star is submitted automatically. Pinned Lucide
  share/star SVGs use the existing license. No social widget/API is introduced.
- Branding: a small native SVG radar on opaque white supplies the favicon.
  Main logo, README banner, font and artwork palette are unchanged. The favicon
  was rendered and inspected at 16/32/64px, with 32px white-corner/nonblank checks.
- Verification: 144 records validate; 70 Python tests and browser smoke pass
  at 1440/1051/1050/768/390/320px. Checks cover default 76-opportunity membership,
  collapsed clearing/focus, heading alignment, all-eight-family visibility,
  expanded internal scrolling, retained Time series matching, exact sharing
  parameters, safe new-tab links, responsive header bounds and prior route tests.
  Desktop/mobile views were visually inspected. Two builds are identical;
  all 187 calendar feeds, conference data/workbook and main artwork are unchanged.
  ADR-033, architecture, status, roadmap, topic audit and maintainer guidance
  document the current behavior.
- Publication: b4c31e0 pushed to main. Build 37608172074 and Pages 37608170301
  passed; live HTML matched the tested build and full live browser smoke passed
  at all six widths.

## 2026-10-07 (submission-focused countdown and honest opening states)

- Objective: Align submission status, Time left and the collapsed track/action,
  preserving the full schedule and chronological placement of closed editions.
- Implemented: the earliest required contribution action drives eligible rows,
  including mandatory abstract/registration gates. Organizer proposals, portal
  openings, commitments, notifications and production steps remain expanded
  details, not fresh-submission countdown targets. Actual workshop papers and
  other research-contribution routes remain eligible.
- Status: evidenced Open, explicit future Scheduled submission and confirmed
  opening-unverified Submission opportunity are green. Inferred timing or
  eligibility remains yellow; Closed to new submissions is red; Deadline
  unannounced is grey. Tooltips explain opening evidence; a scheduled route
  becomes Open at its stored opening time. No author-registration note is
  promoted to opening evidence without verification.
- Examples: AAMAS on Oct 7 counts down to its Nov 5 Blue Sky abstract gate,
  not the closed main-track Oct 8 paper cutoff. MLSys counts down to Oct 30,
  not its Oct 10 opening. After a mandatory abstract gate expires, that track
  cannot count as a fresh opportunity. Closed rows say Closed in Time left;
  their schedule fallback still places them between earlier/later opportunities.
- Verification: 144 records validate; 68 Python tests pass. Browser smoke passes
  at 1440/1051/1050/768/390/320px, including AAMAS/MLSys transitions and 26
  focused route fixtures. Opportunity membership remains 76 on the frozen
  Oct 6 clock. Every visible edition's countdown/summary pairing is checked;
  desktop/mobile views and corrected status rows have been visually inspected.
  All 187 ICS feeds are byte-identical to the previous release; two HTML builds
  are identical. Conference YAML, metadata/workbook and calendar UIDs/dates
  are untouched. ADR-032 records the new contract and supersedes the relevant
  parts of ADR-016; maintenance and developer instructions are synchronized.
- Publication: d02f114 pushed to main. Build 37605902067 and Pages 37605901201
  passed; the live HTML matched the tested build and the full browser smoke
  passed against the live page at all six widths.

## 2026-10-07 (eight-topic filters and language/robotics expansion)

- Objective: Implement the approved eight-topic map and all 16 selected series,
  preserving concise main tags, richer curated scope and deferred candidate memory.
- Added: ACL, EMNLP, NAACL, COLING, CoNLL, LREC, IJCNLP, SIGIR, ECIR, RecSys,
  WWW, COLM, ISWC, ICRA, RSS and SMC. Their 22 editions bring the catalog to
  144 editions / 113 series. Added five focused agent/retrieval/recommender/graph
  leaves and eight city aliases. Existing CIKM/WSDM received reviewed profiles;
  profile coverage is 63 / 113 with 50 missing profiles explicitly queued.
- Taxonomy: eight families and a Time series shortcut; complete curated
  central identities for every series. Whole-family matching is distinct from
  broader specific-leaf matching. Four main topics remain visible; additional
  topics and prose remain curated, not imported from catch-all CFP lists.
  The long complex-systems label stays one line; topic filters occupy their own
  row below 1200px with tighter spacing only on very narrow screens.
- Evidence: direct ICORE/CCF totals are 66/55. Four new track-specific historical
  rates bring evidence coverage to 34; twelve new rates remain Unknown. Sources
  and denominator limitations are recorded in nlp_robotics_expansion.md.
- Dates: SIGIR proposed schedules, SMC proposal dates and unpublished next
  editions remain estimated. LREC is biennial; NAACL/COLING/IJCNLP do not get
  automatic annual projections. ARR commitments and RSS invited final papers
  cannot masquerade as fresh opportunities. ECIR resources are an independent
  archival route. ICRA PST wording and SMC camera-ready conflicts are flagged.
- Backlog: all 57 original candidates retained, 42 added and 15 deferred;
  ICWM remains separate. Respected deferred HCI venues are not called minor.
- Workbook: synchronized and re-imported 113 exact catalog rows, 40 vocabulary
  leaves and 63 profiles. Native table names/styles, existing row order,
  definitions and unrelated catalog values preserved. Rendered catalog,
  vocabulary and new scope profiles visually checked.
- Verification: 144 records validate; 68 Python tests pass. Browser smoke passes
  at 1440/1051/1050/768/390/320px with 76 opportunities on its frozen Oct 6 clock,
  one central ML/dynamics intersection, and 84 confirmed future editions in 68
  mapped cities. ARR/RSS/ECIR gates, new leaves, central-versus-method matching,
  shortcut clearing and single-line labels all pass. Rendered views checked.
- Calendar preservation: all 187 feeds satisfy CRLF and 75-octet folding.
  Existing UIDs, timing and non-description properties remain unchanged;
  599 memberships are added, seven AAMAS evolutionary memberships deliberately
  removed, and 126 old feeds are byte-identical. Original edition fields are
  unchanged except AAMAS/LoG main-topic refinements. A second build is identical.
- Publication: release d869465 pushed to gon-uri/venue-radar/main. Build run
  37603403662 and Pages run 37603401667 both completed successfully. The live
  HTML is byte-identical to the release, and the full browser smoke passes
  against the published page at all six widths. All 30 aggregate/new-series/
  new-topic feed downloads return 200 and match the local files byte-for-byte.
  Working tree was clean after the release; this verification record is a
  documentation-only follow-up, with no generated-output changes.

## 2026-10-07 (AI, vision, multimedia and biometrics expansion)

- Objective: Add the three selected AI/methodology venues, all remaining
  Vision, Imaging and Multimedia candidates, and every dedicated biometrics
  venue in the 46-entry backlog. FG and IJCB satisfy the last request within
  the same batch; BTAS/ICB are not duplicated as separate IJCB predecessors.
- Added: EuroGP, KR, ICAPS, 3DV, ACM MM, ACM SIGGRAPH, BMVC, CVPR, ECCV,
  EUVIP, FG, ICCV, ICMR, IJCB, and WACV. There are 18 new edition records,
  bringing the catalog to 122 editions / 97 series. The original AI Deadlines
  gap now has 26 tracked and 31 untracked series; ICWM remains separate.
- Evidence: official meeting and CFP pages, direct ICORE2026 entries,
  the CCF 2026 seventh edition, and track-specific organizer acceptance
  statistics. Mapping totals are 52 ICORE, 43 CCF, and 30 acceptance series.
  Ten additions remain Unknown for acceptance; ranks do not imply rates.
  Size approximations are labeled as editorial unless attendance is sourced.
- Dates and routes: FG's Oct 5 extension is reflected in its Oct 23/30
  abstract/paper cutoffs; IJCB's Mar 15 opening and Apr 9 paper deadline are
  confirmed. WACV rounds retain independent abstract prerequisites. Poster
  assets, checksum uploads, supplementary files, and camera-ready deadlines
  do not become fresh paper routes. Missing precise deadline hours stay
  date-only. The ICCV official-page conflict is documented for reconciliation.
- Estimates: ECCV and ICCV retain biennial cadence; other additions follow
  their reviewed annual pattern. Completed ECCV/EUVIP editions are archived
  alongside next-edition estimates. KR and ACM MM announced hosts do not
  confirm their estimated meeting dates, so those editions stay off the map.
  No unverified portal-open observation is fabricated.
- Discovery: five focused leaves bring the vocabulary to 35 within the same
  seven families. Biometrics & Human Sensing identifies FG and IJCB and
  relevant broader vision scopes. Detailed profiles now cover 45 / 97 series;
  the original 52 missing profiles remain queued. Tables still show at most
  four main topics. Ten city aliases and the concise site description were
  updated for the expanded coverage.
- Preservation: all 104 old edition records, 30 old profiles, and existing
  rank/acceptance mappings remain exactly unchanged. The re-imported workbook
  contains 97 exact catalog rows, 35 leaves, and 45 exact profiles; original
  catalog values, original definitions, and native table names/styles survive.
  Workbook previews were visually checked, including the biometrics profile.
- Verification: 122 records validate; 62 Python tests and the full build pass.
  Browser checks cover both tabs, new subtopics, biometrics, WACV transitions,
  map eligibility, and overflow at 1440/1051/1050/768/390/320px. All 160 feeds
  satisfy CRLF/folding checks. Against the prior commit, every existing event
  property in 137 feeds is unchanged; 501 memberships are added and 118 feeds
  remain byte-identical.
- Maintenance and publication: vision_ai_expansion.md records official
  sources, relevance distinctions, caveats, and prioritized monthly checks.
  Candidate memory, topic audit, architecture, status, roadmap, maintenance,
  and ADR-029 are synchronized. Source, workbook, tests, documentation, and
  generated HTML/ICS are prepared together for the existing main/docs release.

## 2026-10-07 (curated detailed conference scopes)

- Objective: Preserve richer topic/scope metadata without expanding the four
  visible tags or blindly copying enormous organizer CFP inventories.
- Implemented: conference_scopes.yml and a series-profile module with up to
  six characteristic additional leaves, concise scope prose, official evidence
  URLs/year, and an independent review date. Missing profiles are legal and
  fall back to main topics. Canonical edition data, dates, rankings, rates,
  recurrence patterns, and submission statuses remain unchanged.
- Coverage: 30 of 82 series reviewed, including all 11 recent AI Deadlines
  additions. The 52 missing profiles remain explicitly queued. Several profiles
  retain prior-edition evidence; GECCO's 2027 URL currently serves a 2026 CFP.
  No new conference series or controlled subtopic was added in this session.
- Curation: characterize the research community and contribution focus, not
  every imaginable application. Broad ML venues do not gain blanket healthcare
  or neuroscience tags. ICIP's application inventory is not copied wholesale;
  incidental MLSys fairness/interpretability entries are not defining tags.
  Zero extra topics is valid and the six-topic cap is not a target.
- Discovery: search uses scope prose and the primary/additional topic union;
  hierarchical filters and map matching use the same union in both tabs.
  Tables remain primary-only. Topic feeds match the union and descriptions
  include scope provenance; existing event UIDs/timing stay stable.
- Maintenance: added the third scope queue for missing, stale, or prior-edition
  profiles; documented editorial rules and monthly reviews in conference_scopes.md,
  data_maintenance.md, architecture, status, roadmap, ADR-028, and AGENTS.
- Workbook: added the separate Conference Scope sheet with 30 profiles, native
  table formatting, wrapped prose, and real review dates. Rendered and re-imported
  the result; the original 82-series catalog and 30-leaf vocabulary values,
  formulas, and native table names/styles remain unchanged.
- Verification: all 104 editions validate; 50 Python tests and the full build
  pass. Browser smoke passes at 1440/1051/1050/768/390/320px, including LoG
  graph-kernel search, AutoML Bayesian-optimization search, extra-topic matching,
  primary-only labels, both tabs, map matching, and existing UI regressions.
  Compared all 137 feeds with the prior commit: every existing event property
  except DESCRIPTION is unchanged; 438 topic-feed memberships were added and
  70 feeds remain byte-identical. CRLF and 75-octet folding are preserved.
- Publication: source, workbook, documentation, tests, and generated HTML/ICS
  are committed together for main/docs publication. Scope completion remains
  ongoing editorial work; this is not a claim that all 82 profiles were reviewed.

## 2026-10-07 (AI Deadlines additions and candidate backlog)

- Objective: Add the 11 recommended venues, preserve the other audit candidates,
  and extend subtopics only where the new venues need focused classifications.
- Added: AutoML, LoG, CoRL, GECCO, SaTML, ProbML, AAMAS, MLSys, CogSci, ICIP,
  and Interspeech. Catalog now has 104 editions / 82 series. Existing 93 edition
  records and their per-edition feeds remain unchanged.
- Evidence: official organizer meeting/CFP pages, CoRL's public OpenReview
  metadata, ICORE 2026 export, CCF 2026 catalog, and organizer/proceedings rate
  statistics. AutoML/ProbML meeting projections and GECCO/CogSci submission
  projections remain estimated. ICIP/Interspeech date-only cutoffs emit all-day
  ICS events. Source discrepancies and outstanding checks are documented.
- Metadata: three new central leaves within the existing seven families;
  eight new city aliases; explicit annual cadence for all additions. Rank maps
  now cover 39 ICORE and 31 CCF series. Historical rate evidence covers 25
  series, adding AutoML 2024, LoG 2023, and AAMAS 2026; unsupported rates stay
  Unknown. Size approximations are explicitly noted, not attendance claims.
- Tracks: AAMAS main and Blue Sky Ideas use independent prerequisite gates.
  Registered-only main papers have an explicit milestone label. Interspeech
  Show & Tell is separate; paper updates, camera-ready, and SaTML revisions
  are not fresh submission routes.
- Candidate memory: conference_candidates.md, linked from AGENTS and roadmap,
  preserves all 57 originally missing series: 11 added and 46 still untracked.
  ICWM is separate (future-only). The source retained no 2024 entries; the
  limitation and all candidate names, official links, and visible years are
  recorded. The 46-entry backlog exactly matches the remaining snapshot gap.
- Workbook: synchronized and re-imported 82 series / 30 vocabulary leaves,
  preserving native tables/order, verified exact canonical values, checked for
  formula errors, and visually inspected both sheets. New long type cells wrap.
- Verification: validation, 42 Python tests, full build, idempotent rollover,
  maintenance queue, and desktop/mobile browser checks pass. Browser scenarios
  cover independent tracks, openings, expired gates, subtopics, ranks, map
  markers, and overflow at 1440/1051/1050/768/390/320px. Generated feeds retain
  their existing deterministic UID namespace and RFC-required folding/CRLF.
- Publication: source, workbook, docs, tests, and generated HTML/ICS are committed
  together for main/docs publication. No additional backlog venue is approved.

## 2026-10-07 (repository rename migration)

- Objective: Adapt the project after the user renamed the GitHub repository
  from scientific-conference-calendar to venue-radar.
- Completed: README website/banner/request links, content attribution, public
  request/discussion/star/license links, Giscus repository name, and local Git
  origin now use gon-uri/venue-radar. Pages still publishes main/docs and its
  configured homepage is https://gon-uri.github.io/venue-radar/.
- Stable identities: GitHub and Giscus's own category API confirm unchanged
  repository/category IDs and retained Discussions support. Keep the specific
  Venue Radar community mapping and the published calendar UID namespace.
  Relative download paths work under the new Pages base. Existing subscribers
  must update old absolute feed URLs; no replacement legacy repository is made.
- Verification: all 93 records validate; 34 Python tests and the full build
  pass. Browser checks pass at 1440/1051/1050/768/390/320px, including new links,
  injected Giscus settings, relative calendar paths, and unchanged UI behavior.
  All 123 ICS feeds and canonical data are unchanged. No old navigable project
  URLs remain in maintained sources or generated HTML. The workbook contains
  no obsolete project URL and needs no modification.
- Publication: sources, migration notes, regression checks, and generated
  HTML are committed together for the renamed repository's existing Pages setup.

## 2026-10-07 (open submission status simplification)

- Objective: Remove the leading dot from open submission statuses and publish.
- Completed: removed the CSS pseudo-element from the site generator. Open
  abstract and paper labels retain their wording, bold green text, and pale
  green background. Submission logic, filtering, and all conference data stay
  unchanged.
- Regression coverage: browser checks assert both open label types are present,
  have no leading pseudo-element, and preserve their text color and weight.
  Dedicated desktop screenshots capture the abstract and paper examples.
- Verification: all 93 conference records validate, 32 Python tests and the
  full build pass, and browser checks pass at 1440/1051/1050/768/390/320px.
  Both open-status example screenshots were visually inspected. Git confirms
  that conference data and all ICS feeds are unchanged.
- Publication: generator, generated HTML, browser regression, and maintained
  documentation are committed together for the existing main/docs deployment.

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
