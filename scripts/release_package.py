#!/usr/bin/env python3
"""Build and inspect Fieldnotes' immutable CI package; never deploy it."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone

from assurance import package_digest, verify_package

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "ravisingh11/ai-software-toolkit-reference-app"
WORKFLOW = ".github/workflows/acceptance.yml"
WRANGLER_VERSION = "4.151.2"
CONFIG_KEYS = {"$schema", "name", "main", "compatibility_date", "account_id", "assets", "d1_databases", "version_metadata", "vars", "observability"}
ARTIFACT_FILES = {"package-manifest.json", "candidate.json", "verification.json"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o644)


def git(root: Path, *arguments: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *arguments], text=True).strip()


def canonical_configuration(config: dict, revision: str) -> dict:
    """Only the reviewed application's existing binding/configuration surface."""
    if not isinstance(config, dict) or set(config) - CONFIG_KEYS:
        raise ValueError("Review new Wrangler configuration keys before packaging")
    result = json.loads(json.dumps(config))
    result.pop("$schema", None)
    if result.get("name") != "ai-software-toolkit-reference-app":
        raise ValueError("Wrong Worker application")
    if result.get("main") != "src/index.ts":
        raise ValueError("Unexpected source entrypoint")
    assets = result.get("assets", {})
    if assets.get("directory") != "./public" or assets.get("binding") != "ASSETS":
        raise ValueError("Unexpected static asset binding")
    bindings = result.get("d1_databases", [])
    if len(bindings) != 1 or bindings[0].get("binding") != "DB" or bindings[0].get("migrations_dir") != "migrations":
        raise ValueError("Unexpected D1 migration/configuration surface")
    if set(result.get("vars", {})) != {"APP_REVISION", "TOOLKIT_REVISION"}:
        raise ValueError("Package may contain only the two non-secret revision variables")
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Full immutable source revision required")
    if not re.fullmatch(r"[0-9a-f]{40}", result["vars"]["TOOLKIT_REVISION"]):
        raise ValueError("Immutable toolkit revision required")
    result["main"] = "worker/index.js"
    result["no_bundle"] = True
    result["assets"]["directory"] = "public"
    result["vars"]["APP_REVISION"] = revision
    return result


def copy_tree(source: Path, destination: Path) -> None:
    if source.is_symlink() or not source.is_dir():
        raise ValueError("Expected a regular source directory")
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise ValueError("Package source may not contain symlinks")
        if path.is_file():
            relative = path.relative_to(source)
            if any(part in {"node_modules", ".git", ".env", ".dev.vars"} or part.startswith((".env.", ".dev.vars.")) for part in relative.parts):
                raise ValueError("Private/dependency content cannot enter the package")
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            target.chmod(0o644)


def stage(root: Path, output: Path) -> dict:
    if output.exists() or output.is_symlink():
        raise ValueError("Preserve existing package output; use a new directory")
    revision = git(root, "rev-parse", "HEAD")
    tree = git(root, "rev-parse", "HEAD^{tree}")
    config = canonical_configuration(read_json(root / "wrangler.jsonc"), revision)
    lock = read_json(root / "toolkit.lock.json")
    if config["vars"]["TOOLKIT_REVISION"] != lock["revision"]:
        raise ValueError("Toolkit source pins disagree")
    if read_json(root / "package.json")["devDependencies"]["wrangler"] != WRANGLER_VERSION:
        raise ValueError("Review the deployment-tool version before changing the package contract")
    if not (root / "dist/index.js").is_file():
        raise ValueError("Build the Worker once before packaging")
    output.mkdir(parents=True)
    payload = output / "payload"
    payload.mkdir()
    copy_tree(root / "dist", payload / "worker")
    copy_tree(root / "public", payload / "public")
    copy_tree(root / "migrations", payload / "migrations")
    write_json(payload / "deploy-config.json", config)
    files = []
    for path in sorted(payload.rglob("*")):
        if path.is_file():
            files.append({"path": path.relative_to(payload).as_posix(), "size": path.stat().st_size, "sha256": sha(path), "mode": "0755" if path.stat().st_mode & stat.S_IXUSR else "0644"})
    manifest = {"version": 1, "kind": "package-manifest", "source": {"repository": "https://github.com/" + REPOSITORY, "revision": revision, "tree": tree}, "build": {"tool": "wrangler", "version": WRANGLER_VERSION}, "configuration": {"path": "deploy-config.json", "sha256": sha(payload / "deploy-config.json")}, "files": files}
    write_json(output / "package-manifest.json", manifest)
    initial = {"version": 1, "kind": "package-candidate", "source_revision": revision, "manifest_sha256": sha(output / "package-manifest.json"), "package_digest": package_digest(manifest)}
    write_json(output / "candidate.json", initial)
    verify_directory(output, expected_manifest=initial["manifest_sha256"])
    return initial


