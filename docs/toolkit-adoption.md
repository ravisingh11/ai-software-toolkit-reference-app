# Toolkit adoption

The runtime and workflows were installed from [toolkit v2.1.0](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.1.0) at immutable upstream commit `9e72693f08e9137467e4651d9e7b9fbff6070b1b` using the public `tooling/install.py --profile github --refresh-existing --scorecard-badge` entrypoint. Previously installed skills are preserved; their installation uses `tooling/install-skills.sh`. Exact commands and revision are in `toolkit.lock.json`. Application-specific generated QA skills extend the installed bootstrap.

Core and GitHub profile controls begin advisory. Application acceptance is a separate deterministic required check on main, verified with a passing implementation and an intentionally failing follow-up PR. No AI review or functional QA result is an enforced merge gate. Oversized bootstrap scope, unavailable providers, and incomplete evidence remain visible rather than changing policy to hide them.

Producer bindings: build=`npm run build`; unit tests=`npm run test:coverage`; format/lint=`npm run lint`; migrations=`npm run validate:migrations`; setup=`npm ci`. CodeQL default setup analyzes its configured Actions, JavaScript/TypeScript, and Python languages. Changed-code coverage is **not activated**: current coverage measures pure domain validation, while real Worker/D1 and frontend flows are verified by API/browser acceptance without line instrumentation. That test evidence must not be reported as full changed-line coverage. Artifact provenance and hosted agent QA are likewise not activated.

To upgrade, clone the toolkit at an exact reviewed commit, run its installer with `--refresh-existing` and the selected profile, refresh selected skills using the installer's merge/refresh guidance, review configuration preservation and all runtime diffs, update toolkit.lock.json and the Worker TOOLKIT_REVISION, and submit a PR. Run application acceptance, migration validation, scans, and generated local agent QA before merging. Treat a failing consumer test as an upstream compatibility signal.

## Claude Code setup

The v2.1.0 release refreshes onboarding and Claude guidance; its runtime,
workflows, and skills are unchanged from this app's previous toolkit pin.
The supported installer refresh produced no runtime or workflow differences.
`toolkit.lock.json`, `examples/polyglot/toolkit.json`, and the Worker
`TOOLKIT_REVISION` now identify the same immutable release commit. Updating
source metadata does not update the deployed Worker or establish new scan results.

Read [CLAUDE.md](../CLAUDE.md) before working in this application. To add starter
skills for Claude Code, use a separate trusted toolkit checkout at the pinned
release and preview the selection first:

```sh
git clone https://github.com/ravisingh11/ai-software-toolkit.git /path/to/toolkit
git -C /path/to/toolkit checkout --detach 9e72693f08e9137467e4651d9e7b9fbff6070b1b
python3 /path/to/toolkit/tooling/ai_toolkit init --target /path/to/ai-software-toolkit-reference-app --components skills --clients claude-code --skills starter --preview
# After reviewing the preview, apply the same selection:
python3 /path/to/toolkit/tooling/ai_toolkit init --target /path/to/ai-software-toolkit-reference-app --components skills --clients claude-code --skills starter --yes
```

This selection installs skills into `.claude/skills/` without installing Proof
workflows or running checks. Use `--clients codex,claude-code` when adopting both
clients. This upgrade preserves the existing Codex skills and app-specific QA;
it does not install the optional Claude skill selection automatically. Keep
application instructions in this repository's CLAUDE.md; the installer does not
write that file.

