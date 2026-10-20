# Verification-only container for the real Fieldnotes Worker and local D1.
# This is not the production Cloudflare deployment artifact.
FROM node:24-trixie-slim@sha256:7f486cabe892bff8fef04c0f7da8dba84a560be3e4e2740b7a86afc57ebec315
# Patch the vendor npm toolchain before switching HOME/user for the application.
ADD --checksum=sha256:dd77c48eb845f4856c2cdba347cfb52bd877a2655a1ea48ff0c4796e3df9dd7b https://registry.npmjs.org/npm/-/npm-11.21.1.tgz /tmp/npm-11.21.1.tgz
RUN npm install --global --ignore-scripts --no-audit --no-fund /tmp/npm-11.21.1.tgz && rm /tmp/npm-11.21.1.tgz && npm cache clean --force
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