def verify_directory(package: Path, *, expected_manifest: str | None = None) -> dict:
    if package.is_symlink() or not package.is_dir():
        raise ValueError("Package must be a regular directory")
    if any(p.is_symlink() for p in package.rglob("*")):
        raise ValueError("Package may not contain symlinks")
    unexpected = {p.name for p in package.iterdir()} - ARTIFACT_FILES - {"payload"}
    if unexpected:
        raise ValueError("Unexpected artifact root members")
    manifest_path = package / "package-manifest.json"
    manifest = read_json(manifest_path)
    if expected_manifest is not None and (not re.fullmatch(r"[0-9a-f]{64}", expected_manifest) or sha(manifest_path) != expected_manifest):
        raise ValueError("Frozen manifest changed after the build")
    verify_package(package / "payload", manifest)
    candidate = read_json(package / "candidate.json")
    if candidate != {"version": 1, "kind": "package-candidate", "source_revision": manifest["source"]["revision"], "manifest_sha256": sha(manifest_path), "package_digest": package_digest(manifest)}:
        raise ValueError("Candidate record does not describe the verified package")
    config = read_json(package / "payload/deploy-config.json")
    source_config = dict(config, main="src/index.ts")
    source_config.pop("no_bundle", None)
    source_config["assets"] = dict(config["assets"], directory="./public")
    if canonical_configuration(source_config, manifest["source"]["revision"]) != config:
        raise ValueError("Incompatible packaged deployment configuration")
    if manifest["source"]["repository"] != "https://github.com/" + REPOSITORY or manifest["build"] != {"tool": "wrangler", "version": WRANGLER_VERSION}:
        raise ValueError("Unexpected package repository or builder")
    for name in ("worker/index.js", "public/index.html", "public/app.js", "public/styles.css"):
        if not (package / "payload" / name).is_file():
            raise ValueError("Required compiled Worker/static file missing")
    if not list((package / "payload/migrations").glob("*.sql")):
        raise ValueError("Migration inventory missing")
    return {"manifest": manifest, "manifest_sha256": sha(manifest_path), "package_digest": package_digest(manifest)}


def seal(package: Path, expected_manifest: str, *, environment: dict[str, str] | None = None) -> dict:
    env = os.environ if environment is None else environment
    verified = verify_directory(package, expected_manifest=expected_manifest)
    steps = json.loads(env.get("PACKAGE_STEP_RESULTS", "{}"))
    observed = {}
    for name in ("build", "package", "unit_tests", "migrations", "repository", "checkpoint_tests", "package_tests", "e2e"):
        step = steps.get(name, {})
        if step.get("outcome") != "success" or step.get("conclusion") != "success":
            raise ValueError("Package cannot be retained after a failed, skipped or incomplete step: " + name)
        observed[name] = {"outcome": step["outcome"], "conclusion": step["conclusion"]}
    if env.get("GITHUB_REPOSITORY") != REPOSITORY:
        raise ValueError("Wrong repository context")
    for key in ("GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT"):
        if not re.fullmatch(r"[1-9][0-9]*", env.get(key, "")):
            raise ValueError("Hosted run identity missing")
    record = {"version": 1, "kind": "package-test-evidence", "source_revision": verified["manifest"]["source"]["revision"], "manifest_sha256": verified["manifest_sha256"], "package_digest": verified["package_digest"], "repository": REPOSITORY, "workflow_path": WORKFLOW, "run_id": int(env["GITHUB_RUN_ID"]), "run_attempt": int(env["GITHUB_RUN_ATTEMPT"]), "event": env.get("GITHUB_EVENT_NAME"), "ref": env.get("GITHUB_REF"), "observed_at_utc": datetime.now(timezone.utc).isoformat(), "steps": observed, "limits": "Named workflow-step observations only. Final GitHub run conclusion and artifact identity must be verified independently before promotion; this is not native build provenance or deployment evidence."}
    destination = package / "verification.json"
    if destination.exists():
        raise ValueError("Verification receipt already exists; never rewrite it")
    write_json(destination, record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("stage", "verify", "seal"))
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--expected-manifest")
    args = parser.parse_args()
    try:
        if args.command == "stage":
            result = stage(args.root.resolve(), args.package)
            if os.environ.get("GITHUB_OUTPUT"):
                with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
                    stream.write("manifest-sha=" + result["manifest_sha256"] + "\n")
        elif args.command == "seal":
            if not args.expected_manifest:
                raise ValueError("A manifest frozen before tests is required")
            result = seal(args.package, args.expected_manifest)
        else:
            result = verify_directory(args.package, expected_manifest=args.expected_manifest)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print("ERROR " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
