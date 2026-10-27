# Application instructions
This repository is Fieldnotes, the deployed reference consumer of AI Software Toolkit. Keep application contracts in docs/design.md and upstream toolkit policy in the pinned .proof runtime. Never modify vendored runtime merely to make a check pass.

Use PRs for normal main changes. Preserve unrelated work. Use bounded native subagents when useful; they must not overwrite another lane. No credentials, real customer data, or production identity claims in this public demo. Demo workspaces expire after 24 hours. Keep API authorization independent of UI affordances.

Before PR: npm ci, npm run build, npm run lint, npm run test:coverage, npm run validate:migrations, npm run test:e2e, python3 .proof/validators/validate_repository.py, git diff --check. Run app-specific .agents/skills/qa for agent functional QA; deterministic tests alone are not agent QA. Missing producers are never passed. Functional QA stays advisory.

Deploy only a clean committed revision; use scripts/release.sh once available. Verify live health revision and real API/browser operation. Code rollback never reverses D1 schema; migrations must be backward compatible. See docs/design.md and docs/deployment.md.

## Choose a skill for the task

Read the selected `.agents/skills/<name>/SKILL.md` before following its procedure.
Use the installed project copy, not an unrelated user-wide copy with the same name.

| Task | Installed skill |
| --- | --- |
| Understand toolkit adoption and setup | `toolkit-setup` |
| Establish change boundaries and revision-bound evidence | `prepare-safe-change` |
| Review a change | `code-review` |
| Review dependency risk | `dependency-risk-review` |
| Find test gaps | `test-gap-finder` |
| Review security boundaries | `security-audit-lite` |
| Repair documentation or onboarding | `docs-sync` |
| Plan a substantial feature | `spec-driven-development` |
| Review repository setup | `repo-bootstrap` |
| Configure app-specific QA procedures | `qa-bootstrap` |
| Perform authorized app functional QA | `qa` (routes to `qa-web` and `qa-api`) |
| Review release readiness | `release-readiness` |

User execution limits override generic skill commands and the local verification
commands above. When local tests or QA are excluded, use required hosted CI and
report local verification as not run. Do not bootstrap QA merely to run it;
preserve the generated app-specific skills and their configuration.

Installation, discovery, invocation, and passing evidence are separate states.
Toolkit checks remain optional to adopt and enforce, Core stays advisory, and
lifecycle/polyglot workflows remain manual. Skill routing grants no authority
to merge, deploy, publish, change credentials, or change branch protection.
See [workspace and skill onboarding](docs/onboarding.md) for client selection,
the exact starter skills, and the limits of historical verification.

## Scope the SDLC decision

Follow [SDLC checkpoints](docs/sdlc-checkpoints.md) for coding through merge.
Name the actual working/index, head/base, integration or merged subject and
retain result identities across edits and squash/merge. Existing operations
remain `change`/`release`; recommended placement installs no hooks or triggers.
Use installed skills and existing hosted evidence within user execution limits.
Missing/failed/stale/not-run results never become passes. Main CI is separate
from live deployment evidence and grants no deployment authority.

<!-- BEGIN WORKSPACE HYGIENE:20261018 -->
## Workspace Hygiene

- At task start, inspect status, the current branch, registered worktrees,
  relevant open PRs, and active task ownership. Reuse a suitable checkout;
  preserve primary/default, locked, shared, and actively used worktrees.
- Record task-owned scratch paths and processes. Retain release evidence and
  reusable outputs in a named artifact location; unknown temporary files are
  not disposable merely because of their age or name.
- When cleanup is requested, fetch the intended upstream and verify current
  PR state. Committed or pushed does not mean merged: require exact commit
  reachability from the intended upstream target before ordinary removal.
  Fail closed on Git or API errors; missing results are not safety evidence.
- Before removal, check tracked, untracked, and ignored files, nested Git
  repositories/submodules, active processes, and checkout ownership. Preserve
  local-only commits, local databases/configuration, and evidence. A clean
  tracked-file status alone is insufficient; recheck immediately before acting.
- Record paths, before/after refs, preservation evidence, and recovery refs or
  archive manifests. Use the application's archive operation for managed
  worktrees; otherwise use `git worktree remove` without force. Do not use
  broad temporary-directory deletion or global `git clean`. Preserve needed
  ignored files separately; a Git snapshot may omit them.
- Squash/cherry-pick equivalence is not exact reachability. Retain these
  branches/worktrees for explicit review or a verified recoverable archive;
  never force-delete based on patch equivalence or empty `git cherry` output.
- At completion, stop task-owned processes and remove only task-created,
  disposable scratch after its consumers stop. Report branch, PR, worktree,
  scratch, and retained-evidence disposition, including blockers. Branch
  deletion still requires an explicit request; remote deletion and PR
  merge/closure require explicit task authority and current checks.

These instructions guide agent behavior; they do not schedule cleanup or
enforce retention automatically. Verify repo-specific cleanup commands before
using them.
<!-- END WORKSPACE HYGIENE:20261018 -->