For example: “Use the code-review skill to review this change. Explain risks
with file references. Do not run tests or commands unless I ask.” Review the
[versioned upstream onboarding](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.1.0/docs/quickstart.md#claude-code-setup)
and [CLI guide](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.1.0/docs/install.md).
All toolkit checks remain optional. Application acceptance remains the only
required CI check; the polyglot workflow remains manual and optional.

## Observed consumer behavior

### Optional provider waiting

The installed scorecard supports the upstream optional-provider wait fix. Only an explicit `false` value (case-insensitive) for `SNYK_CODE_ENABLED` or `SNYK_OPEN_SOURCE_ENABLED` stops waiting for an absent matching check. Already queued or running checks still wait; other providers retain their normal wait budget. Missing selected evidence remains `no_result`, with its existing advisory or enforced policy outcome. The setting does not deactivate a control or manufacture a pass.

The dependency-vulnerability control is not activated in this consumer’s Proof policy, although the default Snyk Open Source provider binding remains configured. These hints do not activate a control. Its independent consumer-owned Snyk workflow continues to report its own scans. Each repository decides which checks to adopt and enforce.

### GitHub CodeQL default setup

The supported installer refresh and
`python3 .proof/configure.py --select-provider deep-sast=github-codeql-default-setup`
select the separate **GitHub CodeQL Default Setup** provider. GitHub default setup
is already configured; the advanced workflow opt-in `PROOF_CODEQL_LANGUAGES`
remains unset to avoid conflicting uploads. The scorecard workflow has only
read access to security events for inspecting platform analysis provenance.

The collector requires the exact PR head and trusted base, GitHub Advanced
Security aggregate-check identity, the GitHub-managed dynamic workflow and
GitHub Actions job identities, and complete successful code-scanning analyses
for all configured languages. The configuration must predate the run and match
the trusted base; language aliases normalize to a complete configured set.
Missing permissions, missing or warning-bearing analyses, changed configuration,
reruns or ambiguous runs, and unsupported configuration remain explicit
`no_result` evidence. A scan conclusion or check name alone cannot pass this
provider. The existing advanced-workflow provider contract is unchanged.

A PR installing a new trusted runtime may still be evaluated by its older base
runtime. Its initial missing deep-SAST result is historical evidence, not a pass;
a fresh hosted collection after merge is required to verify this provider with
the updated trusted runtime and workflow token permissions. The provider does
not fill changed-code coverage, platform secret protection, or dependency
remediation gaps. All checks remain optional and the polyglot workflow remains
manual; only Application acceptance is separately required by GitHub.

### Snyk CI

The consumer-owned `Snyk` workflow runs on pull requests, pushes to main, and manual dispatch. Its `Snyk Open Source` check scans only the application root npm lockfile, including development dependencies; it does not scan the polyglot examples’ dependency graphs; `Snyk Code` scans source. Both use the SHA-256-verified native Snyk CLI `1.1307.4`, the exact PR head, and the repository's `SNYK_TOKEN` Actions secret. High or critical findings fail the relevant check. Authentication errors, quota exhaustion, missing credentials, and unsupported scans cannot pass. Fork PRs report blocked without checking out or scanning their code.

These checks are advisory and are not required for merge. CodeQL remains the authoritative deep-SAST provider. Snyk is not yet activated in the Proof policy; installing this workflow alone does not change the scorecard or prove a scan passed. Each run has a summary and, when the CLI produces one, a JSON artifact. A clean Snyk Code scan may omit its JSON output. Source and dependency data are sent to Snyk for analysis.

No application dependencies or lifecycle scripts are installed or executed by this workflow. Open Source analysis requires regular root manifest and lockfile files, and uses the fixed lockfile path without recursive project discovery. The repository secret trusts contributors who can edit same-repository workflows: this integration does not isolate credentials from malicious same-repository workflow changes. It is separate from the canonical Proof provider workflow and does not produce its run-bound provider evidence or provide its protected-environment credential isolation.

See the [Snyk workflow](../.github/workflows/snyk.yml), [dependency scan documentation](https://docs.snyk.io/developer-tools/snyk-cli/commands/test), and [code scan documentation](https://docs.snyk.io/developer-tools/snyk-cli/commands/code-test).

Run `npm run toolkit:check` from a clean commit. The wrapper makes a retained local Git snapshot, uses the full commit SHA, runs documentation validation before build installs dependencies, and stores the report under `.artifacts/toolkit/`. Docker must be running for the pinned scanners.

On the first implementation revision, scanning the populated developer workspace exposed an upstream validator limitation: it traverses dependency Markdown under `node_modules`. The clean source snapshot passed documentation validation without changing the installed validator or suppressing its results. Its scorecard was ORANGE/ALLOW: 9 of 15 advisory capabilities passed, bootstrap change scope exceeded limits, and 5 capabilities had no local producer result. CodeQL passed separately in GitHub. The initial hosted scorecard could not load the trusted runtime until the installation was merged into main; the follow-up PR verifies that producer.

## Temporary transitive security remediations

The latest reviewed Wrangler still pins Miniflare to an Undici version with newly reported security issues, so the application overrides only `miniflare@5.20261012.1-beta` to use the patched same-major Undici `7.30.1`. Remove this override when Wrangler supplies a patched dependency graph.

ESLint still uses Ajv 6, whose `uri-js` parser has no published fix for its Unicode line-separator loop. The scoped `ajv@6.15.0` override replaces that transitive parser with `fast-uri@4.2.2`; it does not replace Ajv's major version or disable schema validation. Tests exercise external schema references, invalid ESLint options, and bounded Unicode parsing. This verifies the APIs used by this lint toolchain, not universal compatibility with every `uri-js` consumer. Reassess the alias when ESLint/Ajv adopt a maintained parser upstream. Snyk continues to scan development dependencies at the existing severity threshold.

## Configured providers in the scorecard

Each scorecard check identifies its configured provider even when the evidence is missing or the check is inactive. An explicitly unselected provider is shown as **Not configured**. Older artifacts that do not report the selection show **Not reported**. Missing evidence remains a missing result; a provider label does not imply a passing scan.

Provider names link to `.proof/providers.yaml` at the evaluated revision in this public repository. **Latest reported run** links use reported authoritative evidence, restricted to GitHub Actions run, job, or check URLs in this same repository. They identify the latest reported evidence for the scorecard subject, not an unrelated latest scan. When evidence is missing, no run link is invented and the missing result remains visible.

The public scorecard uses approved built-in provider labels and a generic label for custom providers. Configuration links expose only the fixed public configuration path and evaluated revision; arbitrary private configuration and evidence payloads are not published. These display changes do not activate or enforce checks. For example, inactive dependency-vulnerability and static-quality checks retain their configured Snyk Open Source and SonarQube labels. The consumer-owned Snyk scans do not become Proof evidence producers merely because a provider is named.

## Live PR scorecard

The optional upstream publisher owns this repository’s dedicated GitHub Pages site at https://ravisingh11.github.io/ai-software-toolkit-reference-app/. Pages uses GitHub Actions; repository variables `PROOF_SCORECARD_BADGE_ENABLED=true` and `PROOF_SCORECARD_BADGE_PAGES_MODE=dedicated` activate publication. No separate credential is needed. The application itself continues to run on Cloudflare Workers.

After a Proof Scorecard run completes, the trusted default-branch publisher validates source provenance and publishes the newest acceptable PR scorecard. A six-hour reconciliation schedule recovers missed events. The public page contains aggregate counts/status, source-run metadata, a subject digest, and allowlisted built-in control and provider labels. Custom providers use a generic label. The explicit public configuration path and validated same-repository GitHub evidence links are published; raw findings and private evidence payloads remain in the source Actions reports. Publishing never changes merge enforcement or turns missing evidence into a pass. The README and app navigation link to this live report; the [v0.1.0 snapshot](verification/scorecard.md) remains historical evidence.

This installation pins Proof runtime source commit `bb4130d4a27eb2d127fc832200797c732443119a`.
The supported runtime refresh separates failed checks from unavailable evidence,
shows snapshot identity and freshness, preserves coverage workflow identity, and
explains why smaller, actionable PRs are easier for humans to review. Application
policy remains unchanged. The public dashboard displays validated aggregate
measurements and source metadata, plus the fixed public provider configuration path and validated same-repository evidence links. Private findings and arbitrary source filenames are not published.
Installed application QA skills remain unchanged.

## Optional language examples

The five [polyglot examples](../examples/polyglot/README.md) use quality helpers
from toolkit commit `bb4130d4a27eb2d127fc832200797c732443119a`, matching the installed Proof runtime.
The helper checkout remains separately recorded in `examples/polyglot/toolkit.json`.
Explicit setup refreshes its clean cached checkout to that exact revision; modified
or mismatched caches fail visibly. Setup does not change policy defaults.

`npm run toolkit:check -- --polyglot` opts the installed snapshot scanner into
native builds, real lint, conformance tests and architecture checks. Docker and
all example toolchains are needed. Scoped changed-line coverage is run separately
with `npm run polyglot:check -- --base REF`; it does not activate the legacy
full-app coverage capability. The manual `Optional polyglot examples` workflow
is advisory. Repositories decide whether to adopt any of it or require it.

## Guardrails to Proof cutover

The upgrade follows the upstream [migration guide](https://github.com/ravisingh11/ai-software-toolkit/blob/bb4130d4a27eb2d127fc832200797c732443119a/docs/proof/migrating-from-guardrails.md): preserve policy and repository mappings, reinstall canonical runtime/workflows under `.proof/`, and copy the existing repository command/provider variables to `PROOF_*`. Legacy variables are retained while older open branches still use them. The only required check remains Application acceptance; the five-language workflow remains manual and optional.

The first migration PR retained only the unchanged `.guardrails/policy.yaml` as temporary data for the old trusted default-branch scorecard. After the Proof workflows reached main, the follow-up removed that bridge. No legacy runtime directory remains. Refreshing the public runtime and selected-skill installers at the pinned revision produces no changes. Application-specific generated QA skills are preserved.

## Repeated PR-size evidence

The collector accepts repeated trusted PR-size observations only when every matching run passes the existing provenance checks and reports identical metrics for the same PR revision and base. It retains the validated observations and chooses a deterministic latest run link. Conflicting, malformed, missing, or untrusted evidence remains unverified; no arbitrary latest result overrides a disagreement. Actual scope-limit failures remain visible advisory failures. This refresh does not activate checks or change enforcement.

## Snapshot freshness

The scorecard checks its displayed snapshot against the newest published snapshot
on load, when returning to the tab, and periodically while visible. A newer
published snapshot shows a refresh action; the page preserves the current check
anchor when refreshing. A failed freshness check remains explicit, and results
are never silently replaced or treated as current when the check cannot complete.
This detects publication changes, not unreported CI results. Missing evidence
stays visible and all Proof checks remain optional.

## Optional lifecycle verification

The supported installer installs the manual `lifecycle-verification.yml`
workflow and provenance-checking collector. The repository-owned
`.proof/lifecycle.json` and `examples/lifecycle/` fixture are preserved on refresh.
The lifecycle runtime is pinned to the reviewed, merged upstream revision
`bb4130d4a27eb2d127fc832200797c732443119a`. All three adoption pins agree.

The runtime and manual workflow reached the trusted main branch in PR #36.
IaC is now selected advisory for change evaluation; container vulnerability,
artifact SBOM, artifact vulnerability/provenance, deployment policy, DAST,
runtime assurance and runtime soak are selected advisory for release evaluation.
These optional choices do not add required checks or change branch protection.
During this adoption bootstrap, fresh accepted lifecycle evidence remains pending;
selection is not a pass.
The repository's non-secret
`PROOF_LIFECYCLE_ENABLED=true` setting explicitly opts PR collection into importing
verified manual-run receipts after this configuration and trusted runtime merge.

Dispatch `Lifecycle Verification` from main against an open same-repository PR
number and its full current head SHA. A fresh PR scorecard event after completion
imports only provenance-checked receipts. A PR changing trusted lifecycle files
needs those changes merged before its new producer can supply accepted evidence.
Do not weaken that boundary or relabel an initial missing snapshot as passed.

The fixture builds with the locked dependencies inside Docker using explicit
`build_network: default`, which allows outbound build dependency retrieval and
is not a registry-only firewall. Dependency install scripts are disabled. The
runtime stays on an internal network without credentials or host source mounts,
with a read-only root, non-root user and ephemeral local D1. Health reads the real
schema and returns the source SHA. Negative probes require unauthenticated issue
and session reads to return 401. The 30-second workload is a short endurance
smoke; runtime/container evidence describes this local verification environment,
not production Worker deployment, approvals or telemetry.

Configuration regression tests pass locally. After an initial local Docker disk
failure, [hosted lifecycle run 39340897859](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39340897859)
built and ran the actual Worker at `e0b588854d0989b43a27ee64396ccea938354159`:
429 probes over 30 seconds, zero errors. Trivy reported 68 high/critical entries;
ZAP was blocked by the upstream report-path bug. These historical findings remain
visible, independently of the orchestration workflow succeeding.
[Hosted scorecard 39341694688](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39341694688)
verified the signed artifact/environment bindings and accepted artifact provenance
(13/17 advisory controls passed). Other new lifecycle controls remained inactive
under the trusted base policy.

The updated verification image ran in [diagnostic 39345279160](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39345279160)
at `694b81751f5c8df46fdbb91818acd017f2446ba6`, using trusted workflow/base
`5ae91e812042fee3b27f01a284d808cfbcaa7d94`. The real Worker completed 432 probes
over 30.18 seconds with zero errors. Both container and SBOM scans report the
same **43 HIGH / zero CRITICAL** entries, with no fixed versions reported. They
remain failed; those are 43 findings represented twice, not 86 unique findings.
The protected fixture differs from the trusted baseline, so these are raw
diagnostics, not accepted scorecard evidence. Merge the reviewed fixture first,
then collect a fresh default-branch producer run. ZAP remains blocked in this
historical diagnostic; verification with the installed fix is pending during this bootstrap phase.
The live scorecard identifies later accepted snapshots and their exact source runs.

At [PR #39 verification](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39353272529),
CodeQL default-setup evidence was unverified: its configuration API required
repository Administration read access beyond the workflow token, and the optional
configuration credential was absent. The installed collector supports that
narrowly scoped read; successful native analyses alone do not satisfy provenance.
Missing evidence remains visible. No Snyk finding is ignored or suppressed; the
existing picomatch finding remains an independent failed CI result under the
scoped rollout exception below. The polyglot workflow
is unchanged, manual and optional.

### Existing Snyk rollout exception

[PR #36 Snyk run 39339879707](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39339879707)
evaluated head `d18c7e7122c82dfbf951c89cf6fc4f0dbaf00a05` and failed for
[picomatch ReDoS SNYK-JS-PICOMATCH-21248802](https://security.snyk.io/vuln/SNYK-JS-PICOMATCH-21248802),
with no fixed release available at review, and reported exhausted monthly private
test quota. [PR #37 Snyk run 39345281350](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39345281350)
at `694b81751f5c8df46fdbb91818acd017f2446ba6` reports the same single advisory ID
and 200-test quota failure. The user explicitly authorized this rollout's reference merges with
this unchanged failure visible when all other current CI passes. This is a
scoped merge decision, not a suppression, rule change, successful scan or accepted
passing Proof evidence. Preserve fresh native Snyk results separately from
lifecycle receipts and scorecard evidence; any different failure needs review.

### ZAP warning classification adoption

The current immutable toolkit pin includes the strict mapping correction from
upstream PR #119. The real [reference run 39349413608](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39349413608)
reported one informational alert (rule10031) with ZAP's warning exit status.
The prior adapter marked the mismatch blocked; that historical result remains
unchanged. The updated adapter preserves raw alerts and handles this documented
exit/report combination without suppressing findings or relaxing provenance.
Fresh accepted evidence is pending this trusted-baseline adoption and a new
manual run. CodeQL configuration credentials were still unconfigured at the
recorded PR #39 verification; later status requires fresh hosted evidence.


### Optional CodeQL configuration credential

This credential is optional and does not make any check required. To let the
collector verify GitHub CodeQL default setup:

1. Create an expiring fine-grained GitHub personal access token scoped only to
   `ravisingh11/ai-software-toolkit-reference-app`, with repository
   **Administration: read** and the automatically included **Metadata: read**.
   Use a bounded expiration, such as 30 days; no write permission is needed.
2. Save it as the repository Actions secret `PROOF_CODEQL_CONFIGURATION_TOKEN`.
   Keep its value out of commits, PRs, logs and evidence files. The installed
   collector uses it only to read default-setup configuration; other collection
   retains the workflow token.
3. Use a fresh open PR and inspect its hosted Proof Scorecard after the managed
   CodeQL analyses finish. Confirm that accepted evidence binds the exact PR
   revision and each configured language's analysis and run. A saved secret or
   successful native analysis alone is insufficient.
4. For a full scorecard, manually dispatch Lifecycle Verification from the trusted
   default branch for that exact open PR head, then inspect the collected artifact
   and environment evidence. Missing, expired or insufficient credentials must
   remain visible as unverified evidence. Rotate or remove the secret when needed.

Consult the [live scorecard](https://ravisingh11.github.io/ai-software-toolkit-reference-app/)
for the accepted snapshot and source run. This checklist does not claim a new
successful CodeQL verification. All checks stay optional; the separate five-language
polyglot workflow stays manual and is unchanged by credential setup.
