# mixu-fixtures quality gates. Run via `just check`, never bare tool invocations.
set shell := ["bash", "-euo", "pipefail", "-c"]

check: lint-md validate

lint-md:
    markdownlint-cli2 --config .markdownlint-cli2.jsonc

validate:
    python3 tools/validate_fixtures.py
