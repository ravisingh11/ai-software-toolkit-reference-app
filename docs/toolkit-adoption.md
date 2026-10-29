# Toolkit adoption

The runtime and selected skills are pinned to published [toolkit v2.3.3](https://github.com/ravisingh11/ai-software-toolkit/releases/tag/v2.3.3)
at immutable upstream commit `248d8f02e774e4f75af6ea2de49b466688dfae54`.
This patch packages the separate PR/main checkpoint report examples and authentic
README screenshot. The app already adopted the same canonical page renderer;
staged refresh produces no runtime, skill or workflow differences. Its existing
policies, optional selections, manual lifecycle/polyglot triggers, generated app
QA and required Application acceptance workflow are preserved. Installer and CLI
version 2.3.3 are recorded in the custom provenance lock. Historical refresh,
renderer, deployment, skill and hook records keep their original identities.

This repository's `toolkit.lock.json` is application-owned provenance, not the
CLI managed-file inventory, and it has no `toolkit.toml`. Refresh in a tracked-source
staging directory with this provenance record excluded, using
`tooling/install.py --profile github --refresh-existing --scorecard-badge` and the
selected standalone skill installer. Review and apply only generated runtime,
workflow and selected-skill changes; then update provenance, helper and Worker
source pins together. Do not point CLI `init`/`update` at this custom lock or
silently migrate it to the CLI schema.

Core and GitHub profile controls begin advisory. Application acceptance is a separate deterministic required check on main, verified with a passing implementation and an intentionally failing follow-up PR. No AI review or functional QA result is an enforced merge gate. Oversized bootstrap scope, unavailable providers, and incomplete evidence remain visible rather than changing policy to hide them.

Producer bindings: build=`npm run build`; unit tests=`npm run test:coverage`; format/lint=`npm run lint`; migrations=`npm run validate:migrations`; setup=`npm ci`. CodeQL default setup analyzes its configured Actions, JavaScript/TypeScript, and Python languages. Changed-code coverage is selected advisory by the Core profile but remains **unverified**: current coverage measures pure domain validation, while real Worker/D1 and frontend flows are verified by API/browser acceptance without line instrumentation. That test evidence must not be reported as full changed-line coverage. Artifact provenance belongs to the app’s optional release/lifecycle example and is excluded from ordinary PR scoring; hosted agent QA is available to adopt.

To upgrade, obtain the exact reviewed release, follow the staging procedure above, refresh selected skills with the supported installer, review configuration preservation and generated diffs, align all source pins, and submit a PR. Follow task execution limits: when local testing is excluded, verify required hosted Application acceptance instead of running local tests or agent QA. A failing consumer check is an upstream compatibility signal.

## Selected Codex skills

The [workspace guide](onboarding.md) adapts the upstream onboarding and routing
cleanup from [toolkit PR #156](https://github.com/ravisingh11/ai-software-toolkit/pull/156).
The initial documentation/selected-skill adoption used published v2.3.0, with
no runtime or deployment change. The subsequent recorded v2.3.1 refresh below adopts the
published patch and retains these skill contents and task routes.

The existing installation now includes all seven starter skills plus `docs-sync`
and the app's existing maintenance and generated QA skills. Three previously
absent starter skills (`toolkit-setup`, `code-review`, `dependency-risk-review`)
and `docs-sync` were added from the v2.3.0 source with the supported
standalone installer, preview first, using `--skip-existing`. Existing skills,
shared support and generated QA were not refreshed or replaced.

From a separate trusted toolkit checkout at the exact revision above:

```sh
bash /path/to/toolkit/tooling/install-skills.sh --client codex \
  --target /path/to/ai-software-toolkit-reference-app/.agents/skills \
  --skill toolkit-setup --skill code-review --skill dependency-risk-review \
  --skill docs-sync --skip-existing --dry-run
```

Review the preview, then remove `--dry-run` to install missing selections. This
command does not run tests, invoke a skill, install workflows or change policy.
The [AGENTS task map](../AGENTS.md#choose-a-skill-for-the-task) routes actual work.
Upstream fixture demonstrations and this app's historical QA are distinct; see
[the evidence limits](onboarding.md#what-the-evidence-establishes).

## Claude Code setup

The initial v2.1.0 upgrade refreshed onboarding and Claude guidance without
runtime, workflow, or skill differences at that time. The subsequent scorecard
refresh below updates the installed renderer and action pins.
`toolkit.lock.json`, `examples/polyglot/toolkit.json`, and the Worker
`TOOLKIT_REVISION` now identify the same immutable toolkit commit. Updating
source metadata does not update the deployed Worker or establish new scan results.

Read [CLAUDE.md](../CLAUDE.md) before working in this application. To add starter
skills for Claude Code, use a separate trusted toolkit checkout at the pinned
revision and preview the selection first:

```sh
git clone https://github.com/ravisingh11/ai-software-toolkit.git /path/to/toolkit
git -C /path/to/toolkit checkout --detach 248d8f02e774e4f75af6ea2de49b466688dfae54
bash /path/to/toolkit/tooling/install-skills.sh --client claude-code \
  --target /path/to/ai-software-toolkit-reference-app/.claude/skills \
  --skill toolkit-setup --skill prepare-safe-change --skill code-review \
  --skill test-gap-finder --skill security-audit-lite \
  --skill dependency-risk-review --skill qa-bootstrap --dry-run
```

After reviewing the preview, replace `--dry-run` with `--merge-existing` to copy
missing files while preserving customized skills. This standalone selection
installs skills into `.claude/skills/` without creating CLI configuration or installing Proof
workflows or running checks. For both clients, run separate standalone commands using `--client codex`
and `--client claude-code`, each with its own destination. The shell installer
accepts one client per invocation; `--clients` is a CLI `init` option. This upgrade preserves the existing Codex skills and app-specific QA;
it does not install the optional Claude skill selection automatically. Keep
application instructions in this repository's CLAUDE.md; the installer does not
write that file.

For example: “Use the code-review skill to review this change. Explain risks
with file references. Do not run tests or commands unless I ask.” Review the
[versioned upstream onboarding](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.3.3/docs/quickstart.md#claude-code-setup)
and [CLI guide](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.3.3/docs/install.md).
All toolkit checks remain optional. Application acceptance remains the only
required CI check; lifecycle and polyglot workflows remain manual and optional.

## Safe skill-replacement refresh

The current pin includes upstream [PR #129](https://github.com/ravisingh11/ai-software-toolkit/pull/129),
which fixes the standalone shell skill installer's no-rsync replacement path.
It stages the complete new copy beside the destination before moving the
installed skill. Failed promotion and handled interruptions restore the original;
if restoration cannot complete, it retains the original and reports its
recovery path. Recovery is per skill, and uncatchable termination can require
manual recovery from staging.

The shell installer is used from a separate trusted toolkit checkout and is
not vendored into this app. The earlier safe skill-replacement-only refresh in PR #44
produced no runtime or workflow differences; existing skills and generated app
QA were preserved. Use the pinned checkout above when invoking
`tooling/install-skills.sh` to get the fix. The toolkit lock, optional polyglot
helper pin, and Worker source metadata agree on the new revision.

All toolkit checks remain optional, Application acceptance remains separately
required, and polyglot stays manual (`workflow_dispatch`). This source update
neither runs the polyglot examples nor deploys the Worker.

## Scorecard wording refresh

Upstream [PR #128](https://github.com/ravisingh11/ai-software-toolkit/pull/128)
clarifies the published HTML and Markdown summaries. **Selected checks** counts
advisory and enforced checks selected for the evaluation, without claiming
execution. Failed, blocked, and unverified outcomes remain distinct. Reported
inactive checks are shown separately and excluded from the selected total;
this can include checks evaluated on another subject. A missing row is not
assumed inactive, and inconsistent evidence does not acquire fabricated counts.
An empty enforcement set says **No checks enforced**.

The supported installer refresh also carries the synchronized upstream action
updates: `actions/attest` v4.2.2 and `sigstore/cosign-installer` v4.1.2. The
lifecycle workflow retains `cosign-release: v2.6.0`; installer v4 supports it.
No producer, policy mode, permissions, workflow triggers, required checks, or
application-specific QA skills are changed. All toolkit checks remain optional;
Application acceptance stays separately required, and polyglot remains manual.

The published page uses the trusted default-branch renderer on its next
successful publication. Source installation alone does not prove publication,
a new scan, or a Worker deployment.

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

The latest reviewed Wrangler still pins Miniflare to an Undici version with newly reported security issues, so the application overrides only `miniflare@5.20261019.0-beta` to use the patched same-major Undici `7.30.1`. Remove this override when Wrangler supplies a patched dependency graph.

ESLint still uses Ajv 6, whose `uri-js` parser has no published fix for its Unicode line-separator loop. The scoped `ajv@6.15.0` override replaces that transitive parser with `fast-uri@4.2.2`; it does not replace Ajv's major version or disable schema validation. Tests exercise external schema references, invalid ESLint options, and bounded Unicode parsing. This verifies the APIs used by this lint toolchain, not universal compatibility with every `uri-js` consumer. Reassess the alias when ESLint/Ajv adopt a maintained parser upstream. Snyk continues to scan development dependencies at the existing severity threshold.

## Configured providers in the scorecard

Each scorecard check identifies its configured provider even when the evidence is missing or the check is inactive. An explicitly unselected provider is shown as **Not configured**. Older artifacts that do not report the selection show **Not reported**. Missing evidence remains a missing result; a provider label does not imply a passing scan.

Provider names link to `.proof/providers.yaml` at the evaluated revision in this public repository. **Latest reported run** links use reported authoritative evidence, restricted to GitHub Actions run, job, or check URLs in this same repository. They identify the latest reported evidence for the scorecard subject, not an unrelated latest scan. When evidence is missing, no run link is invented and the missing result remains visible.

The public scorecard uses approved built-in provider labels and a generic label for custom providers. Configuration links expose only the fixed public configuration path and evaluated revision; arbitrary private configuration and evidence payloads are not published. These display changes do not activate or enforce checks. For example, inactive dependency-vulnerability and static-quality checks retain their configured Snyk Open Source and SonarQube labels. The consumer-owned Snyk scans do not become Proof evidence producers merely because a provider is named.

## Live PR scorecard

The optional upstream publisher owns this repository’s dedicated GitHub Pages site at https://ravisingh11.github.io/ai-software-toolkit-reference-app/. Pages uses GitHub Actions; repository variables `PROOF_SCORECARD_BADGE_ENABLED=true` and `PROOF_SCORECARD_BADGE_PAGES_MODE=dedicated` activate publication. No separate credential is needed. The application itself continues to run on Cloudflare Workers.

After a Proof Scorecard run completes, the trusted default-branch publisher validates source provenance and publishes the newest acceptable PR scorecard. A six-hour reconciliation schedule recovers missed events. The public page contains aggregate counts/status, source-run metadata, a subject digest, and allowlisted built-in control and provider labels. Custom providers use a generic label. The explicit public configuration path and validated same-repository GitHub evidence links are published; raw findings and private evidence payloads remain in the source Actions reports. Publishing never changes merge enforcement or turns missing evidence into a pass. The README and app navigation link to this live report; the [v0.1.0 snapshot](verification/scorecard.md) remains historical evidence.

The earlier installation pinned Proof runtime source commit `bb4130d4a27eb2d127fc832200797c732443119a`; the current reviewed pin is recorded in toolkit.lock.json and the stage-specific refresh below.
The supported runtime refresh separates failed checks from unavailable evidence,
shows snapshot identity and freshness, preserves coverage workflow identity, and
explains why smaller, actionable PRs are easier for humans to review. Application
policy remains unchanged. The public dashboard displays validated aggregate
measurements and source metadata, plus the fixed public provider configuration path and validated same-repository evidence links. Private findings and arbitrary source filenames are not published.
Installed application QA skills remain unchanged.

## Optional language examples

The five [polyglot examples](../examples/polyglot/README.md) use quality helpers
from toolkit v2.2.1 commit `bf05798e4b03610551f9882620767f31de03d1df`, matching the installed Proof runtime.
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
The current runtime is pinned to published v2.3.3 upstream revision
`248d8f02e774e4f75af6ea2de49b466688dfae54`. The toolkit lock, optional helper pin and Worker source metadata agree.

The runtime and manual workflow reached the trusted main branch in PR #36.
That historical bootstrap selected IaC advisory for change evaluation; container vulnerability,
artifact SBOM, artifact vulnerability/provenance, deployment policy, DAST,
runtime assurance and runtime soak are selected advisory for release evaluation.
These optional choices do not add required checks or change branch protection.
During this adoption bootstrap, fresh accepted lifecycle evidence remains pending;
selection is not a pass.
The repository's non-secret
`PROOF_LIFECYCLE_ENABLED=true` setting enables lifecycle receipt support.
Import into an explicit lifecycle evaluation additionally requires
`PROOF_SCORECARD_STAGE=lifecycle`; ordinary PR development no longer imports
artifact/environment companions. This does not dispatch the manual producer.

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

## Historical stage-specific selection and adoption refresh

The supported installer was run from the exact merged upstream source revision
`4706e359dd1478036457613e6c7dd2a23466985d` (upstream PR #141):

```sh
python3 /path/to/reviewed-toolkit/tooling/install.py --target /path/to/ai-software-toolkit-reference-app --profile github --refresh-existing --scorecard-badge
```

The renderer, reconciler, GitHub evidence collector and scorecard workflow changed;
other generated runtime files stayed identical. Application-owned commands,
provider selections (including managed CodeQL), lifecycle fixtures, and generated
QA skills were preserved. No local tests, dependency installation, agent QA, or
Worker deployment were run for this refresh; required CI provides validation.

Ordinary **pull-request development** selects the existing Core/GitHub profile's
16 checks, all advisory. The old change-stage IaC override was removed because
its producer belongs to the manual verification fixture; IaC remains available
to adopt, not a missing PR requirement. The app's explicit advisory release
example choices are preserved for an intentional lifecycle evaluation. No
release/environment receipt is imported into an ordinary PR score merely because
lifecycle support is enabled.

The public report shows **Selected checks**, **Tools available to adopt** (9), and
**Checks relevant later** (8), with optional setup steps and stage descriptions.
Only policy-selected checks applicable to the actual evaluation enter the score.
A selected failure, blocker, or unavailable result is never moved into discovery
to improve the score. Incomplete selection remains unknown. Historical snapshots
retain their original counts, policy, and evaluation scope.

Advisory/Enforced remains a separate mode. Enforced checks require a passing
result; GitHub independently requires Application acceptance. The selected Core
coverage control still lacks full changed-line instrumentation, and missing
security-settings proof stays visible. The independent Snyk finding example is
preserved. Polyglot and lifecycle workflows remain manual (`workflow_dispatch`).

The Pages publisher uses the trusted renderer after merge and fresh evidence
collection. A changed source pin does not update the deployed Worker; its health
metadata continues describing the previously deployed revision until an authorized
deployment. No toolkit release or application deployment is part of this update.


## Historical full 33-check overview refresh

The supported installer refreshed the installed runtime and managed workflows
from reviewed upstream commit `3997edd64e32cfc6412526000e6613ff7fa5ab36`
(upstream PR #144). At that refresh, the toolkit lock, optional polyglot helper pin, and Worker
source metadata identified that same immutable revision. The recorded 2.1.1
version referred to the CLI; the current lock distinguishes it from the standalone
installer version. Previously installed skills and generated application QA skills are
preserved.

The live Pages report now has an always-visible **All 33 checks** overview above
its results. Each name links to its detail card. Selected, available-to-adopt,
and relevant-later groups use validated snapshot selection; unknown selection
and separate evaluation context remain explicit. Selected failures stay selected,
and only selected applicable checks enter the score. The overview stacks on mobile.

This supported refresh also installs the upstream independent provenance and
Trivy starters and their provider definitions. Their opt-in variables and provider
selections are not enabled by this refresh. Application policy and existing
provider selections, the consumer-owned Snyk workflow and its visible finding
example, and lifecycle fixtures remain unchanged. Lifecycle and polyglot remain
manual. GitHub still requires only Application acceptance.

No extra local tests, scans, dependency installation, agent QA, Worker deployment,
or release publication were run for this update. Required hosted CI validates the
PR. Updating Worker source metadata does not change the deployed application's
health revision. The Pages renderer update presents historical PR evidence without
rerunning its producers or applying newer policy to old results.

## Published v2.2.1 alignment

The supported installer was run from exact tag commit `bf05798e4b03610551f9882620767f31de03d1df`.
Its generated runtime and workflows are unchanged from the preceding reviewed
pin. This update aligns the toolkit lock, optional helper pin, Worker source
metadata, README, and Claude guidance with the published release. It preserves
app-specific provider configuration, advisory policy, generated QA skills,
manual polyglot/lifecycle triggers, dependencies and the intentional independent
Snyk failure example. Historical reports and deployed Worker metadata are not
relabelled as current verification. No Worker deployment is part of this update.

The v2.2.1 upstream patch renames the composite action to AI Software Toolkit
Proof Attestation and advances the CLI version. This application continues to
consume its pinned installed runtime; it does not add a new action invocation,
activate providers or make toolkit checks mandatory.


## Published v2.3.0 refresh

The published release resolves to `9108f2fda1cc04087cb1326e0457302fab214f3c`. Its canonical
standalone installer and the previously selected six skills were refreshed in
staging, retaining this application's custom provenance-lock format. Generated
changes are limited to `.proof/activation.py`, `.proof/doctor.py`,
`.proof/validators/validate_documentation.py`, and the specification-driven skill.
Installer/CLI version reporting now agrees at 2.3.0. The lock, optional polyglot
helper pin, Worker source metadata, README and Claude guidance agree on the source.

The [33-check activation index](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.3.0/docs/activation.md)
distinguishes installation, selection, configuration, execution and verified
evidence. Read-only doctor adds per-check setup/evidence guidance; it does not
execute producers or activate checks. Documentation validation uses Git-tracked
files, with dependency/generated exclusions for non-Git source snapshots, and
missing configuration or comparison baselines remain failures.

The new starter defaults apply to fresh CLI installations. This existing app
retains its Core/GitHub selections, all existing workflows, app-owned mappings,
lifecycle fixtures, generated QA, and consumer-owned Snyk failure example. No
Claude directories or extra skills are adopted. Spec Kit is optional and separate;
no preset is installed. Lifecycle and polyglot triggers remain manual and optional.
Application acceptance remains the separate required merge check.

No extra local tests, dependency setup, scans, agent QA, provider activation,
branch-protection changes or Worker deployment are part of this refresh. The
deployment report at that source-only refresh was the historical v2.2.1
deployment; updating the source pin alone did not change the running application.
The subsequent [v2.3.0 live deployment verification](verification/deployment-v2.3.0.md)
records the actual deployed app/toolkit/Worker identity and API/browser observations.
Older deployment and CI snapshots retain their original identities.


## Published v2.3.1 refresh

The published patch resolves to `f53a167be5283c1378740f475f231aa130f3aee9`.
Its supported standalone runtime installer and ten selected canonical skills
were refreshed in tracked-source staging without the app-owned provenance lock.
Only generated differences were applied. The runtime and installed skill bytes
are unchanged; the repository-validation and unit-test workflow templates now
include the canonical conditional source-history checkout. This app has no
`tooling/validate-skills.py`, so that extra checkout is skipped here.

The lock, optional polyglot helper pin, Worker source variable/type, README,
Claude guidance and onboarding guide identify the same published source. The
historical `skillAdditions` record retains its original v2.3.0 identity; the new
`skillRefresh` record identifies this refresh. Generated app-specific QA is not
replaced, and no Claude installation is added. Upstream Codex fixture evidence
does not establish a fresh agent QA run against this application.

All toolkit checks remain optional; Core and functional QA remain advisory.
Application acceptance is the separately required merge check. Lifecycle and
polyglot workflows retain manual-only triggers. No extra local tests, scanners,
agent QA, credential changes, provider activation or deployment are included.
The [latest recorded live deployment](verification/deployment-main-7d5df0a.md)
still identifies app `7d5df0a` with toolkit v2.3.0. Updating source metadata does
not update that deployed Worker or refresh its historical verification.


## Published v2.3.2 refresh

The published patch resolves to `8a36b246f6bd0c3808276de0f7794b26f574ce5e`. The source archive was downloaded
from the published release and checked against its verified manifest/checksums.
The supported standalone installers ran in tracked-source staging with this
application's custom provenance lock excluded. Only generated differences were
applied: optional CodeQL init/analyze pins advance together to v4.39.1 in the
existing workflow. This does not activate advanced CodeQL; GitHub Default Setup
remains the selected provider.

Runtime, selected skill and generated app QA bytes are unchanged. The app-owned
Application acceptance workflow, its invocation output, existing optional policy
selections, and manual-only lifecycle/polyglot triggers are preserved. The lock,
optional helper pin, Worker source variable/type, onboarding, Claude guidance and
README agree on v2.3.2. Historical v2.3.1 refresh and skill-addition identities
remain recorded separately.

Verification uses required hosted Application acceptance; no extra local tests,
scanners, agent QA, credential changes or provider activation are included.
The independent Snyk vulnerability/quota failure remains visible. Updating source
metadata does not deploy the Worker or relabel earlier deployment, skill or hook
invocation evidence. Existing deployment records retain their original subjects.

## Checkpoint page renderer adoption

The [application report](https://ravisingh11.github.io/ai-software-toolkit-reference-app/)
includes separate PR and main checkpoint examples. The initial pinned page
renderer adoption came from toolkit source `e7e1626a0bc7e3013710c8a48ad234d126c058ca`, recorded independently in
`toolkit.lock.json` under `pageRendererHistory`. At that adoption, the base toolkit
remained v2.3.2; the subsequent published refresh below aligns both pins.

The supported standalone installer ran with `--profile github
--refresh-existing --scorecard-badge` against tracked-source staging, excluding
this application's custom provenance lock. Only `.proof/render_scorecard_badge.py`
changed; only that generated difference was applied. Evaluator, policy,
provider configuration, skills and workflows retain their existing bytes.
The renderer is byte-identical to the pinned upstream source.

Historical PR #63 (`510e25a6c8f4816a35ef9f2d4d1d00f2db74cab8`) comes from
[Proof Scorecard 40879661416](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/40879661416/attempts/1).
Its metadata, size, changed-coverage and dependency-review results stay as
recorded, including failure and missing evidence. Main
`c3df3f459f14dd4a9945f4988722ebaafc804edd` comes from
[Application acceptance 40632274819](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/40632274819/attempts/1).
Its build, unit/coverage, browser and migration results are workflow observations,
not a full Proof policy score or production verification. These are different
changes, not a claim that PR #63 produced that earlier main commit.

The examples do not contribute to the live scorecard totals. The latest PR
snapshot retains its original subject, policy/runtime identity and freshness
checks. New regression coverage runs through existing hosted acceptance; no
extra local test suites, scans, agent QA, producer activation, branch-protection
changes or Worker deployment are included. Existing deployment, skill and hook
evidence remain unchanged. Checks optional, Core advisory, lifecycle/polyglot
manual. CI logs and artifacts are subject to GitHub retention.


## Published v2.3.3 refresh

The immutable release resolves to `248d8f02e774e4f75af6ea2de49b466688dfae54`. All ten published assets were
downloaded and checked against GitHub's recorded hashes; all nine SHA256SUMS
entries verify. The source and CLI hashes agree with the release manifest and
hosted distribution-verification report. These are asset-integrity checks, not
native build provenance or new application test results.

The supported standalone runtime and selected-skill installers ran in
tracked-source staging with the app-owned provenance lock excluded. Preview and
refresh produced no added, removed or changed files. In particular, the already
adopted checkpoint renderer is byte-identical to this published source. Its
current `pageRenderer` pin now agrees with the release revision; the original
pre-release adoption is retained in `pageRendererHistory`. Prior release asset
hashes and skill-refresh identities are retained separately in the lock.

The lock, optional polyglot helper, Worker source variable/type, onboarding,
Claude guidance and README identify v2.3.3. The renderer identity assertion is
updated for the published pin and runs through existing hosted acceptance.
Existing historical examples, the README screenshot, deployment verification,
real skill evidence and hook invocation records are preserved. PR #63's separate
actionable workflow reporting is not included in this update.

Verification uses required hosted Application acceptance. No extra local tests,
scanners, agent QA, credential changes, provider activation, branch-protection
changes or deployments are included. All toolkit checks remain optional, Core
stays advisory, lifecycle/polyglot execution remains manual, and missing or failed
evidence stays visible. Updating source metadata does not update the deployed
Worker or relabel an older evaluation as a result for this revision.
