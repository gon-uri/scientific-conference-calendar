from __future__ import annotations

from datetime import timezone
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
    return f'<a href="{_attr(url)}">Source</a>'


def _display_deadline_datetime(value: Any) -> str:
    if isinstance(value, str):
        return escape(value.replace("T", " "))
    parsed = parse_datetime(value)
    if parsed.tzinfo is not None and parsed.utcoffset() is not None:
        parsed = parsed.astimezone(timezone.utc)
        return parsed.strftime("%Y-%m-%d %H:%M UTC")
    return parsed.strftime("%Y-%m-%d %H:%M")


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
        search_text = _search_text(
            conference, [deadline["label"], deadline["type"], source_url]
        )
        rows.append(
            f'<tr data-filter-row data-search="{_attr(search_text)}" '
            f'data-topics="{_attr(_topic_slugs(conference.get("topics", [])))}">'
            f"<td>{_display_deadline_datetime(deadline['datetime'])}</td>"
            f"<td>{escape(deadline['label'])}</td>"
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
        start = parse_date(conference["conference_start"]).isoformat()
        end = parse_date(conference["conference_end"]).isoformat()
        source_url = _conference_source_url(conference)
        search_text = _search_text(conference, [source_url])
        rows.append(
            f'<tr data-filter-row data-search="{_attr(search_text)}" '
            f'data-topics="{_attr(_topic_slugs(conference.get("topics", [])))}">'
            f"<td>{escape(start)} to {escape(end)}</td>"
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
    return max(dates).isoformat() if dates else "unknown"


def _topics(conferences: list[dict[str, Any]]) -> list[str]:
    return sorted(
        {topic for conference in conferences for topic in conference.get("topics", [])},
        key=lambda value: value.casefold(),
    )


def _topic_options(conferences: list[dict[str, Any]]) -> str:
    options = ['<option value="">All topics</option>']
    for topic in _topics(conferences):
        options.append(f'<option value="{_attr(stable_slug(topic))}">{escape(topic)}</option>')
    return "\n".join(options)


def _topic_feed_links(conferences: list[dict[str, Any]]) -> str:
    links = []
    for topic in _topics(conferences):
        slug = stable_slug(topic)
        links.append(f'<li><a href="tags/{_attr(slug)}.ics">{escape(topic)}</a></li>')
    return "\n".join(links)


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
      --text: #17202a;
      --muted: #5d6975;
      --line: #d8dee6;
      --surface: #f6f8fb;
      --accent: #005f73;
      --tag: #e7f0ea;
      --tag-text: #1f5f3b;
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
      width: min(1160px, calc(100% - 32px));
      margin: 0 auto;
      padding: 32px 0 48px;
    }}
    header {{
      border-bottom: 1px solid var(--line);
      margin-bottom: 24px;
      padding-bottom: 18px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(2rem, 3vw, 3rem);
      line-height: 1.1;
    }}
    h2 {{
      margin-top: 34px;
      font-size: 1.35rem;
    }}
    p {{
      max-width: 760px;
      color: var(--muted);
    }}
    a {{
      color: var(--accent);
    }}
    .feeds {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 16px 0 0;
      padding: 0;
      list-style: none;
    }}
    .feeds a {{
      display: inline-block;
      border: 1px solid var(--line);
      padding: 7px 10px;
      text-decoration: none;
      background: var(--surface);
      border-radius: 6px;
    }}
    .controls {{
      display: grid;
      grid-template-columns: minmax(220px, 1fr) minmax(180px, 260px);
      gap: 12px;
      margin: 22px 0 8px;
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
      border: 1px solid var(--line);
      border-radius: 6px;
      color: var(--text);
      background: #ffffff;
      padding: 9px 10px;
      font: inherit;
    }}
    .table-wrap {{
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 900px;
    }}
    th,
    td {{
      border-bottom: 1px solid var(--line);
      padding: 10px 12px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: var(--surface);
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    tr:last-child td {{
      border-bottom: 0;
    }}
    tr[hidden] {{
      display: none;
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
      background: var(--surface);
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
    footer {{
      margin-top: 34px;
      color: var(--muted);
      font-size: 0.92rem;
    }}
    @media (max-width: 720px) {{
      .controls {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Scientific Conference Calendar</h1>
      <p>Static conference deadline and date feeds for ML, AI, neuroscience, medical AI, vision, LLMs, time-series analysis, and biomedical signal processing.</p>
      <ul class="feeds" aria-label="Calendar feeds">
        <li><a href="calendar-all.ics">All events</a></li>
        <li><a href="deadlines.ics">Deadlines</a></li>
        <li><a href="conferences.ics">Conference dates</a></li>
      </ul>
      <ul class="feeds" aria-label="Topic calendar feeds">
        {_topic_feed_links(conferences)}
      </ul>
    </header>

    <div class="controls">
      <label>
        Search
        <input id="search" type="search" autocomplete="off" placeholder="Conference, topic, location, deadline">
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
              <th>Date and time</th>
              <th>Deadline</th>
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
      Data last checked through {escape(last_checked)}. Subscribe to any .ics link from a calendar app that supports public feeds.
    </footer>
  </main>
  <script>
    const search = document.querySelector("#search");
    const topicFilter = document.querySelector("#topic-filter");
    const rows = [...document.querySelectorAll("[data-filter-row]")];

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

    search.addEventListener("input", applyFilters);
    topicFilter.addEventListener("change", applyFilters);
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
