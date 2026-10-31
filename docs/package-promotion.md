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
