# SPDX-License-Identifier: Apache-2.0
"""Frozen source-defined selection and bounded structural update-link proxies.

Generation must never load targets.json. This module is an offline evaluator,
not an extraction prompt, a semantic judge, or a graph repair mechanism.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import unicodedata

VERSION = "graph-update-eval-1"
KINDS = ("entities", "facts", "transitions", "identity_merges")
MAX_PROVENANCE = 16
SELECTION = {
    "gm-en-01": [2, 4, 5],
    "gm-ja-01": [2, 4, 5],
    "gm-zh-02": [2, 3],
    "hgm-en-01": [4, 8, 11],
    "hgm-ja-01": [4, 8, 11],
    "hgm-zh-01": [3, 9, 11],
    "gm-en-01-n048-d002": [10, 29, 38],
}
ROLE_ALIASES = {
    "hgm-en-01": {"Leon": ["bell mender", "the bell mender"]},
    "hgm-ja-01": {"栗原澄": ["朝番の配送係"]},
    "hgm-zh-01": {"岑雨": ["夜班保管员"]},
}
RELATION_ALIASES = {
    "occupation": ["has_occupation", "works_as", "is_a"],
    "stored": ["stored_at", "kept", "kept_at"],
    "same_as": ["identical_to"],
    "distinct_from": ["different_from"],
}


def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value):
    return hashlib.sha256(value).hexdigest()


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", str(value)).casefold().split())


def values(state, kind):
    records = state.get(kind, {})
    return list(records.values()) if isinstance(records, dict) else list(records)


def string_fields(record, fields):
    return all(isinstance(record.get(field), str) and record[field] for field in fields)


def qualifier_shape(qualifier):
    return isinstance(qualifier, dict) and all(isinstance(k, str) and isinstance(v, str)
                                             for k, v in qualifier.items())


def record_shape(record, kind):
    """Check evaluator-safe v1 record shapes, not semantic or full reducer validity."""
    if not isinstance(record, dict):
        return False
    proofs = record.get("provenance")
    if not isinstance(proofs, list) or not 0 < len(proofs) <= MAX_PROVENANCE:
        return False
    for proof in proofs:
        # The generation contract makes coordinates optional. Only source text,
        # never reference gold, may derive them in the read-only scoring view.
        if not isinstance(proof, dict) or not string_fields(proof, ["segment_id", "quote"]):
            return False
    if "layer" in record and not isinstance(record["layer"], str):
        return False
    if kind == "entities":
        aliases = record.get("aliases", [])
        return (string_fields(record, ["entity_id", "name"]) and isinstance(aliases, list) and
                all(isinstance(v, str) for v in aliases))
    if kind == "facts":
        return (string_fields(record, ["fact_id", "subject", "relation", "object", "layer", "epistemic_status"]) and
                qualifier_shape(record.get("qualifier", {})))
    if kind == "identity_merges":
        return string_fields(record, ["merge_id", "left", "right", "relation"])
    if not string_fields(record, ["transition_id", "to_status"]):
        return False
    if "fact_id" in record and not isinstance(record["fact_id"], str):
        return False
    if isinstance(record.get("fact_id"), str) and record["fact_id"]:
        return True
    query = record.get("target")
    return (isinstance(query, dict) and string_fields(query, ["subject", "relation", "object", "layer"]) and
            ("epistemic_status" not in query or isinstance(query["epistemic_status"], str)) and
            qualifier_shape(query.get("qualifier", {})))


def source_view(record, history):
    """Resolve optional coordinates on a copy with the frozen source-only proof rules."""
    by_id = {s["segment_id"]: s for s in history}
    normalized = copy.deepcopy(record)
    counts = {"normalized_spans": 0, "ambiguous_spans": 0,
              "nonverbatim_spans": 0, "unknown_spans": 0}
    scorable = True
    for proof in normalized["provenance"]:
        source = by_id.get(proof["segment_id"])
        if source is None:
            counts["unknown_spans"] += 1
            scorable = False
            continue
        quote = proof["quote"]
        start, end = proof.get("start"), proof.get("end")
        valid_slice = (type(start) is int and type(end) is int and
                       0 <= start < end <= len(source["text"]) and
                       source["text"][start:end] == quote)
        if not valid_slice:
            positions, pos = [], source["text"].find(quote)
            while pos >= 0:
                positions.append(pos)
                pos = source["text"].find(quote, pos + 1)
            if len(positions) != 1:
                counts["ambiguous_spans" if positions else "nonverbatim_spans"] += 1
                scorable = False
                continue
            start, end = positions[0], positions[0] + len(quote)
        if (proof.get("start"), proof.get("end"), proof.get("ordinal")) != (start, end, source["ordinal"]):
            counts["normalized_spans"] += 1
        proof.update(start=start, end=end, ordinal=source["ordinal"])
    return normalized if scorable else None, counts


def inspect_raw(raw_delta, history):
    """Inspect source-normalized copies; raw bytes/objects and gold stay untouched."""
    diagnostics = {"invalid_envelope": int(not isinstance(raw_delta, dict) or set(raw_delta) != set(KINDS)),
                   "invalid_kind_collections": [], "invalid_record_shapes": {k: 0 for k in KINDS},
                   "source_normalized_records": 0, "source_normalized_spans": 0,
                   "source_unscorable_records": 0, "source_ambiguous_spans": 0,
                   "source_nonverbatim_spans": 0, "source_unknown_spans": 0}
    safe = {kind: [] for kind in KINDS}
    if not isinstance(raw_delta, dict):
        return safe, diagnostics
    for kind in KINDS:
        records = raw_delta.get(kind)
        if not isinstance(records, list):
            diagnostics["invalid_kind_collections"].append(kind)
            diagnostics["invalid_envelope"] = 1
            continue
        for record in records:
            if not record_shape(record, kind):
                diagnostics["invalid_record_shapes"][kind] += 1
            else:
                viewed, counts = source_view(record, history)
                for key, count in counts.items():
                    diagnostics["source_" + key] += count
                if viewed is None:
                    diagnostics["source_unscorable_records"] += 1
                else:
                    diagnostics["source_normalized_records"] += int(counts["normalized_spans"] > 0)
                    safe[kind].append(viewed)
    return safe, diagnostics


def build(corpus, output):
    manifest_bytes = (corpus / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    by_case = {row["case_id"]: row for row in manifest["cases"]}
    samples, targets, sources = [], [], {}
    for case_id, horizons in SELECTION.items():
        row = by_case[case_id]
        inp_bytes = (corpus / row["input_path"]).read_bytes()
        gold_bytes = (corpus / row["gold_path"]).read_bytes()
        if sha(inp_bytes) != row["input_sha256"] or sha(gold_bytes) != row["gold_sha256"]:
            raise ValueError("Corpus source checksum mismatch")
        inp, gold = json.loads(inp_bytes), json.loads(gold_bytes)
        if gold["content_basis"] != "SYNTHETIC_ORIGINAL":
            raise ValueError("This selection requires the frozen original synthetic corpus")
        sources[case_id] = {"input_sha256": sha(inp_bytes), "gold_sha256": sha(gold_bytes)}
        facts = {f["fact_id"]: f for f in gold["facts"]}
        entities = {e["entity_id"]: e["name"] for e in gold["entities"]}
        for horizon in horizons:
            segment = next(s for s in inp["segments"] if s["ordinal"] == horizon)
            samples.append({"case_id": case_id, "horizon": horizon})
            transitions = []
            for t in gold["transitions"]:
                if t["ordinal"] == horizon:
                    transitions.append({**t, "claim": facts[t["claim_fact_id"]],
                                        "current_evidence": [p for fid in t["evidence_fact_ids"]
                                                             for p in facts[fid]["provenance"]
                                                             if p["ordinal"] == horizon]})
            identities = []
            for identity in gold["identity_constraints"]:
                if identity["valid_from_ordinal"] == horizon:
                    identities.append({**identity, "left": entities[identity["left"]],
                                       "right": entities[identity["right"]]})
            unresolved = []
            if case_id == "gm-ja-01" and horizon in [2, 4]:
                unresolved.append({"left": entities["e1"], "right": entities["e2"],
                                   "allowed_asserted_relations": []})
            # Different full names and separate files do not establish a typed identity proof.
            if case_id == "gm-zh-02" and horizon == 2:
                unresolved.append({"left": entities["e1"], "right": entities["e2"],
                                   "allowed_asserted_relations": []})
            role_pairs = [{"left": name, "right": alias} for name, aliases in
                          ROLE_ALIASES.get(case_id, {}).items() for alias in aliases[:1]]
            targets.append({
                "case_id": case_id, "horizon": horizon,
                "current_segment_sha256": sha(packed(segment).encode()),
                "fact_targets": [f for f in gold["facts"] if f.get("critical") and
                                 f["valid_from_ordinal"] == horizon],
                "transition_targets": transitions, "identity_targets": identities,
                "unresolved_identity_pairs": unresolved, "role_same_person_pairs": role_pairs,
                "source_role_aliases": ROLE_ALIASES.get(case_id, {}),
            })
    output.mkdir(parents=True, exist_ok=True)
    selection = {"samples": samples}
    target_document = {"evaluation_version": VERSION, "content_basis": "SYNTHETIC_ORIGINAL",
                       "license": "CC0-1.0", "rights_note": "Derived annotations of the original Mixu synthetic corpus; no published book text.",
                       "source_manifest_sha256": sha(manifest_bytes), "source_files": sources,
                       "selection_sha256": sha((packed(selection) + "\n").encode()),
                       "relation_aliases": RELATION_ALIASES, "samples": targets}
    (output / "selection.json").write_text(packed(selection) + "\n")
    (output / "targets.json").write_text(packed(target_document) + "\n")
    return {"samples": len(samples), "selection_sha256": target_document["selection_sha256"],
            "targets_sha256": sha((output / "targets.json").read_bytes())}


def alias_lookup(targets, sample):
    result = {}
    for canonical, aliases in sample.get("source_role_aliases", {}).items():
        for alias in [canonical, *aliases]:
            result[norm(alias)] = norm(canonical)
    return result


def surface(value, state, aliases):
    key = str(value)
    key = state.get("_entity_aliases", {}).get(key, key)
    record = state.get("entities", {}).get(key, {})
    name = norm(record.get("name", key))
    return aliases.get(name, name)


def relation(value, targets):
    name = norm(value)
    for canonical, aliases in targets.get("relation_aliases", {}).items():
        if name in [norm(canonical), *map(norm, aliases)]:
            return norm(canonical)
    return name


def signature(fact, state, aliases, targets):
    qualifier = fact.get("qualifier") or {}
    return (surface(fact.get("subject", ""), state, aliases), relation(fact.get("relation", ""), targets),
            surface(fact.get("object", ""), state, aliases), fact.get("layer", "OUTER"),
            fact.get("epistemic_status"), surface(qualifier.get("speaker", ""), state, aliases),
            qualifier.get("polarity", "POSITIVE"))


def anchored(record, history, ordinal=None, expected=None):
    segments = {s["ordinal"]: s for s in history}
    proofs = record.get("provenance", [])
    if not isinstance(proofs, list):
        return False
    for p in proofs:
        if not isinstance(p, dict) or type(p.get("ordinal")) is not int:
            continue
        if ordinal is not None and p.get("ordinal") != ordinal:
            continue
        source = segments.get(p.get("ordinal"))
        if not source or p.get("segment_id") != source.get("segment_id"):
            continue
        start, end = p.get("start"), p.get("end")
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(source["text"]):
            continue
        if "quote" in p and p["quote"] != source["text"][start:end]:
            continue
        if expected is None or any(p["ordinal"] == e["ordinal"] and
                                   max(start, e["start"]) < min(end, e["end"])
                                   for e in expected):
            return True
    return False


def claim_reference_match(fact, gold, state, aliases, history):
    """Source-claim attribution proxy, deliberately not full semantic entailment."""
    q, gq = fact.get("qualifier") or {}, gold.get("qualifier") or {}
    return (fact.get("epistemic_status") == "CLAIMED" and
            fact.get("layer", "OUTER") == gold.get("layer", "OUTER") and
            q.get("polarity", "POSITIVE") == gq.get("polarity", "POSITIVE") and
            surface(q.get("speaker", ""), state, aliases) == norm(gq.get("speaker", "")) and
            anchored(fact, history, expected=gold["provenance"]))


def fresh_records(before, after, kind, id_key):
    old = {r[id_key] for r in values(before, kind)}
    return [r for r in values(after, kind) if r.get(id_key) not in old]


def admitted_current_facts(before, after, horizon):
    """Include newly admitted evidence on reused facts, including reducer event ledgers."""
    def project(state):
        records = {r["fact_id"]: copy.deepcopy(r) for r in values(state, "facts")}
        for event in values(state, "_fact_events"):
            if event.get("fact_id") in records:
                record = records[event["fact_id"]]
                for proof in event.get("provenance", []):
                    if proof not in record.get("provenance", []):
                        record.setdefault("provenance", []).append(proof)
        return records

    old, new = project(before), project(after)
    return [record for key, record in new.items() if key not in old or
            any(proof.get("ordinal") == horizon and proof not in old[key].get("provenance", [])
                for proof in record.get("provenance", []))]


def transition_candidates(record, state, targets, aliases):
    fact_id = state.get("_fact_aliases", {}).get(record.get("fact_id"), record.get("fact_id"))
    if fact_id in state.get("facts", {}):
        return [state["facts"][fact_id]]
    query = record.get("target")
    if not isinstance(query, dict):
        return []
    candidates = []
    for fact in values(state, "facts"):
        if not all(surface(fact.get(k, ""), state, aliases) == surface(query[k], state, aliases)
                   for k in ["subject", "object"] if k in query):
            continue
        if "relation" in query and relation(fact.get("relation", ""), targets) != relation(query["relation"], targets):
            continue
        if "layer" in query and fact.get("layer", "OUTER") != query["layer"]:
            continue
        if "epistemic_status" in query and fact.get("epistemic_status") != query["epistemic_status"]:
            continue
        q = query.get("qualifier") or {}
        if any(surface((fact.get("qualifier") or {}).get(k, ""), state, aliases) != surface(v, state, aliases)
               for k, v in q.items()):
            continue
        candidates.append(fact)
    return candidates if len(candidates) == 1 else []


def score_update(targets, case_id, horizon, before_state, raw_delta, after_state, history):
    """Return bounded per-target metrics; callers must keep targets out of execution."""
    if any(s["ordinal"] > horizon for s in history):
        raise ValueError("Future source segment in evaluator history")
    sample = next(s for s in targets["samples"] if s["case_id"] == case_id and s["horizon"] == horizon)
    current = next(s for s in history if s["ordinal"] == horizon)
    if sha(packed(current).encode()) != sample["current_segment_sha256"]:
        raise ValueError("Current source segment checksum mismatch")
    aliases = alias_lookup(targets, sample)
    raw_records, raw_shape_diagnostics = inspect_raw(raw_delta, history)
    raw_state = copy.deepcopy(before_state)
    for kind, key in [("entities", "entity_id"), ("facts", "fact_id")]:
        raw_state.setdefault(kind, {})
        for record in raw_records[kind]:
            if isinstance(record, dict) and record.get(key):
                raw_state[kind][record[key]] = record
    views = {
        "raw": (raw_state, raw_records),
        "admitted": (after_state, {kind: fresh_records(before_state, after_state, kind, key)
                                  for kind, key in [("transitions", "transition_id"),
                                                    ("identity_merges", "merge_id")]}),
    }
    views["admitted"][1]["facts"] = admitted_current_facts(before_state, after_state, horizon)
    old_fact_ids = {f["fact_id"] for f in values(before_state, "facts")}
    result = {"evaluation_version": VERSION, "case_id": case_id, "horizon": horizon,
              "fact_reference_required": len(sample["fact_targets"]),
              "correction_required": len(sample["transition_targets"]),
              "identity_required": len(sample["identity_targets"]),
              "unresolved_pair_checks": len(sample["unresolved_identity_pairs"]),
              "role_same_person_pair_checks": len(sample["role_same_person_pairs"]),
              "raw_envelope_invalid": raw_shape_diagnostics["invalid_envelope"],
              "raw_record_collections_invalid": len(raw_shape_diagnostics["invalid_kind_collections"]),
              "raw_record_shapes_invalid": sum(raw_shape_diagnostics["invalid_record_shapes"].values()),
              "raw_evidence_view": "source_normalized_read_only",
              **{"raw_" + key: value for key, value in raw_shape_diagnostics.items()
                 if key.startswith("source_")},
              "admitted_reused_current_evidence_facts": sum(f["fact_id"] in old_fact_ids
                                                           for f in views["admitted"][1]["facts"]),
              "raw_shape_diagnostics": raw_shape_diagnostics, "views": {}}
    for view_name, (state, delta) in views.items():
        fact_results = []
        for gold in sample["fact_targets"]:
            matching = [f for f in delta.get("facts", []) if signature(f, state, aliases, targets) ==
                        signature(gold, {}, aliases, targets) and anchored(f, history, horizon)]
            fact_results.append({"target_id": gold["fact_id"], "matched": bool(matching)})
        corrections = []
        for target in sample["transition_targets"]:
            gold = target["claim"]
            predecessors = [f for f in values(before_state, "facts")
                            if claim_reference_match(f, gold, before_state, aliases, history)]
            correct = []
            for transition in delta.get("transitions", []):
                candidates = transition_candidates(transition, state, targets, aliases)
                if (len(candidates) == 1 and transition.get("to_status") == target["to_status"] and
                        anchored(transition, history, horizon, target["current_evidence"]) and
                        claim_reference_match(candidates[0], gold, state, aliases, history) and
                        any(candidates[0].get("fact_id") == p.get("fact_id") for p in predecessors)):
                    correct.append(transition)
            corrections.append({"claim_target_id": target["claim_fact_id"],
                                "precursor_source_attribution_available": bool(predecessors),
                                "correct_source_claim_link": bool(correct)})
        identity_results = []
        for target in sample["identity_targets"]:
            pair = {norm(target["left"]), norm(target["right"])}
            correct = any({surface(m.get("left", ""), state, {}), surface(m.get("right", ""), state, {})} == pair
                          and m.get("relation") == target["relation"] and anchored(m, history, horizon)
                          for m in delta.get("identity_merges", []))
            identity_results.append({"relation": target["relation"], "explicit_current_link": correct,
                                     "canonical_reuse_semantics": "UNASSESSED"})
        unresolved, contradictory_role = 0, 0
        for m in delta.get("identity_merges", []):
            if m.get("relation") not in ["SAME_AS", "DISTINCT"]:
                continue
            pair = {surface(m.get("left", ""), state, {}), surface(m.get("right", ""), state, {})}
            if not anchored(m, history, horizon):
                continue
            for target in sample["unresolved_identity_pairs"]:
                if pair == {norm(target["left"]), norm(target["right"])}:
                    unresolved += 1
            if m.get("relation") == "DISTINCT":
                for target in sample["role_same_person_pairs"]:
                    if pair == {norm(target["left"]), norm(target["right"])}:
                        contradictory_role += 1
        result["views"][view_name] = {
            "fact_reference_matched": sum(f["matched"] for f in fact_results),
            "fact_reference_findings": fact_results,
            "precursor_source_attribution_available": sum(c["precursor_source_attribution_available"] for c in corrections),
            "correct_source_claim_links": sum(c["correct_source_claim_link"] for c in corrections),
            "correction_findings": corrections,
            "explicit_identity_links": sum(i["explicit_current_link"] for i in identity_results),
            "identity_findings": identity_results,
            "unresolved_asserted_identity_candidates": unresolved,
            "contradictory_role_distinct_candidates": contradictory_role,
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.corpus, args.output_dir), sort_keys=True))


if __name__ == "__main__":
    main()
