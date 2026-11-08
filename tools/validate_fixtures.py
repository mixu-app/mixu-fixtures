#!/usr/bin/env python3
"""Validate every spoiler fixture in this repository.

A fixture is only useful if its annotations are internally consistent: an
ordinal that does not exist, a reference to a missing identifier, or a
"forbidden" entry whose reveal is *earlier* than the horizon makes the test
weaker while still looking green. This script rejects those cases.

Checks:

1. `fixture.json` validates against `schema/fixture.schema.json`.
2. The referenced `story_file` exists and is non-empty.
3. Every identifier referenced by names/assertions/identity_links/status_changes
   exists.
4. Identifiers are unique across the fixture.
5. Every horizon lists ordinals inside the range revealed by the fixture.
6. For each horizon: `expected_present` entries have `first_reveal <= ordinal`,
   and `forbidden` entries have `first_reveal > ordinal`. A violation means the
   fixture contradicts itself.

Exit codes: 0 = clean, 1 = at least one fixture problem.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "fixture.schema.json").read_text(encoding="utf-8"))


def reveal_map(fixture: dict) -> dict[str, int]:
    reveals: dict[str, int] = {}
    for key in ("entities", "names", "identity_links", "assertions"):
        for item in fixture.get(key, []):
            entry_id = item.get("id") or item.get("assertion_id")
            if not entry_id:
                continue
            ordinal = item.get("first_reveal", item.get("reveal_ordinal"))
            if ordinal is not None:
                reveals[entry_id] = ordinal
    for change in fixture.get("status_changes", []):
        reveals.setdefault(change["id"], change["reveal_ordinal"])
    return reveals


def validate_fixture(path: Path) -> list[str]:
    problems: list[str] = []
    rel = path.relative_to(ROOT)
    try:
        fixture = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel}: invalid JSON: {exc}"]

    validator = Draft202012Validator(SCHEMA)
    for error in sorted(validator.iter_errors(fixture), key=lambda e: list(e.path)):
        problems.append(f"{rel}: {'/'.join(map(str, error.path)) or '<root>'}: {error.message}")
    if problems:
        return problems

    story = path.parent / fixture["story_file"]
    if not story.exists() or not story.read_text(encoding="utf-8").strip():
        problems.append(f"{rel}: story_file {fixture['story_file']} missing or empty")

    ids = [item["id"] for key in ("entities", "names", "assertions", "identity_links") for item in fixture.get(key, [])]
    ids += [item["id"] for item in fixture.get("status_changes", [])]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    for duplicate in duplicates:
        problems.append(f"{rel}: duplicate identifier {duplicate}")

    entity_ids = {item["id"] for item in fixture["entities"]}
    for name in fixture["names"]:
        if name["entity_id"] not in entity_ids:
            problems.append(f"{rel}: name {name['id']} references unknown entity {name['entity_id']}")
    for link in fixture.get("identity_links", []):
        for entity_id in link["entity_ids"]:
            if entity_id not in entity_ids:
                problems.append(f"{rel}: identity link {link['id']} references unknown entity {entity_id}")
    for assertion in fixture["assertions"]:
        if assertion["subject_id"] not in entity_ids:
            problems.append(f"{rel}: assertion {assertion['id']} references unknown subject {assertion['subject_id']}")
    assertion_ids = {item["id"] for item in fixture["assertions"]}
    for change in fixture.get("status_changes", []):
        if change["assertion_id"] not in assertion_ids:
            problems.append(f"{rel}: status change {change['id']} references unknown assertion {change['assertion_id']}")

    reveals = reveal_map(fixture)
    max_ordinal = max(reveals.values()) if reveals else 0
    for horizon in fixture["horizons"]:
        ordinal = horizon["ordinal"]
        if ordinal > max_ordinal:
            problems.append(f"{rel}: horizon {ordinal} exceeds the fixture's last reveal {max_ordinal}")
        for entry_id in horizon["expected_present"]:
            if entry_id not in reveals:
                problems.append(f"{rel}: horizon {ordinal} expects unknown identifier {entry_id}")
            elif reveals[entry_id] > ordinal:
                problems.append(
                    f"{rel}: horizon {ordinal} expects {entry_id} but its reveal is {reveals[entry_id]}"
                )
        for entry_id in horizon["forbidden"]:
            if entry_id not in reveals:
                problems.append(f"{rel}: horizon {ordinal} forbids unknown identifier {entry_id}")
            elif reveals[entry_id] <= ordinal:
                problems.append(
                    f"{rel}: horizon {ordinal} forbids {entry_id} but it is revealed at {reveals[entry_id]} "
                    "(self-contradictory fixture)"
                )
    return problems


def main() -> int:
    fixtures = sorted(ROOT.glob("fixtures/**/fixture.json"))
    if not fixtures:
        print("no fixtures found", file=sys.stderr)
        return 1
    problems: list[str] = []
    for path in fixtures:
        problems += validate_fixture(path)
    for problem in problems:
        print(problem)
    if problems:
        print(f"\n{len(problems)} fixture problem(s)", file=sys.stderr)
        return 1
    print(f"fixtures ok: {len(fixtures)} validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
