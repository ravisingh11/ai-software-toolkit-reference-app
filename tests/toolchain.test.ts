import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { spawnSync } from 'node:child_process';

const require = createRequire(import.meta.url);
const eslintRequire = createRequire(require.resolve('eslint'));
const ajvPath = eslintRequire.resolve('ajv');
const ajvRequire = createRequire(ajvPath);
const Ajv = eslintRequire('ajv');
const { ESLint } = require('eslint');

test('ESLint schema validator resolves external relative references and fragments', () => {
  const ajv = new Ajv();
  ajv.addSchema({
    $id: 'https://schemas.example.test/common/value.json',
    definitions: { label: { type: 'string', minLength: 2 } },
  });
  const validate = ajv.compile({
    $id: 'https://schemas.example.test/rules/options.json',
    type: 'object',
    properties: { label: { $ref: '../common/value.json#/definitions/label' } },
    required: ['label'],
    additionalProperties: false,
  });
  assert.equal(validate({ label: 'valid' }), true);
  for (const value of [{ label: 'x' }, { label: 3 }, {}, { label: 'valid', extra: true }]) {
    assert.equal(validate(value), false, JSON.stringify(value));
    assert.ok(validate.errors?.length);
  }
});

test('ESLint rejects invalid built-in rule options before linting', async () => {
  const eslint = new ESLint({
    overrideConfigFile: true,
    overrideConfig: { rules: { 'no-unused-vars': ['error', { vars: 'invalid-option' }] } },
  });
  await assert.rejects(eslint.lintText('const unused = 1;'), /no-unused-vars[\s\S]*invalid-option/);
});

test('Ajv URI parser terminates when normalizing and resolving Unicode line separators', () => {
  // Isolate the parser: a regression must time out, not hang the test runner.
  const script = `
    const assert = require('node:assert/strict');
    const uri = require(process.argv[1]);
    const options = { iri: true, unicodeSupport: true };
    for (const separator of ['\\u2028', '\\u2029']) {
      const input = 'https://schemas.example.test/' + separator + '/schema.json';
      const normalized = uri.normalize(input, options);
      assert.equal(typeof normalized, 'string');
      assert.equal(uri.normalize(normalized, options), normalized);
      assert.ok(normalized.endsWith('/' + encodeURIComponent(separator) + '/schema.json'));
      const resolved = uri.resolve('https://schemas.example.test/base/', '../' + separator + '/schema.json', options);
      assert.equal(typeof resolved, 'string');
      assert.ok(resolved.endsWith('/' + encodeURIComponent(separator) + '/schema.json'));
    }
    process.stdout.write('completed');
  `;
  const result = spawnSync(process.execPath, ['--max-old-space-size=64', '-e', script, ajvRequire.resolve('uri-js')], {
    encoding: 'utf8',
    timeout: 3000,
  });
  assert.ifError(result.error);
  assert.equal(result.signal, null);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout, 'completed');
});
