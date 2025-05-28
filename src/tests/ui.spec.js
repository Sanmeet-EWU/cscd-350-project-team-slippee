const { test, expect } = require('@playwright/test');

test('Project Slippe 64 UI loads correctly', async ({ page }) => {
  await page.goto('http://localhost:8080');

  await expect(page.locator('text=Project Slippe 64')).toBeVisible();
  await expect(page.locator('input[placeholder="Insert Rom"]')).toBeVisible();
  await expect(page.locator('select')).toHaveCount(1);
  await expect(page.locator('option')).toHaveCount(3);
});
