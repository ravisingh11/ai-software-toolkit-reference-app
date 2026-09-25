---
name: qa-api
description: >
  HTTP functional QA flows for the Fieldnotes Worker API. Load when Worker API,
  D1 migrations, sessions, validation, or authorization behavior is affected.
---

# Fieldnotes API QA

## Testing target

Start the Worker from this checkout with `npm run dev` and poll
`http://localhost:8791/api/health`. Send HTTP requests only to that branch-owned
local URL. Retain session cookies in an ephemeral local cookie jar per persona;
never print the cookie value or reuse it across roles. The workers.dev URL is
release-only evidence and never proves a PR change.

Use bounded JSON payloads and synthetic titles/comments. Send a same-origin
`Origin: http://localhost:8791` header for every mutation and `Content-Type:
application/json` with valid JSON. Record status and only redacted response
fields in evidence.

## Flow menu

### F1: Health exposes ready deployment metadata

- **Covers:** `/api/health`, D1 readiness query, revision metadata.
- **Smoke:** yes
- **Personas:** anonymous
- **Steps:** Request `/api/health` after Worker readiness succeeds.
- **Success criteria:** It returns 200 JSON with `status: "ok"`, `revision`, `toolkitRevision`, and `version`.
- **Negative checks:** A failed local D1 migration or unavailable binding must not be represented as healthy.
- **Cleanup:** none.

### F2: Editor write lifecycle

- **Covers:** `/api/session`, issues, allowed status transitions, comments, D1 persistence.
- **Smoke:** yes
- **Personas:** editor
- **Steps:** Create an editor session in a fresh cookie jar; create one issue; list issues; transition it `triage` to `in_progress`; add one comment; retrieve comments.
- **Success criteria:** Creation returns 201, the issue and comment are visible only through that editor's session, and returned status reflects each allowed mutation.
- **Negative checks:** Invalid issue input returns 400; an invalid transition returns 409; unknown or cross-board IDs return 404.
- **Cleanup:** The synthetic session expires; do not reset remote D1.

### F3: Viewer and request-boundary enforcement

- **Covers:** viewer authorization, Origin/content-type/body-size checks, no-store API responses.
- **Smoke:** yes
- **Personas:** viewer
- **Steps:** Create a viewer session in a separate cookie jar and read its seeded issues; attempt create, comment, and status PATCH requests.
- **Success criteria:** Reads work; every mutation returns 403 with `{error:string}` and makes no observable change.
- **Negative checks:** Missing session returns 401; a cross-origin mutation, non-JSON mutation, or oversized body is rejected without a write. Verify `Cache-Control: no-store` on API responses.
- **Cleanup:** The synthetic session expires.

## Known failure modes

- Local Wrangler/D1 state belongs to the branch-owned process. Apply local migrations before testing a schema-dependent flow; do not apply remote migrations for QA.
- Rate limiting is per IP/hour. A 429 is an observable boundary result, but repeated setup quota exhaustion blocks unrelated flows and must be reported as BLOCKED.

<!-- qa:learned:start -->
<!-- qa:learned:end -->
