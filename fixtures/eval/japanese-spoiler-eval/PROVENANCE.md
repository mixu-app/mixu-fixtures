# Provenance and Rights Record for Japanese Spoiler Decision Evaluation Set

This document records the provenance, authorship methodology, rights basis, ruby annotation policies, and clean boundary guarantees for the held-out Japanese spoiler-decision evaluation set (`japanese-spoiler-eval`).

## Overview and purpose

The `japanese-spoiler-eval` corpus is a held-out multilingual benchmark designed to evaluate automated spoiler detection classifiers, LLM-based narrative firewall filters, and reader-copilot safety guardrails for the Mixu project in Japanese.

Spoiler safety in Japanese presents unique linguistic and structural challenges, including modal particle nuances (`〜かもしれない`, `〜に違いない`), hearsay markers (`〜らしい`, `〜と証言した`), passive voice constructions (`〜された`), and typographic conventions such as ruby glosses. This evaluation set tests six core spoiler challenges:

1. `direct_reveal`: Premature explicit disclosure of culprits, accomplices, murder methods, or concealed wills.
2. `implicit_hint`: Subtle narrowing of suspect sets, pointing toward unnoticed forensic indicators, or premature deduction.
3. `alias_identity`: Premature merging or identification of disguised personas, pseudonyms, or secret kinships.
4. `wrong_inference`: Red herrings, speculative reader deductions, and false accusations that must remain `SAFE`.
5. `benign_explanation`: Objective physical lore, chemical reactions, architectural layouts, or cultural context that is `SAFE`.
6. `paraphrase`: Semantic evasion attempting to disclose future plot developments through literary synonyms or metaphorical expressions.

## Authorship and synthetic methodology

All narrative scenarios, reading state summaries, candidate queries, rationales, and ground-truth labels in this evaluation set were authored entirely *de novo* by the Mixu project maintainers.

- **Zero published text:** No text from any published book, light novel, short story, screenplay, manga, or web fiction was consulted, copied, scraped, or adapted.
- **De novo mystery scenarios:** All three source scenarios employ classical Japanese mystery (*shin-honkaku*) archetypes (isolated island mansion locked-room poisoning, snowbound hot spring inn missing dagger, ancient temple bell-tower automaton sabotage) composed from scratch.
- **Ruby annotation coverage:** Includes samples with both standard HTML ruby tags (e.g. `<ruby>茶室<rt>ちゃしつ</rt></ruby>`) and Aozora Bunko style ruby notations (e.g. `｜閂《かんぬき》`), ensuring that evaluation systems maintain invariant classification whether ruby formatting is preserved or stripped.
- **Synchronous horizon design:** Every sample is strictly indexed against an integer horizon ordinal ($h \ge 0$), with an explicit summary of reader knowledge up to that horizon.
- **Split isolation:** To prevent data leakage (especially paraphrase and thematic memorization), dataset splits (`train`, `val`, `test`) are partitioned strictly by `source_text_id`. No scenario or character appears in more than one split.

## Source texts and split partitioning

| Source Text ID | Title | Genre Archetype | Assigned Split | Total Horizons | Sample Count |
|---|---|---|---|---|---|
| `src_mist_pavilion` | 霧幻館の双重密室 | Isolated pavilion, tea-room poison & ice delay trick | `train` | 3 | 28 |
| `src_snow_hotspring` | 白雪楼の消えた短刀 | Snowbound hot spring inn & staged dagger theft | `val` | 3 | 20 |
| `src_clock_temple` | 時鐘寺の傀儡鐘楼 | Temple belfry & automaton salt-melting timer | `test` | 3 | 20 |

Total samples: 68.

## Rights dedication under CC0-1.0

All data, schema definitions, annotations, and documentation in this directory are irrevocably dedicated to the public domain under the **Creative Commons Zero v1.0 Universal (CC0-1.0)** dedication.

- **No rights reserved:** All copyright and related rights worldwide are waived.
- **Unencumbered redistribution:** May be embedded in open-source libraries, proprietary test harnesses, research benchmarks, and offline datasets without royalty, attribution requirement, or copyleft viral effect.
- **Clean boundary assurance:** Contains zero third-party intellectual property, zero bearer credentials, and zero private reader data.
