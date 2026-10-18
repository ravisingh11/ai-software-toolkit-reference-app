# Five languages, one defensive domain contract

These runnable examples exercise Fieldnotes issue transitions in Java, TypeScript,
Python, PHP and Scala. The deployed Worker remains TypeScript. The examples are
small domain/CLI adapters, not five web servers or production identity systems.
TypeScript calls the production domain functions; the other four implement the
same contract independently.

Every language needs its own tools. Copying a TypeScript ESLint configuration into
a Java repository will not lint Java. Extend or replace the relevant language
adapter to suit your runtime, framework, source layout and architecture.

| Example | Runtime | Real lint | Coverage | Architecture check |
| --- | --- | --- | --- | --- |
| [Java](java/README.md) | JDK 21 | Checkstyle | JaCoCo | compiled dependencies via jdeps |
| [TypeScript](typescript/README.md) | Node 24–26 | type-aware ESLint | c8/V8 | dependency-cruiser |
| [Python](python/README.md) | Python 3.9+ | Ruff | coverage.py | conservative AST purity rules |
| [PHP](php/README.md) | Docker PHP 8.4 | PHPStan max | Xdebug | conservative token-based purity rules |
| [Scala](scala/README.md) | Scala 2.13.16 / JDK 21 | WartRemover | JaCoCo | compiled dependencies via jdeps |

Compilation/syntax checks are separate from lint. Prettier is an optional
TypeScript formatting example (`npm run polyglot:format`). Tool versions and
checksums are recorded beside each example; npm tooling uses the root lockfile.
Python tooling and the two quality helpers use the immutable optional toolkit
revision in [toolkit.json](toolkit.json), separately from the installed `.guardrails`.

## Run it

Install Node 24+, Python 3.9+ with venv support, JDK 21, and a running Docker daemon
(for PHP). Explicit setup downloads pinned tools; subsequent native checks use the
local tools. Do not run setup scripts from unreviewed branches with secrets present.

```sh
npm run polyglot:setup
python3 -m unittest discover -s scripts/tests
# Commit source changes first: coverage binds evidence to a clean revision.
npm run polyglot:check -- --base origin/main --threshold 90
# Or select just one language:
python3 scripts/polyglot.py setup --language java
python3 scripts/polyglot.py check --language java --base origin/main --threshold 90
```

The reference app chooses 90% changed-line coverage as an example. Each consuming
repository chooses languages, scopes, thresholds, CI triggers and merge policy.
The new GitHub workflow is manual only. None of these examples installs required
checks, changes rulesets, or imposes toolkit-wide enforcement. Commands return
nonzero on failed/unavailable checks so owners can wire them to their own policy.

## Contract and evidence

[cases.tsv](cases.tsv) contains 23 synthetic scenarios. Authorization is evaluated
before resource lookup and validation: missing session is unauthenticated; a role
other than editor is forbidden; a different workspace returns not_found. Invalid
statuses are rejected. Equal statuses are idempotent; a transition through
in_progress is allowed; direct triage/done transitions are rejected. This models
a domain contract, not a full HTTP/authentication stack.

The driver withholds expected answers from each native process and asserts every
returned result. Missing, duplicate, malformed or extra responses fail. A fresh
JUnit report records actually executed assertions; the toolkit integrity helper
rejects empty/all-skipped/stale/failed results. Tests include malformed input,
invalid roles/statuses and workspace isolation, with harness regression tests.

Coverage uses actual runtime instrumentation and Cobertura, then the toolkit's
diff-cover helper compares changed executable lines to an explicit Git base.
Scopes are deliberate: Java/Python/PHP/TypeScript domain examples; Scala domain
and CLI. **This is not full-app changed-code coverage.** Worker routing, frontend,
other infrastructure and uninstrumented lines are outside those measurements.
The TypeScript adapter calls production functions but only adapter lines are in
its scoped coverage report. Domain branch coverage is measured separately by
`npm run test:coverage`; this runner measures changed lines.

Logs and machine-readable results go to ignored `.artifacts/polyglot/`. Results
include revision, fixture hash, helper revision, source-tree cleanliness, stage
status and coverage percentages when measured. Missing tooling fails visibly;
no changed executable lines is reported as not applicable, not a coverage pass.
Native architecture checks complement runtime tests; they are not proofs of
security, dynamic dependency safety or cross-language service isolation.
