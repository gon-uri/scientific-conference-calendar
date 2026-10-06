# Venue Radar Proposal

Date: 2026-10-06

## Status

Approved and implemented as Venue Radar. Option 2 was refined into a bespoke
calendar/radar mark with a sector-shaped sweep. The active mark now has a
unified light blue radar and a muted red location dot; the original amber
version remains archived. The geometry is unchanged by the approved pixel recolor.
The canonical catalog, website, workbook, README, licenses, and maintenance
documentation now reflect the approved package. Giscus prerequisites are
confirmed by the official checker and the published comments widget renders.

## Resolved Choices

- Selected public name: Venue Radar. Keep the existing repository name and URL.
- Selected logo: option 2, the calendar with a radar inside, regenerated and
  refined after the user's sector-sweep feedback. It remains text-free.
- Second tab: a world map and date-sorted conference table; no submission status
  column there. The submission-opportunities checkbox applies to deadlines only.
- License selection: MIT for project code; CC BY 4.0 for original content.
  Preserve applicable third-party notices and exclude third-party material and
  unprotectable facts from claims of ownership.
- Comments: Giscus, backed by GitHub Discussions; repository/app setup verified.
- Add all eight proposed series: L4DC, IFAC SYSID, IEEE CDC, ACC, NOLTA,
  SIAM DS, CCS, and NetSci. Clearly distinguish paper routes from presentation
  abstract routes, and respect each series' recurrence.
- Hierarchical topics: broad families, automatically derived from up to four
  accurate central subtopics per conference. Do not force four tags.
- Author: Gonzalo Uribarri, Assistant Professor at the Department of Computer
  and Systems Sciences, Stockholm University (wording requested by the author).
- GitHub: https://github.com/gon-uri
- X: https://x.com/gonzauri
- Department: https://www.su.se/english/divisions/department-of-computer-and-systems-sciences
- Google Scholar: https://scholar.google.com/citations?user=q5sweuIAAAAJ&hl=en
- SU profile: https://www.su.se/profiles/g/gour8957

## Implemented Package

- Normalize sizes to S, M, L, XL, XXL and order the filter accordingly.
  Mixed-label mapping: S/M to M, M/L to L, L/XL to XL.
- Keep location out of the deadline table. Show only officially confirmed future
  dates and cities on the map, group markers by city, support keyboard and touch,
  and synchronize markers with shared filters. Keep estimated editions in the
  conference table and past editions separate.
- Refine typography, spacing, neutral dividers, and a restrained teal accent;
  preserve semantic status colors and improve mobile layouts.
- Simplify README with a prominent website link, short project description,
  author links, and license summary. Move technical material into project_docs.
- Remove per-row deadline-table calendar downloads, reallocating width mainly
  to Next milestone. Retain global and conference-tab downloads.
- Add a compact request to star the repository and follow the author's X account.
- Add Giscus and a structured conference-request link.
- Audit the topic assignments from official scopes, preserve existing feed URLs
  when labels change, and keep topic metadata easy to review and maintain.
- Synchronize the workbook, update architecture/status/decisions/maintenance docs,
  validate, build, test desktop/mobile behavior, then commit, push, and verify
  publication. Verification outcomes are recorded in the session log.

## Responsible AI Coverage Review

The current 63-series catalog contains 13 series tagged Fairness & Responsible AI
and 10 tagged Explainability & Interpretability, with 21 distinct series in their
union. These existing tags are not evidence that all 21 specialize in the area.

Two already tracked series clearly specialize in this area:
- ACM FAccT: https://facctconference.org/2026/cfp.html
- AIES: https://www.aies-conference.com/2026/call-for-papers/

ACML explicitly lists trustworthy ML, explainability, fairness, privacy, robustness,
and AI safety: https://www.acml-conf.org/2026/calls/papers/

Approved and implemented: a seventh broad family,
Responsible & Trustworthy AI, with separate subtopics for fairness/accountability,
explainability/interpretability, ethics/governance, privacy-preserving ML, and
robustness/safety. Conference tagging must reflect central advertised scope,
not merely a possible application.

Federated & Distributed Learning belongs under ML & AI rather than being
automatically classified as ethics. Federated learning can be privacy-related
but does not itself imply privacy, fairness, or ethical guarantees. KDD explicitly
includes federated learning in its systems scope:
https://kdd2027.kdd.org/research-track-call-for-papers/
ICLR proceedings also demonstrate relevant coverage:
https://proceedings.iclr.cc/paper_files/paper/2026/hash/b7988dbf1eb774d60fbe71e7d9d672c5-Abstract-Conference.html

There is no currently tracked conference series dedicated to federated learning;
it is an ML subtopic, not a separate broad family.

## Selected Logo Refinement

Mode: reference-image edit, built-in image generation, transparent background.
Source: the selected calendar/radar candidate, refined twice; the final edit
replaced the thin ray with a filled sector after the user's explicit feedback.
Original generation: `assets/venue-radar-original.png`. The pre-recolor 256px
source is `assets/branding/venue-radar-source.png`; the active header/favicon
asset is `assets/venue-radar.png`. No vector reconstruction or SVG tracing was used.

Original Generation Prompt (2026-10-06):

