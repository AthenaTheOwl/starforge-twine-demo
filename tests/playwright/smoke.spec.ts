import { expect, test } from '@playwright/test';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';

const buildRoot = path.resolve(__dirname, '..', '..', 'build');
let server: http.Server;

function resolveRequestPath(urlPath: string): string | null {
  const decoded = decodeURIComponent(urlPath.split('?')[0]);
  const normalized = decoded === '/' ? '/index.html' : decoded;
  const candidate = path.resolve(buildRoot, `.${normalized}`);
  return candidate.startsWith(buildRoot) ? candidate : null;
}

test.beforeAll(async () => {
  server = http.createServer((request, response) => {
    const filePath = resolveRequestPath(request.url || '/');
    if (!filePath) {
      response.writeHead(403);
      response.end('forbidden');
      return;
    }

    fs.readFile(filePath, (error, body) => {
      if (error) {
        response.writeHead(404);
        response.end('not found');
        return;
      }
      response.writeHead(200);
      response.end(body);
    });
  });

  await new Promise<void>((resolve) => {
    server.listen(4173, '127.0.0.1', resolve);
  });
});

test.afterAll(async () => {
  await new Promise<void>((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
});

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