#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .wrangler
app_test_state=$(mktemp -d "$PWD/.wrangler/test-XXXXXX")
trap 'rm -rf "$app_test_state"' EXIT
if [[ -n ${APP_PACKAGE_DIR:-} ]]; then
  # CI tests the frozen compiled package. The ordinary local dev path stays below.
  python3 scripts/release_package.py verify --package "$APP_PACKAGE_DIR" --expected-manifest "${APP_PACKAGE_MANIFEST_SHA:?Expected frozen manifest hash is required}"
  package_config="$APP_PACKAGE_DIR/payload/deploy-config.json"
  npx wrangler d1 migrations apply DB --config "$package_config" --local --persist-to "$app_test_state"
  npx wrangler dev --config "$package_config" --no-bundle --port 8791 --inspector-port 0 --persist-to "$app_test_state"
else
  npx wrangler d1 migrations apply DB --local --persist-to "$app_test_state"
  npx wrangler dev --port 8791 --inspector-port 0 --persist-to "$app_test_state"
fi
