from __future__ import annotations

import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

import yaml

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
    return " ".join(f'<span class="tag">{escape(topic)}</span>' for topic in topics)


CONFIDENCE_HELP = {
    "confirmed": "Confirmed dates come from an official conference source.",
    "estimated": (
        "Estimated entries include at least one date we have not fully confirmed; "
        "some use prior-edition timing because organizers have not yet disclosed "
        "the next official schedule."
    ),
    "announced_no_deadlines": (
        "The conference has been announced, but deadline details are not yet available."
    ),
    "not_yet_announced": "The next edition has not yet been officially announced.",
    "stale": "This entry needs review because the source information may be outdated.",
}


def _confidence_label(confidence: str) -> str:
    class_name = f"confidence confidence-{stable_slug(confidence)}"
    title = CONFIDENCE_HELP.get(confidence, f"Confidence: {confidence}")
    return (
        f'<span class="{_attr(class_name)}" title="{_attr(title)}">'
        f"{escape(confidence)}</span>"
    )


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


def _deadline_sort_key(item: tuple[dict[str, Any], dict[str, Any]]):
    parsed = parse_datetime(item[1]["datetime"])
    if parsed.tzinfo is not None and parsed.utcoffset() is not None:
        parsed = parsed.astimezone(timezone.utc)
    return (parsed, item[0]["id"], stable_slug(item[1]["type"]))


def _search_text(conference: dict[str, Any], extra: list[str] | None = None) -> str:
    parts = [
        conference["series"],
        conference["title"],
        conference["short_title"],
        conference.get("location", ""),
        conference.get("confidence", ""),
        conference.get("size", ""),
        conference.get("submission_type", ""),
        " ".join(conference.get("topics", [])),
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
    ccf_source: str,
) -> str:
    ccf_entry = ccf.get(conference["series"])
    if ccf_entry:
        rank = ccf_entry["rank"]
        source = f'{ccf_source}#page={ccf_entry["page"]}'
        ccf_html = (
            f'<a class="rank-link rank-link-ccf" href="{_attr(source)}" '
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
        else f'Estimated ({entry["year"]})'
    )
    return (
        '<span class="acceptance-cell">'
        f'<strong>{escape(band)}</strong> '
        f'<a href="{_attr(entry["source_url"])}" '
        f'title="{_attr(entry["track"])}; historical edition {entry["year"]}">'
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
        f'aria-label="Download calendar for {_attr(conference["short_title"])}">'
        "ICS <span aria-hidden=\"true\">&#8595;</span>"
        "</a>"
    )


def _colgroup(widths: list[str]) -> str:
    columns = "".join(f'<col style="width: {width}">' for width in widths)
    return f"<colgroup>{columns}</colgroup>"


def _filter_attributes(
    conference: dict[str, Any],
    search_text: str,
    icore: dict[str, Any],
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
        }
        for deadline in conference.get("deadlines", [])
    ]
    return (
        f'data-filter-row data-search="{_attr(search_text)}" '
        f'data-topics="{_attr(_topic_slugs(conference.get("topics", [])))}" '
        f'data-size="{_attr(_value_slug(conference.get("size", "")))}" '
        f'data-icore="{_attr(icore.get(conference["series"], {}).get("rank", "Unranked"))}" '
        f'data-acceptance="{_attr(_value_slug(band))}" '
        f'data-confidence="{_attr(conference["confidence"])}" '
        f'data-conference-end="{_attr(conference["conference_end"])}" '
        f'data-deadlines="{_attr(json.dumps(deadlines, separators=(",", ":")))}"'
    )


def _deadline_grid_rows(deadlines: list[dict[str, Any]]) -> str:
    if not deadlines:
        return '<span class="deadline-unknown">No deadline announced</span>'
    rows = []
    for index, deadline in enumerate(deadlines):
        deadline_utc = _deadline_iso_utc(deadline["datetime"])
        row_hidden = "" if index == 0 else " hidden"
        rows.append(
            f'<div class="deadline-grid-row" data-deadline-row data-entry-index="{index}" '
            f'data-deadline-type="{_attr(deadline["type"])}"{row_hidden}>'
            f'<time datetime="{_attr(deadline_utc)}">'
            f"{escape(_display_deadline_datetime(deadline['datetime']))}</time>"
            f'<span class="deadline-milestone">'
            f"{escape(_display_deadline_label(deadline['label']))}</span>"
            f'<span class="deadline-passed" data-deadline-passed="{_attr(deadline_utc)}"></span>'
            "</div>"
        )
    return f'<div class="deadline-grid" data-deadline-grid>{"".join(rows)}</div>'


