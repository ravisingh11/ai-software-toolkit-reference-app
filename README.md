# Fieldnotes · AI Software Toolkit reference app

A working issue tracker that consumes [AI Software Toolkit](https://github.com/ravisingh11/ai-software-toolkit) through its supported installers. This separate repository makes adoption, QA, guardrails, and release evidence inspectable.

**[Open the live demo](https://ai-software-toolkit-reference-app.navivision-account.workers.dev)** · [Release and verification evidence](https://github.com/ravisingh11/ai-software-toolkit-reference-app/releases/tag/v0.1.0) · [Evidence guide](docs/verification/README.md)

## Toolkit scorecard

[![Latest PR Scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/guardrails-badge.svg)](https://ravisingh11.github.io/ai-software-toolkit-reference-app/)

[Open the live PR scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/) · [Scorecard CI runs](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/workflows/guardrails-scorecard.yml)

The Pages report is published automatically from the latest accepted PR scorecard. It shows this application’s results, including missing evidence, and does not attest the current default branch or deployed Worker.

### Release snapshot (v0.1.0)

**v0.1.0 snapshot: ORANGE — 12/15 advisory controls passed; 3 have no result.**

[Read the scorecard](docs/verification/scorecard.md) · [Recorded CI run](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/36139392302) · [Newer CI scorecards](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/workflows/guardrails-scorecard.yml)

Evaluated PR commit: [`8bc67cb`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/8bc67cbcca74580b564ab2c9beb7a40285ba86d0). This release snapshot does not refresh automatically. Missing evidence: changed-code coverage, platform secret protection, and dependency remediation. No Guardrails controls are enforced in this snapshot; GitHub separately requires **Application acceptance** for merging.

## Try it locally

```sh
npm ci                         # Node 24
npm run db:local
npm run dev                    # http://localhost:8791
```

Choose **Editor** to create issues, move them through triage/in progress/done, and add comments. Choose **Viewer** to exercise read-only access. Search and priority/status filters work on your isolated board. Every new demo creates a separate synthetic workspace, expiring after 24 hours. Role selection is public demo functionality, not production login. Enter fictional data only.

## What this proves

- Real browser UI and JSON API with persistent D1 storage, server-side permissions, session isolation, input validation, and status transitions.
- Toolkit installed at immutable revision [`75207e1`](https://github.com/ravisingh11/ai-software-toolkit/commit/75207e17a06cdc16ace777571cac2e9f4eaceef1); see [provenance](toolkit.lock.json) and [adoption](docs/toolkit-adoption.md).
- Deterministic domain, migration, API, and Chromium acceptance tests, including negative permissions and race/error regressions.
- Generated app-specific local agent QA skills, executed through the actual Codex browser and HTTP tools. Agent QA remains advisory and separate from deterministic tests.
- Clean-commit Cloudflare release script, live revision verification, and a documented code rollback procedure.

## Verification

```sh
npm run build
npm run lint
npm run test:coverage
npm run validate:migrations
npm run test:e2e
python3 .guardrails/validators/validate_repository.py
npm run toolkit:check          # clean committed snapshot; Docker required for scans
```

Domain line/branch coverage is measured separately from Worker/UI integration coverage; **full changed-code line coverage is not activated**. Core/GitHub Guardrails profiles are advisory. Hosted agent QA, artifact attestation, and automatic Cloudflare deployment are unconfigured. A missing provider is never passed. See [the evidence index](docs/verification/README.md) for actual results, revisions, and remaining limits.

## Repository map

| Directory | Purpose |
| --- | --- |
| `src/` | Worker API and domain validation |
| `public/` | Browser UI, styles, and security headers |
| `migrations/` | Versioned D1 schema |
| `tests/` | Domain and real Worker/browser acceptance |
| `scripts/` | Migration verification, isolated test server, release smoke/release |
| `.guardrails/` | Installed upstream runtime and policy |
| `.agents/skills/` | Installed toolkit skills and generated app-specific QA |
| `docs/` | App design, adoption, deployment, and verification evidence |

Read [design](docs/design.md), [deployment and rollback](docs/deployment.md), [contribution guidance](CONTRIBUTING.md), and [security](SECURITY.md). Toolkit upgrades use a reviewed, pinned PR and rerun this consumer's acceptance checks.
