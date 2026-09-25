---
name: qa-web
description: >
  Browser functional QA flows for the Fieldnotes synthetic issue board. Load when
  public UI, assets, or end-to-end user interactions are affected.
---

# Fieldnotes web QA

## Testing target

Start the Worker from this checkout with `npm run dev` and wait for
`http://localhost:8791/api/health`. Use that exact local base URL. Never use a
workers.dev, preview, staging, or shared environment for a branch change run.

Drive the app through the Codex browser. Wait for a visible state transition
before capturing evidence. The site is a public synthetic demo: select editor or
viewer by creating that role's session. The role is not production identity, but
the server-side permission boundary must still be exercised.

## Flow menu

### F1: Editor creates and finds an issue

- **Covers:** issue creation UI, input validation, issue cards, search, priority and status filters.
- **Smoke:** yes
- **Personas:** editor
- **Steps:** Start an editor board; create a valid synthetic issue; search for its title; apply a priority or status filter that includes it.
- **Success criteria:** The issue appears once with its submitted title, priority, and `triage` status; filters and search update the visible list.
- **Negative checks:** Empty or too-long required fields show an accessible validation error and do not add a card.
- **Cleanup:** The isolated session board expires; do not create customer-like data.

### F2: Editor changes status and comments

- **Covers:** detail panel, comments, allowed status transitions, updates to issue cards.
- **Smoke:** yes
- **Personas:** editor
- **Steps:** Open an issue; change `triage` to `in_progress`; add one synthetic comment; move it to `done`.
- **Success criteria:** Each successful action is visible after the UI refresh, and the comment is shown once with its body.
- **Negative checks:** An unavailable transition is not presented as an enabled action; a repeated status action stays idempotent.
- **Cleanup:** The isolated session board expires.

### F3: Viewer remains read-only

- **Covers:** role switching, disabled mutation controls, viewer explanation, read access.
- **Smoke:** yes
- **Personas:** viewer
- **Steps:** Start a viewer board and open a seeded issue.
- **Success criteria:** Seeded issues remain visible and the UI explains viewer permissions.
- **Negative checks:** Create, comment, and status-change controls cannot produce a mutation from the viewer session. Confirm the API boundary through `qa-api` when authorization code changes.
- **Cleanup:** The isolated session board expires.

## Known failure modes

- The per-IP session quota can return 429 after repeated browser setup. Record BLOCKED with the status and wait for the hourly bucket rather than changing the application or testing another environment.
- A browser cookie identifies the isolated board. Do not record its value in evidence.

<!-- qa:learned:start -->
<!-- qa:learned:end -->
