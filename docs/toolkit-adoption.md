# Toolkit adoption

The runtime and workflows were installed from reviewed upstream commit `7b8b3a1edd6a4409faaee4d359a62e5820afb749` using the public `tooling/install.py --profile github --refresh-existing --scorecard-badge` and `tooling/install-skills.sh` entrypoints. Exact commands and revision are in `toolkit.lock.json`. Application-specific generated QA skills extend the installed bootstrap.

Core and GitHub profile controls begin advisory. Application acceptance is a separate deterministic required check on main, verified with a passing implementation and an intentionally failing follow-up PR. No AI review or functional QA result is an enforced merge gate. Oversized bootstrap scope, unavailable providers, and incomplete evidence remain visible rather than changing policy to hide them.

Producer bindings: build=`npm run build`; unit tests=`npm run test:coverage`; format/lint=`npm run lint`; migrations=`npm run validate:migrations`; setup=`npm ci`. CodeQL uses JavaScript/TypeScript. Changed-code coverage is **not activated**: current coverage measures pure domain validation, while real Worker/D1 and frontend flows are verified by API/browser acceptance without line instrumentation. That test evidence must not be reported as full changed-line coverage. Artifact provenance and hosted agent QA are likewise not activated.

To upgrade, clone the toolkit at an exact reviewed commit, run its installer with `--refresh-existing` and the selected profile, refresh selected skills using the installer's merge/refresh guidance, review configuration preservation and all runtime diffs, update toolkit.lock.json and the Worker TOOLKIT_REVISION, and submit a PR. Run application acceptance, migration validation, scans, and generated local agent QA before merging. Treat a failing consumer test as an upstream compatibility signal.

## Observed consumer behavior

### Optional provider waiting

The installed scorecard supports the upstream optional-provider wait fix. Only an explicit `false` value (case-insensitive) for `SNYK_CODE_ENABLED` or `SNYK_OPEN_SOURCE_ENABLED` stops waiting for an absent matching check. Already queued or running checks still wait; other providers retain their normal wait budget. Missing selected evidence remains `no_result`, with its existing advisory or enforced policy outcome. The setting does not deactivate a control or manufacture a pass.

The dependency-vulnerability control is not activated in this consumer’s Proof policy, although the default Snyk Open Source provider binding remains configured. These hints do not activate a control. Its independent consumer-owned Snyk workflow continues to report its own scans. Each repository decides which checks to adopt and enforce.

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

The public scorecard uses approved built-in provider labels and a generic label for custom providers, keeping private configuration out of the published page. These display changes do not activate or enforce checks. For example, inactive dependency-vulnerability and static-quality checks retain their configured Snyk Open Source and SonarQube labels. The consumer-owned Snyk scans do not become Proof evidence producers merely because a provider is named.

## Live PR scorecard

The optional upstream publisher owns this repository’s dedicated GitHub Pages site at https://ravisingh11.github.io/ai-software-toolkit-reference-app/. Pages uses GitHub Actions; repository variables `PROOF_SCORECARD_BADGE_ENABLED=true` and `PROOF_SCORECARD_BADGE_PAGES_MODE=dedicated` activate publication. No separate credential is needed. The application itself continues to run on Cloudflare Workers.

After a Proof Scorecard run completes, the trusted default-branch publisher validates source provenance and publishes the newest acceptable PR scorecard. A six-hour reconciliation schedule recovers missed events. The public page contains only aggregate counts/status, source-run metadata, and a subject digest; detailed controls and evidence remain in Actions. Publishing never changes merge enforcement or turns missing evidence into a pass. The README and app navigation link to this live report; the [v0.1.0 snapshot](verification/scorecard.md) remains historical evidence.

This installation pins Proof runtime source commit `7b8b3a1edd6a4409faaee4d359a62e5820afb749`.
The supported runtime refresh separates failed checks from unavailable evidence,
shows snapshot identity and freshness, preserves coverage workflow identity, and
explains why smaller, actionable PRs are easier for humans to review. Application
policy remains unchanged. The public dashboard displays validated aggregate
measurements and source metadata; no filenames or private findings are published.
Installed application QA skills remain unchanged.

## Optional language examples

The five [polyglot examples](../examples/polyglot/README.md) use quality helpers
from toolkit commit `7b8b3a1edd6a4409faaee4d359a62e5820afb749`, matching the installed Proof runtime.
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

The upgrade follows the upstream [migration guide](https://github.com/ravisingh11/ai-software-toolkit/blob/7b8b3a1edd6a4409faaee4d359a62e5820afb749/docs/proof/migrating-from-guardrails.md): preserve policy and repository mappings, reinstall canonical runtime/workflows under `.proof/`, and copy the existing repository command/provider variables to `PROOF_*`. Legacy variables are retained while older open branches still use them. The only required check remains Application acceptance; the five-language workflow remains manual and optional.

The first migration PR retained only the unchanged `.guardrails/policy.yaml` as temporary data for the old trusted default-branch scorecard. After the Proof workflows reached main, the follow-up removed that bridge. No legacy runtime directory remains. Refreshing the public runtime and selected-skill installers at the pinned revision produces no changes. Application-specific generated QA skills are preserved.
