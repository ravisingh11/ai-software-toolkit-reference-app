# Application instructions
This repository is Fieldnotes, the deployed reference consumer of AI Software Toolkit. Keep application contracts in docs/design.md and upstream toolkit policy in the pinned .guardrails runtime. Never modify vendored runtime merely to make a check pass.

Use PRs for normal main changes. Preserve unrelated work. Use bounded native subagents when useful; they must not overwrite another lane. No credentials, real customer data, or production identity claims in this public demo. Demo workspaces expire after 24 hours. Keep API authorization independent of UI affordances.

Before PR: npm ci, npm run build, npm run lint, npm run test:coverage, npm run validate:migrations, npm run test:e2e, python3 .guardrails/validators/validate_repository.py, git diff --check. Run app-specific .agents/skills/qa for agent functional QA; deterministic tests alone are not agent QA. Missing producers are never passed. Functional QA stays advisory.

Deploy only a clean committed revision; use scripts/release.sh once available. Verify live health revision and real API/browser operation. Code rollback never reverses D1 schema; migrations must be backward compatible. See docs/design.md and docs/deployment.md.
