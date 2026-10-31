import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

test('acceptance serves the retained compiled package and its source revision', async ({ request }) => {
  const packageRoot = process.env.APP_PACKAGE_DIR;
  test.skip(!packageRoot, 'Local development remains source-based; hosted acceptance selects a compiled package.');
  const manifest = JSON.parse(readFileSync(join(packageRoot!, 'package-manifest.json'), 'utf8'));
  const health = await request.get('/api/health');
  expect(health.status()).toBe(200);
  const metadata = await health.json();
  expect(metadata.status).toBe('ok');
  expect(metadata.revision).toBe(manifest.source.revision);
  for (const [url, name] of [['/', 'index.html'], ['/app.js', 'app.js'], ['/styles.css', 'styles.css']]) {
    const response = await request.get(url);
    expect(response.status()).toBe(200);
    expect(await response.body()).toEqual(readFileSync(join(packageRoot!, 'payload/public', name)));
  }
});
