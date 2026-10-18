#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../../.." && pwd)"
lane="$root/examples/polyglot/php"
artifacts="$root/.artifacts/polyglot/php"
image="fieldnotes-polyglot-php:8.4.20-xdebug3.4.7-phpstan2.1.32"
cd "$root"
case "${1:-}" in
  setup)
    mkdir -p "$artifacts"
    python3 - "$lane" "$artifacts" <<'PY'
import hashlib, json, pathlib, sys, urllib.request
lane, artifacts = map(pathlib.Path, sys.argv[1:])
config = json.loads((lane / 'toolchain.json').read_text())
for key, name in [('phpstan', 'phpstan.phar'), ('xdebug', 'xdebug.tgz')]:
    target = artifacts / name
    if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest() != config[key]['sha256']:
        with urllib.request.urlopen(config[key]['url']) as response:
            target.write_bytes(response.read())
    if hashlib.sha256(target.read_bytes()).hexdigest() != config[key]['sha256']:
        raise SystemExit(f'{key} checksum mismatch')
(artifacts / 'php-image.txt').write_text(config['phpImage'])
PY
    docker build --build-arg "PHP_IMAGE=$(cat "$artifacts/php-image.txt")" -f "$lane/Dockerfile" -t "$image" "$artifacts"
    exit
    ;;
esac
docker image inspect "$image" >/dev/null 2>&1 || { echo 'Run php/check.sh setup first' >&2; exit 2; }
container=(docker run --rm --network none -i -v "$root:$root:ro" -w "$root")
case "${1:-}" in
  build) "${container[@]}" "$image" sh -ec 'for file in examples/polyglot/php/*.php examples/polyglot/php/src/*.php examples/polyglot/php/src/Domain/*.php; do php -l "$file"; done' ;;
  lint) "${container[@]}" "$image" php /opt/phpstan.phar analyse -c examples/polyglot/php/phpstan.neon --no-progress ;;
  run) "${container[@]}" "$image" php examples/polyglot/php/src/cli.php ;;
  architecture) "${container[@]}" "$image" php examples/polyglot/php/architecture.php ;;
  coverage)
    : "${POLYGLOT_COVERAGE_REPORT:?Set absolute POLYGLOT_COVERAGE_REPORT}"
    [[ "$POLYGLOT_COVERAGE_REPORT" = /* ]] || { echo 'Coverage path must be absolute' >&2; exit 2; }
    mkdir -p "$(dirname "$POLYGLOT_COVERAGE_REPORT")"
    "${container[@]}" -v "$(dirname "$POLYGLOT_COVERAGE_REPORT"):$(dirname "$POLYGLOT_COVERAGE_REPORT")" -e POLYGLOT_COVERAGE_REPORT -e XDEBUG_MODE=coverage "$image" php examples/polyglot/php/coverage.php
    ;;
  versions) "${container[@]}" "$image" sh -c 'php --version; php /opt/phpstan.phar --version; php --ri xdebug | head -20' ;;
  *) echo 'Usage: check.sh setup|build|lint|run|coverage|architecture|versions' >&2; exit 2 ;;
esac
