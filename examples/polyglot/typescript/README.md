# TypeScript quality example

This adapter calls Fieldnotes' existing production `requireEditor`, `parseStatus`,
and `canTransition` functions. The other languages implement the shared domain
contract independently; this example checks parity with the existing application.
It does not create a second TypeScript server.

From the repository root, run `python3 scripts/polyglot.py setup --language typescript`
then `python3 scripts/polyglot.py check --language typescript --base origin/main`.
Root `package-lock.json` pins the toolchain; Node 24–26 is supported.

- TypeScript compilation is separate from real type-aware ESLint checks.
- The shared fixture driver asserts actual native results and emits JUnit.
- c8 instruments Node/V8 execution and emits Cobertura domain-line coverage.
- dependency-cruiser inspects imports, including type-only dependencies, and
  rejects cycles, unresolved imports, and domain-to-CLI/Node-I/O dependencies.
  Static imports do not establish runtime workspace isolation.

These TypeScript rules are not universal. Java, Python, PHP and Scala have
separate native checks in sibling directories. Repositories select adoption,
thresholds and whether any check affects merging.
