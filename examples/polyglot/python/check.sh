#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
python="${POLYGLOT_PYTHON:-$PWD/.artifacts/polyglot/tools/venv/bin/python}"
case "${1:-}" in
  setup) "$python" -m ruff --version; "$python" -m coverage --version ;;
  build) "$python" -c 'import ast,pathlib; [ast.parse(p.read_text(), filename=str(p)) for p in pathlib.Path("examples/polyglot/python").rglob("*.py")]' ;;
  lint) "$python" -m ruff check --config examples/polyglot/python/ruff.toml examples/polyglot/python ;;
  run) "$python" -m examples.polyglot.python.src.cli ;;
  coverage)
    : "${POLYGLOT_COVERAGE_REPORT:?Absolute Cobertura report path is required}"
    mkdir -p .artifacts/polyglot/python
    report_dir=$(mktemp -d "$PWD/.artifacts/polyglot/python/coverage-XXXXXX")
    trap 'rm -rf "$report_dir"' EXIT
    "$python" -m coverage run --rcfile=/dev/null --data-file="$report_dir/data" --source=examples/polyglot/python/src --module examples.polyglot.python.src.cli
    "$python" -m coverage xml --rcfile=/dev/null --data-file="$report_dir/data" --include='*/domain.py' -o "$POLYGLOT_COVERAGE_REPORT" >&2
    ;;
  architecture) "$python" examples/polyglot/python/architecture.py ;;
  versions) "$python" --version; "$python" -m ruff --version; "$python" -m coverage --version ;;
  *) echo 'Usage: check.sh setup|build|lint|run|coverage|architecture|versions' >&2; exit 2 ;;
esac
