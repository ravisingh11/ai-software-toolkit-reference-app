"""Trust-boundary tests for native adapter conformance evidence."""
from contextlib import redirect_stderr, redirect_stdout
import csv
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET


SCRIPT = Path(__file__).resolve().parents[1] / "polyglot_conformance.py"
SPEC = importlib.util.spec_from_file_location("polyglot_conformance", SCRIPT)
conformance = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(conformance)
HEADER = "id\trole\tsession_workspace\tissue_workspace\tcurrent_status\trequested_status\texpected\n"
ROW = "transition\teditor\tboard-a\tboard-a\ttriage\tin_progress\tin_progress\n"


def case(identifier="transition", expected="in_progress"):
    return dict(zip(conformance.FIELDS, [identifier, "editor", "board-a", "board-a", "triage", "in_progress", expected]))


def execute(*tests):
    result = conformance.RecordedResult()
    unittest.TestSuite(tests).run(result)
    return result


class SharedFixtureTests(unittest.TestCase):
    def load(self, text):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "cases.tsv"
            fixture.write_text(text)
            return conformance.load_cases(fixture)

    def test_loads_checked_in_defensive_cases_with_unique_nonempty_ids(self):
        cases = conformance.load_cases(conformance.ROOT / "examples/polyglot/cases.tsv")
        ids = [row["id"] for row in cases]
        self.assertTrue(ids)
        self.assertTrue(all(ids))
        self.assertEqual(len(ids), len(set(ids)))

    def test_preserves_empty_input_fields_for_negative_cases(self):
        rows = self.load(HEADER + ROW.replace("\tboard-a\tboard-a", "\t\tboard-a"))
        self.assertEqual(rows[0]["session_workspace"], "")

    def test_rejects_header_only_fixture(self):
        with self.assertRaises(ValueError):
            self.load(HEADER)

    def test_rejects_duplicate_case_ids(self):
        with self.assertRaises(ValueError):
            self.load(HEADER + ROW + ROW)

    def test_rejects_empty_case_id(self):
        with self.assertRaises(ValueError):
            self.load(HEADER + ROW.replace("transition", "", 1))

    def test_rejects_whitespace_case_id(self):
        with self.assertRaises(ValueError):
            self.load(HEADER + ROW.replace("transition", "   ", 1))

    def test_rejects_reordered_header(self):
        with self.assertRaises(ValueError):
            self.load(HEADER.replace("id\trole", "role\tid") + ROW)

    def test_rejects_missing_column(self):
        with self.assertRaises(ValueError):
            self.load(HEADER + "\t".join(ROW.rstrip("\n").split("\t")[:-1]) + "\n")

    def test_rejects_extra_column(self):
        with self.assertRaises(ValueError):
            self.load(HEADER + ROW.rstrip("\n") + "\textra\n")

    def test_adapter_input_excludes_expected_results_and_header(self):
        payload = conformance.input_tsv([case(expected="secret-oracle-value")])
        rows = list(csv.reader(io.StringIO(payload), delimiter="\t"))
        self.assertEqual(rows, [["transition", "editor", "board-a", "board-a", "triage", "in_progress"]])
        self.assertNotIn("secret-oracle-value", payload)


class NativeOutputTests(unittest.TestCase):
    def test_rejects_native_log_line(self):
        with self.assertRaises(ValueError):
            conformance.output_rows("starting adapter\ntransition\tin_progress\n")

    def test_rejects_extra_result_column(self):
        with self.assertRaises(ValueError):
            conformance.output_rows("transition\tin_progress\textra\n")

    def test_matching_native_result_passes_one_executed_case(self):
        result = execute(conformance.ContractCase(case(), conformance.output_rows("transition\tin_progress\n")))
        self.assertEqual(result.testsRun, 1)
        self.assertTrue(result.wasSuccessful())

    def test_missing_native_result_fails_executed_case(self):
        result = execute(conformance.ContractCase(case(), conformance.output_rows("")))
        self.assertEqual(len(result.failures), 1)

    def test_duplicate_native_result_fails_even_when_both_values_match(self):
        result = execute(conformance.ContractCase(case(), conformance.output_rows("transition\tin_progress\ntransition\tin_progress\n")))
        self.assertEqual(len(result.failures), 1)

    def test_wrong_native_result_fails_executed_case(self):
        result = execute(conformance.ContractCase(case(), conformance.output_rows("transition\tdone\n")))
        self.assertEqual(len(result.failures), 1)


