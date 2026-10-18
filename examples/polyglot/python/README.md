# Python quality example

The pure Python domain implements the same shared Fieldnotes transition contract.
It is an independently executed example, not a deployed Python service.

From the repository root, run `python3 scripts/polyglot.py setup --language python`
then `python3 scripts/polyglot.py check --language python --base origin/main`.
The common setup creates an ignored virtual environment with the versions from
the pinned toolkit requirements; it does not modify the system Python.

- Build checks parse the Python sources separately from lint.
- Ruff applies correctness and bugbear rules from `ruff.toml`.
- The shared driver asserts all fixture results, withholding expected answers
  from the native program, and emits a JUnit report for the toolkit helper.
- coverage.py instruments actual execution and emits Cobertura domain-line
  coverage, including zero-hit executable lines. CLI coverage is outside the
  selected source scope.
- `architecture.py` checks Python ASTs and rejects imports and direct I/O in
  this deliberately dependency-free domain. It is a small static purity
  contract, not a complete Python dependency graph or runtime sandbox.

`check.sh` also exposes `setup`, `build`, `lint`, `run`, `coverage`, `architecture`,
and `versions` for inspection. Coverage needs an absolute
`POLYGLOT_COVERAGE_REPORT`; the common driver supplies it. Repositories select
commands, scope, target, and whether results affect merging.
