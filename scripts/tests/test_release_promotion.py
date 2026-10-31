"""Hosted fixture-only promotion tests. No real GitHub/Cloudflare/live calls."""
from __future__ import annotations

import base64
import copy
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import stat
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import assurance
import promote_package as promote
import release_package as package


class PromotionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.source = "a" * 40
        self.tree = "b" * 40
        self.run = {"id": 123, "run_attempt": 2, "repository": {"id": 11, "full_name": package.REPOSITORY}, "head_repository": {"id": 11, "full_name": package.REPOSITORY}, "event": "push", "head_branch": "main", "status": "completed", "conclusion": "success", "path": package.WORKFLOW, "workflow_id": 99, "head_sha": self.source, "created_at": "2026-10-31T12:00:00Z", "updated_at": "2026-10-31T14:00:00Z", "html_url": "https://github.com/" + package.REPOSITORY + "/actions/runs/123"}
        self.workflow = {"id": 99, "path": package.WORKFLOW, "state": "active"}
        self.job = {"name": "Application acceptance", "status": "completed", "conclusion": "success", "head_sha": self.source, "run_id": 123, "run_attempt": 2, "steps": [{"name": n, "status": "completed", "conclusion": "success"} for n in promote.REQUIRED_STEPS]}
        self.directory = self.root / "fixture-package"
        payload = self.directory / "payload"
        payload.mkdir(parents=True)
        self.source_config = package.read_json(package.ROOT / "wrangler.jsonc")
        config = package.canonical_configuration(self.source_config, self.source)
        package.write_json(payload / "deploy-config.json", config)
        for name, data in {"worker/index.js": b"export default {fetch(){return new Response('compiled')}};", "public/index.html": b"<h1>fixture</h1>", "public/app.js": b"// fixture", "public/styles.css": b"body {}", "migrations/0001.sql": b"CREATE TABLE fixture(id TEXT);"}.items():
            p = payload / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
            p.chmod(0o644)
        manifest = {"version": 1, "kind": "package-manifest", "source": {"repository": "https://github.com/" + package.REPOSITORY, "revision": self.source, "tree": self.tree}, "build": {"tool": "wrangler", "version": package.WRANGLER_VERSION}, "configuration": {"path": "deploy-config.json", "sha256": package.sha(payload / "deploy-config.json")}, "files": [{"path": p.relative_to(payload).as_posix(), "size": p.stat().st_size, "sha256": package.sha(p), "mode": "0644"} for p in sorted(payload.rglob("*")) if p.is_file()]}
        package.write_json(self.directory / "package-manifest.json", manifest)
        candidate = {"version": 1, "kind": "package-candidate", "source_revision": self.source, "manifest_sha256": package.sha(self.directory / "package-manifest.json"), "package_digest": assurance.package_digest(manifest)}
        package.write_json(self.directory / "candidate.json", candidate)
        record = {"version": 1, "kind": "package-test-evidence", "source_revision": self.source, "manifest_sha256": candidate["manifest_sha256"], "package_digest": candidate["package_digest"], "repository": package.REPOSITORY, "workflow_path": package.WORKFLOW, "run_id": 123, "run_attempt": 2, "event": "push", "ref": "refs/heads/main", "observed_at_utc": "2026-10-31T13:00:00Z", "steps": {n: {"outcome": "success", "conclusion": "success"} for n in ("build", "package", "unit_tests", "migrations", "repository", "checkpoint_tests", "package_tests", "e2e")}, "limits": "Fixture observations, not deployment evidence"}
        package.write_json(self.directory / "verification.json", record)
        self.archive = self.root / "fixture.zip"
        with zipfile.ZipFile(self.archive, "w") as zipped:
            for p in sorted(self.directory.rglob("*")):
                if p.is_file(): zipped.write(p, p.relative_to(self.directory).as_posix())
        self.artifact = {"id": 456, "name": "worker-release-" + self.source, "expired": False, "expires_at": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(), "size_in_bytes": self.archive.stat().st_size, "digest": "sha256:" + package.sha(self.archive), "workflow_run": {"id": 123, "head_sha": self.source, "head_branch": "main", "repository_id": 11, "head_repository_id": 11}}
        self.candidate = candidate

    def github(self, endpoint):
        if endpoint == "actions/runs/123": return copy.deepcopy(self.run)
        if endpoint == "actions/workflows/acceptance.yml": return copy.deepcopy(self.workflow)
        if endpoint.startswith("compare/"): return {"status": "ahead", "merge_base_commit": {"sha": self.source}}
        if endpoint == "actions/runs/123/artifacts?per_page=100": return {"total_count": 1, "artifacts": [copy.deepcopy(self.artifact)]}
        if endpoint == "actions/runs/123/attempts/2/jobs?per_page=100": return {"total_count": 1, "jobs": [copy.deepcopy(self.job)]}
        if endpoint == "git/commits/" + self.source: return {"tree": {"sha": self.tree}}
        if endpoint == "git/ref/heads/main": return {"object": {"sha": self.source}}
        if endpoint.startswith("contents/wrangler.jsonc?ref="):
            data = json.dumps(self.source_config).encode()
            return {"encoding": "base64", "size": len(data), "content": base64.b64encode(data).decode()}
        raise AssertionError("Unexpected GitHub endpoint " + endpoint)

    def download(self, command, **kwargs):
        self.assertEqual(command[:2], ["gh", "api"])
        self.assertTrue(command[2].endswith("/actions/artifacts/456/zip"))
        kwargs["stdout"].write(self.archive.read_bytes())
        return subprocess.CompletedProcess(command, 0)

    def prepared(self):
        output = self.root / "prepared"
        with patch.object(promote, "api", side_effect=self.github), patch.object(promote.subprocess, "run", side_effect=self.download):
            report = promote.prepare(123, output)
        return output, report

    def test_prepare_verifies_platform_and_exact_bytes_without_cloud_credentials(self):
        with patch.object(promote, "wrangler", side_effect=AssertionError("Credentials must not be read")):
            output, record = self.prepared()
        self.assertEqual(record["state"], "verified-awaiting-separate-deployment-authorization")
        self.assertEqual(record["package_digest"], self.candidate["package_digest"])
        self.assertFalse(record["native_build_provenance"])
        self.assertEqual((output / "artifact.zip").read_bytes(), self.archive.read_bytes())

    def test_wrong_repository_source_workflow_or_unsuccessful_run_rejected(self):
        for field, value in (("event", "pull_request"), ("head_branch", "feature"), ("status", "in_progress"), ("conclusion", "cancelled"), ("conclusion", "failure"), ("path", ".github/workflows/other.yml"), ("workflow_id", 1234)):
            run = copy.deepcopy(self.run);run[field] = value
            with self.assertRaises(ValueError, msg=field): promote.validate_run(run, self.workflow)
        for key in ("repository", "head_repository"):
            run = copy.deepcopy(self.run);run[key]["full_name"] = "untrusted/elsewhere"
            with self.assertRaises(ValueError): promote.validate_run(run, self.workflow)

    def test_expired_wrong_run_wrong_source_and_unsigned_artifacts_rejected(self):
        changes = [lambda a: a.update(expired=True), lambda a: a.update(expires_at="2020-01-01T00:00:00Z"), lambda a: a.update(digest=None), lambda a: a.update(name="worker-release-wrong"), lambda a: a["workflow_run"].update(id=999), lambda a: a["workflow_run"].update(head_sha="c" * 40), lambda a: a["workflow_run"].update(repository_id=12), lambda a: a.update(size_in_bytes=promote.MAX_ARCHIVE + 1)]
        for change in changes:
            artifact = copy.deepcopy(self.artifact);change(artifact)
            with self.assertRaises((ValueError, TypeError)): promote.validate_artifact(artifact, self.run)

    def test_failed_skipped_cancelled_and_incomplete_package_jobs_rejected(self):
        for outcome in ("failure", "skipped", "cancelled", None):
            job = copy.deepcopy(self.job);job["steps"][0]["conclusion"] = outcome
            with self.assertRaises(ValueError): promote.validate_jobs([job], self.run)
        for key, value in (("head_sha", "c" * 40), ("run_attempt", 1), ("conclusion", "failure")):
            job = copy.deepcopy(self.job);job[key] = value
            with self.assertRaises(ValueError): promote.validate_jobs([job], self.run)
        with self.assertRaises(ValueError): promote.validate_jobs([self.job, self.job], self.run)

    def test_ambiguous_or_missing_artifact_does_not_download(self):
        def duplicate(endpoint):
            if "artifacts?" in endpoint: return {"total_count": 2, "artifacts": [self.artifact, self.artifact]}
            return self.github(endpoint)
        with patch.object(promote, "api", side_effect=duplicate), patch.object(promote.subprocess, "run") as execute:
            with self.assertRaisesRegex(ValueError, "ambiguous"): promote.prepare(123, self.root / "missing")
            execute.assert_not_called()

    def test_stale_attempt_false_pass_and_wrong_subject_evidence_rejected(self):
        path = self.directory / "verification.json";original = package.read_json(path)
        for change in (lambda r: r.update(run_attempt=1), lambda r: r.update(source_revision="c" * 40), lambda r: r["steps"]["e2e"].update(outcome="failure"), lambda r: r.update(version=99)):
            record = copy.deepcopy(original);change(record);package.write_json(path, record)
            with self.assertRaises(ValueError): promote.validate_test_record(self.directory, self.run)
        package.write_json(path, original)

    def test_corrupt_download_rejected_before_extract_or_credentials(self):
        self.artifact["digest"] = "sha256:" + "0" * 64
        with patch.object(promote, "api", side_effect=self.github), patch.object(promote.subprocess, "run", side_effect=self.download), patch.object(promote, "wrangler") as credentials:
            with self.assertRaisesRegex(ValueError, "digest differs"): promote.prepare(123, self.root / "corrupt")
            credentials.assert_not_called()
        self.assertFalse((self.root / "corrupt/package").exists())

    def test_path_traversal_symlinks_and_duplicate_zip_members_rejected(self):
        for name in ("../escape", "/absolute", "payload/../../escape", "payload\\outside", "payload/a:b", "unexpected.json"):
            p = self.root / "bad.zip"
            with zipfile.ZipFile(p, "w") as zipped: zipped.writestr(name, b"blocked")
            with self.assertRaises(ValueError): promote.safe_extract(p, self.root / "unpack")
            self.assertFalse((self.root / "unpack").exists())
        p = self.root / "link.zip"
        with zipfile.ZipFile(p, "w") as zipped:
            info = zipfile.ZipInfo("payload/link");info.create_system = 3;info.external_attr = (stat.S_IFLNK | 0o777) << 16;zipped.writestr(info, "../../outside")
        with self.assertRaises(ValueError): promote.safe_extract(p, self.root / "unpack")
        p = self.root / "duplicate.zip"
        with zipfile.ZipFile(p, "w") as zipped:
            zipped.writestr("payload/a", b"one");zipped.writestr("payload/a", b"two")
        with self.assertRaises(ValueError): promote.safe_extract(p, self.root / "unpack")

    def test_source_config_mismatch_rejected_even_when_package_checksums_are_valid(self):
        self.source_config["account_id"] = "other-account"
        with patch.object(promote, "api", side_effect=self.github):
            with self.assertRaisesRegex(ValueError, "configuration differs"): promote.verify_source(self.directory, self.run)

    def command_output(self, command, **kwargs):
        if command[:2] == ["node", "--version"]: return "v24.19.0\n"
        if "status" in command: return ""
        if "rev-parse" in command: return self.source + "\n"
        raise AssertionError("Unexpected local command " + str(command))

    def test_changed_prepared_archive_rejected_before_cloud_credentials(self):
        prepared, _ = self.prepared();(prepared / "artifact.zip").write_bytes(b"tampered")
        with patch.object(promote, "inspect_platform", return_value=(self.run, self.artifact)), patch.object(promote.subprocess, "check_output", side_effect=self.command_output), patch.object(promote, "wrangler") as credentials:
            with self.assertRaisesRegex(ValueError, "archive bytes changed"): promote.deploy(prepared, self.root / "deploy")
            credentials.assert_not_called()

    def fake_github_write(self, endpoint, body, request):
        package.write_json(request, body)
        if endpoint == "deployments": return {"id": 789, "sha": self.source, "environment": "production"}
        return {"id": 999, "state": body["state"]}

    def cloud_fixture(self, *, mutation=None, fail_upload=False, pending_migrations=False):
        self.cloud_calls = []
        count = 0
        def operation(command, *, config, log, cwd):
            nonlocal count
            self.cloud_calls.append(command)
            if command == ["whoami"]:
                value = self.source_config["account_id"]
                if mutation: mutation(config.parent)
            elif command[:3] == ["d1", "migrations", "list"]:
                value = "Pending 0002.sql" if pending_migrations else "No migrations to apply!"
            elif command[0] == "deployments":
                count += 1
                value = json.dumps([{"id": "2" * 8 + "-" + "2" * 4 + "-" + "2" * 4 + "-" + "2" * 4 + "-" + "2" * 12, "created_on": "2026-10-31T13:00:00Z", "annotations": {"workers/message": "git:" + self.source}, "versions": [{"version_id": self.deployment_fixture()["worker_version"] if count > 1 else "old-worker", "percentage": 100}]}])
            elif command[0] == "deploy":
                self.assertIn("--no-bundle", command)
                self.assertIn("--autoconfig=false", command)
                self.assertEqual((config.parent / "worker/index.js").read_bytes(), (self.directory / "payload/worker/index.js").read_bytes())
                if fail_upload: raise ValueError("Injected upload failure")
                value = "Current Version ID: " + self.deployment_fixture()["worker_version"]
            else: raise AssertionError("Unexpected cloud operation " + str(command))
            log.write_text(value)
            return value
        return operation

    def test_deploy_uses_fresh_verified_archive_and_keeps_live_handoff_unverified(self):
        prepared, _ = self.prepared()
        (prepared / "package/payload/worker/index.js").write_text("UNTRUSTED extracted copy")
        with patch.object(promote, "api", side_effect=self.github), patch.object(promote, "inspect_platform", return_value=(self.run, self.artifact)), patch.object(promote.subprocess, "check_output", side_effect=self.command_output), patch.object(promote, "wrangler", side_effect=self.cloud_fixture()), patch.object(promote, "github_write", side_effect=self.fake_github_write):
            record = promote.deploy(prepared, self.root / "deployed")
        self.assertEqual(record["state"], "deployed-awaiting-live-verification")
        self.assertEqual(record["live_pilot"], "unverified")
        self.assertEqual(record["traffic_percentage"], 100)
        receipt = assurance.read_document(self.root / "deployed/deployment-receipt.json")
        self.assertEqual(receipt["results"][-1]["status"], "not_run")

    def test_mutation_during_preflight_and_pending_migrations_stop_before_upload(self):
        prepared, _ = self.prepared()
        def change(payload): (payload / "worker/index.js").write_text("changed during preflight")
        with patch.object(promote, "api", side_effect=self.github), patch.object(promote, "inspect_platform", return_value=(self.run, self.artifact)), patch.object(promote.subprocess, "check_output", side_effect=self.command_output), patch.object(promote, "wrangler", side_effect=self.cloud_fixture(mutation=change)), patch.object(promote, "github_write") as external:
            with self.assertRaises(ValueError): promote.deploy(prepared, self.root / "changed-deploy")
            external.assert_not_called()
        self.assertFalse(any(c[0] == "deploy" for c in self.cloud_calls))
        with patch.object(promote, "api", side_effect=self.github), patch.object(promote, "inspect_platform", return_value=(self.run, self.artifact)), patch.object(promote.subprocess, "check_output", side_effect=self.command_output), patch.object(promote, "wrangler", side_effect=self.cloud_fixture(pending_migrations=True)), patch.object(promote, "github_write") as external:
            with self.assertRaisesRegex(ValueError, "Pending D1"): promote.deploy(prepared, self.root / "pending-deploy")
            external.assert_not_called()
        self.assertFalse(any(c[0] == "deploy" for c in self.cloud_calls))

    def test_upload_failure_retains_incomplete_record_and_never_retries_or_claims_success(self):
        prepared, _ = self.prepared()
        with patch.object(promote, "api", side_effect=self.github), patch.object(promote, "inspect_platform", return_value=(self.run, self.artifact)), patch.object(promote.subprocess, "check_output", side_effect=self.command_output), patch.object(promote, "wrangler", side_effect=self.cloud_fixture(fail_upload=True)), patch.object(promote, "github_write", side_effect=self.fake_github_write):
            with self.assertRaisesRegex(ValueError, "Injected upload"): promote.deploy(prepared, self.root / "failed-deploy")
        self.assertEqual(sum(c[0] == "deploy" for c in self.cloud_calls), 1)
        record = package.read_json(self.root / "failed-deploy/deployment.json")
        self.assertEqual(record["state"], "upload-or-verification-incomplete")
        self.assertEqual(record["live_pilot"], "unverified")
        self.assertFalse((self.root / "failed-deploy/deployment-receipt.json").exists())
        self.assertEqual(package.read_json(self.root / "failed-deploy/github-failure-request.json")["state"], "failure")

    def deployment_fixture(self):
        return {"version": 1, "kind": "package-deployment-observation", "state": "deployed-awaiting-live-verification", "observed_at_utc": "2026-10-31T13:00:00Z", "source_revision": self.source, "toolkit_revision": "b" * 40, "worker_version": "1" * 8 + "-" + "1" * 4 + "-" + "1" * 4 + "-" + "1" * 4 + "-" + "1" * 12, "cloudflare_deployment_id": "2" * 8 + "-" + "2" * 4 + "-" + "2" * 4 + "-" + "2" * 4 + "-" + "2" * 12, "package_digest": self.candidate["package_digest"], "manifest_sha256": self.candidate["manifest_sha256"], "configuration_digest": package.read_json(self.directory / "package-manifest.json")["configuration"]["sha256"], "artifact_id": 456, "archive_digest": self.artifact["digest"], "run_id": 123, "run_attempt": 2, "run_url": self.run["html_url"], "environment_url": promote.LIVE_URL, "github_deployment_id": 789, "traffic_percentage": 100}

    def live_fixture(self):
        record = self.deployment_fixture();record.update(kind="package-live-observations", state="verified-at-observation-time")
        record["release_smoke"] = {"status": "passed", "revision": self.source, "toolkitRevision": record["toolkit_revision"], "workerVersion": record["worker_version"], "checks": ["database health", "isolated session", "create issue", "transition", "persist comment"], "private_cookie": "DO-NOT-PUBLISH"}
        record["browser"] = {"status": "passed", "observed_at_utc": record["observed_at_utc"], "source_revision": self.source, "toolkit_revision": record["toolkit_revision"], "worker_version": record["worker_version"], "checks": [{"name": name, "status": "passed"} for name in sorted(promote.LIVE_CHECKS)], "screenshots": [], "page_errors": [], "private_cookie": "DO-NOT-PUBLISH"}
        shots = self.root / "screenshots";shots.mkdir(exist_ok=True)
        for name in sorted(promote.LIVE_IMAGES):
            data = b"\x89PNG\r\n\x1a\n" + b"\0" * 8 + struct.pack(">II", 390, 844)
            (shots / name).write_bytes(data)
            record["browser"]["screenshots"].append({"file": name, "sha256": hashlib.sha256(data).hexdigest(), "width": 390, "height": 844})
        record["limits"] = "DO-NOT-PUBLISH freeform note"
        return record

    def test_runtime_receipt_binds_subject_and_expires_without_changing_proof(self):
        record = self.live_fixture();evidence = self.root / "live-observations.json";package.write_json(evidence, record)
        receipt = self.root / "runtime-receipt.json";promote.write_checkpoint(receipt, evidence, record, checkpoint="runtime", valid_for_seconds=3600)
        parsed = assurance.read_document(receipt)
        expected = {"source_revision": self.source, "configuration_digest": record["configuration_digest"]}
        result = assurance.verify_receipt(receipt, expected=expected, now=datetime(2026, 10, 31, 13, 30, tzinfo=timezone.utc))
        self.assertTrue(result["all_reported_checks_passed"])
        self.assertFalse(result["authenticated_producer"])
        self.assertFalse(result["authorization_granted"])
        stale = assurance.verify_receipt(receipt, expected=expected, now=datetime(2026, 10, 31, 14, 1, tzinfo=timezone.utc))
        self.assertIn("expired-observation", stale["invalidation_reasons"])
        with self.assertRaisesRegex(ValueError, "already exists"): promote.write_checkpoint(receipt, evidence, record, checkpoint="runtime")
        self.assertEqual(parsed["observed_at"], record["observed_at_utc"])

    def test_deployment_receipt_keeps_live_handoff_not_run(self):
        record = self.deployment_fixture();evidence = self.root / "deployment.json";package.write_json(evidence, record)
        receipt = self.root / "deployment-receipt.json";promote.write_checkpoint(receipt, evidence, record, checkpoint="deployment")
        self.assertEqual(assurance.read_document(receipt)["results"][-1]["status"], "not_run")

    def test_render_preserves_observation_time_and_bytes_without_network_or_credential_calls(self):
        record = self.live_fixture();observations = self.root / "live-observations.json";package.write_json(observations, record);before = observations.read_bytes()
        with patch.object(promote, "api", side_effect=AssertionError("No network")), patch.object(promote, "wrangler", side_effect=AssertionError("No cloud credentials")), patch.object(promote.subprocess, "run", side_effect=AssertionError("No producers")):
            result = promote.render(observations, self.root / "public-docs")
        self.assertFalse(result["new_live_checks"])
        self.assertEqual(observations.read_bytes(), before)
        text = (self.root / "public-docs/verification.json").read_text()
        self.assertNotIn("DO-NOT-PUBLISH", text)
        self.assertEqual(json.loads(text)["observed_at_utc"], record["observed_at_utc"])
        for image in record["browser"]["screenshots"]:
            self.assertEqual((self.root / "public-docs/screenshots" / image["file"]).read_bytes(), (self.root / "screenshots" / image["file"]).read_bytes())

    def test_false_or_incomplete_live_observations_and_changed_screenshots_rejected(self):
        original = self.live_fixture()
        for change in (lambda r: r.update(source_revision="c" * 40), lambda r: r["browser"].update(status="failed"), lambda r: r["browser"]["checks"].pop(), lambda r: r["browser"]["screenshots"][0].update(file="../outside.png")):
            record = copy.deepcopy(original);change(record)
            with self.assertRaises(ValueError): promote.validate_live_record(record)
        observations = self.root / "live-observations.json";package.write_json(observations, original)
        (self.root / "screenshots" / original["browser"]["screenshots"][0]["file"]).write_bytes(b"modified")
        with self.assertRaisesRegex(ValueError, "screenshot bytes differ"): promote.render(observations, self.root / "changed-docs")

    def test_existing_and_symlink_output_is_preserved(self):
        destination = self.root / "keep";destination.mkdir();marker = destination / "custom.txt";marker.write_text("preserve")
        with self.assertRaisesRegex(ValueError, "Preserve"): promote.prepare(123, destination)
        self.assertEqual(marker.read_text(), "preserve")
        link = self.root / "linked";link.symlink_to(destination, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"): promote.safe_output(link / "new")


if __name__ == "__main__":
    unittest.main()
