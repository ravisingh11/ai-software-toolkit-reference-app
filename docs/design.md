# Fieldnotes reference application

## Purpose
A small issue tracker that consumes AI Software Toolkit through its public installer and demonstrates a tested, deployed change lifecycle. The application is a separate repository; toolkit policy remains upstream.

## Contract
Cloudflare Worker serves static HTML/CSS/JavaScript and a JSON API backed by D1. Each demo session receives a new isolated board and cryptographically random HttpOnly SameSite=Strict cookie; only its hash is stored. Sessions expire after 24 hours. Demo roles are selected at creation and persisted server-side; choosing an editor session is intentionally public, not production identity authentication. Never enter real customer data.

- `GET /api/health`: `{status:"ok",revision,toolkitRevision,version}` with a real database readiness query.
- `POST /api/session` body `{role:"editor"|"viewer"}`: creates fresh seeded workspace, returns `{role,expiresAt}` and cookie. Rate-limited per IP/hour; replaces this browser's cookie.
- `GET /api/session`: `{role,expiresAt}` or 401.
- `GET /api/issues`: `{issues:[{id,title,description,priority,status,createdAt,updatedAt}]}` for this workspace. Browser filters locally.
- `POST /api/issues` body `{title,description,priority}`: editor only, returns `{issue}` 201. Status starts `triage`.
- `PATCH /api/issues/:id` body `{status}`: editor only, returns `{issue}`. Allowed: triage -> in_progress; in_progress -> triage/done; done -> in_progress. Same status is idempotent.
- `GET /api/issues/:id/comments`: `{comments:[{id,body,createdAt}]}`.
- `POST /api/issues/:id/comments` body `{body}`: editor only, returns `{comment}` 201.
- Errors: `{error:string}` and meaningful HTTP status. Missing/cross-board ID ->404; malformed input ->400; unauthenticated ->401; viewer mutation ->403; invalid transition ->409; quota ->429.

Request writes require same-origin Origin header, JSON content type, bounded streamed bodies (8 KiB). Validate title 1..120, description 0..2000, comment 1..1000 characters; priority low/medium/high, status triage/in_progress/done. Bound session board to 100 issues and each issue to 50 comments. Query IDs and workspace in SQL predicates; parameterize all values. API responses no-store. HTML has CSP and security headers. Limit demo creation to 10/hour/IP (Cloudflare connecting IP in hosted environment); cleanup expired sessions and rate buckets when a new demo session starts. No request bodies/tokens in logs.

## UI
Fieldnotes is a calm, polished issue board with header, environment/evidence link, status tabs, search, priority filter, issue cards, create dialog, detail panel/comments, and clearly labelled demo role switching. Empty/error/loading states and keyboard accessible controls. Synthetic seeded examples. Viewer sees disabled mutation controls and explanation; API still enforces authorization.

## Acceptance and execution plan
1. Bootstrap separate public repo and pin toolkit commit `6e0422ae58602db39a43cb0a7bea5b28a410aa0a`; install core/GitHub advisory profile and relevant skills.
2. Implement backend/domain/migration tests and frontend concurrently against this contract.
3. Run domain coverage, migration validation, real local Worker/D1 API and Chromium flows; inspect rendered UI. Generate app-specific agent QA skills and execute actual functional QA.
4. Push implementation PR; bind toolkit producers to real commands. Observe checks and scorecard. Promote only stable deterministic app checks to required checks after real pass/fail proof.
5. Merge passing change; deploy exact clean commit using authenticated local Wrangler. Record GitHub deployment + public URL + health revision. Verify live UI/API; demonstrate compatible-code rollback without rolling back database schema.
6. Demonstrate intentional failing test PR blocked by required check, repair it, then merge only the passing revision. Store evidence links and limitations in README/docs.

Hosted AI-agent QA and automatic Cloudflare deployment require separately provisioned provider credentials. Do not copy workstation OAuth into GitHub. Local agent QA and authenticated local releases are supported; unconfigured hosted producers must remain explicitly unconfigured.
