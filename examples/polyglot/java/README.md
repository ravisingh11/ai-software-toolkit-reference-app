# Java transition example

This lane implements the shared Fieldnotes transition contract in Java 21. It is a
small domain example, not a second deployed application. Each repository chooses
its own tools, rules, thresholds, and whether checks affect merging.

Prerequisites: JDK 21 (set `JAVA_HOME`), Python 3, and network access for explicit
setup. On this development machine the script also discovers Homebrew's JDK 21.
Tools are pinned by version, URL, and SHA-256 in `toolchain.json`. `setup` is the
only command that downloads tools, into `.artifacts/polyglot/java/`. Subsequent
lint and coverage invocations verify the downloaded JAR checksums.

From the repository root:

```sh
examples/polyglot/java/check.sh setup
examples/polyglot/java/check.sh build
examples/polyglot/java/check.sh lint
examples/polyglot/java/check.sh architecture
examples/polyglot/java/check.sh versions
printf 'one\teditor\talpha\talpha\ttriage\tin_progress\n' | examples/polyglot/java/check.sh run
python3 scripts/polyglot_conformance.py --language java \
  --junit .artifacts/polyglot/java/tests.xml \
  --coverage .artifacts/polyglot/java/coverage.xml
```

`run` and `coverage` consume six tab-separated fields per row: ID, role, session
workspace, issue workspace, current status, requested status. They output exactly
`ID<TAB>result` for each row. Expected results stay in the caller's test driver.
A malformed TSV row fails the process; domain denials are ordinary result codes.

- **Build:** `javac --release 21 -Xlint:all -Werror`, separate from lint.
- **Lint:** Checkstyle 10.21.4 checks imports, braces, empty catches, switch
  fallthrough, and other configured source rules. This is a deliberately small
  example ruleset; it is not full Java security analysis.
- **Architecture:** JDK `jdeps` examines compiled class dependencies. Domain
  classes may reference other domain classes and an explicit small set of JDK
  value/collection classes. CLI, I/O, network, reflection, and process APIs are
  outside that allowlist. This checks static dependencies, not runtime behavior.
- **Coverage:** JaCoCo 0.8.13 instruments the actual JVM execution. Its report is
  converted to Cobertura executable-line data for the shared changed-code helper.
  Every reported domain executable line is retained, including zero-hit lines.
  A hit means at least one instruction on that line executed; the converted
  report does not claim branch coverage. CLI coverage is excluded deliberately.
  No coverage threshold is imposed by this lane.

The shared conformance driver supplies defensive cases and verifies returned
results. The domain deliberately has no persistence, HTTP server, or real tenant
authorization backend; production integration tests must cover those boundaries.
