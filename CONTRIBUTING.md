# Contributing

Use Node 24, `npm ci`, `npm run db:local`, and `npm run dev`. Run the checks in AGENTS.md before a pull request. See docs/design.md for the API and permission contract. Use synthetic data only.

Work on a branch and submit a PR. Functional QA runs against that checkout's local Worker and D1 database. The live demo is only a release smoke target. Update canonical documentation when behavior changes. Do not modify the installed toolkit runtime to suppress a finding; propose upstream fixes and adopt a reviewed toolkit revision.
