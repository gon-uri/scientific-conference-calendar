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


def _source_link(url: str) -> str:
    return f'<a class="source-link" href="{_attr(url)}">Source</a>'


def _format_date(value: datetime) -> str:
    return f"{MONTHS[value.month - 1]} {value.day}, {value.year}"


def _format_time(value: datetime) -> str:
    hour = value.hour % 12 or 12
    suffix = "AM" if value.hour < 12 else "PM"
    return f"{hour}:{value.minute:02d} {suffix}"


def _format_offset(value: datetime) -> str:
    offset = value.utcoffset()
    if offset is None:
        return "UTC"
    total_minutes = int(offset.total_seconds() // 60)
    if total_minutes == 0:
        return "UTC"
    sign = "+" if total_minutes > 0 else "-"
    total_minutes = abs(total_minutes)
    hours, minutes = divmod(total_minutes, 60)
    if minutes:
        return f"UTC{sign}{hours:02d}:{minutes:02d}"
    return f"UTC{sign}{hours}"


def _deadline_iso_utc(value: Any) -> str:
    parsed = parse_datetime(value)
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _display_deadline_datetime(value: Any) -> str:
    parsed = parse_datetime(value)
    return f"{_format_date(parsed)}, {_format_time(parsed)} {_format_offset(parsed)}"


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
        " ".join(conference.get("topics", [])),
    ]
    if extra:
        parts.extend(extra)
    return " ".join(str(part) for part in parts if part)


def _topic_slugs(topics: list[str]) -> str:
    return " ".join(stable_slug(topic) for topic in topics)


def _deadline_rows(conferences: list[dict[str, Any]]) -> str:
    rows = []
    items = sorted(
        (
            (conference, deadline)
            for conference in conferences
            for deadline in conference.get("deadlines", [])
        ),
        key=_deadline_sort_key,
    )
    for conference, deadline in items:
        source_url = _deadline_source_url(conference, deadline)
        label = _display_deadline_label(deadline["label"])
        search_text = _search_text(
            conference, [label, deadline["type"], source_url]
        )
        deadline_utc = _deadline_iso_utc(deadline["datetime"])
        rows.append(
            f'<tr data-filter-row data-search="{_attr(search_text)}" '
            f'data-topics="{_attr(_topic_slugs(conference.get("topics", [])))}">'
            f"<td><time datetime=\"{_attr(deadline_utc)}\">"
            f"{escape(_display_deadline_datetime(deadline['datetime']))}</time></td>"
            f"<td><span class=\"remaining\" data-deadline=\"{_attr(deadline_utc)}\">Calculating...</span></td>"
            f"<td>{escape(label)}</td>"
            f"<td><a href=\"{_attr(conference['website'])}\">{escape(conference['short_title'])}</a></td>"
            f"<td>{_topic_labels(conference.get('topics', []))}</td>"
            f"<td>{_source_link(source_url)}</td>"
            f"<td>{_confidence_label(conference['confidence'])}</td>"
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
            f'<tr data-filter-row data-search="{_attr(search_text)}" '
            f'data-topics="{_attr(_topic_slugs(conference.get("topics", [])))}">'
            f"<td>{escape(_display_conference_dates(conference['conference_start'], conference['conference_end']))}</td>"
            f"<td><a href=\"{_attr(conference['website'])}\">{escape(conference['short_title'])}</a></td>"
            f"<td>{escape(conference.get('location', 'TBD'))}</td>"
            f"<td>{_topic_labels(conference.get('topics', []))}</td>"
            f"<td>{_source_link(source_url)}</td>"
            f"<td>{_confidence_label(conference['confidence'])}</td>"
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


def _topic_options(conferences: list[dict[str, Any]]) -> str:
    options = ['<option value="">All topics</option>']
    for topic in _topics(conferences):
        options.append(
            f'<option value="{_attr(stable_slug(topic))}">{escape(topic)}</option>'
        )
    return "\n".join(options)


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
      width: min(1180px, calc(100% - 32px));
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
      grid-template-columns: minmax(240px, 1fr) minmax(180px, 260px);
      gap: 12px;
      margin: 22px 0 8px;
      padding: 14px;
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
    .table-wrap {{
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 980px;
    }}
    th,
    td {{
      border-bottom: 1px solid var(--line);
      padding: 11px 12px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: var(--surface-strong);
      color: #394657;
      font-size: 0.78rem;
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
    time {{
      font-weight: 650;
      color: #1e2a38;
    }}
    .remaining {{
      display: inline-block;
      min-width: 5.5rem;
      color: #1e2a38;
      font-weight: 650;
      white-space: nowrap;
    }}
    .remaining-past {{
      color: var(--muted);
      font-weight: 500;
    }}
    .tag,
    .confidence {{
      display: inline-block;
      margin: 0 5px 5px 0;
      padding: 2px 7px;
      border-radius: 999px;
      font-size: 0.82rem;
      white-space: nowrap;
    }}
    .tag {{
      background: var(--tag);
      color: var(--tag-text);
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
    .source-link {{
      font-weight: 600;
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
    }}
    footer {{
      margin-top: 34px;
      color: var(--muted);
      font-size: 0.92rem;
    }}
    @media (max-width: 760px) {{
      main {{
        width: min(100% - 24px, 1180px);
      }}
      .controls {{
        grid-template-columns: 1fr;
      }}
      .calendar-action {{
        align-items: flex-start;
        flex-direction: column;
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
      <label>
        Topic
        <select id="topic-filter">
          {_topic_options(conferences)}
        </select>
      </label>
    </div>

    <section>
      <h2>Upcoming Deadlines</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Remaining</th>
              <th>Milestone</th>
              <th>Conference</th>
              <th>Topics</th>
              <th>Source</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {_deadline_rows(conferences)}
          </tbody>
        </table>
      </div>
    </section>

    <section>
      <h2>Upcoming Conferences</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Dates</th>
              <th>Conference</th>
              <th>Location</th>
              <th>Topics</th>
              <th>Source</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {_conference_rows(conferences)}
          </tbody>
        </table>
      </div>
    </section>

    <footer>
      Data last checked through {escape(last_checked)}. Edit data/conferences.yml and rebuild to update this static page and calendar feed.
    </footer>
  </main>
  <script>
    const search = document.querySelector("#search");
    const topicFilter = document.querySelector("#topic-filter");
    const rows = [...document.querySelectorAll("[data-filter-row]")];
    const remainingItems = [...document.querySelectorAll("[data-deadline]")];

    function applyFilters() {{
      const query = search.value.trim().toLowerCase();
      const topic = topicFilter.value;

      rows.forEach((row) => {{
        const haystack = row.dataset.search.toLowerCase();
        const topics = row.dataset.topics.split(" ");
        const matchesSearch = !query || haystack.includes(query);
        const matchesTopic = !topic || topics.includes(topic);
        row.hidden = !(matchesSearch && matchesTopic);
      }});
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

    search.addEventListener("input", applyFilters);
    topicFilter.addEventListener("change", applyFilters);
    updateRemaining();
    setInterval(updateRemaining, 60 * 1000);
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
