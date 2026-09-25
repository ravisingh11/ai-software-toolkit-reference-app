# Toolkit scorecard · v0.1.0

**ORANGE · 12 of 15 advisory controls passed · 3 have no result.**

This is the recorded CI scorecard for the v0.1.0 release's tested PR commit. It is a versioned snapshot, not a live assessment of the current default branch or running application. The 80% figure measures passed advisory controls, not application quality, test coverage, or developer productivity.

## Evidence and provenance

| Field | Recorded value |
| --- | --- |
| Evaluated commit | [`8bc67cbcca74580b564ab2c9beb7a40285ba86d0`](https://github.com/ravisingh11/ai-software-toolkit-reference-app/commit/8bc67cbcca74580b564ab2c9beb7a40285ba86d0) |
| Pull request | [#5: gate demonstration and operational follow-up](https://github.com/ravisingh11/ai-software-toolkit-reference-app/pull/5) |
| CI run | [Guardrail Scorecard · September 25, 2026](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/runs/36139392302) |
| Release | [v0.1.0](https://github.com/ravisingh11/ai-software-toolkit-reference-app/releases/tag/v0.1.0) |
| Status / decision | `ORANGE` / `allow` |
| Advisory controls | 12 of 15 passed; 3 have no result |
| Enforced Guardrails controls | 0 configured; percentage is not applicable |

The release's merged source revision is `0f7574ded7b47a475aa7cf65574f79aed01b7d61`. The scorecard evaluates the PR head shown above, not that merge commit. The raw [machine-readable release attachment](https://github.com/ravisingh11/ai-software-toolkit-reference-app/releases/download/v0.1.0/guardrails-scorecard.json) contains the source results used for this report; GitHub downloads that attachment.

## Controls

| Control | Mode | Evidence result |
| --- | --- | --- |
| Repository validation | Advisory | Passed |
| Documentation validation | Advisory | Passed |
| Repository ground truth | Advisory | Passed |
| Change scope | Advisory | Passed |
| Format and lint | Advisory | Passed |
| Migration validation | Advisory | Passed |
| Build | Advisory | Passed |
| Unit tests | Advisory | Passed |
| Changed-code coverage | Advisory | No result |
| Custom static analysis (Semgrep) | Advisory | Passed |
| Secret detection (Gitleaks) | Advisory | Passed |
| Deep SAST (CodeQL) | Advisory | Passed |
| Dependency change review | Advisory | Passed |
| Platform secret protection | Advisory | No result |
| Dependency remediation | Advisory | No result |

`No result` means the producer did not supply usable evidence. It is never a pass. Changed-code coverage is not activated with full instrumentation. The platform secret-protection and dependency-remediation probes need the settings token described in [the evidence guide](README.md); enabling platform settings alone does not produce scorecard evidence.

All controls in this snapshot are advisory, so `allow` does not mean all checks passed or that Guardrails enforces them. GitHub separately requires **Application acceptance** for merging to main. That check is outside this scorecard's enforced-control total; its failing-then-passing demonstration is documented in [the evidence guide](README.md).

## How this connects to CI

The repository's [Guardrail Scorecard workflow](../../.github/workflows/guardrails-scorecard.yml) runs when a PR is opened, updated, or reopened, when a review is submitted or dismissed, and on manual dispatch. It collects CI evidence for the evaluated revision, writes a readable report to the Actions run summary, and uploads Markdown/JSON artifacts.

For newer changes, use [scorecard workflow runs](https://github.com/ravisingh11/ai-software-toolkit-reference-app/actions/workflows/guardrails-scorecard.yml) and check the evaluated commit in the report. A successful workflow run is not equivalent to a green scorecard: advisory gaps can produce an orange result while the workflow succeeds.

This repository page and the README summary do not refresh automatically. When publishing a new release snapshot, update both from its verified CI artifact, retain the exact evaluated revision and run link, and preserve missing evidence. Hosted agent QA, unattended deployment, and artifact attestation remain unconfigured; they are not additional passed controls.
