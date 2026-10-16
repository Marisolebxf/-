#!/usr/bin/env node
/** 短探（P0-21 / FUNC-01281 评审模式零泄漏 前置实证）：评审开态采集——
 *  ① trace-info-icon aria-label 全集（用例指定三枚：培育服务机构推荐分析/分析配置/培育模型权重）；
 *  ② 「指标未登记：培育综合分」角标现场形态（aria-label icon 按钮 vs 文本；红问号形态记 observed）；
 *  ③ 长提示全文（附录 A.5 对照：未入正式指标库 / 禁止前端重算 / Q063 / Q-SVCCHAIN-05）；
 *  ④ 点击三个追溯按钮各一次（TriggerPopup 弹层形态记 observed，P4 不判关闭缺失）；
 *  ⑤ 构造非默认草稿（权重键入 30）基线，供脚本「业务态不变」断言设计。
 *  只读往返，0 POST（不起任务）。产出 scout-p021-review.json + p021-*.png。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import fileURLToPathShim from 'node:url';

const __dirname = path.dirname(fileURLToPathShim.fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const out = { probed_at: new Date().toISOString(), entry: 'svc-rec-cultivate', purpose: 'P0-21 / FUNC-01281 review-mode zero-leak pre-evidence (trace buttons aria-labels, unregistered badge form, long hint fulltext, popup behavior, draft baseline)' };
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
const URL_CULT = baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate';
await page.goto(URL_CULT, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2200);
const close = page.locator('button[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false)) && (await close.first().isEnabled().catch(() => false))) { try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }

// —— ① 确保评审模式开启（P3 路径，自适应）——
const ensureReview = async (wantOn) => {
  const m = await main();
  const hasHint = /培育综合分未入/.test(m);
  let n = await page.locator('button.trace-info-icon').count();
  const isOn = () => n >= 2 || hasHint;
  if (wantOn === true && isOn()) return { already: true, trace_count: n, hint: hasHint };
  if (wantOn === false && !(await page.locator('button.trace-info-icon').count())) return { already: true, trace_count: 0, hint: false };
  let opener = page.locator('.persona-switch').first();
  if (!(await opener.isVisible().catch(() => false))) opener = page.locator('[class*="persona" i]').first();
  await opener.click({ timeout: 5000 });
  await page.waitForTimeout(800);
  const sw = page.locator('button[role=switch][aria-label="内部评审模式"], [aria-label="内部评审模式"]').first();
  let checked = await sw.getAttribute('aria-checked').catch(() => null);
  if (checked === null) { const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]'); checked = /arco-switch-checked/.test((await holder.first().getAttribute('class').catch(() => '')) || '') ? 'true' : 'false'; }
  const target = wantOn ? 'true' : 'false';
  if (checked !== target) { await sw.click({ timeout: 5000 }); await page.waitForTimeout(1200); }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(800);
  return { toggled: true, before: checked, after: target };
};
out.review_on = await ensureReview(true);
await page.waitForTimeout(800);

// —— ① trace-info-icon aria-label 全集 ——
out.trace_labels = await page.locator('button.trace-info-icon').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label') || '(no-aria-label)'));
out.trace_count = out.trace_labels.length;
const wanted = ['培育服务机构推荐分析需求追溯', '分析配置需求追溯', '培育模型权重需求追溯'];
out.wanted_hit = {};
for (const lb of wanted) {
  const b = page.locator('button.trace-info-icon').filter({ hasText: '' }).locator(`[aria-label*="${lb.replace(/需求追溯$/, '')}"]`);
  out.wanted_hit[lb] = (await page.locator(`button.trace-info-icon[aria-label*="${lb.replace(/需求追溯$/, '')}"]`).count()) > 0;
}
out.trace_visible_enabled = [];
for (let i = 0; i < out.trace_count; i++) {
  const b = page.locator('button.trace-info-icon').nth(i);
  out.trace_visible_enabled.push({ label: out.trace_labels[i], visible: await b.isVisible().catch(() => false), enabled: await b.isEnabled().catch(() => false) });
}

// —— ② 「指标未登记：培育综合分」角标现场形态 ——
const badgeSel = '[aria-label="指标未登记：培育综合分"]';
out.badge = {};
out.badge.aria_label_count = await page.locator(badgeSel).count();
out.badge.text_count = await page.getByText('指标未登记：培育综合分').count();
const badgeEl = page.locator(badgeSel).first();
if (out.badge.aria_label_count) {
  out.badge.tag = await badgeEl.evaluate((e) => e.tagName.toLowerCase() + '.' + String(e.className).slice(0, 80));
  out.badge.visible = await badgeEl.isVisible().catch(() => false);
  out.badge.enabled = await badgeEl.isEnabled().catch(() => false);
  out.badge.parent_text = ((await badgeEl.locator('xpath=ancestor::div[1]').innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 160);
  out.badge.outer_snip = ((await badgeEl.evaluate((e) => e.outerHTML).catch(() => '')) || '').slice(0, 300);
}
// 红问号形态旁证：页面内含「？」或 IconQuestionCircle 类
out.badge.question_icon_evidence = await page.locator('[class*="question" i], [class*="Question" i]').count();

// —— ③ 长提示全文（附录 A.5 对照）——
const m1 = await main();
const hintIdx = m1.indexOf('培育综合分未入');
out.long_hint_fulltext = hintIdx >= 0 ? m1.slice(Math.max(0, hintIdx - 40), hintIdx + 240).replace(/\s+/g, ' ').trim() : null;
out.hint_hits = {
  weiru: /未入正式指标库|未入指标库/.test(m1),
  no_rescore: /禁止前端按四维度权重重算|禁止.*重算/.test(m1),
  q063: m1.includes('Q063'),
  q_svcchain: m1.includes('Q-SVCCHAIN-05'),
  no_green: /不改绿|禁止改绿/.test(m1),
  score_only: /只展示 Java rec-list 上送/.test(m1),
};

// —— ④ 点击三个追溯按钮（弹层形态记 observed）——
out.popups = [];
for (const lb of wanted) {
  const key = lb.replace(/需求追溯$/, '');
  const b = page.locator(`button.trace-info-icon[aria-label*="${key}"]`).first();
  if (!(await b.count())) { out.popups.push({ wanted: lb, found: false }); continue; }
  try {
    await b.click({ timeout: 5000 });
    await page.waitForTimeout(900);
    const pop = page.locator('.arco-trigger-popup:visible, .arco-popover:visible').first();
    const popTxt = (await pop.count()) && (await pop.isVisible().catch(() => false)) ? ((await pop.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 220) : null;
    out.popups.push({ wanted: lb, found: true, popup_text: popTxt });
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(400);
  } catch (e) {
    out.popups.push({ wanted: lb, found: true, click_error: String(e.message).split('\n')[0] });
  }
}
await page.screenshot({ path: path.join(__dirname, 'p021-review-on.png') }).catch(() => {});

// —— ⑤ 构造非默认草稿基线（权重键入 30），关评审 + reload 后回读（业务态不变预验）——
const spin0 = page.locator('main [role=spinbutton]').first();
await spin0.click({ timeout: 5000 });
await spin0.fill('30');
await spin0.blur().catch(() => {});
await page.waitForTimeout(700);
out.draft_weight_before_off = String(await spin0.inputValue().catch(() => ''));

// —— 关评审 + reload，零泄漏预验 ——
out.review_off = await ensureReview(false);
await page.waitForTimeout(500);
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);
const close2 = page.locator('button[aria-label="关闭对比篮"]');
if ((await close2.count()) && (await close2.first().isVisible().catch(() => false))) { try { await close2.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
const m2 = await main();
out.after_off_reload = {};
out.after_off_reload.trace_count = await page.locator('button.trace-info-icon').count();
out.after_off_reload.badge_aria_label_count = await page.locator(badgeSel).count();
out.after_off_reload.review_dom = (await page.locator('[data-review-metric]').count()) + (await page.locator('.metric-spec-card').count());
for (const k of ['评审', '需求追溯', '指标未登记', '培育综合分未入', 'Q063', 'Q-SVCCHAIN', 'GAP-', 'metric_id', 'M_SVC_REC_CULTIVATE_SCORE']) {
  out.after_off_reload['leak_' + k] = m2.includes(k);
}
out.after_off_reload.spin_count = await page.locator('main [role=spinbutton]').count();
out.after_off_reload.weight_first = out.after_off_reload.spin_count ? String(await page.locator('main [role=spinbutton]').first().inputValue().catch(() => '')) : null;
out.after_off_reload.business_terms = {};
for (const k of ['分析配置', '重点产业方向', '机构类型', '高校', '科研院所', '企业', '服务环节', '培育评估模型', '现有规模', '技术创新能力', '服务成效', '市场缺口', '权重合计', '恢复默认权重', '开始分析', '演示模型口径']) {
  out.after_off_reload.business_terms[k] = m2.includes(k);
}
out.after_off_reload.url = page.url();
await page.screenshot({ path: path.join(__dirname, 'p021-review-off.png') }).catch(() => {});
out.posts_total = posts.length;
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-review.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify({ traces: out.trace_labels, badge_aria: out.badge.aria_label_count, hint: !!out.long_hint_fulltext, hint_hits: out.hint_hits, popups_ok: out.popups.filter((p) => p.popup_text).length, draft_w: out.draft_weight_before_off, off: { trace: out.after_off_reload.trace_count, badge: out.after_off_reload.badge_aria_label_count, dom: out.after_off_reload.review_dom, w: out.after_off_reload.weight_first, posts: posts.length } }, null, 1));
