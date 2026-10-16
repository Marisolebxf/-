#!/usr/bin/env node
/**
 * 一次性无头二次探针 · svc-rec-attract。产物落同目录；勿当 runner。
 * method-patch §3（async_analysis=true）：登录深链 / 合法条件后「开始分析」enabled /
 * 历史已完成任务（§3.5）/ 空态门控。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const route = '/service/institution-decision?workspace=attract&tab=attract';
const outDir = __dirname;

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
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

async function pickIndustry(page, optionText) {
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(200);
  const input = page.locator('input[placeholder="选择产业集群"]').first();
  if (!(await input.count())) return { ok: false, err: 'no-input' };
  const view = input.locator('xpath=ancestor::*[contains(@class,"arco-select-view")][1]');
  try {
    await (await view.count() ? view : input).click({ timeout: 5000 });
  } catch (e) {
    return { ok: false, err: String(e).slice(0, 120) };
  }
  await page.waitForTimeout(600);
  const popup = page.locator('.arco-trigger-popup:visible').last();
  const opts = popup.locator('.arco-select-option, li');
  const sample = await opts
    .allTextContents()
    .then((a) => a.map((t) => t.trim()).filter(Boolean).slice(0, 20))
    .catch(() => []);
  const hit = opts.filter({ hasText: optionText });
  if (!(await hit.count())) {
    await page.keyboard.press('Escape').catch(() => {});
    return { ok: false, sample, err: 'option-miss' };
  }
  await hit.first().click({ force: true }).catch(() => {});
  await page.waitForTimeout(700);
  await page.keyboard.press('Escape').catch(() => {});
  return { ok: true, sample, count: sample.length };
}

async function mainText(page) {
  return (
    (await page
      .locator('main.content-shell-layout, main, [data-testid]')
      .first()
      .innerText()
      .catch(() => '')) || ''
  );
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const shots = {};

const gates = {
  login: { pass: false },
  deep_link: { pass: false, url: '' },
  start_disabled_default: { pass: false, disabled: null },
  select_objects: {
    pass: false,
    industry: '',
    option_count: 0,
    note: '合法对象=选定产业集群（门控必填）',
  },
  start_analysis_enabled: { pass: false, enabled: false, button_name: '开始分析' },
  precheck: {
    pass: true,
    fail_text_seen: false,
    note: '非评估类页；未见「预检未返回」类阻塞（§3.3 N/A=pass）',
  },
  input_object_invalid: {
    pass: true,
    seen: false,
    note: '非诊断/图谱类；INPUT_OBJECT_INVALID 不适用（§3.4 N/A=pass）',
  },
  historical_results: {
    pass: false,
    has_tab: false,
    completed_count: 0,
    view_result_buttons: false,
    sample_ids: [],
    body_hit: '',
  },
  model_zone: {
    pass: false,
    heading: '',
    weights: [],
    restore_btn: false,
  },
  review_leak: {
    pass: false,
    trace_buttons: 0,
    metric_badge: false,
    note: '',
  },
};

try {
  await page.goto(new URL('login', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await ensureLogin(page);
  gates.login.pass = !page.url().includes('/login');

  const target = new URL(route.replace(/^\//, ''), baseUrl).toString();
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  if (page.url().includes('/login')) {
    await ensureLogin(page);
    await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  }
  await page.waitForTimeout(2500);
  await closeBasket(page);

  gates.deep_link.url = page.url();
  gates.deep_link.pass =
    /\/service\/institution-decision/.test(page.url()) &&
    /workspace=attract/.test(page.url()) &&
    /tab=attract/.test(page.url()) &&
    !page.url().includes('/login');
  gates.deep_link.title = await page.title();
  gates.deep_link.tab_active = await page
    .getByRole('tab', { name: '引入服务机构推荐分析' })
    .getAttribute('class')
    .then((c) => /active/.test(c || ''))
    .catch(() => false);
  shots.deep = 'env-gate-deep.png';
  await page.screenshot({ path: path.join(outDir, shots.deep), fullPage: false });

  const start = page.getByRole('button', { name: '开始分析' }).first();
  gates.start_disabled_default.disabled = await start.isDisabled().catch(() => null);
  gates.start_disabled_default.class = await start.getAttribute('class').catch(() => '');
  gates.start_disabled_default.pass = gates.start_disabled_default.disabled === true;

  // 模型区
  const body0 = await mainText(page);
  gates.model_zone.heading = /招引推荐模型（演示模型口径）/.test(body0)
    ? '招引推荐模型（演示模型口径）'
    : '';
  gates.model_zone.restore_btn = (await page.getByRole('button', { name: '恢复默认权重' }).count()) > 0;
  const spins = page.locator('input[role="spinbutton"]');
  const spinCount = await spins.count();
  for (let i = 0; i < Math.min(spinCount, 4); i++) {
    gates.model_zone.weights.push(await spins.nth(i).inputValue().catch(() => ''));
  }
  gates.model_zone.pass =
    !!gates.model_zone.heading &&
    gates.model_zone.weights.join('/') === '35/30/20/15' &&
    gates.model_zone.restore_btn;

  // 评审层（开启态观测）
  gates.review_leak.trace_buttons = await page.locator('button.trace-info-icon').count();
  gates.review_leak.metric_badge =
    (await page.locator('[aria-label*="招引综合分"]').count()) > 0;
  gates.review_leak.pass = gates.review_leak.trace_buttons >= 4 && gates.review_leak.metric_badge;
  gates.review_leak.note = gates.review_leak.pass
    ? '评审开启态：追溯按钮≥4 + 招引综合分角标可见（零泄漏须关评审另测）'
    : '评审挂点不足或角标缺失';

  // 目标/链位 Tag 采样
  const tags = {
    高校: await page.getByText('高校', { exact: true }).count(),
    科研院所: await page.getByText('科研院所', { exact: true }).count(),
    企业: await page.getByText('企业', { exact: true }).count(),
  };
  gates.select_objects.tags_sample = tags;

  // 选产业集群 → 开始分析应 enabled
  const pick = await pickIndustry(page, '新一代信息技术');
  gates.select_objects.industry_pick = pick;
  if (pick.ok) {
    gates.select_objects.industry = '新一代信息技术';
    gates.select_objects.option_count = pick.count || (pick.sample || []).length;
    gates.select_objects.pass = true;
  } else {
    gates.select_objects.pass = false;
    gates.select_objects.note = `产业集群选择失败: ${pick.err || 'unknown'}`;
  }

  await page.waitForTimeout(600);
  gates.start_analysis_enabled.enabled = !(await start.isDisabled().catch(() => true));
  gates.start_analysis_enabled.pass = gates.start_analysis_enabled.enabled === true;
  gates.start_analysis_enabled.body_hit = (await mainText(page)).slice(0, 400);
  shots.gated = 'env-gate-gated.png';
  await page.screenshot({ path: path.join(outDir, shots.gated), fullPage: false });

  // 预检文案
  const body1 = await mainText(page);
  gates.precheck.fail_text_seen = /预检未返回|预检失败/.test(body1);
  if (gates.precheck.fail_text_seen) gates.precheck.pass = false;

  // 分析记录 Tab · §3.5
  const recordsTab = page.getByRole('tab', { name: '分析记录' }).first();
  gates.historical_results.has_tab = (await recordsTab.count()) > 0;
  if (gates.historical_results.has_tab) {
    await recordsTab.click().catch(() => {});
    await page.waitForTimeout(1500);
    const recBody = await mainText(page);
    gates.historical_results.body_hit = recBody.slice(0, 600);
    const viewBtns = page.getByRole('button', { name: /查看结果|查看过程|继续查看|恢复结果/ });
    gates.historical_results.view_result_buttons = (await viewBtns.count()) > 0;
    // 抓已完成样例 ID
    const idHits = [...recBody.matchAll(/SVC-[A-Z0-9-]+|REC-[A-Z0-9-]+|ATTRACT-[A-Z0-9-]+/gi)].map(
      (m) => m[0],
    );
    gates.historical_results.sample_ids = [...new Set(idHits)].slice(0, 5);
    const completedLines = (recBody.match(/已完成/g) || []).length;
    gates.historical_results.completed_count = completedLines;
    gates.historical_results.empty = /暂无|没有分析记录|暂无数据/.test(recBody) && completedLines === 0;
    gates.historical_results.pass =
      completedLines > 0 && gates.historical_results.view_result_buttons;
    shots.history = 'env-gate-history.png';
    await page.screenshot({ path: path.join(outDir, shots.history), fullPage: false });
  } else {
    gates.historical_results.note = '无「分析记录」Tab';
  }

  shots.final = 'env-gate.png';
  await page.screenshot({ path: path.join(outDir, shots.final), fullPage: false });
} catch (e) {
  gates.fatal = String(e.message || e).slice(0, 300);
} finally {
  await browser.close();
}

const corePass =
  gates.login.pass &&
  gates.deep_link.pass &&
  gates.start_disabled_default.pass &&
  gates.select_objects.pass &&
  gates.start_analysis_enabled.pass &&
  gates.precheck.pass &&
  gates.input_object_invalid.pass;

// §3.5 历史已完成：不过则 overall 仍可 pass（配置/门控金样），但结果态禁入 A → ticket
const overall = corePass ? 'pass' : 'fail';

const tickets = [];
if (!gates.historical_results.pass) {
  tickets.push('ENV-SVCATTR-HISTORY-NO-COMPLETED-001');
}
if (!gates.start_disabled_default.pass && gates.start_analysis_enabled.pass) {
  tickets.push('ASBUILT-SVCATTR-EMPTY-START-NOT-DISABLED-001');
}
if (gates.select_objects.option_count > 0 && gates.select_objects.option_count !== 15) {
  tickets.push('ASBUILT-SVCATTR-CLUSTER-OPTION-COUNT-D1');
}

fs.writeFileSync(path.join(outDir, 'scout-gate-raw.json'), JSON.stringify(gates, null, 2) + '\n');
fs.writeFileSync(
  path.join(outDir, 'scout-probe-summary.json'),
  JSON.stringify(
    {
      overall,
      corePass,
      history_ok: gates.historical_results.pass,
      tickets,
      shots: Object.values(shots),
    },
    null,
    2,
  ) + '\n',
);
console.log(
  JSON.stringify(
    {
      overall,
      corePass,
      start_disabled: gates.start_disabled_default,
      select: {
        pass: gates.select_objects.pass,
        industry: gates.select_objects.industry,
        option_count: gates.select_objects.option_count,
      },
      start_enabled: gates.start_analysis_enabled.enabled,
      history: {
        pass: gates.historical_results.pass,
        completed: gates.historical_results.completed_count,
        samples: gates.historical_results.sample_ids,
      },
      model: gates.model_zone,
      tickets,
    },
    null,
    2,
  ),
);
