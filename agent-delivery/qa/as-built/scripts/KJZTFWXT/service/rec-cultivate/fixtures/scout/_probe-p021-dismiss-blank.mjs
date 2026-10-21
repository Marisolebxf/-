#!/usr/bin/env node
/** 短探 11（P0-21 r2 红归因 + 关弹层路径）：三验：
 *  ① 弹层开态是否跨 goto 恢复（goto 后 :visible 弹层计数与内容头）；
 *  ② 远处空白点击（避开弹层区域，如 (1500,600)/(960,950)）能否关掉恢复的弹层；
 *  ③ 关弹层后 2nd/3rd 枚按钮原生 click（无 force）是否可点且弹层内容切换为各自锚点；
 *  ④ r2 场景复现：评审关态 + 弹层开态遗留 → opener(.persona-switch).click 是否超时、先关弹层后是否恢复可点。
 *  产出 scout-p021-dismiss-blank.json。0 POST 只读。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const URL_CULT = baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate';
const out = { probed_at: new Date().toISOString(), purpose: 'P0-21 popup persists across goto? blank-click dismiss? then native click 2nd/3rd' };
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
const visPops = async () => {
  const pops = page.locator('.arco-trigger-popup:visible, .arco-popover:visible');
  const n = await pops.count();
  let head = '';
  if (n) head = ((await pops.nth(0).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 60);
  return { n, head };
};
// 开评审（沿用成熟路径）
await page.goto(URL_CULT, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2400);
let m = (await page.locator('main').first().innerText().catch(() => '')) || '';
if (!/培育综合分未入/.test(m)) {
  let opener = page.locator('.persona-switch').first();
  if (!(await opener.isVisible().catch(() => false))) opener = page.locator('[class*="persona" i]').first();
  await opener.click({ timeout: 5000 });
  await page.waitForTimeout(800);
  const sw = page.locator('button[role=switch][aria-label="内部评审模式"], [aria-label="内部评审模式"]').first();
  let checked = await sw.getAttribute('aria-checked').catch(() => null);
  if (checked === null) { const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]'); checked = /arco-switch-checked/.test((await holder.first().getAttribute('class').catch(() => '')) || '') ? 'true' : 'false'; }
  if (checked !== 'true') { await sw.click({ timeout: 5000 }); await page.waitForTimeout(1200); }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(800);
}
// ① 点开第 1 枚弹层
const b1 = page.locator('button.trace-info-icon[aria-label^="培育服务机构推荐分析"]').first();
await b1.click({ timeout: 5000 }).catch((e) => { out.open1_err = String(e.message).split('\n')[0]; });
await page.waitForTimeout(1000);
out.after_open1 = await visPops();
// goto 后弹层是否恢复
await page.goto(URL_CULT, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2200);
out.after_goto = await visPops();
// ② 远处空白点击关弹层（多坐标试）
out.blank_trials = [];
for (const [x, y] of [[1500, 600], [960, 950], [1800, 1000]]) {
  await page.mouse.click(x, y).catch(() => {});
  await page.waitForTimeout(600);
  const v = await visPops();
  out.blank_trials.push({ x, y, ...v });
  if (!v.n) break;
}
await page.screenshot({ path: path.join(__dirname, 'p021-blank.png') }).catch(() => {});
// ③ 关弹层后原生 click 2nd 枚
if (!(await visPops()).n) {
  const b2 = page.locator('button.trace-info-icon[aria-label^="分析配置"]').first();
  try {
    await b2.click({ timeout: 5000 });
    await page.waitForTimeout(1000);
    out.native_click_2nd = { ok: true, ...(await visPops()) };
  } catch (e) { out.native_click_2nd = { ok: false, err: String(e.message).split('\n')[0] }; }
}
// ④ r2 场景：关评审 → 留弹层开态 → goto → opener 可点性
// （先把评审关掉）
let opener2 = page.locator('.persona-switch').first();
if (!(await opener2.isVisible().catch(() => false))) opener2 = page.locator('[class*="persona" i]').first();
try { await opener2.click({ timeout: 5000 }); await page.waitForTimeout(800);
  const sw = page.locator('button[role=switch][aria-label="内部评审模式"], [aria-label="内部评审模式"]').first();
  let checked = await sw.getAttribute('aria-checked').catch(() => null);
  if (checked === null) { const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]'); checked = /arco-switch-checked/.test((await holder.first().getAttribute('class').catch(() => '')) || '') ? 'true' : 'false'; }
  if (checked !== 'false') { await sw.click({ timeout: 5000 }); await page.waitForTimeout(1200); }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(500);
  out.r2_scenario_review_off = true;
} catch (e) { out.r2_scenario_err = String(e.message).split('\n')[0]; }
await page.goto(URL_CULT, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2400);
out.r2_after_goto = await visPops();
// opener 直点
const opener3 = page.locator('.persona-switch').first();
out.r2_opener_visible = await opener3.isVisible().catch(() => false);
try { await opener3.click({ timeout: 5000 }); out.r2_opener_click = 'ok'; await page.waitForTimeout(600);
  // 关菜单收场
  await page.keyboard.press('Escape').catch(() => {});
} catch (e) { out.r2_opener_click = String(e.message).split('\n')[0]; }
// 若弹层开着，先空白关掉再试点 opener
if ((await visPops()).n) {
  await page.mouse.click(1500, 600).catch(() => {});
  await page.waitForTimeout(600);
  out.r2_after_blank = await visPops();
  try { await opener3.click({ timeout: 5000 }); out.r2_opener_click_after_blank = 'ok'; await page.keyboard.press('Escape').catch(() => {}); } catch (e) { out.r2_opener_click_after_blank = String(e.message).split('\n')[0]; }
}
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-dismiss-blank.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify(out, null, 1));
