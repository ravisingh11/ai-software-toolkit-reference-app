# Verification evidence

The live demo is at https://ai-software-toolkit-reference-app.navivision-account.workers.dev. `/api/health` exposes the serving Git revision, toolkit pin, Worker version, and database readiness.

- [Readable toolkit scorecard](scorecard.md): the v0.1.0 CI snapshot, including all 15 advisory controls, missing evidence, evaluated commit, and source run. New CI runs publish their own Actions summaries; this repository snapshot is versioned separately.
- [Implementation PR](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/1): 7 domain tests, 6 API/browser tests, migrations, build/lint, CodeQL, Gitleaks, and Semgrep passed. The initial trusted scorecard was unavailable before its runtime existed on main.
- [Local agent functional QA](local-qa.md): actual Codex browser/HTTP interactions with a branch-owned Worker, separate from automated tests. Source SHA-256 binding included. Advisory.
- [Gate demonstration and operational follow-up](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/5): the deliberately incorrect test at `3c91ec0` [failed acceptance](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/36139189519). With Application acceptance required on main, GitHub reported BLOCKED. The repair removes the negative control and retains the correct transition policy. Passing-head evidence is captured in the release record.
- [Release record](https://github.com/ravisingh11/ai-software-toolkit-reference-app/releases/tag/v0.1.0): published after live verification, with exact source commit, Worker versions, GitHub deployment, sanitized smoke/rollback evidence, and gate run links. Use that immutable record for completion claims.

The initial Worker upload succeeded but cron installation hit the account limit. The follow-up replaces cron cleanup with deletion of expired records on the next demo creation. It does not upgrade the account or alter existing applications.

Unavailable: hosted agent QA credentials, unattended deployment credentials, full changed-code line instrumentation, and artifact attestation. The GitHub secret-protection and Dependabot evidence probes need a separate settings token; platform settings alone do not activate those producers. These are not passed checks.
