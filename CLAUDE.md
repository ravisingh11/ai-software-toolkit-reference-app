# Fieldnotes application guidance

Read [AGENTS.md](AGENTS.md) for repository instructions and
[docs/design.md](docs/design.md) for application contracts. Fieldnotes is a
TypeScript issue tracker using Cloudflare Workers and D1. Keep application
contracts here and upstream toolkit policy in the pinned `.proof/` runtime.
Never edit vendored runtime merely to make a check pass.

Toolkit [v2.3.1](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.3.1) is pinned at immutable commit `f53a167be5283c1378740f475f231aa130f3aee9` in [toolkit.lock.json](toolkit.lock.json).
Use its versioned [Claude onboarding](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.3.1/docs/quickstart.md#claude-code-setup)
and [installation guide](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.3.1/docs/install.md).
See [toolkit adoption](docs/toolkit-adoption.md#claude-code-setup) for optional
Claude skills and [README.md](README.md) for setup and evidence links.

## Workspace and skills

Follow [workspace and skill onboarding](docs/onboarding.md) and the
[task-to-skill map](AGENTS.md#choose-a-skill-for-the-task). The committed
`.agents/skills/` copies are installed for Codex. Claude Code uses its own
`.claude/skills/` discovery directory; follow the preview-first optional install
in the adoption guide. Reading a named file explicitly does not establish that
Claude automatically discovered it. Codex alone is sufficient for this app.
Neither installation nor upstream Codex demonstrations verify Claude execution.

Use [SDLC checkpoints](docs/sdlc-checkpoints.md) and the
[README invocation examples](README.md#invoke-a-skill-or-inspect-evidence) to
identify the decision and actual evidence subject. Checkpoint names add no
runtime flags, automatic hooks, or action authority. Preserve original result
identities across PR edits, integration checks, and merge.

## Execution and review

Follow the user's execution limits. Do not run tests, install dependencies,
perform functional QA, deploy, or change GitHub settings unless authorized by
the task. When local execution is excluded, report it and use required CI as
requested; do not claim checks or QA ran locally.

Use PRs for changes to main. GitHub separately requires Application acceptance.
Toolkit controls and agent QA remain optional/advisory; lifecycle and polyglot
workflows stay manual (`workflow_dispatch`). Installing skills is not evidence
that checks passed. Preserve missing and failed evidence.

Keep credentials and real customer data out of this public demo. Preserve
server-side authorization independently of UI controls. Deployment requires a
separate authorized task and a clean committed revision; follow
[docs/deployment.md](docs/deployment.md).
