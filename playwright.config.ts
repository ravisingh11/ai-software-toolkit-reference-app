import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/e2e', fullyParallel: false, workers: 1,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: { baseURL: 'http://localhost:8791', trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  webServer: {
    command: 'scripts/test-server.sh',
    url: 'http://localhost:8791/api/health', reuseExistingServer: false,
    timeout: 120000,
  },
});
