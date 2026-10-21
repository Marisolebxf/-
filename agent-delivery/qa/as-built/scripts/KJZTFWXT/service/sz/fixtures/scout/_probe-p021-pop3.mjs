// _probe-p021-pop3.mjs — 弹层存留根因诊断：
//   a) reload 是否真空文档（window marker 复核）
//   b) localStorage/sessionStorage 是否有 pin/trace/review 键
//   c) 弹层内有无关闭按钮；再点同一按钮是否 toggle 收起
//   d) goto 真导航是否清弹层
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
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
if (checked !== 'true') { await sw.click({ timeout: 5000 }); await page.waitForTimeout(1200); }
await page.keyboard.press('Escape').catch(() => {});
await page.waitForTimeout(800);
out.switch = checked;

const popVis = async () => await page.evaluate(() => {
  const pops = Array.from(document.querySelectorAll('.arco-trigger-popup, .arco-popover'));
  const vis = pops.filter((e) => !!(e.offsetWidth || e.offsetHeight));
  return { total: pops.length, visible: vis.length, sample: (vis[0] ? (vis[0].innerText || '').replace(/\s+/g, ' ').slice(0, 60) : '') };
});

const storageDump = async () => await page.evaluate(() => {
  const grab = (s) => { const o = {}; for (let i = 0; i < s.length; i++) { const k = s.key(i); const v = s.getItem(k) || ''; if (/review|trace|persona|popover|pin|popup/i.test(k + ' ' + v.slice(0, 200))) o[k] = v.slice(0, 200); } return o; };
  return { local: grab(localStorage), session: grab(sessionStorage) };
});

out.storage_before = await storageDump();

// 点「分析配置」按钮
const btnSel = 'button.trace-info-icon[aria-label*="分析配置"]';
await page.locator(btnSel).first().click({ timeout: 5000 });
await page.waitForTimeout(1200);
out.after_click = await popVis();

// b) 弹层内有无关闭按钮 / aria
out.pop_structure = await page.evaluate(() => {
  const vis = Array.from(document.querySelectorAll('.arco-trigger-popup, .arco-popover')).filter((e) => !!(e.offsetWidth || e.offsetHeight));
  const p = vis[0];
  if (!p) return null;
  const btns = Array.from(p.querySelectorAll('button, [class*=close], [aria-label*=关闭]')).map((b) => ({ tag: b.tagName, cls: (b.className || '').toString().slice(0, 60), aria: b.getAttribute('aria-label'), text: (b.innerText || '').slice(0, 20) }));
  return { cls: p.className, role: p.getAttribute('role'), btns: btns.slice(0, 6) };
});

// c) 再点同一按钮是否 toggle
await page.locator(btnSel).first().click({ timeout: 5000 }).catch(() => {});
await page.waitForTimeout(800);
out.after_second_click = await popVis();

// 若还开着，点页面空白处
if ((await popVis()).visible > 0) {
  await page.mouse.click(960, 540).catch(() => {});
  await page.waitForTimeout(800);
  out.after_body_click = await popVis();
}

// d) 真导航 goto（带新参数）是否清
await page.locator(btnSel).first().click({ timeout: 5000 }).catch(() => {});
await page.waitForTimeout(800);
out.before_goto = await popVis();
await page.goto(BASE + ROUTE + '&nav=2', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2000);
out.after_goto = await popVis();
out.storage_after = await storageDump();

// e) reload marker 复核（真空文档？）
await page.evaluate(() => { window.__marker = 'alive'; });
await page.locator(btnSel).first().click({ timeout: 5000 }).catch(() => {});
await page.waitForTimeout(800);
out.before_reload = await popVis();
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);
out.marker_after_reload = await page.evaluate(() => window.__marker || 'gone(fresh-doc)');
out.after_reload = await popVis();
out.storage_after_reload = await storageDump();

fs.writeFileSync(path.join(__dirname, '_probe-p021-pop3.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
