# Toolkit adoption

The runtime and workflows were installed from reviewed upstream commit `9f08989980f9a5a828925d537692e8c502ccee14` using the public `tooling/install.py --profile github --refresh-existing --scorecard-badge` and `tooling/install-skills.sh` entrypoints. Exact commands and revision are in `toolkit.lock.json`. Application-specific generated QA skills extend the installed bootstrap.

Core and GitHub profile controls begin advisory. Application acceptance is a separate deterministic required check on main, verified with a passing implementation and an intentionally failing follow-up PR. No AI review or functional QA result is an enforced merge gate. Oversized bootstrap scope, unavailable providers, and incomplete evidence remain visible rather than changing policy to hide them.

Producer bindings: build=`npm run build`; unit tests=`npm run test:coverage`; format/lint=`npm run lint`; migrations=`npm run validate:migrations`; setup=`npm ci`. CodeQL uses JavaScript/TypeScript. Changed-code coverage is **not activated**: current coverage measures pure domain validation, while real Worker/D1 and frontend flows are verified by API/browser acceptance without line instrumentation. That test evidence must not be reported as full changed-line coverage. Artifact provenance and hosted agent QA are likewise not activated.

To upgrade, clone the toolkit at an exact reviewed commit, run its installer with `--refresh-existing` and the selected profile, refresh selected skills using the installer's merge/refresh guidance, review configuration preservation and all runtime diffs, update toolkit.lock.json and the Worker TOOLKIT_REVISION, and submit a PR. Run application acceptance, migration validation, scans, and generated local agent QA before merging. Treat a failing consumer test as an upstream compatibility signal.

## Observed consumer behavior

Run `npm run toolkit:check` from a clean commit. The wrapper makes a retained local Git snapshot, uses the full commit SHA, runs documentation validation before build installs dependencies, and stores the report under `.artifacts/toolkit/`. Docker must be running for the pinned scanners.

On the first implementation revision, scanning the populated developer workspace exposed an upstream validator limitation: it traverses dependency Markdown under `node_modules`. The clean source snapshot passed documentation validation without changing the installed validator or suppressing its results. Its scorecard was ORANGE/ALLOW: 9 of 15 advisory capabilities passed, bootstrap change scope exceeded limits, and 5 capabilities had no local producer result. CodeQL passed separately in GitHub. The initial hosted scorecard could not load the trusted runtime until the installation was merged into main; the follow-up PR verifies that producer.

## Live PR scorecard

The optional upstream publisher owns this repository’s dedicated GitHub Pages site at https://ravisingh11.github.io/ai-software-toolkit-reference-app/. Pages uses GitHub Actions; repository variables `GUARDRAILS_SCORECARD_BADGE_ENABLED=true` and `GUARDRAILS_SCORECARD_BADGE_PAGES_MODE=dedicated` activate publication. No separate credential is needed. The application itself continues to run on Cloudflare Workers.

After a Guardrail Scorecard run completes, the trusted default-branch publisher validates source provenance and publishes the newest acceptable PR scorecard. A six-hour reconciliation schedule recovers missed events. The public page contains only aggregate counts/status, source-run metadata, and a subject digest; detailed controls and evidence remain in Actions. Publishing never changes merge enforcement or turns missing evidence into a pass. The README and app navigation link to this live report; the [v0.1.0 snapshot](verification/scorecard.md) remains historical evidence.

This upgrade pins metric-fidelity reporting source commit `9f08989980f9a5a828925d537692e8c502ccee14`.
The supported runtime refresh separates failed checks from unavailable evidence,
shows snapshot identity and freshness, preserves coverage workflow identity, and
explains why smaller, actionable PRs are easier for humans to review. Application
policy remains unchanged. The public dashboard displays validated aggregate
measurements and source metadata; no filenames or private findings are published.
Installed application QA skills remain unchanged.
