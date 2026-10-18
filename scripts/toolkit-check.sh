#!/usr/bin/env bash
# Run the installed toolkit against an immutable, dependency-free source snapshot.
set -euo pipefail
cd "$(dirname "$0")/.."
[[ -z $(git status --porcelain) ]] || { echo 'Commit changes before collecting revision-bound evidence.' >&2; exit 1; }
mode=${1:-}
[[ "$mode" == '' || "$mode" == '--polyglot' ]] || { echo 'Usage: toolkit-check.sh [--polyglot]' >&2; exit 2; }
app_revision=$(git rev-parse HEAD)
app_base=$(git rev-parse "${GUARDRAILS_BASE_REF:-origin/main}")
mkdir -p .artifacts/toolkit
app_snapshot=$(mktemp -d "$PWD/.artifacts/toolkit/snapshot-XXXXXX")
git clone --quiet --no-hardlinks --no-checkout "$PWD" "$app_snapshot/repo"
git -C "$app_snapshot/repo" checkout --quiet --detach "$app_revision"
# The documentation producer runs before build installs dependencies. Scanning
# a developer workspace would include node_modules README files in this toolkit version.
export GUARDRAILS_BUILD_COMMAND='npm ci && npm run build'
export GUARDRAILS_UNIT_TEST_COMMAND='npm run test:coverage'
export GUARDRAILS_FORMAT_LINT_COMMAND='npm run lint'
export GUARDRAILS_MIGRATION_VALIDATION_COMMAND='npm run validate:migrations'
if [[ "$mode" == '--polyglot' ]]; then
  export GUARDRAILS_BUILD_COMMAND='npm run build && npm run polyglot:setup && npm run polyglot:build'
  export GUARDRAILS_UNIT_TEST_COMMAND='npm run test:coverage && python3 -m unittest discover -s scripts/tests && npm run polyglot:test'
  export GUARDRAILS_FORMAT_LINT_COMMAND='npm run lint && npm run polyglot:lint && npm run polyglot:architecture && npm run polyglot:format'
  # This producer deliberately does not claim full-app changed-line coverage.
  # Run the scoped native coverage separately with polyglot:check -- --base REF.
  export GUARDRAILS_SETUP_COMMAND='npm ci'
fi
python3 "$app_snapshot/repo/.guardrails/scan.py" \
  --target "$app_snapshot/repo" --revision "$app_revision" --base-ref "$app_base" \
  --evidence-dir "$PWD/.artifacts/toolkit/evidence" \
  --report "$PWD/.artifacts/toolkit/report.md" --json > .artifacts/toolkit/scorecard.json
# Keep the snapshot and evidence for inspection, including failed runs.
cat .artifacts/toolkit/report.md
