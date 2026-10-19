// Starts the actual built Worker against an isolated, ephemeral local D1 database.
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { spawn, spawnSync } from 'node:child_process';
import { localConfiguration } from './config.mjs';

const revision = readFileSync('/app/revision', 'utf8');
if (!/^[a-f0-9]{40}$/.test(revision)) throw new Error('Missing immutable source revision');
const source = JSON.parse(readFileSync('/app/wrangler.jsonc', 'utf8'));
const state = '/tmp/proof-fieldnotes';
mkdirSync(state, { recursive: true });
writeFileSync(`${state}/wrangler.json`, JSON.stringify(localConfiguration(source, revision)));
const cli = '/app/node_modules/wrangler/bin/wrangler.js';
const common = { cwd: state, env: process.env, stdio: 'inherit' };
const migration = spawnSync(process.execPath, [cli, 'd1', 'migrations', 'apply', 'DB', '--local', '--config', `${state}/wrangler.json`, '--persist-to', `${state}/db`], common);
if (migration.status !== 0) process.exit(migration.status || 1);
const server = spawn(process.execPath, [cli, 'dev', '--local', '--config', `${state}/wrangler.json`, '--ip', '0.0.0.0', '--port', '8080', '--inspector-port', '0', '--persist-to', `${state}/db`], common);
for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => server.kill(signal));
server.on('error', error => { console.error(error); process.exit(1); });
server.on('exit', code => process.exit(code ?? 1));
