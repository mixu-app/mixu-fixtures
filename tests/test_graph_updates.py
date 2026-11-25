# SPDX-License-Identifier: Apache-2.0
"""Negative controls for the bounded update-link evaluator."""

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("graph_update_eval", ROOT / "tools/graph_update_eval.py")
EVAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVAL)


def span(segment, start=0, end=None):
    end = len(segment["text"]) if end is None else end
    return {"ordinal": segment["ordinal"], "segment_id": segment["segment_id"],
            "start": start, "end": end, "quote": segment["text"][start:end]}


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.history = [
            {"ordinal": 1, "segment_id": "s1", "text": "Owen said the door was locked."},
            {"ordinal": 2, "segment_id": "s2", "text": "Bea said the lamp was lit."},
            {"ordinal": 3, "segment_id": "s3", "text": "Owen withdraws his door claim. Unrelated chairs arrived."},
        ]
        self.claim = {"fact_id": "door", "subject": "door", "relation": "locked_at",
                      "object": "noon", "epistemic_status": "CLAIMED", "layer": "OUTER",
                      "qualifier": {"speaker": "Owen", "polarity": "POSITIVE"},
                      "provenance": [span(self.history[0])]}
        other = {**self.claim, "fact_id": "lamp", "subject": "lamp", "relation": "lit_at",
                 "qualifier": {"speaker": "Bea"}, "provenance": [span(self.history[1])]}
        self.before = {"entities": {}, "facts": {"door": self.claim, "lamp": other},
                       "transitions": {}, "identity_merges": {}}
        self.transition = {"transition_id": "withdraw", "fact_id": "door", "to_status": "RETRACTED",
                           "provenance": [span(self.history[2], 0, 29)]}
        self.sample = {"case_id": "test", "horizon": 3,
                       "current_segment_sha256": EVAL.sha(EVAL.packed(self.history[-1]).encode()),
                       "fact_targets": [], "identity_targets": [], "unresolved_identity_pairs": [],
                       "role_same_person_pairs": [], "source_role_aliases": {},
                       "transition_targets": [{"claim_fact_id": "gold_door", "claim": self.claim,
                                                "to_status": "RETRACTED",
                                                "current_evidence": [span(self.history[2], 0, 29)]}]}
        self.targets = {"samples": [self.sample], "relation_aliases": {}}

    def score(self, transition=None, before=None):
        before = copy.deepcopy(self.before if before is None else before)
        delta = {"facts": [], "entities": [], "transitions": [self.transition if transition is None else transition],
                 "identity_merges": []}
        after = copy.deepcopy(before)
        after["transitions"] = {delta["transitions"][0]["transition_id"]: delta["transitions"][0]}
        return EVAL.score_update(self.targets, "test", 3, before, delta, after, self.history)

    def test_correct_link_retains_historical_claim_and_separates_views(self):
        original = copy.deepcopy(self.before)
        result = self.score()
        for view in ["raw", "admitted"]:
            self.assertEqual(result["views"][view]["correct_source_claim_links"], 1)
        self.assertEqual(self.before, original)

    def test_wrong_old_claim_not_credited_with_valid_current_evidence(self):
        result = self.score({**self.transition, "fact_id": "lamp"})
        self.assertEqual(result["views"]["admitted"]["correct_source_claim_links"], 0)

    def test_wrong_speaker_and_wrong_status_do_not_match_precursor(self):
        for changed in ["speaker", "status"]:
            before = copy.deepcopy(self.before)
            if changed == "speaker":
                before["facts"]["door"]["qualifier"]["speaker"] = "Bea"
            else:
                before["facts"]["door"]["epistemic_status"] = "OBSERVED"
            self.assertEqual(self.score(before=before)["views"]["raw"]["precursor_source_attribution_available"], 0)

    def test_unrelated_current_anchor_and_nonverbatim_quote_rejected(self):
        for p in [span(self.history[2], 30), {**span(self.history[2], 0, 29), "quote": "invented"}]:
            result = self.score({**self.transition, "provenance": [p]})
            self.assertEqual(result["views"]["raw"]["correct_source_claim_links"], 0)

    def test_missing_precursor_keeps_unconditional_denominator(self):
        before = {**self.before, "facts": {"lamp": self.before["facts"]["lamp"]}}
        result = self.score(before=before)
        self.assertEqual(result["correction_required"], 1)
        self.assertEqual(result["views"]["raw"]["precursor_source_attribution_available"], 0)
        self.assertEqual(result["views"]["raw"]["correct_source_claim_links"], 0)

    def test_semantic_target_lookup_must_be_unique(self):
        query = {"subject": "door", "relation": "locked_at", "object": "noon", "layer": "OUTER",
                 "qualifier": {"speaker": "Owen"}}
        transition = {k: v for k, v in self.transition.items() if k != "fact_id"}
        transition["target"] = query
        self.assertEqual(self.score(transition)["views"]["raw"]["correct_source_claim_links"], 1)
        before = copy.deepcopy(self.before)
        before["facts"]["duplicate"] = {**self.claim, "fact_id": "duplicate"}
        self.assertEqual(self.score(transition, before)["views"]["raw"]["correct_source_claim_links"], 0)

    def test_future_history_and_changed_current_source_fail_closed(self):
        with self.assertRaises(ValueError):
            EVAL.score_update(self.targets, "test", 3, self.before, {}, self.before,
                              self.history + [{"ordinal": 4, "segment_id": "future", "text": "future"}])
        changed = copy.deepcopy(self.history)
        changed[-1]["text"] += "changed"
        with self.assertRaises(ValueError):
            EVAL.score_update(self.targets, "test", 3, self.before, {}, self.before, changed)

    def test_unresolved_is_not_distinct_and_role_alias_reuse_unassessed(self):
        self.sample["transition_targets"] = []
        self.sample["unresolved_identity_pairs"] = [{"left": "visitor", "right": "Mori"}]
        self.sample["identity_targets"] = [{"left": "visitor", "right": "Mori", "relation": "SAME_AS"}]
        before = {**self.before, "entities": {"v": {"name": "visitor"}, "m": {"name": "Mori"}}}
        merged = {"merge_id": "m1", "left": "v", "right": "m", "relation": "DISTINCT",
                  "provenance": [span(self.history[-1])]}
        after = {**before, "identity_merges": {"m1": merged}}
        result = EVAL.score_update(self.targets, "test", 3, before, {"identity_merges": [merged]}, after, self.history)
        self.assertEqual(result["views"]["raw"]["unresolved_asserted_identity_candidates"], 1)
        self.assertEqual(result["views"]["raw"]["explicit_identity_links"], 0)
        reuse = EVAL.score_update(self.targets, "test", 3, before, {}, before, self.history)
        self.assertEqual(reuse["views"]["raw"]["identity_findings"][0]["canonical_reuse_semantics"], "UNASSESSED")

    def test_frozen_selection_and_target_checksums_agree(self):
        root = ROOT / "fixtures/benchmarks/graph-updates"
        selection_bytes = (root / "selection.json").read_bytes()
        targets = json.loads((root / "targets.json").read_text())
        selection = json.loads(selection_bytes)
        self.assertEqual(len(selection["samples"]), 20)
        self.assertEqual(EVAL.sha(selection_bytes), targets["selection_sha256"])
        self.assertEqual(selection["samples"], [{"case_id": s["case_id"], "horizon": s["horizon"]}
                                               for s in targets["samples"]])

    def test_invalid_json_envelopes_keep_target_denominators(self):
        for raw in [None, [], ["not", "an", "object"], "text", 12,
                    {"entities": [], "facts": None, "transitions": [], "identity_merges": []},
                    {"entities": [], "facts": "bad", "transitions": [], "identity_merges": []}]:
            result = EVAL.score_update(self.targets, "test", 3, self.before, raw, self.before, self.history)
            self.assertEqual(result["raw_shape_diagnostics"]["invalid_envelope"], 1)
            self.assertEqual(result["raw_envelope_invalid"], 1)
            self.assertEqual(result["correction_required"], 1)
            self.assertEqual(result["views"]["raw"]["correct_source_claim_links"], 0)

    def test_malformed_records_are_counted_without_repair_or_crash(self):
        valid = copy.deepcopy(self.claim)
        broken_facts = [None, "fact", {**valid, "qualifier": []}, {**valid, "qualifier": None},
                        {**valid, "provenance": "proof"}, {**valid, "provenance": [None]},
                        {**valid, "provenance": [{"ordinal": [], "segment_id": "s3", "start": 0, "end": 1}]},
                        {**valid, "subject": []}]
        raw = {"entities": [None], "facts": broken_facts,
               "transitions": [None, {**self.transition, "fact_id": []},
                               {**self.transition, "provenance": None}], "identity_merges": [None]}
        original = copy.deepcopy(raw)
        result = EVAL.score_update(self.targets, "test", 3, self.before, raw, self.before, self.history)
        self.assertEqual(raw, original)
        self.assertEqual(result["raw_shape_diagnostics"]["invalid_record_shapes"],
                         {"entities": 1, "facts": len(broken_facts), "transitions": 3, "identity_merges": 1})
        self.assertEqual(result["raw_record_shapes_invalid"], len(broken_facts) + 5)
        self.assertEqual(result["views"]["raw"]["correct_source_claim_links"], 0)

    def test_admitted_reused_fact_with_new_proof_is_counted(self):
        history = [{"ordinal": 1, "segment_id": "s1", "text": "The lamp is lit at noon."},
                   {"ordinal": 3, "segment_id": "s3", "text": "The lamp remains lit at noon."}]
        fact = {"fact_id": "lamp", "subject": "lamp", "relation": "lit_at", "object": "noon",
                "epistemic_status": "OBSERVED", "layer": "OUTER", "qualifier": {},
                "provenance": [span(history[0])]}
        before = {"entities": {}, "facts": {"lamp": fact}, "transitions": {}, "identity_merges": {}}
        sample = {**self.sample, "transition_targets": [], "fact_targets": [fact],
                  "current_segment_sha256": EVAL.sha(EVAL.packed(history[-1]).encode())}
        targets = {**self.targets, "samples": [sample]}
        for use_event in [False, True]:
            after = copy.deepcopy(before)
            if use_event:
                after["_fact_events"] = {"dedup-event": {**fact, "provenance": [span(history[-1])]}}
            else:
                after["facts"]["lamp"]["provenance"].append(span(history[-1]))
            original = copy.deepcopy(after)
            result = EVAL.score_update(targets, "test", 3, before, {}, after, history)
            self.assertEqual(result["views"]["admitted"]["fact_reference_matched"], 1)
            self.assertEqual(result["admitted_reused_current_evidence_facts"], 1)
            self.assertEqual(after, original)
        unchanged = EVAL.score_update(targets, "test", 3, before, {}, before, history)
        self.assertEqual(unchanged["views"]["admitted"]["fact_reference_matched"], 0)
        self.assertEqual(unchanged["admitted_reused_current_evidence_facts"], 0)

    def test_unique_exact_quote_with_optional_or_wrong_coordinates_is_normalized_read_only(self):
        quote = self.history[-1]["text"][:29]
        for p in [{"segment_id": "s3", "quote": quote},
                  {"segment_id": "s3", "quote": quote, "ordinal": 99, "start": [], "end": None}]:
            transition = {**self.transition, "provenance": [p]}
            original = copy.deepcopy(transition)
            result = self.score(transition)
            self.assertEqual(result["raw_record_shapes_invalid"], 0)
            self.assertEqual(result["raw_source_normalized_records"], 1)
            self.assertEqual(result["raw_source_normalized_spans"], 1)
            self.assertEqual(result["raw_evidence_view"], "source_normalized_read_only")
            self.assertEqual(result["views"]["raw"]["correct_source_claim_links"], 1)
            self.assertEqual(transition, original)

    def test_ambiguous_quote_unscorable_but_valid_explicit_offsets_disambiguate(self):
        history = copy.deepcopy(self.history)
        quote = "Owen withdraws."
        history[-1]["text"] = quote + " " + quote
        self.sample["current_segment_sha256"] = EVAL.sha(EVAL.packed(history[-1]).encode())
        self.sample["transition_targets"][0]["current_evidence"] = [span(history[-1], 0, len(quote))]
        for explicit in [False, True]:
            p = {"segment_id": "s3", "quote": quote}
            if explicit:
                p.update(ordinal=3, start=0, end=len(quote))
            raw = {"entities": [], "facts": [], "transitions": [{**self.transition, "provenance": [p]}],
                   "identity_merges": []}
            result = EVAL.score_update(self.targets, "test", 3, self.before, raw, self.before, history)
            self.assertEqual(result["raw_source_unscorable_records"], int(not explicit))
            self.assertEqual(result["raw_source_ambiguous_spans"], int(not explicit))
            self.assertEqual(result["views"]["raw"]["correct_source_claim_links"], int(explicit))

    def test_unknown_source_and_nonverbatim_quote_not_resolved_with_gold(self):
        for p, category in [({"segment_id": "s4", "quote": "Owen withdraws"}, "unknown"),
                            ({"segment_id": "s3", "quote": "Changed testimony"}, "nonverbatim")]:
            result = self.score({**self.transition, "provenance": [p]})
            self.assertEqual(result["raw_record_shapes_invalid"], 0)
            self.assertEqual(result["raw_source_unscorable_records"], 1)
            self.assertEqual(result["raw_source_" + category + "_spans"], 1)
            self.assertEqual(result["views"]["raw"]["correct_source_claim_links"], 0)

    def test_source_claim_link_is_not_a_full_semantic_proposition_judge(self):
        before = copy.deepcopy(self.before)
        # Same speaker and exact source anchor do not prove its payload entails
        # that source. This intentionally documents the proxy's known boundary.
        before["facts"]["door"]["subject"] = "unrelated subject"
        self.assertEqual(self.score(before=before)["views"]["raw"]["correct_source_claim_links"], 1)


if __name__ == "__main__":
    unittest.main()
