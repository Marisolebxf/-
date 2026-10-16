// _probe-p016.mjs — P0-16 收尾探针（探针公约：独立无头，一次性）
// 目的：① 确认评审开关存储机制（localStorage vs 服务端）与本 run 后的默认态；
//       ② 采集开启态 trace-info-icon aria-label 全集（observed）；③ 若因本条把共享账号默认态改为关，恢复开启。
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://111.198.38.90:50892';
const out = { probed_at: new Date().toISOString(), entry: 'svc-chain-shortboard' };

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await ctx.newPage();

// 登录（跳 /login 才登）
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

await page.goto(BASE + '/service/chain-analysis?workspace=chain&tab=chain', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);

const close = page.locator('button[aria-label="关闭对比篮"]');
if (await close.count() && await close.first().isVisible().catch(() => false)) { await close.first().click({ timeout: 1500 }).catch(() => {}); await page.waitForTimeout(300); }

// ① 新上下文首访默认态（判断持久化）
out.trace_count_fresh_context = await page.locator('button.trace-info-icon').count();

// ② localStorage 键快照（评审/人设相关）
out.localStorage_review_keys = await page.evaluate(() => {
  const hits = {};
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i);
    if (/review|persona|评审/i.test(k)) hits[k] = localStorage.getItem(k);
  }
  return hits;
});

// ③ 若默认关：开菜单→开评审→采集全集；若默认开：直接采集全集，再读当前 checked 态
const opener = page.locator('.persona-switch').first();
if (!(await opener.isVisible().catch(() => false))) { out.note = 'persona-switch 不可见（兜底 class*=persona）'; }
await opener.click({ timeout: 5000 }).catch(async (e) => {
  await page.locator('[class*="persona" i]').first().click({ timeout: 5000 }).catch(() => {});
});
await page.waitForTimeout(800);
const sw = page.locator('button[role=switch][aria-label="内部评审模式"], [aria-label="内部评审模式"]').first();
out.switch_present = await sw.count();
let checked = await sw.getAttribute('aria-checked').catch(() => null);
if (checked === null) {
  const cls = await sw.getAttribute('class').catch(() => '');
  checked = /arco-switch-checked/.test(cls || '') ? 'true' : 'false';
}
out.switch_checked_in_menu = checked;
if (checked !== 'true') {
  await sw.click({ timeout: 5000 });
  await page.waitForTimeout(1200);
  out.restored_to_on = true; // 恢复勘察默认开启态（若为持久化存储，避免污染兄弟入口）
} else {
  out.restored_to_on = false;
}
await page.keyboard.press('Escape').catch(() => {});
await page.waitForTimeout(800);

out.trace_labels_on = await page.locator('button.trace-info-icon').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label') || ''));

fs.writeFileSync(path.join(__dirname, '_probe-p016.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
