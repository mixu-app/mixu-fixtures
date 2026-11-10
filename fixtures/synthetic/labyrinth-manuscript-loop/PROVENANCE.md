# Provenance: 星晷馆的迷宫手稿与二重轮回 (Labyrinth Manuscript Loop)

Corpus identifier: `labyrinth-manuscript-loop`
Content basis: `SYNTHETIC_ORIGINAL`
License: Creative Commons Zero v1.0 Universal ([CC0-1.0](../../../LICENSE))

## Authorship and generation method

This fixture is a 100% original Chinese synthetic mystery scenario authored
specifically for the Mixu spoiler regression suite. It was composed from scratch
by the project maintainers to stress-test knowledge-horizon isolation across
three intersecting Shin-Honkaku narrative structures: nested diegesis
(`INNER_WORK` manuscript vs. `OUTER_REALITY` mansion), time-loop epochs
(`loop_epoch: 1` vs. `loop_epoch: 2`), and competing detective hypothesis
cascades (`solution_alpha` refuted and superseded by `solution_omega`).

The narrative text (`story.md`) and corresponding graph annotations
(`fixture.json`) were constructed simultaneously to create deterministic test
conditions across four sequential horizon ordinals:

1. **Horizon 1 (Scene 1):** Establishes the nested diegetic boundary: a
   character named `久我怜司` dies inside the `INNER_WORK` manuscript
   (`a_inner_manuscript_death`), while the `OUTER_REALITY` author `久我怜司`
   (`e_author_kuga`) is alive sealing the manuscript in `loop_epoch: 1`
   (`a_outer_author_alive_epoch1`).
2. **Horizon 2 (Scene 2):** Introduces the bolted study in `loop_epoch: 1` and
   Detective Kanzaki's initial hypothesis (`hypothesis_frame: "solution_alpha"`,
   `a_hypothesis_alpha_wire_trick`) accusing Secretary Shiina of rigging a wire
   through the transom.
3. **Horizon 3 (Scene 3):** Advances to `loop_epoch: 2`, where Shiina's watched
   alibi (`a_epoch2_shiina_alibi`) and the lead-sealed transom refute
   `solution_alpha` via `t_solution_alpha_contradicted` (`CONTRADICTED`), while
   keeping `solution_omega` hidden.
4. **Horizon 4 (Scene 4):** Reveals the superseding deduction
   (`hypothesis_frame: "solution_omega"`, `a_hypothesis_omega_author_staged`),
   showing that Kuga himself used a thermal wax latch inside the bronze
   astrolabe across epochs and used the `INNER_WORK` manuscript to misdirect
   observers.

The scenario was authored completely from scratch without copying, translating,
adapting, or paraphrasing any existing literary work.

## Rights basis and legal dedication

The narrative text in `story.md` and all annotations, entities, assertions,
qualifiers, status transitions, and horizons in `fixture.json` are dedicated to
the public domain worldwide under the terms of the **Creative Commons Zero v1.0
Universal (CC0-1.0)** dedication.

To the extent possible under law, the authors have waived all copyright and
related or neighboring rights to this work. No copyright is reserved, and no
prior permission is required to copy, modify, distribute, or incorporate this
corpus into other software.

## Clean boundary guarantee

- **Zero third-party literary content:** Contains no excerpts, quotations,
  character names, or structural adaptations from copyrighted mystery novels or
  publications.
- **Zero user or personal data:** Contains no real-world personal data, reading
  notes, highlights, or telemetry. All character names (`久我怜司`, `神崎理人`,
  `椎名步美`) and settings (`星晷馆`) are entirely fictional.
- **Independent creation:** Created in a clean environment as deterministic test
  fixtures for knowledge-horizon validation.

## Redistribution statement

This corpus is safe for unrestricted worldwide redistribution, inclusion in
public or proprietary source repositories, packaging into Git submodules
(e.g., in `mixu-client`, `mixu-graph`, `mixu-spoiler`), mirroring across public
registries, and execution in continuous integration test harnesses.
