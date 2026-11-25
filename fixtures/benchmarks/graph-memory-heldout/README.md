# Held-out role-linked claim revision cohort

Status: authored before extraction-quality measurements; independent semantic
review pending. This is a separate extension to the initially frozen corpus.
It is not evidence that graph memory improves a model.

## Cases and mechanism

| Opaque ID | Language | Central mechanism |
| --- | --- | --- |
| hgm-zh-01 | zh-Hans | A uniquely assigned keeper and previously introduced key connect later role/pronoun references to a withdrawn storage claim |
| hgm-en-01 | en | An earlier named craft worker and marked case identify later anonymous actions, contradicting a caretaker's earlier storage claim |
| hgm-ja-01 | ja | A unique delivery role and distinctive package connect later references to an explicitly withdrawn witness account |

Each case has twelve ordered segments. Narration is natural story prose, with
no instruction to the extractor about inference or identity. Closing paragraphs
do not supply a repeated answer summary. Each story has one central role-linked
claim-revision mechanism, rather than collecting unrelated identity tricks.
The named role and marked object are introduced early; later role/pronoun
references omit the person's proper name. Central gold therefore includes both
earlier identifying passages and the later action, not only a current-segment
triple. A later camera observation is a distinct source-confirmation record, not a
second copy of the earlier observed action. A witness's explicit withdrawal has
earlier-claim and newer evidence
spans, plus a semantic transition target.

English contains 550 whitespace-delimited words. Chinese contains 887 non-space
code points and Japanese 1,081; whitespace word counts are not meaningful for
those scripts. These are short natural narratives in the intended 150–600-word
equivalent range, not representative novel passages or a controlled language
comparison.

## Separate export and freeze

Supply the output directory yourself:

```sh
just export-graph-memory-heldout "$GRAPH_MEMORY_HELDOUT_OUTPUT"
just validate-graph-memory-heldout
just check
```

The existing input/gold format is reused without changing its schemas. Inputs
contain only opaque case ID, language and ordered segment text. Gold and
manifests must never be supplied to generation, retrieval, ID assignment or
repair. Every boundary has complete required-reference and forbidden-future
lists. Span offsets remain exact raw Unicode code points, half-open, with no
normalization.

The three-case manifest has `cohort: heldout-v1` and a `source_sha256` computed
from the canonical JSON encoding of the ordered input/gold pairs. Each exported
file also has its own SHA-256. Exporting the initial source still produces its
unchanged frozen manifest; held-out export does not silently add stress cases.

## Preregistration and limits

The commander authorized this cohort before any extraction-quality results to
address the initial corpus's current-sentence extraction weakness. It adds
**3 cases × 12 segments × 4 models × 3 arms × 2 repeats = 864 planned calls**.
Execution is staged under the existing internal spend ceiling and is not
performed by this repository. The protocol owns model order, repetitions,
budgets and execution approval. No live API call is part of corpus validation.

Gold is target/reference-only, not exhaustive annotation of every incidental
object or sentence. Named-reference scores and exact typed signatures are
proxies; unmatched valid paraphrases are not confirmed hallucinations. Claim
status records refer to gold claim IDs for annotation linkage. Resolution scoring
must use the semantic transition target or evaluator-only ID alignment; it must
not demand model-generated claim IDs equal the gold IDs. This alignment never
feeds later generation.

All three cases share a mechanism, with one case per language. This supports a
small memory-dependent diagnostic, not broad scenario or language superiority,
real-novel transfer, or a zero-spoiler guarantee. The cohort is publicly visible
and therefore not a secret test set; “held-out” means separate from initial
capability and design probes, not guaranteed absent from training data.
