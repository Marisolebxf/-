// _probe-p021-pop2.mjs — reload 后弹层存留诊断（评审开 → 点按钮 → reload → DOM 计数 + 截图 + 试点）
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

// 评审开
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
out.switch_before = checked;
if (checked !== 'true') { await sw.click({ timeout: 5000 }); await page.waitForTimeout(1200); }
await page.keyboard.press('Escape').catch(() => {});
await page.waitForTimeout(800);

const domInfo = async (tag) => {
  return await page.evaluate((t) => {
    const pops = Array.from(document.querySelectorAll('.arco-trigger-popup, .arco-popover'));
    const vis = pops.filter((e) => !!(e.offsetWidth || e.offsetHeight));
    return {
      tag: t,
      url: location.href.slice(-80),
      pop_total: pops.length,
      pop_visible: vis.length,
      pop_sample: (vis[0] ? (vis[0].innerText || '').replace(/\s+/g, ' ').slice(0, 100) : ''),
    };
  }, tag);
};

out.step1_review_on = await domInfo('review-on');
out.trace_count = await page.locator('button.trace-info-icon').count();

const btn = page.locator('button.trace-info-icon[aria-label*="分析配置"]').first();
await btn.click({ timeout: 5000 });
await page.waitForTimeout(1200);
out.step2_after_click = await domInfo('after-click');

await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);
out.step3_after_reload = await domInfo('after-reload');
await page.screenshot({ path: path.join(__dirname, 'probe-p021-pop2-after-reload.png') });

// reload 后试点 select（force:false 正常点 + 出错时记拦截者）
try {
  await page.locator('.industry-catalog-select').first().click({ timeout: 5000 });
  out.step4_select_click = 'ok';
} catch (e) {
  out.step4_select_click = 'blocked';
  out.step4_error_head = String(e).split('\n').slice(0, 6).join(' | ');
}

// 再等 3s 复核（SPA 慢挂载可能）
await page.waitForTimeout(3000);
out.step5_late = await domInfo('late-3s');

fs.writeFileSync(path.join(__dirname, '_probe-p021-pop2.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
