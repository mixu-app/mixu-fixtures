# SPDX-License-Identifier: Apache-2.0
"""Generation-only export and offline source-coverage targets for fresh rollouts."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "fixtures/benchmarks/sequential-source"
VERSION = "sequential-source-fixtures-1"
SCORER_SHA256 = "0970e112a39f1c37590a1db80e2a2c7ec7ded92faeb61f582ca2a846f3fa7c86"
OLD_CASES = ("gm-en-01", "gm-ja-01", "gm-zh-02", "hgm-en-01", "hgm-ja-01", "hgm-zh-01", "gm-en-01-n048-d002")
PILOT_CASE = "gm-zh-01"
NEW_HORIZONS = (3, 4, 5, 6, 7, 8, 10, 11, 12)
LAYERS = {"OUTER", "INNER:loop1", "INNER:loop2"}
RELATIONS = {"stored", "placed", "replaced", "moved", "has_damage", "same_as", "locked_at", "lit_at",
             "open_at", "status", "records", "occupation", "deposited", "hung", "received", "distinct_from",
             "delivered", "confirms", "entered", "broke", "condition", "left_untouched", "quotes", "contains",
             "classification", "location", "links_to", "stored_in"}
GENERATION_FIELDS = {"case_id", "language", "input_path", "input_sha256", "segment_count", "rights_basis"}
MAX_NEW_CASE_CHARACTERS = 1200


def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else packed(value).encode()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def relative(root, name):
    if not isinstance(name, str) or Path(name).is_absolute():
        raise ValueError("Artifact path must be relative")
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Artifact path escapes export")
    return path


def validate_source(inp, gold, *, require_literal_entity_surfaces=False):
    if set(inp) != {"schema_version", "case_id", "language", "segments"} or inp["schema_version"] != 1:
        raise ValueError("Invalid generation input envelope")
    segments = inp["segments"]
    if (not segments or any(type(s.get("ordinal")) is not int for s in segments) or
            [s["ordinal"] for s in segments] != list(range(1, len(segments) + 1))):
        raise ValueError("Nonsequential source ordinals")
    if len({s["segment_id"] for s in segments}) != len(segments):
        raise ValueError("Duplicate segment ID")
    for segment in segments:
        if (set(segment) != {"ordinal", "segment_id", "text"} or
                not isinstance(segment["segment_id"], str) or not segment["segment_id"] or
                not isinstance(segment["text"], str) or not segment["text"]):
            raise ValueError("Invalid generation segment")
    if (gold["case_id"] != inp["case_id"] or gold["content_basis"] != "SYNTHETIC_ORIGINAL" or
            gold["license"] != "CC0-1.0" or not gold["rights_note"]):
        raise ValueError("Invalid source rights or case identity")
    by_ordinal = {s["ordinal"]: s for s in segments}

    def proofs(rows, horizon, mention=False):
        if not rows:
            raise ValueError("Missing source proof")
        for p in rows:
            if type(p.get("ordinal")) is not int:
                raise ValueError("Invalid proof ordinal")
            source = by_ordinal.get(p["ordinal"])
            if source is None or p["ordinal"] > horizon or p["segment_id"] != source["segment_id"]:
                raise ValueError("Unknown or future proof")
            a, b = p["start"], p["end"]
            if (type(a) is not int or type(b) is not int or not 0 <= a < b <= len(source["text"]) or
                    source["text"][a:b] != p["text" if mention else "quote"]):
                raise ValueError("Nonverbatim source proof")

    entities = {e["entity_id"]: e for e in gold["entities"]}
    facts = {f["fact_id"]: f for f in gold["facts"]}
    if len(entities) != len(gold["entities"]) or len(facts) != len(gold["facts"]):
        raise ValueError("Duplicate reference ID")
    for entity in entities.values():
        proofs(entity["mentions"], len(segments), mention=True)
        for name in [entity["name"], *entity.get("aliases", [])] if require_literal_entity_surfaces else []:
            if not any(name in s["text"] for s in segments):
                raise ValueError("Entity surface absent from source")
    for fact in facts.values():
        if fact["relation"] not in RELATIONS or fact["layer"] not in LAYERS or fact["epistemic_status"] not in {"OBSERVED", "CLAIMED"}:
            raise ValueError("Outside frozen benchmark vocabulary")
        if type(fact["valid_from_ordinal"]) is not int or not 1 <= fact["valid_from_ordinal"] <= len(segments):
            raise ValueError("Invalid reference reveal horizon")
        if fact["epistemic_status"] == "CLAIMED" and not fact["qualifier"].get("speaker"):
            raise ValueError("Claim lacks explicit speaker")
        proofs(fact["provenance"], fact["valid_from_ordinal"])
    for transition in gold["transitions"]:
        claim = facts.get(transition["claim_fact_id"])
        if (type(transition["ordinal"]) is not int or not 1 <= transition["ordinal"] <= len(segments) or
                claim is None or claim["epistemic_status"] != "CLAIMED" or
                transition["ordinal"] <= claim["valid_from_ordinal"] or
                transition["to_status"] not in {"RETRACTED", "CORROBORATED", "CONTRADICTED"}):
            raise ValueError("Invalid correction target/horizon")
        if any(fid not in facts for fid in transition["evidence_fact_ids"]):
            raise ValueError("Unknown correction evidence")
        evidence = [facts[fid] for fid in transition["evidence_fact_ids"]]
        if not any(f["valid_from_ordinal"] == transition["ordinal"] for f in evidence):
            raise ValueError("Correction lacks current evidence")
        if any(f["valid_from_ordinal"] > transition["ordinal"] for f in evidence):
            raise ValueError("Future correction evidence")
    for identity in gold["identity_constraints"]:
        if (type(identity["valid_from_ordinal"]) is not int or
                not 1 <= identity["valid_from_ordinal"] <= len(segments) or
                identity["left"] not in entities or identity["right"] not in entities or
                identity["left"] == identity["right"] or identity["relation"] not in {"SAME_AS", "DISTINCT"}):
            raise ValueError("Invalid identity reference")
        proofs(identity["provenance"], identity["valid_from_ordinal"])
    if (len(gold["horizons"]) != len(segments) or
            any(type(h["ordinal"]) is not int for h in gold["horizons"]) or
            {h["ordinal"] for h in gold["horizons"]} != set(by_ordinal)):
        raise ValueError("Missing source horizon")
    for horizon in gold["horizons"]:
        h = horizon["ordinal"]
        required = {f["fact_id"] for f in facts.values() if f["valid_from_ordinal"] <= h}
        forbidden = set(facts) - required
        if set(horizon["required_fact_ids"]) != required or set(horizon["forbidden_fact_ids"]) != forbidden:
            raise ValueError("Inconsistent reveal horizon")


def new_samples(inp, gold):
    facts = {f["fact_id"]: f for f in gold["facts"]}
    names = {e["entity_id"]: e["name"] for e in gold["entities"]}
    samples = []
    for horizon in NEW_HORIZONS:
        segment = next(s for s in inp["segments"] if s["ordinal"] == horizon)
        aliases = {"林岚": ["装裱师"]}
        if horizon >= 8:
            aliases["桑禾"] = ["黄披肩客人"]
        transitions = []
        for t in gold["transitions"]:
            if t["ordinal"] == horizon:
                transitions.append({**t, "claim": facts[t["claim_fact_id"]],
                                    "current_evidence": [p for fid in t["evidence_fact_ids"]
                                                         for p in facts[fid]["provenance"] if p["ordinal"] == horizon]})
        samples.append({"case_id": inp["case_id"], "horizon": horizon,
                        "current_segment_sha256": digest(segment),
                        "fact_targets": [f for f in gold["facts"] if f["critical"] and f["valid_from_ordinal"] == horizon],
                        "transition_targets": transitions,
                        "identity_targets": [{**i, "left": names[i["left"]], "right": names[i["right"]]}
                                             for i in gold["identity_constraints"] if i["valid_from_ordinal"] == horizon],
                        "source_role_aliases": aliases,
                        "role_same_person_pairs": [{"left": "林岚", "right": "装裱师"}],
                        "unresolved_identity_pairs": []})
    return samples


def export(corpus, old_targets_path, output):
    manifest = load(corpus / "manifest.json")
    old_targets = load(old_targets_path)
    old_cases = {r["case_id"]: r for r in manifest["cases"]}
    output.mkdir(parents=True, exist_ok=True)
    (output / "inputs").mkdir(exist_ok=True)
    (output / "gold").mkdir(exist_ok=True)
    cases, pilot, evaluation = [], [], []
    for case_id in [*OLD_CASES, PILOT_CASE]:
        row = old_cases[case_id]
        inp_bytes = relative(corpus, row["input_path"]).read_bytes()
        gold_bytes = relative(corpus, row["gold_path"]).read_bytes()
        if digest(inp_bytes) != row["input_sha256"] or digest(gold_bytes) != row["gold_sha256"]:
            raise ValueError("Old source checksum mismatch")
        inp, gold = json.loads(inp_bytes), json.loads(gold_bytes)
        validate_source(inp, gold)
        path = f"inputs/{case_id}.json"
        (output / path).write_bytes(inp_bytes)
        generation = dict(case_id=case_id, language=inp["language"], input_path=path,
                          input_sha256=digest(inp_bytes), segment_count=len(inp["segments"]), rights_basis=gold["content_basis"])
        if case_id == PILOT_CASE:
            pilot.append(generation)
        else:
            cases.append(generation)
            gold_path = f"gold/{case_id}.json"
            (output / gold_path).write_bytes(gold_bytes)
            evaluation.append({**generation, "gold_path": gold_path, "gold_sha256": digest(gold_bytes)})
    inp_bytes, gold_bytes = (DATA / "new-input.json").read_bytes(), (DATA / "new-gold.json").read_bytes()
    inp, gold = json.loads(inp_bytes), json.loads(gold_bytes)
    validate_source(inp, gold, require_literal_entity_surfaces=True)
    if len(inp["segments"]) != 12 or sum(len(s["text"]) for s in inp["segments"]) > MAX_NEW_CASE_CHARACTERS:
        raise ValueError("New diagnostic source size changed")
    case_id = inp["case_id"]
    path, gold_path = f"inputs/{case_id}.json", f"gold/{case_id}.json"
    (output / path).write_bytes(inp_bytes)
    (output / gold_path).write_bytes(gold_bytes)
    row = dict(case_id=case_id, language=inp["language"], input_path=path, input_sha256=digest(inp_bytes),
               segment_count=len(inp["segments"]), rights_basis=gold["content_basis"])
    cases.append(row)
    evaluation.append({**row, "gold_path": gold_path, "gold_sha256": digest(gold_bytes)})
    for filename, rows in [("generation.json", cases), ("pilot-generation.json", pilot)]:
        if any(set(r) != GENERATION_FIELDS for r in rows):
            raise ValueError("Generation manifest field boundary violated")
        (output / filename).write_text(packed(dict(schema_version=1, benchmark_id="sequential-source-generation-1", cases=rows)) + "\n")
    selected = [copy.deepcopy(s) for s in old_targets["samples"] if s["case_id"] in OLD_CASES]
    if len(selected) != 20 or len({(s["case_id"], s["horizon"]) for s in selected}) != 20:
        raise ValueError("Frozen original target selection changed")
    for sample in selected:
        source = load(output / f"inputs/{sample['case_id']}.json")
        current = next((s for s in source["segments"] if s["ordinal"] == sample["horizon"]), None)
        if current is None or sample["current_segment_sha256"] != digest(current):
            raise ValueError("Original selected target source mismatch")
    targets = {"evaluation_version": VERSION, "content_basis": "SYNTHETIC_ORIGINAL", "license": "CC0-1.0",
               "relation_aliases": old_targets["relation_aliases"], "samples": [*selected, *new_samples(inp, gold)]}
    (output / "targets.json").write_text(packed(targets) + "\n")
    offline = dict(schema_version=1, benchmark_id="sequential-source-evaluation-1", scorer_sha256=SCORER_SHA256,
                   generation_manifest_sha256=digest((output / "generation.json").read_bytes()),
                   targets_path="targets.json", targets_sha256=digest((output / "targets.json").read_bytes()),
                   source_manifest_sha256=digest((corpus / "manifest.json").read_bytes()),
                   original_targets_sha256=digest(old_targets_path.read_bytes()), cases=evaluation)
    (output / "evaluation.json").write_text(packed(offline) + "\n")
    return {"main_cases": len(cases), "main_segments": sum(r["segment_count"] for r in cases),
            "target_horizons": len(targets["samples"]), "pilot_cases": len(pilot),
            **{name + "_sha256": digest((output / name).read_bytes()) for name in
               ["generation.json", "pilot-generation.json", "evaluation.json", "targets.json"]}}


def source_coverage(targets, case_id, horizon, selected_sources, history):
    """Offline historical claim-source span coverage; never a retrieval query."""
    if any(s["ordinal"] > horizon for s in history):
        raise ValueError("Future history in source coverage")
    sources = {s["ordinal"]: s for s in history}
    valid, invalid = [], 0
    for fragment in selected_sources:
        if not isinstance(fragment, dict) or type(fragment.get("ordinal")) is not int:
            invalid += 1
            continue
        ordinal, text = fragment.get("ordinal"), fragment.get("text")
        source = sources.get(ordinal)
        if (source is None or ordinal >= horizon or fragment.get("segment_id") != source["segment_id"] or
                not isinstance(text, str) or not text):
            invalid += 1
            continue
        start = fragment.get("start")
        if type(start) is int and 0 <= start <= len(source["text"]) - len(text) and source["text"][start:start + len(text)] == text:
            pass
        else:
            positions, pos = [], source["text"].find(text)
            while pos >= 0:
                positions.append(pos)
                pos = source["text"].find(text, pos + 1)
            if len(positions) != 1:
                invalid += 1
                continue
            start = positions[0]
        valid.append((ordinal, start, start + len(text)))
    sample = next((s for s in targets["samples"] if s["case_id"] == case_id and s["horizon"] == horizon), None)
    findings = []
    for transition in sample["transition_targets"] if sample else []:
        claim = transition["claim"]
        spans = [p for p in claim["provenance"] if p["ordinal"] == claim["valid_from_ordinal"] and p["ordinal"] < horizon]
        if not spans:
            raise ValueError("Reference correction lacks historical claim-source spans")
        hits = [any(n == p["ordinal"] and a <= p["start"] and b >= p["end"] for n, a, b in valid) for p in spans]
        findings.append(dict(claim_target_id=transition["claim_fact_id"], required_span_count=len(spans),
                             covered_span_count=sum(hits), fully_covered=all(hits)))
    return dict(coverage_version=VERSION, case_id=case_id, horizon=horizon,
                historical_claim_targets=len(findings), historical_claim_source_spans_required=sum(f["required_span_count"] for f in findings),
                historical_claim_source_spans_covered=sum(f["covered_span_count"] for f in findings),
                historical_claims_fully_covered=sum(f["fully_covered"] for f in findings),
                selected_source_fragments=len(selected_sources), invalid_retrieved_fragments=invalid,
                identity_source_coverage="UNASSESSED", claim_findings=findings)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--old-targets", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(export(args.corpus, args.old_targets, args.output_dir), sort_keys=True))


if __name__ == "__main__":
    main()
