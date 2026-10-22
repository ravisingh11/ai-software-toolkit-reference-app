# Fieldnotes application guidance

Read [AGENTS.md](AGENTS.md) for repository instructions and
[docs/design.md](docs/design.md) for application contracts. Fieldnotes is a
TypeScript issue tracker using Cloudflare Workers and D1. Keep application
contracts here and upstream toolkit policy in the pinned `.proof/` runtime.
Never edit vendored runtime merely to make a check pass.

Toolkit v2.1.0 baseline and reviewed post-release updates through the stage-specific scorecard adoption are recorded in [toolkit.lock.json](toolkit.lock.json).
See [toolkit adoption](docs/toolkit-adoption.md#claude-code-setup) for optional
Claude skills and [README.md](README.md) for setup and evidence links.

## Execution and review

Follow the user's execution limits. Do not run tests, install dependencies,
perform functional QA, deploy, or change GitHub settings unless authorized by
the task. When local execution is excluded, report it and use required CI as
requested; do not claim checks or QA ran locally.

Use PRs for changes to main. GitHub separately requires Application acceptance.
Toolkit controls and agent QA remain optional/advisory; the polyglot examples
workflow stays manual (`workflow_dispatch`). Installing skills is not evidence
that checks passed. Preserve missing and failed evidence.

Keep credentials and real customer data out of this public demo. Preserve
server-side authorization independently of UI controls. Deployment requires a
separate authorized task and a clean committed revision; follow
[docs/deployment.md](docs/deployment.md).
