"""Hosted-only package contract regressions; no real producer or deployment."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import release_package as package


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        self.root.mkdir()
        self.output = Path(self.temporary.name) / "artifact"
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Package fixture"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "fixture@example.invalid"], check=True)
        config = {"name": "ai-software-toolkit-reference-app", "main": "src/index.ts", "compatibility_date": "2026-09-25", "account_id": "fixture", "assets": {"directory": "./public", "binding": "ASSETS", "run_worker_first": ["/api/*"]}, "d1_databases": [{"binding": "DB", "database_name": "fixture", "database_id": "fixture", "migrations_dir": "migrations"}], "version_metadata": {"binding": "CF_VERSION_METADATA"}, "vars": {"APP_REVISION": "development", "TOOLKIT_REVISION": "b" * 40}, "observability": {"enabled": True}}
        self.write("wrangler.jsonc", config)
        self.write("toolkit.lock.json", {"revision": "b" * 40})
        self.write("package.json", {"devDependencies": {"wrangler": package.WRANGLER_VERSION}})
        for name, text in {"public/index.html": "<h1>fixture</h1>", "public/app.js": "console.log('fixture');", "public/styles.css": "body {}", "migrations/0001.sql": "CREATE TABLE fixture(id TEXT);"}.items():
            self.write(name, text)
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "--quiet", "-m", "fixture"], check=True)
        self.write("dist/index.js", "export default {fetch(){return new Response('compiled fixture')}};")

    def write(self, name, value):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value) if isinstance(value, dict) else value)
        return p

    def stage(self):
        return package.stage(self.root, self.output)

    def test_stage_binds_compiled_bytes_config_and_source_without_secrets(self):
        self.write(".dev.vars", "SYNTHETIC_UNPACKAGED_VALUE=do-not-copy")
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        frozen = self.stage()
        verified = package.verify_directory(self.output, expected_manifest=frozen["manifest_sha256"])
        config = package.read_json(self.output / "payload/deploy-config.json")
        self.assertTrue(config["no_bundle"])
        self.assertEqual(config["main"], "worker/index.js")
        self.assertEqual(config["vars"]["APP_REVISION"], package.git(self.root, "rev-parse", "HEAD"))
        self.assertEqual(verified["package_digest"], frozen["package_digest"])
        self.assertFalse((self.output / "payload/.dev.vars").exists())
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_portable_verifier_snapshot_matches_recorded_candidate_source(self):
        root = Path(__file__).resolve().parents[2]
        provenance = package.read_json(root / "scripts/assurance-source.json")
        self.assertEqual(provenance["repository"], "https://github.com/ravisingh11/ai-software-toolkit")
        self.assertRegex(provenance["revision"], r"^[0-9a-f]{40}$")
        self.assertEqual(package.sha(root / provenance["installed_path"]), provenance["sha256"])

    def test_modified_bytes_missing_and_added_members_are_rejected(self):
        frozen = self.stage()
        compiled = self.output / "payload/worker/index.js"
        old = compiled.read_bytes()
        compiled.write_bytes(old + b"// altered")
        with self.assertRaises(ValueError): package.verify_directory(self.output, expected_manifest=frozen["manifest_sha256"])
        compiled.write_bytes(old)
        extra = self.output / "payload/unexpected.txt"
        extra.write_text("extra")
        with self.assertRaises(ValueError): package.verify_directory(self.output)
        extra.unlink()
        compiled.unlink()
        with self.assertRaises(ValueError): package.verify_directory(self.output)

    def test_rewriting_manifest_after_test_cannot_bypass_frozen_hash(self):
        frozen = self.stage()
        manifest_path = self.output / "package-manifest.json"
        manifest = package.read_json(manifest_path)
        manifest["source"]["revision"] = "c" * 40
        package.write_json(manifest_path, manifest)
        with self.assertRaisesRegex(ValueError, "Frozen manifest"):
            package.verify_directory(self.output, expected_manifest=frozen["manifest_sha256"])

    def test_invalid_contract_version_duplicate_and_unsafe_members_rejected(self):
        self.stage()
        path = self.output / "package-manifest.json"
        original = package.read_json(path)
        for mutate in (lambda m: m.update(version=99), lambda m: m["files"].append(dict(m["files"][0])), lambda m: m["files"][0].update(path="../escape")):
            m = copy.deepcopy(original)
            mutate(m)
            package.write_json(path, m)
            with self.assertRaises(ValueError): package.verify_directory(self.output)
        path.write_text('{"version":1,"version":2}')
        with self.assertRaisesRegex(ValueError, "Duplicate"): package.verify_directory(self.output)

    def test_source_and_config_drift_stop_staging(self):
        self.write("toolkit.lock.json", {"revision": "c" * 40})
        with self.assertRaisesRegex(ValueError, "pins disagree"): self.stage()
        self.assertFalse(self.output.exists())
        self.write("toolkit.lock.json", {"revision": "b" * 40})
        config = package.read_json(self.root / "wrangler.jsonc")
        config["build"] = {"command": "do not execute"}
        self.write("wrangler.jsonc", config)
        with self.assertRaisesRegex(ValueError, "configuration keys"): self.stage()

    def test_existing_output_and_symlinks_are_preserved(self):
        self.output.mkdir()
        marker = self.output / "custom.txt"
        marker.write_text("preserve")
        with self.assertRaisesRegex(ValueError, "Preserve"): self.stage()
        self.assertEqual(marker.read_text(), "preserve")
        shutil.rmtree(self.output)
        (self.root / "public/linked").symlink_to(self.root / "package.json")
        with self.assertRaisesRegex(ValueError, "symlink"): self.stage()

    def environment(self):
        return {"GITHUB_REPOSITORY": package.REPOSITORY, "GITHUB_RUN_ID": "123", "GITHUB_RUN_ATTEMPT": "2", "GITHUB_EVENT_NAME": "push", "GITHUB_REF": "refs/heads/main", "PACKAGE_STEP_RESULTS": json.dumps({name: {"outcome": "success", "conclusion": "success"} for name in ("build", "package", "unit_tests", "migrations", "repository", "checkpoint_tests", "package_tests", "e2e")})}

    def test_seal_retains_observations_but_not_final_run_or_deployment_claims(self):
        frozen = self.stage()
        record = package.seal(self.output, frozen["manifest_sha256"], environment=self.environment())
        self.assertEqual(record["run_attempt"], 2)
        self.assertEqual(record["package_digest"], frozen["package_digest"])
        self.assertIn("Final GitHub run conclusion", record["limits"])
        with self.assertRaisesRegex(ValueError, "never rewrite"):
            package.seal(self.output, frozen["manifest_sha256"], environment=self.environment())

    def test_failed_skipped_cancelled_and_missing_steps_cannot_seal(self):
        frozen = self.stage()
        for result in ("failure", "skipped", "cancelled", ""):
            env = self.environment()
            steps = json.loads(env["PACKAGE_STEP_RESULTS"])
            steps["e2e"] = {"outcome": result, "conclusion": result}
            env["PACKAGE_STEP_RESULTS"] = json.dumps(steps)
            with self.assertRaisesRegex(ValueError, "cannot be retained"):
                package.seal(self.output, frozen["manifest_sha256"], environment=env)
            self.assertFalse((self.output / "verification.json").exists())
        env = self.environment()
        env["GITHUB_REPOSITORY"] = "someone/else"
        with self.assertRaisesRegex(ValueError, "repository"):
            package.seal(self.output, frozen["manifest_sha256"], environment=env)


if __name__ == "__main__":
    unittest.main()
