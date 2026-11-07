# Fixture format

A fixture is a directory under `fixtures/synthetic/` (or a future
`fixtures/public-domain/`) that contains a story and its annotations.

```text
<fixture-id>/
  story.md        # the narrative text; original or public domain
  fixture.json    # annotations consumed by tests and by the extraction harness
```

`fixture.json` is validated against `schema/fixture.schema.json` and then
checked for internal consistency by `tools/validate_fixtures.py`.

## Fields that matter

| Field | Why it exists |
|---|---|
| `content_basis`, `rights_note` | Proves the text may be committed and redistributed |
| `scenario` | Maps the fixture to a scenario from `docs/testing/test-and-evaluation.md` |
| `entities[].first_reveal` | The earliest ordinal at which the entity may be shown **at all** |
| `names[].first_reveal` | An alias revealed later must not rename the entity earlier |
| `identity_links[].first_reveal` | Before this ordinal the two personas stay separate |
| `assertions[].attribution` | Narrator, witness claim, observation and inference are different classes |
| `status_changes[].reveal_ordinal` | Later evidence appends a transition; earlier views keep the earlier status |
| `horizons[]` | The actual test cases: what must appear, what must not, at ordinal `r` |

## Writing a new fixture

1. Choose a scenario not yet covered (see the table in the repository README).
2. Write the shortest text that reproduces the narrative trick. 150–600 words
   is usually enough; a long text makes the annotations expensive to review.
3. Annotate the graph only with what the text actually states. Do not add facts
   the story implies but never discloses — that turns a leak test into a guess.
4. Add at least two horizons: one before the trick resolves, one after.
   `forbidden` is the list that must stay empty in a projection.
5. Run `just validate`. A fixture whose annotations contradict each other is
   rejected: an identifier forbidden at ordinal `r` must have a reveal ordinal
   greater than `r`.

## What a fixture does not cover

- Rendering, E-Ink policy, and navigation history (client-level tests).
- Extraction quality metrics (private evaluation harness; it consumes the same
  fixtures but reports precision/recall).
- Rights review of a real book. A fixture proves behaviour, not permission.

## Adding real literature

Only public-domain or explicitly licensed text, with the licence recorded in
`rights_note` and, where required, the attribution preserved verbatim in
`story.md`. When in doubt, write an original text instead: it is cheaper than a
rights review and equally useful for projection tests.
