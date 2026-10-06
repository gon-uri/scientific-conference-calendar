"""Print a source-linked review queue for the static conference catalog."""

from __future__ import annotations

import argparse
from datetime import date

from validate import load_acceptance_rates, load_conferences, parse_date


def review_queue(
    conferences: list[dict], as_of: date, max_age_days: int,
) -> list[tuple[str, str, str, str]]:
    queue = []
    latest_by_series = {
        series: max(
            (item for item in conferences if item["series"] == series),
            key=lambda item: item["year"],
        )
        for series in {item["series"] for item in conferences}
    }
    for item in conferences:
        reasons = []
        checked = parse_date(item["last_checked"])
        age = (as_of - checked).days
        upcoming = parse_date(item["conference_end"]) >= as_of
        if upcoming:
            if item["confidence"] != "confirmed":
                reasons.append(item["confidence"].replace("_", " "))
            if any(
                deadline.get("confidence", item["confidence"]) != "confirmed"
                for deadline in item.get("deadlines", [])
            ):
                reasons.append("estimated deadline(s): compare with official CFP")
            if age > max_age_days:
                reasons.append(f"last checked {age} days ago")
            if not item.get("deadlines"):
                reasons.append("no submission deadline recorded")
        elif latest_by_series[item["series"]] is item and item["series"] != "IJCAI-ECAI":
            reasons.append("next edition not tracked")
        if reasons:
            source = (item.get("source_urls") or [item.get("cfp_url") or item["website"]])[0]
            queue.append((item["short_title"], item["id"], ", ".join(reasons), source))
    return sorted(queue, key=lambda row: ("next edition not tracked" in row[2], row[0].casefold()))


def acceptance_queue(conferences: list[dict], rates: dict, as_of: date) -> list[str]:
    names = sorted({item["series"] for item in conferences}, key=str.casefold)
    return [
        f"{name}: " + (
            "no sourced rate" if name not in rates
            else f"latest evidence is {rates[name]['year']}"
        )
        for name in names
        if name not in rates or as_of.year - rates[name]["year"] > 2
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    parser.add_argument("--max-age-days", type=int, default=30)
    args = parser.parse_args()
    if args.max_age_days < 0:
        parser.error("--max-age-days must be non-negative")
    conferences = load_conferences()
    rates = load_acceptance_rates()["rates"]
    rows = review_queue(conferences, args.as_of, args.max_age_days)
    print(f"Edition review as of {args.as_of}: {len(rows)} of {len(conferences)} editions")
    for title, identifier, reason, source in rows:
        print(f"- {title} ({identifier}): {reason}\n  {source}")
    rate_rows = acceptance_queue(conferences, rates, args.as_of)
    print(f"\nAcceptance evidence review: {len(rate_rows)} series")
    for row in rate_rows:
        print(f"- {row}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
