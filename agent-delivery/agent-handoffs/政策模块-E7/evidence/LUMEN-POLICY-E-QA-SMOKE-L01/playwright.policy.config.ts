import { defineConfig, devices } from '@playwright/test'

const baseURL = process.env.E2E_BASE_URL || 'http://192.168.88.50:30892'
if (/localhost|127\.0\.0\.1/i.test(baseURL)) {
  throw new Error('Policy gold forbids localhost; set E2E_BASE_URL to the published K8s frontend')
}

export default defineConfig({
  testDir: '.',
  testMatch: 'policy-gold.spec.ts',
  timeout: 300_000,
  expect: { timeout: 20_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [
    ['line'],
    ['json', { outputFile: 'results.json' }],
    ['html', { open: 'never', outputFolder: 'playwright-report' }],
  ],
  outputDir: 'test-results',
  use: {
    ...devices['Desktop Chrome'],
    baseURL,
    headless: true,
    viewport: { width: 1440, height: 900 },
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    launchOptions: process.env.CI
      ? { args: ['--no-sandbox', '--disable-dev-shm-usage'] }
      : undefined,
  },
})
