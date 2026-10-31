#!/usr/bin/env python3
"""Explicit manual promotion of an independently verified main-run Worker package.

prepare is read-only on GitHub/Cloudflare. deploy uploads only after a separate
operator invocation. observe performs explicitly requested live release checks.
render formats retained observations without probing or changing deployment.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

from assurance import canonical, package_digest, validate_receipt
from release_package import REPOSITORY, WORKFLOW, WRANGLER_VERSION, canonical_configuration, read_json, sha, verify_directory, write_json

ROOT = Path(__file__).resolve().parents[1]
API = "repos/" + REPOSITORY
LIVE_URL = "https://ai-software-toolkit-reference-app.navivision-account.workers.dev"
MAX_ARCHIVE = 128 * 1024 * 1024
MAX_UNCOMPRESSED = 512 * 1024 * 1024
LIVE_CHECKS = {"exact-health-identity", "anonymous-and-origin-boundaries", "editor-create-and-input-boundaries", "search-and-priority-filters", "status-comment-and-reload-persistence", "repository-link-and-keyboard-focus", "viewer-api-permissions-and-board-isolation", "mobile-viewer-and-layout", "compact-mobile-layout"}
LIVE_IMAGES = {"desktop-editor-board.png", "desktop-editor-detail.png", "mobile-viewer-board.png", "compact-mobile-board.png"}
REQUIRED_STEPS = {"Stage immutable Worker package", "Release package regressions", "Run npm run test:e2e", "Check frozen package after acceptance", "Retain verified Worker package"}


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def safe_output(path: Path) -> None:
    absolute = path.absolute()
    require(not any(parent.is_symlink() for parent in (absolute, *absolute.parents)), "Output path may not traverse a symlink")
    require(not path.exists(), "Preserve existing output; choose a new directory")


def private_output(path: Path) -> None:
    safe_output(path)
    absolute = path.absolute()
    if absolute.is_relative_to(ROOT):
        require(absolute.relative_to(ROOT).parts[:1] == (".artifacts",), "Private promotion records inside this checkout belong under .artifacts")


def checked_archive_bytes(path: Path, digest: str) -> bytes:
    require(not path.is_symlink() and path.is_file(), "Archive must be a regular file")
    with path.open("rb") as stream:
        content = stream.read(MAX_ARCHIVE + 1)
    require(len(content) <= MAX_ARCHIVE and "sha256:" + hashlib.sha256(content).hexdigest() == digest, "Prepared/downloaded archive bytes changed or digest differs")
    return content


def instant(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.tzinfo is not None, "Timezone required")
    return result


def api(endpoint: str):
    return json.loads(subprocess.check_output(["gh", "api", API + "/" + endpoint]))


def github_write(endpoint: str, value: dict, request: Path) -> dict:
    write_json(request, value)
    return json.loads(subprocess.check_output(["gh", "api", "--method", "POST", API + "/" + endpoint, "--input", str(request)]))


def validate_run(run: dict, workflow: dict) -> None:
    require(run.get("repository", {}).get("full_name") == REPOSITORY and run.get("head_repository", {}).get("full_name") == REPOSITORY, "Run must belong to this repository")
    require(run.get("event") == "push" and run.get("head_branch") == "main", "Only a main-push package can be promoted")
    require(run.get("status") == "completed" and run.get("conclusion") == "success", "Run must have completed successfully")
    require(run.get("path") == WORKFLOW and run.get("workflow_id") == workflow.get("id") and workflow.get("path") == WORKFLOW and workflow.get("state") == "active", "Wrong acceptance workflow")
    require(type(run.get("id")) is int and run["id"] > 0 and type(run.get("run_attempt")) is int and run["run_attempt"] > 0, "Run/attempt identity missing")
    require(re.fullmatch(r"[0-9a-f]{40}", run.get("head_sha", "")) is not None, "Full source revision required")


def validate_artifact(artifact: dict, run: dict, *, now: datetime | None = None) -> None:
    clock = now or datetime.now(timezone.utc)
    require(artifact.get("name") == "worker-release-" + run["head_sha"], "Wrong package artifact name")
    require(type(artifact.get("id")) is int and artifact["id"] > 0 and artifact.get("expired") is False and instant(artifact["expires_at"]) > clock, "Artifact missing or expired")
    require(type(artifact.get("size_in_bytes")) is int and 0 < artifact["size_in_bytes"] <= MAX_ARCHIVE, "Archive size exceeds policy")
    require(re.fullmatch(r"sha256:[0-9a-f]{64}", artifact.get("digest", "")) is not None, "Artifact archive digest missing")
    association = artifact.get("workflow_run", {})
    require(association.get("id") == run["id"] and association.get("head_sha") == run["head_sha"] and association.get("head_branch") == "main", "Artifact/run association differs")
    require(association.get("repository_id") == run["repository"]["id"] and association.get("head_repository_id") == run["head_repository"]["id"], "Artifact repository identity differs")


def validate_jobs(jobs: list, run: dict) -> None:
    candidates = [j for j in jobs if j.get("name") == "Application acceptance"]
    require(len(candidates) == 1, "Acceptance job missing or ambiguous")
    job = candidates[0]
    require(job.get("status") == "completed" and job.get("conclusion") == "success" and job.get("head_sha") == run["head_sha"] and job.get("run_id") == run["id"], "Acceptance job source or conclusion differs")
    require(job.get("run_attempt", run["run_attempt"]) == run["run_attempt"], "Wrong job attempt")
    for name in REQUIRED_STEPS:
        steps = [s for s in job.get("steps", []) if s.get("name") == name]
        require(len(steps) == 1 and steps[0].get("status") == "completed" and steps[0].get("conclusion") == "success", "Required package step did not pass: " + name)


def safe_extract(archive: Path | bytes, destination: Path) -> None:
    safe_output(destination)
    with zipfile.ZipFile(io.BytesIO(archive) if isinstance(archive, bytes) else archive) as zipped:
        entries = zipped.infolist()
        require(0 < len(entries) <= 20100 and sum(e.file_size for e in entries) <= MAX_UNCOMPRESSED, "Archive membership/size exceeds policy")
        names = set()
        for entry in entries:
            raw = entry.filename.rstrip("/")
            parts = raw.split("/")
            require(raw and entry.orig_filename == entry.filename and not raw.startswith("/") and "\\" not in raw and ":" not in raw and all(p not in {"", ".", ".."} for p in parts) and all(ord(c) >= 32 for c in raw), "Unsafe archive path")
            require(raw not in names, "Duplicate archive path")
            names.add(raw)
            kind = stat.S_IFMT(entry.external_attr >> 16)
            require((entry.is_dir() and kind in {0, stat.S_IFDIR}) or (not entry.is_dir() and kind in {0, stat.S_IFREG}), "Unsupported archive member type")
            require(entry.file_size <= 64 * 1024 * 1024 and not entry.flag_bits & 1, "Oversized or encrypted member")
            require(parts[0] in {"payload", "candidate.json", "package-manifest.json", "verification.json"}, "Unexpected artifact root member")
            require((parts[0] == "payload" and (len(parts) > 1 or entry.is_dir())) or (len(parts) == 1 and not entry.is_dir()), "Unexpected root structure")
            if parts[0] != "payload":
                require(entry.file_size <= 2 * 1024 * 1024, "Metadata document too large")
        destination.mkdir(parents=True)
        for entry in entries:
            target = destination / entry.filename
            if entry.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with zipped.open(entry) as source, target.open("xb") as output:
                    while block := source.read(65536):
                        output.write(block)
                target.chmod(0o644)


def validate_test_record(package: Path, run: dict) -> dict:
    verified = verify_directory(package)
    record = read_json(package / "verification.json")
    require(record.get("version") == 1 and record.get("kind") == "package-test-evidence", "Unsupported package evidence record")
    require(record.get("repository") == REPOSITORY and record.get("workflow_path") == WORKFLOW and record.get("event") == "push" and record.get("ref") == "refs/heads/main", "Package receipt context differs")
    require(record.get("run_id") == run["id"] and record.get("run_attempt") == run["run_attempt"], "Stale run-attempt receipt")
    require(record.get("source_revision") == run["head_sha"] == verified["manifest"]["source"]["revision"], "Package source differs")
    require(record.get("manifest_sha256") == verified["manifest_sha256"] and record.get("package_digest") == verified["package_digest"], "Package receipt content identity differs")
    require(instant(run["created_at"]) <= instant(record["observed_at_utc"]) <= instant(run["updated_at"]), "Package observation lies outside run lifetime")
    expected = {"build", "package", "unit_tests", "migrations", "repository", "checkpoint_tests", "package_tests", "e2e"}
    require(set(record.get("steps", {})) == expected and all(s == {"outcome": "success", "conclusion": "success"} for s in record["steps"].values()), "Package test outcomes incomplete or unsuccessful")
    return verified


def source_configuration(run: dict) -> dict:
    content = api("contents/wrangler.jsonc?ref=" + run["head_sha"])
    require(content.get("encoding") == "base64" and content.get("size", MAX_ARCHIVE) < 65536, "Source configuration unavailable")
    raw = base64.b64decode(content["content"], validate=False)
    return canonical_configuration(json.loads(raw), run["head_sha"])


def inspect_platform(run_id: int) -> tuple[dict, dict]:
    require(type(run_id) is int and run_id > 0, "Positive run ID required")
    run = api(f"actions/runs/{run_id}")
    validate_run(run, api("actions/workflows/acceptance.yml"))
    require(type(run.get("check_suite_id")) is int and run["check_suite_id"] > 0, "Run check-suite identity missing")
    suite = api(f"check-suites/{run['check_suite_id']}")
    require(suite.get("app", {}).get("id") == 15368 and suite.get("head_sha") == run["head_sha"] and suite.get("repository", {}).get("id") == run["repository"]["id"] and suite.get("status") == "completed" and suite.get("conclusion") == "success", "GitHub Actions application/source identity differs")
    compare = api("compare/" + run["head_sha"] + "...main")
    require(compare.get("status") in {"ahead", "identical"} and compare.get("merge_base_commit", {}).get("sha") == run["head_sha"], "Run source is not retained on main")
    listing = api(f"actions/runs/{run_id}/artifacts?per_page=100")
    require(listing.get("total_count", 101) <= 100, "Ambiguous oversized artifact listing")
    matches = [a for a in listing.get("artifacts", []) if a.get("name") == "worker-release-" + run["head_sha"]]
    require(len(matches) == 1, "Package artifact missing or ambiguous")
    artifact = matches[0]
    validate_artifact(artifact, run)
    jobs = api(f"actions/runs/{run_id}/attempts/{run['run_attempt']}/jobs?per_page=100")
    require(jobs.get("total_count", 101) <= 100, "Oversized job listing")
    validate_jobs(jobs.get("jobs", []), run)
    return run, artifact


def verify_source(package: Path, run: dict) -> dict:
    verified = validate_test_record(package, run)
    commit = api("git/commits/" + run["head_sha"])
    require(commit.get("tree", {}).get("sha") == verified["manifest"]["source"]["tree"], "Package source tree differs")
    require(read_json(package / "payload/deploy-config.json") == source_configuration(run), "Packaged deployment configuration differs from reviewed source")
    return verified


def prepare(run_id: int, output: Path) -> dict:
    private_output(output)
    run, artifact = inspect_platform(run_id)
    output.mkdir(parents=True)
    archive = output / "artifact.zip"
    with archive.open("xb") as stream:
        subprocess.run(["gh", "api", API + f"/actions/artifacts/{artifact['id']}/zip"], stdout=stream, check=True)
    content = checked_archive_bytes(archive, artifact["digest"])
    safe_extract(content, output / "package")
    verified = verify_source(output / "package", run)
    report = {"version": 1, "kind": "promotion-preparation", "observed_at_utc": datetime.now(timezone.utc).isoformat(), "repository": REPOSITORY, "source_revision": run["head_sha"], "run_id": run["id"], "run_attempt": run["run_attempt"], "run_url": run["html_url"], "workflow_path": WORKFLOW, "artifact_id": artifact["id"], "artifact_name": artifact["name"], "archive_digest": artifact["digest"], "package_digest": verified["package_digest"], "manifest_sha256": verified["manifest_sha256"], "state": "verified-awaiting-separate-deployment-authorization", "native_build_provenance": False, "limits": "Successful same-repository main-run/platform and downloaded byte identities were checked. This preparation authorizes no upload, deployment or publication and is not a signed build attestation."}
    write_json(output / "promotion.json", report)
    return report


def wrangler(command: list[str], *, config: Path, log: Path, cwd: Path) -> str:
    require(read_json(ROOT / "node_modules/wrangler/package.json").get("version") == WRANGLER_VERSION, "Install the reviewed pinned Wrangler before deployment")
    args = ["node", str(ROOT / "node_modules/wrangler/bin/wrangler.js"), *command, "--config", str(config)]
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    require(result.returncode == 0, "Wrangler operation failed; inspect retained private log without exposing credentials")
    return result.stdout


def deploy(prepared: Path, output: Path) -> dict:
    private_output(output)
    require(re.fullmatch(r"v24\.[0-9]+\.[0-9]+", subprocess.check_output(["node", "--version"], text=True).strip()) is not None, "Use the reviewed Node 24 deployment runtime")
    selected = read_json(prepared / "promotion.json")
    require(selected.get("version") == 1 and selected.get("kind") == "promotion-preparation" and selected.get("state") == "verified-awaiting-separate-deployment-authorization", "Unsupported promotion preparation")
    run, artifact = inspect_platform(selected["run_id"])
    require(selected.get("artifact_id") == artifact["id"] and selected.get("archive_digest") == artifact["digest"], "Prepared artifact selection changed")
    archive = prepared / "artifact.zip"
    content = checked_archive_bytes(archive, artifact["digest"])
    require(subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain"], text=True) == "", "Deployment tool checkout must be clean")
    require(subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip() == api("git/ref/heads/main")["object"]["sha"], "Deployment tool must be reviewed current main")
    output.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix="fieldnotes-promotion-") as temporary:
        package = Path(temporary).resolve() / "package"
        # Extraction reads the exact bytes hashed above, even if the path changes.
        safe_extract(content, package)
        verified = verify_source(package, run)
        require(verified["package_digest"] == selected.get("package_digest") and verified["manifest_sha256"] == selected.get("manifest_sha256"), "Prepared package identity changed")
        payload = package / "payload"
        config = payload / "deploy-config.json"
        configuration = read_json(config)
        account = wrangler(["whoami"], config=config, log=output / "account-private.log", cwd=payload)
        require(configuration["account_id"] in account, "Expected Cloudflare account unavailable")
        migrations = wrangler(["d1", "migrations", "list", "DB", "--remote"], config=config, log=output / "migrations-private.log", cwd=payload)
        require("No migrations to apply!" in migrations, "Pending D1 migrations require separate reviewed authorization")
        before = json.loads(wrangler(["deployments", "list", "--json"], config=config, log=output / "before-deployments-private.log", cwd=payload))
        previous = max(before, key=lambda d: d["created_on"])
        # Recheck platform/source selection and frozen bytes immediately before upload.
        current_run, current_artifact = inspect_platform(run["id"])
        require(current_run["run_attempt"] == run["run_attempt"] and current_artifact["id"] == artifact["id"] and current_artifact["digest"] == artifact["digest"], "Platform package selection changed during preflight")
        verify_directory(package, expected_manifest=verified["manifest_sha256"])
        record = {"version": 1, "kind": "package-deployment-observation", "state": "upload-started", "observed_at_utc": datetime.now(timezone.utc).isoformat(), "repository": REPOSITORY, "source_revision": run["head_sha"], "toolkit_revision": configuration["vars"]["TOOLKIT_REVISION"], "package_digest": verified["package_digest"], "manifest_sha256": verified["manifest_sha256"], "configuration_digest": verified["manifest"]["configuration"]["sha256"], "artifact_id": artifact["id"], "archive_digest": artifact["digest"], "run_id": run["id"], "run_attempt": run["run_attempt"], "run_url": run["html_url"], "environment_url": LIVE_URL, "rollback": {"deployment_id": previous["id"], "versions": previous["versions"], "limits": "Code/configuration rollback does not reverse D1 contents."}, "migrations_applied": False, "live_pilot": "unverified", "limits": "Upload-to-version is a Wrangler/platform observation, not remote code execution attestation. Live API/browser verification is a separate explicit operation."}
        github_deployment = github_write("deployments", {"ref": run["head_sha"], "auto_merge": False, "required_contexts": ["Application acceptance"], "environment": "production", "description": "Manual promotion of the independently verified CI Worker package; live observations pending.", "transient_environment": False, "production_environment": True}, output / "github-deployment-request.json")
        require(github_deployment.get("sha") == run["head_sha"] and github_deployment.get("environment") == "production", "GitHub production deployment identity differs")
        record["github_deployment_id"] = github_deployment["id"]
        github_status_path = f"deployments/{github_deployment['id']}/statuses"
        github_write(github_status_path, {"state": "in_progress", "description": "Manual verified-package upload; live verification remains separate.", "environment_url": LIVE_URL, "log_url": run["html_url"], "auto_inactive": False}, output / "github-in-progress-request.json")
        write_json(output / "deployment.json", record)
        try:
            response = wrangler(["deploy", "--no-bundle", "--autoconfig=false", "--message", "git:" + run["head_sha"]], config=config, log=output / "deploy-private.log", cwd=payload)
            match = re.search(r"Current Version ID:\s*([0-9a-f-]{36})", response)
            require(match is not None, "Upload may have completed; Worker version could not be parsed. Inspect without retrying automatically")
            deployments = json.loads(wrangler(["deployments", "list", "--json"], config=config, log=output / "after-deployments-private.log", cwd=payload))
            verify_directory(package, expected_manifest=verified["manifest_sha256"])
            latest = max(deployments, key=lambda d: d["created_on"])
            require(latest.get("annotations", {}).get("workers/message") == "git:" + run["head_sha"] and latest.get("versions") == [{"version_id": match[1], "percentage": 100}], "Serving deployment/version/traffic differs")
            record.update(state="deployed-awaiting-live-verification", worker_version=match[1], cloudflare_deployment_id=latest["id"], traffic_percentage=100, observed_at_utc=datetime.now(timezone.utc).isoformat())
        except Exception:
            record["state"] = "upload-or-verification-incomplete"
            write_json(output / "deployment.json", record)
            try:
                github_write(github_status_path, {"state": "failure", "description": "Package upload or version/traffic verification incomplete; inspect retained evidence.", "environment_url": LIVE_URL, "log_url": run["html_url"], "auto_inactive": False}, output / "github-failure-request.json")
            except (ValueError, OSError, subprocess.SubprocessError):
                record["github_failure_status_update"] = "unverified"
                write_json(output / "deployment.json", record)
            raise
        write_json(output / "deployment.json", record)
        write_checkpoint(output / "deployment-receipt.json", output / "deployment.json", record, checkpoint="deployment")
    return record


def observe(deployment: Path, output: Path, *, valid_for_seconds: int = 3600) -> dict:
    private_output(output)
    require(type(valid_for_seconds) is int and 1 <= valid_for_seconds <= 86400, "Observation freshness must be 1..86400 seconds")
    record = read_json(deployment)
    require(record.get("version") == 1 and record.get("kind") == "package-deployment-observation" and record.get("state") == "deployed-awaiting-live-verification" and record.get("environment_url") == LIVE_URL and record.get("traffic_percentage") == 100, "Verified deployment inventory required before live observations")
    github_deployment = api("deployments/" + str(record["github_deployment_id"]))
    require(github_deployment.get("sha") == record["source_revision"] and github_deployment.get("environment") == "production", "GitHub production deployment subject differs")
    output.mkdir(parents=True)
    environment = {key: os.environ[key] for key in ("PATH", "HOME", "SYSTEMROOT", "TMPDIR", "TMP", "TEMP", "LANG", "LC_ALL", "TZ", "PLAYWRIGHT_BROWSERS_PATH") if key in os.environ}
    environment.update(APP_URL=LIVE_URL, APP_REVISION=record["source_revision"])
    with (output / "release-smoke.json").open("w", encoding="utf-8") as stream:
        subprocess.run(["node", str(ROOT / "scripts/smoke.mjs")], env=environment, stdout=stream, check=True)
    smoke = read_json(output / "release-smoke.json")
    require(smoke.get("revision") == record["source_revision"] and smoke.get("toolkitRevision") == record["toolkit_revision"] and smoke.get("workerVersion") == record["worker_version"], "Live health does not match package deployment")
    with (output / "browser-private.log").open("w", encoding="utf-8") as stream:
        subprocess.run(["node", str(ROOT / "scripts/observe_release.mjs"), "--deployment", str(deployment.resolve()), "--output", str(output.resolve())], env=environment, stdout=stream, stderr=subprocess.STDOUT, check=True)
    browser = read_json(output / "browser-observations.json")
    require(browser.get("status") == "passed" and browser.get("source_revision") == record["source_revision"] and browser.get("worker_version") == record["worker_version"] and browser.get("toolkit_revision") == record["toolkit_revision"], "Browser observations incomplete or wrong-subject")
    observed = {"version": 1, "kind": "package-live-observations", "state": "verified-at-observation-time", "observed_at_utc": browser["observed_at_utc"], "environment_url": LIVE_URL, "source_revision": record["source_revision"], "toolkit_revision": record["toolkit_revision"], "worker_version": record["worker_version"], "package_digest": record["package_digest"], "manifest_sha256": record["manifest_sha256"], "configuration_digest": record["configuration_digest"], "artifact_id": record["artifact_id"], "archive_digest": record["archive_digest"], "run_id": record["run_id"], "run_attempt": record["run_attempt"], "run_url": record["run_url"], "cloudflare_deployment_id": record["cloudflare_deployment_id"], "github_deployment_id": record["github_deployment_id"], "traffic_percentage": record["traffic_percentage"], "release_smoke": smoke, "browser": browser, "limits": "Bounded synthetic live health/API/UI observations, not local PR QA or future availability. They do not create a Proof policy pass or establish native build provenance."}
    validate_live_record(observed)
    status = github_write(f"deployments/{record['github_deployment_id']}/statuses", {"state": "success", "description": "Verified package identity, live health/API and desktop/mobile browser flows at observation time.", "environment_url": LIVE_URL, "log_url": record["run_url"], "auto_inactive": True}, output / "github-success-request.json")
    observed["github_success_status_id"] = status["id"]
    write_json(output / "live-observations.json", observed)
    write_checkpoint(output / "runtime-receipt.json", output / "live-observations.json", observed, checkpoint="runtime", valid_for_seconds=valid_for_seconds)
    return observed


def write_checkpoint(destination: Path, evidence: Path, record: dict, *, checkpoint: str, valid_for_seconds: int = 3600) -> None:
    require(not destination.exists(), "Checkpoint receipt already exists")
    runtime = checkpoint == "runtime"
    identity = {key: record[key] for key in ("source_revision", "worker_version", "package_digest", "cloudflare_deployment_id")}
    reference = {"path": evidence.name, "sha256": sha(evidence), "size": evidence.stat().st_size}
    receipt = {"version": 1, "kind": "checkpoint-receipt", "checkpoint": checkpoint,
               "subject": {"type": "environment", "revision": "sha256:" + hashlib.sha256(canonical(identity)).hexdigest()},
               "observed_at": record["observed_at_utc"], "context": {"invocation": "manual:package-" + checkpoint, "repository": REPOSITORY, "run_url": record["run_url"], "run_id": str(record["run_id"]), "run_attempt": str(record["run_attempt"])},
               "dependencies": {"source_revision": record["source_revision"], "configuration_digest": record["configuration_digest"]},
               "results": [{"check": "live-health-api" if runtime else "package-upload", "provider": "release-observations" if runtime else "wrangler", "status": "passed", "evidence": [evidence.name]},
                           {"check": "live-browser", "provider": "release-observations", **({"status": "passed", "evidence": [evidence.name]} if runtime else {"status": "not_run", "reason": "Separate explicit live verification has not run."})}],
               "evidence_refs": [reference], "relationships": [{"relation": "observed" if runtime else "deployed", "subject": {"type": "artifact", "revision": "sha256:" + record["package_digest"]}, "evidence": evidence.name}],
               "platform_requirements": ["Operator authorization remains separate from receipt integrity."]}
    if runtime:
        receipt["expires_at"] = (instant(record["observed_at_utc"]) + timedelta(seconds=valid_for_seconds)).isoformat()
    validate_receipt(receipt)
    write_json(destination, receipt)


def validate_live_record(record: dict) -> None:
    require(record.get("version") == 1 and record.get("kind") == "package-live-observations" and record.get("state") == "verified-at-observation-time" and record.get("environment_url") == LIVE_URL, "Complete live record required")
    for key, length in (("source_revision", 40), ("toolkit_revision", 40), ("package_digest", 64), ("manifest_sha256", 64), ("configuration_digest", 64)):
        require(re.fullmatch(r"[0-9a-f]{" + str(length) + "}", record.get(key, "")) is not None, "Invalid live record content identity")
    require(re.fullmatch(r"[0-9a-f-]{36}", record.get("worker_version", "")) is not None and re.fullmatch(r"[0-9a-f-]{36}", record.get("cloudflare_deployment_id", "")) is not None, "Invalid platform version identity")
    for key in ("artifact_id", "run_id", "run_attempt", "github_deployment_id"):
        require(type(record.get(key)) is int and record[key] > 0, "Invalid platform identifier")
    require(record.get("run_url") == "https://github.com/" + REPOSITORY + "/actions/runs/" + str(record["run_id"]), "Unexpected evidence URL")
    require(re.fullmatch(r"sha256:[0-9a-f]{64}", record.get("archive_digest", "")) is not None and record.get("traffic_percentage") == 100, "Archive/traffic identity missing")
    instant(record["observed_at_utc"])
    smoke = record.get("release_smoke", {})
    require(smoke.get("status") == "passed" and smoke.get("revision") == record["source_revision"] and smoke.get("toolkitRevision") == record["toolkit_revision"] and smoke.get("workerVersion") == record["worker_version"], "Wrong-subject release smoke")
    require(smoke.get("checks") == ["database health", "isolated session", "create issue", "transition", "persist comment"], "Incomplete release API observations")
    browser = record.get("browser", {})
    require(browser.get("status") == "passed" and browser.get("source_revision") == record["source_revision"] and browser.get("toolkit_revision") == record["toolkit_revision"] and browser.get("worker_version") == record["worker_version"] and browser.get("observed_at_utc") == record["observed_at_utc"] and browser.get("page_errors") == [], "Wrong-subject/incomplete browser observations")
    checks = browser.get("checks", [])
    require(len(checks) == len(LIVE_CHECKS) and {c.get("name") for c in checks} == LIVE_CHECKS and all(set(c) == {"name", "status"} and c["status"] == "passed" for c in checks), "Missing or unsuccessful browser flow")
    images = browser.get("screenshots", [])
    require(len(images) == len(LIVE_IMAGES) and {i.get("file") for i in images} == LIVE_IMAGES, "Original screenshot inventory incomplete")
    for image in images:
        require(set(image) == {"file", "sha256", "width", "height"} and re.fullmatch(r"[0-9a-f]{64}", image.get("sha256", "")) is not None and type(image.get("width")) is int and type(image.get("height")) is int and 1 <= image["width"] <= 2048 and 1 <= image["height"] <= 10000, "Invalid screenshot identity")


def render(observations: Path, output: Path) -> dict:
    safe_output(output)
    record = read_json(observations)
    validate_live_record(record)
    output.mkdir(parents=True)
    public = {key: record[key] for key in ("version", "kind", "state", "observed_at_utc", "environment_url", "source_revision", "toolkit_revision", "worker_version", "package_digest", "artifact_id", "archive_digest", "run_id", "run_attempt", "run_url", "cloudflare_deployment_id", "github_deployment_id", "traffic_percentage")}
    public["release_smoke"] = {k: record["release_smoke"][k] for k in ("status", "revision", "toolkitRevision", "workerVersion", "checks")}
    public["limits"] = "Retained bounded live release observations, not new probes, local PR QA, future availability or native build provenance. Formatting validates local structure and bytes; it does not independently authenticate platform or producer claims."
    public["browser"] = {k: record["browser"][k] for k in ("status", "observed_at_utc", "source_revision", "toolkit_revision", "worker_version", "checks", "screenshots", "page_errors")}
    for image in public["browser"]["screenshots"]:
        name = image["file"]
        require(re.fullmatch(r"[a-z0-9-]+\.png", name) is not None, "Unsafe screenshot reference")
        source = observations.parent / "screenshots" / name
        require(not source.is_symlink() and source.stat().st_size <= 16 * 1024 * 1024 and source.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n" and sha(source) == image["sha256"], "Original screenshot bytes differ")
        target = output / "screenshots" / name
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(source.read_bytes())
    write_json(output / "verification.json", public)
    summary = f"# Package deployment verification\n\nRecorded at `{record['observed_at_utc']}`. This document formats prior live observations; it does not deploy or reverify anything.\n\nApp `{record['source_revision']}`; toolkit `{record['toolkit_revision']}`.\nPackage `sha256:{record['package_digest']}` from successful hosted [run]({record['run_url']}), artifact `{record['artifact_id']}`, archive `{record['archive_digest']}`.\nWorker `{record['worker_version']}`, Cloudflare deployment `{record['cloudflare_deployment_id']}`, recorded traffic {record['traffic_percentage']}%.\n\nLive health, release API persistence/permissions, and desktop/mobile UI passed at that observation time. [Sanitized data](verification.json).\n\n"
    summary += "\n".join(f"- [{image['file']}](screenshots/{image['file']})" for image in public["browser"]["screenshots"])
    summary += "\n\nChecks optional, Core advisory, lifecycle/polyglot manual. Package integrity is not signed build provenance or exhaustive application certification. Formatting validates retained bytes without independently authenticating their producer. Later documentation CI does not update this observation time.\n"
    (output / "verification.md").write_text(summary, encoding="utf-8")
    return {"recorded_observation": record["observed_at_utc"], "source_revision": record["source_revision"], "new_live_checks": False, "output": str(output)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("prepare")
    command.add_argument("--run-id", required=True, type=int)
    command.add_argument("--output", required=True, type=Path)
    command = commands.add_parser("deploy")
    command.add_argument("--prepared", required=True, type=Path)
    command.add_argument("--output", required=True, type=Path)
    command = commands.add_parser("observe")
    command.add_argument("--deployment", required=True, type=Path)
    command.add_argument("--output", required=True, type=Path)
    command.add_argument("--valid-for-seconds", type=int, default=3600)
    command = commands.add_parser("render")
    command.add_argument("--observations", required=True, type=Path)
    command.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = prepare(args.run_id, args.output) if args.command == "prepare" else deploy(args.prepared, args.output) if args.command == "deploy" else observe(args.deployment, args.output, valid_for_seconds=args.valid_for_seconds) if args.command == "observe" else render(args.observations, args.output)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError, zipfile.BadZipFile) as error:
        print("ERROR " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
