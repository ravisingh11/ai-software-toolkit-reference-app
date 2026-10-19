# Fieldnotes lifecycle verification fixture

This opt-in fixture builds the actual Fieldnotes Worker with the locked Node
packages and starts its built bundle in local Wrangler with the real D1
migrations. It is a verification container, not the deployed Cloudflare Worker.
The lifecycle configuration selects public-registry access during the sandboxed
build; the running container uses the collector's isolated internal network,
read-only filesystem, non-root user, bounded resources and ephemeral `/tmp`.
No production credentials, host dependencies or production database are used.

The Dockerfile-specific ignore file is an allowlist and requires BuildKit.
Use a matching root `.dockerignore` if supporting Docker's legacy builder;
never send a developer checkout's secrets or local D1 state as build context.
The Node base image is pinned to its official multi-platform registry digest.

`PROOF_REVISION` must be a full source SHA. Startup rejects missing identity,
preserves the application's bindings and toolkit revision, replaces the remote
account/database identity with a local database, then verifies that migrations
succeed before serving. The existing `/api/health` endpoint reads the real DB
and returns the injected revision. Missing bindings fail startup.

The configured negative probes require unauthenticated issue/session access to
return 401 with the application's actual security/cache headers. Thirty seconds
of probes is a short endurance smoke, not proof of production stability. The
DAST scanner separately inspects the running application and retains findings.
This fixture does not prove remote deployment approvals, production telemetry,
WAF configuration, or production image security.

Run the fixture configuration regressions with:

```sh
node --test examples/lifecycle/config.test.mjs
```

Actual container build, runtime, scanner and collected scorecard evidence are
separate verification steps. Keep failures and unavailable evidence visible.
The existing polyglot workflow remains manual and independent.
