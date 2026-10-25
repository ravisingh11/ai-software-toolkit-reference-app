# Contributing

Use Node 24, `npm ci`, `npm run db:local`, and `npm run dev`. Start with [workspace and skill onboarding](docs/onboarding.md) and the
[task-to-skill map](AGENTS.md#choose-a-skill-for-the-task). Follow the user's execution limits: when local checks or QA are excluded, use hosted
Application acceptance and report local verification as not run. Otherwise, run
the applicable checks in AGENTS.md before a pull request. See docs/design.md for the API and permission contract. Use synthetic data only.

Work on a branch and submit a PR. Functional QA runs against that checkout's local Worker and D1 database. The live demo is only a release smoke target. Update canonical documentation when behavior changes. Do not modify the installed toolkit runtime to suppress a finding; propose upstream fixes and adopt a reviewed toolkit revision.

For changes to `examples/polyglot/` or its runner, follow the setup and checks in
[the polyglot guide](examples/polyglot/README.md). Verify the harness with
`python3 -m unittest discover -s scripts/tests`. Commit before scoped changed-line
coverage, supply the intended comparison base, and retain `.artifacts/polyglot/`
results for review. Adoption and merge enforcement remain repository decisions.

Toolkit checks remain optional to adopt and enforce; Core and functional QA stay
advisory. Lifecycle and polyglot workflows run only by explicit manual dispatch;
this guide does not authorize running them for every documentation change.
