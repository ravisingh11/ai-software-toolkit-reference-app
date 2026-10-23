# Toolkit v2.3.0 deployment verification

**Status: DEPLOYED AND VERIFIED.**

Observed on October 23, 2026 at **07:25 EDT (America/New_York)**;
UTC timestamp `2026-10-23T11:25:02.243Z`. These are live release observations,
separate from local PR QA, deterministic test suites and the Proof scorecard.
This documentation records the deployed commit below; merging it does not
redeploy the Worker or make later source commits part of this verification.

## Verified live identity

| Item | Observed value |
| --- | --- |
| Application commit | [`cbb10d6d79304efa01635d3b6815cc6809b054bb`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/cbb10d6d79304efa01635d3b6815cc6809b054bb) |
| Toolkit release | [v2.3.0](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.3.0) |
| Toolkit commit | `9108f2fda1cc04087cb1326e0457302fab214f3c` |
| Serving Worker version | `0ecf8e4b-03cd-4ce1-94c4-06f6a5cc0d25`, 100% traffic |
| Cloudflare deployment | `4daddf96-9106-43d7-9cf3-26b3ddcb26d2` |
| GitHub production deployment | [7276941546](https://api.github.com/repos/ravisingh11/ai-software-toolkit-reference-app/deployments/7276941546), [success status](https://api.github.com/repos/ravisingh11/ai-software-toolkit-reference-app/deployments/7276941546/statuses/20386902074) |

[Open Fieldnotes](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/)
· [Live health](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/api/health)
· [Sanitized verification data](deployment-v2.3.0.json)
· [Previous v2.2.1 deployment](deployment-v2.2.1.md)

The health response reported `status: ok` and the exact app, toolkit and Worker
identities above. A responding health endpoint alone was not treated as full
application verification. The live links can advance; the recorded source,
version and timestamp identify this observation.

## Observed API and browser behavior

| Flow | Observation |
| --- | --- |
| Desktop editor board | New isolated session seeded three issues; editor controls enabled |
| Create, search and priority filter | HTTP 201; four issues after creation; title search found one result; priority filters showed the expected matching and empty states |
| Status, comment and reload persistence | Moved the synthetic issue to in progress; comment and status persisted after reload |
| Literal markup display | Synthetic markup appeared as text rather than an injected element |
| Invalid input and transition | Empty title HTTP 400; direct triage-to-done transition HTTP 409; required-title browser validation rejected an empty field |
| Anonymous and cross-origin boundaries | Anonymous board read HTTP 401; cross-origin session write HTTP 403 |
| Mobile viewer | At 390 × 844, create/status/comment controls were disabled; filtering worked and there was no horizontal overflow |
| Server-side viewer restrictions | Direct create, status and comment attempts each returned HTTP 403 |
| Cross-board isolation | Viewer access to the editor board's comments returned HTTP 404 |
| Browser runtime errors | No page errors were observed |

The release API smoke also passed database health, isolated session, issue
creation, transition and comment persistence. Desktop/mobile screenshots were
visually inspected. They contain only synthetic data:

- [Desktop editor board](evidence/v2.3.0/desktop-editor-board.png)
- [Editor detail after status/comment updates](evidence/v2.3.0/desktop-editor-detail.png)
- [Mobile viewer board](evidence/v2.3.0/mobile-viewer-board.png)

The verification JSON records screenshot SHA-256 hashes. The detail screenshot
precedes the reload; persistence after reload is recorded in the live observations.

## Procedure, limits and preservation

Deployment reused [passing hosted Application acceptance](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39894944025)
on the exact clean merged app commit. It used Wrangler 4.151.1 and Node 24.19.0.
The full `scripts/release.sh` was not invoked because it repeats local test suites;
its production deployment and release-smoke steps were executed directly under
the user's no-extra-local-tests constraint. Dependency installation and deployment
bundling were necessary deployment steps. Remote D1 reported **no migrations to
apply**, and there were no migration-file changes from the previously deployed
source. No schema changes or database rollback occurred.

Three isolated synthetic sessions were used: one API smoke board and two browser
editor/viewer boards. Demo sessions expire after 24 hours. Browser contexts were
closed; cookies, credential values and real customer data are not included here.
These bounded observations do not establish exhaustive security, load, availability
or application certification.

All toolkit checks remain optional/advisory. Lifecycle and polyglot remain manual
and were not dispatched. The independent Snyk failure example, provider selections,
policy, credentials, billing and branch protection were unchanged. No extra local
test suites or local PR agent QA ran. Required hosted CI for this documentation PR
is separate evidence and does not repeat the recorded production verification.

An initial Python urllib preflight health request returned HTTP 403. Subsequent
curl, Node smoke, Playwright API and actual-browser requests succeeded. The cause
was not established; the unsuccessful request is retained rather than described
as an uninterrupted passing preflight.

The prior serving Worker version `780741bf-a7e5-42cf-809f-7ed97c4bcc1a` was retained
in before-deployment records for code rollback. Code rollback does not reverse D1
contents. Historical v2.2.1 deployment evidence, including its earlier quota blocker,
is preserved without relabelling its source or results.
