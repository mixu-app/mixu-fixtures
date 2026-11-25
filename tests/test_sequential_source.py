# SPDX-License-Identifier: Apache-2.0
"""Negative controls for source separation, reveal bounds and quote-span coverage."""

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("source_fixtures", ROOT / "tools/sequential_source_fixtures.py")
FIX = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIX)


class SequentialSourceTest(unittest.TestCase):
    def setUp(self):
        self.source = FIX.load(FIX.DATA / "new-input.json")
        self.gold = FIX.load(FIX.DATA / "new-gold.json")
        self.targets = {"samples": FIX.new_samples(self.source, self.gold)}
        self.history = self.source["segments"][:10]

    def coverage(self, fragments, *, targets=None, history=None):
        return FIX.source_coverage(targets or self.targets, "ss-zh-01", 10, fragments,
                                   self.history if history is None else history)

    def test_new_source_has_exact_rights_spans_and_reveal_boundaries(self):
        FIX.validate_source(self.source, self.gold, require_literal_entity_surfaces=True)
        self.assertEqual(len(self.source["segments"]), 12)
        self.assertEqual(len(self.gold["facts"]), 14)
        samples = self.targets["samples"]
        self.assertNotIn("桑禾", samples[0]["source_role_aliases"])
        self.assertEqual(next(s for s in samples if s["horizon"] == 8)["identity_targets"][0]["relation"], "SAME_AS")
        self.assertEqual(next(s for s in samples if s["horizon"] == 10)["transition_targets"][0]["claim_fact_id"], "f4")
        self.assertEqual(next(s for s in samples if s["horizon"] == 11)["transition_targets"][0]["claim_fact_id"], "f6")

    def test_negative_reveal_control_rejects_already_revealed_forbidden_fact(self):
        altered = copy.deepcopy(self.gold)
        altered["horizons"][0]["forbidden_fact_ids"].append("f1")
        with self.assertRaisesRegex(ValueError, "reveal horizon"):
            FIX.validate_source(self.source, altered)

    def test_nonverbatim_and_future_proofs_fail(self):
        for mutate in (lambda g: g["facts"][0]["provenance"][0].update(quote="invented"),
                       lambda g: g["facts"][0].update(valid_from_ordinal=0),
                       lambda g: g["facts"][0]["provenance"][0].update(ordinal=True)):
            altered = copy.deepcopy(self.gold)
            mutate(altered)
            with self.assertRaises(ValueError):
                FIX.validate_source(self.source, altered)

    def test_identity_and_correction_reveal_bounds_fail_closed(self):
        for mutate in (lambda g: g["identity_constraints"][0].update(valid_from_ordinal=99),
                       lambda g: g["identity_constraints"][0].update(valid_from_ordinal=7),
                       lambda g: g["transitions"][0].update(ordinal=4),
                       lambda g: g["transitions"][0].update(evidence_fact_ids=["missing"]),
                       lambda g: g["horizons"].append(g["horizons"][0])):
            altered = copy.deepcopy(self.gold)
            mutate(altered)
            with self.assertRaises(ValueError):
                FIX.validate_source(self.source, altered)

    def test_rights_and_inference_metadata_do_not_pass_source_boundary(self):
        altered = copy.deepcopy(self.gold)
        altered["content_basis"] = "UNKNOWN"
        with self.assertRaisesRegex(ValueError, "rights"):
            FIX.validate_source(self.source, altered)
        altered_source = copy.deepcopy(self.source)
        altered_source["expected_answer"] = "hidden gold"
        with self.assertRaisesRegex(ValueError, "generation input envelope"):
            FIX.validate_source(altered_source, self.gold)

    def test_whole_claim_source_covers_only_introduction_spans(self):
        result = self.coverage([self.history[3]])
        self.assertEqual(result["historical_claim_targets"], 1)
        self.assertEqual(result["historical_claim_source_spans_required"], 1)
        self.assertEqual(result["historical_claim_source_spans_covered"], 1)
        self.assertEqual(result["historical_claims_fully_covered"], 1)
        self.assertEqual(result["invalid_retrieved_fragments"], 0)
        self.assertEqual(result["identity_source_coverage"], "UNASSESSED")

    def test_right_ordinal_with_wrong_or_partial_quote_is_not_a_hit(self):
        source = self.history[3]
        target = next(s for s in self.targets["samples"] if s["horizon"] == 10)
        span = target["transition_targets"][0]["claim"]["provenance"][-1]
        for text in (source["text"][:10], span["quote"][:-1]):
            fragment = {"ordinal": 4, "segment_id": source["segment_id"], "text": text}
            result = self.coverage([fragment])
            self.assertEqual(result["invalid_retrieved_fragments"], 0)
            self.assertEqual(result["historical_claim_source_spans_covered"], 0)

    def test_every_required_claim_span_must_be_enclosed(self):
        source = self.history[3]
        altered = copy.deepcopy(self.targets)
        target = next(s for s in altered["samples"] if s["horizon"] == 10)
        claim = target["transition_targets"][0]["claim"]
        quote = claim["provenance"][-1]
        second = {**quote, "start": 0, "end": 4, "quote": source["text"][:4]}
        claim["provenance"] = [quote, second]
        fragment = {"ordinal": 4, "segment_id": source["segment_id"], "text": quote["quote"]}
        result = self.coverage([fragment, fragment], targets=altered)
        self.assertEqual(result["historical_claim_source_spans_required"], 2)
        self.assertEqual(result["historical_claim_source_spans_covered"], 1)
        self.assertEqual(result["historical_claims_fully_covered"], 0)
        self.assertEqual(self.coverage([source], targets=altered)["historical_claims_fully_covered"], 1)

    def test_current_future_unknown_and_nonverbatim_retrieval_are_invalid(self):
        source = self.history[3]
        fragments = [self.history[-1], self.source["segments"][10],
                     {**source, "segment_id": "wrong"}, {**source, "text": "invented quote"}]
        result = self.coverage(fragments)
        self.assertEqual(result["invalid_retrieved_fragments"], len(fragments))
        self.assertEqual(result["historical_claim_source_spans_covered"], 0)
        with self.assertRaisesRegex(ValueError, "Future history"):
            self.coverage([], history=self.source["segments"])

    def test_ambiguous_fragment_needs_valid_explicit_start(self):
        history = [{"ordinal": 1, "segment_id": "s1", "text": "alpha alpha"},
                   {"ordinal": 2, "segment_id": "s2", "text": "withdrawal"}]
        targets = {"samples": [{"case_id": "toy", "horizon": 2, "transition_targets": [
            {"claim_fact_id": "c", "claim": {"valid_from_ordinal": 1, "provenance": [
                {"ordinal": 1, "start": 0, "end": 5, "quote": "alpha"}]}}]}]}
        fragment = {"ordinal": 1, "segment_id": "s1", "text": "alpha"}
        result = FIX.source_coverage(targets, "toy", 2, [fragment], history)
        self.assertEqual(result["invalid_retrieved_fragments"], 1)
        self.assertEqual(FIX.source_coverage(targets, "toy", 2, [{**fragment, "start": 6}], history)["historical_claims_fully_covered"], 0)
        self.assertEqual(FIX.source_coverage(targets, "toy", 2, [{**fragment, "start": 0}], history)["historical_claims_fully_covered"], 1)

    def test_unselected_horizon_has_no_fabricated_required_claim(self):
        result = FIX.source_coverage(self.targets, "ss-zh-01", 9, [], self.source["segments"][:9])
        self.assertEqual(result["historical_claim_targets"], 0)
        self.assertEqual(result["historical_claim_source_spans_required"], 0)

    def test_generation_export_has_no_gold_or_answer_fields_and_preserves_bytes(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            corpus, output = root / "corpus", root / "output"
            corpus.mkdir()
            rows, samples, originals = [], [], {}
            for index, case in enumerate([*FIX.OLD_CASES, FIX.PILOT_CASE]):
                inp = {"schema_version": 1, "case_id": case, "language": "en", "segments": [
                    {"ordinal": n, "segment_id": f"s{n}", "text": f"Original synthetic observation {n}."} for n in (1, 2, 3)]}
                gold = {"case_id": case, "content_basis": "SYNTHETIC_ORIGINAL", "license": "CC0-1.0",
                        "rights_note": "Original test content.", "entities": [], "facts": [],
                        "transitions": [], "identity_constraints": [], "horizons": [
                            {"ordinal": n, "required_fact_ids": [], "forbidden_fact_ids": []} for n in (1, 2, 3)]}
                raw = (json.dumps(inp, indent=2) + "\n").encode()
                gold_raw = (FIX.packed(gold) + "\n").encode()
                (corpus / f"{case}.json").write_bytes(raw)
                (corpus / f"{case}.gold.json").write_bytes(gold_raw)
                originals[case] = raw
                rows.append({"case_id": case, "input_path": f"{case}.json", "input_sha256": FIX.digest(raw),
                             "gold_path": f"{case}.gold.json", "gold_sha256": FIX.digest(gold_raw)})
                if case != FIX.PILOT_CASE:
                    for segment in inp["segments"][:2 if index == len(FIX.OLD_CASES) - 1 else 3]:
                        samples.append({"case_id": case, "horizon": segment["ordinal"],
                                        "current_segment_sha256": FIX.digest(segment)})
            (corpus / "manifest.json").write_text(FIX.packed({"cases": rows}))
            old_targets = root / "targets.json"
            old_targets.write_text(FIX.packed({"relation_aliases": {}, "samples": samples}))
            summary = FIX.export(corpus, old_targets, output)
            self.assertEqual(summary["main_cases"], 8)
            self.assertEqual(summary["target_horizons"], 29)
            for filename in ("generation.json", "pilot-generation.json"):
                manifest = FIX.load(output / filename)
                self.assertEqual(set(manifest), {"schema_version", "benchmark_id", "cases"})
                for row in manifest["cases"]:
                    self.assertEqual(set(row), FIX.GENERATION_FIELDS)
                    if row["case_id"] in originals:
                        self.assertEqual((output / row["input_path"]).read_bytes(), originals[row["case_id"]])
            with self.assertRaisesRegex(ValueError, "relative"):
                FIX.relative(output, str(output.resolve()))
            with self.assertRaisesRegex(ValueError, "escapes"):
                FIX.relative(output, "../escape.json")


if __name__ == "__main__":
    unittest.main()
