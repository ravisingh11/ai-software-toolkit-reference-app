# Toolkit v2.2.1 deployment verification

**Status: DEPLOYED AND VERIFIED after the daily D1 reset.**

Verified on 2026-10-22 (America/New_York; observed UTC timestamp
`2026-10-23T00:07:24.036Z`). This is live release evidence, separate from
local PR QA and the revision-bound CI scorecard. The earlier blocked attempt is
retained below; its unavailable checks were not retroactively marked passed.

## Verified live identity

| Item | Observed value |
| --- | --- |
| App commit | `9ca17a30a776cca7c6ff68cb959def0808dd8d94` |
| Toolkit release | [v2.2.1](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.2.1) |
| Toolkit commit | `bf05798e4b03610551f9882620767f31de03d1df` |
| Cloudflare Worker version | `780741bf-a7e5-42cf-809f-7ed97c4bcc1a` |
| GitHub deployment | [7266781356](https://api.github.com/repos/ravisingh11/ai-software-toolkit-reference-app/deployments/7266781356), success |

[Open Fieldnotes](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/)
· [Live health](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/api/health)
· [Sanitized verification data](deployment-v2.2.1.json)
· [Live PR scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/)

## Release procedure and observed behavior

Deployment used the exact clean merged app commit above and the documented
`scripts/release.sh` procedure. Dependency installation, build dry-run, eleven
unit tests with domain-only coverage, migration validation and six browser/API
acceptance tests passed. Remote D1 reported no migrations to apply. No billing,
quota, provider activation or enforcement setting was changed.

The deployment succeeded, but the script's immediate smoke request initially
reported a health/revision mismatch during propagation. A subsequent health
request identified the intended app/toolkit/Worker version, and one explicit smoke
retry passed the full API lifecycle. This transient first failure is retained;
the release script is not described as an uninterrupted success.

Live browser and HTTP observations used isolated, synthetic demo sessions:

| Flow | Result |
| --- | --- |
| App/toolkit/Worker metadata | Passed: exact values above |
| Editor creation, search and priority filter | Passed |
| Status transition, comment and reload persistence | Passed |
| Empty title and invalid direct status transition | Rejected as expected; invalid transition HTTP 409 and invalid input HTTP 400 |
| Anonymous access and cross-origin mutation | HTTP 401 / 403 as expected |
| Mobile viewer UI | Read-only controls disabled; no horizontal overflow |
| Direct viewer create/status/comment attempts | HTTP 403 as expected |
| Cross-board comment access | HTTP 404 as expected |

The successful flows establish observed availability after reset, not a measured
root cause of the earlier account-wide read exhaustion or a guarantee that the
free quota cannot recur. The user's read-usage investigation remains separate.
A health response alone is not full application verification.

All toolkit checks remain optional/advisory; polyglot and advanced lifecycle
execution remain manual. The intentional independent Snyk failure example and
its workflow are unchanged. Synthetic workspaces expire after 24 hours; cookies,
credentials and real customer data are not part of this report.

## Earlier pre-reset blocked attempt — retained history

### Original pre-reset report

**Status: BLOCKED before deployment — Cloudflare D1 daily quota exhausted.**

Recorded 2026-10-22 (America/New_York). This is deployment preflight evidence,
not a passing deployment or a replacement for the PR scorecard. The updated
Worker has **not** been deployed by this attempt.

## Source and live identity

| Item | Revision |
| --- | --- |
| Intended app source | `9ca17a30a776cca7c6ff68cb959def0808dd8d94` ([PR #47](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/47)) |
| Intended toolkit release | [v2.2.1](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.2.1), `bf05798e4b03610551f9882620767f31de03d1df` |
| Observed live app source | `d9e79f91583685e7537737bca7b29a89d8cd3927` |
| Observed live toolkit source | `75207e17a06cdc16ace777571cac2e9f4eaceef1` |
| Observed Worker version | `d98ae58b-0a84-4a9f-8a8f-96f96d31f3e0` |

Live application: [Fieldnotes](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/).
The public [health endpoint](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/api/health)
returned HTTP 200 with the observed older revisions above. It does not establish
that the intended source is deployed or that the board's database operations work.

[Application acceptance passed](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39774599951)
on PR #47's exact head before merge; the merge tree matched that tested head.
That PR also recorded six local API/browser acceptance tests and four advisory
local functional-QA flows. Local and CI results do not replace live verification.

## Live observations

| Check | Observation |
| --- | --- |
| Cloudflare authentication | Configured account confirmed; credential values were not collected or published |
| Migration compatibility | No migration-file changes between observed live app source and intended source |
| Remote migration listing | Blocked: Cloudflare D1 code 7500, daily free-tier row-read quota exceeded |
| Browser initial load | Application shell loads |
| Anonymous session read | HTTP 401 before starting a demo, as expected |
| Start editor demo | HTTP 503; UI has no issue cards and reports temporary unavailability |
| Issue creation, search, status, comments and viewer permissions | Not verified live for v2.2.1; blocked by session creation |

The CLI reported that the account must wait for the midnight UTC quota reset or
use a paid plan. For this observation date, midnight UTC is **8 p.m. New York on
2026-10-22**. No billing change or quota bypass was attempted. The failed session
request and migration-query failure are retained as unavailable verification,
not passed checks. A responding health endpoint alone is insufficient.

## Resume and completion

1. After quota availability returns, confirm the intended clean source and
   authenticated Cloudflare account, then run the documented
   [release procedure](../deployment.md) and `scripts/release.sh`.
2. Verify the live app SHA, toolkit SHA and serving Worker version against that
   exact deployment. Record the GitHub deployment and sanitized API smoke output.
3. Exercise real browser editor/viewer flows and API permission/input boundaries
   with isolated synthetic data. Keep cookies and credentials out of reports.
4. Replace this blocked status only after those observations succeed, retaining
   this attempt's source identity and quota limitation in the history.

No Worker deployment, remote migration application, rollback, billing change or
provider activation was performed during this blocked attempt. All toolkit
checks remain optional/advisory. Polyglot and lifecycle workflows stay manual.
The intentional independent Snyk failure example and its workflow are preserved.

## Related reports

- [Live PR scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/): revision-bound CI evidence, not a production availability monitor.
- [Verification evidence index](README.md): historical releases, local QA and other verification records.
- [Toolkit adoption](../toolkit-adoption.md): exact published toolkit pin and optional configuration.
