#!/usr/bin/env python3
"""Validate every spoiler fixture and evaluation set in this repository.

A fixture is only useful if its annotations are internally consistent: an
ordinal that does not exist, a reference to a missing identifier, or a
"forbidden" entry whose reveal is *earlier* than the horizon makes the test
weaker while still looking green. This script rejects those cases.

Checks for fixtures:

1. `fixture.json` validates against `schema/fixture.schema.json`.
2. The referenced `story_file` exists and is non-empty.
3. Every identifier referenced by names/assertions/identity_links/status_changes
   exists.
4. Identifiers are unique across the fixture.
5. Every horizon lists ordinals inside the range revealed by the fixture.
6. For each horizon: `expected_present` entries have `first_reveal <= ordinal`,
   and `forbidden` entries have `first_reveal > ordinal`. A violation means the
   fixture contradicts itself.

Checks for evaluation sets:

1. `eval-set.json` validates against `schema/eval-set.schema.json`.
2. The parent directory contains a non-empty `PROVENANCE.md`.
3. Sample identifiers are unique.
4. Every sample references a declared `source_text_id`.
5. Split partitioning is strictly preserved: each `source_text_id` is assigned
   to a single split, and all its samples have the identical split.
6. Every sample uses a valid category and label.

Exit codes: 0 = clean, 1 = at least one problem.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_SCHEMA = json.loads(
    (ROOT / "schema" / "fixture.schema.json").read_text(encoding="utf-8")
)
EVAL_SCHEMA_PATH = ROOT / "schema" / "eval-set.schema.json"
EVAL_SCHEMA = (
    json.loads(EVAL_SCHEMA_PATH.read_text(encoding="utf-8"))
    if EVAL_SCHEMA_PATH.exists()
    else None
)

ALLOWED_CATEGORIES = {
    "direct_reveal",
    "implicit_hint",
    "alias_identity",
    "wrong_inference",
    "benign_explanation",
    "paraphrase",
}
ALLOWED_LABELS = {"SPOILER", "SAFE"}
ALLOWED_SPLITS = {"train", "val", "test"}


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
    try:
        rel: Path | str = path.relative_to(ROOT)
    except ValueError:
        rel = path
    try:
        fixture = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel}: invalid JSON: {exc}"]

    validator = Draft202012Validator(FIXTURE_SCHEMA)
    for error in sorted(validator.iter_errors(fixture), key=lambda e: list(e.path)):
        problems.append(
            f"{rel}: {'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        )
    if problems:
        return problems

    story = path.parent / fixture["story_file"]
    if not story.exists() or not story.read_text(encoding="utf-8").strip():
        problems.append(f"{rel}: story_file {fixture['story_file']} missing or empty")

    ids = [
        item["id"]
        for key in ("entities", "names", "assertions", "identity_links")
        for item in fixture.get(key, [])
    ]
    ids += [item["id"] for item in fixture.get("status_changes", [])]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    for duplicate in duplicates:
        problems.append(f"{rel}: duplicate identifier {duplicate}")

    entity_ids = {item["id"] for item in fixture["entities"]}
    for name in fixture["names"]:
        if name["entity_id"] not in entity_ids:
            problems.append(
                f"{rel}: name {name['id']} references unknown entity {name['entity_id']}"
            )
    for link in fixture.get("identity_links", []):
        for entity_id in link["entity_ids"]:
            if entity_id not in entity_ids:
                problems.append(
                    f"{rel}: identity link {link['id']} references unknown entity {entity_id}"
                )
    for assertion in fixture["assertions"]:
        if assertion["subject_id"] not in entity_ids:
            problems.append(
                f"{rel}: assertion {assertion['id']} references unknown subject {assertion['subject_id']}"
            )
    assertion_ids = {item["id"] for item in fixture["assertions"]}
    for change in fixture.get("status_changes", []):
        if change["assertion_id"] not in assertion_ids:
            problems.append(
                f"{rel}: status change {change['id']} references unknown assertion {change['assertion_id']}"
            )

    reveals = reveal_map(fixture)
    max_ordinal = max(reveals.values()) if reveals else 0
    for horizon in fixture["horizons"]:
        ordinal = horizon["ordinal"]
        if ordinal > max_ordinal:
            problems.append(
                f"{rel}: horizon {ordinal} exceeds the fixture's last reveal {max_ordinal}"
            )
        for entry_id in horizon["expected_present"]:
            if entry_id not in reveals:
                problems.append(
                    f"{rel}: horizon {ordinal} expects unknown identifier {entry_id}"
                )
            elif reveals[entry_id] > ordinal:
                problems.append(
                    f"{rel}: horizon {ordinal} expects {entry_id} but its reveal is {reveals[entry_id]}"
                )
        for entry_id in horizon["forbidden"]:
            if entry_id not in reveals:
                problems.append(
                    f"{rel}: horizon {ordinal} forbids unknown identifier {entry_id}"
                )
            elif reveals[entry_id] <= ordinal:
                problems.append(
                    f"{rel}: horizon {ordinal} forbids {entry_id} but it is revealed at {reveals[entry_id]} "
                    "(self-contradictory fixture)"
                )
    return problems


def validate_eval_set(path: Path) -> list[str]:
    problems: list[str] = []
    try:
        rel: Path | str = path.relative_to(ROOT)
    except ValueError:
        rel = path
    if EVAL_SCHEMA is None:
        return [f"{rel}: evaluation set schema missing at {EVAL_SCHEMA_PATH}"]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel}: invalid JSON: {exc}"]

    validator = Draft202012Validator(EVAL_SCHEMA)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        problems.append(
            f"{rel}: {'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        )
    if problems:
        return problems

    provenance = path.parent / "PROVENANCE.md"
    if not provenance.exists() or not provenance.read_text(encoding="utf-8").strip():
        problems.append(
            f"{rel}: PROVENANCE.md missing or empty in {path.parent.relative_to(ROOT)}"
        )

    source_texts = data.get("source_texts", [])
    source_map: dict[str, dict] = {}
    for st in source_texts:
        st_id = st.get("id")
        if not st_id:
            continue
        if st_id in source_map:
            problems.append(f"{rel}: duplicate source_text_id '{st_id}'")
        source_map[st_id] = st
        if st.get("split") not in ALLOWED_SPLITS:
            problems.append(
                f"{rel}: source text '{st_id}' has invalid split '{st.get('split')}'"
            )

    samples = data.get("samples", [])
    if not samples:
        problems.append(f"{rel}: samples array is empty")

    seen_sample_ids: set[str] = set()
    source_to_split: dict[str, set[str]] = {}

    for idx, sample in enumerate(samples):
        s_id = sample.get("id", f"<index {idx}>")
        if s_id in seen_sample_ids:
            problems.append(f"{rel}: duplicate sample id '{s_id}'")
        seen_sample_ids.add(s_id)

        st_id = sample.get("source_text_id")
        if st_id not in source_map:
            problems.append(
                f"{rel}: sample '{s_id}' references undeclared source_text_id '{st_id}'"
            )
        else:
            expected_split = source_map[st_id].get("split")
            actual_split = sample.get("split")
            if actual_split != expected_split:
                problems.append(
                    f"{rel}: sample '{s_id}' split '{actual_split}' does not match declared split '{expected_split}' for '{st_id}'"
                )
            source_to_split.setdefault(st_id, set()).add(actual_split)

            total_h = source_map[st_id].get("total_horizons", 0)
            h_ord = sample.get("horizon_ordinal", 0)
            if h_ord > total_h:
                problems.append(
                    f"{rel}: sample '{s_id}' horizon_ordinal {h_ord} exceeds total_horizons {total_h} for '{st_id}'"
                )

        cat = sample.get("category")
        if cat not in ALLOWED_CATEGORIES:
            problems.append(f"{rel}: sample '{s_id}' has unknown category '{cat}'")

        label = sample.get("label")
        if label not in ALLOWED_LABELS:
            problems.append(f"{rel}: sample '{s_id}' has unknown label '{label}'")

    for st_id, splits in source_to_split.items():
        if len(splits) > 1:
            problems.append(
                f"{rel}: source_text_id '{st_id}' is mixed across multiple splits: {sorted(splits)}"
            )

    return problems


def main() -> int:
    fixtures = sorted(ROOT.glob("fixtures/**/fixture.json"))
    eval_sets = sorted(ROOT.glob("fixtures/eval/**/eval-set.json"))

    if not fixtures and not eval_sets:
        print("no fixtures or evaluation sets found", file=sys.stderr)
        return 1

    problems: list[str] = []
    for path in fixtures:
        problems += validate_fixture(path)
    for path in eval_sets:
        problems += validate_eval_set(path)

    for problem in problems:
        print(problem)

    if problems:
        print(f"\n{len(problems)} problem(s) found", file=sys.stderr)
        return 1

    eval_msg = f", {len(eval_sets)} eval set(s)" if eval_sets else ""
    print(f"fixtures ok: {len(fixtures)} fixture(s){eval_msg} validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
