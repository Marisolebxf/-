#!/usr/bin/env node
/** 短探 9（P0-21 修稿诊断）：e.click() 后弹层真实形态——层级/可见性/计数口径。
 *  正式跑 r1 红：`.arco-trigger-popup:visible, .arco-popover:visible` first() count/visible 判 0。
 *  探针 2 native click 后同 selector 读到文本。差异疑点：e.click()（DOM 事件）不触发 Arco Trigger 的
 *  popup open 动作？——探针 6 dom_head 读到的是残留弹层（storage 恢复），并非 e.click() 新开。
 *  本验：fresh 会话（不清 storage、无残留）→ 仅 e.click() 首枚 → 弹层 DOM 全量快照（count/visible/类名/文本头）。
 *  产出 scout-p021-eclick-diag.json。0 POST 只读。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const out = { probed_at: new Date().toISOString(), purpose: 'P0-21 does e.click() really open the trace popup? full DOM snapshot after click' };
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2400);
const close = page.locator('button[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
// 初始弹层态
out.before = await page.evaluate(() => {
  const els = document.querySelectorAll('.arco-trigger-popup, .arco-popover, .trace-info-popover');
  return { total: els.length, detail: [...els].slice(0, 6).map((e) => ({ cls: String(e.className).slice(0, 70), visible: !!(e.offsetWidth || e.offsetHeight), display: getComputedStyle(e).display, text_head: ((e.innerText || '') + '').replace(/\s+/g, ' ').slice(0, 60) })) };
});
// e.click() 首枚
const b = page.locator('button.trace-info-icon[aria-label^="培育服务机构推荐分析"]').first();
await b.evaluate((e) => e.click());
await page.waitForTimeout(1200);
out.after_eclick = await page.evaluate(() => {
  const els = document.querySelectorAll('.arco-trigger-popup, .arco-popover, .trace-info-popover');
  return { total: els.length, detail: [...els].slice(0, 6).map((e) => ({ cls: String(e.className).slice(0, 70), visible: !!(e.offsetWidth || e.offsetHeight), display: getComputedStyle(e).display, text_head: ((e.innerText || '') + '').replace(/\s+/g, ' ').slice(0, 60) })) };
});
await page.screenshot({ path: path.join(__dirname, 'p021-eclick-diag.png') }).catch(() => {});
// 对照：native click（force）后
await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2400);
const b2 = page.locator('button.trace-info-icon[aria-label^="培育服务机构推荐分析"]').first();
await b2.click({ force: true, timeout: 5000 }).catch((e) => { out.force_err = String(e.message).split('\n')[0]; });
await page.waitForTimeout(1200);
out.after_force = await page.evaluate(() => {
  const els = document.querySelectorAll('.arco-trigger-popup, .arco-popover, .trace-info-popover');
  return { total: els.length, detail: [...els].slice(0, 6).map((e) => ({ cls: String(e.className).slice(0, 70), visible: !!(e.offsetWidth || e.offsetHeight), display: getComputedStyle(e).display, text_head: ((e.innerText || '') + '').replace(/\s+/g, ' ').slice(0, 60) })) };
});
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-eclick-diag.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify(out, null, 1));
