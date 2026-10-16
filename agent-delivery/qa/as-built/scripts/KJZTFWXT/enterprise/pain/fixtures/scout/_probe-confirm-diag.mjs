#!/usr/bin/env node
/** 诊断：选择分析企业浮层「确定」为何点不到 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const target = 'enterprise/risk?workspace=pain-points&tab=pain-points';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

await page.goto(base + target, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);
const close = page.locator('[aria-label="关闭对比篮"]');
if (await close.count() && (await close.first().isVisible().catch(() => false))) {
  try {
    await close.first().click({ timeout: 1500 });
    await page.waitForTimeout(300);
  } catch {}
}

await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
await page.waitForTimeout(1000);

const diag = await page.evaluate(() => {
  const btns = [...document.querySelectorAll('button')].filter((b) => (b.innerText || '').trim() === '确定');
  return btns.map((b) => {
    const r = b.getBoundingClientRect();
    const mid = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return {
      disabled: b.disabled,
      class: (b.className || '').toString().slice(0, 120),
      box: { x: r.x, y: r.y, w: r.width, h: r.height },
      topTag: mid ? mid.tagName + '.' + (mid.className || '').toString().slice(0, 80) : null,
      topText: mid ? (mid.innerText || '').slice(0, 40) : null,
      inDialog: !!b.closest('.arco-modal, [role=dialog], .arco-drawer'),
    };
  });
});

const sels = page.locator('[aria-label^="选择 "]');
await sels.nth(0).click();
await page.waitForTimeout(500);

const diag2 = await page.evaluate(() => {
  const btns = [...document.querySelectorAll('button')].filter((b) => (b.innerText || '').trim() === '确定');
  return btns.map((b) => {
    const r = b.getBoundingClientRect();
    const mid = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return {
      disabled: b.disabled,
      class: (b.className || '').toString().slice(0, 120),
      box: { x: r.x, y: r.y, w: r.width, h: r.height },
      topTag: mid ? mid.tagName + '.' + (mid.className || '').toString().slice(0, 80) : null,
      covered: mid !== b && !b.contains(mid),
    };
  });
});

const dialogConfirm = page.locator('.arco-modal, [role=dialog], .arco-drawer').getByRole('button', { name: '确定' });
let clickWays = {};
for (const [name, loc] of [
  ['dialog_scope', dialogConfirm.first()],
  ['force', page.getByRole('button', { name: '确定' }).first()],
]) {
  try {
    if (name === 'force') await loc.click({ force: true, timeout: 3000 });
    else await loc.click({ timeout: 5000 });
    await page.waitForTimeout(1500);
    clickWays[name] = {
      ok: true,
      url: page.url(),
      filled: !!(await page.getByText(/来自对比篮/).count()),
    };
    break;
  } catch (e) {
    clickWays[name] = { ok: false, err: String(e.message || e).slice(0, 120) };
  }
}

const start = page.getByRole('button', { name: '开始分析' });
const out = {
  surveyed_at: new Date().toISOString(),
  diag_before_pick: diag,
  diag_after_pick: diag2,
  clickWays,
  url: page.url(),
  start_disabled: await start.isDisabled().catch(() => null),
  body: (await page.locator('main.content-shell-layout').innerText().catch(() => '')).slice(0, 400),
};
await page.screenshot({ path: path.join(__dirname, 'env-gate-confirm-diag.png'), fullPage: false });
fs.writeFileSync(path.join(__dirname, 'scout-confirm-diag.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
