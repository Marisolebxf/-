#!/usr/bin/env node
/** 短探 7（P0-21 定稿验证）：镜像脚本路径——同页顺序 e.click() 三枚按钮（不 goto，避免丢草稿参数）。
 *  ① 清 storage 全新会话：验证干净态下 2/3 枚原生可点（无遮挡）+ 采三枚各自弹层锚点全文头；
 *  ② 同页顺序 e.click() 1→2→3：每步后 filter(hasText 锚点) 可见性 —— 脚本断言口径预验。
 *  产出 scout-p021-seq.json。0 POST 只读。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const URL_CULT = baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate';
const out = { probed_at: new Date().toISOString(), purpose: 'P0-21 clean-session native clickability per button + sequential same-page e.click() popup anchors' };
const labels = ['培育服务机构推荐分析', '分析配置', '培育模型权重'];
const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await ctx.newPage();
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
// —— ① 干净会话逐枚原生点击（每枚清 storage 重进）——
out.clean_native = [];
for (const lb of labels) {
  await page.evaluate(() => { try { sessionStorage.clear(); localStorage.clear(); } catch {} });
  await page.goto(URL_CULT, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2400);
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
  const b = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  const e0 = { wanted: lb };
  try {
    await b.click({ timeout: 5000 });
    await page.waitForTimeout(1000);
    const p = page.locator('.arco-trigger-popup:visible, .arco-popover:visible').filter({ hasText: lb });
    e0.native_click_ok = true;
    e0.popup_match_count = await p.count();
    if (await p.count()) e0.popup_head = ((await p.first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 150);
  } catch (e) { e0.native_click_ok = false; e0.err = String(e.message).split('\n')[0]; }
  out.clean_native.push(e0);
}
// —— ② 同页顺序 e.click()（不清 storage 不 goto，镜像脚本）——
await page.evaluate(() => { try { sessionStorage.clear(); localStorage.clear(); } catch {} });
await page.goto(URL_CULT, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2400);
const close2 = page.locator('button[aria-label="关闭对比篮"]');
if ((await close2.count()) && (await close2.first().isVisible().catch(() => false))) { try { await close2.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
out.seq_eclick = [];
for (const lb of labels) {
  const b = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  const e1 = { wanted: lb };
  try {
    await b.evaluate((e) => e.click());
    await page.waitForTimeout(1000);
    const p = page.locator('.arco-trigger-popup:visible, .arco-popover:visible').filter({ hasText: lb });
    e1.match_count = await p.count();
    e1.match_visible = (await p.count()) ? await p.first().isVisible().catch(() => false) : false;
    if (await p.count()) e1.popup_head = ((await p.first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 120);
  } catch (e) { e1.err = String(e.message).split('\n')[0]; }
  out.seq_eclick.push(e1);
}
// 顺序点击后弹层叠着，验证 persona 菜单仍可开（右上远端）+ 评审开关可达（toggle-off 前置）
const opener = page.locator('.persona-switch').first();
out.persona_reachable_after_popups = await opener.isVisible().catch(() => false);
try { await opener.click({ timeout: 4000 }); await page.waitForTimeout(700); } catch (e) { out.persona_open_err = String(e.message).split('\n')[0]; }
const sw = page.locator('button[role=switch][aria-label="内部评审模式"]').first();
out.review_switch_count_after_popups = await page.locator('button[role=switch][aria-label="内部评审模式"]').count();
await page.keyboard.press('Escape').catch(() => {});
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-seq.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify(out, null, 1));
