from __future__ import annotations

import json
import base64
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

import yaml
from catalog_metadata import CITIES_PATH, CONFERENCE_FAMILIES_PATH, FAMILIES_PATH, load_mapping, map_events, validate_catalog_metadata, validate_conference_families
from conference_scopes import SCOPES_PATH, all_topics, load_scopes, validate_scopes, with_scopes

from validate import (
    DATA_PATH,
    CCF_PATH,
    ACCEPTANCE_PATH,
    ICORE_PATH,
    SUBMISSION_TYPES,
    acceptance_band,
    load_acceptance_rates,
    load_ccf_rankings,
    load_conferences,
    load_controlled_topics,
    load_icore_rankings,
    parse_date,
    parse_datetime,
    stable_slug,
    validate_conferences,
    validate_acceptance_rates,
    validate_ccf_rankings,
    validate_icore_rankings,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
METADATA_PATH = ROOT / "data" / "metadata.yml"
ASSETS_DIR = ROOT / "assets"
TOPIC_CATALOG = load_mapping(FAMILIES_PATH)
CONFERENCE_FAMILIES = load_mapping(CONFERENCE_FAMILIES_PATH)
TIME_ESTIMATE_TOOLTIP = (
    "Official day; exact hour/timezone unannounced. "
    "Countdown uses a provisional calendar time."
)

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def _attr(value: Any) -> str:
    return escape(str(value), quote=True)


def _topic_labels(topics: list[str]) -> str:
    return '<div class="topic-tags">' + " ".join(
        f'<span class="tag" title="{_attr(topic)}">{escape(TOPIC_CATALOG["labels"].get(topic, topic))}</span>'
        for topic in topics
    ) + '</div>'


def _conference_source_url(conference: dict[str, Any]) -> str:
    source_urls = conference.get("source_urls") or []
    if source_urls:
        return source_urls[0]
    return conference.get("cfp_url") or conference["website"]


def _deadline_source_url(
    conference: dict[str, Any], deadline: dict[str, Any]
) -> str:
    return deadline.get("source_url") or _conference_source_url(conference)


def _format_date(value: datetime) -> str:
    return f"{MONTHS[value.month - 1]} {value.day}, {value.year}"


def _deadline_iso_utc(value: Any) -> str:
    parsed = parse_datetime(value)
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _display_deadline_datetime(value: Any) -> str:
    parsed = parse_datetime(value)
    return _format_date(parsed)


def _display_deadline_label(label: str) -> str:
    cleaned = label.strip()
    suffix = " deadline"
    if cleaned.lower().endswith(suffix):
        cleaned = cleaned[: -len(suffix)].rstrip()
    return cleaned


def _display_conference_dates(start_value: Any, end_value: Any) -> str:
    start = parse_date(start_value)
    end = parse_date(end_value)
    if start == end:
        return f"{MONTHS[start.month - 1]} {start.day}, {start.year}"
    if start.year == end.year and start.month == end.month:
        return f"{MONTHS[start.month - 1]} {start.day}-{end.day}, {start.year}"
    if start.year == end.year:
        return (
            f"{MONTHS[start.month - 1]} {start.day} - "
            f"{MONTHS[end.month - 1]} {end.day}, {start.year}"
        )
    return (
        f"{MONTHS[start.month - 1]} {start.day}, {start.year} - "
        f"{MONTHS[end.month - 1]} {end.day}, {end.year}"
    )


def _search_text(conference: dict[str, Any], extra: list[str] | None = None) -> str:
    topics = all_topics(conference)
    parts = [
        conference["series"],
        conference["title"],
        conference["short_title"],
        conference.get("location", ""),
        conference.get("confidence", ""),
        conference.get("size", ""),
        conference.get("submission_type", ""),
        " ".join(topics),
        " ".join(TOPIC_CATALOG["labels"].get(topic, topic) for topic in topics),
        " ".join(family["label"] for family in TOPIC_CATALOG["families"]
                 if family["id"] in CONFERENCE_FAMILIES.get(conference["series"], [])),
        conference.get("scope", {}).get("scope_summary", ""),
    ]
    if extra:
        parts.extend(extra)
    return " ".join(str(part) for part in parts if part)


def _topic_slugs(topics: list[str]) -> str:
    return " ".join(stable_slug(topic) for topic in topics)


def _value_slug(value: Any) -> str:
    return stable_slug(str(value))


def _metadata_label(value: Any) -> str:
    return f'<span class="meta-pill">{escape(str(value))}</span>'


def _icore_cell(conference: dict[str, Any], rankings: dict[str, Any]) -> str:
    entry = rankings.get(conference["series"])
    if entry is None:
        return (
            '<span class="rank-empty" title="No ICORE 2026 main-track rank '
            'is listed for this conference series.">&mdash;</span>'
        )
    rank = entry["rank"]
    url = f'https://portal.core.edu.au/conf-ranks/{entry["portal_id"]}/'
    return (
        f'<a class="rank-link" href="{_attr(url)}" '
        f'aria-label="ICORE 2026 rank {_attr(rank)}" '
        f'title="ICORE 2026: {_attr(rank)}. Applies to main-track full papers.">'
        f"{escape(rank)}</a>"
    )


def _ranking_cell(
    conference: dict[str, Any],
    icore: dict[str, Any],
    ccf: dict[str, Any],
    ccf_page: str,
) -> str:
    ccf_entry = ccf.get(conference["series"])
    if ccf_entry:
        rank = ccf_entry["rank"]
        ccf_html = (
            f'<a class="rank-link rank-link-ccf" href="{_attr(ccf_page)}" '
            f'aria-label="CCF 2026 rank {_attr(rank)}" '
            f'title="CCF 2026: {_attr(rank)}. Main-track full papers only.">'
            f"{escape(rank)}</a>"
        )
    else:
        ccf_html = '<span class="rank-empty" title="No direct CCF 2026 rank">&mdash;</span>'
    return (
        '<span class="rank-pair">'
        f"{_icore_cell(conference, icore)}"
        '<span class="rank-separator" aria-hidden="true">/</span>'
        f"{ccf_html}</span>"
    )


def _acceptance_cell(conference: dict[str, Any], rates: dict[str, Any]) -> str:
    entry = rates.get(conference["series"])
    if entry is None:
        return '<span class="rate-unknown" title="No defensible historical rate is available">Unknown</span>'
    percent = entry.get("percent")
    band = acceptance_band(percent) if percent is not None else entry["band"]
    detail = (
        f'{"~" if entry.get("approximate") else ""}{percent:g}% ({entry["year"]})'
        if percent is not None
        else "(estimated)"
    )
    return (
        '<span class="acceptance-cell">'
        f'<strong>{escape(band)}</strong> '
        f'<a href="{_attr(entry["source_url"])}" '
        f'title="{_attr(entry["track"])}; evidence year {entry["year"]}; {_attr(entry.get("basis", "historical rate"))}">'
        f"{escape(detail)}</a></span>"
    )


def _conference_calendar_href(conference: dict[str, Any]) -> str:
    return f"conferences/{conference['id']}.ics"


def _conference_calendar_link(conference: dict[str, Any]) -> str:
    title = (
        f"Download an ICS calendar file for {conference['short_title']} with "
        "conference dates and deadlines."
    )
    return (
        f'<a class="row-calendar-button" href="{_attr(_conference_calendar_href(conference))}" '
        f'download title="{_attr(title)}" '
        f'aria-label="Download calendar for {_attr(conference["short_title"])}">' +
        (ASSETS_DIR / "vendor" / "download.svg").read_text(encoding="utf-8") +
        "</a>"
    )


def _colgroup(widths: list[str]) -> str:
    columns = "".join(f'<col style="width: {width}">' for width in widths)
    return f"<colgroup>{columns}</colgroup>"


def _filter_attributes(
    conference: dict[str, Any],
    search_text: str,
    icore: dict[str, Any],
    ccf: dict[str, Any],
    rates: dict[str, Any],
) -> str:
    rate = rates.get(conference["series"])
    band = (
        acceptance_band(rate["percent"])
        if rate and rate.get("percent") is not None
        else rate.get("band", "Unknown") if rate else "Unknown"
    )
    deadlines = [
        {
            "type": deadline["type"],
            "label": _display_deadline_label(deadline["label"]),
            "at": _deadline_iso_utc(deadline["datetime"]),
            "gate_for": deadline.get("gate_for"),
            "opens_at": _deadline_iso_utc(deadline["opens_at"]) if deadline.get("opens_at") else None,
            "open_observed_on": str(deadline["open_observed_on"]) if deadline.get("open_observed_on") else None,
            "estimated": deadline.get("confidence", conference["confidence"]) != "confirmed",
            "approximate_time": deadline.get("time_precision") == "date",
        }
        for deadline in conference.get("deadlines", [])
    ]
    return (
        f'data-filter-row data-edition="{_attr(conference["id"])}" data-search="{_attr(search_text)}" '
        f'data-topics="{_attr(_topic_slugs(all_topics(conference)))}" '
        f'data-families="{_attr(" ".join(CONFERENCE_FAMILIES.get(conference["series"], [])))}" '
        f'data-size="{_attr(_value_slug(conference.get("size", "")))}" '
        f'data-icore="{_attr(icore.get(conference["series"], {}).get("rank", "Unranked"))}" '
        f'data-ccf="{_attr(ccf.get(conference["series"], {}).get("rank", "Unranked"))}" '
        f'data-acceptance="{_attr(_value_slug(band))}" '
        f'data-confidence="{_attr(conference["confidence"])}" '
        f'data-conference-start="{_attr(conference["conference_start"])}" '
        f'data-conference-end="{_attr(conference["conference_end"])}" '
        f'data-deadlines="{_attr(json.dumps(deadlines, separators=(",", ":")))}"'
    )


def _milestones(conference: dict[str, Any]) -> list[dict[str, Any]]:
    milestones = []
    for deadline in conference.get("deadlines", []):
        milestones.append({
            "type": deadline["type"],
            "label": _display_deadline_label(deadline["label"]),
            "datetime": deadline["datetime"],
            "estimated": deadline.get("confidence", conference["confidence"]) != "confirmed",
            "approximate_time": deadline.get("time_precision") == "date",
        })
        if deadline.get("opens_at"):
            milestones.append({
                "type": f'{deadline["type"]}_opens',
                "label": f'{_display_deadline_label(deadline["label"])} opens',
                "datetime": deadline["opens_at"],
                "estimated": deadline.get("confidence", conference["confidence"]) != "confirmed",
                "approximate_time": deadline.get("time_precision") == "date",
            })
    milestones.append({
        "type": "conference_start",
        "label": "Conference starts",
        "datetime": f'{conference["conference_start"]}T00:00:00Z',
        "estimated": conference["confidence"] in {"estimated", "not_yet_announced", "stale"},
    })
    return sorted(milestones, key=lambda item: _deadline_iso_utc(item["datetime"]))


def _deadline_grid_rows(milestones: list[dict[str, Any]]) -> str:
    rows = []
    for index, milestone in enumerate(milestones):
        deadline_utc = _deadline_iso_utc(milestone["datetime"])
        row_hidden = "" if index == 0 else " hidden"
        estimate = ' <span class="milestone-estimate" title="Estimated date">(est.)</span>' if milestone["estimated"] else ""
        time_title = ""
        if milestone.get("approximate_time") and not milestone["estimated"]:
            time_title = f' title="{_attr(TIME_ESTIMATE_TOOLTIP)}"'
        rows.append(
            f'<div class="deadline-grid-row" data-deadline-row data-entry-index="{index}" '
            f'data-deadline-type="{_attr(milestone["type"])}"{row_hidden}>'
            f'<time datetime="{_attr(deadline_utc)}"{time_title}>'
            f"{escape(_display_deadline_datetime(milestone['datetime']))}</time>{estimate}"
            f'<span class="deadline-milestone">'
            f"{escape(milestone['label'])}</span>"
            f'<span class="deadline-passed" data-deadline-passed="{_attr(deadline_utc)}"></span>'
            "</div>"
        )
    return f'<div class="deadline-grid" data-deadline-grid>{"".join(rows)}</div>'


def _deadline_group_rows(
    conferences: list[dict[str, Any]],
    icore: dict[str, Any],
    ccf: dict[str, Any],
    ccf_page: str,
    rates: dict[str, Any],
) -> str:
    rows = []
    for conference in conferences:
        milestones = _milestones(conference)
        search_extras = []
        for deadline in conference.get("deadlines", []):
            search_extras.extend(
                [
                    _display_deadline_label(deadline["label"]),
                    deadline["type"],
                    _deadline_source_url(conference, deadline),
                ]
            )
        search_text = _search_text(conference, search_extras)
        group_id = stable_slug(conference["id"])
        toggle_html = ""
        if len(milestones) > 1:
            toggle_html = (
                f"<button class=\"deadline-toggle\" type=\"button\" aria-expanded=\"false\" "
                f"aria-label=\"Show milestones for {_attr(conference['short_title'])}\">"
                "<span class=\"expand-icon\" aria-hidden=\"true\">&#9656;</span>"
                "</button>"
            )
        rows.append(
            f'<tr class="deadline-group-row" {_filter_attributes(conference, search_text, icore, ccf, rates)} '
            f'data-deadline-group="{_attr(group_id)}" data-expanded="false">'
            f"<td data-label=\"Conference\"><a href=\"{_attr(conference['website'])}\">{escape(conference['short_title'])}</a></td>"
            '<td data-label="Submission status"><span class="submission-status" data-submission-status>Checking...</span></td>'
            '<td data-label="Time left"><div class="time-left-cell">'
            '<span class="time-left" data-time-left>&mdash;</span>'
            f'<span class="time-estimate" data-time-estimate hidden title="{_attr(TIME_ESTIMATE_TOOLTIP)}">(time est.)</span>'
            '</div></td>'
            f'<td class="deadline-combined-cell" data-label="Next milestone"><div class="deadline-cell-content">{toggle_html}{_deadline_grid_rows(milestones)}</div></td>'
            f"<td data-label=\"Topics\">{_topic_labels(conference.get('topics', []))}</td>"
            f'<td data-label="Accept. rate">{_acceptance_cell(conference, rates)}</td>'
            f'<td data-label="ICORE / CCF">{_ranking_cell(conference, icore, ccf, ccf_page)}</td>'
            f"<td data-label=\"Size\">{_metadata_label(conference.get('size', ''))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _conference_rows(
    conferences: list[dict[str, Any]],
    icore: dict[str, Any],
    ccf: dict[str, Any],
    ccf_page: str,
    rates: dict[str, Any],
) -> str:
    rows = []
    for conference in sorted(
        conferences,
        key=lambda item: (parse_date(item["conference_start"]), item["id"]),
    ):
        source_url = _conference_source_url(conference)
        search_text = _search_text(conference, [source_url])
        date_estimate = (
            ' <span class="milestone-estimate" title="Conference dates estimated">(est.)</span>'
            if conference["confidence"] in {"estimated", "not_yet_announced", "stale"}
            else ""
        )
        rows.append(
            f'<tr {_filter_attributes(conference, search_text, icore, ccf, rates)} data-conference-row>'
            f"<td data-label=\"Conference\"><a href=\"{_attr(conference['website'])}\">{escape(conference['short_title'])}</a></td>"
            f"<td data-label=\"Dates\">{escape(_display_conference_dates(conference['conference_start'], conference['conference_end']))}{date_estimate}</td>"
            f"<td data-label=\"Location\">{escape(conference.get('location', 'TBD'))}</td>"
            f"<td data-label=\"Topics\">{_topic_labels(conference.get('topics', []))}</td>"
            f'<td data-label="Accept. rate">{_acceptance_cell(conference, rates)}</td>'
            f'<td data-label="ICORE / CCF">{_ranking_cell(conference, icore, ccf, ccf_page)}</td>'
            f"<td data-label=\"Size\">{_metadata_label(conference.get('size', ''))}</td>"
            f"<td data-label=\"Calendar\">{_conference_calendar_link(conference)}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _max_last_checked(conferences: list[dict[str, Any]]) -> str:
    dates = [parse_date(conference["last_checked"]) for conference in conferences]
    if not dates:
        return "unknown"
    latest = max(dates)
    return f"{MONTHS[latest.month - 1]} {latest.day}, {latest.year}"


def _load_metadata(path: Path = METADATA_PATH) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def _dataset_last_updated(conferences: list[dict[str, Any]]) -> str:
    metadata = _load_metadata()
    if metadata.get("last_updated"):
        updated = parse_date(metadata["last_updated"])
        return f"{MONTHS[updated.month - 1]} {updated.day}, {updated.year}"
    return _max_last_checked(conferences)


def _topics(conferences: list[dict[str, Any]]) -> list[str]:
    return sorted(
        {topic for conference in conferences for topic in all_topics(conference)},
        key=lambda value: value.casefold(),
    )


def _unique_values(conferences: list[dict[str, Any]], field: str) -> list[str]:
    return sorted(
        {
            str(conference[field])
            for conference in conferences
            if str(conference.get(field, "")).strip()
        },
        key=lambda value: value.casefold(),
    )


def _checkbox_group(
    label: str,
    group: str,
    values: list[str],
    slug_values: bool = True,
    link_href: str | None = None,
) -> str:
    boxes = []
    for value in values:
        filter_value = stable_slug(value) if slug_values else value
        boxes.append(
            "<label class=\"check-option\">"
            f"<input type=\"checkbox\" data-filter-group=\"{_attr(group)}\" "
            f"value=\"{_attr(filter_value)}\">"
            f"<span>{escape(value)}</span>"
            "</label>"
        )
    heading = escape(label)
    if link_href:
        heading = f'<a href="{_attr(link_href)}">{heading}</a>'
    return (
        "<fieldset class=\"filter-group\">"
        f"<legend>{heading}</legend>"
        f"<div class=\"check-list\">{''.join(boxes)}</div>"
        "</fieldset>"
    )


def _topic_filter() -> str:
    families = []
    for family in TOPIC_CATALOG["families"]:
        children = ''.join(
            f'<label class="check-option"><input type="checkbox" data-filter-group="topics" '
            f'data-topic-family="{_attr(family["id"])}" value="{_attr(stable_slug(topic))}">'
            f'<span>{escape(TOPIC_CATALOG["labels"][topic])}</span></label>'
            for topic in family["topics"]
        )
        families.append(
            f'<details class="topic-family"><summary title="Expand or collapse subtopics"><label class="check-option">'
            f'<input type="checkbox" data-family-toggle="{_attr(family["id"])}" '
            f'title="{_attr("Central conference focus: " + family["label"])}">'
            f'<span>{escape(family["label"])}</span></label></summary>'
            f'<div class="check-list">{children}</div></details>'
        )
    shortcut = ('<label class="check-option topic-shortcut"><input id="time-series-shortcut" '
                'type="checkbox"><span>Time series</span></label>')
    return '<fieldset class="topic-filter"><legend>Topics &amp; Subtopics</legend>' + shortcut + '<div class="topic-tree">' + ''.join(families) + '</div></fieldset>'


def build_site(
    data_path: Path = DATA_PATH,
    docs_dir: Path = DOCS_DIR,
    rankings_path: Path = ICORE_PATH,
    ccf_path: Path = CCF_PATH,
    acceptance_path: Path = ACCEPTANCE_PATH,
    scopes_path: Path = SCOPES_PATH,
) -> Path:
    conferences = load_conferences(data_path)
    icore_data = load_icore_rankings(rankings_path)
    ccf_data = load_ccf_rankings(ccf_path)
    acceptance_data = load_acceptance_rates(acceptance_path)
    scopes = load_scopes(scopes_path)
    errors = validate_conferences(conferences, load_controlled_topics())
    cities = load_mapping(CITIES_PATH)
    errors.extend(validate_catalog_metadata(load_controlled_topics() or set(), TOPIC_CATALOG, cities))
    errors.extend(validate_conference_families(conferences, CONFERENCE_FAMILIES, TOPIC_CATALOG,
                                              allow_extra=data_path != DATA_PATH))
    errors.extend(validate_icore_rankings(conferences, icore_data))
    errors.extend(validate_ccf_rankings(conferences, ccf_data))
    errors.extend(validate_acceptance_rates(conferences, acceptance_data))
    errors.extend(validate_scopes(conferences, scopes, load_controlled_topics() or set()))
    if errors:
        raise ValueError("conference data is invalid; run scripts/validate.py")
    conferences = with_scopes(conferences, scopes)

    docs_dir.mkdir(parents=True, exist_ok=True)
    output = docs_dir / "index.html"
    last_updated = _dataset_last_updated(conferences)
    icore = icore_data["rankings"]
    ccf = ccf_data["rankings"]
    ccf_page = ccf_data["page_url"]
    rates = acceptance_data["rates"]
    logo = 'data:image/png;base64,' + base64.b64encode((ASSETS_DIR / 'venue-radar.png').read_bytes()).decode('ascii')
    title_font = base64.b64encode((ASSETS_DIR / 'vendor' / 'audiowide-latin.woff2').read_bytes()).decode('ascii')
    custom_css = (ASSETS_DIR / 'site.css').read_text(encoding='utf-8')
    leaflet_css = (ASSETS_DIR / 'vendor' / 'leaflet.css').read_text(encoding='utf-8')
    leaflet_js = (ASSETS_DIR / 'vendor' / 'leaflet.js').read_text(encoding='utf-8')
    custom_js = (ASSETS_DIR / 'site.js').read_text(encoding='utf-8')
    map_data = json.dumps({
        'events': map_events(conferences, cities),
        'land': json.loads((ASSETS_DIR / 'vendor' / 'world-land.geojson').read_text()),
        'resetIcon': (ASSETS_DIR / 'vendor' / 'globe.svg').read_text(encoding='utf-8'),
    }, separators=(',', ':')).replace('</', '<\\/')
    download_icon = (ASSETS_DIR / 'vendor' / 'download.svg').read_text(encoding='utf-8')
    vendor_notices = '\n\n'.join(
        (ASSETS_DIR / 'vendor' / name).read_text(encoding='utf-8')
        for name in ['Leaflet-LICENSE', 'Lucide-LICENSE', 'Audiowide-OFL.txt']
    ).replace('--', '- -')
    vendor_notices = '\n'.join(line.rstrip() for line in vendor_notices.splitlines())

    html = f"""<!doctype html>
<!-- Embedded third-party license notices:
{vendor_notices}
-->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Venue Radar | Scientific Conference Calendar</title>
  <meta name="description" content="Scientific conference deadlines and locations for machine learning, data science, vision, multimedia, biometrics, signals, biomedical AI, dynamics, control and neuroscience.">
  <link rel="icon" href="{logo}">
  <style>
    :root {{
      color-scheme: light;
      --text: #18212f;
      --muted: #5f6c7b;
      --line: #d7dde6;
      --line-strong: #b8c2cf;
      --surface: #f7f9fc;
      --surface-strong: #edf3f8;
      --accent: #0b6b78;
      --accent-dark: #064e58;
      --tag: #e8f3ec;
      --tag-text: #1c5d3a;
      --warn: #7a4f00;
      --warn-bg: #fff5d6;
    }}
    body {{
      margin: 0;
      color: var(--text);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
      background: #ffffff;
    }}
    main {{
      width: min(1320px, calc(100% - 28px));
      margin: 0 auto;
      padding: 34px 0 50px;
    }}
    header {{
      border-bottom: 1px solid var(--line);
      margin-bottom: 24px;
      padding-bottom: 22px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(2rem, 3vw, 2.85rem);
      line-height: 1.08;
    }}
    h2 {{
      margin: 34px 0 12px;
      font-size: 1.25rem;
      line-height: 1.2;
    }}
    p {{
      max-width: 800px;
      color: var(--muted);
      margin: 0;
    }}
    a {{
      color: var(--accent);
    }}
    .eyebrow {{
      margin: 0 0 8px;
      color: var(--accent-dark);
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    .subhead {{
      font-size: 1.02rem;
    }}
    .calendar-action {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      margin-top: 18px;
    }}
    .calendar-button {{
      display: inline-block;
      border: 1px solid var(--accent);
      border-radius: 6px;
      background: var(--accent);
      color: #ffffff;
      padding: 6px 10px;
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 650;
      line-height: 1.2;
    }}
    .calendar-note {{
      color: var(--muted);
      font-size: 0.9rem;
    }}
    .controls {{
      display: grid;
      grid-template-columns: minmax(230px, 2fr) minmax(0, 4fr);
      gap: 14px;
      margin: 22px 0 8px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--surface);
    }}
    .filter-details {{ min-width: 0; }}
    .filter-details summary {{ display: none; }}
    .filter-grid {{
      display: grid;
      grid-template-columns: minmax(190px, 1.35fr) minmax(90px, 0.55fr) minmax(125px, 0.8fr) minmax(155px, 1fr);
      gap: 14px;
    }}
    label {{
      display: grid;
      gap: 5px;
      color: var(--muted);
      font-size: 0.9rem;
      line-height: 1.25;
    }}
    .search-control {{
      display: block;
    }}
    .control-label {{
      display: block;
      margin: 0 0 5px;
      color: var(--muted);
      font-size: 0.9rem;
      line-height: 1.25;
    }}
    input,
    select {{
      width: 100%;
      box-sizing: border-box;
      border: 1px solid var(--line-strong);
      border-radius: 6px;
      color: var(--text);
      background: #ffffff;
      padding: 9px 10px;
      font: inherit;
    }}
    input:focus,
    select:focus {{
      outline: 2px solid rgba(11, 107, 120, 0.18);
      border-color: var(--accent);
    }}
    fieldset {{
      min-width: 0;
      margin: 0;
      padding: 0;
      border: 0;
    }}
    legend {{
      margin: 0 0 5px;
      color: var(--muted);
      font-size: 0.9rem;
      line-height: 1.25;
    }}
    .check-list {{
      max-height: 13rem;
      overflow: auto;
      display: grid;
      gap: 4px;
      padding: 8px;
      border: 1px solid var(--line-strong);
      border-radius: 6px;
      background: #ffffff;
    }}
    .check-option {{
      display: flex;
      grid-template-columns: none;
      align-items: flex-start;
      gap: 7px;
      color: var(--text);
      font-size: 0.86rem;
      line-height: 1.25;
    }}
    .check-option input {{
      width: auto;
      margin: 2px 0 0;
      padding: 0;
      flex: 0 0 auto;
      accent-color: var(--accent);
    }}
    .tab-shell {{
      margin-top: 30px;
    }}
    .tab-toolbar {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 8px;
    }}
    .table-tabs {{
      display: inline-flex;
      flex-wrap: wrap;
      gap: 4px;
      margin: 0;
      border: 1px solid var(--line);
      border-bottom: 0;
      border-radius: 8px 8px 0 0;
      background: var(--surface);
      padding: 4px;
    }}
    .tab-button {{
      border: 0;
      border-radius: 6px;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      font: inherit;
      font-size: 0.94rem;
      font-weight: 650;
      line-height: 1.2;
      padding: 8px 12px;
    }}
    .tab-button[aria-selected="true"] {{
      background: #ffffff;
      color: var(--accent-dark);
      box-shadow: 0 0 0 1px var(--line);
    }}
    .tab-button:focus {{
      outline: 2px solid rgba(11, 107, 120, 0.22);
      outline-offset: 2px;
    }}
    .tab-panel[hidden] {{
      display: none;
    }}
    .open-toggle {{
      display: flex;
      align-items: center;
      gap: 7px;
      padding-bottom: 7px;
      color: var(--text);
      font-weight: 600;
    }}
    .toolbar-actions {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    #result-count {{
      color: var(--muted);
      font-size: 0.85rem;
      white-space: nowrap;
    }}
    .open-toggle input {{
      width: auto;
      margin: 0;
      accent-color: var(--accent);
    }}
    .results-line {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin: 3px 0 10px;
      color: var(--muted);
      font-size: 0.85rem;
    }}
    .clear-filters {{
      border: 0;
      background: none;
      color: var(--accent-dark);
      font: inherit;
      font-weight: 650;
      cursor: pointer;
      padding: 3px 0;
    }}
    .table-wrap {{
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: visible;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 0;
      table-layout: fixed;
    }}
    th,
    td {{
      border-bottom: 1px solid var(--line);
      padding: 8px 9px;
      text-align: left;
      vertical-align: middle;
      font-size: 0.9rem;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }}
    th {{
      background: var(--surface-strong);
      color: #394657;
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0;
      white-space: nowrap;
    }}
    tr:last-child td {{
      border-bottom: 0;
    }}
    tr[hidden] {{
      display: none;
    }}
    .deadline-group-row {{
      background: #ffffff;
    }}
    .deadline-group-row.is-expanded td {{
      border-bottom-color: var(--line-strong);
    }}
    .deadline-toggle {{
      width: 1.35rem;
      height: 1.35rem;
      margin: 0;
      border: 1px solid var(--line-strong);
      border-radius: 4px;
      background: #ffffff;
      color: var(--accent-dark);
      cursor: pointer;
      line-height: 1;
      vertical-align: middle;
      flex: 0 0 auto;
    }}
    .deadline-toggle[hidden] {{
      display: none;
    }}
    .deadline-toggle:focus {{
      outline: 2px solid rgba(11, 107, 120, 0.22);
      outline-offset: 2px;
    }}
    .expand-icon {{
      display: inline-block;
      transform-origin: center;
      transition: transform 140ms ease;
    }}
    .deadline-toggle[aria-expanded="true"] .expand-icon {{
      transform: rotate(90deg);
    }}
    time {{
      font-weight: 650;
      color: #1e2a38;
      white-space: nowrap;
    }}
    .deadline-combined-cell {{
      min-width: 0;
    }}
    .deadline-cell-content {{
      display: flex;
      align-items: flex-start;
      gap: 6px;
      min-width: 0;
    }}
    .deadline-grid {{
      display: grid;
      row-gap: 5px;
      min-width: 0;
      width: 100%;
    }}
    .deadline-grid-row {{
      display: flex;
      align-items: baseline;
      gap: 5px;
      min-width: 0;
      overflow: hidden;
    }}
    .deadline-grid-row[hidden] {{
      display: none;
    }}
    .deadline-grid-row time {{
      font-size: 0.78rem;
      flex: 0 0 auto;
    }}
    .deadline-milestone {{
      min-width: 0;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }}
    .deadline-passed {{
      color: #9c5d60;
      font-size: 0.76rem;
      font-weight: 700;
      flex: 0 0 auto;
    }}
    .deadline-grid-row.is-past time,
    .deadline-grid-row.is-past .deadline-milestone {{
      color: #8e6668;
    }}
    .milestone-estimate {{
      color: var(--warn);
      font-size: 0.72rem;
      flex: 0 0 auto;
    }}
    .deadline-unknown {{
      color: var(--muted);
    }}
    .time-left {{
      font-weight: 700;
      white-space: nowrap;
    }}
    .submission-status {{
      display: inline-block;
      border-radius: 4px;
      padding: 3px 5px;
      font-size: 0.79rem;
      font-weight: 700;
      line-height: 1.3;
    }}
    .status-open {{ background: #d8efdd; color: #155b2d; }}
    .status-scheduled, .status-opportunity {{ background: #eaf5e8; color: #3d7044; }}
    .status-estimated {{ background: #fff3d7; color: #765321; }}
    .status-closed, .status-ongoing {{ background: #f4e9e9; color: #8a3e42; }}
    .status-past {{ background: #eef1f4; color: #52606f; }}
    .status-unknown {{ background: #eef1f4; color: #52606f; }}
    .acceptance-cell strong {{
      display: block;
      font-size: 0.82rem;
    }}
    .acceptance-cell a,
    .rate-unknown {{
      font-size: 0.77rem;
      white-space: nowrap;
    }}
    .rate-unknown {{
      color: var(--muted);
    }}
    .tag,
    .meta-pill {{
      display: inline-block;
      margin: 0 3px 4px 0;
      padding: 2px 6px;
      border-radius: 999px;
      font-size: 0.75rem;
      line-height: 1.25;
      overflow-wrap: normal;
    }}
    .tag {{
      background: var(--tag);
      color: var(--tag-text);
    }}
    .meta-pill {{
      background: #eef2f6;
      color: #344255;
    }}
    .rank-link,
    .rank-empty {{
      display: inline-block;
      min-width: 1.5rem;
      padding: 2px 4px;
      text-align: center;
      font-size: 0.82rem;
      font-weight: 700;
      white-space: nowrap;
    }}
    .rank-link {{
      border-radius: 4px;
      background: #e8f3ec;
      color: #1c5d3a;
      text-decoration: none;
    }}
    .rank-link:hover,
    .rank-link:focus {{
      text-decoration: underline;
    }}
    .rank-empty {{
      color: var(--muted);
      font-weight: 500;
    }}
    .rank-pair {{
      display: inline-flex;
      align-items: center;
      gap: 2px;
      white-space: nowrap;
    }}
    .rank-separator {{ color: var(--muted); }}
    .rank-link-ccf {{
      background: #e8eef4;
      color: #284d6d;
    }}
    .row-calendar-button {{
      display: inline-block;
      border: 1px solid var(--line-strong);
      border-radius: 6px;
      background: #ffffff;
      color: var(--accent-dark);
      padding: 4px 7px;
      text-decoration: none;
      font-size: 0.76rem;
      font-weight: 700;
      line-height: 1.2;
    }}
    .row-calendar-button:hover,
    .row-calendar-button:focus {{
      border-color: var(--accent);
      outline: 0;
    }}
    footer {{
      margin-top: 34px;
      color: var(--muted);
      font-size: 0.92rem;
    }}
    @media (max-width: 1100px) and (min-width: 761px) {{
      .controls {{
        grid-template-columns: 1fr;
      }}
    }}
    @media (max-width: 760px) {{
      main {{
        width: min(100% - 24px, 1320px);
      }}
      .controls {{
        grid-template-columns: 1fr;
      }}
      .filter-details summary {{
        display: list-item;
        color: var(--accent-dark);
        cursor: pointer;
        font-weight: 650;
      }}
      .filter-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
        margin-top: 12px;
      }}
      .filter-grid fieldset:first-child,
      .filter-grid fieldset:last-child {{
        grid-column: 1 / -1;
      }}
      .filter-grid fieldset:first-child .check-list {{
        max-height: 8rem;
      }}
      .filter-grid fieldset:last-child .check-list {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}
      .calendar-action {{
        align-items: flex-start;
        flex-direction: column;
      }}
      .tab-shell {{
        margin-top: 24px;
      }}
      .table-tabs {{
        display: grid;
        grid-template-columns: 1fr;
        width: 100%;
        box-sizing: border-box;
        border-bottom: 1px solid var(--line);
        border-radius: 8px;
        margin-bottom: 10px;
      }}
      .tab-toolbar {{ align-items: stretch; }}
      .open-toggle {{ padding: 0 2px 4px; }}
      .tab-button {{
        width: 100%;
        text-align: left;
      }}
      .table-wrap {{
        border: 0;
      }}
      table,
      colgroup,
      thead,
      tbody,
      tr,
      th,
      td {{
        display: block;
        width: 100%;
      }}
      thead {{
        position: absolute;
        width: 1px;
        height: 1px;
        overflow: hidden;
        clip: rect(0 0 0 0);
      }}
      tr {{
        box-sizing: border-box;
        margin-bottom: 10px;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: #ffffff;
      }}
      td {{
        box-sizing: border-box;
        display: grid;
        grid-template-columns: minmax(7rem, 34%) 1fr;
        gap: 10px;
        border-bottom: 1px solid var(--line);
        padding: 8px 10px;
      }}
      td::before {{
        content: attr(data-label);
        color: var(--muted);
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
      }}
      .deadline-grid-row {{
        flex-wrap: wrap;
      }}
      .deadline-milestone {{
        white-space: normal;
      }}
      tr:last-child td,
      td:last-child {{
        border-bottom: 0;
      }}
    }}
    {leaflet_css}
    @font-face {{
      font-family: Audiowide;
      font-style: normal;
      font-weight: 400;
      font-display: swap;
      src: url(data:font/woff2;base64,{title_font}) format('woff2');
    }}
    {custom_css}
  </style>
</head>
<body>
  <main>
    <header>
      <div class="brand-copy">
        <div class="brand-line"><img class="brand-mark" src="{logo}" alt="" width="82" height="82"><h1>Venue Radar</h1></div>
        <p class="subhead">Scientific conferences in ML &amp; data science, NLP, agents &amp; retrieval, complex systems, time series &amp; signals, vision &amp; multimedia, healthcare &amp; biometrics, neuroscience, robotics &amp; control, and responsible AI.</p>
      </div>
      <div class="calendar-action">
        <span class="calendar-caption">Download calendar</span>
        <a class="calendar-button" href="calendar-all.ics" download>{download_icon}All events (.ics)</a>
      </div>
    </header>

    <details class="controls filter-details" id="filter-details">
      <summary><span class="filter-disclosure-icon" aria-hidden="true">&#9654;</span><span>Filters &amp; search</span></summary>
      <div class="filter-content">
        <div class="filter-grid">
          {_topic_filter()}
          {_checkbox_group("Size", "size", ["S", "M", "L", "XL", "XXL"])}
          {_checkbox_group("ICORE Rank", "icore", ["A*", "A", "B", "C", "Unranked"], slug_values=False, link_href="https://portal.core.edu.au/conf-ranks/")}
          {_checkbox_group("CCF Rank", "ccf", ["A", "B", "C", "Unranked"], slug_values=False, link_href=ccf_page)}
          {_checkbox_group("Acceptance rate", "acceptance", ["Very low", "Low", "Moderate", "High", "Very high", "Unknown"])}
          <label class="search-control">
            <span class="control-label">Search</span>
            <input id="search" type="search" autocomplete="off" placeholder="Conference, topic, location, milestone">
          </label>
        </div>
        <div class="filter-actions">
          <label class="topic-mode"><span>Match</span><select id="topic-match" aria-label="Topic family matching"><option value="any">Any selected family</option><option value="all">All selected families</option></select></label>
          <button class="clear-filters" id="clear-filters" type="button">Clear filters</button>
        </div>
      </div>
    </details>

    <section class="tab-shell" aria-label="Conference calendar tables">
      <div class="tab-toolbar">
        <div class="table-tabs" role="tablist" aria-label="Table view">
          <button class="tab-button" id="tab-deadlines" type="button" role="tab" aria-selected="true" aria-controls="panel-deadlines" data-tab-target="deadlines">Upcoming Deadlines</button>
          <button class="tab-button" id="tab-conferences" type="button" role="tab" aria-selected="false" aria-controls="panel-conferences" data-tab-target="conferences" tabindex="-1">Conferences</button>
        </div>
        <label class="open-toggle"><input id="open-only" type="checkbox">Show only submission opportunities</label>
        <div class="toolbar-actions">
          <span id="result-count" aria-live="polite"></span>
        </div>
      </div>

      <div class="tab-panel" id="panel-deadlines" role="tabpanel" aria-labelledby="tab-deadlines" data-tab-panel="deadlines">
        <div class="table-wrap">
          <table>
            {_colgroup(["12%", "14%", "7%", "30%", "15%", "9%", "9%", "4%"])}
            <thead>
              <tr>
                <th>Conference</th>
                <th>Submission status</th>
                <th>Time left</th>
                <th>Next milestone</th>
                <th>Topics</th>
                <th>Accept. rate</th>
                <th>ICORE / CCF</th>
                <th>Size</th>
              </tr>
            </thead>
            <tbody id="deadlines-body">
              {_deadline_group_rows(conferences, icore, ccf, ccf_page, rates)}
            </tbody>
          </table>
        </div>
      </div>

      <div class="tab-panel" id="panel-conferences" role="tabpanel" aria-labelledby="tab-conferences" data-tab-panel="conferences" hidden>
        <section class="map-section" aria-label="Confirmed upcoming conference locations">
          <div class="map-heading"><h2>On the map</h2><span id="map-count" aria-live="polite"></span></div>
          <div id="conference-map" aria-label="World map of confirmed upcoming conferences"></div>
          <p id="map-empty" class="map-empty" hidden>No confirmed upcoming locations match these filters.</p>
          <div id="map-cities" class="map-cities" aria-label="Conference cities"></div>
        </section>
        <div class="table-wrap">
          <table>
            {_colgroup(["15%", "15%", "16%", "22%", "10%", "10%", "5%", "7%"])}
            <thead>
              <tr>
                <th>Conference</th>
                <th>Dates</th>
                <th>Location</th>
                <th>Topics</th>
                <th>Accept. rate</th>
                <th>ICORE / CCF</th>
                <th>Size</th>
                <th>Calendar</th>
              </tr>
            </thead>
            <tbody id="upcoming-conferences-body">
              {_conference_rows(conferences, icore, ccf, ccf_page, rates)}
            </tbody>
          </table>
        </div>
        <details id="past-conferences-section" hidden>
          <summary>Ongoing and past conferences</summary>
          <div class="table-wrap">
            <table>
              {_colgroup(["15%", "15%", "16%", "22%", "10%", "10%", "5%", "7%"])}
              <thead><tr><th>Conference</th><th>Dates</th><th>Location</th><th>Topics</th><th>Accept. rate</th><th>ICORE / CCF</th><th>Size</th><th>Calendar</th></tr></thead>
              <tbody id="past-conferences-body"></tbody>
            </table>
          </div>
        </details>
      </div>
    </section>

    <section class="community" id="community" aria-labelledby="community-title">
      <h2 id="community-title">Community</h2>
      <p>Missing a conference, or spotted a correction? Leave a comment or send a conference request.</p>
      <div class="community-links">
        <a href="https://github.com/gon-uri/venue-radar/issues/new?template=conference-request.yml">Request a conference</a>
        <a href="https://github.com/gon-uri/venue-radar/discussions">GitHub discussions</a>
        <a href="https://github.com/gon-uri/venue-radar">Find Venue Radar useful? Star the repository</a>
        <a href="https://x.com/gonzauri">Follow @gonzauri on X</a>
      </div>
      <div class="giscus"></div>
      <noscript><a href="https://github.com/gon-uri/venue-radar/discussions">Join the discussion on GitHub</a></noscript>
    </section>
    <footer>
      <strong>Database last updated {escape(last_updated)}.</strong>
      The calendar is reviewed regularly as organizers publish new schedules. An estimated submission status or date means the information is uncertain. Some estimated dates use prior-edition timing as a proxy until organizers publish the next schedule.
      <div>ICORE 2026 and CCF 2026 ranks are separate assessments of main-track full papers; a dash means no direct rank is shown. Historical acceptance rates refer to the linked year and track, not the next edition's expected outcome. Unknown means no defensible rate is available.</div>
      <div>Size is a qualitative scale, not a verified attendance count. A time-estimated milestone has a published day but no confirmed cutoff hour. Always check the organizer's call before submitting.</div>
      <div class="author">Created and maintained by <strong>Gonzalo Uribarri</strong>, Assistant Professor at the <a href="https://www.su.se/english/divisions/department-of-computer-and-systems-sciences">Department of Computer and Systems Sciences</a>, Stockholm University.</div>
      <div class="author-links"><a href="https://www.su.se/profiles/g/gour8957">University profile</a><a href="https://scholar.google.com/citations?user=q5sweuIAAAAJ&amp;hl=en">Google Scholar</a><a href="https://github.com/gon-uri">GitHub</a><a href="https://github.com/gon-uri/venue-radar/blob/main/LICENSE">Code: MIT</a><a href="https://github.com/gon-uri/venue-radar/blob/main/CONTENT-LICENSE.md">Original content: CC BY 4.0</a></div>
    </footer>
  </main>
  <script>{leaflet_js}</script>
  <script>const venueMapData = {map_data};
  {custom_js}</script>
  <script>
    const search = document.querySelector("#search");
    const filters = [...document.querySelectorAll("[data-filter-group]")];
    const rows = [...document.querySelectorAll("[data-filter-row]")];
    const openOnly = document.querySelector("#open-only");
    const resultCount = document.querySelector("#result-count");
    const clearFilters = document.querySelector("#clear-filters");
    const tabButtons = [...document.querySelectorAll("[data-tab-target]")];
    const tabPanels = [...document.querySelectorAll("[data-tab-panel]")];
    const deadlinesBody = document.querySelector("#deadlines-body");
    const deadlineGroups = [...document.querySelectorAll("[data-deadline-group]")];
    const conferenceRows = [...document.querySelectorAll("[data-conference-row]")];
    const upcomingConferenceBody = document.querySelector("#upcoming-conferences-body");
    const pastConferenceBody = document.querySelector("#past-conferences-body");
    const pastSection = document.querySelector("#past-conferences-section");
    const submissionTypes = new Set({json.dumps(sorted(SUBMISSION_TYPES))});
    const deadlineData = new Map(rows.map((row) => [
      row,
      JSON.parse(row.dataset.deadlines).map((deadline) => ({{
        ...deadline,
        time: Date.parse(deadline.at),
      }})),
    ]));
    const stateByRow = new Map();

    function selectedValues(group) {{
      return filters
        .filter((input) => input.dataset.filterGroup === group && input.checked)
        .map((input) => input.value);
    }}

    function matchesGroup(row, group, selected) {{
      if (!selected.length) {{
        return true;
      }}
      const values = (row.dataset[group] || "").split(" ").filter(Boolean);
      return selected.some((value) => values.includes(value));
    }}

    function rowMatchesFilters(row) {{
      const query = search.value.trim().toLowerCase();
      const selectedSizes = selectedValues("size");
      const selectedIcore = selectedValues("icore");
      const selectedCcf = selectedValues("ccf");
      const selectedAcceptance = selectedValues("acceptance");

      const haystack = row.dataset.search.toLowerCase();
      const matchesSearch = !query || haystack.includes(query);
      const matchesTopic = venueTopicMatch(row);
      const matchesSize = matchesGroup(row, "size", selectedSizes);
      const matchesIcore = matchesGroup(row, "icore", selectedIcore);
      const matchesCcf = matchesGroup(row, "ccf", selectedCcf);
      const matchesAcceptance = matchesGroup(row, "acceptance", selectedAcceptance);
      const matchesOpen = !row.hasAttribute("data-deadline-group") || !openOnly.checked || ["open", "scheduled", "opportunity", "estimated"].includes(stateByRow.get(row)?.kind);
      return matchesSearch && matchesTopic && matchesSize && matchesIcore && matchesCcf && matchesAcceptance && matchesOpen;
    }}

    function formatRemaining(deadline, now) {{
      const diff = deadline - now;
      const hour = 60 * 60 * 1000;
      const day = 24 * hour;
      const days = Math.floor(diff / day);
      const hours = Math.floor((diff % day) / hour);

      if (days > 0) {{
        return `${{days}}d ${{hours}}h`;
      }}
      if (hours > 0) {{
        return `${{hours}}h`;
      }}
      return "<1h";
    }}

    function openLabel(type) {{
      if (["abstract", "late_abstract", "extended_abstract"].includes(type)) return "Open abstract submissions";
      if (type === "poster") return "Open poster submissions";
      if (type === "discussion_paper") return "Open discussion papers (non-archival)";
      if (type === "journal_paper") return "Open joint journal/paper submissions";
      return "Open paper submissions";
    }}

    function submissionState(row, now) {{
      const details = deadlineData.get(row) || [];
      const end = Date.parse(`${{row.dataset.conferenceEnd}}T23:59:59Z`);
      const start = Date.parse(`${{row.dataset.conferenceStart}}T00:00:00Z`);
      if (end < now) return {{ kind: "past", label: "Edition passed" }};
      if (start <= now) return {{ kind: "ongoing", label: "Closed to new submissions" }};
      const milestones = details.flatMap((item) => [
        item,
        ...(item.opens_at ? [{{
          type: `${{item.type}}_opens`,
          time: Date.parse(item.opens_at),
          estimated: item.estimated,
          approximate_time: item.approximate_time,
        }}] : []),
      ]);
      milestones.push({{
        type: "conference_start", time: start,
        estimated: ["estimated", "not_yet_announced", "stale"].includes(row.dataset.confidence),
      }});
      // Closed and unannounced routes retain a chronological schedule fallback.
      const scheduleMilestone = milestones.filter((item) => item.time > now)
        .sort((a, b) => a.time - b.time)[0] || null;
      const submissions = details.filter((deadline) =>
        submissionTypes.has(deadline.type) && !deadline.gate_for
      );
      const opportunities = submissions.flatMap((deadline) => {{
        if (deadline.time <= now) return [];
        const gates = details.filter((item) => item.gate_for === deadline.type);
        if (gates.some((gate) => gate.time <= now)) return [];
        const action = gates.sort((a, b) => a.time - b.time)[0] || deadline;
        return [{{
          action,
          estimated: deadline.estimated || gates.some((gate) => gate.estimated),
        }}];
      }}).sort((a, b) => a.action.time - b.action.time);
      const next = opportunities[0];
      if (next) {{
        const estimated = next.estimated;
        const opensAt = Date.parse(next.action.opens_at);
        const scheduled = opensAt > now;
        const open = !scheduled && (opensAt <= now ||
          (next.action.open_observed_on && Date.parse(`${{next.action.open_observed_on}}T00:00:00Z`) <= now));
        const action = {{ ...next.action, estimated }};
        return {{
          kind: estimated ? "estimated" : open ? "open" : scheduled ? "scheduled" : "opportunity",
          label: estimated ? "Submission opportunity (estimated)"
            : open ? openLabel(action.type) : scheduled ? "Scheduled submission" : "Submission opportunity",
          description: estimated ? "Submission timing or eligibility is estimated; check the organizer's call."
            : open ? "Opening evidence is recorded for this submission step."
            : scheduled ? `This submission step opens ${{new Date(opensAt).toISOString()}}; the countdown targets its deadline.`
            : "A submission deadline is confirmed, but opening information has not been verified.",
          action,
          milestone: action,
        }};
      }}
      if (submissions.length === 0) {{
        return {{ kind: "unknown", label: "Deadline unannounced", milestone: scheduleMilestone }};
      }}
      return {{
        kind: "closed",
        label: "Closed to new submissions",
        milestone: scheduleMilestone,
      }};
    }}

    function updateStatus(row, state) {{
      const label = row.querySelector("[data-submission-status]");
      if (!label) return;
      label.textContent = state.label;
      label.className = `submission-status status-${{state.kind}}`;
      label.title = state.description || "";
    }}

    function renderDeadlineGroups(now) {{
      const blocks = [];
      deadlineGroups.forEach((group) => {{
        const groupId = group.dataset.deadlineGroup;
        const state = stateByRow.get(group);
        const details = [...group.querySelectorAll("[data-deadline-row]")];
        const groupMatches = group.dataset.filterMatch === "true";
        const summaryDetail = details.find((detail) =>
          detail.dataset.deadlineType === state.milestone?.type &&
          Date.parse(detail.querySelector("time").dateTime) === state.milestone.time
        ) || details[0];
        const canExpand = details.length > 1;
        const button = group.querySelector(".deadline-toggle");
        const expanded = canExpand && group.dataset.expanded === "true";
        group.hidden = !groupMatches || !state.milestone || state.kind === "past";
        group.classList.toggle("is-expanded", expanded);
        const timeLeft = group.querySelector("[data-time-left]");
        timeLeft.textContent = state.kind === "closed" ? "Closed" : state.action
          ? `${{state.action.estimated || state.action.approximate_time ? "~" : ""}}${{formatRemaining(state.action.time, now)}}`
          : "\u2014";
        group.querySelector("[data-time-estimate]").hidden =
          !(state.action?.approximate_time && !state.action.estimated);
        details.forEach((detail) => {{
          detail.hidden = !(expanded || detail === summaryDetail);
          const passed = Date.parse(detail.querySelector("time").dateTime) <= now;
          detail.classList.toggle("is-past", passed);
          detail.querySelector("[data-deadline-passed]").textContent = passed ? "Passed" : "";
        }});
        if (!group.hidden) {{
          blocks.push({{
            sortTime: state.milestone?.time ?? Infinity,
            id: groupId,
            row: group,
          }});
        }}
      }});

      blocks
        .sort((left, right) => {{
          const timeSort = left.sortTime - right.sortTime;
          return timeSort || left.id.localeCompare(right.id);
        }})
        .forEach((block) => {{
          deadlinesBody.appendChild(block.row);
        }});
    }}

    function updateResultCount() {{
      const active = document.querySelector('[role="tab"][aria-selected="true"]').dataset.tabTarget;
      const visible = (active === "deadlines" ? deadlineGroups : conferenceRows)
        .filter((row) => !row.hidden).length;
      const total = active === "deadlines"
        ? deadlineGroups.filter((row) => stateByRow.get(row)?.milestone).length
        : conferenceRows.length;
      resultCount.textContent = `${{visible}} of ${{total}} conferences`;
    }}

    function applyFilters() {{
      syncTopicParents();
      const now = Date.now();
      rows.forEach((row) => {{
        const state = submissionState(row, now);
        stateByRow.set(row, state);
        updateStatus(row, state);
        row.dataset.filterMatch = String(rowMatchesFilters(row));
      }});
      renderDeadlineGroups(now);
      conferenceRows.forEach((row) => {{
        const past = ["past", "ongoing"].includes(stateByRow.get(row).kind);
        const target = past ? pastConferenceBody : upcomingConferenceBody;
        if (row.parentElement !== target) target.appendChild(row);
        row.hidden = row.dataset.filterMatch !== "true";
      }});
      [...pastConferenceBody.children]
        .sort((a, b) => b.dataset.conferenceStart.localeCompare(a.dataset.conferenceStart))
        .forEach((row) => pastConferenceBody.appendChild(row));
      pastSection.hidden = ![...pastConferenceBody.children].some((row) => !row.hidden);
      updateResultCount();
      updateConferenceMap();
    }}

    function activateTab(tabId) {{
      tabButtons.forEach((button) => {{
        const selected = button.dataset.tabTarget === tabId;
        button.setAttribute("aria-selected", String(selected));
        button.tabIndex = selected ? 0 : -1;
      }});
      tabPanels.forEach((panel) => {{
        panel.hidden = panel.dataset.tabPanel !== tabId;
      }});
      updateResultCount();
      openOnly.closest("label").hidden = tabId !== "deadlines";
      updateConferenceMap();
    }}

    tabButtons.forEach((button, index) => {{
      button.addEventListener("click", () => activateTab(button.dataset.tabTarget));
      button.addEventListener("keydown", (event) => {{
        if (!["ArrowLeft", "ArrowRight"].includes(event.key)) {{
          return;
        }}
        event.preventDefault();
        const direction = event.key === "ArrowRight" ? 1 : -1;
        const nextIndex = (index + direction + tabButtons.length) % tabButtons.length;
        tabButtons[nextIndex].focus();
        activateTab(tabButtons[nextIndex].dataset.tabTarget);
      }});
    }});

    deadlineGroups.forEach((group) => {{
      const button = group.querySelector(".deadline-toggle");
      if (!button) {{
        return;
      }}
      button.addEventListener("click", () => {{
        if (button.disabled || button.hidden) {{
          return;
        }}
        const expanded = group.dataset.expanded === "true";
        group.dataset.expanded = String(!expanded);
        button.setAttribute("aria-expanded", String(!expanded));
        button.setAttribute(
          "aria-label",
          `${{!expanded ? "Hide" : "Show"}} milestones for ${{group.querySelector("a").textContent.trim()}}`,
        );
        renderDeadlineGroups(Date.now());
      }});
    }});

    search.addEventListener("input", applyFilters);
    filters.forEach((input) => input.addEventListener("change", applyFilters));
    document.querySelectorAll("[data-family-toggle]").forEach((input) => input.addEventListener("change", () => {{
      document.querySelectorAll(`[data-topic-family="${{input.dataset.familyToggle}}"]`).forEach((child) => {{ child.checked = input.checked; }});
      applyFilters();
    }}));
    document.querySelector("#topic-match").addEventListener("change", applyFilters);
    document.querySelector("#time-series-shortcut").addEventListener("change", applyFilters);
    openOnly.addEventListener("change", applyFilters);
    clearFilters.addEventListener("click", () => {{
      search.value = "";
      filters.forEach((input) => {{ input.checked = false; }});
      openOnly.checked = false;
      document.querySelector("#time-series-shortcut").checked = false;
      document.querySelector("#topic-match").value = "any";
      applyFilters();
      search.focus();
    }});
    applyFilters();
    setInterval(applyFilters, 60 * 1000);
    const commentObserver = new IntersectionObserver((entries) => {{
      if (entries.some((entry) => entry.isIntersecting)) {{ loadCommunityComments(); commentObserver.disconnect(); }}
    }}, {{rootMargin: "150px"}});
    commentObserver.observe(document.querySelector("#community"));
  </script>
</body>
</html>
"""
    output.write_text(html, encoding="utf-8")
    return output


def main() -> int:
    output = build_site()
    print(output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
