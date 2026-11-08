# Provenance: The False Witness

Corpus identifier: `false-witness`
Content basis: `SYNTHETIC_ORIGINAL`
License: Creative Commons Zero v1.0 Universal ([CC0-1.0](../../../LICENSE))

## Authorship and generation method

This fixture is a 100% original synthetic mystery scenario authored specifically
for the Mixu spoiler regression suite. It was written by the project maintainers
to test adversarial narrative modifications, including multi-alias reveals,
unverified witness testimony, and retroactive contradiction and retraction
transitions.

The story (`story.md`) and annotated graph structure (`fixture.json`) were
constructed together to validate horizon progression across four sequential
scenes:

1. **Horizon 1 (Scene 1):** The theft of Lord Harrington's golden chronometer by
   an elusive burglar known only by the alias "Clockmaker".
2. **Horizon 2 (Scene 2):** False witness testimony by housekeeper Mrs. Gable
   accusing gardener Thomas Cole of the burglary.
3. **Horizon 3 (Scene 3):** Arrest of Julian Price in Southwark, who is revealed
   as the true "Clockmaker" and confesses to acting alone.
4. **Horizon 4 (Scene 4):** Presentation of jail log records establishing Cole's
   airtight alibi, causing Mrs. Gable to retract her accusation and triggering
   retroactive status transitions (`CONTRADICTED` and `RETRACTED`).

The narrative was composed entirely from scratch to exercise adversarial edge
cases without utilizing or drawing from any existing novels, stories, or media.

## Rights basis and legal dedication

All components of this fixture—including the narrative text in `story.md` and the
complete annotation model in `fixture.json`—are dedicated to the public domain
under the **Creative Commons Zero v1.0 Universal (CC0-1.0)** dedication.

All copyright and related rights are waived worldwide. No licensing fees,
permissions, or restrictions apply to the reproduction, redistribution, or
adaptation of this fixture.

## Clean boundary guarantee

- **Zero third-party literary content:** Contains no excerpts, borrowings, or
  derivative plot structures from copyrighted literature or third-party authors.
- **Zero user or personal data:** All names (Detective Bradley, Lord Harrington,
  Mrs. Gable, Thomas Cole, Julian Price), places, and plot details are wholly
  fictional. No real-world user data, notes, or telemetry are incorporated.
- **Clean-room synthetic construct:** Authored independently to provide formal
  anti-spoiler assertion fixtures.

## Redistribution statement

This fixture is safe for unrestricted redistribution, inclusion in open-source
submodules across the Mixu ecosystem (e.g., `mixu-client`, `mixu-graph`,
`mixu-spoiler`), and incorporation into third-party evaluation benchmarks.
