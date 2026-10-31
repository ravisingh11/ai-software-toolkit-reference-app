# Test and retain one Worker package

This candidate integration is application-owned. The base toolkit remains the
published revision in `toolkit.lock.json`; it is not described as a published
v2.4.0 installation. Checks stay optional, Core advisory, and lifecycle/polyglot
execution stays manual. Existing deployment, skill and hook records retain their
original subjects.

Application acceptance builds the Worker once with pinned Wrangler, then copies
its compiled modules, static assets, migration files and a bounded deployment
configuration into one payload. The package manifest records exact source/tree,
build-tool identity, configuration hash, regular-file membership, sizes, modes
and SHA-256 values. It contains no publication or deployment authorization.

The manifest is outside the payload, so it does not hash itself. Its hash is
frozen as an independent job output before acceptance. Hosted API/browser flows
serve the compiled entrypoint with `--no-bundle`, not the source entrypoint.
A final check compares the frozen manifest and every payload byte again. A
separate receipt retains the named successful workflow-step observations;
publication, final run success and deployment are not inferred from it.

Only successful acceptance retains `worker-release-<actual checkout SHA>` for
30 days. PR packages identify the tested integration checkout. They are not
production candidates. A future manual promotion must independently verify the
same-repository successful push-to-main run, current attempt, workflow, artifact
identity/expiry, inventory and deployment configuration before any upload.
A missing, cancelled, skipped or incomplete result is never a pass.

`APP_PACKAGE_DIR` and `APP_PACKAGE_MANIFEST_SHA` select this compiled-package
path for hosted acceptance. Without those explicit inputs, `scripts/test-server.sh`
keeps ordinary source-based local development behavior. This change installs no
Git hook, automatic deployment, new scanner or branch protection.

The portable package verifier is an exact pinned candidate toolkit source copy
with separate provenance in `scripts/assurance-source.json`. It validates
integrity; it does not authenticate a builder or change Proof scores. Signed
build provenance requires separate trusted-platform verification. The existing
manual production deployment and historical live verification are unchanged;
the live package-promotion handoff remains **unverified** until separately
approved and performed.

## Manual promotion and evidence

The repository's `scripts/release.sh` now requires an explicit subcommand. It
never rebuilds a source checkout, installs dependencies or applies migrations.
Authenticated GitHub artifact read access is needed for preparation. Node 24,
the reviewed pinned Wrangler installation, and an existing authorized Cloudflare
session are prerequisites for deployment. Live browser observations also need
the installed pinned Playwright browser. No mode installs these prerequisites.

First prepare a package from an approved **successful main-push Acceptance run**:

```sh
scripts/release.sh prepare --run-id APPROVED_MAIN_RUN_ID \
  --output .artifacts/v2.4.0-promotion-review
```

Preparation independently checks repository, workflow, main ancestry, final run
conclusion, attempt, named package-step outcomes, unique nonexpired artifact and
its GitHub archive digest. It rejects unsafe ZIP members, symlinks, duplicates,
wrong source/tree and deployment configuration, and changed/missing/extra files.
It reads no Cloudflare credentials and grants no deployment authority. A PR
package is retained for review but is never accepted as a production candidate.

After separate maintainer review and deployment authorization:

```sh
scripts/release.sh deploy --prepared .artifacts/v2.4.0-promotion-review \
  --output .artifacts/v2.4.0-package-upload
```

Deployment requires a clean current-main tool checkout. It revalidates the
platform and archive, freshly extracts verified bytes, verifies the original
source configuration, checks the selected Cloudflare account, and blocks if D1
has pending migrations. Required migrations need their own reviewed procedure;
this command never applies them. It rechecks package identity immediately before
and after upload. Wrangler receives the packaged config and `--no-bundle`; no
source build command is run. Incomplete upload/version/traffic verification
retains an incomplete record and never retries or rolls back automatically.

The resulting deployment receipt links package identity to the platform's Worker
version and 100% traffic observation, while live checks remain `not_run`. This
is a platform observation, not an independent attestation of remotely running
code. The receipt does not satisfy a Proof provider or grant further authority.
GitHub production status remains in progress until separate live observations.

Explicitly verify the live release, then format those retained observations:

```sh
scripts/release.sh observe \
  --deployment .artifacts/v2.4.0-package-upload/deployment.json \
  --output .artifacts/v2.4.0-package-live --valid-for-seconds 3600
scripts/release.sh render \
  --observations .artifacts/v2.4.0-package-live/live-observations.json \
  --output .artifacts/v2.4.0-package-docs
```

`observe` targets only this app's fixed public release URL. It verifies exact
health/source/toolkit/Worker identity, the existing release API smoke, and real
editor/viewer desktop/mobile flows using isolated synthetic expiring boards.
It saves original screenshots without cookies or request bodies. Failure remains
explicit; no retry conceals it. This is release verification, not local PR agent
QA or exhaustive security/load coverage.

The runtime sidecar's default 3600-second freshness window is advisory observation
metadata, configurable from 1 to 86400 seconds. It does not change Proof policy,
provider authority or platform merge requirements. Expiry makes current
applicability stale; the original timestamped historical record remains intact.

`render` reads retained records and original PNGs, preserves their timestamps,
revisions and hashes, and emits sanitized README-ready Markdown/JSON/images. It
runs no producers, network probes or deployment. Copy those outputs through a
reviewed documentation PR; later documentation CI must retain its own revision.
Raw private logs and existing historical evidence stay outside tracked docs.

The compiled-package live pilot is **not yet performed**. Until a maintainer
separately approves and runs these manual operations, its production handoff
remains unverified and the toolkit release candidate remains unpublished.