def _deadline_group_rows(
    conferences: list[dict[str, Any]],
    icore: dict[str, Any],
    ccf: dict[str, Any],
    ccf_source: str,
    rates: dict[str, Any],
) -> str:
    rows = []
    for conference in conferences:
        deadlines = sorted(
            conference.get("deadlines", []),
            key=lambda deadline: _deadline_sort_key((conference, deadline)),
        )
        search_extras = []
        for deadline in deadlines:
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
        if len(deadlines) > 1:
            toggle_html = (
                f"<button class=\"deadline-toggle\" type=\"button\" aria-expanded=\"false\" "
                f"aria-label=\"Show deadlines for {_attr(conference['short_title'])}\">"
                "<span class=\"expand-icon\" aria-hidden=\"true\">&#9656;</span>"
                "</button>"
            )
        rows.append(
            f'<tr class="deadline-group-row" {_filter_attributes(conference, search_text, icore, rates)} '
            f'data-deadline-group="{_attr(group_id)}" data-expanded="false">'
            f"<td data-label=\"Conference\"><a href=\"{_attr(conference['website'])}\">{escape(conference['short_title'])}</a></td>"
            '<td data-label="Submission status"><span class="submission-status" data-submission-status>Checking...</span></td>'
            '<td data-label="Time left"><span class="time-left" data-time-left>&mdash;</span></td>'
            f'<td class="deadline-combined-cell" data-label="Submission deadline"><div class="deadline-cell-content">{toggle_html}{_deadline_grid_rows(deadlines)}</div></td>'
            f"<td data-label=\"Topics\">{_topic_labels(conference.get('topics', []))}</td>"
            f'<td data-label="Acceptance rate">{_acceptance_cell(conference, rates)}</td>'
            f'<td data-label="ICORE / CCF">{_ranking_cell(conference, icore, ccf, ccf_source)}</td>'
            f"<td data-label=\"Size\">{_metadata_label(conference.get('size', ''))}</td>"
            f"<td data-label=\"Confidence\">{_confidence_label(conference['confidence'])}</td>"
            f"<td data-label=\"Calendar\">{_conference_calendar_link(conference)}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _conference_rows(
    conferences: list[dict[str, Any]],
    icore: dict[str, Any],
    ccf: dict[str, Any],
    ccf_source: str,
    rates: dict[str, Any],
) -> str:
    rows = []
    for conference in sorted(
        conferences,
        key=lambda item: (parse_date(item["conference_start"]), item["id"]),
    ):
        source_url = _conference_source_url(conference)
        search_text = _search_text(conference, [source_url])
        rows.append(
            f'<tr {_filter_attributes(conference, search_text, icore, rates)} data-conference-row>'
            f"<td data-label=\"Conference\"><a href=\"{_attr(conference['website'])}\">{escape(conference['short_title'])}</a></td>"
            '<td data-label="Submission status"><span class="submission-status" data-submission-status>Checking...</span></td>'
            f"<td data-label=\"Dates\">{escape(_display_conference_dates(conference['conference_start'], conference['conference_end']))}</td>"
            f"<td data-label=\"Location\">{escape(conference.get('location', 'TBD'))}</td>"
            f"<td data-label=\"Topics\">{_topic_labels(conference.get('topics', []))}</td>"
            f'<td data-label="Acceptance rate">{_acceptance_cell(conference, rates)}</td>'
            f'<td data-label="ICORE / CCF">{_ranking_cell(conference, icore, ccf, ccf_source)}</td>'
            f"<td data-label=\"Size\">{_metadata_label(conference.get('size', ''))}</td>"
            f"<td data-label=\"Confidence\">{_confidence_label(conference['confidence'])}</td>"
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
        {topic for conference in conferences for topic in conference.get("topics", [])},
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


def _checkbox_group(label: str, group: str, values: list[str], slug_values: bool = True) -> str:
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
    return (
        "<fieldset class=\"filter-group\">"
        f"<legend>{escape(label)}</legend>"
        f"<div class=\"check-list\">{''.join(boxes)}</div>"
        "</fieldset>"
    )


def build_site(
    data_path: Path = DATA_PATH,
    docs_dir: Path = DOCS_DIR,
    rankings_path: Path = ICORE_PATH,
    ccf_path: Path = CCF_PATH,
    acceptance_path: Path = ACCEPTANCE_PATH,
) -> Path:
    conferences = load_conferences(data_path)
    icore_data = load_icore_rankings(rankings_path)
    ccf_data = load_ccf_rankings(ccf_path)
    acceptance_data = load_acceptance_rates(acceptance_path)
    errors = validate_conferences(conferences, load_controlled_topics())
    errors.extend(validate_icore_rankings(conferences, icore_data))
    errors.extend(validate_ccf_rankings(conferences, ccf_data))
    errors.extend(validate_acceptance_rates(conferences, acceptance_data))
    if errors:
        raise ValueError("conference data is invalid; run scripts/validate.py")

    docs_dir.mkdir(parents=True, exist_ok=True)
    output = docs_dir / "index.html"
    last_updated = _dataset_last_updated(conferences)
    icore = icore_data["rankings"]
    ccf = ccf_data["rankings"]
    rates = acceptance_data["rates"]

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Scientific Conference Calendar</title>
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
      grid-template-columns: minmax(230px, 2fr) minmax(200px, 1.35fr) minmax(82px, 0.55fr) minmax(125px, 0.8fr) minmax(155px, 1fr);
      gap: 14px;
      margin: 22px 0 8px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--surface);
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
    .status-open {{ background: #e7f2e9; color: #205d38; }}
    .status-estimated {{ background: #fff3d7; color: #765321; }}
    .status-closed {{ background: #f5ecec; color: #865456; }}
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
    .meta-pill,
    .confidence {{
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
    .confidence {{
      background: #ffffff;
      color: var(--muted);
      border: 1px solid var(--line);
    }}
    .confidence-estimated,
    .confidence-stale,
    .confidence-not-yet-announced {{
      background: var(--warn-bg);
      border-color: #ead388;
      color: var(--warn);
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
        grid-template-columns: minmax(220px, 2fr) minmax(180px, 1.5fr) minmax(90px, 0.7fr);
      }}
    }}
    @media (max-width: 760px) {{
      main {{
        width: min(100% - 24px, 1320px);
      }}
      .controls {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}
      .search-control,
      .controls fieldset:first-of-type,
      .controls fieldset:last-of-type {{
        grid-column: 1 / -1;
      }}
      .controls fieldset:first-of-type .check-list {{
        max-height: 8rem;
      }}
      .controls fieldset:last-of-type .check-list {{
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
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Scientific Conference Calendar</h1>
      <p class="subhead">Conference deadlines and dates for ML, AI, neuroscience, medical AI, vision, LLMs, time-series analysis, and biomedical signal processing.</p>
      <div class="calendar-action">
        <a class="calendar-button" href="calendar-all.ics" download>Download all events (.ics)</a>
        <span class="calendar-note">Static calendar file with every deadline and conference date.</span>
      </div>
    </header>

    <div class="controls">
      <label class="search-control">
        <span class="control-label">Search</span>
        <input id="search" type="search" autocomplete="off" placeholder="Conference, topic, location, milestone">
      </label>
      {_checkbox_group("Topics", "topics", _topics(conferences))}
      {_checkbox_group("Size", "size", _unique_values(conferences, "size"))}
      {_checkbox_group("ICORE", "icore", ["A*", "A", "B", "C", "Unranked"], slug_values=False)}
      {_checkbox_group("Acceptance rate", "acceptance", ["Very low", "Low", "Moderate", "High", "Very high", "Unknown"])}
    </div>

    <section class="tab-shell" aria-label="Conference calendar tables">
      <div class="tab-toolbar">
        <div class="table-tabs" role="tablist" aria-label="Table view">
          <button class="tab-button" id="tab-deadlines" type="button" role="tab" aria-selected="true" aria-controls="panel-deadlines" data-tab-target="deadlines">Upcoming Deadlines</button>
          <button class="tab-button" id="tab-conferences" type="button" role="tab" aria-selected="false" aria-controls="panel-conferences" data-tab-target="conferences" tabindex="-1">Upcoming Conferences</button>
        </div>
        <label class="open-toggle"><input id="open-only" type="checkbox">Show only open conferences</label>
      </div>
      <div class="results-line"><span id="result-count" aria-live="polite"></span><button class="clear-filters" id="clear-filters" type="button">Clear filters</button></div>

      <div class="tab-panel" id="panel-deadlines" role="tabpanel" aria-labelledby="tab-deadlines" data-tab-panel="deadlines">
        <div class="table-wrap">
          <table>
            {_colgroup(["13%", "13%", "7%", "15%", "15%", "9%", "9%", "4%", "9%", "6%"])}
            <thead>
              <tr>
                <th>Conference</th>
                <th>Submission status</th>
                <th>Time left</th>
                <th>Submission deadline</th>
                <th>Topics</th>
                <th>Acceptance rate</th>
                <th>ICORE / CCF</th>
                <th>Size</th>
                <th>Confidence</th>
                <th>Calendar</th>
              </tr>
            </thead>
            <tbody id="deadlines-body">
              {_deadline_group_rows(conferences, icore, ccf, ccf_data["source_url"], rates)}
            </tbody>
          </table>
        </div>
      </div>

      <div class="tab-panel" id="panel-conferences" role="tabpanel" aria-labelledby="tab-conferences" data-tab-panel="conferences" hidden>
        <div class="table-wrap">
          <table>
            {_colgroup(["12%", "12%", "11%", "9%", "15%", "10%", "10%", "5%", "9%", "7%"])}
            <thead>
              <tr>
                <th>Conference</th>
                <th>Submission status</th>
                <th>Dates</th>
                <th>Location</th>
                <th>Topics</th>
                <th>Acceptance rate</th>
                <th>ICORE / CCF</th>
                <th>Size</th>
                <th>Confidence</th>
                <th>Calendar</th>
              </tr>
            </thead>
            <tbody>
              {_conference_rows(conferences, icore, ccf, ccf_data["source_url"], rates)}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <footer>
      <strong>Database last updated {escape(last_updated)}.</strong>
      The calendar is reviewed regularly as organizers publish new schedules. Entries are marked {_confidence_label("estimated")} when we are not fully certain about a particular scraped or researched date. In some cases, prior-edition timing is used as a proxy because the next official dates or deadlines have not yet been disclosed.
      <div>ICORE 2026 and CCF 2026 ranks are separate assessments of main-track full papers; a dash means no direct rank is shown. Historical acceptance rates refer to the linked year and track, not the next edition's expected outcome. Unknown means no defensible rate is available.</div>
    </footer>
  </main>
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
      const selectedTopics = selectedValues("topics");
      const selectedSizes = selectedValues("size");
      const selectedIcore = selectedValues("icore");
      const selectedAcceptance = selectedValues("acceptance");

      const haystack = row.dataset.search.toLowerCase();
      const matchesSearch = !query || haystack.includes(query);
      const matchesTopic = matchesGroup(row, "topics", selectedTopics);
      const matchesSize = matchesGroup(row, "size", selectedSizes);
      const matchesIcore = matchesGroup(row, "icore", selectedIcore);
      const matchesAcceptance = matchesGroup(row, "acceptance", selectedAcceptance);
      const matchesOpen = !openOnly.checked || stateByRow.get(row)?.kind === "open";
      return matchesSearch && matchesTopic && matchesSize && matchesIcore && matchesAcceptance && matchesOpen;
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

    function routeLabel(type) {{
      if (type === "workshop_paper") return "Workshop papers open";
      if (type === "short_paper") return "Short papers open";
      if (type === "special_session_paper") return "Special-session papers open";
      if (type === "poster") return "Poster submissions open";
      if (["abstract", "late_abstract", "extended_abstract"].includes(type)) return "Abstract submissions open";
      return "Paper submissions open";
    }}

    function submissionState(row, now) {{
      const details = deadlineData.get(row) || [];
      const submissions = details.filter((deadline) =>
        submissionTypes.has(deadline.type) && !deadline.gate_for
      );
      const opportunities = submissions.flatMap((deadline) => {{
        if (deadline.time <= now) return [];
        const gates = details.filter((item) => item.gate_for === deadline.type);
        if (gates.some((gate) => gate.time <= now)) return [];
        const action = gates.sort((a, b) => a.time - b.time)[0] || deadline;
        return [{{ action, route: deadline.type }}];
      }}).sort((a, b) => a.action.time - b.action.time);
      const next = opportunities[0];
      if (next) {{
        const confirmed = row.dataset.confidence === "confirmed";
        return {{
          kind: confirmed ? "open" : "estimated",
          label: confirmed ? routeLabel(next.route) : "Deadline estimated",
          action: next.action,
          summary: next.action,
          sortTime: next.action.time,
        }};
      }}
      if (details.length === 0 && Date.parse(`${{row.dataset.conferenceEnd}}T23:59:59Z`) > now) {{
        return {{ kind: "unknown", label: "Deadline unannounced", summary: null, sortTime: Date.parse(row.dataset.conferenceEnd) }};
      }}
      const pastSubmission = submissions.sort((a, b) => b.time - a.time)[0];
      const summary = pastSubmission || details.sort((a, b) => b.time - a.time)[0] || null;
      return {{
        kind: "closed",
        label: Date.parse(`${{row.dataset.conferenceEnd}}T23:59:59Z`) <= now
          ? "Edition passed" : "Closed to new submissions",
        summary,
        sortTime: summary?.time || 0,
      }};
    }}

    function updateStatus(row, state) {{
      const label = row.querySelector("[data-submission-status]");
      label.textContent = state.label;
      label.className = `submission-status status-${{state.kind}}`;
    }}

    function renderDeadlineGroups(now) {{
      const blocks = [];
      deadlineGroups.forEach((group) => {{
        const groupId = group.dataset.deadlineGroup;
        const state = stateByRow.get(group);
        const details = [...group.querySelectorAll("[data-deadline-row]")];
        const groupMatches = group.dataset.filterMatch === "true";
        const summaryDetail = details.find((detail) => detail.dataset.deadlineType === state.summary?.type) || details[0];
        const canExpand = details.length > 1;
        const button = group.querySelector(".deadline-toggle");
        const expanded = canExpand && group.dataset.expanded === "true";
        group.hidden = !groupMatches;
        group.classList.toggle("is-expanded", expanded);
        const timeLeft = group.querySelector("[data-time-left]");
        timeLeft.textContent = state.action
          ? `${{state.kind === "estimated" ? "~" : ""}}${{formatRemaining(state.action.time, now)}}`
          : "\u2014";
        details.forEach((detail) => {{
          detail.hidden = !(expanded || detail === summaryDetail);
          const passed = Date.parse(detail.querySelector("time").dateTime) <= now;
          detail.classList.toggle("is-past", passed);
          detail.querySelector("[data-deadline-passed]").textContent = passed ? "Passed" : "";
        }});
        if (groupMatches) {{
          blocks.push({{
            sortBucket: {{ open: 0, estimated: 1, unknown: 2, closed: 3 }}[state.kind],
            sortTime: state.sortTime,
            id: groupId,
            row: group,
          }});
        }}
      }});

      blocks
        .sort((left, right) => {{
          if (left.sortBucket !== right.sortBucket) {{
            return left.sortBucket - right.sortBucket;
          }}
          const timeSort = left.sortBucket < 3
            ? left.sortTime - right.sortTime
            : right.sortTime - left.sortTime;
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
      resultCount.textContent = `${{visible}} of ${{conferenceRows.length}} conferences`;
    }}

    function applyFilters() {{
      const now = Date.now();
      rows.forEach((row) => {{
        const state = submissionState(row, now);
        stateByRow.set(row, state);
        updateStatus(row, state);
        row.dataset.filterMatch = String(rowMatchesFilters(row));
      }});
      renderDeadlineGroups(now);
      conferenceRows.forEach((row) => {{
        row.hidden = row.dataset.filterMatch !== "true";
      }});
      updateResultCount();
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
          `${{!expanded ? "Hide" : "Show"}} deadlines for ${{group.querySelector("a").textContent.trim()}}`,
        );
        renderDeadlineGroups(Date.now());
      }});
    }});

    search.addEventListener("input", applyFilters);
    filters.forEach((input) => input.addEventListener("change", applyFilters));
    openOnly.addEventListener("change", applyFilters);
    clearFilters.addEventListener("click", () => {{
      search.value = "";
      filters.forEach((input) => {{ input.checked = false; }});
      openOnly.checked = false;
      applyFilters();
      search.focus();
    }});
    applyFilters();
    setInterval(applyFilters, 60 * 1000);
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