> Use case: logo-brand / precise-object-edit. Edit the attached calendar-radar
> logo into a more distinctive, stylish tech brand mark for Venue Radar. Keep
> the instantly recognizable calendar outline with two binding tabs and a radar
> inside. Replace the single thin ray with a clear triangular circular-sector
> sweep (pizza-slice shape), pointed at the radar center and widening to a curved
> outer edge toward the upper right. The muted amber detection dot must sit
> INSIDE this teal wedge, not at its tip or outside it. Give the symbol a bespoke
> silhouette: slightly squared outer calendar corners with thoughtful rounded
> inner corners, two neat offset radar arcs, intentional negative-space breaks,
> and balanced unequal stroke weights. It should feel like a crafted
> contemporary tech/game-company logo, not a stock UI icon. Keep it simple
> enough to recognize at 48px, with no tiny decorative detail. Color harmony:
> charcoal #263238 calendar, deep teal #137C82 arcs, a lighter muted teal sweep
> sector, amber #D8A33A detection dot. Flat clean graphic mark, subtle two-tone
> layering is welcome but NO glow, gradients, bevel, texture, shadow, 3D or
> mockup. Genuine transparent background, square composition, compact 8 percent
> margin, no text, no watermark. One finished standalone logo.

### Four-Color Recolor And README Banner (2026-10-07)

The user requested color changes only and approved direct pixel processing
to prevent shape drift. Two built-in image-editor trials were not adopted:
their edges/shading were not exact enough for this requirement.

Active palette: border #263238; arcs, radar center and sweep #38A6B0;
location dot #C85C62; calendar interior #FFFFFF. scripts/recolor_logo.mjs
preserves every original nontransparent foreground pixel's alpha and position,
maps its RGB to the selected palette, and fills transparent interior space
between the existing calendar sides. The exterior and the space above the
binding tabs stay transparent. Assertions verify exactly four nontransparent
RGB colors, unchanged foreground edge coverage, and opaque white interior/header.
Browser rendering retains alpha antialiasing; no shape is traced or redrawn.

The 1400x175 white banner at assets/branding/venue-radar-banner.png pairs this
logo with the real Audiowide face at native weight 400. It uses the website's
logo/title proportions and optical alignment, scaled by 1.5. It appears first
in README, spans the content width, and links to the calendar. The prominent
text link follows it. scripts/build_readme_banner.mjs regenerates the PNG;
development.md documents both optional commands. Neither trial image nor
additional font family is included in the public page.

## Logo Candidates

Generated with the built-in image-generation tool. All three are symbol-only
transparent PNGs, suitable for pairing with an HTML/README wordmark. The originals
are 1254 x 1254 pixels and have an alpha channel. Option 2 is selected; optimize
it for small display during implementation. The candidate filenames and prompts
retain the earlier Conference Radar working name as generation provenance.

1. assets/branding/candidates/conference-radar-01-sweep.png: radar sweep.
2. assets/branding/candidates/conference-radar-02-calendar.png: calendar radar.
3. assets/branding/candidates/conference-radar-03-network.png: research network.

### Prompt 1

Use case: logo-brand. Create one polished, compact symbol-only logo for an academic conference calendar called Conference Radar. Concept 1: a minimalist radar sweep identifying upcoming research opportunities. A nearly complete charcoal circular outline, two restrained concentric teal arcs, one crisp teal scanning ray, and two small amber/teal detection points; inventive but immediately readable, with a balanced open silhouette. Professional editorial identity for a sober scientific tool, not military or gaming. Flat vector-like artwork, consistent line weight, no gradients, no glow, no shadows, no 3D, no mockup, no text, no watermark. Genuine transparent background. Square composition with modest clear margins. Design must remain recognizable at 40 to 64 pixels. Return one standalone PNG logo, not a contact sheet.

### Prompt 2

Use case: logo-brand. Create one polished compact symbol-only logo for Conference Radar, an academic conference and submission deadline calendar. Concept 2: a clean calendar page fused with a radar scanner. Minimal charcoal outline of a calendar with two short top binding strokes, generous negative space, and inside it a teal quarter-circle radar sweep with two simple concentric arcs and a single small amber event point. Distinct from a plain radar circle: the calendar silhouette must be clearly recognizable. Refined, sober scientific identity. Flat solid colors, consistent medium-weight strokes, no gradient, no glow, no shading, no 3D, no text, no watermark, no mockup. Genuine transparent background. Square composition, centered, modest clear margins. Readable as a tiny 40 to 64 pixel header mark. Return a single standalone PNG logo, not a contact sheet.

### Prompt 3

Use case: logo-brand. Create one sophisticated compact symbol-only logo for Conference Radar, a scientific conference discovery calendar spanning ML, neuroscience, signal processing, dynamics and control. Concept 3: a research constellation being detected by a radar. A crisp open charcoal ring surrounds three asymmetric teal nodes connected by two fine straight charcoal segments, with one amber node near an outward diagonal teal radar pointer. The nodes and connection lines should suggest a small scientific network, not an atom, molecule, brain or globe. A single incomplete inner arc suggests scanning; sparse well-balanced geometry and generous negative space. Distinct from a standard radar dial or a calendar icon. Flat vector-like design, solid charcoal teal and amber colors only, no gradients, no glow, no shadows, no shading, no 3D, no text, no watermark, no mockup. Genuine transparent background. Square centered composition with modest clear margins. Strong silhouette and readable at 40 to 64 pixels. One standalone PNG symbol, not a contact sheet.
