# Toolkit refresh verification

The [manual optional polyglot run 39185524558](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/39185524558) passed on source `2f9ac1fcce571ed54d51b7fdf2aa50a8aadbe3b9` with a clean working tree and toolkit `c46a7c263ea7667ea9c0fe061b628afd51ed6507`. It ran on the refresh branch, before the documentation-only evidence update; it is not a deployment result.

The workflow was explicitly dispatched for `language=all`, baseline `2932827657d4758cdf030ab693239cfb2a23e258` (before the examples), and threshold `90`. All 30 stages passed: versions, build, lint, test, architecture, and scoped changed-line coverage for each language. Each language passed 23 conformance cases, 115 total. Fixture SHA-256: `54a245d4c4486c0e7439e260371cadbe213eede6325df96b96b387b78c7dede0`.

| Language | Scoped changed-line coverage |
| --- | --- |
| Java | 100% |
| TypeScript | 93% |
| Python | 100% |
| PHP | 100% |
| Scala | 92% |

These measure the example scopes. Full-application changed-line coverage remains unconfigured. Each language uses its own tools and configuration; repositories can extend or replace them. This workflow remains `workflow_dispatch` only, optional and advisory. It does not change merge requirements.

Local acceptance passed: dependency installation, build/typecheck, lint, unit coverage, migration validation, six API/browser tests, repository contract validation and 38 script tests. The first browser attempt lacked the required Playwright executable; installing the pinned browser resolved that environment prerequisite, and all six tests passed on retry.

Separate local Codex agent QA used the branch-owned Worker at localhost:8791. Four advisory rows passed: exact toolkit revision in health output, Worker/D1 readiness with development revision and version, unauthorized read and cross-origin write rejection, and browser editor-board startup with three seeded issues. This is local functional evidence; hosted agent QA remains unconfigured. No deployment or live production verification was performed.

The supported installer refreshed only the collector and scorecard workflow; selected skills, application QA skills, policy, and the consumer-owned Snyk workflow were preserved. The lock, Worker toolkit metadata, and polyglot helper pin agree. See [adoption notes](../toolkit-adoption.md#optional-provider-waiting) for the explicit-disable wait behavior and preserved missing-evidence semantics. The dependency-vulnerability control is not activated in this consumer's Proof policy; its default Snyk Open Source provider binding remains configured.
