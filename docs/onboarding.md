# Workspace and skill onboarding

This is Fieldnotes, an existing consumer of toolkit v2.3.1, not a fresh toolkit
installation. Start with [local app setup](../README.md#try-it-locally),
[AGENTS.md](../AGENTS.md) and [application contracts](design.md). Its runtime pin
is `f53a167be5283c1378740f475f231aa130f3aee9` in
[toolkit.lock.json](../toolkit.lock.json).

## Open the application checkout

Open the reference app's actual Git folder in the agent client, rather than the
separate toolkit checkout. After moving a checkout, update the client's saved
project entry as well as opening the new directory. An attached folder or a
shell working directory does not prove the saved project path changed.

Inspect the client's terminal before editing:

```sh
pwd
git rev-parse --show-toplevel
git status --short
```

Confirm the Git root is `ai-software-toolkit-reference-app`. With Codex CLI,
`codex app /path/to/ai-software-toolkit-reference-app` opens that workspace;
confirm any saved project entry also uses that location.

## Client discovery

The committed Codex skills live in `.agents/skills/<name>/SKILL.md`. Claude Code
uses `.claude/skills/<name>/SKILL.md`, which is an optional separate installation
and is not created by this change. `docs/ai/skills/` is not an automatic client
discovery location. Codex is sufficient; no Claude installation or credential is
required. Follow [optional Claude setup](toolkit-adoption.md#claude-code-setup)
if you choose that client.

The seven starter skills are `toolkit-setup`, `prepare-safe-change`, `code-review`,
`test-gap-finder`, `security-audit-lite`, `dependency-risk-review` and `qa-bootstrap`.
This app also keeps `docs-sync`, `repo-bootstrap`, `release-readiness`,
`spec-driven-development` and the generated `qa`, `qa-web` and `qa-api` skills.
`_shared-project-ops` contains shared support, not another task skill.

Use the [task map](../AGENTS.md#choose-a-skill-for-the-task). In the client selector,
confirm the skill's name and project path; same-named user-wide copies can differ.
For example, explicitly invoke `$code-review` in Codex and ask:

> Read AGENTS.md and use this repository's code-review skill to review the diff.
> Do not run local tests or QA. Use the linked hosted CI and report unavailable
> verification. Keep checks optional and lifecycle/polyglot manual.

If discovery fails, check the workspace, destination and client skill settings
before reinstalling. Do not install the entire catalog as a discovery workaround.
To add selected skills, use the [pinned standalone installer](toolkit-adoption.md#selected-codex-skills).
This app has a custom provenance lock: do not run CLI `init`/`update` against it.
Fresh toolkit installations default to Proof plus seven skills and 11 workflows
covering 12 advisory Core checks; that default does not replace this app's
existing workflow or skill selection.

## What the evidence establishes

| State | Required evidence |
| --- | --- |
| Installed | Expected skill files and source pin |
| Discovered | Client exposes the intended name and project path |
| Invoked | Run identifies and reads the selected skill |
| Performed | Task-specific findings or edits |
| Verified | Passing outcome evidence for the exact evaluated revision |

The toolkit's [five captured Codex demonstrations](https://github.com/ravisingh11/ai-software-toolkit/blob/31a3f61e6fde51ff093be1ea739545008a22ed56/docs/verification/action-skills/codex/README.md)
exercise isolated upstream fixtures. They do not verify this application's
installed skills, deployed Worker, Claude execution or current functional QA.
The app's [recorded Codex QA](verification/local-qa.md) is historical local
browser/API evidence from September 25, 2026, not a new run. Preserve its source
binding and the [deployment records](verification/README.md).

Follow the user's execution limits. When local checks are excluded, use required
hosted **Application acceptance**; it is deterministic CI, not agent functional
QA. Missing, skipped, stale or failed evidence remains explicit. All toolkit
checks are optional to adopt and enforce, Core and agent QA stay advisory, and
lifecycle/polyglot execution stays manual. No skill grants merge, deployment,
publication, credential or branch-protection authority.
