# Provenance and Rights Record for Chinese Spoiler Decision Evaluation Set

This document records the provenance, authorship methodology, rights basis, and clean boundary guarantees for the held-out Chinese spoiler-decision evaluation set (`chinese-spoiler-eval`).

## Overview and purpose

The `chinese-spoiler-eval` corpus is a held-out benchmark designed to evaluate automated spoiler detection classifiers, LLM-based narrative firewall filters, and reader-copilot safety guardrails for the Mixu project.

Spoiler safety cannot be tested purely on ad-hoc queries or non-adversarial prompts; it requires precise ground truth paired with explicit reading horizons and semantic boundary challenges. This evaluation set tests six core spoiler challenges:

1. `direct_reveal`: Explicit premature disclosure of culprits, methods, or secret plots.
2. `implicit_hint`: Subtle narrowing of suspect spaces or premature clue correlations.
3. `alias_identity`: Premature merging of multiple personas before canonical unmasking.
4. `wrong_inference`: In-universe red herrings and incorrect reader deductions that must remain `SAFE`.
5. `benign_explanation`: Factual background lore, layout descriptions, or scientific context that is `SAFE`.
6. `paraphrase`: Semantic evasion attempting to disclose future secrets via metaphors, synonyms, or periphrasis.

## Authorship and synthetic methodology

All narrative scenarios, reading state summaries, candidate queries, rationales, and ground-truth labels in this evaluation set were authored entirely de novo by the Mixu project maintainers.

- **Zero published text:** No text from any published book, novel, short story, screenplay, fan fiction, or web fiction was consulted, copied, scraped, or adapted.
- **De novo mystery scenarios:** All five source scenarios employ classical mystery conventions (locked rooms, disguises, twin substitutions, mechanical alibis, alchemical stagecraft) composed from scratch.
- **Synchronous horizon design:** Every sample is strictly indexed against an integer horizon ordinal ($h \ge 0$), with an explicit summary of reader knowledge up to that horizon.
- **Split isolation:** To prevent data leakage (especially paraphrase and thematic memorization), dataset splits (`train`, `val`, `test`) are partitioned strictly by `source_text_id`. No scenario or character appears in more than one split.

## Source texts and split partitioning

| Source Text ID | Title | Genre Archetype | Assigned Split | Total Horizons | Sample Count |
|---|---|---|---|---|---|
| `src_manor_poison` | 海雾庄园晚宴案 | Manor poisoning & locked room | `train` | 4 | 55 |
| `src_gallery_theft` | 月影画廊失窃案 | Museum heist & disguise unmasking | `train` | 3 | 50 |
| `src_clocktower_fall` | 旧钟楼暗影坠亡案 | Clocktower fall & twin substitution | `train` | 3 | 45 |
| `src_midnight_train` | 午夜雪原快车案 | Snowbound train & mechanical lock | `val` | 3 | 35 |
| `src_alchemist_chamber` | 秘境炼金密室案 | Vanishing alchemist & secret flue | `test` | 3 | 35 |

Total samples: 220.

## Rights dedication under CC0-1.0

All data, schema definitions, annotations, and documentation in this directory are irrevocably dedicated to the public domain under the **Creative Commons Zero v1.0 Universal (CC0-1.0)** dedication.

- **No rights reserved:** All copyright and related rights worldwide are waived.
- **Unencumbered redistribution:** May be embedded in open-source libraries, proprietary test harnesses, research benchmarks, and offline datasets without royalty, attribution requirement, or copyleft viral effect.
- **Clean boundary assurance:** Contains zero third-party intellectual property, zero bearer credentials, and zero private reader data.
