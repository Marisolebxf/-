#!/usr/bin/env node
/** P0-09 补探 D：关评踢门户后，再开评审能否深链回 maintenance 且文案恢复。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const route = '/service/maintenance';

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function setReview(page, wantTrue) {
  const persona = page.locator('button.persona-switch').first();
  await persona.click({ timeout: 5000 });
  await page.waitForTimeout(600);
  const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
  await sw.waitFor({ state: 'visible', timeout: 8000 });
  let checked = await sw.getAttribute('aria-checked');
  const want = wantTrue ? 'true' : 'false';
  if (checked !== want) {
    const box = await sw.boundingBox();
    if (box) await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
    else await sw.click({ timeout: 5000 });
    await page.waitForTimeout(1200);
    checked = await sw.getAttribute('aria-checked');
  }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(400);
  return checked;
}

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 })).newPage();
const out = { probed_at: new Date().toISOString(), steps: [] };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(1200);
  const heading0 = ((await page.locator('section.diagnosis-page-heading, .diagnosis-page-heading').first().innerText()) || '').replace(/\s+/g, ' ').trim();
  const title0 = await page.title();
  out.steps.push({ id: 'baseline', url: page.url(), heading0, title0 });

  await setReview(page, false);
  out.steps.push({ id: 'after_off', url: page.url() });

  await setReview(page, true);
  out.steps.push({ id: 'after_on_again', url: page.url() });

  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(1500);
  const heading1 = ((await page.locator('section.diagnosis-page-heading, .diagnosis-page-heading').first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  const title1 = await page.title();
  out.steps.push({
    id: 'deeplink_after_reon',
    url: page.url(),
    heading1,
    title1,
    onMaintenance: /\/service\/maintenance/.test(page.url()),
    copyRestored: heading1 === heading0,
    titleRestored: title1 === title0,
  });

  fs.writeFileSync(path.join(__dirname, 'probe-p009d.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
} catch (e) {
  out.error = String(e && e.stack ? e.stack : e);
  fs.writeFileSync(path.join(__dirname, 'probe-p009d.json'), JSON.stringify(out, null, 2));
  console.error(out.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
