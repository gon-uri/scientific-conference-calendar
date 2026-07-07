from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

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
TAGS_DIR = DOCS_DIR / "tags"
UID_DOMAIN = "scientific-conference-calendar"
DTSTAMP = "19700101T000000Z"


def _escape_text(value: Any) -> str:
    text = str(value)
    return (
        text.replace("\\", "\\\\")
        .replace("\n", "\\n")
        .replace(";", "\\;")
        .replace(",", "\\,")
    )


def _fold_line(line: str) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in line:
        candidate = current + char
        limit = 75 if not lines else 74
        if len(candidate.encode("utf-8")) > limit:
            lines.append(current)
            current = " " + char
        else:
            current = candidate
    lines.append(current)
    return lines


def _property(name: str, value: Any) -> list[str]:
    return _fold_line(f"{name}:{_escape_text(value)}")


def _format_datetime(value: datetime) -> str:
    if value.tzinfo is not None and value.utcoffset() is not None:
        value = value.astimezone(timezone.utc)
        return value.strftime("%Y%m%dT%H%M%SZ")
    return value.strftime("%Y%m%dT%H%M%S")


def _deadline_sort_datetime(deadline: dict[str, Any]) -> datetime:
    value = parse_datetime(deadline["datetime"])
    if value.tzinfo is not None and value.utcoffset() is not None:
        return value.astimezone(timezone.utc)
    return value.replace(tzinfo=timezone.utc)


def _conference_sort_datetime(conference: dict[str, Any]) -> datetime:
    return datetime.combine(
        parse_date(conference["conference_start"]), time.min, tzinfo=timezone.utc
    )


def _topic_prefix(conference: dict[str, Any]) -> str:
    topics = conference.get("topics", [])[:2]
    return "".join(f"[{topic}]" for topic in topics)


def _conference_source_url(conference: dict[str, Any]) -> str:
    source_urls = conference.get("source_urls") or []
    if source_urls:
        return source_urls[0]
    return conference.get("cfp_url") or conference["website"]


def _deadline_source_url(
    conference: dict[str, Any], deadline: dict[str, Any]
) -> str:
    return deadline.get("source_url") or _conference_source_url(conference)


def _description(conference: dict[str, Any], source_url: str) -> str:
    lines = [
        f"Conference title: {conference['title']}",
        f"Website: {conference['website']}",
        f"Source URL: {source_url}",
        f"Location: {conference.get('location', 'TBD')}",
        f"Topics: {', '.join(conference.get('topics', []))}",
        f"Confidence: {conference['confidence']}",
        f"Last checked date: {conference['last_checked']}",
        f"Notes: {conference.get('notes') or ''}",
    ]
    return "\n".join(lines)


def _deadline_event(conference: dict[str, Any], deadline: dict[str, Any]) -> list[str]:
    start = parse_datetime(deadline["datetime"])
    end = start + timedelta(hours=1)
    deadline_key = stable_slug(deadline["type"])
    summary = (
        f"{_topic_prefix(conference)} {conference['short_title']} - {deadline['label']}"
    )
    source_url = _deadline_source_url(conference, deadline)

    return [
        "BEGIN:VEVENT",
        *_property(
            "UID", f"{conference['id']}-deadline-{deadline_key}@{UID_DOMAIN}"
        ),
        f"DTSTAMP:{DTSTAMP}",
        f"DTSTART:{_format_datetime(start)}",
        f"DTEND:{_format_datetime(end)}",
        *_property("SUMMARY", summary),
        *_property("DESCRIPTION", _description(conference, source_url)),
        *_property("URL", source_url),
        "END:VEVENT",
    ]


def _conference_event(conference: dict[str, Any]) -> list[str]:
    start = parse_date(conference["conference_start"])
    end = parse_date(conference["conference_end"]) + timedelta(days=1)
    summary = f"{_topic_prefix(conference)} {conference['short_title']} - Conference"
    source_url = _conference_source_url(conference)

    lines = [
        "BEGIN:VEVENT",
        *_property("UID", f"{conference['id']}-conference@{UID_DOMAIN}"),
        f"DTSTAMP:{DTSTAMP}",
        f"DTSTART;VALUE=DATE:{start.strftime('%Y%m%d')}",
        f"DTEND;VALUE=DATE:{end.strftime('%Y%m%d')}",
        *_property("SUMMARY", summary),
        *_property("DESCRIPTION", _description(conference, source_url)),
        *_property("URL", source_url),
    ]
    if conference.get("location"):
        lines.extend(_property("LOCATION", conference["location"]))
    lines.append("END:VEVENT")
    return lines


