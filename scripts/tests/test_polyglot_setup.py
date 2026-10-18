"""Exercise explicit toolkit cache updates using local Git repositories only."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("polyglot", Path(__file__).resolve().parents[1] / "polyglot.py")
polyglot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(polyglot)


class ToolkitCacheTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.origin = self.root / "origin"
        self.origin.mkdir()
        self.git(self.origin, "init", "-q")
        self.git(self.origin, "config", "user.name", "Test")
        self.git(self.origin, "config", "user.email", "test@example.invalid")
        (self.origin / "version.txt").write_text("first\n")
        self.git(self.origin, "add", ".")
        self.git(self.origin, "commit", "-qm", "First")
        self.first = self.git(self.origin, "rev-parse", "HEAD")
        (self.origin / "version.txt").write_text("second\n")
        self.git(self.origin, "commit", "-qam", "Second")
        self.second = self.git(self.origin, "rev-parse", "HEAD")
        self.cache = self.root / "cache"
        self.toolkit = self.cache / "toolkit"
        self.python = self.root / "python"
        self.python.touch()
        self.pin = {"repository": str(self.origin), "revision": self.first}
        for name, value in {"ROOT": self.root, "CACHE": self.cache, "TOOLKIT": self.toolkit,
                            "PYTHON": self.python, "PIN": self.pin}.items():
            patcher = patch.object(polyglot, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        original_run = polyglot.run

        def git_only(argv, **kwargs):
            if str(argv[0]) == "git":
                return original_run(argv, **kwargs)
            self.assertEqual(str(argv[0]), str(self.python))
            self.assertEqual(argv[1:4], ["-m", "pip", "install"])
            return subprocess.CompletedProcess(argv, 0)

        patcher = patch.object(polyglot, "run", side_effect=git_only)
        patcher.start()
        self.addCleanup(patcher.stop)

    def git(self, path, *args):
        return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()

    def test_explicit_setup_refreshes_clean_cache_to_new_immutable_pin(self):
        polyglot.setup([])
        self.assertEqual(self.git(self.toolkit, "rev-parse", "HEAD"), self.first)
        self.pin["revision"] = self.second
        polyglot.setup([])
        self.assertEqual(self.git(self.toolkit, "rev-parse", "HEAD"), self.second)
        self.assertEqual((self.toolkit / "version.txt").read_text(), "second\n")

    def test_dirty_cache_is_rejected_without_changing_local_work(self):
        polyglot.setup([])
        (self.toolkit / "version.txt").write_text("local edits\n")
        self.pin["revision"] = self.second
        with self.assertRaises(ValueError):
            polyglot.setup([])
        self.assertEqual(self.git(self.toolkit, "rev-parse", "HEAD"), self.first)
        self.assertEqual((self.toolkit / "version.txt").read_text(), "local edits\n")

    def test_untracked_cache_file_is_preserved(self):
        polyglot.setup([])
        local = self.toolkit / "notes.txt"
        local.write_text("keep me")
        self.pin["revision"] = self.second
        with self.assertRaises(ValueError):
            polyglot.setup([])
        self.assertEqual(local.read_text(), "keep me")
        self.assertEqual(self.git(self.toolkit, "rev-parse", "HEAD"), self.first)

    def test_ignored_generated_files_survive_clean_refresh(self):
        polyglot.setup([])
        (self.toolkit / ".git/info/exclude").write_text("generated.txt\n")
        generated = self.toolkit / "generated.txt"
        generated.write_text("keep generated output")
        self.pin["revision"] = self.second
        polyglot.setup([])
        self.assertEqual(generated.read_text(), "keep generated output")
        self.assertEqual(self.git(self.toolkit, "rev-parse", "HEAD"), self.second)

    def test_refresh_cannot_overwrite_ignored_local_file(self):
        polyglot.setup([])
        (self.toolkit / ".git/info/exclude").write_text("future.txt\n")
        local = self.toolkit / "future.txt"
        local.write_text("keep local data")
        (self.origin / "future.txt").write_text("upstream data")
        self.git(self.origin, "add", "future.txt")
        self.git(self.origin, "commit", "-qm", "Add future file")
        self.pin["revision"] = self.git(self.origin, "rev-parse", "HEAD")
        with self.assertRaises(subprocess.CalledProcessError):
            polyglot.setup([])
        self.assertEqual(local.read_text(), "keep local data")
        self.assertEqual(self.git(self.toolkit, "rev-parse", "HEAD"), self.first)

    def test_non_repository_cache_is_not_initialized_over_existing_data(self):
        self.toolkit.mkdir(parents=True)
        local = self.toolkit / "notes.txt"
        local.write_text("keep me")
        with self.assertRaises(ValueError):
            polyglot.setup([])
        self.assertEqual(local.read_text(), "keep me")
        self.assertFalse((self.toolkit / ".git").exists())

    def test_wrong_origin_is_rejected_even_with_correct_commit(self):
        polyglot.setup([])
        self.git(self.toolkit, "remote", "set-url", "origin", str(self.root / "other"))
        with self.assertRaises(ValueError):
            polyglot.setup([])
        self.assertEqual(self.git(self.toolkit, "remote", "get-url", "origin"), str(self.root / "other"))
        self.assertEqual(self.git(self.toolkit, "rev-parse", "HEAD"), self.first)

    def test_normal_check_rejects_stale_cache_without_fetch_or_checkout(self):
        polyglot.setup([])
        self.pin["revision"] = self.second
        with patch.object(polyglot, "run") as run, patch.object(polyglot.subprocess, "run", wraps=subprocess.run) as subprocess_run:
            with self.assertRaises(ValueError):
                polyglot.check(["python"], ["lint"], None, 90)
            run.assert_not_called()
            # check_output uses subprocess.run internally; only local cache inspection is permitted.
            self.assertTrue(all("fetch" not in str(call) and "checkout" not in str(call)
                                for call in subprocess_run.call_args_list))
        self.assertEqual(self.git(self.toolkit, "rev-parse", "HEAD"), self.first)

    def test_setup_rejects_mutable_revision_before_creating_cache(self):
        self.pin["revision"] = "main"
        with self.assertRaises(ValueError):
            polyglot.setup([])
        self.assertFalse(self.toolkit.exists())


if __name__ == "__main__":
    unittest.main()
