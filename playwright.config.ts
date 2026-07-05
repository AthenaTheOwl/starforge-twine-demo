import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/playwright',
  timeout: 30_000,
  fullyParallel: false,
  reporter: [['list']],
  outputDir: '.gstack/playwright-results',
  use: {
    baseURL: 'http://127.0.0.1:4173',
    trace: 'off',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});