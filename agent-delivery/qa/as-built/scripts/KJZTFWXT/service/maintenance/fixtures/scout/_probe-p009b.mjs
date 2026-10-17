#!/usr/bin/env node
/**
 * P0-09 补探：关评审后路由是否漂移、漂移发生在哪一步。
 */
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
  let opener = page.locator('button.persona-switch, .persona-switch').first();
  if (!(await opener.isVisible().catch(() => false))) opener = page.locator('[class*="persona" i]').first();
  await opener.click({ timeout: 5000 });
  await page.waitForTimeout(600);
  const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"], button[role=switch][aria-label="内部评审模式"]').first();
  await sw.waitFor({ state: 'visible', timeout: 8000 });
  let checked = await sw.getAttribute('aria-checked').catch(() => null);
  if (checked === null) {
    const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]');
    checked = /arco-switch-checked/.test((await holder.first().getAttribute('class').catch(() => '')) || '') ? 'true' : 'false';
  }
  const want = wantTrue ? 'true' : 'false';
  if (checked !== want) {
    await sw.click({ timeout: 5000 });
    await page.waitForTimeout(1200);
  }
  checked = await sw.getAttribute('aria-checked').catch(() => null);
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(400);
  return checked;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const log = [];
const push = (id) => log.push({ id, url: page.url(), title: '' });

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(1500);
  push('after_goto');
  log[log.length - 1].title = await page.title();

  const close = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }

  const heading0 = ((await page.locator('section.diagnosis-page-heading, .diagnosis-page-heading').first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();

  // 关评审（默认多为开）
  const afterOff = await setReview(page, false);
  push('after_toggle_off');
  log[log.length - 1].review = afterOff;
  log[log.length - 1].title = await page.title();
  log[log.length - 1].heading = ((await page.locator('section.diagnosis-page-heading, .diagnosis-page-heading').first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();

  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  push('after_reload');
  log[log.length - 1].title = await page.title();
  log[log.length - 1].heading = ((await page.locator('section.diagnosis-page-heading, .diagnosis-page-heading').first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  log[log.length - 1].h1 = ((await page.getByRole('heading', { name: '维护管理', level: 1 }).innerText().catch(() => '')) || '').trim();

  // 若漂移，深链回页再验关态
  if (!/\/service\/maintenance/.test(page.url())) {
    await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1500);
    push('deeplink_back');
    log[log.length - 1].title = await page.title();
    // 再确认评审仍关
    const still = await setReview(page, false);
    push('after_reconfirm_off');
    log[log.length - 1].review = still;
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    push('after_second_reload');
    log[log.length - 1].title = await page.title();
  }

  // 零泄漏扫 main
  const mainText = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  const leaks = ['指标说明', '指标未登记', '需求追溯', 'metric_id', 'GAP-'].filter((k) => mainText.includes(k));
  if (/Q0\d{2}/.test(mainText)) leaks.push('Q0xx');
  // Q- 单独：附录 A 含 Q-，但占位文案无 Q-；扫「Q-」前缀治理码
  if (/Q-[A-Z]/.test(mainText)) leaks.push('Q-prefix');

  const heading1 = ((await page.locator('section.diagnosis-page-heading, .diagnosis-page-heading').first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  const out = {
    probed_at: new Date().toISOString(),
    heading0,
    heading1,
    copyUnchanged: heading0 === heading1,
    leaks,
    onMaintenance: /\/service\/maintenance/.test(page.url()),
    log,
  };
  fs.writeFileSync(path.join(__dirname, 'probe-p009b.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
} catch (e) {
  const err = { error: String(e && e.stack ? e.stack : e), log };
  fs.writeFileSync(path.join(__dirname, 'probe-p009b.json'), JSON.stringify(err, null, 2));
  console.error(err.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
