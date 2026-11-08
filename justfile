# mixu-fixtures quality gates. Run via `just check`, never bare tool invocations.
set shell := ["bash", "-euo", "pipefail", "-c"]

py := if `which uv 2>/dev/null` != "" { "uv run" } else { "" }

check: lint-md validate

lint-md:
    markdownlint-cli2 --config .markdownlint-cli2.jsonc

validate:
    {{py}} python3 tools/validate_fixtures.py
