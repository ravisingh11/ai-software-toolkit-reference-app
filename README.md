# Fieldnotes · AI Software Toolkit reference app

A working issue tracker that consumes [AI Software Toolkit](https://github.com/ravisingh11/ai-software-toolkit) through its supported installers. This separate repository makes adoption, QA, Proof checks, and release evidence inspectable.

**[Open the live demo](https://ai-software-toolkit-reference-app.navivision-account.workers.dev)** · [Release and verification evidence](https://github.com/ravisingh11/ai-software-toolkit-reference-app/releases/tag/v0.1.0) · [Evidence guide](docs/verification/README.md)

**Deployment report:** [Latest live deployment verification — updated main, toolkit v2.3.0](docs/verification/deployment-main-7d5df0a.md).
Verified on October 23, 2026 at 12:31 EDT: app [`7d5df0a`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/7d5df0a4910f99ec6cdc1bc80d33655bf398c66e),
exact toolkit/Worker identity, live API flows, and desktop/mobile UI. This recorded
deployment is separate from the PR scorecard and later documentation commits.

## Toolkit scorecard

[![Latest PR Scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/proof-badge.svg)](https://ravisingh11.github.io/ai-software-toolkit-reference-app/)

[Open the live PR scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/) · [Scorecard CI runs](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/workflows/proof-scorecard.yml)

The **All 33 checks** overview near the top of the report links every built-in
check to its details, grouped as **Selected**, **Available to adopt**, and
**Relevant later**. Only selected applicable checks count toward the score.
Checks remain optional to adopt; lifecycle and polyglot workflows stay manual.

The Pages report is published automatically from the latest accepted PR scorecard. It shows this application’s results, including missing evidence, and does not attest the current default branch or deployed Worker.

### Latest recorded CodeQL verification

[PR #40](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/40)
merged the credential setup documentation. Its [hosted Proof run 39359728920](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39359728920)
accepted real **GitHub CodeQL Default Setup** evidence for PR head
[`8170fa5`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/8170fa54ca12abf682c91b689f6a6e1b17ab8523).
The [managed CodeQL run 39359727461](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39359727461)
completed analyses for **Actions, JavaScript/TypeScript, and Python**. The
collector verified configuration, GitHub app identity, exact revision, managed
workflow and complete analysis provenance; saving the optional read-only
credential alone was not treated as evidence.

That snapshot records **20/25 advisory controls passed, zero enforced controls**.
Changed-code coverage, platform secret protection, and dependency remediation
still have **no result**. Container and artifact vulnerability checks remain
**failed**, with findings visible. The [separate Snyk run](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39359728840)
retains the previously authorized picomatch finding and quota failure; it is not
passing security evidence. [Manual lifecycle run 39359753235](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39359753235)
supplied seven accepted passing lifecycle controls and those two failed scans.

[Reference app Deep SAST scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/#check-deep-sast)
· [Toolkit scorecard](https://ravisingh11.github.io/ai-software-toolkit/#check-deep-sast).
These live links can advance to newer publications; the runs above identify the
recorded snapshot, not current `main` or the deployed Worker. **All toolkit
checks remain optional** to adopt and enforce. The separate five-language
polyglot workflow stays **manual (`workflow_dispatch`) and optional**; these
three CodeQL languages do not claim CodeQL coverage for Java, PHP or Scala.

### Stage-specific scorecard

The live report separates **Selected checks**, **Tools available to adopt**, and
**Checks relevant later**, with direct links to each group and setup guidance.
For this app's **pull-request development** stage, the existing Core/GitHub
profiles select 16 advisory checks. Nine optional tools are available to adopt;
eight release/deployment/runtime checks are relevant later. Only selected,
applicable checks enter the score. Selected failures and missing evidence remain
visible; unselected tools are not reported as failures or silently counted as passes.

Advisory/Enforced is separate from status: Passed, Failed, Blocked, Not configured,
Disabled, Awaiting manual run, or Unable to verify. Zero-count categories are
hidden. Missing changed-line coverage or security-settings evidence for a selected
check remains unverifiable. This does not change the separately reported Snyk
finding example or the app's dependencies.

This source uses [toolkit v2.3.0](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.3.0)
at immutable revision [`9108f2f`](https://github.com/ravisingh11/ai-software-toolkit/commit/9108f2fda1cc04087cb1326e0457302fab214f3c)
through the supported installer, including the stage-specific groups and full catalog.
The [activation index](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.3.0/docs/activation.md)
and read-only doctor explain setup and evidence gaps for all 33 checks. Existing
workflows and selections are retained; fresh starter defaults do not prune this app.
All toolkit checks remain optional;
**Application acceptance** remains the separate required merge check. Polyglot
and lifecycle producers stay **manual and optional**. The source update does not
deploy the Worker or rerun a historical snapshot using a newer policy.

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
- Toolkit **[v2.3.0](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.3.0)**, installed at immutable revision [`9108f2f`](https://github.com/ravisingh11/ai-software-toolkit/commit/9108f2fda1cc04087cb1326e0457302fab214f3c); see [provenance](toolkit.lock.json) and [adoption](docs/toolkit-adoption.md).
- Deterministic domain, migration, API, and Chromium acceptance tests, including negative permissions and race/error regressions.
- Generated app-specific local agent QA skills, executed through the actual Codex browser and HTTP tools. Agent QA remains advisory and separate from deterministic tests.
- Clean-commit Cloudflare release script, live revision verification, and a documented code rollback procedure.

## Use with Claude Code

Start with this application's [CLAUDE.md](CLAUDE.md) for repository context and
execution limits. Toolkit v2.3.0 provides [Claude Code onboarding](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.3.0/docs/quickstart.md#claude-code-setup),
[installation and updates](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.3.0/docs/install.md),
and the [release notes](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.3.0/docs/releases/v2.3.0.md).
See [the app's Claude setup](docs/toolkit-adoption.md#claude-code-setup) for a
preview-first skills install from the pinned release.

Skills guide work; installing them does not run checks or provide passing
evidence. All toolkit checks remain optional to adopt and enforce. GitHub
separately requires **Application acceptance** here. The polyglot workflow stays
**manual (`workflow_dispatch`) and optional**.

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

## Recorded live verification and cleanup (2026-10-19)

The live Pages HTML and JSON matched the latest successful publication at the
recorded verification: [scorecard run 39295060071, attempt 1](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39295060071/attempts/1),
evaluating PR head `629c125831f9445962efb7e4d7ec1e0e83dcf1a3` from
[merged PR #34](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/34),
published by [Pages run 39296050722](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39296050722).
An already-open older tab displayed the newer-snapshot notice; keyboard activation
of **Refresh latest** loaded that publication and preserved `#size-title`. No
relevant browser warnings, errors, or horizontal overflow were observed at
1280 × 720. This verifies publication freshness, not current `main`, subsequent
CI runs, or the deployed Worker.

That snapshot remains **13/16 advisory controls passed, zero enforced controls**.
Changed-code coverage, platform secret protection, and dependency remediation
still have **no result**; refreshing does not fill those evidence gaps. All toolkit
checks remain optional to adopt and enforce, and the polyglot workflow remains
**manual (`workflow_dispatch`) and optional**. The five-language results below
are recorded results from their linked run, not a new run from this verification.

Across both repositories, cleanup archived and removed **310 ignored cache/junk
files** (304 toolkit, 6 reference app) and hash-verified **8,589 existing
verification/state files** unchanged. All **183 tracked YAML files** were reviewed;
none was confirmed obsolete, so none was deleted. No tracked source, workflow,
or enforcement configuration changed, and no application was deployed. Recovery
archives and verification evidence were retained locally. See the
[toolkit's matching verification record](https://github.com/ravisingh11/ai-software-toolkit#recorded-live-verification-and-cleanup-2026-10-19)
for its separately recorded scorecard result.

Since that linked PR snapshot was produced, GitHub CodeQL default setup was
enabled for Actions, JavaScript/TypeScript, and Python. It conflicts with uploads
from the separate advanced CodeQL workflow. During this README update, the
optional `PROOF_CODEQL_LANGUAGES` activation variable was unset to avoid duplicate
uploads; default setup remains enabled. At that time, its analysis results were separate from
the selected advanced Proof provider contract: the deep-SAST check was
unverified, and that historical missing evidence remains visible. This does not
reinterpret the recorded 13/16 snapshot or make any toolkit check required.

## GitHub CodeQL default setup

Deep SAST now selects **GitHub CodeQL Default Setup** through the supported
provider configuration. The collector verifies GitHub app identity, the exact PR
head and trusted base, the managed dynamic workflow, and complete successful
analyses for every configured language (Actions, JavaScript/TypeScript, and
Python). It also rejects changed scan configuration, ambiguous runs, and
incomplete or inaccessible platform evidence. A successful check name alone is
not accepted. [Provider contract and adoption](docs/toolkit-adoption.md#github-codeql-default-setup)
describe the boundaries.

The separate advanced workflow remains unactivated. Missing changed-code
coverage, platform secret protection, and dependency remediation results remain
explicit; selecting this provider does not supply them. All toolkit checks
remain optional, and the polyglot workflow remains manual (`workflow_dispatch`).
This adoption does not alter historical verification snapshots or deploy the app.

<a id="latest-recorded-verification-2026-10-19"></a>

## Historical freshness verification (2026-10-19)

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

The recorded [manual five-language run](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39349416084)
verified main source `92c27786b157f5770a9a032f2fd2a823e22142d0` with toolkit
`698409630ce7de4ca0398994908fcde92f2fc893`: **25 non-coverage stages passed and
115 conformance cases passed** across Java, TypeScript, Python, PHP and Scala.
All five changed-line coverage stages were explicitly **not applicable** because
the example sources were unchanged against `5ae91e812042fee3b27f01a284d808cfbcaa7d94`;
this is not new measured coverage. The workflow remains manual and optional.
The older percentages below are historical measurements from their linked run.

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

Domain line/branch coverage is measured separately from Worker/UI integration coverage; **full changed-code line coverage is not activated**. Core/GitHub Proof profiles are advisory. Hosted agent QA and automatic Cloudflare deployment are unconfigured. The recorded PR #40 scorecard above accepted lifecycle artifact attestation and six other lifecycle controls; container and artifact vulnerability checks remained failed. A missing provider is never passed. See [the evidence index](docs/verification/README.md) for actual results, revisions, and remaining limits.

## Optional lifecycle verification

The current adoption pins toolkit `bb4130d4a27eb2d127fc832200797c732443119a`,
which fixes ZAP informational-warning exit/report classification without
suppressing findings. Historical [run 39349413608](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39349413608)
remains blocked for the original mismatch; no corrected result is claimed for
that run. The collector subsequently reached the trusted main baseline; PR #40 verification
above records the accepted follow-up results. All checks stay optional and advisory.


[PR #37](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/37)
merged the optional advisory lifecycle controls, revised verification fixture and
toolkit `698409630ce7de4ca0398994908fcde92f2fc893` at application source
[`92c2778`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/92c27786b157f5770a9a032f2fd2a823e22142d0).
[Source Proof CI](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39348583465)
passed; the unchanged [native Snyk failure](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39348587300)
remained visible under the scoped rollout exception below. Other current CI
passed or was intentionally skipped/neutral. This source merge establishes the
trusted baseline; it does not prove new lifecycle scans have passed. Subsequent manual lifecycle verification is recorded above. The later
[manual five-language run 39352901729](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39352901729)
passed 25 non-coverage stages and 115 conformance cases; all five changed-line
coverage stages were not applicable because the example sources were unchanged.
That run does not supply new measured coverage or full-application PR coverage. The [live
scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/) identifies
accepted snapshots, their subjects and actual missing/failed evidence. CodeQL's
optional configuration credential was unconfigured at the recorded PR #39 verification.


The manual **Lifecycle Verification** workflow builds the actual Fieldnotes
Worker in a pinned Node container and starts the built bundle with isolated
local D1 storage. Its configured probes use the real health/revision endpoint
and require unauthenticated API access to fail. It can produce IaC, container,
SBOM, artifact vulnerability/provenance, local deployment policy, DAST, runtime
and short endurance evidence. The trusted runtime is installed; these nine controls are now selected advisory
and remain optional. The recorded PR #40 scorecard above contains the subsequent
accepted evidence for this fixture.

This is a verification container, not a production Cloudflare deployment.
Thirty seconds of endurance probes does not prove production stability. Scanner
findings, blocked runs and absent evidence remain explicit. The initial local
container build was blocked by Docker disk exhaustion. The first hosted run
subsequently built the actual Worker and passed 429 probes over 30 seconds,
while reporting real container/artifact vulnerabilities and blocked ZAP output.
At that bootstrap stage, a hosted scorecard accepted signed artifact provenance;
the other new controls awaited the advisory policy merge. The updated image then ran in
[diagnostic run 39345279160](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39345279160):
432 probes, zero errors, and **43 HIGH / zero CRITICAL** vulnerability entries
with no fixed versions reported. The container and SBOM scans describe the same
43 findings, not 86 unique findings, and remain failed. These raw diagnostics
were not accepted scorecard evidence: the revised fixture still needed to reach
the trusted baseline and run again using the updated default-branch producer.
ZAP verification was pending at that bootstrap stage; the PR #40 record above
links the subsequent accepted hosted evidence. See [setup and limitations](docs/toolkit-adoption.md#optional-lifecycle-verification)
and [fixture details](examples/lifecycle/README.md).

The five-language polyglot workflow remains separate, manual and optional.
At [PR #39 verification](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39353272529),
CodeQL default-setup evidence was unverified because the optional configuration
credential was absent. The installed collector supports
`PROOF_CODEQL_CONFIGURATION_TOKEN` for repository Administration read access.
See the [read-only credential setup and verification checklist](docs/toolkit-adoption.md#optional-codeql-configuration-credential);
saving a credential alone does not prove that a fresh hosted scorecard accepted CodeQL evidence.

The [PR #36 native Snyk run](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39339879707)
failed for [picomatch ReDoS SNYK-JS-PICOMATCH-21248802](https://security.snyk.io/vuln/SNYK-JS-PICOMATCH-21248802)
and reported an exhausted private-test quota. The [PR #37 native Snyk run](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39345281350)
at `694b817` reports the same finding and quota failure. At review there was no fixed release.
The user explicitly authorized this rollout's merges with that unchanged failure
visible when other CI passes. This is an independent native CI result, not
accepted passing Proof evidence; no finding was suppressed or rule relaxed.

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
