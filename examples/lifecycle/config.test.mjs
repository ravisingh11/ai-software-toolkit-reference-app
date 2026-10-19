import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import { localConfiguration } from './config.mjs';
const source = JSON.parse(readFileSync(new URL('../../wrangler.jsonc', import.meta.url), 'utf8'));
const revision = 'a'.repeat(40);
test('uses actual build, bindings, migration files and revision with no remote account', () => {
  const local = localConfiguration(source, revision);
  assert.equal(local.account_id, undefined);
  assert.equal(local.main, '/app/dist/index.js');
  assert.equal(local.no_bundle, true);
  assert.equal(local.vars.APP_REVISION, revision);
  assert.equal(local.vars.TOOLKIT_REVISION, source.vars.TOOLKIT_REVISION);
  assert.deepEqual(local.assets.run_worker_first, source.assets.run_worker_first);
  assert.equal(local.d1_databases[0].binding, source.d1_databases[0].binding);
  assert.equal(local.d1_databases[0].migrations_dir, '/app/migrations');
  assert.notEqual(local.d1_databases[0].database_id, source.d1_databases[0].database_id);
  assert.equal(source.vars.APP_REVISION, 'development');
});
test('rejects absent, symbolic or malformed revision instead of serving false identity', () => {
  for (const value of ['', 'main', 'development', 'a'.repeat(39), revision + '\n']) {
    assert.throws(() => localConfiguration(source, value));
  }
});
test('rejects changed application bindings instead of inventing a successful fixture', () => {
  for (const value of [{ ...source, d1_databases: [] }, { ...source, assets: {} }, { ...source, vars: {} }]) {
    assert.throws(() => localConfiguration(value, revision));
  }
});
