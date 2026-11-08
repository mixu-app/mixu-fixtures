# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Fixture schema (`schema/fixture.schema.json`) describing a synthetic story
  plus per-horizon "must be visible" / "must not be visible" annotations.
- `fixtures/synthetic/locked-stair`: original delayed-identity mini-mystery
  (CC0-1.0) with four horizons and a conflicting-testimony status change.
- `fixtures/synthetic/silent-courier`: second delayed-identity mini-mystery
  (CC0-1.0) with four horizons, delayed identity link, and alibi contradiction.
- `fixtures/synthetic/false-witness`: adversarial mini-mystery (CC0-1.0) with
  four horizons, multi-alias reveal, unverified witness claim, and retroactive
  CONTRADICTED/RETRACTED transitions.
- `tools/validate_fixtures.py`, which rejects self-contradictory annotations and
  missing references; `just check` runs it.
- Comprehensive provenance and rights documentation per corpus (`PROVENANCE.md`
  in `fixtures/`, `locked-stair`, `silent-courier`, and `false-witness`),
  certifying 100% original synthetic generation, CC0-1.0 public domain dedication,
  clean boundary guarantees, and submodule redistribution safety.
