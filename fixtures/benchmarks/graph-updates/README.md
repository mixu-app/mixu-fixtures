# Source-defined graph update probes

This is an original-synthetic, CC0-1.0 evaluation derivative of the frozen
IGM-2 corpus. It contains no published book text or private extraction prompts.
`selection.json` is the only file visible to the replay planner. `targets.json`
is an **offline evaluation input** and must never enter generation, predecessor
construction, retrieval or repair. Both are generated with:

```sh
just graph-updates-export "$CORPUS_EXPORT" fixtures/benchmarks/graph-updates
```

The source export and its per-file hashes are recorded in `targets.json`.
The selection is fixed from source/gold alone, before inspecting old next-step
outputs or scores: 20 case/horizon pairs covering claim introduction, explicit
withdrawal/corroboration, delayed identity and role-reference updates. The
planner pairs exactly the same existing model-generated predecessor with each
encoding treatment. This is a one-step replay study, not a complete sequential
rollout or a claim about novels. Existing predecessors can contain errors.

## Frozen measurements

- Fact reference matching is a representation-sensitive signature proxy over
  subject/relation/object/layer/status/speaker/polarity and valid current-source
  evidence. A small source-defined relation/unique-role alias map is frozen
  before calls. Composite object decompositions remain unassessed by this proxy.
- Correction linkage measures a typed transition to an **existing generated
  predecessor claim**, with matching historical claim-source overlap, speaker,
  polarity and layer, correct later status, and current reference-evidence overlap.
  This is a source-attributed claim-link proxy, not full semantic entailment.
  An anchor can overlap a source without expressing its meaning correctly.
- Missing precursor attribution is an explicit eligibility field. Every selected
  correction remains in the unconditional denominator; conditional eligible
  results must be labelled separately. No gold precursor is inserted.
- Identity linkage measures the exact explicit source-confirmed pair/relation
  with current evidence. Canonical entity reuse can retain the same meaning
  without a new identity edge: its semantics are **UNASSESSED**, not deemed wrong.
- At unresolved horizons, an asserted `SAME_AS` or `DISTINCT` edge for the
  designated pair is a candidate for review. Separate records, different names
  and lack of confirmation do not establish `DISTINCT`.
- `DISTINCT` between a name and its explicitly assigned unique role is another
  source-defined candidate. This is bounded pair detection, not exhaustive
  identity accuracy or a guarantee against other semantic errors.

Raw response and admitted-delta measurements are separate. The evaluator does
not change either graph. No source/gold-dependent rule belongs in the admission
validator. Mechanical invariants such as known references, valid spans,
non-self `DISTINCT`, status types and append-only history can be checked without
gold; meaning, attribution and role resolution generally need additional review.

Malformed raw envelopes and per-kind collections are counted explicitly, as are
malformed record shapes. Failed output retains all target denominators. A raw
object with an invalid envelope can still have its individually well-shaped
record fragments inspected; this is partial raw inspection, not a repaired
response or successful admission. Shape checks are evaluator-safety checks,
not a replacement for the reducer's full schema/type/source validation. No
missing semantic field or evidence is fabricated for raw inspection.

The `raw` metric view is **source-normalized, read-only**: the generation
contract requires an exact quote and source segment but makes ordinal/start/end
optional. On a copy, the evaluator accepts valid exact given offsets, or resolves
the quote only when it occurs uniquely in that supplied source segment. It also
derives the source ordinal, matching the frozen reducer's source-only proof
semantics. The original raw object/bytes never change. This uses no reference
gold; ambiguous, nonverbatim and unknown/future-source proofs are explicitly
unscorable rather than anchored from answers. Normalized record/span counts and
unscorable record/reason counts are reported. A software-normalized source span
still does not establish that a payload expresses the source's meaning. In
particular, the correction source-attribution proxy does not adjudicate every
subject/relation/object argument of that earlier generated claim.

Admitted fact measurements include new fact IDs **and reused canonical facts
that gain current evidence**, whether the reducer stores that evidence directly
or in its `_fact_events` ledger. Projection uses the admitted canonical payload
and accumulated proofs without changing stored state. Old retained facts with
no newly admitted current evidence do not count as a new extraction success.

The evaluator does not compute semantic F1, precision, zero-spoiler guarantees
or human-adjudicated accuracy. The aliases and rules must not be expanded after
seeing results without a separately labelled exploratory amendment.
