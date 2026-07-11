import { defineConfig, devices } from "@playwright/test";

const PORT = 3100;

/**
 * E2E scaffold. Full runs require browsers: `pnpm exec playwright install`.
 * The webServer builds and starts the app, then tests run against it.
 */
export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  reporter: "list",
  use: {
    baseURL: `http://localhost:${PORT}`,
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: `pnpm build && pnpm start -p ${PORT}`,
    url: `http://localhost:${PORT}`,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
