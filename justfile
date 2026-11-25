# mixu-fixtures quality gates. Run via `just check`, never bare tool invocations.
set shell := ["bash", "-euo", "pipefail", "-c"]

py := if `which uv 2>/dev/null` != "" { "uv run" } else { "" }

check: lint-md validate validate-graph-memory validate-graph-memory-heldout test-graph-memory test-graph-updates test-sequential-source

lint-md:
    markdownlint-cli2 --config .markdownlint-cli2.jsonc

validate:
    {{py}} python3 tools/validate_fixtures.py

# Validate segmented benchmark isolation, provenance and every prefix horizon.
validate-graph-memory source="fixtures/benchmarks/graph-memory":
    {{py}} python3 tools/graph_memory.py validate --source {{source}}

# Deterministic export; model consumers must read inputs/ only, never gold/.
export-graph-memory output="local/graph-memory-export" stress_segments="24,48" distractors="1":
    {{py}} python3 tools/graph_memory.py export --output {{output}} --stress-segments {{stress_segments}} --distractors {{distractors}}

# Includes intentional negative horizon and input-leak mutations.
test-graph-memory:
    {{py}} python3 -m unittest discover -s tests -p 'test_graph_memory.py' -v

# Separate harder cohort; the initial six cases and export remain unchanged.
validate-graph-memory-heldout:
    {{py}} python3 tools/graph_memory.py validate --source fixtures/benchmarks/graph-memory-heldout

export-graph-memory-heldout output="local/graph-memory-heldout-export":
    {{py}} python3 tools/graph_memory.py export --source fixtures/benchmarks/graph-memory-heldout --output {{output}} --stress-segments ""

test-graph-updates:
    python3 -m unittest discover -s tests -p 'test_graph_updates.py' -v

graph-updates-export corpus output_dir:
    python3 tools/graph_update_eval.py --corpus '{{corpus}}' --output-dir '{{output_dir}}'

test-sequential-source:
    python3 -m unittest discover -s tests -p 'test_sequential_source.py' -v

sequential-source-export corpus old_targets output_dir:
    python3 tools/sequential_source_fixtures.py --corpus '{{corpus}}' --old-targets '{{old_targets}}' --output-dir '{{output_dir}}'
