#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-sz P0-07（FUNC-01287 显式触发开始分析）现场核实。
 * 产物落同目录 scout-p007-*.json；勿当 runner。遵守探针公约（无 IDE/有头浏览器）。
 * 核实点：
 *  S7 fresh 起任务链路：选定「新能源」→ 点「开始分析」→ URL/网络/DOM 时间线 → 完成 → 分析记录 diff
 *      （用「新能源」而非「新一代信息技术」：把主路径首选集群留给 runner 正跑，避免同日复用污染）
 *  S8 同日同条件二次发起行为（当天复用 / 拦截 / 再起任务）——用「新能源」复测
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

async function mainText(page, n = 60) {
  return page
    .locator('main')
    .first()
    .innerText()
    .then((t) => t.split('\n').map((s) => s.trim()).filter(Boolean).slice(0, n))
    .catch(() => []);
}

async function recordsSnapshot(page) {
  await page.getByRole('tab', { name: '分析记录', exact: true }).first().click();
  await page.waitForTimeout(2000);
  const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  const ids = [...new Set([...body.matchAll(/SVC-\d{8}-\d+/g)].map((m) => m[0]))];
  return { ids, count: ids.length, snippet: body.split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 40) };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const report = { probed_at: new Date().toISOString(), stages: {} };

// 网络监听：任务相关 API（创建/查询）
const netLog = [];
page.on('response', (r) => {
  const u = r.url();
  if (/task|analysis|svc|chain/i.test(u) && /api|internal|service/i.test(u)) {
    netLog.push({ t: new Date().toISOString().slice(11, 23), method: r.request().method(), status: r.status(), url: u.slice(0, 200) });
  }
});
page.on('requestfailed', (r) => {
  const u = r.url();
  if (/task|analysis|svc|chain/i.test(u)) netLog.push({ t: new Date().toISOString().slice(11, 23), method: r.method(), status: 'FAILED', url: u.slice(0, 200) });
});

