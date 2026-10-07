"""Draft the next edition of verified recurring series from prior-edition timing.

This is an editorial helper, not an automatic source of confirmed dates. Review
official pages and edit the appended records before publication.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path

import yaml

from validate import DATA_PATH, load_conferences, parse_date, stable_slug


# Only series with a documented recurring cadence belong here. Irregular
# workshops and the one-off joint IJCAI-ECAI edition are intentionally absent.
CADENCE_YEARS = {
    "ICML": 1, "UAI": 1, "ECML PKDD": 1, "KDD": 1, "MLHC": 1,
    "CHIL": 1, "MICCAI": 1, "MIDL": 1, "IEEE EMBC": 1,
    "IEEE MLSP": 1, "CCN": 1, "Bernstein Conference": 1,
    "CNS*": 1, "ICANN": 1, "EUSIPCO": 1,
    "BIOMAG": 2, "ICPR": 2, "S+SSPR": 2,
    "L4DC": 1, "IFAC SYSID": 3, "IEEE CDC": 1, "ACC": 1,
    "NOLTA": 1, "SIAM DS": 2, "CCS": 1, "NetSci": 1,
    "AutoML": 1, "LoG": 1, "CoRL": 1, "GECCO": 1, "SaTML": 1,
    "ProbML": 1, "AAMAS": 1, "MLSys": 1, "CogSci": 1,
    "ICIP": 1, "Interspeech": 1,
}


def _shift(value: str, years: int) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00")) if "T" in value else date.fromisoformat(value)
    try:
        shifted = parsed.replace(year=parsed.year + years)
    except ValueError:  # February 29 when the target year is not a leap year.
        shifted = parsed.replace(year=parsed.year + years, day=28)
    return shifted.isoformat()


def rollover_candidates(conferences: list[dict], as_of: date) -> list[dict]:
    latest = {}
    for item in conferences:
        if item["series"] not in latest or item["year"] > latest[item["series"]]["year"]:
            latest[item["series"]] = item
    candidates = []
    for series, cadence in CADENCE_YEARS.items():
        previous = latest.get(series)
        if previous is None or parse_date(previous["conference_end"]) >= as_of:
            continue
        years = cadence
        while parse_date(_shift(previous["conference_end"], years)) < as_of:
            years += cadence
        projected = deepcopy(previous)
        projected["year"] = previous["year"] + years
        projected["id"] = f'{stable_slug(series)}-{projected["year"]}'
        projected["short_title"] = f'{series} {projected["year"]}'
        projected["conference_start"] = _shift(previous["conference_start"], years)
        projected["conference_end"] = _shift(previous["conference_end"], years)
        projected["location"] = "To be announced"
        projected["confidence"] = "estimated"
        projected["last_checked"] = as_of.isoformat()
        projected["notes"] = (
            f'Provisional {cadence}-year cadence projection from {previous["short_title"]}. '
            "Meeting dates, location, and deadlines require organizer confirmation; "
            "website and source links refer to the prior edition."
        )
        for deadline in projected["deadlines"]:
            deadline["datetime"] = _shift(deadline["datetime"], years)
            deadline["confidence"] = "estimated"
            deadline.pop("open_observed_on", None)
            if deadline.get("opens_at"):
                deadline["opens_at"] = _shift(deadline["opens_at"], years)
        candidates.append(projected)
    return candidates


def append_candidates(path: Path, candidates: list[dict]) -> None:
    if not candidates:
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n# Provisional future editions; review organizer sources before publishing.\n")
        yaml.safe_dump(candidates, handle, sort_keys=False, allow_unicode=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    parser.add_argument("--write", action="store_true", help="Append projected records to data/conferences.yml")
    args = parser.parse_args()
    candidates = rollover_candidates(load_conferences(), args.as_of)
    for item in candidates:
        print(f'{item["id"]}: estimated from {item["notes"].split(" from ")[1].split(".")[0]}')
    if args.write:
        append_candidates(DATA_PATH, candidates)
    print(f"{len(candidates)} candidate edition(s){' appended' if args.write else ' (dry run)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
