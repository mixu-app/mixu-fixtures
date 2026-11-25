# Fresh sequential source-lookup fixtures

This is a local experimental draft corpus, not a novel benchmark or a paper
artifact. The seven reused synthetic cases remain development diagnostics.
`new-input.json` is a newly authored, original Chinese diagnostic: 12 segments,
816 characters, with an explicit unique role, two separately attributed witness
claims, later withdrawal/corroboration and a delayed identity confirmation.
The narrative, reference annotations and derived corpus are CC0-1.0. No
published text, reader notes, account data or private extraction prompt is used.

## Export and separation

```sh
just sequential-source-export "$OLD_CORPUS" "$OLD_TARGETS" "$OUTPUT_DIR"
```

`generation.json` contains only input references, hashes, language, segment
counts and rights metadata: eight cases / 114 segments. It has no gold paths,
target IDs, scenario labels or answer hints. `pilot-generation.json` separately
contains the excluded original `gm-zh-01` source. Old input and gold bytes are
copied unchanged. The runner chooses its explicit pilot segment limit.

`evaluation.json`, `targets.json` and `gold/` are offline-only. There are 29
target horizons: the 20 frozen prior selections plus nine source-defined new
horizons. The existing source-normalized scorer is pinned by SHA-256; its
source-attributed claim links are structural proxies, not full proposition
entailment. Composite event decompositions and canonical identity reuse still
need separate inspection. Earlier observational evidence may justify other
supported claim updates; reference annotations are not exhaustive.

Reveal ordinal follows presentation order, including the flashbacks in new
segments 5 and 7. The named visitor is explicitly identified only at segment 8.
The segment-10 withdrawal refers to the segment-4 witness claim; segment 11
corroborates the other witness's segment-6 claim. Historical CLAIMED records
remain legitimate historical records after later status transitions.

## Historical claim-source coverage

`source_coverage(targets, case_id, horizon, selected_sources, history)` is an
offline evaluator. It never selects retrieval input or repairs a graph. It
checks that retrieved text is an exact, unambiguous source substring before
the current horizon, or has a valid explicit start offset. A claim is fully
covered only when every annotated introduction-source span is enclosed by the
selected text. Selecting another passage with the same ordinal is insufficient.
Invalid fragments are counted, not silently treated as hits.

The returned integer counters are `historical_claim_targets`,
`historical_claim_source_spans_required`,
`historical_claim_source_spans_covered`, `historical_claims_fully_covered`,
`selected_source_fragments` and `invalid_retrieved_fragments`. Per-claim findings
retain the denominators. Entity/role evidence coverage is **UNASSESSED**.
Finding the right source span does not prove the model interpreted it correctly.

Fresh trajectory prefixes may diverge across arms. Required target counts stay
source-defined, while generated precursor availability is arm-specific and
must not be forced equal. No gold predecessor is inserted into generation.

`just check` includes negative controls for rights, source hashes, horizon
violations, malformed reveal ordinals, wrong/current/future retrieval, partial
quote coverage, ambiguity and the generation/offline boundary.
