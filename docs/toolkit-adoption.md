# Toolkit adoption

The runtime and workflows were installed from reviewed upstream commit `6e0422ae58602db39a43cb0a7bea5b28a410aa0a` using the public `tooling/install.py --profile github` and `tooling/install-skills.sh` entrypoints. Exact commands and revision are in `toolkit.lock.json`. Application-specific generated QA skills extend the installed bootstrap.

Core and GitHub profile controls begin advisory. Application acceptance is a separate deterministic required check once proven on representative passing and failing PRs. No AI review or functional QA result is an enforced merge gate. Oversized bootstrap scope, unavailable providers, and incomplete evidence remain visible rather than changing policy to hide them.

Producer bindings: build=`npm run build`; unit tests=`npm run test:coverage`; format/lint=`npm run lint`; migrations=`npm run validate:migrations`; setup=`npm ci`. CodeQL uses JavaScript/TypeScript. Changed-code coverage is **not activated**: current coverage measures pure domain validation, while real Worker/D1 and frontend flows are verified by API/browser acceptance without line instrumentation. That test evidence must not be reported as full changed-line coverage. Artifact provenance and hosted agent QA are likewise not activated.

To upgrade, clone the toolkit at an exact reviewed commit, run its installer with `--refresh-existing` and the selected profile, refresh selected skills using the installer's merge/refresh guidance, review configuration preservation and all runtime diffs, update toolkit.lock.json and the Worker TOOLKIT_REVISION, and submit a PR. Run application acceptance, migration validation, scans, and generated local agent QA before merging. Treat a failing consumer test as an upstream compatibility signal.
