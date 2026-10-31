#!/usr/bin/env bash
# Manual only. Each subcommand has a separate read/act boundary; no default deploy.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/promote_package.py "$@"
