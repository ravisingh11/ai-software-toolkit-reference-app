#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
case "${1:-}" in
  setup) test -x node_modules/.bin/eslint || { echo 'Run npm ci first.' >&2; exit 2; } ;;
  build) node_modules/.bin/tsc --noEmit --project examples/polyglot/typescript/tsconfig.json ;;
  lint) node_modules/.bin/eslint examples/polyglot/typescript/src/domain.ts --max-warnings 0; node --check examples/polyglot/typescript/src/cli.mjs ;;
  run) node examples/polyglot/typescript/src/cli.mjs ;;
  coverage)
    : "${POLYGLOT_COVERAGE_REPORT:?Absolute Cobertura report path is required}"
    mkdir -p .artifacts/polyglot/typescript
    report_dir=$(mktemp -d "$PWD/.artifacts/polyglot/typescript/coverage-XXXXXX")
    trap 'rm -rf "$report_dir"' EXIT
    node node_modules/c8/bin/c8.js --include='examples/polyglot/typescript/src/domain.ts' --reporter=cobertura --reports-dir="$report_dir" node examples/polyglot/typescript/src/cli.mjs
    cp "$report_dir/cobertura-coverage.xml" "$POLYGLOT_COVERAGE_REPORT"
    ;;
  architecture) node_modules/.bin/depcruise --config examples/polyglot/typescript/dependency-cruiser.cjs examples/polyglot/typescript/src --output-type err-long ;;
  versions) node --version; node_modules/.bin/eslint --version; node_modules/.bin/tsc --version; node_modules/.bin/depcruise --version ;;
  *) echo 'Usage: check.sh setup|build|lint|run|coverage|architecture|versions' >&2; exit 2 ;;
esac
