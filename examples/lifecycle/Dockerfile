# Verification-only container for the real Fieldnotes Worker and local D1.
# This is not the production Cloudflare deployment artifact.
FROM node:24-bookworm-slim@sha256:a5f4366e834695d5f363b920c104953a535d3a9864d1bdf74566a0ebe01daee5
ARG PROOF_REVISION
ENV HOME=/tmp/proof-home \
    XDG_CONFIG_HOME=/tmp/proof-home/config \
    WRANGLER_CACHE_DIR=/tmp/proof-cache \
    WRANGLER_REGISTRY_PATH=/tmp/proof-registry \
    WRANGLER_LOG_PATH=/tmp/proof-logs \
    WRANGLER_SEND_METRICS=false \
    WRANGLER_SEND_ERROR_REPORTS=false \
    CI=true
WORKDIR /app
RUN chown 65532:65532 /app
COPY --chown=65532:65532 package.json package-lock.json tsconfig.json worker-configuration.d.ts wrangler.jsonc ./
COPY --chown=65532:65532 src ./src
COPY --chown=65532:65532 public ./public
COPY --chown=65532:65532 migrations ./migrations
COPY --chown=65532:65532 examples/lifecycle ./examples/lifecycle
USER 65532:65532
# Registry access is explicitly opted in by trusted lifecycle configuration.
# No lifecycle/install scripts from dependencies run during installation.
RUN npm ci --ignore-scripts --no-audit --no-fund && npm run build && npm cache clean --force
RUN node -e 'if (!/^[a-f0-9]{40}$/.test(process.argv[1])) process.exit(1); require("fs").writeFileSync("/app/revision", process.argv[1]);' "$PROOF_REVISION"
EXPOSE 8080
ENTRYPOINT ["node", "/app/examples/lifecycle/start.mjs"]
