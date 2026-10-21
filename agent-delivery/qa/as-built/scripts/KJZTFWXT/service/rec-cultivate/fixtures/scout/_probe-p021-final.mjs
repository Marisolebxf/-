#!/usr/bin/env node
/** 短探 8（P0-21 定稿验证 · 终版）：探针 2/6 已实证路径的完整链预演（不清 storage、不 goto 循环中）：
 *  ① goto → 确保评审开（长提示锚点）→ 三枚按钮可见 enabled（aria-label 各自定位）；
 *  ② 同页顺序 e.click() 1→2→3，每枚后 filter(hasText 锚点) 弹层可见 —— 「逐一点击」脚本口径；
 *  ③ 角标 aria-label 定位 + 可见 + 长提示全文片段（附录 A.5 对照）；
 *  ④ 构造草稿（权重 30 + 产业选定）→ 关评审 → reload → 零泄漏三重（追溯按钮 0 + 评审层 DOM 0 + 正文无泄漏字样）
 *     + 业务态不变（产业回显 + 四权重值 + 配置区骨架）；
 *  ⑤ 0 POST（只读往返）。
 *  产出 scout-p021-final.json + p021-final-*.png。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const URL_CULT = baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate';
const out = { probed_at: new Date().toISOString(), purpose: 'P0-21 full-chain rehearsal (final path: sequential e.click + filter anchors + toggle-off + reload zero-leak + draft-invariant)' };
const posts = [];
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('request', (r) => { if (r.method() === 'POST' && /\/topicAsync\/topic\/v1\/analysis\/tasks\/?(\?|$)/.test(r.url())) posts.push(r.url().slice(0, 120)); });
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
const main = async () => (await page.locator('main').first().innerText().catch(() => '')) || '';
const labels = ['培育服务机构推荐分析', '分析配置', '培育模型权重'];

// —— ① goto + 确保评审开 ——
await page.goto(URL_CULT, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2200);
const close = page.locator('button[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false)) && (await close.first().isEnabled().catch(() => false))) { try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
let m = await main();
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
  m = await main();
}
out.review_on_hint = /培育综合分未入/.test(m);
out.trace_all_labels = await page.locator('button.trace-info-icon').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label') || ''));
out.btn_states = [];
for (const lb of labels) {
  const b = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  out.btn_states.push({ wanted: lb, count: await b.count(), visible: await b.isVisible().catch(() => false), enabled: await b.isEnabled().catch(() => false) });
}

// —— ② 同页顺序 e.click()，各自弹层锚点（filter hasText）——
out.seq = [];
for (const lb of labels) {
  const b = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  const e1 = { wanted: lb };
  try {
    await b.evaluate((e) => e.click());
    await page.waitForTimeout(1000);
    const p = page.locator('.arco-trigger-popup:visible, .arco-popover:visible').filter({ hasText: lb });
    e1.match_count = await p.count();
    e1.match_visible = (await p.count()) ? await p.first().isVisible().catch(() => false) : false;
    if (await p.count()) e1.popup_head = ((await p.first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 130);
  } catch (e) { e1.err = String(e.message).split('\n')[0]; }
  out.seq.push(e1);
}
await page.screenshot({ path: path.join(__dirname, 'p021-final-review-on.png') }).catch(() => {});

// —— ③ 角标 + 长提示 ——
const badge = page.locator('[aria-label="指标未登记：培育综合分"]').first();
out.badge = { count: await page.locator('[aria-label="指标未登记：培育综合分"]').count(), visible: (await page.locator('[aria-label="指标未登记：培育综合分"]').count()) ? await badge.isVisible().catch(() => false) : false };
const m2 = await main();
const hi = m2.indexOf('培育综合分未入');
out.hint_fulltext = hi >= 0 ? m2.slice(Math.max(0, hi - 60), hi + 200).replace(/\s+/g, ' ') : null;
out.hint_parts = { weiru: /未入指标库|未入正式指标库/.test(m2), q063: m2.includes('Q063'), qsvc: m2.includes('Q-SVCCHAIN-05'), nogreen: /不改绿/.test(m2) };

// —— ④ 构造草稿（权重 30 + 产业=新一代信息技术）→ 关评审 → reload → 零泄漏 + 业务态不变 ——
const spin0 = page.locator('main [role=spinbutton]').first();
await spin0.click({ timeout: 5000 }).catch(() => {});
await spin0.fill('30');
await spin0.blur().catch(() => {});
await page.waitForTimeout(700);
const sel = page.locator('.industry-catalog-select').first();
const indBefore = ((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
out.draft = { weight1: String(await spin0.inputValue().catch(() => '')), industry_before: indBefore };
// persona 开关：弹层叠着时先收（点 body 空白区无效已证；试 Esc + 直接点 persona —— persona 在右上远端）
await page.keyboard.press('Escape').catch(() => {});
await page.waitForTimeout(300);
let opener2 = page.locator('.persona-switch').first();
if (!(await opener2.isVisible().catch(() => false))) opener2 = page.locator('[class*="persona" i]').first();
out.persona_open_ok = null;
try { await opener2.click({ timeout: 5000 }); out.persona_open_ok = true; } catch (e) { out.persona_open_ok = false; out.persona_err = String(e.message).split('\n')[0]; }
if (out.persona_open_ok) {
  await page.waitForTimeout(800);
  const sw = page.locator('button[role=switch][aria-label="内部评审模式"], [aria-label="内部评审模式"]').first();
  let checked = await sw.getAttribute('aria-checked').catch(() => null);
  if (checked === null) { const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]'); checked = /arco-switch-checked/.test((await holder.first().getAttribute('class').catch(() => '')) || '') ? 'true' : 'false'; }
  if (checked !== 'false') { await sw.click({ timeout: 5000 }); await page.waitForTimeout(1200); }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(500);
}
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2600);
const close3 = page.locator('button[aria-label="关闭对比篮"]');
if ((await close3.count()) && (await close3.first().isVisible().catch(() => false))) { try { await close3.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
const m3 = await main();
out.after = {};
out.after.trace_count = await page.locator('button.trace-info-icon').count();
out.after.badge_count = await page.locator('[aria-label="指标未登记：培育综合分"]').count();
out.after.review_dom = (await page.locator('[data-review-metric]').count()) + (await page.locator('.metric-spec-card').count());
out.after.leaks = {};
for (const k of ['评审', '需求追溯', '指标未登记', '培育综合分未入', 'Q063', 'Q-SVCCHAIN', 'GAP-', 'metric_id', 'M_SVC_REC_CULTIVATE_SCORE']) out.after.leaks[k] = m3.includes(k);
// 业务态
const spins = page.locator('main [role=spinbutton]');
out.after.spin_count = await spins.count();
out.after.weights = [];
for (let i = 0; i < 4; i++) out.after.weights.push(String(await spins.nth(i).inputValue().catch(() => '')));
const sel2 = page.locator('.industry-catalog-select').first();
out.after.industry_echo = ((await sel2.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
out.after.business = {};
for (const k of ['分析配置', '重点产业方向', '机构类型', '高校', '科研院所', '企业', '服务环节', '培育评估模型', '现有规模', '技术创新能力', '服务成效', '市场缺口', '权重合计', '恢复默认权重', '开始分析', '演示模型口径']) out.after.business[k] = m3.includes(k);
out.after.url = page.url();
out.after.view_residue = /view=processing|view=result/.test(out.after.url);
await page.screenshot({ path: path.join(__dirname, 'p021-final-after-off.png') }).catch(() => {});
out.posts_total = posts.length;
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-final.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify({ hint: out.review_on_hint, btns: out.btn_states.map((b) => b.visible && b.enabled), seq_ok: out.seq.map((s) => s.match_count > 0), badge: out.badge, persona_ok: out.persona_open_ok, after: { trace: out.after.trace_count, badge: out.after.badge_count, dom: out.after.review_dom, leaks: Object.values(out.after.leaks).filter(Boolean).length, w: out.after.weights, ind: out.after.industry_echo, posts: posts.length } }, null, 1));
