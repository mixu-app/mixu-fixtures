# Fixtures Provenance and Rights Record

This document records the provenance, authorship methodology, and rights basis
for the corpora in `mixu-fixtures`.

## Overview and purpose

`mixu-fixtures` provides a rights-cleared, public regression corpus for testing
the Mixu temporal narrative graph engine (`mixu-graph`) and anti-spoiler
firewall (`mixu-spoiler`).

The primary objective of this repository is to turn "no spoilers" into a verifiable,
reproducible test suite that can fail in CI, without depending on copyrighted
literary works or proprietary reader data.

## Authorship and synthetic generation methodology

All corpora currently located under `fixtures/synthetic/` are 100% original
synthetic mystery scenarios authored directly by the Mixu project maintainers.

- **Purpose-built test design:** Each story is authored as a concise
  (150–600 words) micro-narrative specifically tailored to stress-test one
  narrative trick (e.g., delayed identity reveals, persona merging, false witness
  testimony, retroactive state retraction).
- **Synchronous annotation:** The narrative prose (`story.md`) and the ground-truth
  graph annotations (`fixture.json`) are developed concurrently. Entity reveals,
  alias bindings, assertion attributions, and horizon boundaries are precisely
  aligned to ordinal positions in the text.
- **De novo composition:** Scenarios employ classic mystery archetypes (e.g.,
  locked guesthouse staircases, masked nocturnal messengers, stolen antique
  chronometers) authored completely from scratch. No text generation relies on
  copyrighted literary works.

## Rights basis and public domain dedication

All fixture text and annotation data in this repository are dedicated to the
public domain under the **Creative Commons Zero v1.0 Universal (CC0-1.0)**
dedication. The full legal text is available in the repository root [LICENSE](../LICENSE).

Under CC0-1.0:

- All copyright, neighboring, and related rights are waived worldwide to the
  maximum extent permitted by law.
- Anyone may copy, modify, distribute, display, or build upon the fixtures for
  any purpose—including commercial applications—without needing prior permission
  or paying licensing royalties.
- Downstream projects (both open-source and proprietary) can safely mount, embed,
  or vendor these corpora without inheriting copyleft obligations.

## Clean boundary guarantees

To ensure complete legal safety for all consumers, `mixu-fixtures` enforces three
strict boundary guarantees:

1. **No third-party literary works:** Neither whole texts nor excerpts from
   published books, copyrighted novels, translations, or commercial mystery
   fiction are permitted.
2. **No user or private data:** Fixtures contain zero user reading logs,
   highlights, margin notes, annotations, or personal data. All characters,
   locations, and events are purely fictional.
3. **No bearer credentials or secrets:** Fixtures never contain API keys,
   tokens, account identifiers, or system credentials.

## Submodule and redistribution safety

Because all synthetic corpora are original and dedicated to the public domain
under CC0-1.0:

- **Submodule embedding:** Safe to mount as a Git submodule in open-source
  repositories (`mixu-client`, `mixu-graph`, `mixu-spoiler`) and private or
  commercial systems without legal encumbrance.
- **Packaging and mirroring:** Safe for distribution via package registries,
  tarballs, offline test suites, and public mirrors.
- **Open development:** Third-party contributors and researchers may study,
  evaluate, and extend these fixtures without licensing friction.

## Corpus directory index

| Corpus ID | Scenario | Content Basis | License | Provenance Detail |
|---|---|---|---|---|
| [`locked-stair`](synthetic/locked-stair/fixture.json) | Delayed identity reveal | `SYNTHETIC_ORIGINAL` | CC0-1.0 | [PROVENANCE.md](synthetic/locked-stair/PROVENANCE.md) |
| [`silent-courier`](synthetic/silent-courier/fixture.json) | Disguise & alibi contradiction | `SYNTHETIC_ORIGINAL` | CC0-1.0 | [PROVENANCE.md](synthetic/silent-courier/PROVENANCE.md) |
| [`false-witness`](synthetic/false-witness/fixture.json) | Adversarial retroactive retraction | `SYNTHETIC_ORIGINAL` | CC0-1.0 | [PROVENANCE.md](synthetic/false-witness/PROVENANCE.md) |

## Future corpora and admission criteria

Any future corpus added to this repository must satisfy one of the following
provenance tiers before acceptance:

1. **Synthetic original (`SYNTHETIC_ORIGINAL`):** Original micro-story authored
   for testing and dedicated under CC0-1.0. Must include a corpus-level
   `PROVENANCE.md`.
2. **Public domain (`PUBLIC_DOMAIN`):** Verified public-domain historical text
   whose term of copyright has expired in all major jurisdictions (e.g., pre-1929
   works), with verifiable historical edition details in `PROVENANCE.md`.
3. **Explicitly licensed (`EXPLICITLY_LICENSED`):** Corpus provided under an
   explicit permissive open-source license compatible with public distribution,
   with the original license and attribution preserved verbatim.
