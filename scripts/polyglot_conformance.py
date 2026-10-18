#!/usr/bin/env python3
"""Assert native-language results against shared cases and emit actual JUnit results."""
from __future__ import annotations

import argparse
import csv
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("java", "typescript", "python", "php", "scala")
FIELDS = ("id", "role", "session_workspace", "issue_workspace", "current_status", "requested_status", "expected")


def load_cases(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != list(FIELDS):
            raise ValueError("Shared case header is invalid")
        rows = list(reader)
    if not rows or len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Shared cases must be nonempty and have unique IDs")
    if any(set(row) != set(FIELDS) or any(value is None for value in row.values()) for row in rows):
        raise ValueError("Shared case columns are malformed")
    if any(not row["id"].strip() for row in rows):
        raise ValueError("Shared case IDs must not be blank")
    return rows


def input_tsv(cases: list[dict[str, str]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
    for case in cases:
        writer.writerow([case[field] for field in FIELDS[:-1]])
    return buffer.getvalue()


def output_rows(output: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in output.splitlines():
        fields = line.split("\t")
        if len(fields) != 2:
            raise ValueError("Native adapter emitted a non-result line")
        rows.setdefault(fields[0], []).append(fields[1])
    return rows


class ContractCase(unittest.TestCase):
    def __init__(self, case: dict[str, str], actual: dict[str, list[str]]):
        super().__init__()
        self.case = case
        self.actual = actual

    def shortDescription(self):
        return self.case["id"]

    def runTest(self):
        self.assertEqual(self.actual.get(self.case["id"]), [self.case["expected"]])


class RecordedResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.executed = []

    def startTest(self, test):
        super().startTest(test)
        self.executed.append(test)


def write_junit(path: Path, language: str, result: RecordedResult) -> None:
    suite = ET.Element("testsuite", name=f"fieldnotes-{language}", tests=str(result.testsRun),
                       failures=str(len(result.failures)), errors=str(len(result.errors)), skipped="0")
    failures = {id(test): trace for test, trace in result.failures}
    errors = {id(test): trace for test, trace in result.errors}
    for test in result.executed:
        case = ET.SubElement(suite, "testcase", name=test.shortDescription() or test.id(), classname=language)
        for tag, outcomes in (("failure", failures), ("error", errors)):
            if id(test) in outcomes:
                ET.SubElement(case, tag).text = outcomes[id(test)]
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(suite).write(path, encoding="utf-8", xml_declaration=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=LANGUAGES, required=True)
    parser.add_argument("--junit", type=Path, required=True)
    parser.add_argument("--coverage", type=Path)
    args = parser.parse_args(argv)
    try:
        args.junit.unlink(missing_ok=True)
        if args.coverage:
            args.coverage.unlink(missing_ok=True)
        cases = load_cases(ROOT / "examples/polyglot/cases.tsv")
        environment = dict(os.environ)
        if args.coverage:
            environment["POLYGLOT_COVERAGE_REPORT"] = str(args.coverage.resolve())
        process = subprocess.run(
            [str(ROOT / f"examples/polyglot/{args.language}/check.sh"), "coverage" if args.coverage else "run"],
            cwd=ROOT, input=input_tsv(cases), text=True, capture_output=True, timeout=180, env=environment,
        )
        if process.returncode:
            raise ValueError(f"Native {args.language} process failed ({process.returncode}): {process.stderr[-3000:]}")
        actual = output_rows(process.stdout)
        if set(actual) != {case["id"] for case in cases}:
            raise ValueError("Native adapter omitted cases or emitted unexpected IDs")
        suite = unittest.TestSuite(ContractCase(case, actual) for case in cases)
        result = RecordedResult()
        suite.run(result)
        write_junit(args.junit, args.language, result)
        print(f"{args.language}: {result.testsRun} conformance tests executed; {len(result.failures) + len(result.errors)} failed")
        return 0 if result.wasSuccessful() else 1
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
