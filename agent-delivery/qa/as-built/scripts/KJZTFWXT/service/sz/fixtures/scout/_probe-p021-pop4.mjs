// _probe-p021-pop4.mjs — 终定性：a) 全量 localStorage 键 dump；b) 弹层 DOM marker 跨 reload 是否同节点；
//   c) reload 后 body-click 是否收弹层并解锁 select；d) 弹层内文本完整抓取（锚点 REQ-SVC-ECO-* 全文）
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://111.198.38.90:50892';
const ROUTE = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const out = {};

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await ctx.newPage();

await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(800);
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1500);
  if (page.url().includes('/login')) {
    await page.locator('button[type=submit], button:has-text("登录")').first().click().catch(() => {});
    await page.waitForTimeout(1500);
  }
}
await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);

// a) 全量 storage
out.all_storage = await page.evaluate(() => {
  const grab = (s) => { const o = {}; for (let i = 0; i < s.length; i++) { const k = s.key(i); o[k] = (s.getItem(k) || '').slice(0, 300); } return o; };
  return { local: grab(localStorage), session: grab(sessionStorage) };
});

// 评审开（若未开）
let opener = page.locator('.persona-switch').first();
if (!(await opener.isVisible().catch(() => false))) opener = page.locator('[class*="persona" i]').first();
await opener.click({ timeout: 5000 });
await page.waitForTimeout(800);
const sw = page.locator('button[role=switch][aria-label="内部评审模式"], [aria-label="内部评审模式"]').first();
let checked = await sw.getAttribute('aria-checked').catch(() => null);
if (checked === null) {
  const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]');
  checked = /arco-switch-checked/.test((await holder.first().getAttribute('class').catch(() => '')) || '') ? 'true' : 'false';
}
if (checked !== 'true') { await sw.click({ timeout: 5000 }); await page.waitForTimeout(1200); }
await page.keyboard.press('Escape').catch(() => {});
await page.waitForTimeout(800);

// 追溯按钮 aria-label 全集 + 全文抓取（三枚）
out.trace_labels = await page.locator('button.trace-info-icon').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label') || ''));

// b) 点「分析配置」→ marker → reload → 同节点？
const btnSel = 'button.trace-info-icon[aria-label*="分析配置"]';
await page.locator(btnSel).first().click({ timeout: 5000 });
await page.waitForTimeout(1200);
await page.evaluate(() => {
  const vis = Array.from(document.querySelectorAll('.arco-trigger-popup, .arco-popover')).filter((e) => !!(e.offsetWidth || e.offsetHeight));
  if (vis[0]) vis[0].setAttribute('data-probe-marker', 'pop4-m1');
});
out.pop_text_config = await page.evaluate(() => {
  const vis = Array.from(document.querySelectorAll('.arco-trigger-popup, .arco-popover')).filter((e) => !!(e.offsetWidth || e.offsetHeight));
  return vis[0] ? (vis[0].innerText || '').replace(/\s+/g, ' ') : '';
});
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);
out.marker_after_reload = await page.evaluate(() => document.querySelectorAll('[data-probe-marker="pop4-m1"]').length);
out.pop_after_reload = await page.evaluate(() => {
  const vis = Array.from(document.querySelectorAll('.arco-trigger-popup, .arco-popover')).filter((e) => !!(e.offsetWidth || e.offsetHeight));
  return { count: vis.length, sample: vis[0] ? (vis[0].innerText || '').replace(/\s+/g, ' ').slice(0, 120) : '', marker: vis[0] ? vis[0].getAttribute('data-probe-marker') : null };
});

// c) body-click 收弹层 + select 解锁
await page.mouse.click(960, 540).catch(() => {});
await page.waitForTimeout(800);
out.pop_after_bodyclick = await page.evaluate(() => {
  const vis = Array.from(document.querySelectorAll('.arco-trigger-popup, .arco-popover')).filter((e) => !!(e.offsetWidth || e.offsetHeight));
  return vis.length;
});
try {
  await page.locator('.industry-catalog-select').first().click({ timeout: 5000 });
  out.select_after_bodyclick = 'ok';
} catch (e) {
  out.select_after_bodyclick = 'blocked';
}
// 收下拉
await page.keyboard.press('Escape').catch(() => {});

// d) 另两枚按钮全文（重开评审弹层逐一点）
for (const key of ['深圳服务链现状分析', '横向对比分析']) {
  try {
    await page.locator(`button.trace-info-icon[aria-label*="${key}"]`).first().click({ timeout: 5000 });
    await page.waitForTimeout(1200);
    const t = await page.evaluate(() => {
      const vis = Array.from(document.querySelectorAll('.arco-trigger-popup, .arco-popover')).filter((e) => !!(e.offsetWidth || e.offsetHeight));
      return vis[0] ? (vis[0].innerText || '').replace(/\s+/g, ' ') : '';
    });
    out['pop_text_' + (key === '深圳服务链现状分析' ? 'framework' : 'compare')] = t;
    await page.mouse.click(960, 540).catch(() => {});
    await page.waitForTimeout(600);
  } catch (e) {
    out['pop_text_' + (key === '深圳服务链现状分析' ? 'framework' : 'compare')] = 'ERR ' + String(e).slice(0, 100);
  }
}

fs.writeFileSync(path.join(__dirname, '_probe-p021-pop4.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
