#!/usr/bin/env node
/** 短探 10（P0-21 修稿终验）：force click 三枚顺序「逐一点击」全链验证。
 *  探针 9 定案：e.click() 开不了 Arco Trigger（无 pointer 序列）；force native click 可开且绕过常驻层拦截。
 *  本验：单页顺序 force click 1→2→3，每步后收集全部 :visible 弹层合并文本，断言含各自锚点（培育服务机构推荐分析/分析配置/培育模型权重）。
 *  另验：改权重 30 后「权重合计」文案实际形态（105% 未对齐?）。产出 scout-p021-force3.json。0 POST 只读。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const out = { probed_at: new Date().toISOString(), purpose: 'P0-21 sequential force-click x3 popups + weight-sum text with draft 30' };
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
const labels = ['培育服务机构推荐分析', '分析配置', '培育模型权重'];
const visPopsText = async () => {
  const pops = page.locator('.arco-trigger-popup:visible, .arco-popover:visible');
  const n = await pops.count();
  const texts = [];
  for (let i = 0; i < n; i++) texts.push((await pops.nth(i).innerText().catch(() => '')) || '');
  return { count: n, joined: texts.join(' || ').replace(/\s+/g, ' ') };
};
out.seq_force = [];
for (const lb of labels) {
  const b = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  const e1 = { wanted: lb };
  try {
    await b.click({ force: true, timeout: 5000 });
    await page.waitForTimeout(1100);
    const v = await visPopsText();
    e1.visible_pop_count = v.count;
    e1.anchor_in_visible = v.joined.includes(lb);
    e1.joined_head = v.joined.slice(0, 140);
  } catch (e) { e1.err = String(e.message).split('\n')[0]; }
  out.seq_force.push(e1);
}
await page.screenshot({ path: path.join(__dirname, 'p021-force3.png') }).catch(() => {});
// 权重合计文案（草稿 30 后）
const spin0 = page.locator('main [role=spinbutton]').first();
await spin0.click({ timeout: 5000 }).catch(() => {});
await spin0.fill('30');
await spin0.blur().catch(() => {});
await page.waitForTimeout(800);
const m = (await page.locator('main').first().innerText().catch(() => '')) || '';
const wIdx = m.indexOf('权重合计');
out.weight_sum_text = wIdx >= 0 ? m.slice(wIdx, wIdx + 40).replace(/\s+/g, ' ') : null;
out.restore_btn_count = await page.getByRole('button', { name: '恢复默认权重', exact: true }).count();
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-force3.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify({ seq: out.seq_force.map((e) => ({ w: e.wanted, ok: e.anchor_in_visible, pops: e.visible_pop_count })), weight_sum: out.weight_sum_text }, null, 1));