// ---------- 登录 + 深链 ----------
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
if (page.url().includes('/login')) { await ensureLogin(page); await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded' }); }
await page.waitForTimeout(2500);
await closeBasket(page);

// ---------- 记录快照 A（发起前） ----------
const before = await recordsSnapshot(page);
dump('scout-p007-s7-records-before.json', before);

// ---------- S7: 配置 → 选「新能源」→ 点「开始分析」 ----------
const s7 = { steps: [] };
try {
  const main = page.locator('[role=tab][data-tab-key="shenzhen"]').or(page.getByRole('tab', { name: /深圳服务链现状分析/ }));
  await main.first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  await closeBasket(page);
  // 选「新能源」（P7：点可见容器；选项挂 .arco-trigger-popup:visible）
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新能源' }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  s7.url_after_pick = page.url();
  s7.echo = ((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
  // 开始分析按钮（exact 避开粘性提示文案里的「开始分析」）
  const startBtn = page.getByRole('button', { name: '开始分析', exact: true });
  s7.start_btn_n = await startBtn.count();
  s7.start_enabled = s7.start_btn_n ? await startBtn.first().isEnabled() : false;
  const cfgText = ((await page.locator('[data-testid="svc-eco-analysis-config"]').innerText().catch(() => '')) || '');
  s7.config_snippet = cfgText.replace(/\n/g, ' | ').slice(0, 400);
  // 点击开始分析（enabled 才点；公约禁硬点 disabled）
  if (s7.start_btn_n && s7.start_enabled) {
    await startBtn.first().click({ timeout: 8000 });
    // 时间线轮询：URL / 过程壳 / 完成标记，最多 45s
    const t0 = Date.now();
    let sawProcessing = false, sawDone = false;
    while (Date.now() - t0 < 45000) {
      await page.waitForTimeout(1000);
      const url = page.url();
      const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
      const generating = /生成中|可视化分析过程/.test(body);
      const done = /分析结果已生成/.test(body);
      const viewResultBtn = await page.getByRole('button', { name: '查看结果', exact: true }).count();
      if (!sawProcessing && (/[?&]view=processing/.test(url) || generating)) {
        sawProcessing = true;
        s7.steps.push({ t: Date.now() - t0, phase: 'processing', url, generating, done, viewResultBtn });
        await page.screenshot({ path: path.join(outDir, 'scout-p007-s7-processing.png'), fullPage: false });
      }
      if (!sawDone && done) {
        sawDone = true;
        s7.steps.push({ t: Date.now() - t0, phase: 'done', url, viewResultBtn });
        await page.screenshot({ path: path.join(outDir, 'scout-p007-s7-done.png'), fullPage: false });
      }
      if (sawProcessing && sawDone) break;
    }
    s7.final_url = page.url();
    s7.saw_processing = sawProcessing;
    s7.saw_done_marker = sawDone;
    s7.task_id = (s7.final_url.match(/task_id=(SVC-[\d-]+)/) || [])[1] || null;
    s7.view = (s7.final_url.match(/[?&]view=(\w+)/) || [])[1] || null;
    s7.final_text = await mainText(page, 30);
    s7.framework_count = await page.locator('[data-testid="svc-eco-sz-framework"]').count();
    s7.compare_grid_count = await page.locator('[data-testid="svc-eco-sz-compare-grid"]').count();
  } else {
    s7.error = '开始分析按钮不可用或不存在';
  }
} catch (e) { s7.error = String(e).slice(0, 400); }
dump('scout-p007-s7-start-chain.json', s7);
report.stages.s7_start_chain = { ok: !s7.error, saw_processing: s7.saw_processing, saw_done: s7.saw_done_marker, task_id: s7.task_id, view: s7.view };

// ---------- 记录快照 B（发起后） ----------
await page.waitForTimeout(1500);
const after = await recordsSnapshot(page);
dump('scout-p007-s7-records-after.json', after);
report.stages.records_diff = { before: before.count, after: after.count, new: after.ids.filter((x) => !before.ids.includes(x)) };

// ---------- S8: 同日同条件二次发起（当天复用 / 拦截 / 再起任务） ----------
const s8 = {};
try {
  const main2 = page.locator('[role=tab][data-tab-key="shenzhen"]').or(page.getByRole('tab', { name: /深圳服务链现状分析/ }));
  await main2.first().click({ timeout: 8000 });
  await page.waitForTimeout(2000);
  await closeBasket(page);
  const sel2 = page.locator('.industry-catalog-select').first();
  const echo0 = ((await sel2.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
  s8.echo_on_return = echo0;
  const cfgText2 = ((await page.locator('[data-testid="svc-eco-analysis-config"]').innerText().catch(() => '')) || '');
  s8.config_snippet = cfgText2.replace(/\n/g, ' | ').slice(0, 500);
  s8.rerun_btn_n = await page.getByRole('button', { name: '重新分析', exact: true }).count();
  s8.gate_inflight_alert = /同条件已有进行中任务/.test(cfgText2);
  s8.gate_today_hint = /今天|当天|已成功/.test(cfgText2);
  const startBtn2 = page.getByRole('button', { name: '开始分析', exact: true });
  s8.start_btn_n = await startBtn2.count();
  if (s8.start_btn_n) {
    s8.start_enabled = await startBtn2.first().isEnabled();
    if (s8.start_enabled) {
      await startBtn2.first().click({ timeout: 8000 });
      const t0 = Date.now();
      const timeline = [];
      while (Date.now() - t0 < 15000) {
        await page.waitForTimeout(1000);
        const url = page.url();
        const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
        timeline.push({
          t: Date.now() - t0,
          url: url.slice(0, 160),
          view: (url.match(/[?&]view=(\w+)/) || [])[1] || null,
          task_id: (url.match(/task_id=(SVC-[\d-]+)/) || [])[1] || null,
          generating: /生成中|可视化分析过程/.test(body),
          done: /分析结果已生成/.test(body),
          framework: await page.locator('[data-testid="svc-eco-sz-framework"]').count(),
        });
        if (timeline.length >= 6) break;
      }
      s8.timeline = timeline;
      await page.screenshot({ path: path.join(outDir, 'scout-p007-s8-second-start.png'), fullPage: false });
      s8.snippet = await mainText(page, 30);
    }
  }
} catch (e) { s8.error = String(e).slice(0, 400); }
dump('scout-p007-s8-second-start.json', s8);
report.stages.s8_second_start = { ok: !s8.error, rerun_btn: s8.rerun_btn_n, gate_inflight: s8.gate_inflight_alert, final_view: s8.timeline?.at(-1)?.view };

dump('scout-p007-net.json', netLog.slice(0, 80));
dump('scout-p007-summary.json', report);
await browser.close();
console.log('probe p007 done', JSON.stringify(report.stages, null, 2));
