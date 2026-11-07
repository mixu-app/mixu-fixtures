# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Fixture schema (`schema/fixture.schema.json`) describing a synthetic story
  plus per-horizon "must be visible" / "must not be visible" annotations.
- `fixtures/synthetic/locked-stair`: original delayed-identity mini-mystery
  (CC0-1.0) with four horizons and a conflicting-testimony status change.
- `tools/validate_fixtures.py`, which rejects self-contradictory annotations and
  missing references; `just check` runs it.
