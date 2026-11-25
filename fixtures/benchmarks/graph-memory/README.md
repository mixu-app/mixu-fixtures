# Segmented graph-memory diagnostic benchmark

Status: local experimental corpus; no paid-model acceptance is implied.

This separate benchmark format does not change the existing normal-fixture
schema, story length rule or consumer pins. It contains six original CC0 stories,
each in six ordered segments; English, Simplified Chinese and Japanese have two
cases each. Provenance is in [PROVENANCE.md](PROVENANCE.md).

| Opaque input case | Language | Gold-only scenario |
| --- | --- | --- |
| gm-zh-01 | zh-Hans | Distant clue recurrence |
| gm-en-01 | en | Explicit witness retraction and corroboration |
| gm-ja-01 | ja | Delayed identity confirmation |
| gm-zh-02 | zh-Hans | Same surname, distinct people |
| gm-en-02 | en | Nested fictional loops isolated from outer reality |
| gm-ja-02 | ja | Quoted in-story prompt injection |

## Export contract

Run from this repository using a destination supplied by the caller:

```sh
just export-graph-memory "$GRAPH_MEMORY_OUTPUT" 24,48 2
just validate-graph-memory
just test-graph-memory
just check
```

The positional arguments are output directory, comma-separated stress lengths
and number of distractor relationships per filler segment. Default lengths are
24 and 48; any length of at least six is supported. There is no graph-node cap.
Use a fresh output directory: exports do not delete unrelated or stale files.
Consumers must follow `manifest.json`, rather than globbing an older export.

Each `manifest.cases[]` entry provides `case_id`, `language`, `segment_count`,
`input_path`, `input_sha256`, `gold_path`, `gold_sha256`, `base_case_id`,
`source_ordinals`, `distractors_per_filler_segment`,
`relevant_facts_per_filler_segment` and `target_clue_distance_segments`.
Hashes cover exact exported UTF-8 file bytes. The manifest is deterministic,
contains no timestamp or host path, and must not be sent to a model.

Only the selected `inputs/<case_id>.json` is model input. It contains
`schema_version`, opaque `case_id`, `language` and `segments`, whose fields are
`segment_id`, one-based `ordinal`, and `text`. At a prefix horizon the harness may
provide only segments at or before that horizon. Gold, manifests, fact IDs,
future text, target labels and precomputed identity registries must never enter
generation, retrieval queries, registry seeding or repair prompts.

Gold files remain under `gold/` and are opened only by the separate evaluator.
Gold contains facts, exact provenance, entity names/aliases/layers and mentions, identity constraints,
claim transitions and every segment boundary's required/forbidden fact IDs.
Offsets are **Unicode code points**, half-open `[start, end)`, in the exact raw
segment string after JSON decoding. No NFC, whitespace or newline normalization
is applied. Quotes must equal that exact slice; ordinals and segment IDs agree.

Facts describe explicit text only. `critical`, `cross_segment` and `distractor`
are evaluator-only labels. `cross_segment` marks membership in a cross-segment
test, including its initial evidence, rather than claiming every individual
sentence needs earlier context. `required_fact_ids` includes historical claims
as claims; retraction does not delete the fact that a witness made a statement.
The separate transition targets identify later epistemic changes. A future
`SAME_AS` identity constraint must not justify a merge at an earlier horizon;
`DISTINCT` requires the two entities to remain separate.

Claim qualifiers retain speaker, polarity and modality. Explicit transitions
include `claim_fact_id`, semantic `target`, `from_status`, `to_status`, reveal
ordinal and supporting fact IDs. No final answer is inferred from testimony or
from a quoted request to fabricate an answer.

## Stress semantics and limitations

Stress cases preserve all six original segments byte-for-byte, mapping their
ordinals across the requested length. Every additional segment adds one relevant
trace-chain relationship and the configured number of independent inventory
relationships. All added relationships have exact span gold. The trace chain
connects across filler segments, grows the scored relevant graph and is kept
separate from the original story's identity and epistemic claims. The clue span
and ordinal map are recorded explicitly. This is controlled synthetic growth,
not a realistic long novel or proof of useful retrieval.

Two repetitions per model/arm/length belong in the experiment harness; exporting
again must not randomize this corpus. Six scenarios and two cases per language
do not support causal comparisons between languages. Relation labels are a
small experiment vocabulary, not a change to the public graph contract.

## Scoring coverage

Base gold is a named-reference diagnostic set, not an exhaustive annotation of
all people, places, objects or incidental propositions in the prose. Named
identity and alias scores must use the declared reference universe. A valid
extra object or paraphrase is not automatically an unsupported assertion or
false-positive entity; semantic adjudication is separate from literal mismatch.
Stress gold includes every generated trace/brush/cabinet endpoint and its exact
mentions, including the initial T000 node. That completeness does not extend the
base corpus's annotation coverage.

Before any extraction scores, the commander selected **gm-en-01** for the main
24/48-segment stress comparison. The other ten exported stress variants are
available for separately declared follow-up, **NOT RUN** in the main matrix.

The commander briefly proposed gm-zh-01, then amended the choice to gm-en-01
before corpus freeze or extraction-quality calls. The claim-resolution case tests
alignment with prior claims directly. This pre-execution amendment changes no
trial count and is not based on extraction outcomes.
