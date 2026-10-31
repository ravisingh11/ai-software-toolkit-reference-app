# Deployment and rollback

Fieldnotes uses a dedicated Cloudflare Worker and D1 database in the NaviVision account. The public URL is https://ai-software-toolkit-reference-app.navivision-account.workers.dev. Deployment status is documented in README; this URL alone is not deployment evidence.

Use the [manual verified-package procedure](package-promotion.md#manual-promotion-and-evidence). `scripts/release.sh prepare` retrieves and verifies one successful main-run package without Cloudflare access. After separate approval, `deploy` uploads that exact compiled package with `--no-bundle`, then `observe` verifies live health/API and desktop/mobile UI. `render` formats retained evidence without refreshing its timestamp. The tool requires reviewed Node 24/Wrangler prerequisites; it never rebuilds source, installs dependencies, applies migrations or deploys by default. Pending D1 migrations block upload until a separately reviewed migration procedure is completed.

Local development: `npm run db:local`, then `npm run dev`. E2E uses an isolated temporary local D1 directory, discarded after the run. Never point PR functional QA at the live Worker.

## Rollback

1. Read `npx wrangler deployments list --json` and `npx wrangler versions list --json`.
2. Verify the prior version's commit and that current migrations are compatible.
3. Run `npx wrangler rollback <previous-version-id> --message 'reason and source commit'`.
4. Verify `/api/health` identifies that prior version/commit, then run release smoke and inspect the browser.
5. To restore the intended release, roll back to its previously deployed version ID and verify again.

Workers rollback changes code/assets/configuration, not D1 contents. Use additive/backward-compatible migrations; if a migration cannot be reversed safely, forward-fix it. Migration rollback is not claimed by this example.

## Credential boundaries

CI builds, tests, scans, and produces a PR scorecard with its GitHub token. Releases currently use an authenticated maintainer's local Wrangler session. Automatic Cloudflare deployment is **not configured**. To enable it later, provision a dedicated account-scoped Workers/D1 API token as `CLOUDFLARE_API_TOKEN`, use a protected production environment, and demonstrate that workflow on a reviewed revision. Never copy workstation OAuth credentials into GitHub.

Hosted agent QA is also unconfigured; local Codex executes the generated functional QA skills. Browser acceptance is deterministic and separately labelled.

Official references: [static assets](https://developers.cloudflare.com/workers/static-assets/), [D1 migrations](https://developers.cloudflare.com/d1/wrangler-commands/), [Workers rollback](https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/), [CI credentials](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/).

## Cleanup scheduling

The account already uses its free-plan quota of five cron triggers. This application therefore removes expired sessions, their cascading board records, and old rate buckets when a new demo session starts. Authentication rejects expired sessions immediately after 24 hours; physical deletion happens on the next demo creation. No additional scheduled trigger or paid plan is required.
