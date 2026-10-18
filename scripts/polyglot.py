#!/usr/bin/env python3
"""Explicit setup and advisory per-language quality checks; never changes merge rules."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".artifacts/polyglot"
PIN = json.loads((ROOT / "examples/polyglot/toolkit.json").read_text())
TOOLKIT = CACHE / "toolkit"
PYTHON = CACHE / "tools/venv/bin/python"
LANGUAGES = ("java", "typescript", "python", "php", "scala")
SCOPES = {
    "java": "examples/polyglot/java/src/fieldnotes/domain",
    "typescript": "examples/polyglot/typescript/src/domain.ts",
    "python": "examples/polyglot/python/src/domain.py",
    "php": "examples/polyglot/php/src/Domain",
    "scala": "examples/polyglot/scala/src",
}


def run(argv, **kwargs):
    return subprocess.run([str(value) for value in argv], cwd=ROOT, check=True, **kwargs)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def setup(languages):
    CACHE.mkdir(parents=True, exist_ok=True)
    if not (TOOLKIT / ".git").is_dir():
        run(["git", "init", "-q", TOOLKIT])
        run(["git", "-C", TOOLKIT, "remote", "add", "origin", PIN["repository"]])
        run(["git", "-C", TOOLKIT, "fetch", "--depth", "1", "origin", PIN["revision"]])
        run(["git", "-C", TOOLKIT, "checkout", "--detach", PIN["revision"]])
    verify_toolkit()
    if not PYTHON.exists():
        run([sys.executable, "-m", "venv", PYTHON.parents[1]])
    run([PYTHON, "-m", "pip", "install", "-r", TOOLKIT / "tooling/requirements-ci.txt"])
    if "typescript" in languages:
        run(["npm", "ci"])
    for language in languages:
        run([f"examples/polyglot/{language}/check.sh", "setup"], env=environment())


def verify_toolkit():
    result = subprocess.check_output(["git", "-C", str(TOOLKIT), "rev-parse", "HEAD"], text=True).strip()
    if result != PIN["revision"]:
        raise ValueError("Optional toolkit checkout does not match its pinned revision")
    dirty = subprocess.check_output(["git", "-C", str(TOOLKIT), "status", "--porcelain"], text=True).strip()
    if dirty:
        raise ValueError("Optional toolkit checkout must be clean")


def environment():
    env = dict(os.environ)
    env["PATH"] = str(PYTHON.parent) + os.pathsep + env.get("PATH", "")
    env["POLYGLOT_PYTHON"] = str(PYTHON)
    if not env.get("JAVA_HOME") and Path("/opt/homebrew/opt/openjdk@21").is_dir():
        env["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@21"
        env["PATH"] = env["JAVA_HOME"] + "/bin" + os.pathsep + env["PATH"]
    return env


def check(languages, stages, base, threshold):
    CACHE.mkdir(parents=True, exist_ok=True)
    report_path = CACHE / "results.json"
    report_path.unlink(missing_ok=True)
    if "coverage" in stages and not base:
        raise ValueError("Coverage needs an explicit --base comparison ref")
    verify_toolkit()
    if not PYTHON.exists():
        raise ValueError("Run explicit polyglot setup first")
    selected = list(languages)
    head = git("rev-parse", "HEAD")
    fixture_hash = hashlib.sha256((ROOT / "examples/polyglot/cases.tsv").read_bytes()).hexdigest()
    results = {"revision": head, "working_tree_clean": not bool(git("status", "--porcelain")),
               "toolkit_revision": PIN["revision"], "fixture_sha256": fixture_hash,
               "timestamp": datetime.now(timezone.utc).isoformat(), "mode": "advisory", "languages": {}}
    report_path.write_text(json.dumps(results, indent=2) + "\n")
    failed = False
    for language in selected:
        rows = []
        for stage in stages:
            command = [f"examples/polyglot/{language}/check.sh", stage]
            if stage == "test":
                command = [PYTHON, TOOLKIT / "tooling/check_test_integrity.py", "--", PYTHON,
                           ROOT / "scripts/polyglot_conformance.py", "--language", language, "--junit", "{report}"]
            elif stage == "coverage":
                if not base:
                    raise ValueError("Coverage needs an explicit --base comparison ref")
                command = [PYTHON, TOOLKIT / "tooling/check_changed_coverage.py", "--base", base,
                           "--threshold", str(threshold), "--source", SCOPES[language], "--", PYTHON,
                           ROOT / "scripts/polyglot_conformance.py", "--language", language,
                           "--junit", "{report_dir}/tests.xml", "--coverage", "{report}"]
            start = time.monotonic()
            try:
                completed = subprocess.run([str(value) for value in command], cwd=ROOT, env=environment(),
                                           text=True, capture_output=True, timeout=300)
                exit_code = completed.returncode
                output = completed.stdout + completed.stderr
                status = "passed" if exit_code == 0 else "failed"
            except (OSError, subprocess.TimeoutExpired) as error:
                exit_code = 2
                output = str(error)
                status = "blocked"
            log = CACHE / f"{language}-{stage}.log"
            log.write_text(output)
            if status == "passed" and "not_applicable:" in output:
                status = "not_applicable"
            row = {"stage": stage, "status": status, "exit_code": exit_code,
                         "duration_seconds": round(time.monotonic() - start, 2),
                         "log": str(log.relative_to(ROOT))}
            tests = re.search(r"(\d+) conformance tests executed", output)
            coverage = re.search(r"Coverage: ([\d.]+)%", output)
            if tests:
                row["conformance_tests"] = int(tests[1])
            if coverage:
                row["changed_line_coverage_percent"] = float(coverage[1])
                row["threshold_percent"] = threshold
            rows.append(row)
            print(f"{language:10} {stage:12} {status}", flush=True)
            failed |= exit_code != 0
        results["languages"][language] = rows
        report_path.write_text(json.dumps(results, indent=2) + "\n")
    results["comparison_unchanged"] = git("rev-parse", "HEAD") == head and not bool(git("status", "--porcelain"))
    report_path.write_text(json.dumps(results, indent=2) + "\n")
    return 1 if failed else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("setup", "check"))
    parser.add_argument("--language", choices=(*LANGUAGES, "all"), default="all")
    parser.add_argument("--stage", action="append", choices=("build", "lint", "test", "architecture", "coverage", "versions"))
    parser.add_argument("--base")
    parser.add_argument("--threshold", type=float, default=90, help="Reference-app choice; not shared toolkit policy")
    args = parser.parse_args()
    languages = LANGUAGES if args.language == "all" else (args.language,)
    try:
        if args.operation == "setup":
            setup(languages)
            return 0
        return check(languages, args.stage or ("versions", "build", "lint", "test", "architecture", "coverage"), args.base, args.threshold)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"Polyglot check unavailable/failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