def _calendar(name: str, events: Iterable[list[str]]) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Scientific Conference Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        *_property("X-WR-CALNAME", name),
    ]
    for event in events:
        lines.extend(event)
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def _deadline_items(
    conferences: list[dict[str, Any]]
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    return sorted(
        (
            (conference, deadline)
            for conference in conferences
            for deadline in conference.get("deadlines", [])
        ),
        key=lambda item: (
            _deadline_sort_datetime(item[1]),
            item[0]["id"],
            stable_slug(item[1]["type"]),
        ),
    )


def _conference_items(conferences: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        conferences,
        key=lambda conference: (_conference_sort_datetime(conference), conference["id"]),
    )


def _deadline_events(conferences: list[dict[str, Any]]) -> list[list[str]]:
    return [
        _deadline_event(conference, deadline)
        for conference, deadline in _deadline_items(conferences)
    ]


def _conference_events(conferences: list[dict[str, Any]]) -> list[list[str]]:
    return [_conference_event(conference) for conference in _conference_items(conferences)]


def _all_events(conferences: list[dict[str, Any]]) -> list[list[str]]:
    event_records: list[tuple[datetime, str, str, list[str]]] = []
    for conference, deadline in _deadline_items(conferences):
        event_records.append(
            (
                _deadline_sort_datetime(deadline),
                conference["id"],
                f"deadline-{stable_slug(deadline['type'])}",
                _deadline_event(conference, deadline),
            )
        )
    for conference in _conference_items(conferences):
        event_records.append(
            (
                _conference_sort_datetime(conference),
                conference["id"],
                "conference",
                _conference_event(conference),
            )
        )
    return [record[3] for record in sorted(event_records, key=lambda item: item[:3])]


def _topic_groups(conferences: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for conference in conferences:
        for topic in conference.get("topics", []):
            slug = stable_slug(topic)
            if not slug:
                continue
            group = groups.setdefault(slug, {"name": topic, "conferences": []})
            group["conferences"].append(conference)
    return groups


def _write_topic_feeds(conferences: list[dict[str, Any]], tags_dir: Path) -> list[Path]:
    tags_dir.mkdir(parents=True, exist_ok=True)
    for old_feed in sorted(tags_dir.glob("*.ics")):
        old_feed.unlink()

    outputs: list[Path] = []
    for slug, group in sorted(_topic_groups(conferences).items()):
        topic_conferences = sorted(
            group["conferences"],
            key=lambda conference: (_conference_sort_datetime(conference), conference["id"]),
        )
        path = tags_dir / f"{slug}.ics"
        path.write_text(
            _calendar(
                f"Scientific Conferences: {group['name']}",
                _all_events(topic_conferences),
            ),
            encoding="utf-8",
        )
        outputs.append(path)
    return outputs


def build_calendars(
    data_path: Path = DATA_PATH, docs_dir: Path = DOCS_DIR
) -> list[Path]:
    conferences = load_conferences(data_path)
    errors = validate_conferences(conferences, load_controlled_topics())
    if errors:
        raise ValueError("conference data is invalid; run scripts/validate.py")

    docs_dir.mkdir(parents=True, exist_ok=True)

    outputs = [
        (
            docs_dir / "calendar-all.ics",
            _calendar("Scientific Conferences", _all_events(conferences)),
        ),
        (
            docs_dir / "deadlines.ics",
            _calendar("Scientific Conference Deadlines", _deadline_events(conferences)),
        ),
        (
            docs_dir / "conferences.ics",
            _calendar("Scientific Conference Dates", _conference_events(conferences)),
        ),
    ]

    paths: list[Path] = []
    for path, content in outputs:
        path.write_text(content, encoding="utf-8")
        paths.append(path)

    paths.extend(_write_topic_feeds(conferences, docs_dir / "tags"))
    return paths


def main() -> int:
    outputs = build_calendars()
    for output in outputs:
        print(output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
