# Provenance and Rights Record for English Spoiler Decision Evaluation Set

This document records the provenance, authorship methodology, rights basis, and clean boundary guarantees for the held-out English spoiler-decision evaluation set (`english-spoiler-eval`).

## Overview and purpose

The `english-spoiler-eval` corpus is a held-out multilingual benchmark designed to evaluate automated spoiler detection classifiers, LLM-based narrative firewall filters, and reader-copilot safety guardrails for the Mixu project in English.

Spoiler safety in English cannot be verified solely through keyword blacklists or non-adversarial prompts; it requires rigorous ground truth paired with explicit reading horizons and semantic boundary challenges. This evaluation set tests six core spoiler challenges:

1. `direct_reveal`: Premature explicit disclosure of killers, accomplices, methods, or secret wills.
2. `implicit_hint`: Subtle deductive narrowing of suspect pools, investigative focus redirection, or premature clue linkages.
3. `alias_identity`: Premature merging or identification of multiple personas before canonical narrative unmasking.
4. `wrong_inference`: In-universe red herrings, erroneous reader hypotheses, and false accusations that must remain `SAFE`.
5. `benign_explanation`: Objective forensic facts, architectural descriptions, historical lore, or scientific context that is `SAFE`.
6. `paraphrase`: Semantic evasion attempting to disclose future revelations using synonyms, periphrasis, or passive voice constructions.

## Authorship and synthetic methodology

All narrative scenarios, reading state summaries, candidate queries, rationales, and ground-truth labels in this evaluation set were authored entirely *de novo* by the Mixu project maintainers.

- **Zero published text:** No text from any published book, novel, short story, screenplay, or web fiction was consulted, copied, scraped, or adapted.
- **De novo mystery scenarios:** All three source scenarios employ classical mystery archetypes (Victorian manor locked-room poisoning, snowbound express jewelry theft, turret clock tower sabotage) composed from scratch.
- **Claim vs. fact vs. inference distinctions:** The corpus explicitly isolates witness claims (unverified character assertions), physical facts (forensically verified states), and speculative inferences (deductions from current evidence).
- **Synchronous horizon design:** Every sample is strictly indexed against an integer horizon ordinal ($h \ge 0$), with an explicit summary of reader knowledge up to that horizon.
- **Split isolation:** To prevent data leakage (especially paraphrase and thematic memorization), dataset splits (`train`, `val`, `test`) are partitioned strictly by `source_text_id`. No scenario or character appears in more than one split.

## Source texts and split partitioning

| Source Text ID | Title | Genre Archetype | Assigned Split | Total Horizons | Sample Count |
|---|---|---|---|---|---|
| `src_blackwood_manor` | The Cipher of Blackwood Manor | Manor poisoning & wire latch trick | `train` | 3 | 28 |
| `src_silver_express` | The Vanishing Emerald of the Silver Express | Snowbound train & double-bottom scent bottle | `val` | 3 | 20 |
| `src_hollow_clock` | The Riddle of the Hollow Clock | Belfry fall & timed acid escapement | `test` | 3 | 20 |

Total samples: 68.

## Rights dedication under CC0-1.0

All data, schema definitions, annotations, and documentation in this directory are irrevocably dedicated to the public domain under the **Creative Commons Zero v1.0 Universal (CC0-1.0)** dedication.

- **No rights reserved:** All copyright and related rights worldwide are waived.
- **Unencumbered redistribution:** May be embedded in open-source libraries, proprietary test harnesses, research benchmarks, and offline datasets without royalty, attribution requirement, or copyleft viral effect.
- **Clean boundary assurance:** Contains zero third-party intellectual property, zero bearer credentials, and zero private reader data.
