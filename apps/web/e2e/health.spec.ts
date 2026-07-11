import { expect, test } from "@playwright/test";

test("health page loads and shows web status", async ({ page }) => {
  await page.goto("/health");
  await expect(page.getByRole("heading", { name: /web status/i })).toBeVisible();
});
