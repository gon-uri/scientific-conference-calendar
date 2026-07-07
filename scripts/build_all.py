from __future__ import annotations

from pathlib import Path

from build_ics import build_calendars
from build_site import build_site
from validate import ROOT, load_conferences, load_controlled_topics, validate_conferences


def main() -> int:
    conferences = load_conferences()
    errors = validate_conferences(conferences, load_controlled_topics())
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