class JunitEvidenceTests(unittest.TestCase):
    def report(self, result):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "junit.xml"
            conformance.write_junit(path, "python", result)
            return ET.parse(path).getroot()

    def test_report_counts_only_cases_that_actually_ran(self):
        pending = conformance.ContractCase(case("pending"), {})
        result = execute(conformance.ContractCase(case("executed"), {"executed": ["in_progress"]}))
        root = self.report(result)
        self.assertEqual(root.get("tests"), "1")
        self.assertEqual([item.get("name") for item in root.findall("testcase")], ["executed"])
        self.assertTrue(all(test is not pending for test in result.executed))

    def test_report_records_assertion_failures_with_diagnostics(self):
        root = self.report(execute(conformance.ContractCase(case(), {"transition": ["done"]})))
        self.assertEqual(root.get("failures"), "1")
        self.assertEqual(root.get("errors"), "0")
        self.assertIn("AssertionError", root.find("testcase/failure").text)

    def test_report_records_runtime_errors_separately(self):
        class BrokenCase(unittest.TestCase):
            def runTest(self):
                raise RuntimeError("adapter evidence unavailable")

        root = self.report(execute(BrokenCase()))
        self.assertEqual(root.get("errors"), "1")
        self.assertEqual(root.get("failures"), "0")
        self.assertIn("adapter evidence unavailable", root.find("testcase/error").text)

    def test_report_does_not_invent_passes_when_no_cases_ran(self):
        root = self.report(conformance.RecordedResult())
        self.assertEqual(root.get("tests"), "0")
        self.assertEqual(root.findall("testcase"), [])


class CliEvidenceTests(unittest.TestCase):
    def invoke(self, stdout="transition\tin_progress\n", returncode=0, error=None):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.report = Path(self.directory.name) / "junit.xml"
        process = subprocess.CompletedProcess(["native"], returncode, stdout, "native failed")
        with patch.object(conformance, "load_cases", return_value=[case()]), patch.object(
            conformance.subprocess, "run", return_value=process, side_effect=error
        ) as native, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            status = conformance.main(["--language", "python", "--junit", str(self.report)])
        return status, native

    def test_success_executes_native_adapter_without_oracle_column(self):
        status, native = self.invoke()
        self.assertEqual(status, 0)
        self.assertEqual(native.call_args.kwargs["input"], "transition\teditor\tboard-a\tboard-a\ttriage\tin_progress\n")
        self.assertEqual(ET.parse(self.report).getroot().get("tests"), "1")

    def test_wrong_native_answer_returns_failure_and_failed_junit_case(self):
        status, _ = self.invoke(stdout="transition\tdone\n")
        self.assertEqual(status, 1)
        self.assertEqual(ET.parse(self.report).getroot().get("failures"), "1")

    def test_duplicate_native_answer_returns_failure_and_failed_junit_case(self):
        status, _ = self.invoke(stdout="transition\tin_progress\ntransition\tin_progress\n")
        self.assertEqual(status, 1)
        self.assertEqual(ET.parse(self.report).getroot().get("failures"), "1")

    def test_missing_native_answer_returns_error_without_success_report(self):
        status, _ = self.invoke(stdout="")
        self.assertEqual(status, 2)
        self.assertFalse(self.report.exists())

    def test_unexpected_native_case_returns_error_without_success_report(self):
        status, _ = self.invoke(stdout="transition\tin_progress\nunknown\tdone\n")
        self.assertEqual(status, 2)
        self.assertFalse(self.report.exists())

    def test_nonzero_native_exit_cannot_be_hidden_by_correct_stdout(self):
        status, _ = self.invoke(returncode=1)
        self.assertEqual(status, 2)
        self.assertFalse(self.report.exists())

    def test_timeout_returns_error_without_success_report(self):
        status, _ = self.invoke(error=subprocess.TimeoutExpired("native", 180))
        self.assertEqual(status, 2)
        self.assertFalse(self.report.exists())

    def test_native_failure_cannot_leave_an_old_success_report(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "junit.xml"
            report.write_text('<testsuite tests="23" failures="0" errors="0"/>')
            process = subprocess.CompletedProcess(["native"], 1, "", "native failed")
            with patch.object(conformance, "load_cases", return_value=[case()]), patch.object(
                conformance.subprocess, "run", return_value=process
            ), redirect_stderr(io.StringIO()):
                status = conformance.main(["--language", "python", "--junit", str(report)])
            self.assertNotEqual(status, 0)
            if report.exists():
                root = ET.parse(report).getroot()
                self.assertGreater(int(root.get("failures", "0")) + int(root.get("errors", "0")), 0)

    def test_malformed_native_output_returns_error_without_success_report(self):
        status, _ = self.invoke(stdout="debug log\n")
        self.assertEqual(status, 2)
        self.assertFalse(self.report.exists())


if __name__ == "__main__":
    unittest.main()
