# Fieldnotes · AI Software Toolkit reference app

A working issue tracker that consumes [AI Software Toolkit](https://github.com/ravisingh11/ai-software-toolkit) through its supported installers. This separate repository makes adoption, QA, Proof checks, and release evidence inspectable.

**[Open the live demo](https://ai-software-toolkit-reference-app.navivision-account.workers.dev)** · [Release and verification evidence](https://github.com/ravisingh11/ai-software-toolkit-reference-app/releases/tag/v0.1.0) · [Evidence guide](docs/verification/README.md)

## Toolkit scorecard

[![Latest PR Scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/proof-badge.svg)](https://ravisingh11.github.io/ai-software-toolkit-reference-app/)

[Open the live PR scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/) · [Scorecard CI runs](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/workflows/proof-scorecard.yml)

The Pages report is published automatically from the latest accepted PR scorecard. It shows this application’s results, including missing evidence, and does not attest the current default branch or deployed Worker.

### Scorecard freshness

The live scorecard checks for a newer published snapshot on load, when you return
to the tab, and every 60 seconds while the tab is visible. A persistent notice
flags a newer publication; choose **Refresh latest** to load it while keeping the
selected check or section. Existing results remain visible until you refresh.
If a freshness check fails or its metadata cannot be validated, **Freshness
unknown** remains visible; a previously detected newer snapshot stays flagged.

“Matches the latest published snapshot” describes the Pages publication only. It
does not verify current `main`, newer CI results, or the deployed Worker. Without
JavaScript, freshness stays unchecked and the refresh link remains available.
Tabs opened before this feature shipped need one initial reload. Refreshing does
not run CI or enable checks: missing evidence remains visible, and all toolkit
checks remain optional to adopt and enforce.

### Release snapshot (v0.1.0)

**v0.1.0 snapshot: ORANGE — 12/15 advisory controls passed; 3 have no result.**

[Read the scorecard](docs/verification/scorecard.md) · [Recorded CI run](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/36139392302) · [Newer CI scorecards](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/workflows/proof-scorecard.yml)

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
- Toolkit installed at immutable revision [`9ef9297`](https://github.com/ravisingh11/ai-software-toolkit/commit/9ef929780eaff0f863e9c44c5dbca8911f9f21b0); see [provenance](toolkit.lock.json) and [adoption](docs/toolkit-adoption.md).
- Deterministic domain, migration, API, and Chromium acceptance tests, including negative permissions and race/error regressions.
- Generated app-specific local agent QA skills, executed through the actual Codex browser and HTTP tools. Agent QA remains advisory and separate from deterministic tests.
- Clean-commit Cloudflare release script, live revision verification, and a documented code rollback procedure.

## Language-specific quality examples (manual and optional)

**The [Optional polyglot examples workflow](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/workflows/polyglot-examples.yml) runs only when manually dispatched (`workflow_dispatch`).** It does not run on pushes or PRs and is not a required merge check. Each adopting repository decides which checks and thresholds to use and whether to enforce them.

[Run the five-language examples](examples/polyglot/README.md): Java, TypeScript,
Python, PHP and Scala exercise the same defensive issue-transition contract with
native lint, integrity-checked tests, scoped changed-line coverage and architecture
checks. TypeScript is one example; other languages use their own tools. The live
Worker remains TypeScript. Repositories choose adoption and enforcement.

```sh
npm run polyglot:setup
npm run polyglot:check -- --base origin/main --threshold 90
```

Coverage requires a clean committed revision and a meaningful comparison base;
`origin/main` above is suitable for a committed feature branch with changed example
code. In GitHub Actions, choose **Run workflow**, select the target branch,
choose `all` or one language, and supply `base_ref` and `threshold` (the example
default is 90%). See the guide for runtime requirements, coverage scopes and the
separately pinned optional toolkit helpers.

## Latest recorded verification (2026-10-19)

[Scorecard freshness adoption (#33)](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/33)
merged at source [`e34993a`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/e34993afee31f40492dcacafcb93c5ab8e5782cb),
using toolkit [`9ef9297`](https://github.com/ravisingh11/ai-software-toolkit/commit/9ef929780eaff0f863e9c44c5dbca8911f9f21b0).
These recorded runs passed:

| Verification | Recorded result |
| --- | --- |
| [Application acceptance](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39289758236) | Build/typecheck, lint, unit coverage, migrations, repository validation, and API/browser acceptance passed on `e34993a`. |
| [Snyk](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39289758563) | Code and Open Source scans passed on `e34993a`; these remain advisory. |
| [Manual optional five-language run](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39289785991) | All 30 stages and 115 conformance cases passed on `e34993a`. |
| [PR #33 Proof scorecard](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39289788846) | Evaluated PR head `d3df54631961f09c8979c4e59d25017aaf53671b`: ORANGE / allow, 13/16 advisory controls passed, zero enforced controls. |

The manual five-language run measured changed-line coverage in the example scopes:
Java **100%**, TypeScript **93%**, Python **100%**, PHP **100%**, and Scala **92%**,
against baseline [`2932827`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/2932827657d4758cdf030ab693239cfb2a23e258)
and an explicitly selected **90%** threshold. Each language uses its own tools;
these are examples to adapt or replace. The workflow remains **manual
(`workflow_dispatch`) and optional**, with no push or PR trigger.

The PR scorecard still exposes missing changed-code coverage, platform secret
protection, and dependency remediation evidence. The separate polyglot run does
not fill those PR evidence gaps. These are source/CI records, separate from the
v0.1.0 release and deployed Worker; all toolkit checks remain optional, while
GitHub separately requires **Application acceptance** for merging.

## Merged maintenance and recorded verification (2026-10-18)

The merged updates include:

- [Wrangler and dependency remediation (#16)](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/16): Wrangler 4.151.1, scoped Undici 7.30.1 and Ajv URI-parser fixes, and three toolchain regression tests. [Adoption notes](docs/toolkit-adoption.md) explain the overrides and their removal conditions.
- [Playwright update (#19)](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/19): Playwright 1.64.1, retaining compatible TypeScript 5.9.3. Pinned Actions updates use [setup-node 7.1.0 (#17)](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/17) and [upload-artifact 7.0.2 (#18)](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/18).
- [Advisory Snyk scans (#10)](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/10): separate Code and Open Source scans on PRs, pushes to `main`, or manual dispatch. Open Source analyzes the root npm lockfile including development dependencies; it does not scan all five native dependency graphs. These scans do not activate a Snyk provider in Proof policy.

The recorded [manual five-language verification](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39192185020) passed on main source [`7ff99c1`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/7ff99c1eba782ec804cfcc59ae928503fb8f1707), using toolkit `7b8b3a1`: all 30 stages and 115 conformance cases passed. Changed-line coverage was Java **100%**, TypeScript **93%**, Python **100%**, PHP **100%**, and Scala **92%**, against baseline `2932827` and the explicitly selected 90% threshold. [Recorded evidence](docs/verification/toolkit-refresh.md) includes exact revisions and limits.

The scorecard now names each check’s configured provider, including inactive checks. Explicitly unselected providers show **Not configured**; missing selection data in older artifacts shows **Not reported**. Provider names link to the public provider configuration at the evaluated revision. A separate **Latest reported run** link appears only when valid evidence supplies one; missing evidence remains visible. Labels describe configuration, not credential readiness or a passing scan. See [provider semantics](docs/toolkit-adoption.md#configured-providers-in-the-scorecard).

The refreshed scorecard skips waiting for an absent optional Snyk check only when its matching enable variable is explicitly `false`; queued or running checks still wait. Missing selected evidence remains visible as `no_result`. The dependency-vulnerability control is not activated in this consumer’s Proof policy, although its default Snyk Open Source binding remains configured; separate Snyk scans remain advisory. The polyglot workflow is **manual and optional**, and the tools/configurations are **language-specific examples** for repositories to adapt or replace.

Historical main-branch verification follows. The following runs passed on `main` at [`2383bcf`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/2383bcfc9b46ad890f46bd6f4593d52c32772e49), using toolkit revision `e5d3074`:

| Verification | Recorded result |
| --- | --- |
| [Application acceptance](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39168165520) | Build/typecheck, lint, unit coverage, migrations, repository validation, and six API/browser acceptance tests passed. |
| [Snyk](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39168165743) | Code and Open Source scans passed with the configured high-severity threshold. |
| [Manual optional polyglot run](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39168166046) | All five languages passed all 30 stages (versions, build, lint, tests, architecture, coverage), with 23 conformance cases per language: 115 total. |

That polyglot run compared against [`2932827`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/2932827657d4758cdf030ab693239cfb2a23e258), before the examples were introduced, with a chosen 90% changed-line threshold:

| Language | Changed-line coverage in example scope |
| --- | --- |
| Java | 100% |
| TypeScript | 93% |
| Python | 100% |
| PHP | 100% |
| Scala | 92% |

This measures the example scopes; full-application changed-code coverage remains unconfigured. The [PR #10 Proof scorecard](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39167631000) evaluated PR head `d2747a2`: **ORANGE / allow, 13/16 advisory controls passed (81.2%), zero enforced controls**. Missing evidence remains visible. GitHub separately requires **Application acceptance**; the polyglot workflow remains manual and optional.

These are recorded source/CI results, separate from the v0.1.0 release snapshot above. This maintenance did not deploy the application or attest the current live Worker; hosted agent QA remains unconfigured.

Repeated trusted PR-size runs now resolve only when their subject and metrics agree; conflicting or missing evidence remains visible. Scope-limit failures stay advisory, and all toolkit checks remain optional to adopt.

## Verification

```sh
npm run build
npm run lint
npm run test:coverage
npm run validate:migrations
npm run test:e2e
python3 .proof/validators/validate_repository.py
npm run toolkit:check          # clean committed snapshot; Docker required for scans
```

Domain line/branch coverage is measured separately from Worker/UI integration coverage; **full changed-code line coverage is not activated**. Core/GitHub Proof profiles are advisory. Hosted agent QA, artifact attestation, and automatic Cloudflare deployment are unconfigured. A missing provider is never passed. See [the evidence index](docs/verification/README.md) for actual results, revisions, and remaining limits.

## Repository map

| Directory | Purpose |
| --- | --- |
| `src/` | Worker API and domain validation |
| `public/` | Browser UI, styles, and security headers |
| `migrations/` | Versioned D1 schema |
| `tests/` | Domain and real Worker/browser acceptance |
| `examples/polyglot/` | Five native language examples and shared defensive contract |
| `scripts/` | Migration verification, isolated test server, release smoke/release |
| `.proof/` | Installed upstream runtime and policy |
| `.agents/skills/` | Installed toolkit skills and generated app-specific QA |
| `docs/` | App design, adoption, deployment, and verification evidence |

Read [design](docs/design.md), [deployment and rollback](docs/deployment.md), [contribution guidance](CONTRIBUTING.md), and [security](SECURITY.md). Toolkit upgrades use a reviewed, pinned PR and rerun this consumer's acceptance checks.

### PR size report

The **PR Size / Files & LOC** workflow shows counted files, added lines,
added plus deleted lines, and maximum additions per file against configured
limits. The published check retains its compatible name `PR Change Scope`.
Scope is advisory: exceeding a limit warns and does not block merging.
The scorecard dashboard displays validated aggregate measurements when present;
older evidence is explicitly unavailable. See `.proof/change-scope.yaml`
for this application's thresholds and excluded paths.

See [scorecard freshness](#scorecard-freshness) for stale snapshot notices and
refresh behavior. Missing evidence is retained and Proof checks remain optional.
