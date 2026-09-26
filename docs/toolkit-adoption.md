# Toolkit adoption

The runtime and workflows were installed from reviewed upstream commit `75207e17a06cdc16ace777571cac2e9f4eaceef1` using the public `tooling/install.py --profile github --refresh-existing --scorecard-badge` and `tooling/install-skills.sh` entrypoints. Exact commands and revision are in `toolkit.lock.json`. Application-specific generated QA skills extend the installed bootstrap.

Core and GitHub profile controls begin advisory. Application acceptance is a separate deterministic required check on main, verified with a passing implementation and an intentionally failing follow-up PR. No AI review or functional QA result is an enforced merge gate. Oversized bootstrap scope, unavailable providers, and incomplete evidence remain visible rather than changing policy to hide them.

Producer bindings: build=`npm run build`; unit tests=`npm run test:coverage`; format/lint=`npm run lint`; migrations=`npm run validate:migrations`; setup=`npm ci`. CodeQL uses JavaScript/TypeScript. Changed-code coverage is **not activated**: current coverage measures pure domain validation, while real Worker/D1 and frontend flows are verified by API/browser acceptance without line instrumentation. That test evidence must not be reported as full changed-line coverage. Artifact provenance and hosted agent QA are likewise not activated.

To upgrade, clone the toolkit at an exact reviewed commit, run its installer with `--refresh-existing` and the selected profile, refresh selected skills using the installer's merge/refresh guidance, review configuration preservation and all runtime diffs, update toolkit.lock.json and the Worker TOOLKIT_REVISION, and submit a PR. Run application acceptance, migration validation, scans, and generated local agent QA before merging. Treat a failing consumer test as an upstream compatibility signal.

## Observed consumer behavior

### Snyk CI

The consumer-owned `Snyk` workflow runs on pull requests, pushes to main, and manual dispatch. Its `Snyk Open Source` check scans the npm manifest and lockfile, including development dependencies; `Snyk Code` scans source. Both use Snyk CLI `1.1307.4`, the exact PR head, and the repository's `SNYK_TOKEN` Actions secret. High or critical findings fail the relevant check. Authentication errors, quota exhaustion, missing credentials, and unsupported scans cannot pass. Fork PRs report blocked without checking out or scanning their code.

These checks are advisory and are not required for merge. CodeQL remains the authoritative deep-SAST provider. Snyk is not yet activated in the Guardrails policy; installing this workflow alone does not change the scorecard or prove a scan passed. Each run has a summary and, when the CLI produces one, a JSON artifact. A clean Snyk Code scan may omit its JSON output. Source and dependency data are sent to Snyk for analysis.

See the [Snyk workflow](../.github/workflows/snyk.yml), [dependency scan documentation](https://docs.snyk.io/developer-tools/snyk-cli/commands/test), and [code scan documentation](https://docs.snyk.io/developer-tools/snyk-cli/commands/code-test).

Run `npm run toolkit:check` from a clean commit. The wrapper makes a retained local Git snapshot, uses the full commit SHA, runs documentation validation before build installs dependencies, and stores the report under `.artifacts/toolkit/`. Docker must be running for the pinned scanners.

On the first implementation revision, scanning the populated developer workspace exposed an upstream validator limitation: it traverses dependency Markdown under `node_modules`. The clean source snapshot passed documentation validation without changing the installed validator or suppressing its results. Its scorecard was ORANGE/ALLOW: 9 of 15 advisory capabilities passed, bootstrap change scope exceeded limits, and 5 capabilities had no local producer result. CodeQL passed separately in GitHub. The initial hosted scorecard could not load the trusted runtime until the installation was merged into main; the follow-up PR verifies that producer.

## Live PR scorecard

The optional upstream publisher owns this repository’s dedicated GitHub Pages site at https://ravisingh11.github.io/ai-software-toolkit-reference-app/. Pages uses GitHub Actions; repository variables `GUARDRAILS_SCORECARD_BADGE_ENABLED=true` and `GUARDRAILS_SCORECARD_BADGE_PAGES_MODE=dedicated` activate publication. No separate credential is needed. The application itself continues to run on Cloudflare Workers.

After a Guardrail Scorecard run completes, the trusted default-branch publisher validates source provenance and publishes the newest acceptable PR scorecard. A six-hour reconciliation schedule recovers missed events. The public page contains only aggregate counts/status, source-run metadata, and a subject digest; detailed controls and evidence remain in Actions. Publishing never changes merge enforcement or turns missing evidence into a pass. The README and app navigation link to this live report; the [v0.1.0 snapshot](verification/scorecard.md) remains historical evidence.

This upgrade advances the pin from `6e0422ae58602db39a43cb0a7bea5b28a410aa0a` to the reviewed formatting release `75207e17a06cdc16ace777571cac2e9f4eaceef1`. The supported refresh preserves application policy and adds the publisher workflow plus its two runtime files. The installed skills are unchanged between those upstream revisions.
