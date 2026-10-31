// Explicit release-only live observations. Never imported or run by hosted tests.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { chromium } from '@playwright/test';

const args = process.argv.slice(2);
function argument(name) {
  const index = args.indexOf(name);
  if (index < 0 || !args[index + 1]) throw new Error(`${name} is required`);
  return args[index + 1];
}
const deployment = JSON.parse(readFileSync(resolve(argument('--deployment')), 'utf8'));
const output = resolve(argument('--output'));
const base = 'https://ai-software-toolkit-reference-app.navivision-account.workers.dev';
assert.equal(deployment.environment_url, base);
assert.equal(deployment.state, 'deployed-awaiting-live-verification');
assert.equal(deployment.traffic_percentage, 100);
const screenshots = join(output, 'screenshots');
mkdirSync(screenshots, { recursive: true });
const record = {
  version: 1, kind: 'live-browser-observations', status: 'incomplete',
  observed_at_utc: new Date().toISOString(), source_revision: deployment.source_revision,
  toolkit_revision: deployment.toolkit_revision, worker_version: deployment.worker_version,
  checks: [], screenshots: [], page_errors: [],
};
const persist = () => writeFileSync(join(output, 'browser-observations.json'), `${JSON.stringify(record, null, 2)}\n`);
const passed = name => { record.checks.push({ name, status: 'passed' }); persist(); };
async function shot(page, name) {
  const file = `${name}.png`;
  const location = join(screenshots, file);
  await page.screenshot({ path: location, fullPage: true });
  const bytes = readFileSync(location);
  record.screenshots.push({ file, sha256: createHash('sha256').update(bytes).digest('hex'), width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) });
  persist();
}
async function cards(page, count) {
  await page.waitForFunction(expected => document.querySelectorAll('.issue-card').length === expected, count, { timeout: 15000 });
}
async function responseStatus(response, expected) {
  assert.equal(response.status(), expected);
  return response;
}
const browser = await chromium.launch({ headless: true });
const contexts = [];
try {
  const editor = await browser.newContext({ baseURL: base, viewport: { width: 1440, height: 1000 } }); contexts.push(editor);
  const page = await editor.newPage();
  page.on('pageerror', error => record.page_errors.push(error.message));
  const healthResponse = await responseStatus(await editor.request.get('/api/health'), 200);
  const health = await healthResponse.json();
  assert.equal(health.status, 'ok'); assert.equal(health.revision, record.source_revision);
  assert.equal(health.toolkitRevision, record.toolkit_revision); assert.equal(health.version, record.worker_version);
  passed('exact-health-identity');
  await responseStatus(await editor.request.get('/api/issues'), 401);
  await responseStatus(await editor.request.post('/api/session', { headers: { Origin: 'https://untrusted.invalid' }, data: { role: 'editor' } }), 403);
  passed('anonymous-and-origin-boundaries');
  await page.goto(base, { waitUntil: 'networkidle' }); await page.locator('#start-session').click(); await cards(page, 3);
  assert.equal(await page.locator('#new-issue').isEnabled(), true);
  await page.locator('#new-issue').click(); await page.locator('#create-submit').click();
  assert.equal(await page.locator('#issue-title').evaluate(element => element.validity.valueMissing), true);
  const title = 'Verified package live observation';
  const description = '<b>Synthetic release observation</b> stays plain text';
  await page.locator('#issue-title').fill(title); await page.locator('#issue-description').fill(description);
  await page.locator('#issue-priority').selectOption('high');
  const createdResponse = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/api/issues');
  await page.locator('#create-submit').click();
  const created = await responseStatus(await createdResponse, 201); const issue = (await created.json()).issue;
  await page.locator('#create-dialog').waitFor({ state: 'hidden' }); await cards(page, 4);
  await responseStatus(await editor.request.post('/api/issues', { headers: { Origin: base }, data: { title: '', description: '', priority: 'low' } }), 400);
  await responseStatus(await editor.request.patch(`/api/issues/${issue.id}`, { headers: { Origin: base }, data: { status: 'done' } }), 409);
  passed('editor-create-and-input-boundaries');
  await page.locator('#search').fill(title); await cards(page, 1);
  await page.locator('#priority-filter').selectOption('low'); await cards(page, 0);
  await page.locator('#priority-filter').selectOption('high'); await cards(page, 1);
  await shot(page, 'desktop-editor-board'); passed('search-and-priority-filters');
  await page.locator('.issue-card').click();
  assert.equal(await page.locator('#detail-description').textContent(), description);
  assert.equal(await page.locator('#detail-description b').count(), 0);
  await page.locator('#issue-status').selectOption('in_progress'); await page.locator('#status-submit').click();
  await page.waitForFunction(() => document.querySelector('#detail-meta').textContent.includes('In progress'));
  const comment = 'Live package verification, synthetic data only.';
  await page.locator('#comment-body').fill(comment); await page.locator('#comment-submit').click();
  await page.waitForFunction(text => document.querySelector('#comment-list').textContent.includes(text), comment);
  await shot(page, 'desktop-editor-detail'); await page.keyboard.press('Escape');
  await page.locator('#detail-dialog').waitFor({ state: 'hidden' }); await page.reload({ waitUntil: 'networkidle' }); await cards(page, 4);
  await page.getByRole('button', { name: `Open issue: ${title}`, exact: true }).click();
  await page.waitForFunction(text => document.querySelector('#comment-list').textContent.includes(text), comment);
  assert.ok((await page.locator('#detail-meta').textContent()).includes('In progress'));
  passed('status-comment-and-reload-persistence');
  await page.keyboard.press('Escape'); await page.locator('#detail-dialog').waitFor({ state: 'hidden' });
  const repo = page.locator('.repository-link');
  assert.equal(await repo.getAttribute('href'), 'https://github.com/ravisingh11/ai-software-toolkit-reference-app');
  await repo.focus(); assert.equal(await repo.evaluate(element => document.activeElement === element), true);
  const desktopTarget = await repo.boundingBox(); assert.ok(desktopTarget.width >= 44 && desktopTarget.height >= 44);
  passed('repository-link-and-keyboard-focus');
  const viewer = await browser.newContext({ baseURL: base, viewport: { width: 390, height: 844 }, isMobile: true, deviceScaleFactor: 1 }); contexts.push(viewer);
  const mobile = await viewer.newPage(); mobile.on('pageerror', error => record.page_errors.push(error.message));
  await mobile.goto(base, { waitUntil: 'networkidle' }); await mobile.locator('#demo-role').selectOption('viewer');
  await mobile.locator('#start-session').click(); await cards(mobile, 3);
  assert.equal(await mobile.locator('#new-issue').isDisabled(), true); assert.equal(await mobile.locator('#role-note').isVisible(), true);
  const listed = await responseStatus(await viewer.request.get('/api/issues'), 200); const first = (await listed.json()).issues[0];
  await responseStatus(await viewer.request.post('/api/issues', { headers: { Origin: base }, data: { title: 'Denied', description: 'Synthetic', priority: 'low' } }), 403);
  await responseStatus(await viewer.request.patch(`/api/issues/${first.id}`, { headers: { Origin: base }, data: { status: 'in_progress' } }), 403);
  await responseStatus(await viewer.request.post(`/api/issues/${first.id}/comments`, { headers: { Origin: base }, data: { body: 'Denied synthetic request' } }), 403);
  await responseStatus(await viewer.request.get(`/api/issues/${issue.id}/comments`), 404);
  passed('viewer-api-permissions-and-board-isolation');
  await mobile.locator('.issue-card').first().click(); assert.equal(await mobile.locator('#issue-status').isDisabled(), true);
  assert.equal(await mobile.locator('#comment-body').isDisabled(), true);
  await mobile.locator('[data-close="detail-dialog"]').click(); await mobile.locator('#detail-dialog').waitFor({ state: 'hidden' });
  await mobile.locator('#priority-filter').selectOption('high'); await cards(mobile, 1); await mobile.locator('#priority-filter').selectOption('all'); await cards(mobile, 3);
  assert.equal(await mobile.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  await shot(mobile, 'mobile-viewer-board'); passed('mobile-viewer-and-layout');
  await mobile.setViewportSize({ width: 320, height: 844 });
  assert.equal(await mobile.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  assert.equal(await mobile.locator('.repository-link').isVisible(), true); await shot(mobile, 'compact-mobile-board'); passed('compact-mobile-layout');
  assert.deepEqual(record.page_errors, []);
  record.status = 'passed'; record.observed_at_utc = new Date().toISOString(); persist();
  console.log(JSON.stringify({ status: record.status, checks: record.checks.length, screenshots: record.screenshots.length }));
} catch (error) {
  record.status = 'failed'; record.observed_at_utc = new Date().toISOString(); record.error = error.message; persist(); throw error;
} finally {
  for (const context of contexts) await context.close();
  await browser.close();
}
