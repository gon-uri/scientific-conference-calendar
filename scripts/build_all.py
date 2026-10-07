from __future__ import annotations

from pathlib import Path

from build_ics import build_calendars
from build_site import build_site
from conference_scopes import load_scopes, validate_scopes
from validate import (
    ROOT,
    load_acceptance_rates,
    load_ccf_rankings,
    load_conferences,
    load_controlled_topics,
    load_icore_rankings,
    validate_conferences,
    validate_acceptance_rates,
    validate_ccf_rankings,
    validate_icore_rankings,
)


def main() -> int:
    conferences = load_conferences()
    errors = validate_conferences(conferences, load_controlled_topics())
    errors.extend(validate_icore_rankings(conferences, load_icore_rankings()))
    errors.extend(validate_ccf_rankings(conferences, load_ccf_rankings()))
    errors.extend(validate_acceptance_rates(conferences, load_acceptance_rates()))
    errors.extend(validate_scopes(conferences, load_scopes(), load_controlled_topics() or set()))
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(conferences)} conferences.")

    outputs: list[Path] = []
    outputs.extend(build_calendars())
    outputs.append(build_site())

    print("Generated:")
    for output in outputs:
        print(f"- {output.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
