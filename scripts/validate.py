from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "conferences.yml"
TOPICS_PATH = ROOT / "data" / "topics.yml"
ICORE_PATH = ROOT / "data" / "icore_rankings.yml"

REQUIRED_FIELDS = {
    "id",
    "series",
    "year",
    "title",
    "short_title",
    "website",
    "conference_start",
    "conference_end",
    "topics",
    "size",
    "difficulty",
    "submission_type",
    "deadlines",
    "last_checked",
    "confidence",
}

VALID_CONFIDENCE = {
    "confirmed",
    "estimated",
    "announced_no_deadlines",
    "not_yet_announced",
    "stale",
}

VALID_RELEVANCE = {"high", "medium", "low", "watch"}
VALID_ICORE_RANKS = {"A*", "A", "B", "C"}

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def stable_slug(value: Any) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def parse_date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise TypeError(f"expected ISO date string, got {type(value).__name__}")


def parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise TypeError(f"expected ISO datetime string, got {type(value).__name__}")


def load_conferences(path: Path = DATA_PATH) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a YAML list of conferences")
    return data


def load_controlled_topics(path: Path = TOPICS_PATH) -> set[str] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, list) or not all(_non_empty_string(item) for item in data):
        raise ValueError(f"{path} must contain a YAML list of topic strings")
    return {str(item) for item in data}


