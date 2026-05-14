import { expect, test } from '@playwright/test';

test('start page reaches the full Act 1 route map', async ({ page }) => {
  await page.goto('/index.html');
  await expect(page).toHaveTitle(/Starforge Canticles/);
  const passage = page.locator('#passages');
  await expect(passage.getByText('Full Act 1 is routed here')).toBeVisible();

  await passage.getByText('Open Act 1 route map').click();
  await expect(passage.getByText('Chapter 20: The Receipt')).toBeVisible();
  await expect(passage.getByText('Optional 20d: Aleena Pulls Elia From Wreckage')).toBeVisible();
});

test('main spine can move from prologue to chapter one', async ({ page }) => {
  await page.goto('/index.html');
  const passage = page.locator('#passages');
  await passage.getByText('Begin Act 1').click();
  await expect(passage.getByText('Chapter 00: Prologue Floors Not Thrones')).toBeVisible();
  await passage.getByText('Continue to Chapter 01: Cinder Hours').click();
  await expect(passage.getByText('Chapter 01: Cinder Hours')).toBeVisible();
});

test('route map can open a mid-act optional scene', async ({ page }) => {
  await page.goto('/index.html');
  const passage = page.locator('#passages');
  await passage.getByText('Open Act 1 route map').click();
  await passage.getByText('Optional 11b: Senna Small Good Thing').click();
  await expect(page.getByRole('heading', { name: 'Optional 11b: Senna Small Good Thing' })).toBeVisible();
  await expect(passage.getByText('Source: 11b_senna_small_good_thing.md')).toBeVisible();
});

test('route map can open the final main chapter', async ({ page }) => {
  await page.goto('/index.html');
  const passage = page.locator('#passages');
  await passage.getByText('Open Act 1 route map').click();
  await passage.getByText('Chapter 20: The Receipt').click();
  await expect(page.getByRole('heading', { name: 'Chapter 20: The Receipt' })).toBeVisible();
  await passage.getByText('Finish Act 1').first().click();
  await expect(passage.getByText('Ending: Act 1 route complete.')).toBeVisible();
});
