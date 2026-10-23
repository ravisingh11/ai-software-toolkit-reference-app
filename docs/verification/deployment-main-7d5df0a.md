# Updated main deployment verification

**Status: DEPLOYED AND VERIFIED.**

Observed on October 23, 2026 at **12:31 EDT (America/New_York)**;
UTC timestamp `2026-10-23T16:31:43.644Z`. This records the deployment after the
reviewed Dependabot updates in PRs [#51](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/51),
[#52](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/52)
and [#53](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/53).
These are live release observations, separate from local PR QA, deterministic
test suites and the Proof scorecard. Merging this documentation does not deploy
the documentation commit or extend these observations to later source changes.

## Verified live identity

| Item | Observed value |
| --- | --- |
| Application commit | [`7d5df0a4910f99ec6cdc1bc80d33655bf398c66e`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/7d5df0a4910f99ec6cdc1bc80d33655bf398c66e) |
| Toolkit release | [v2.3.0](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.3.0) |
| Toolkit commit | `9108f2fda1cc04087cb1326e0457302fab214f3c` |
| Serving Worker version | `49eec506-0ca7-4bc3-a375-da3475f27fd9`, 100% traffic |
| Cloudflare deployment | `77b6d14e-ab95-4c7b-aaec-79780c2def68` |
| GitHub production deployment | [7283407960](https://api.github.com/repos/ravisingh11/ai-software-toolkit-reference-app/deployments/7283407960), [success status](https://api.github.com/repos/ravisingh11/ai-software-toolkit-reference-app/deployments/7283407960/statuses/20415807393) |

[Open Fieldnotes](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/)
· [Live health](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/api/health)
· [Sanitized verification data](deployment-main-7d5df0a.json)
· [Earlier v2.3.0 deployment](deployment-v2.3.0.md)

Health returned `status: ok` with the app, toolkit and Worker identities above.
The serving deployment inventory assigned 100% traffic to that Worker version.
Live links can advance; the source, version and timestamp identify this record.

## Observed API and browser behavior

| Flow | Observation |
| --- | --- |
| Desktop editor board | Isolated session seeded three issues; editor controls enabled |
| Create, search and priority filter | HTTP 201; four issues after creation; title search found one result; priority filters showed the expected matching and empty states |
| Status, comment and reload persistence | Synthetic issue moved to in progress; status and comment persisted after reload |
| Literal markup display | Synthetic markup appeared as text without an injected element |
| Input and transition boundaries | Empty title HTTP 400; direct triage-to-done HTTP 409; browser rejected an empty required title |
| Anonymous and cross-origin boundaries | Anonymous board read HTTP 401; cross-origin session write HTTP 403 |
| Mobile viewer | At 390 × 844, create/status/comment controls were disabled; filtering worked with no horizontal overflow |
| Server-side viewer restrictions | Direct create, status and comment attempts each returned HTTP 403 |
| Cross-board isolation | Viewer access to the editor board's comments returned HTTP 404 |
| Browser runtime errors | No page errors observed |

The separate release API smoke passed database health, isolated session, issue
creation, transition and comment persistence. Desktop/mobile screenshots were
visually inspected and contain only synthetic data:

- [Desktop editor board](evidence/main-7d5df0a/desktop-editor-board.png)
- [Editor detail after status/comment updates](evidence/main-7d5df0a/desktop-editor-detail.png)
- [Mobile viewer board](evidence/main-7d5df0a/mobile-viewer-board.png)

The verification JSON contains screenshot SHA-256 hashes. The detail screenshot
precedes the reload; persistence after reload is recorded in the observations.

## Procedure, limits and preservation

Deployment reused [passing hosted Application acceptance on the exact clean
merged app commit](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39985294411/job/120523094859).
It used Node 24.19.0 and Wrangler 4.151.2. The full `scripts/release.sh` was not
invoked because it repeats local test suites; its production deployment and live
release-smoke steps were performed directly under the user's no-extra-local-tests
constraint. Dependency installation and deployment bundling were necessary
deployment steps. D1 reported **no migrations to apply**; migration files were
unchanged from the prior deployment. No schema changes or database rollback occurred.

The first post-upload health request returned the prior serving identity. Fresh
health requests, API smoke, browser verification and a final health request then
matched the new app/toolkit/Worker identities. The initial observation is retained;
its cause was not established.

Three isolated synthetic demo boards were used: one for API smoke and two for
editor/viewer browser verification. Sessions expire after 24 hours. Browser
contexts closed and no cookies were saved. These bounded observations do not
establish exhaustive security, load, availability or application certification.

The previous Worker version `0ecf8e4b-03cd-4ce1-94c4-06f6a5cc0d25` was retained
in before-deployment records for code rollback. Code rollback does not reverse D1
contents. Earlier v2.3.0 and v2.2.1 reports retain their original evidence.

Toolkit checks remain optional/advisory; lifecycle and polyglot remain manual
and were not dispatched. The existing advisory Snyk finding, provider selections,
policy, credentials, billing and branch protection were unchanged. No extra local
test suites or local PR agent QA ran. This documentation update performs no
deployment; its required hosted CI is separate from the recorded live observations.
