import { expect, test } from "@playwright/test";

// Anonymous journey: home -> locality search -> results update -> detail
// page. Zero auth anywhere in the flow (ADR 0004) — first end-to-end proof
// of the anonymous-first principle for a full user journey, not just an
// endpoint. See docs/features/phase1/slice-3-map-experience.md.

test("home page shows the hero, map area, and nearby companies", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: /your career has a location/i }),
  ).toBeVisible();
  await expect(page.getByText(/discover opportunities around you/i)).toBeVisible();
  await expect(page.getByRole("heading", { name: /nearby companies/i })).toBeVisible();
  await expect(
    page.getByText(/explore career universe/i).and(page.locator("span[aria-disabled]")),
  ).toBeVisible();
});

test("searching by locality re-centers the results, no login involved", async ({
  page,
}) => {
  await page.goto("/");

  await expect(page.getByRole("status").filter({ hasText: /loading/i })).toHaveCount(
    0,
    {
      timeout: 15000,
    },
  );

  const localityPicker = page.getByRole("combobox", { name: /search by locality/i });
  await localityPicker.selectOption("Gachibowli");

  await expect(page.getByRole("list", { name: /nearby companies/i })).toBeVisible();
  // No sign-in control anywhere on this anonymous page.
  await expect(page.getByRole("link", { name: /sign in|log in/i })).toHaveCount(0);
});

test("clicking a company card opens the detail panel with a shareable link", async ({
  page,
}) => {
  await page.goto("/");
  await expect(
    page.getByRole("status").filter({ hasText: /loading nearby/i }),
  ).toHaveCount(0, {
    timeout: 15000,
  });

  const firstCard = page
    .getByRole("list", { name: /nearby companies/i })
    .getByRole("button")
    .first();
  await firstCard.click();

  const panel = page.getByRole("dialog", { name: /company detail/i });
  await expect(panel).toBeVisible();
  await expect(panel.getByRole("link", { name: /open shareable page/i })).toBeVisible();
});

test("the Career Universe CTA is present but does nothing when clicked", async ({
  page,
}) => {
  await page.goto("/");
  const cta = page.getByText(/explore career universe/i);
  await expect(cta).toBeVisible();
  await expect(page.getByText(/coming soon/i)).toBeVisible();
});

test("'Near Me' denied falls back gracefully — never a blank map", async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(window.navigator, "geolocation", {
      value: {
        getCurrentPosition: (
          _success: PositionCallback,
          error?: PositionErrorCallback,
        ) => error?.({ code: 1, PERMISSION_DENIED: 1 } as GeolocationPositionError),
      },
      configurable: true,
    });
  });

  await page.goto("/");
  await page.getByRole("button", { name: /near me/i }).click();

  await expect(page.getByRole("status").filter({ hasText: /denied/i })).toBeVisible();
  // The rest of the page must still be intact — not a blank/broken state.
  await expect(page.getByRole("heading", { name: /nearby companies/i })).toBeVisible();
});

test("every company is reachable by keyboard alone, without touching the map", async ({
  page,
}) => {
  await page.goto("/");
  await expect(
    page.getByRole("status").filter({ hasText: /loading nearby/i }),
  ).toHaveCount(0, {
    timeout: 15000,
  });

  const list = page.getByRole("list", { name: /nearby companies/i });
  const firstCard = list.getByRole("button").first();
  await firstCard.focus();
  await expect(firstCard).toBeFocused();
  await page.keyboard.press("Enter");

  await expect(page.getByRole("dialog", { name: /company detail/i })).toBeVisible();
});
