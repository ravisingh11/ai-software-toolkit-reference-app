#!/usr/bin/env bash
set -euo pipefail
mkdir -p .wrangler
app_test_state=$(mktemp -d "$PWD/.wrangler/test-XXXXXX")
trap 'rm -rf "$app_test_state"' EXIT
npx wrangler d1 migrations apply DB --local --persist-to "$app_test_state"
npx wrangler dev --port 8791 --inspector-port 0 --persist-to "$app_test_state"
