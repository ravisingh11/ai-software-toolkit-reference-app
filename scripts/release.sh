#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[[ -z $(git status --porcelain) ]] || { echo 'Release requires a clean worktree.' >&2; exit 1; }
app_revision=$(git rev-parse HEAD)
git fetch origin main
git merge-base --is-ancestor "$app_revision" origin/main || { echo 'Release commit must be merged to main.' >&2; exit 1; }
npm ci
npm run build
npm run test:coverage
npm run validate:migrations
npm run test:e2e
npm run db:remote
mkdir -p .artifacts/release
npx wrangler deploy --var "APP_REVISION:$app_revision" --message "git:$app_revision" | tee .artifacts/release/deploy.log
APP_URL=https://ai-software-toolkit-reference-app.navivision-account.workers.dev APP_REVISION="$app_revision" node scripts/smoke.mjs | tee .artifacts/release/smoke.json
npx wrangler deployments list --json > .artifacts/release/deployments.json
