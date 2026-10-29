# Fieldnotes SDLC checkpoints

At each checkpoint ask: **What action are we considering, what has been checked,
and does that evidence justify proceeding?** Git events offer places to run
checks; they do not define the evidence's scope or authorize the next action.

The [README diagram](../README.md#use-the-toolkit-across-the-sdlc) connects the
process, invocation, and relevant capabilities. This guide adapts the
[upstream checkpoint guidance at `2fe38d1`](https://github.com/ravisingh11/ai-software-toolkit/blob/2fe38d1aca97b1745d81a4d41e14cef3918b0843/docs/sdlc-checkpoints.md)
and [README examples](https://github.com/ravisingh11/ai-software-toolkit/blob/2fe38d1aca97b1745d81a4d41e14cef3918b0843/README.md)
to this application's actual commands and workflows. Toolkit v2.3.2 now includes
that guidance; the original adaptation links above retain their source identities.
[toolkit.lock.json](../toolkit.lock.json) remains pinned to
`8a36b246f6bd0c3808276de0f7794b26f574ce5e`.

All 33 checks remain discoverable through the
[versioned activation index](https://github.com/ravisingh11/ai-software-toolkit/blob/v2.3.2/docs/activation.md)
and the upstream guide's full checkpoint mapping. Reuse those guides for
prerequisites and provider adoption rather than treating this placement map as
configuration. Only selected, applicable checks affect scoring. All toolkit
checks remain optional to adopt, Core stays advisory, and lifecycle/polyglot
execution stays manual. **Application acceptance** is a separate GitHub merge
requirement already adopted by Fieldnotes.

## Decisions, subjects, and boundaries

| Checkpoint | Decision and evidence subject | Relevant checks and execution | Authority and next boundary | Reassess when |
| --- | --- | --- | --- | --- |
| Coding finished | Prepare a commit? Working changes, including untracked files. | Human/agent code review, test gaps, docs and architecture impact in the checkout. | Advisory feedback supports preparing/staging; no immutable commit evidence yet. | Work, requirements, configuration, or comparison inputs change. |
| Pre-commit | Record these exact contents? The index, which can differ from the working tree. | Recommended fast lint, secrets and file validity through deliberately adopted local hooks/manual commands. | Local hooks can reject an attempt but are bypassable. General exact staged-snapshot Proof evaluation is future work. | Staged contents or relevant inputs change. |
| Commit creation | Accept this commit record? Proposed message and references. | Repository-owned message conventions; a custom `commit-msg` hook if adopted. | No built-in toolkit message producer or automatic hook here. Message acceptance does not validate code. | Proposed message or references change. |
| Post-commit | What is known about this revision? Created commit. | Authorized local commit-bound checks or hosted feedback after pushing. | Results apply to their recorded subject; a post-commit result cannot prevent creation of that commit. | Revision, policy, tool inputs, or comparison base changes. |
| Pre-push | Share these commits? Outgoing range. | Recommended range-aware secrets/change scope and selected early checks through a custom hook or command. | Repository-owned, optional, bypassable; a single checkout's tests do not prove every outgoing commit passed. | Range, remote base, or local source changes. |
| PR created/updated | Ready for review? Head/base revisions and mutable PR metadata. | Adopted Unit Tests, build, lint, security and metadata workflows, plus Application acceptance. | Advisory Proof results inform review. Application acceptance validates GitHub's integration checkout; standard toolkit source workflows check out the PR head. | Head/base changes, metadata edits for affected metadata evidence, or policy/configuration changes. |
| Pre-merge | Integrate this candidate? Current head, integration candidate and review state. | Inspect required Application acceptance, accepted Proof evidence, findings and resolved review conversations. | GitHub merge requirements gate integration. A passing result does not grant merge authority; verify its subject and currency. | Head/base or review state changes, or the tested integration candidate no longer matches. |
| Post-merge | Is resulting main healthy? Actual merged commit. | Existing Application acceptance on pushes to main; inspect the new result and its subject. | Source/CI health supports a later release handoff. It does not deploy the Worker or establish live health. | Main advances, configuration changes, or later release/deployment evidence is needed. |

The checkpoint labels are documentation. Existing Proof operations remain
`change` and `release`; there is no checkpoint scheduler or `--checkpoint` flag.
Recommended placement is not a claim that every listed capability is installed,
selected, configured, executed, or passed. These are distinct states.

Execution, evaluation, and enforcement also differ: a producer executes a
command, Proof evaluates accepted authoritative evidence, and a separately
adopted GitHub rule or hook gates an action. An advisory `ALLOW` may coexist with
failed or missing evidence. No readiness result grants permission to commit,
push, merge, publish, or deploy.

## Invocation examples

Use the installed project skill from the actual application checkout. For example:

> Use `$code-review` to review my working changes. Read AGENTS.md first.
> Report correctness risks, test gaps, and documentation impact. Do not run
> local tests or QA, commit, or push.

For the pre-merge decision:

> Use `$prepare-safe-change` to assess before-merge using existing change policy
> and hosted evidence. Identify tested revisions, comparison bases, required
> checks, missing evidence and unresolved findings. Do not run local tests or merge.

See [skill onboarding](onboarding.md) for discovery and actual invocation
boundaries. The upstream Codex demonstrations are not new runs of these app skills.

Read-only diagnostics use the installed runtime directly:

```sh
python3 .proof/doctor.py --target . --operation change
```

Doctor reads setup and evidence, without running producers, changing variables,
reading credential values, or enabling enforcement. Missing setup can produce
a nonzero exit status. Local environment configuration and GitHub variables are
separate; finding a workflow or executable does not prove it ran successfully.

Inspect required CI for the current branch's open PR:

```sh
gh pr checks --required
```

Review the linked run's tested revision as well as its status. This command
reads results; it does not run tests or evaluate all 33 controls.

When local execution is explicitly authorized, this app's existing wrapper is:

```sh
npm run toolkit:check
```

Run it only from a clean, committed checkout with Node 24, Python and scanner
prerequisites available, and a meaningful `origin/main` comparison for the
committed feature branch. It creates a source snapshot, configures real app
commands, runs selected producers, and retains artifacts under `.artifacts/toolkit/`.
It can install dependencies, build and execute tests/scanners. It is not a
read-only diagnostic, does not replace browser acceptance or agent QA, and
does not automatically run the optional polyglot examples. Skip it entirely
when local tests are excluded. An explicit `--polyglot` mode remains a separate,
manual choice; this guide does not invoke it.

This app has a custom provenance lock, not a CLI managed-file inventory. Do not
run toolkit CLI `init` or `update` against it. See
[pinned adoption](toolkit-adoption.md) for reviewed standalone-installer updates.

## Unit tests and optional hooks

The adopted [Unit Tests workflow](../.github/workflows/unit-tests.yml) responds
to PR open, reopen, new commits, or explicit manual dispatch. It checks out
`${{ github.event.pull_request.head.sha || github.sha }}`. Its existing GitHub
variables select `PROOF_SETUP_COMMAND=npm ci` and
`PROOF_UNIT_TEST_COMMAND=npm run test:coverage`.

The installed runner's existing calls are:

```sh
python3 .proof/run_repository_command.py --command unit-tests --phase setup
python3 .proof/run_repository_command.py --command unit-tests --phase producer
```

These are execution commands, not diagnostics. GitHub supplies its configured
variables in CI; a local shell does not inherit those repository variables.
For an explicitly authorized local run, supply the same variables yourself.
Nonempty `PROOF_*` variables override the optional consumer-owned
`.proof/commands.json` fallback; this app does not currently have that JSON file,
and this documentation adds none. See
[runner implementation](../.proof/run_repository_command.py).

A missing command fails. Test-command failure remains a failed job. The runner
alone does not issue authoritative hosted evidence: the trusted collector must
verify the provider, workflow, and exact subject before Proof accepts it.
PR-body-only edits do not retrigger Unit Tests; metadata has its own producer.

A repository could choose this custom `pre-push` hook for early feedback:

```sh
#!/bin/sh
export PROOF_UNIT_TEST_COMMAND='npm run test:coverage'
exec python3 .proof/run_repository_command.py \
  --command unit-tests --phase producer
```

Dependencies must already be available. Compose with existing hooks instead of
overwriting them. This example installs nothing and changes no Git settings.
Its exit status can reject a local push, but the hook is bypassable, tests only
its actual checkout, and cannot satisfy required hosted Application acceptance.
Leave it unconfigured when local tests are excluded.

The separate [Application acceptance workflow](../.github/workflows/acceptance.yml)
runs build/typecheck, lint, unit coverage, migrations, repository validation and
API/browser acceptance. On PRs its default checkout is GitHub's integration
revision; on pushes to main it checks the resulting main commit. Do not relabel
the Unit Tests head result as integration evidence, or either result as live
production or agent functional QA evidence.

## Worked evidence boundaries

- **Partial staging:** if the working tree has a fix that is absent from the
  index, passing working-tree tests do not validate the proposed commit. Review
  the index separately; current Proof has no generalized staged-snapshot subject.
- **PR-body edit:** source results can still describe an unchanged head, while
  metadata evidence needs reassessment against the new body. Do not rerun or
  relabel unrelated evidence merely because a metadata event occurred.
- **New commit or comparison base:** reassess source/diff-based results for the
  new subjects and meaningful baseline. A prior passing head or integration
  revision is not automatically current evidence.
- **Squash or merge:** retain original tested identities. Inspect the main
  Application acceptance run for the actual resulting commit; do not relabel a
  PR-head result as a squash commit result. Establish any relationship explicitly.
- **Missing prerequisites or excluded execution:** missing commands/credentials,
  blocked scans, failures, stale results and not-run/manual producers remain
  visible. A selected check with no accepted evidence does not become passed.
- **Selective adoption:** selected applicable checks contribute to scoring;
  unselected checks stay discoverable without being counted as failures or
  passes. Required Application acceptance remains separate from advisory Proof.

## Later handoffs and evidence

Release, deployment, and runtime need their own subjects, evidence and explicit
authorization. The [lifecycle fixture](../examples/lifecycle/README.md) and
[polyglot examples](../examples/polyglot/README.md) remain manual and optional.
Merging this guide does not dispatch either workflow or deploy the Worker.

Preserve [deployment and verification records](verification/README.md),
[historical app agent QA](verification/local-qa.md), and their original revision
bindings. A new README or guide is guidance, not a new live health/API/UI result,
skill demonstration, or change to installed policy/scoring.

## Actionable checkpoint reports

Application acceptance now attempts a final report and retained JSON/Markdown
artifact after its existing steps, including failures. Context captures the
actual PR integration checkout separately from event/head/base identities.
A main-push run records its own resulting revision; no PR or comparison base is
invented when absent. Earlier PR results retain their original subjects.

The report describes only this workflow's named steps. Failed, skipped,
interrupted or unobserved work is not a pass. Raw `outcome` remains visible even
if `continue-on-error` changes a conclusion. Original check and job conclusions
are preserved; best-effort reporting/upload cannot repair a failed check.
Detailed failure reasons remain in the linked step logs. Inspect the separate
Proof Scorecard, current required checks, approvals and conversations before
considering merge. Main CI is not release approval or deployment health.

The shared renderer is explicitly adopted application-owned tooling copied
from the toolkit reporting PR, outside the pinned `.proof` runtime. This is not
a toolkit release upgrade and does not change `toolkit.lock.json`. Its focused
regressions run in existing hosted acceptance, including actual evaluator cards,
stale subjects, supplemental-only success, failure retention and cancellation.
Lifecycle and polyglot producers remain manual.

For read-only presentation of an already collected evaluator card:

```sh
python3 scripts/checkpoint_report.py render \
  --context /path/to/downloaded/context.json \
  --config scripts/checkpoint-report.json \
  --scorecard /path/to/existing/scorecard.json \
  --output-dir /path/to/review-output
```

The command displays the supplied card without rerunning or authenticating it.
Keep its original provenance. `CHECKPOINT_STEPS` defaults to no observed results;
the output directory is explicit. `report.json` is a presentation record, not
Proof producer evidence. It retains the supplied card unchanged, with separate
passed, failed, blocked, unverified/not-run, stale and inactive display groups.
Skills are suggested only from files installed at context-capture time, never
claimed discovered or executed by the agent.

Cancellation, runner loss or checkout failure may prevent summaries/artifacts;
inspect the original GitHub run when missing. Artifact retention/access is
controlled by GitHub. All 33 checks remain discoverable in the
[activation index](https://github.com/ravisingh11/ai-software-toolkit/blob/main/docs/activation.md).
Checks stay optional, Core advisory, and lifecycle/polyglot manual. Deployment,
real skill verification and previous hook evidence remain unchanged.
