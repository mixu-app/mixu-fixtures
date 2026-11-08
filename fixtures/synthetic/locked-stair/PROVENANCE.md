# Provenance: The Locked Stair

Corpus identifier: `locked-stair`
Content basis: `SYNTHETIC_ORIGINAL`
License: Creative Commons Zero v1.0 Universal ([CC0-1.0](../../../LICENSE))

## Authorship and generation method

This fixture is a 100% original synthetic mystery scenario authored specifically
for the Mixu spoiler regression suite. It was written by the project maintainers
as a targeted micro-story to test knowledge-horizon engine behavior under
delayed identity resolution and conflicting witness testimony.

The narrative text (`story.md`) and corresponding graph annotations
(`fixture.json`) were constructed simultaneously to create deterministic test
conditions for four sequential horizon ordinals:

1. **Horizon 1 (Scene 1):** Introduces "Mr. Ishida" checking into a guesthouse.
2. **Horizon 2 (Scene 2):** Introduces the "man in the grey coat" descending the
   stairs during a lamp failure.
3. **Horizon 3 (Scene 3):** Merges the "man in the grey coat" with "Mr. Ishida"
   via the keep's observation of the coat on the peg.
4. **Horizon 4 (Scene 4):** Introduces the porter's conflicting account,
   creating a contradictory witness claim.

The scenario was authored from scratch without copying, translating, adapting,
or paraphrasing any existing literary work.

## Rights basis and legal dedication

The narrative text in `story.md` and all annotations, entities, assertions, and
horizons in `fixture.json` are dedicated to the public domain worldwide under the
terms of the **Creative Commons Zero v1.0 Universal (CC0-1.0)** dedication.

To the extent possible under law, the authors have waived all copyright and
related or neighboring rights to this work. No copyright is reserved, and no
prior permission is required to copy, modify, distribute, or incorporate this
corpus into other software.

## Clean boundary guarantee

- **Zero third-party literary content:** Contains no excerpts, quotations, or
  structural adaptations from copyrighted mystery novels or publications.
- **Zero user or personal data:** Contains no real-world personal data, reading
  notes, highlights, or telemetry. All character names ("Mr. Ishida", the keep,
  the porter) and settings are entirely fictional.
- **Independent creation:** Created in a clean environment as test fixtures for
  knowledge-horizon validation.

## Redistribution statement

This corpus is safe for unrestricted worldwide redistribution, inclusion in
public or proprietary source repositories, packaging into Git submodules
(e.g., in `mixu-client`, `mixu-graph`, `mixu-spoiler`), mirroring across public
registries, and execution in continuous integration test harnesses.
