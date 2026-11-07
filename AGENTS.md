# mixu-fixtures agent guide

## Scope and authority

- Governs only this repository. Workspace rules in `../AGENTS.md` apply.
- Public repository. Corpus (`fixtures/**`) is **CC0-1.0**; tools and schema are
  **Apache-2.0** (`# SPDX-License-Identifier: Apache-2.0` in new scripts).
- Purpose: make "no spoilers" a test that can fail, on a corpus anybody may use.

## Rights rules (hard gates)

- `content_basis` must be `SYNTHETIC_ORIGINAL`, `PUBLIC_DOMAIN` or
  `EXPLICITLY_LICENSED`, with `rights_note` stating the basis. No exceptions.
- No published book text, EPUB, illustration, map or table. No extracted graph of
  an in-copyright work. No personal reading notes or account data.
- When in doubt, write an original micro-story: cheaper than a rights review and
  equally useful for projection tests.
- Attribution required by a third-party licence stays verbatim in `story.md`, and
  that fixture's own terms take precedence over CC0.

## Annotation rules

- Annotate only what the text states. Encoding what a reader may infer turns a
  leak test into a guess.
- Every fixture needs at least two horizons: one before the trick resolves, one
  after. `forbidden` is the list that must stay empty in a projection.
- Raise ordinals honestly: a forbidden identifier must have a reveal ordinal
  **greater** than the horizon that forbids it, or the fixture contradicts itself
  (the validator rejects this).
- Keep stories 150–600 words; long texts make annotation review expensive and hide
  mistakes.
- One narrative trick per fixture, named in `scenario`.

## Gates

```sh
just check      # markdownlint + fixture validation
just validate   # schema + cross-reference + horizon consistency
```

Before trusting the gate, break a horizon on purpose (forbid an already-revealed
id) and confirm a non-zero exit.

## Adding a fixture

1. Pick an uncovered scenario from the table in `README.md`.
2. Write `story.md`, then `fixture.json` against `schema/fixture.schema.json`.
3. Run `just validate`; fix contradictions rather than widening the schema.
4. Add the fixture to the README table in the same change.

## Never

- Never relax the schema to make a self-contradictory fixture pass.
- Never add a fixture without a rights note.
- Never copy a corpus wholesale; a fixture is evidence, and evidence has
  provenance.

## CarryCtx

- `cd` here before `carryctx` or Git; branches `ctx-XXXX/<type>-<slug>`.
- Consumers (`mixu-client`, `mixu-spoiler`, the private harness) pin a commit; a
  fixture rename is a breaking change for them.
- No commit, push or release without authorization.
