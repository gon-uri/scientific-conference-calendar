from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

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


def _confidence_label(confidence: str) -> str:
    class_name = f"confidence confidence-{stable_slug(confidence)}"
    return f'<span class="{_attr(class_name)}">{escape(confidence)}</span>'


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
    return (
        f'<a class="row-calendar-button" href="{_attr(_conference_calendar_href(conference))}" '
        f'download aria-label="Download calendar for {_attr(conference["short_title"])}">'
        "ICS"
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
        first_deadline = deadlines[0]
        first_label = _display_deadline_label(first_deadline["label"])
        first_deadline_utc = _deadline_iso_utc(first_deadline["datetime"])
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
        rows.append(
            f'<tr class="deadline-group-row" {_filter_attributes(conference, search_text)} '
            f'data-deadline-group="{_attr(group_id)}" data-expanded="false">'
            f"<td data-label=\"Date\">"
            f"<button class=\"deadline-toggle\" type=\"button\" aria-expanded=\"false\" "
            f"aria-controls=\"deadline-details-{_attr(group_id)}\" "
            f"aria-label=\"Show deadlines for {_attr(conference['short_title'])}\">"
            "<span class=\"expand-icon\" aria-hidden=\"true\">&#9656;</span>"
            "</button>"
            f"<time data-group-date-time datetime=\"{_attr(first_deadline_utc)}\">"
            f"{escape(_display_deadline_datetime(first_deadline['datetime']))}</time></td>"
            f"<td data-label=\"Remaining\"><span class=\"remaining\" data-group-remaining data-deadline=\"{_attr(first_deadline_utc)}\">Calculating...</span></td>"
            f"<td data-label=\"Milestone\" data-group-milestone>{escape(first_label)}</td>"
            f"<td data-label=\"Conference\"><a href=\"{_attr(conference['website'])}\">{escape(conference['short_title'])}</a></td>"
            f"<td data-label=\"Size\">{_metadata_label(conference.get('size', ''))}</td>"
            f"<td data-label=\"Difficulty\">{_metadata_label(conference.get('difficulty', ''))}</td>"
            f"<td data-label=\"Topics\">{_topic_labels(conference.get('topics', []))}</td>"
            f"<td data-label=\"Confidence\">{_confidence_label(conference['confidence'])}</td>"
            f"<td data-label=\"Calendar\">{_conference_calendar_link(conference)}</td>"
            "</tr>"
        )
        for index, deadline in enumerate(deadlines):
            detail_id = (
                f"deadline-details-{group_id}"
                if index == 0
                else f"deadline-details-{group_id}-{index + 1}"
            )
            source_url = _deadline_source_url(conference, deadline)
            label = _display_deadline_label(deadline["label"])
            search_text = _search_text(
                conference, [label, deadline["type"], source_url]
            )
            deadline_utc = _deadline_iso_utc(deadline["datetime"])
            detail_classes = "deadline-detail-row"
            if index == 0:
                detail_classes += " next-deadline-detail"
            rows.append(
                f'<tr class="{_attr(detail_classes)}" {_filter_attributes(conference, search_text)} '
                f'id="{_attr(detail_id)}" '
                f'data-deadline-detail data-detail-for="{_attr(group_id)}" '
                f'data-deadline-at="{_attr(deadline_utc)}" '
                f'data-date-display="{_attr(_display_deadline_datetime(deadline["datetime"]))}" '
                f'data-deadline-label="{_attr(label)}" hidden>'
                f"<td data-label=\"Date\"><span class=\"detail-indent\"></span>"
                f"<time datetime=\"{_attr(deadline_utc)}\">"
                f"{escape(_display_deadline_datetime(deadline['datetime']))}</time></td>"
                f"<td data-label=\"Remaining\"><span class=\"remaining\" data-deadline=\"{_attr(deadline_utc)}\">Calculating...</span></td>"
                f"<td data-label=\"Milestone\">{escape(label)}</td>"
                "<td class=\"detail-fill\" colspan=\"6\"></td>"
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
    last_checked = _max_last_checked(conferences)

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
      vertical-align: top;
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
    .deadline-group-row.is-expanded td {{
      border-bottom-color: var(--line-strong);
    }}
    .deadline-toggle {{
      width: 1.55rem;
      height: 1.55rem;
      margin: -2px 5px 0 0;
      border: 1px solid var(--line-strong);
      border-radius: 999px;
      background: #ffffff;
      color: var(--accent-dark);
      cursor: pointer;
      line-height: 1;
      vertical-align: middle;
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
    .deadline-detail-row td {{
      background: #fbfcfe;
      color: #344255;
    }}
    .deadline-detail-row.next-deadline-detail td {{
      background: #fff8dc;
    }}
    .detail-indent {{
      display: inline-block;
      width: 2rem;
    }}
    .detail-fill {{
      color: var(--muted);
    }}
    time {{
      font-weight: 650;
      color: #1e2a38;
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
      tr:last-child td,
      td:last-child {{
        border-bottom: 0;
      }}
      .detail-fill {{
        display: none;
      }}
      .detail-indent {{
        display: none;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">Static scientific calendar</p>
      <h1>Scientific Conference Calendar</h1>
      <p class="subhead">Conference deadlines and dates for ML, AI, neuroscience, medical AI, vision, LLMs, time-series analysis, and biomedical signal processing.</p>
      <div class="calendar-action">
        <a class="calendar-button" href="calendar-all.ics" download>Download all events (.ics)</a>
        <span class="calendar-note">Static calendar file with every deadline and conference date.</span>
      </div>
    </header>

    <div class="controls">
      <label>
        Search
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
            {_colgroup(["11%", "8%", "14%", "10%", "6%", "9%", "26%", "8%", "8%"])}
            <thead>
              <tr>
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
            {_colgroup(["12%", "10%", "12%", "6%", "9%", "16%", "24%", "7%", "4%"])}
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
      Data last checked through {escape(last_checked)}. Edit data/conferences.yml and rebuild to update this static page and calendar feed.
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
    const deadlineDetails = [...document.querySelectorAll("[data-deadline-detail]")];
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

    function detailsForGroup(groupId) {{
      return deadlineDetails
        .filter((row) => row.dataset.detailFor === groupId)
        .sort((left, right) => Date.parse(left.dataset.deadlineAt) - Date.parse(right.dataset.deadlineAt));
    }}

    function updateGroupSummary(group, nextDetail) {{
      const time = group.querySelector("[data-group-date-time]");
      const remaining = group.querySelector("[data-group-remaining]");
      const milestone = group.querySelector("[data-group-milestone]");
      time.dateTime = nextDetail.dataset.deadlineAt;
      time.textContent = nextDetail.dataset.dateDisplay;
      remaining.dataset.deadline = nextDetail.dataset.deadlineAt;
      milestone.textContent = nextDetail.dataset.deadlineLabel;
    }}

    function renderDeadlineGroups() {{
      const now = Date.now();
      const blocks = [];

      deadlineGroups.forEach((group) => {{
        const groupId = group.dataset.deadlineGroup;
        const details = detailsForGroup(groupId);
        const upcomingDetails = details.filter((row) => Date.parse(row.dataset.deadlineAt) > now);
        const matchingDetails = upcomingDetails.filter((row) => row.dataset.filterMatch === "true");
        const groupMatches = group.dataset.filterMatch === "true" || matchingDetails.length > 0;
        const nextDetail = upcomingDetails[0];
        const showGroup = Boolean(nextDetail) && groupMatches;
        const expanded = group.dataset.expanded === "true";

        group.hidden = !showGroup;
        group.classList.toggle("is-expanded", showGroup && expanded);

        if (nextDetail) {{
          updateGroupSummary(group, nextDetail);
        }}

        details.forEach((detail) => {{
          const isUpcoming = Date.parse(detail.dataset.deadlineAt) > now;
          detail.classList.toggle("next-deadline-detail", detail === nextDetail);
          detail.hidden = !(showGroup && expanded && isUpcoming);
        }});

        if (showGroup) {{
          blocks.push({{
            sortTime: Date.parse(nextDetail.dataset.deadlineAt),
            id: groupId,
            rows: [group, ...details],
          }});
        }}
      }});

      blocks
        .sort((left, right) => left.sortTime - right.sortTime || left.id.localeCompare(right.id))
        .forEach((block) => {{
          block.rows.forEach((row) => deadlinesBody.appendChild(row));
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
      button.addEventListener("click", () => {{
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
