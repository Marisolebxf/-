#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-sz BATCH32 缺口 18 条（P0-06~P0-23）现场核实。
 * 产物落同目录 scout-b32-*.json；勿当 runner。遵守探针公约（无 IDE/有头浏览器）。
 * 核实点：
 *  S1 历史结果态完整 DOM（框架卡/对比板/结论/梯队/诚实空）
 *  S2 结果态指标多选交互（取消/全取消/恢复 + URL sz_metrics）
 *  S3 结果态返回配置 → draft 草稿恢复（URL industry=）
 *  S4 评审开关 persona-menu 流程（开→追溯挂点→关→零泄漏）
 *  S5 配置区同条件拦截（选定产业后等待 gate 提示）
 *  S6 查看过程按钮（过程壳）
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const route = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const outDir = __dirname;

const dump = (name, data) => {
  fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2), 'utf8');
};

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function closeBasket(page) {
  for (let i = 0; i < 3; i++) {
    const close = page.locator('[aria-label="关闭对比篮"]');
    if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
      await close.first().click().catch(() => {});
      await page.waitForTimeout(300);
    } else break;
  }
}

async function mainText(page, n = 80) {
  return page
    .locator('main')
    .first()
    .innerText()
    .then((t) => t.split('\n').map((s) => s.trim()).filter(Boolean).slice(0, n))
    .catch(() => []);
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const report = { probed_at: new Date().toISOString(), stages: {} };

// ---------- 登录 + 深链 ----------
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
if (page.url().includes('/login')) { await ensureLogin(page); await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded' }); }
await page.waitForTimeout(2500);
await closeBasket(page);

// ---------- S1: 经历史进结果态 ----------
await page.getByRole('tab', { name: '分析记录' }).first().click();
await page.waitForTimeout(2000);
const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /shenzhen/ }).filter({ hasText: /已完成/ }).first();
const viewBtn = row.getByRole('button', { name: /查看结果/ }).first();
await viewBtn.click({ timeout: 8000 });
await page.waitForTimeout(3500);
await closeBasket(page);
const s1Url = page.url();
const s1 = {
  url: s1Url,
  title: await page.title(),
  framework_visible: await page.locator('[data-testid="svc-eco-sz-framework"]').count(),
  framework_name: ((await page.locator('[data-testid="svc-eco-sz-framework-name"]').innerText().catch(() => '')) || '').trim(),
  caliber: ((await page.locator('[data-testid="svc-eco-sz-framework-caliber"]').innerText().catch(() => '')) || '').trim(),
  pending: ((await page.locator('[data-testid="svc-eco-sz-framework-pending"]').innerText().catch(() => '')) || '').trim(),
  metric_list_li: await page.locator('[data-testid="svc-eco-sz-metric-list"] li').count(),
  metric_list_text: ((await page.locator('[data-testid="svc-eco-sz-metric-list"]').innerText().catch(() => '')) || '').replace(/\n/g, ' | ').slice(0, 500),
  completeness_exclude: ((await page.locator('[data-testid="svc-eco-sz-completeness-exclude"]').innerText().catch(() => '')) || '').trim(),
  compare_metrics_text: ((await page.locator('[data-testid="svc-eco-sz-compare-metrics"]').innerText().catch(() => '')) || '').replace(/\n/g, ' | ').slice(0, 500),
  compare_checkbox_count: await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox').count(),
  compare_checkbox_checked: await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').count(),
  compare_caliber: ((await page.locator('[data-testid="svc-eco-sz-compare-caliber"]').innerText().catch(() => '')) || '').trim(),
  compare_empty: await page.locator('[data-testid="svc-eco-sz-compare-empty"]').count(),
  compare_grid: await page.locator('[data-testid="svc-eco-sz-compare-grid"]').count(),
  tier_section: await page.locator('[data-testid="svc-eco-sz-tier"]').count(),
  conclusions_ul: await page.locator('[data-testid="svc-eco-sz-conclusions"]').count(),
  result_bar: ((await page.locator('[data-testid="svc-eco-sz-result-bar"]').innerText().catch(() => '')) || '').replace(/\n/g, ' | ').slice(0, 300),
  rerun_btn: await page.getByRole('button', { name: '重新分析' }).count(),
  main_text: await mainText(page, 60),
};
dump('scout-b32-s1-result-state.json', s1);
report.stages.s1_result = { url: s1Url, has_framework: s1.framework_visible > 0, has_city: s1.compare_grid > 0, honest_empty: s1.compare_empty > 0 };
await page.screenshot({ path: path.join(outDir, 'scout-b32-s1-result.png'), fullPage: false });

