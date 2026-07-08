from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

import yaml

from validate import (
    DATA_PATH,
    load_conferences,
    load_controlled_topics,
    parse_date,
    parse_datetime,
    stable_slug,
    validate_conferences,
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
        "Estimated dates use the previous edition as a proxy because organizers "
        "have not yet disclosed the next official dates."
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
        conference.get("difficulty", ""),
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


def _filter_attributes(conference: dict[str, Any], search_text: str) -> str:
    return (
        f'data-filter-row data-search="{_attr(search_text)}" '
        f'data-topics="{_attr(_topic_slugs(conference.get("topics", [])))}" '
        f'data-size="{_attr(_value_slug(conference.get("size", "")))}" '
        f'data-difficulty="{_attr(_value_slug(conference.get("difficulty", "")))}"'
    )


def _deadline_grid_rows(deadlines: list[dict[str, Any]]) -> str:
    rows = []
    for index, deadline in enumerate(deadlines):
        deadline_utc = _deadline_iso_utc(deadline["datetime"])
        row_hidden = "" if index == 0 else " hidden"
        date_classes = "deadline-cell-entry"
        remaining_classes = "deadline-cell-entry remaining"
        milestone_classes = "deadline-cell-entry"
        if index == 0:
            date_classes += " is-summary"
            remaining_classes += " is-summary"
            milestone_classes += " is-summary"
        common = f'data-deadline-entry data-entry-index="{index}" data-entry-at="{_attr(deadline_utc)}"'
        rows.append(
            f'<div class="deadline-grid-row" data-deadline-row data-entry-index="{index}"{row_hidden}>'
            f'<time class="{_attr(date_classes)}" {common} data-entry-role="date" '
            f'datetime="{_attr(deadline_utc)}">'
            f"{escape(_display_deadline_datetime(deadline['datetime']))}</time>"
            f'<span class="{_attr(remaining_classes)}" {common} data-entry-role="remaining" '
            f'data-deadline="{_attr(deadline_utc)}">Calculating...</span>'
            f'<span class="{_attr(milestone_classes)}" {common} data-entry-role="milestone">'
            f"{escape(_display_deadline_label(deadline['label']))}</span>"
            "</div>"
        )
    return f'<div class="deadline-grid" data-deadline-grid>{"".join(rows)}</div>'


def _deadline_group_rows(conferences: list[dict[str, Any]]) -> str:
    rows = []
    grouped = []
    for conference in conferences:
        deadlines = sorted(
            conference.get("deadlines", []),
            key=lambda deadline: _deadline_sort_key((conference, deadline)),
        )
        if not deadlines:
            continue
        grouped.append((conference, deadlines))

    for conference, deadlines in sorted(
        grouped,
        key=lambda item: (
            _deadline_sort_key((item[0], item[1][0])),
            item[0]["id"],
        ),
    ):
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
            f'<tr class="deadline-group-row" {_filter_attributes(conference, search_text)} '
            f'data-deadline-group="{_attr(group_id)}" data-expanded="false">'
            f"<td class=\"expand-cell\" data-label=\"\">{toggle_html}</td>"
            f"<td class=\"deadline-combined-cell\" data-label=\"Deadlines\" colspan=\"3\">{_deadline_grid_rows(deadlines)}</td>"
            f"<td data-label=\"Conference\"><a href=\"{_attr(conference['website'])}\">{escape(conference['short_title'])}</a></td>"
            f"<td data-label=\"Size\">{_metadata_label(conference.get('size', ''))}</td>"
            f"<td data-label=\"Difficulty\">{_metadata_label(conference.get('difficulty', ''))}</td>"
            f"<td data-label=\"Topics\">{_topic_labels(conference.get('topics', []))}</td>"
            f"<td data-label=\"Confidence\">{_confidence_label(conference['confidence'])}</td>"
            f"<td data-label=\"Calendar\">{_conference_calendar_link(conference)}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _conference_rows(conferences: list[dict[str, Any]]) -> str:
    rows = []
    for conference in sorted(
        conferences,
        key=lambda item: (parse_date(item["conference_start"]), item["id"]),
    ):
        source_url = _conference_source_url(conference)
        search_text = _search_text(conference, [source_url])
        rows.append(
            f'<tr {_filter_attributes(conference, search_text)} data-conference-row>'
            f"<td data-label=\"Dates\">{escape(_display_conference_dates(conference['conference_start'], conference['conference_end']))}</td>"
            f"<td data-label=\"Conference\"><a href=\"{_attr(conference['website'])}\">{escape(conference['short_title'])}</a></td>"
            f"<td data-label=\"Location\">{escape(conference.get('location', 'TBD'))}</td>"
            f"<td data-label=\"Size\">{_metadata_label(conference.get('size', ''))}</td>"
            f"<td data-label=\"Difficulty\">{_metadata_label(conference.get('difficulty', ''))}</td>"
            f"<td data-label=\"Submission Type\">{escape(conference.get('submission_type', ''))}</td>"
            f"<td data-label=\"Topics\">{_topic_labels(conference.get('topics', []))}</td>"
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


def build_site(data_path: Path = DATA_PATH, docs_dir: Path = DOCS_DIR) -> Path:
    conferences = load_conferences(data_path)
    errors = validate_conferences(conferences, load_controlled_topics())
    if errors:
        raise ValueError("conference data is invalid; run scripts/validate.py")

    docs_dir.mkdir(parents=True, exist_ok=True)
    output = docs_dir / "index.html"
    last_updated = _dataset_last_updated(conferences)

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
      grid-template-columns: minmax(240px, 1.2fr) repeat(3, minmax(180px, 1fr));
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
    .table-tabs {{
      display: inline-flex;
      flex-wrap: wrap;
      gap: 4px;
      margin: 0 0 -1px;
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
      white-space: normal;
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
    .expand-header,
    .expand-cell {{
      text-align: center;
      vertical-align: middle;
    }}
    .deadline-group-row.is-expanded td {{
      border-bottom-color: var(--line-strong);
    }}
    .deadline-toggle {{
      width: 1.55rem;
      height: 1.55rem;
      margin: 0;
      border: 1px solid var(--line-strong);
      border-radius: 999px;
      background: #ffffff;
      color: var(--accent-dark);
      cursor: pointer;
      line-height: 1;
      vertical-align: middle;
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
    .remaining {{
      display: inline-block;
      min-width: 0;
      color: #1e2a38;
      font-weight: 650;
    }}
    .remaining-past {{
      color: var(--muted);
      font-weight: 500;
    }}
    .deadline-combined-cell {{
      padding-top: 10px;
      padding-bottom: 10px;
    }}
    .deadline-grid {{
      display: grid;
      align-content: center;
      row-gap: 8px;
    }}
    .deadline-grid-row {{
      display: grid;
      grid-template-columns: minmax(8.8rem, 15fr) minmax(5.4rem, 8fr) minmax(11rem, 13fr);
      column-gap: 16px;
      align-items: start;
    }}
    .deadline-grid-row[hidden] {{
      display: none;
    }}
    .deadline-cell-entry {{
      display: block;
      min-width: 0;
      color: #344255;
      font-weight: 500;
      line-height: 1.35;
    }}
    .deadline-cell-entry.is-summary,
    .deadline-cell-entry.is-next {{
      color: #162235;
      font-weight: 750;
    }}
    .deadline-cell-entry.remaining-past:not(.is-summary):not(.is-next) {{
      color: var(--muted);
      font-weight: 500;
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
    @media (max-width: 760px) {{
      main {{
        width: min(100% - 24px, 1320px);
      }}
      .controls {{
        grid-template-columns: 1fr;
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
      .expand-cell::before {{
        content: "";
      }}
      .deadline-grid-row {{
        grid-template-columns: 1fr;
        row-gap: 3px;
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
      {_checkbox_group("Difficulty", "difficulty", _unique_values(conferences, "difficulty"))}
    </div>

    <section class="tab-shell" aria-label="Conference calendar tables">
      <div class="table-tabs" role="tablist" aria-label="Table view">
        <button class="tab-button" id="tab-deadlines" type="button" role="tab" aria-selected="true" aria-controls="panel-deadlines" data-tab-target="deadlines">Upcoming Deadlines</button>
        <button class="tab-button" id="tab-conferences" type="button" role="tab" aria-selected="false" aria-controls="panel-conferences" data-tab-target="conferences" tabindex="-1">Upcoming Conferences</button>
      </div>

      <div class="tab-panel" id="panel-deadlines" role="tabpanel" aria-labelledby="tab-deadlines" data-tab-panel="deadlines">
        <div class="table-wrap">
          <table>
            {_colgroup(["3%", "15%", "8%", "13%", "10%", "5%", "8%", "23%", "8%", "7%"])}
            <thead>
              <tr>
                <th class="expand-header" aria-label="Expand"></th>
                <th>Date</th>
                <th>Remaining</th>
                <th>Milestone</th>
                <th>Conference</th>
                <th>Size</th>
                <th>Difficulty</th>
                <th>Topics</th>
                <th>Confidence</th>
                <th>Calendar</th>
              </tr>
            </thead>
            <tbody id="deadlines-body">
              {_deadline_group_rows(conferences)}
            </tbody>
          </table>
        </div>
      </div>

      <div class="tab-panel" id="panel-conferences" role="tabpanel" aria-labelledby="tab-conferences" data-tab-panel="conferences" hidden>
        <div class="table-wrap">
          <table>
            {_colgroup(["14%", "10%", "12%", "5%", "8%", "15%", "22%", "7%", "7%"])}
            <thead>
              <tr>
                <th>Dates</th>
                <th>Conference</th>
                <th>Location</th>
                <th>Size</th>
                <th>Difficulty</th>
                <th>Submission Type</th>
                <th>Topics</th>
                <th>Confidence</th>
                <th>Calendar</th>
              </tr>
            </thead>
            <tbody>
              {_conference_rows(conferences)}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <footer>
      <strong>Database last updated {escape(last_updated)}.</strong>
      The calendar is reviewed regularly as organizers publish new schedules. Entries marked {_confidence_label("estimated")} use prior-edition timing as a proxy because the next official dates or deadlines have not been disclosed yet.
    </footer>
  </main>
  <script>
    const search = document.querySelector("#search");
    const filters = [...document.querySelectorAll("[data-filter-group]")];
    const rows = [...document.querySelectorAll("[data-filter-row]")];
    const remainingItems = [...document.querySelectorAll("[data-deadline]")];
    const tabButtons = [...document.querySelectorAll("[data-tab-target]")];
    const tabPanels = [...document.querySelectorAll("[data-tab-panel]")];
    const deadlinesBody = document.querySelector("#deadlines-body");
    const deadlineGroups = [...document.querySelectorAll("[data-deadline-group]")];
    const conferenceRows = [...document.querySelectorAll("[data-conference-row]")];

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
      const selectedDifficulties = selectedValues("difficulty");

      const haystack = row.dataset.search.toLowerCase();
      const matchesSearch = !query || haystack.includes(query);
      const matchesTopic = matchesGroup(row, "topics", selectedTopics);
      const matchesSize = matchesGroup(row, "size", selectedSizes);
      const matchesDifficulty = matchesGroup(row, "difficulty", selectedDifficulties);
      return matchesSearch && matchesTopic && matchesSize && matchesDifficulty;
    }}

    function formatRemaining(deadline) {{
      const diff = deadline - Date.now();
      if (diff <= 0) {{
        return "Passed";
      }}

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

    function updateRemaining() {{
      remainingItems.forEach((item) => {{
        const deadline = Date.parse(item.dataset.deadline);
        item.textContent = Number.isNaN(deadline) ? "Unknown" : formatRemaining(deadline);
        item.classList.toggle("remaining-past", item.textContent === "Passed");
      }});
    }}

    function detailsForGroup(group) {{
      const details = new Map();
      group.querySelectorAll("[data-deadline-entry]").forEach((entry) => {{
        const index = entry.dataset.entryIndex;
        if (!details.has(index)) {{
          details.set(index, {{
            at: entry.dataset.entryAt,
            elements: [],
            index,
            row: entry.closest("[data-deadline-row]"),
            time: Date.parse(entry.dataset.entryAt),
          }});
        }}
        const detail = details.get(index);
        detail[entry.dataset.entryRole] = entry;
        detail.elements.push(entry);
      }});

      return [...details.values()]
        .filter((detail) => !Number.isNaN(detail.time))
        .sort((left, right) => left.time - right.time || Number(left.index) - Number(right.index));
    }}

    function renderDeadlineGroups() {{
      const now = Date.now();
      const blocks = [];

      deadlineGroups.forEach((group) => {{
        const groupId = group.dataset.deadlineGroup;
        const details = detailsForGroup(group);
        const upcomingDetails = details.filter((detail) => detail.time > now);
        const groupMatches = group.dataset.filterMatch === "true";
        const nextDetail = upcomingDetails[0];
        const summaryDetail = nextDetail || details[details.length - 1];
        const showGroup = Boolean(summaryDetail) && groupMatches;
        const canExpand = details.length > 1;
        const button = group.querySelector(".deadline-toggle");

        if (button) {{
          button.hidden = !canExpand;
          button.disabled = !canExpand;
          if (!canExpand) {{
            button.setAttribute("aria-expanded", "false");
          }}
        }}
        if (!canExpand) {{
          group.dataset.expanded = "false";
        }}

        const expanded = canExpand && group.dataset.expanded === "true";

        group.hidden = !showGroup;
        group.classList.toggle("is-expanded", showGroup && expanded);

        details.forEach((detail) => {{
          const isSummary = !expanded && detail === summaryDetail;
          const isNext = expanded && detail === nextDetail;
          const isVisible = showGroup && (expanded || isSummary);
          if (detail.row) {{
            detail.row.hidden = !isVisible;
          }}
          detail.elements.forEach((entry) => {{
            entry.classList.toggle("is-summary", isSummary);
            entry.classList.toggle("is-next", isNext);
          }});
        }});

        if (showGroup) {{
          const hasUpcoming = Boolean(nextDetail);
          blocks.push({{
            sortBucket: hasUpcoming ? 0 : 1,
            sortTime: summaryDetail.time,
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
          const timeSort = left.sortBucket === 0
            ? left.sortTime - right.sortTime
            : right.sortTime - left.sortTime;
          return timeSort || left.id.localeCompare(right.id);
        }})
        .forEach((block) => {{
          deadlinesBody.appendChild(block.row);
        }});
    }}

    function applyFilters() {{
      rows.forEach((row) => {{
        row.dataset.filterMatch = String(rowMatchesFilters(row));
      }});
      renderDeadlineGroups();
      conferenceRows.forEach((row) => {{
        row.hidden = row.dataset.filterMatch !== "true";
      }});
      updateRemaining();
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
        renderDeadlineGroups();
        updateRemaining();
      }});
    }});

    search.addEventListener("input", applyFilters);
    filters.forEach((input) => input.addEventListener("change", applyFilters));
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
