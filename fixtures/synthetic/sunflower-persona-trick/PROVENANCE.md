# Provenance: 向日葵庭院的守望者 (Sunflower Persona Trick)

Corpus identifier: `sunflower-persona-trick`
Content basis: `SYNTHETIC_ORIGINAL`
License: Creative Commons Zero v1.0 Universal ([CC0-1.0](../../../LICENSE))

## Authorship and generation method

This fixture is a 100% original Chinese synthetic mystery scenario authored
specifically for the Mixu spoiler regression suite. It was composed from scratch
by the project maintainers to test knowledge-horizon projection and entity
resolution under two combined Shin-Honkaku narrative tricks: a generational
shared-surname trap and a non-human/persona perspective mask.

The narrative text (`story.md`) and corresponding graph annotations
(`fixture.json`) were constructed simultaneously to create deterministic test
conditions across four sequential horizon ordinals:

1. **Horizon 1 (Scene 1):** Introduces the first-person narrator persona
   (`e_narrator_persona`, "庭院里的守望者") observing "桐生先生"
   (`e_kiryuu_elder`) locking a brass pruning key inside the sunflower
   greenhouse cabinet thirty years ago (`generation_era: "era_thirty_years_ago"`).
2. **Horizon 2 (Scene 2):** Shifts to the present summer
   (`generation_era: "era_present_summer"`), introducing a second figure also
   addressed as "桐生先生" (`e_kiryuu_younger`) alongside Steward Saeki's report
   of gravel traces left by a "失踪的庭院目击者" (`e_missing_witness`).
3. **Horizon 3 (Scene 3):** Resolves the generational surname trap via the
   family register, distinguishing the late botanist `桐生宪一`
   (`e_kiryuu_elder`) from his nephew `桐生慎司` (`e_kiryuu_younger`), while
   keeping the narrator persona's true nature hidden.
4. **Horizon 4 (Scene 4):** Reveals that the first-person narrator persona is the
   long-lived courtyard tortoise `陆龟琥珀` (`n_narrator_tortoise`) and confirms
   the identity link (`l_persona_is_witness`) between `e_narrator_persona` and
   `e_missing_witness`.

The scenario was authored completely from scratch without copying, translating,
adapting, or paraphrasing any existing literary work.

## Rights basis and legal dedication

The narrative text in `story.md` and all annotations, entities, assertions,
qualifiers, and horizons in `fixture.json` are dedicated to the public domain
worldwide under the terms of the **Creative Commons Zero v1.0 Universal
(CC0-1.0)** dedication.

To the extent possible under law, the authors have waived all copyright and
related or neighboring rights to this work. No copyright is reserved, and no
prior permission is required to copy, modify, distribute, or incorporate this
corpus into other software.

## Clean boundary guarantee

- **Zero third-party literary content:** Contains no excerpts, quotations,
  character names, or structural adaptations from copyrighted mystery novels or
  publications.
- **Zero user or personal data:** Contains no real-world personal data, reading
  notes, highlights, or telemetry. All character names (`桐生宪一`, `桐生慎司`,
  `佐伯`, `琥珀`) and settings are entirely fictional.
- **Independent creation:** Created in a clean environment as deterministic test
  fixtures for knowledge-horizon validation.

## Redistribution statement

This corpus is safe for unrestricted worldwide redistribution, inclusion in
public or proprietary source repositories, packaging into Git submodules
(e.g., in `mixu-client`, `mixu-graph`, `mixu-spoiler`), mirroring across public
registries, and execution in continuous integration test harnesses.
