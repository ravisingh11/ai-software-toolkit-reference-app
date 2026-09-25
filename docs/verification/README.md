# Verification evidence

The first implementation is under review. Evidence is separated by producer and immutable source binding; local results do not imply GitHub enforcement or deployment.

- [Local agent functional QA](local-qa.md): actual Codex browser/HTTP interaction with a branch-owned Worker, synthetic editor/viewer sessions. Advisory.
- Deterministic acceptance: 7 domain tests, migration validation, and API/browser regressions; GitHub Actions retains reports/traces for 14 days.
- Deployment and rollback: not yet verified. The completed release record will identify source commit, Worker version, public URL, GitHub deployment, and smoke results.
- Required-check failure/repair demonstration: not yet verified. The completed record will link the intentionally failing PR run and the repaired passing head.

Unavailable: hosted agent QA credentials, unattended deployment credentials, full changed-code line instrumentation, and artifact attestation. Secret-protection evidence needs a separate settings token; repository platform settings alone do not activate that producer.
