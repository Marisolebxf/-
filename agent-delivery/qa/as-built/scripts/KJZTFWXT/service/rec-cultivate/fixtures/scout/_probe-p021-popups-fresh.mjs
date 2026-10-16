#!/usr/bin/env node
/** 短探 3（P0-21 补充）：弹层常驻遮挡下「逐一点击」可行路径 = 每枚点击前 fresh goto。
 *  验证：fresh 页面直接点第 2/3 枚（分析配置/培育模型权重）各能开各自弹层；记录弹层锚点文本。
 *  产出 scout-p021-popups-fresh.json。0 POST 只读。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const out = { probed_at: new Date().toISOString(), purpose: 'P0-21 per-button fresh-goto click path' };
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
out.per_button_fresh = [];
for (const lb of labels) {
  await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2200);
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
  const entry = { wanted: lb };
  const b = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  entry.visible_before = await b.isVisible().catch(() => false);
  try {
    await b.click({ timeout: 5000 });
    await page.waitForTimeout(900);
    const p = page.locator('.arco-trigger-popup:visible, .arco-popover:visible').first();
    entry.popup = (await p.count()) && (await p.isVisible().catch(() => false)) ? (((await p.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 200)) : null;
    entry.ok = true;
  } catch (e) { entry.ok = false; entry.err = String(e.message).split('\n')[0]; }
  out.per_button_fresh.push(entry);
}
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-popups-fresh.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify(out.per_button_fresh.map((e) => ({ w: e.wanted, ok: e.ok, popup: (e.popup || e.err || '').slice(0, 80) })), null, 1));
