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
- `fixtures/eval/english-spoiler-eval`: English evaluation slice with 68 synthetic samples
  across train/val/test splits, evaluating 6 core spoiler challenges and claim vs. fact vs. inference boundaries.
- `fixtures/eval/japanese-spoiler-eval`: Japanese evaluation slice with 68 synthetic samples
  across train/val/test splits, evaluating modal/hearsay particles, ruby annotation invariance (HTML and Aozora Bunko formats), and shin-honkaku mystery conventions.
- `fixtures/eval/CROSS_LANGUAGE_AUDIT.md`: Cross-language boundary analysis and 24-item audit
  register certifying semantic boundary invariance across Chinese, English, and Japanese.
