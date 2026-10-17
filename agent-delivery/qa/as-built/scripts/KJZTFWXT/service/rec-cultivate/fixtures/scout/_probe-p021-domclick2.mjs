#!/usr/bin/env node
/** 短探 6（P0-21 补充）：修正弹层容器类名重验 DOM click。
 *  探针 2 实证弹层容器 = .arco-trigger-popup:visible（内容行 = trace-info-popover__row）；探针 5 查错类名。
 *  本验：每枚 fresh goto → e.click() → 查 .arco-trigger-popup:visible/.arco-popover:visible 文本锚点（含按钮名=各自弹层）。
 *  另验 force click 对照。产出 scout-p021-domclick2.json。0 POST 只读。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const out = { probed_at: new Date().toISOString(), purpose: 'P0-21 DOM click re-verify with correct popup container class' };
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
const labels = ['培育服务机构推荐分析', '分析配置', '培育模型权重'];
const popText = async () => {
  const p = page.locator('.arco-trigger-popup:visible, .arco-popover:visible').first();
  if ((await p.count()) && (await p.isVisible().catch(() => false))) return ((await p.innerText().catch(() => '')) || '').replace(/\s+/g, ' ');
  return null;
};
out.per_button = [];
for (const lb of labels) {
  await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2200);
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
  const b = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  const entry = { wanted: lb };
  try {
    await b.evaluate((e) => e.click());
    await page.waitForTimeout(1100);
    const t = await popText();
    entry.domclick_popup_head = t ? t.slice(0, 110) : null;
    entry.anchor_match = t ? t.includes(lb) : false;
  } catch (e) { entry.err = String(e.message).split('\n')[0]; }
  // force click 对照（fresh）
  await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2200);
  const close2 = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close2.count()) && (await close2.first().isVisible().catch(() => false))) { try { await close2.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
  const b2 = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  try {
    await b2.click({ force: true, timeout: 4000 });
    await page.waitForTimeout(1100);
    const t2 = await popText();
    entry.force_popup_head = t2 ? t2.slice(0, 110) : null;
    entry.force_anchor_match = t2 ? t2.includes(lb) : false;
  } catch (e) { entry.force_err = String(e.message).split('\n')[0]; }
  out.per_button.push(entry);
}
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-domclick2.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify(out.per_button.map((e) => ({ w: e.wanted, dom: e.anchor_match, dom_head: (e.domclick_popup_head || e.err || '').slice(0, 60), force: e.force_anchor_match, force_head: (e.force_popup_head || e.force_err || '').slice(0, 60) })), null, 1));
