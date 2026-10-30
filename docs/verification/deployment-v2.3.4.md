# Toolkit v2.3.4 live deployment verification

**Status: DEPLOYED AND VERIFIED at the recorded observation time.**

Observed on October 29, 2026 at **19:30 EDT (America/New_York)**;
UTC timestamp `2026-10-29T23:30:32.675426+00:00`. These are retained live release
observations for app `9d24e43`, separate from local PR QA, deterministic suites
and Proof scorecards. Later documentation commits do not inherit these results
and have not been deployed. Recording this evidence performs no deployment,
new live verification or extra local tests.

## Verified live identity

| Item | Observed value |
| --- | --- |
| Application commit | [`9d24e434d211eea1d00927d578893001a9d5116c`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/9d24e434d211eea1d00927d578893001a9d5116c) |
| Toolkit release | [v2.3.4](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.3.4) |
| Toolkit commit | `2da5654836210fc484399cbc82c85fd821bc666d` |
| Serving Worker version | `1870a3a2-51cc-4554-bfd0-9b1a1a338a39`, 100% traffic |
| Cloudflare deployment | `ed1e44f5-e462-49e7-8355-ec531b6d8486` |
| GitHub production deployment | [7426690570](https://api.github.com/repos/ravisingh11/ai-software-toolkit-reference-app/deployments/7426690570), [success status](https://api.github.com/repos/ravisingh11/ai-software-toolkit-reference-app/deployments/7426690570/statuses/20955444608) |

[Open Fieldnotes](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/)
· [Live health](https://ai-software-toolkit-reference-app.navivision-account.workers.dev/api/health)
· [Sanitized verification data](deployment-v2.3.4.json)
· [Previous v2.3.3 deployment](deployment-v2.3.3.md)
· [Evidence index](README.md)

Health returned HTTP 200, `status: ok`, and the exact app, toolkit and Worker
identities above. The deployment inventory assigned 100% traffic to this Worker.
Live links can advance; this record is bound to its timestamp and revisions.

## Observed API and browser behavior

| Flow | Observation |
| --- | --- |
| Static assets | Live HTML, JavaScript and CSS bytes matched the committed source |
| Desktop editor board | Isolated session seeded three issues; editor controls enabled |
| Create, search and priority filter | HTTP 201; four issues after creation; search and priority filters showed matching and empty states |
| Status, comment and reload persistence | In-progress status and one comment survived reload; the editor subsequently completed the issue to done |
| Literal markup display | Synthetic markup appeared as text without an injected element |
| Input and transition boundaries | Empty title HTTP 400; direct triage-to-done HTTP 409; browser rejected an empty required title |
| Anonymous and cross-origin boundaries | Anonymous board read HTTP 401; cross-origin session write HTTP 403 |
| Mobile viewer | At 390 × 844, mutation controls were disabled; priority filtering worked without horizontal overflow |
| Server-side viewer restrictions | Direct create, status and comment attempts each returned HTTP 403 |
| Cross-board isolation | Viewer access to the editor board's comments returned HTTP 404; API responses used no-store |
| Repository link and compact layout | Correct GitHub URL and keyboard focus on desktop; 44 × 44 targets at 1440 and 390 px; source icon remained visible without horizontal overflow at 320 px |
| Runtime observations | No browser page errors; one expected unauthenticated startup `/api/session` HTTP 401 console message |

The separate release API smoke passed database health, isolated session,
issue creation, transition and comment persistence. Four original screenshots
were visually inspected during the live verification and contain only synthetic
data. They are copied unchanged:

- [Desktop editor board](evidence/v2.3.4/desktop-editor-board.png)
- [Editor detail with status/comment updates](evidence/v2.3.4/desktop-editor-detail.png)
- [Mobile viewer board](evidence/v2.3.4/mobile-viewer-board.png)
- [Compact mobile board](evidence/v2.3.4/compact-mobile-board.png)

The verification JSON records each original PNG's SHA-256 and dimensions. The
detail screenshot precedes reload and completion to done; those later results
are recorded observations rather than a claim about that earlier image.

## Procedure, limits and recovery

Deployment reused [passing hosted Application acceptance on the exact clean
merged app commit](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/40972856771).
Node 24.19.0 and Wrangler 4.151.2 were used with the expected Cloudflare account.
The full `scripts/release.sh` was not invoked because it repeats local suites;
its deployment and live release-smoke steps were performed directly under the
user's no-extra-local-tests constraint. Existing pinned dependencies were
reused, and Wrangler performed deployment bundling.

D1 reported **no migrations to apply**; none were applied. Application code,
dependencies and migration files were unchanged from the previous deployment
`4df96f9`; the reviewed toolkit update changed the Worker toolkit revision
setting. Previous Worker version `9014d612-2da6-4836-aa2d-d3ddac0ef0ff` was retained
for rollback. Code rollback changes code/configuration, not D1 contents. See the
[deployment and rollback procedure](../deployment.md).

One pre-deployment Python urllib health probe returned HTTP 403. Curl, native
Node and browser requests returned HTTP 200 with matching revision metadata.
This client-specific observation is retained; no application workaround or
credential change was made.

Three isolated synthetic sessions were used: one for release API smoke and two
for editor/viewer browser observations. Sessions expire after 24 hours. Browser
and HTTP contexts closed; no cookies were saved. These bounded observations do
not establish exhaustive security, load, future availability or application
certification. No credentials, account email, cookies or raw logs are included
in the public verification data.

Toolkit checks remain optional, Core advisory, and lifecycle/polyglot manual;
those optional producers were not dispatched. The existing advisory Snyk
picomatch finding remains visible. No producer selection, credential, billing
or branch-protection change was made. No extra local suites or local PR agent
QA ran. Documentation CI is separate from this deployment's observations, and
earlier deployment, real skill and hook evidence retain their original subjects.
