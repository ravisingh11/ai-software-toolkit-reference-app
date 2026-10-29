# Toolkit v2.3.3 live deployment verification

**Status: DEPLOYED AND VERIFIED at the recorded observation time.**

Observed on October 29, 2026 at **12:24 EDT (America/New_York)**;
UTC timestamp `2026-10-29T16:24:29.190458+00:00`. These are retained live release
observations for app `4df96f9`, separate from local PR QA, deterministic suites
and Proof scorecards. Later reporting/documentation commits have not been
deployed and do not inherit these results. Recording this evidence performs no
deployment or new live verification.

## Verified live identity

| Item | Observed value |
| --- | --- |
| Application commit | [`4df96f9f9e7da4951e122ce88456ca6eb624a9b4`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/4df96f9f9e7da4951e122ce88456ca6eb624a9b4) |
| Toolkit release | [v2.3.3](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.3.3) |
| Toolkit commit | `248d8f02e774e4f75af6ea2de49b466688dfae54` |
| Serving Worker version | `9014d612-2da6-4836-aa2d-d3ddac0ef0ff`, 100% traffic |
| Cloudflare deployment | `6a8524bd-1e32-4d0a-9706-f56b786c1189` |
| GitHub production deployment | [7417873746](https://api.github.com/repos/ravisingh11/ai-software-toolkit-reference-app/deployments/7417873746), [success status](https://api.github.com/repos/ravisingh11/ai-software-toolkit-reference-app/deployments/7417873746/statuses/20926849332) |

[Open Fieldnotes](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/)
· [Live health](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/api/health)
· [Sanitized verification data](deployment-v2.3.3.json)
· [Earlier deployment records](README.md)

Health returned HTTP 200, `status: ok`, and the exact app, toolkit and Worker
identities above. The deployment inventory assigned 100% traffic to this Worker.
Live links can advance; this record is bound to its timestamp and revisions.

## Observed API and browser behavior

| Flow | Observation |
| --- | --- |
| Static assets | Live HTML, JavaScript and CSS bytes matched the committed source |
| Desktop editor board | Isolated session seeded three issues; editor controls enabled |
| Create, search and priority filter | HTTP 201; four issues after creation; title search found one result; priority filters showed matching and empty states |
| Status, comment and reload persistence | In-progress status and comment survived reload; the editor subsequently completed the issue to done |
| Literal markup display | Synthetic markup appeared as text without an injected element |
| Input and transition boundaries | Empty title HTTP 400; direct triage-to-done HTTP 409; browser rejected an empty required title |
| Anonymous and cross-origin boundaries | Anonymous board read HTTP 401; cross-origin session write HTTP 403 |
| Mobile viewer | At 390 × 844, mutation controls were disabled; filtering worked without horizontal overflow |
| Server-side viewer restrictions | Direct create, status and comment attempts each returned HTTP 403 |
| Cross-board isolation | Viewer access to the editor board's comments returned HTTP 404 |
| Repository navigation | Source icon visible at 1440, 390 and 320 px, with a 44 × 44 target and no header overlap; desktop/mobile opened the correct GitHub page |
| Keyboard and runtime observations | Desktop source link had visible keyboard focus; scorecard link remained correct; no browser page errors observed |

The separate release API smoke passed database health, isolated session,
issue creation, transition and comment persistence. Six original screenshots
were visually inspected and contain only synthetic data:

- [Desktop editor board](evidence/v2.3.3/desktop-editor-board.png)
- [Editor detail with status/comment updates](evidence/v2.3.3/desktop-editor-detail.png)
- [Mobile viewer board](evidence/v2.3.3/mobile-viewer-board.png)
- [Desktop repository link with keyboard focus](evidence/v2.3.3/desktop-repo-icon.png)
- [Mobile repository navigation](evidence/v2.3.3/mobile-repo-icon.png)
- [Compact mobile repository navigation](evidence/v2.3.3/compact-mobile-repo-icon.png)

The verification JSON records each original PNG's SHA-256 and dimensions. The
detail screenshot precedes reload and completion to done; those later results
are recorded observations rather than a claim about that earlier image.

## Procedure, limits and recovery

Deployment reused [passing hosted Application acceptance on the exact clean
merged app commit](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/40909619781/job/123573710376).
Node 24.19.0 and Wrangler 4.151.2 were used with the expected Cloudflare account.
The full `scripts/release.sh` was not invoked because it repeats local suites;
its deployment and live release-smoke steps were performed directly under the
user's no-extra-local-tests constraint. Existing pinned dependencies were
reused, and Wrangler performed the deployment bundling.

D1 reported **no migrations to apply**; none were applied. Application code,
dependency and migration files were unchanged from the previous deployed app
`c3df3f4`; the reviewed toolkit update aligned source metadata. The previous
Worker version `d21b5b88-b7f8-4427-af3d-01495caa1330` was retained for rollback.
Code rollback changes code/configuration, not D1 contents. See the
[deployment and rollback procedure](../deployment.md).

Three isolated synthetic sessions were used: one for API smoke and two for
editor/viewer browser observations. Sessions expire after 24 hours. Browser and
HTTP contexts closed; no cookies were saved. These bounded observations do not
establish exhaustive security, load, future availability or application
certification. No credentials, account email, session cookies or raw logs are
included in the public verification data.

Toolkit checks remain optional, Core advisory, and lifecycle/polyglot manual;
those optional producers were not dispatched. The existing advisory Snyk
finding remains visible. No producer selection, credential, billing or
branch-protection change was made. No extra local suites or local PR agent QA
ran. Documentation CI is separate from this deployment's observations, and
earlier deployment, real skill and hook evidence retain their original subjects.
