# PHP quality example

The PHP 8.4 domain implements the shared Fieldnotes contract, independently of
the deployed Worker. Docker is required; no system PHP or Composer is installed.

From the repository root, run `python3 scripts/polyglot.py setup --language php`
then `python3 scripts/polyglot.py check --language php --base origin/main`.
`toolchain.json` pins the official PHP image by digest and PHPStan/Xdebug downloads
by SHA-256. Explicit setup builds a local image. Subsequent checks disable
container networking and mount source read-only.

- PHP syntax checking is separate from PHPStan's maximum-level static analysis.
- The shared driver asserts actual output for each fixture and emits JUnit.
- Xdebug measures executed lines; `coverage.php` converts measured counts to
  Cobertura and retains unexecuted executable lines. Branch coverage is not
  measured. The selected changed-code scope is `src/Domain`, excluding the CLI.
- `architecture.php` uses PHP's tokenizer to enforce this dependency-free domain's
  purity boundary. This is a conservative static check, not a complete PHP
  dependency graph or protection against arbitrary dynamic execution.

`check.sh` exposes setup/build/lint/run/coverage/architecture/versions. Coverage
receives an absolute `POLYGLOT_COVERAGE_REPORT` from the driver. Repositories
choose tools, thresholds, applicability and enforcement.

The converter removes Xdebug's covered implicit file return at one line beyond
EOF, because that opcode has no physical source line. Any other out-of-range
line fails conversion; unexecuted physical source lines remain in the report.
