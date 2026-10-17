#!/usr/bin/env node
/** 短探 2（P0-21 补充）：三枚追溯按钮「逐一点击」的弹层收起路径验证。
 *  探针 1 实证：首枚点击后弹层常驻（TriggerPopup），Escape 无效，二三枚被遮挡 timeout。
 *  本验证依次试：①再点按钮自身（toggle）②page.mouse.click 页面空白 ③Escape，找到可行收起路径后依次点三枚取弹层文本。
 *  产出 scout-p021-popups.json。0 POST 只读。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const out = { probed_at: new Date().toISOString(), purpose: 'P0-21 trace popup dismiss path + per-button popup texts' };
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
await page.waitForTimeout(2200);
const close = page.locator('button[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
const popCount = async () => await page.locator('.arco-trigger-popup:visible, .arco-popover:visible').count();
const popText = async () => { const p = page.locator('.arco-trigger-popup:visible, .arco-popover:visible').first(); if ((await p.count()) && (await p.isVisible().catch(() => false))) return (((await p.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 200)); return null; };

const labels = ['培育服务机构推荐分析', '分析配置', '培育模型权重'];
// —— 弹层收起路径验证（首枚）——
const b1 = page.locator('button.trace-info-icon[aria-label^="培育服务机构推荐分析"]').first();
await b1.click({ timeout: 5000 });
await page.waitForTimeout(900);
out.open_popup = await popText();
out.dismiss_trials = {};
// ① toggle：再点按钮自身
try { await b1.click({ timeout: 2000 }); await page.waitForTimeout(500); } catch (e) { out.dismiss_trials.toggle_err = String(e.message).split('\n')[0]; }
out.dismiss_trials.after_toggle = await popCount();
if (await popCount()) {
  // ② 点页面空白（main 区顶部标题附近偏左，避开控件）
  try { await page.mouse.click(400, 260); await page.waitForTimeout(500); } catch (e) { out.dismiss_trials.blank_err = String(e.message).split('\n')[0]; }
  out.dismiss_trials.after_blank_click = await popCount();
}
if (await popCount()) {
  // ③ Escape
  try { await page.keyboard.press('Escape'); await page.waitForTimeout(500); } catch {}
  out.dismiss_trials.after_escape = await popCount();
}
// —— 依次点三枚取弹层 ——
out.per_button = [];
for (const lb of labels) {
  const b = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  const entry = { wanted: lb };
  try {
    await b.click({ timeout: 5000 });
    await page.waitForTimeout(900);
    entry.popup = await popText();
    entry.ok = true;
    // 收起（按已验证路径）
    try { await b.click({ timeout: 2000 }); await page.waitForTimeout(400); } catch {}
    if (await popCount()) { try { await page.mouse.click(400, 260); await page.waitForTimeout(400); } catch {} }
    entry.pop_after_dismiss = await popCount();
  } catch (e) { entry.ok = false; entry.err = String(e.message).split('\n')[0]; }
  out.per_button.push(entry);
}
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-popups.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify(out, null, 1));
