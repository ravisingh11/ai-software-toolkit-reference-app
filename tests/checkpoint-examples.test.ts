import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const renderer = join(root, '.proof/render_scorecard_badge.py');
const repository = 'ravisingh11/ai-software-toolkit-reference-app';
const fixture = JSON.parse(readFileSync(join(root, 'tests/fixtures/checkpoint-examples.json'), 'utf8'));

test('branding metadata keeps the published base and binds each canonical source copy', () => {
  const lock = JSON.parse(readFileSync(join(root, 'toolkit.lock.json'), 'utf8'));
  const branding = JSON.parse(readFileSync(join(root, 'scripts/branding-source.json'), 'utf8'));
  assert.equal(lock.release, 'v2.3.4');
  assert.equal(lock.pageRenderer.revision, lock.revision);
  assert.match(lock.pageRenderer.revision, /^[0-9a-f]{40}$/);
  assert.equal(lock.pageRenderer.repository, 'https://github.com/ravisingh11/ai-software-toolkit');
  assert.equal(branding.version, 1);
  assert.equal(branding.kind, 'project-branding-source');
  assert.equal(branding.repository, 'https://github.com/ravisingh11/ai-engineering-guardrails');
  assert.equal(branding.repository_id, 1348591078);
  assert.equal(branding.revision, '242308aa6e652d3a9e9dec6c552c6fd8d98673e1');
  assert.deepEqual(branding.published_base, { lock: 'toolkit.lock.json', release: lock.release, revision: lock.revision });
  const expectedCopies = {
    '.proof/activation.py': 'tooling/activation.py',
    '.proof/render_scorecard_badge.py': 'tooling/render_scorecard_badge.py',
    'scripts/checkpoint_report.py': 'tooling/checkpoint_report.py',
    '.agents/skills/toolkit-setup/SKILL.md': 'skills/toolkit-setup/SKILL.md',
    '.agents/skills/toolkit-setup/agents/openai.yaml': 'skills/toolkit-setup/agents/openai.yaml',
  };
  assert.deepEqual(branding.files.map(file => file.installed_path).sort(), Object.keys(expectedCopies).sort());
  for (const file of branding.files) {
    assert.equal(file.source_path, expectedCopies[file.installed_path]);
    assert.match(file.sha256, /^[0-9a-f]{64}$/);
    assert.match(file.previous_sha256, /^[0-9a-f]{64}$/);
    assert.equal(createHash('sha256').update(readFileSync(join(root, file.installed_path))).digest('hex'), file.sha256);
  }
  const currentRenderer = branding.files.find(file => file.installed_path === '.proof/render_scorecard_badge.py');
  assert.equal(currentRenderer.source_path, lock.pageRenderer.sourcePath);
  assert.equal(currentRenderer.previous_sha256, lock.pageRenderer.sha256);
});

test('app page separates historical PR checks from its own main checks and live score', () => {
  const temporary = mkdtempSync(join(tmpdir(), 'checkpoint-page-'));
  try {
    const source = join(temporary, 'source');
    const output = join(temporary, 'site');
    mkdirSync(source);
    const revision = 'b'.repeat(40);
    const card = {
      version: 2, status: 'GREEN', decision: 'allow', policy: 'synthetic-ui-fixture', operation: 'change',
      subject: { type: 'git-commit', revision },
      enforced: { passed: 0, total: 0 }, advisory: { passed: 1, total: 1 },
      controls: [{ id: 'unit-tests', effective_mode: 'advisory', evidence_status: 'passed',
        authoritative_provider: { id: 'repository-unit-tests' },
        authoritative_result: { status: 'passed', evidence: ['Synthetic UI fixture'] } }],
    };
    const original = JSON.stringify(card);
    writeFileSync(join(source, 'scorecard-ui.json'), original);
    writeFileSync(join(source, 'scorecard-ui.md'), 'Synthetic UI input, not execution evidence.\n');
    writeFileSync(join(temporary, '.ignored'), 'preserve');
    execFileSync('python3', [renderer, '--source-dir', source, '--output-dir', output,
      '--repository', repository, '--run-id', '999', '--run-attempt', '1',
      '--run-url', `https://github.com/${repository}/actions/runs/999/attempts/1`,
      '--source-run-created-at', '2026-10-29T00:00:00Z', '--expected-revision', revision],
    { encoding: 'utf8', timeout: 20000 });
    const page = readFileSync(join(output, 'index.html'), 'utf8');
    const gallery = page.split('<section class="checkpoint-gallery"')[1].split('<section class="scorecard-section"')[0];
    const pr = gallery.split('id="checkpoint-pr-example"')[1].split('</article>')[0];
    const main = gallery.split('id="checkpoint-main-example"')[1].split('</article>')[0];
    assert.ok(gallery.includes(`Historical examples from <strong>${repository}</strong>`));
    assert.ok(gallery.includes('These runs come from different changes'));
    assert.ok(!gallery.includes('/ai-software-toolkit/actions/runs/'));
    assert.ok(pr.includes(fixture.pr.revision.slice(0, 12)));
    assert.ok(main.includes(fixture.main.revision.slice(0, 12)));
    assert.notEqual(fixture.pr.revision, fixture.main.revision);
    const outcomes = { passed: 'Passed', failed: 'Failed', no_result: 'Unverified' };
    for (const [identifier, recorded] of Object.entries(fixture.pr.checks)) {
      const row = pr.split(`data-example-check="${identifier}"`)[1].split('</li>')[0];
      assert.ok(row.includes(`${outcomes[recorded.status]} · advisory`), identifier);
    }
    for (const identifier of ['application-build', 'unit-tests', 'browser-acceptance', 'migration-validation']) {
      const row = main.split(`data-example-check="${identifier}"`)[1].split('</li>')[0];
      assert.ok(row.includes('>Passed</span>'), identifier);
      assert.ok(!pr.includes(`data-example-check="${identifier}"`));
    }
    assert.ok(main.includes('not a Proof policy score or live deployment evidence'));
    const published = JSON.parse(readFileSync(join(output, 'scorecard.json'), 'utf8'));
    assert.equal(published.passed, 1);
    assert.equal(published.total, 1);
    assert.equal(published.decision, 'allow');
    assert.equal(readFileSync(join(source, 'scorecard-ui.json'), 'utf8'), original);
    assert.equal(readFileSync(join(temporary, '.ignored'), 'utf8'), 'preserve');
  } finally {
    rmSync(temporary, { recursive: true, force: true });
  }
});