// ---------- S2: 指标多选交互（取消一项→全取消→恢复） ----------
const s2 = { steps: [] };
try {
  const boxes = page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox');
  const n = await boxes.count();
  s2.checkbox_n = n;
  // 取消第一项
  await boxes.nth(0).click({ timeout: 5000 });
  await page.waitForTimeout(800);
  s2.steps.push({ act: 'uncheck#1', url_sz_metrics: (page.url().match(/sz_metrics=([^&]*)/) || [])[1] || null, checked: await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').count() });
  // 再点第一项恢复
  await boxes.nth(0).click({ timeout: 5000 });
  await page.waitForTimeout(800);
  s2.steps.push({ act: 'recheck#1', url_sz_metrics: (page.url().match(/sz_metrics=([^&]*)/) || [])[1] || null, checked: await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').count() });
  // 全取消
  for (let i = 0; i < n; i++) {
    const c = await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').count();
    if (!c) break;
    await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').first().click({ timeout: 5000 });
    await page.waitForTimeout(600);
  }
  await page.waitForTimeout(600);
  s2.none_warn = ((await page.locator('[data-testid="svc-eco-sz-compare-none"]').innerText().catch(() => '')) || '').trim();
  s2.steps.push({ act: 'uncheck-all', url_sz_metrics: (page.url().match(/sz_metrics=([^&]*)/) || [])[1] || null, none_warn_visible: await page.locator('[data-testid="svc-eco-sz-compare-none"]').count() > 0 });
  // 恢复全选（刷新页面验证 none 持久化）
  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  await closeBasket(page);
  s2.after_reload_url = page.url();
  s2.after_reload_none_warn = await page.locator('[data-testid="svc-eco-sz-compare-none"]').count();
  s2.after_reload_checked = await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').count();
  // 恢复：全部勾回（点击第一个可见 checkbox 逐个）
  for (let i = 0; i < 5; i++) {
    const total = await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox').count();
    const checked = await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').count();
    if (checked >= total) break;
    await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox').nth(i).click({ timeout: 5000 });
    await page.waitForTimeout(600);
  }
  s2.restored_checked = await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').count();
  s2.restored_url_param = (page.url().match(/sz_metrics=([^&]*)/) || [])[1] || null;
} catch (e) {
  s2.error = String(e).slice(0, 300);
}
dump('scout-b32-s2-metric-toggles.json', s2);
report.stages.s2_metric_toggles = { ok: !s2.error, none_warn: s2.none_warn };

// ---------- S3: 返回配置 → draft 草稿 ----------
const s3 = {};
try {
  const back = page.getByRole('button', { name: '返回配置' }).first();
  if (await back.count()) {
    await back.click({ timeout: 5000 });
    await page.waitForTimeout(1500);
    s3.url_after_back = page.url();
    s3.draft_param = /draft=1/.test(s3.url_after_back);
    const selVal = ((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
    s3.industry_echo = selVal;
    s3.start_btn = await page.getByRole('button', { name: '开始分析', exact: true }).count();
    s3.rerun_visible = await page.getByRole('button', { name: '重新分析', exact: true }).count();
    s3.config_note = ((await page.locator('[data-testid="svc-eco-analysis-config"]').innerText().catch(() => '')) || '').replace(/\n/g, ' | ').slice(0, 400);
  } else { s3.error = '无返回配置按钮'; }
} catch (e) { s3.error = String(e).slice(0, 300); }
dump('scout-b32-s3-back-config.json', s3);
report.stages.s3_back_config = { ok: !s3.error, url: s3.url_after_back, industry: s3.industry_echo };
await page.screenshot({ path: path.join(outDir, 'scout-b32-s3-back-config.png'), fullPage: false });

// ---------- S4: 评审开关 ----------
const s4 = {};
try {
  // 回到干净配置页
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await closeBasket(page);
  // 打开 persona 菜单（右上 persona-switch）
  const pBtn = page.locator('button.persona-switch').first();
  if (await pBtn.count()) {
    await pBtn.click({ timeout: 5000 });
    await page.waitForTimeout(800);
    const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
    s4.switch_found = await sw.count();
    // 若当前为关，打开它
    const ariaOn = (await sw.getAttribute('aria-checked').catch(() => null));
    s4.initial_aria_checked = ariaOn;
    if (ariaOn !== 'true') {
      await sw.click({ timeout: 5000 });
      await page.waitForTimeout(1000);
    }
    s4.after_on_leak_words = {};
    // 关闭菜单（点击页面其他位置）
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(600);
    await page.locator('main').first().click({ position: { x: 10, y: 10 } }).catch(() => {});
    await page.waitForTimeout(600);
    const bodyOn = ((await page.locator('body').innerText().catch(() => '')) || '');
    s4.trace_icon_n_on = await page.locator('[aria-label*="需求追溯"]').count();
    s4.review_note_on = /评审模式/.test(bodyOn);
    // 重新开菜单关掉
    await pBtn.click({ timeout: 5000 });
    await page.waitForTimeout(800);
    const sw2 = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
    const ariaNow = (await sw2.getAttribute('aria-checked').catch(() => null));
    if (ariaNow === 'true') {
      await sw2.click({ timeout: 5000 });
      await page.waitForTimeout(1000);
    }
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(600);
    await page.locator('main').first().click({ position: { x: 10, y: 10 } }).catch(() => {});
    await page.waitForTimeout(600);
    const bodyOff = ((await page.locator('body').innerText().catch(() => '')) || '');
    s4.trace_icon_n_off = await page.locator('[aria-label*="需求追溯"]').count();
    s4.off_leak = {
      metric_id: /metric_id|M_SVC_SZ_SCALE|M_SVC_ORG_TECH_SCORE|M_SVC_RELATION_DENSITY/.test(bodyOff),
      gap: /GAP-/.test(bodyOff),
      q_ticket: /Q-SVCCHAIN/.test(bodyOff),
      trace_text: /需求追溯/.test(bodyOff),
      review_word: /评审模式/.test(bodyOff),
    };
  } else { s4.error = '未找到 persona-switch'; }
} catch (e) { s4.error = String(e).slice(0, 300); }
dump('scout-b32-s4-review-switch.json', s4);
report.stages.s4_review = { ok: !s4.error, trace_on: s4.trace_icon_n_on, leak_off: s4.off_leak };

// ---------- S5: 配置区选定产业 → gate 提示（同条件拦截） ----------
const s5 = {};
try {
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await closeBasket(page);
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
  await page.waitForTimeout(2500);
  s5.url_after_pick = page.url();
  s5.industry_param = (s5.url_after_pick.match(/industry=([^&]*)/) || [])[1] || null;
  s5.echo = ((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
  const cfgText = ((await page.locator('[data-testid="svc-eco-analysis-config"]').innerText().catch(() => '')) || '');
  s5.gate_inflight_alert = /同条件已有进行中任务/.test(cfgText);
  s5.gate_today_rerun = await page.getByRole('button', { name: '重新分析', exact: true }).count();
  s5.config_snippet = cfgText.replace(/\n/g, ' | ').slice(0, 400);
  // 切到记录再切回，验证配置保留（URL 驱动）
  await page.getByRole('tab', { name: '分析记录', exact: true }).first().click();
  await page.waitForTimeout(1200);
  await page.getByRole('tab', { name: /深圳服务链现状分析/ }).first().click();
  await page.waitForTimeout(1200);
  s5.url_after_tab_round = page.url();
  s5.echo_after_round = ((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
  // 清空（hover 出 clear）
  const selView = page.locator('.industry-catalog-select').first();
  await selView.hover();
  await page.waitForTimeout(400);
  const clear = page.locator('.industry-catalog-select .arco-select-view-clear-btn, .industry-catalog-select .arco-icon-hover');
  const clearN = await clear.count();
  s5.clear_btn_n = clearN;
  if (clearN) {
    await clear.first().click({ force: true, timeout: 5000 }).catch(async (e) => {
      s5.clear_click_err = String(e).slice(0, 160);
    });
    await page.waitForTimeout(1000);
    s5.url_after_clear = page.url();
    s5.echo_after_clear = ((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
    s5.placeholder_visible = await page.getByPlaceholder('选择产业集群').count();
  }
} catch (e) { s5.error = String(e).slice(0, 300); }
dump('scout-b32-s5-config-gate.json', s5);
report.stages.s5_config = { ok: !s5.error, industry: s5.industry_param, echo_after_round: s5.echo_after_round, clear: s5.echo_after_clear };

// ---------- S6: 记录页「查看过程」 ----------
const s6 = {};
try {
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  await page.getByRole('tab', { name: '分析记录', exact: true }).first().click();
  await page.waitForTimeout(2000);
  const procBtn = page.getByRole('button', { name: /查看过程/ }).first();
  s6.proc_btn_n = await page.getByRole('button', { name: /查看过程/ }).count();
  if (await procBtn.count()) {
    await procBtn.click({ timeout: 8000 });
    await page.waitForTimeout(3000);
    s6.url = page.url();
    const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    s6.process_shell = /可视化分析过程/.test(body);
    s6.task_id_shown = /任务 ID/.test(body);
    s6.status_tag = /已完成|进行中|排队/.test(body);
    s6.view_result_btn = await page.getByRole('button', { name: '查看结果', exact: true }).count();
    s6.snippet = body.split('\n').map((x) => x.trim()).filter(Boolean).slice(0, 30);
  }
} catch (e) { s6.error = String(e).slice(0, 300); }
dump('scout-b32-s6-process.json', s6);
report.stages.s6_process = { ok: !s6.error, url: s6.url, shell: s6.process_shell };

dump('scout-b32-summary.json', report);
await browser.close();
console.log('probe b32 done', JSON.stringify(report.stages, null, 2));
