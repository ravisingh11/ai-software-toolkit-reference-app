#!/usr/bin/env bash
set -euo pipefail
lane="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$lane/../../.." && pwd)"
artifacts="$root/.artifacts/polyglot/java"
if [[ -n "${JAVA_HOME:-}" ]]; then
  java_bin="$JAVA_HOME/bin"
elif [[ -x /opt/homebrew/opt/openjdk@21/bin/java ]]; then
  java_bin=/opt/homebrew/opt/openjdk@21/bin
else
  java_bin="$(dirname "$(command -v java)")"
fi
java_version="$("$java_bin/java" -version 2>&1 | head -n 1)"
if [[ ! "$java_version" =~ \"21\. ]]; then
  echo "Java 21 required; set JAVA_HOME (found $java_version)" >&2
  exit 1
fi
verify_tools() {
  python3 - "$lane/toolchain.json" "$artifacts" <<'PY'
import hashlib, json, pathlib, sys
for tool in json.load(open(sys.argv[1]))['tools']:
    file = pathlib.Path(sys.argv[2]) / tool['file']
    if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != tool['sha256']:
        raise SystemExit(f'Missing or invalid {file}; run check.sh setup')
PY
}
build() {
  mkdir -p "$artifacts/classes"
  find "$artifacts/classes" -type f -name '*.class' -delete
  "$java_bin/javac" --release 21 -Xlint:all -Werror -g -d "$artifacts/classes" \
    "$lane/src/fieldnotes/domain/Transition.java" "$lane/src/fieldnotes/cli/Main.java"
}
case "${1:-}" in
  setup)
    mkdir -p "$artifacts"
    python3 - "$lane/toolchain.json" "$artifacts" <<'PY'
import hashlib, json, pathlib, sys, urllib.request
for tool in json.load(open(sys.argv[1]))['tools']:
    dest = pathlib.Path(sys.argv[2]) / tool['file']
    if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() == tool['sha256']:
        continue
    data = urllib.request.urlopen(tool['url'], timeout=60).read()
    if hashlib.sha256(data).hexdigest() != tool['sha256']:
        raise SystemExit(f'Checksum mismatch: {tool["file"]}')
    dest.write_bytes(data)
PY
    verify_tools
    ;;
  build) build ;;
  lint)
    verify_tools
    "$java_bin/java" -jar "$artifacts/checkstyle.jar" -c "$lane/checkstyle.xml" "$lane/src"
    ;;
  run)
    build
    "$java_bin/java" -cp "$artifacts/classes" fieldnotes.cli.Main
    ;;
  coverage)
    : "${POLYGLOT_COVERAGE_REPORT:?Set absolute POLYGLOT_COVERAGE_REPORT}"
    verify_tools
    build
    "$java_bin/java" "-javaagent:$artifacts/jacocoagent.jar=destfile=$artifacts/jacoco.exec,append=false" \
      -cp "$artifacts/classes" fieldnotes.cli.Main
    "$java_bin/java" -jar "$artifacts/jacococli.jar" report "$artifacts/jacoco.exec" \
      --classfiles "$artifacts/classes" --sourcefiles "$lane/src" --xml "$artifacts/jacoco.xml" >&2
    python3 "$lane/coverage.py" "$artifacts/jacoco.xml"
    ;;
  architecture)
    build
    "$java_bin/jdeps" -verbose:class -filter:none "$artifacts/classes" > "$artifacts/jdeps.txt"
    python3 "$lane/architecture.py" "$artifacts/jdeps.txt"
    ;;
  versions)
    echo "$java_version"
    cat "$lane/toolchain.json"
    ;;
  *) echo 'Usage: check.sh setup|build|lint|run|coverage|architecture|versions' >&2; exit 2 ;;
esac
