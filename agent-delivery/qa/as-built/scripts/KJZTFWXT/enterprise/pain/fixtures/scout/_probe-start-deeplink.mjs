#!/usr/bin/env node
/** 深链带对象 + 浮层选企（scroll）双路径核对 start_analysis 闸门 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const code = '0a2b82208071ce5a0e3bd562b80e263b';
const deepFilled =
  `enterprise/risk?workspace=pain-points&tab=pain-points&enterprise_codes[]=${code}&source=compare-basket`;
const deepEmpty = 'enterprise/risk?workspace=pain-points&tab=pain-points';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

async function login() {
  await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const loginBtn = page.getByRole('button', { name: /登录/ });
  if (await loginBtn.count()) await loginBtn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function closeBasket() {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if (await close.count() && (await close.first().isVisible().catch(() => false))) {
    try {
      await close.first().click({ timeout: 1500 });
      await page.waitForTimeout(300);
    } catch {
      await page.keyboard.press('Escape').catch(() => {});
    }
  }
}

await login();

// Path A: deep-link with enterprise_codes
await page.goto(base + deepFilled, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2000);
await closeBasket();
const startA = page.getByRole('button', { name: '开始分析' });
const pathA = {
  url: page.url(),
  object_echo: !!(await page.getByText(/来自对比篮/).count()),
  start_disabled: await startA.isDisabled().catch(() => null),
  start_enabled: (await startA.isDisabled().catch(() => null)) === false,
  body: (await page.locator('main.content-shell-layout').innerText().catch(() => '')).slice(0, 500),
};
await page.screenshot({ path: path.join(__dirname, 'env-gate-deeplink.png'), fullPage: false });

// Path B: overlay select with scroll
await page.goto(base + deepEmpty, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);
await closeBasket();
let pathB = { opened: false };
try {
  await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  await page.getByText('选择分析企业').first().waitFor({ state: 'visible', timeout: 5000 }).catch(() => {});
  const sels = page.locator('[aria-label^="选择 "]');
  pathB.select_count = await sels.count();
  pathB.opened = pathB.select_count > 0 || !!(await page.getByText('选择分析企业').count());
  if (pathB.select_count > 0) {
    await sels.nth(0).click();
    await page.waitForTimeout(400);
    const confirm = page.getByRole('button', { name: '确定' });
    await confirm.evaluate((el) => el.scrollIntoView({ block: 'center', inline: 'nearest' }));
    await page.waitForTimeout(300);
    await confirm.click({ timeout: 10000 });
    await page.waitForTimeout(2000);
    await closeBasket();
    const startB = page.getByRole('button', { name: '开始分析' });
    pathB = {
      ...pathB,
      confirm_ok: true,
      url: page.url(),
      object_echo: !!(await page.getByText(/来自对比篮/).count()),
      start_disabled: await startB.isDisabled().catch(() => null),
      start_enabled: (await startB.isDisabled().catch(() => null)) === false,
      body: (await page.locator('main.content-shell-layout').innerText().catch(() => '')).slice(0, 400),
    };
  }
} catch (e) {
  pathB.error = String(e.message || e).slice(0, 200);
}
await page.screenshot({ path: path.join(__dirname, 'env-gate-overlay.png'), fullPage: false });

const out = {
  surveyed_at: new Date().toISOString(),
  pathA_deeplink: pathA,
  pathB_overlay: pathB,
  start_analysis_gate_pass: !!(pathA.start_enabled || pathB.start_enabled),
};
fs.writeFileSync(path.join(__dirname, 'scout-start-deeplink.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
