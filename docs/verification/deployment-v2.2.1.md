# Toolkit v2.2.1 deployment verification

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