def load_icore_rankings(path: Path = ICORE_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _non_empty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(
        _non_empty_string(item) for item in value
    )


def _has_source_urls(conference: dict[str, Any]) -> bool:
    return _non_empty_string_list(conference.get("source_urls"))


def validate_conferences(
    conferences: list[dict[str, Any]], controlled_topics: set[str] | None = None
) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()

    for index, conference in enumerate(conferences, start=1):
        label = f"entry #{index}"
        if not isinstance(conference, dict):
            errors.append(f"{label}: must be a mapping")
            continue

        conference_id = conference.get("id", f"<missing-{index}>")
        label = str(conference_id)

        missing = sorted(REQUIRED_FIELDS - set(conference))
        for field in missing:
            errors.append(f"{label}: missing required field '{field}'")

        if "id" in conference:
            if not _non_empty_string(conference["id"]):
                errors.append(f"{label}: id must be a non-empty string")
            elif not ID_RE.match(conference["id"]):
                errors.append(
                    f"{label}: id must use lowercase letters, numbers, and hyphens"
                )
            elif conference["id"] in seen_ids:
                errors.append(f"{label}: duplicate id")
            seen_ids.add(conference["id"])

        for field in (
            "series",
            "title",
            "short_title",
            "website",
            "size",
            "difficulty",
            "submission_type",
        ):
            if field in conference and not _non_empty_string(conference[field]):
                errors.append(f"{label}: {field} must be a non-empty string")

        if "year" in conference and not isinstance(conference["year"], int):
            errors.append(f"{label}: year must be an integer")

        start = None
        end = None
        if "conference_start" in conference:
            try:
                start = parse_date(conference["conference_start"])
            except (TypeError, ValueError) as exc:
                errors.append(f"{label}: conference_start is invalid: {exc}")
        if "conference_end" in conference:
            try:
                end = parse_date(conference["conference_end"])
            except (TypeError, ValueError) as exc:
                errors.append(f"{label}: conference_end is invalid: {exc}")
        if start and end and end < start:
            errors.append(f"{label}: conference_end is before conference_start")

        if "last_checked" in conference:
            try:
                parse_date(conference["last_checked"])
            except (TypeError, ValueError) as exc:
                errors.append(f"{label}: last_checked is invalid: {exc}")

        if "source_urls" in conference and not _non_empty_string_list(
            conference["source_urls"]
        ):
            errors.append(f"{label}: source_urls must be a non-empty list of strings")

        confidence = conference.get("confidence")
        if "confidence" in conference and confidence not in VALID_CONFIDENCE:
            errors.append(
                f"{label}: confidence must be one of {sorted(VALID_CONFIDENCE)}"
            )

        relevance = conference.get("relevance")
        if relevance is not None and relevance not in VALID_RELEVANCE:
            errors.append(f"{label}: relevance must be one of {sorted(VALID_RELEVANCE)}")

        topics = conference.get("topics")
        if "topics" in conference:
            if not isinstance(topics, list) or not topics:
                errors.append(f"{label}: topics must be a non-empty list")
            else:
                for topic in topics:
                    if not _non_empty_string(topic):
                        errors.append(f"{label}: topics must contain non-empty strings")
                    elif controlled_topics is not None and topic not in controlled_topics:
                        errors.append(
                            f"{label}: topic '{topic}' is not in data/topics.yml"
                        )

        if confidence == "confirmed" and not _has_source_urls(conference):
            errors.append(
                f"{label}: confirmed conference dates require at least one source_urls entry"
            )

        deadlines = conference.get("deadlines")
        if "deadlines" in conference:
            if not isinstance(deadlines, list):
                errors.append(f"{label}: deadlines must be a list")
            else:
                seen_deadline_keys: set[str] = set()
                for deadline_index, deadline in enumerate(deadlines, start=1):
                    deadline_label = f"{label}: deadline #{deadline_index}"
                    if not isinstance(deadline, dict):
                        errors.append(f"{deadline_label}: must be a mapping")
                        continue

                    for field in ("type", "label", "datetime"):
                        if field not in deadline:
                            errors.append(f"{deadline_label}: missing '{field}'")

                    deadline_type = deadline.get("type")
                    if "type" in deadline:
                        if not _non_empty_string(deadline_type):
                            errors.append(f"{deadline_label}: type must be non-empty")
                        else:
                            uid_key = stable_slug(deadline_type)
                            if not uid_key:
                                errors.append(
                                    f"{deadline_label}: type cannot form a stable UID"
                                )
                            elif uid_key in seen_deadline_keys:
                                errors.append(
                                    f"{deadline_label}: duplicate deadline type '{deadline_type}'"
                                )
                            seen_deadline_keys.add(uid_key)

                    if "label" in deadline and not _non_empty_string(
                        deadline["label"]
                    ):
                        errors.append(f"{deadline_label}: label must be non-empty")

                    if "datetime" in deadline:
                        try:
                            parse_datetime(deadline["datetime"])
                        except (TypeError, ValueError) as exc:
                            errors.append(f"{deadline_label}: datetime is invalid: {exc}")

                    if "source_url" in deadline and not _non_empty_string(
                        deadline["source_url"]
                    ):
                        errors.append(f"{deadline_label}: source_url must be non-empty")

                    if (
                        conference.get("confidence") == "confirmed"
                        and not _non_empty_string(deadline.get("source_url"))
                    ):
                        errors.append(
                            f"{deadline_label}: confirmed deadlines require source_url"
                        )

    return errors


def validate_icore_rankings(
    conferences: list[dict[str, Any]], data: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    if data.get("release") != "ICORE2026":
        errors.append("ICORE release must be ICORE2026")
    try:
        parse_date(data.get("checked_on"))
    except (TypeError, ValueError):
        errors.append("ICORE checked_on must be an ISO date")
    source_url = data.get("source_url")
    if not _non_empty_string(source_url) or not source_url.startswith(
        "https://portal.core.edu.au/conf-ranks/"
    ):
        errors.append("ICORE source_url must point to the official conference portal")

    rankings = data.get("rankings")
    if not isinstance(rankings, dict):
        return errors + ["ICORE rankings must be a mapping"]

    series_records: dict[str, list[dict[str, Any]]] = {}
    for conference in conferences:
        if isinstance(conference, dict) and _non_empty_string(conference.get("series")):
            series_records.setdefault(conference["series"], []).append(conference)

    seen_portal_ids: set[int] = set()
    for series, entry in rankings.items():
        if not _non_empty_string(series) or series not in series_records:
            errors.append(f"ICORE series '{series}' is not in conferences.yml")
            continue
        if not isinstance(entry, dict):
            errors.append(f"ICORE {series}: entry must be a mapping")
            continue
        rank = entry.get("rank")
        if not isinstance(rank, str) or rank not in VALID_ICORE_RANKS:
            errors.append(f"ICORE {series}: rank must be A*, A, B, or C")
        portal_id = entry.get("portal_id")
        if type(portal_id) is not int or portal_id <= 0:
            errors.append(f"ICORE {series}: portal_id must be a positive integer")
        elif portal_id in seen_portal_ids:
            errors.append(f"ICORE {series}: duplicate portal_id {portal_id}")
        else:
            seen_portal_ids.add(portal_id)
        if any(
            "workshop" in str(record.get("submission_type", "")).lower()
            for record in series_records[series]
        ):
            errors.append(f"ICORE {series}: workshops must not inherit main-track ranks")
    return errors


def main() -> int:
    try:
        conferences = load_conferences()
        controlled_topics = load_controlled_topics()
        icore_rankings = load_icore_rankings()
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_conferences(conferences, controlled_topics)
    errors.extend(validate_icore_rankings(conferences, icore_rankings))
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(conferences)} conferences.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
