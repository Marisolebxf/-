#!/usr/bin/env node
/**
 * svc-org-trend 环境闸门二次探针（无头）。产物落同目录；勿当 runner。
 * 覆盖：登录深链 / 时间范围控件 / 产业下拉 / 开始分析门控 / 过程·结果可达 / 分析记录。
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
const route = '/service/institution-judgment?workspace=trend&tab=trend';
const target = `${baseUrl.replace(/\/?$/, '')}${route}`;
const outDir = __dirname;

const dump = (name, data) => {
  fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2));
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
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

async function shot(page, name) {
  const p = path.join(outDir, name);
  await page.screenshot({ path: p, fullPage: false });
  return name;
}

async function mainSnippet(page, n = 60) {
  return page
    .locator('main')
    .innerText()
    .then((t) =>
      t
        .split('\n')
        .map((s) => s.trim())
        .filter(Boolean)
        .slice(0, n),
    )
    .catch(() => []);
}

async function detectTimeControls(page) {
  return page.evaluate(() => {
    const main = document.querySelector('main') || document.body;
    const text = (main.innerText || '').replace(/\s+/g, ' ');
    const labels = [];
    const re = /近\s*\d+\s*年|时间窗|时间范围|起止|年份|年区间|统计周期/g;
    let m;
    while ((m = re.exec(text))) labels.push(m[0]);
    const radios = [...main.querySelectorAll('.arco-radio, [role=radio], .arco-radio-button')]
      .map((el) => (el.innerText || el.textContent || '').trim())
      .filter((t) => /年|时间|近/.test(t))
      .slice(0, 12);
    const selects = [...main.querySelectorAll('.arco-select-view, .arco-picker, input[placeholder*="年"], input[placeholder*="时间"]')]
      .map((el) => ({
        ph: el.getAttribute('placeholder') || '',
        text: (el.innerText || '').trim().slice(0, 40),
        cls: (el.className || '').toString().slice(0, 80),
      }))
      .filter((x) => /年|时间|range|picker|date/i.test(`${x.ph}${x.text}${x.cls}`))
      .slice(0, 10);
    return {
      text_hits: [...new Set(labels)].slice(0, 20),
      radio_like: radios,
      select_like: selects,
      has_any: labels.length + radios.length + selects.length > 0,
    };
  });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const gates = {};

// —— G1 登录 + 深链 ——
await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(2000);
await closeBasket(page);

const urlOk =
  page.url().includes('workspace=trend') && page.url().includes('tab=trend') && !page.url().includes('/login');
const title = await page.title();
const tabs = await page.evaluate(() =>
  [...document.querySelectorAll('[role=tab]')]
    .filter((t) => !String(t.id || '').startsWith('compare-basket'))
    .map((t) => ({
      text: (t.innerText || '').trim().replace(/\s+/g, ' '),
      selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
    })),
);
gates.g1_login_deeplink = {
  pass: urlOk && /服务机构新增趋势分析/.test(title),
  detail: { url: page.url(), title, tabs },
  shot: await shot(page, 'env-gate-deep.png'),
};

const startBtn = page.getByRole('button', { name: '开始分析' }).first();
const emptyDisabled = await startBtn.isDisabled().catch(() => null);
const emptyClass = (await startBtn.getAttribute('class').catch(() => '')) || '';
const emptyHint = await page
  .locator('main')
  .innerText()
  .then((t) => /请先选择分析机构|开始分析/.test(t))
  .catch(() => false);
const timeEmpty = await detectTimeControls(page);
gates.g2_empty_start_gate = {
  pass: emptyDisabled === true || /arco-btn-disabled|disabled/.test(emptyClass) || emptyHint,
  detail: {
    start_disabled: emptyDisabled,
    start_class: emptyClass,
    gate_hint_visible: emptyHint,
    snippet: await mainSnippet(page, 30),
  },
  shot: await shot(page, 'env-gate-empty.png'),
};
gates.g3_time_range_config = {
  pass: true, // 配置空态无时间窗 ≠ 闸门失败；记 as-built
  detail: {
    phase: 'config_empty',
    present: timeEmpty.has_any,
    ...timeEmpty,
    note: timeEmpty.has_any
      ? '配置区可见时间相关控件'
      : '配置空态未见时间窗/近N年控件（用例 00666 属结果态；不阻塞配置门控）',
  },
};

// —— G4 产业下拉 ——
await page.locator('main .industry-catalog-select.arco-select-view, main .industry-catalog-select').first().click({
  timeout: 8000,
});
await page.waitForTimeout(600);
const industryOpts = (
  await page.locator('.arco-trigger-popup:visible .arco-select-option').allTextContents()
)
  .map((t) => t.trim())
  .filter(Boolean);
dump('scout-industry-options.json', { count: industryOpts.length, options: industryOpts });
const pickIndustry = industryOpts.find((t) => t.includes('新一代信息技术')) || industryOpts[0];
if (pickIndustry) {
  await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: pickIndustry }).first().click();
}
await page.waitForTimeout(500);
await page.keyboard.press('Escape');
await page.waitForTimeout(300);
const afterIndustryDisabled = await startBtn.isDisabled().catch(() => null);
gates.g4_industry_select = {
  pass: industryOpts.length >= 15,
  detail: {
    count: industryOpts.length,
    options: industryOpts,
    selected: pickIndustry || '',
    start_disabled_after_industry_only: afterIndustryDisabled,
    filter_ph: await page.locator('input[placeholder="筛选领域（不改分析指纹）"]').count(),
  },
  shot: await shot(page, 'env-gate-industry.png'),
};

// —— G5 选择机构 → 合法条件后开始分析 enabled ——
await page.getByRole('button', { name: '选择机构' }).click({ timeout: 8000 });
await page.waitForTimeout(1000);
const modalText = await page.evaluate(() => {
  const m = document.querySelector(
    '.arco-modal:not([style*="display: none"]), .arco-drawer:not([style*="display: none"])',
  );
  return (m?.innerText || '').slice(0, 1000);
});
const cbCount = await page.locator('.arco-modal:visible .arco-checkbox, .arco-drawer:visible .arco-checkbox').count();
let orgPicked = false;
const cb = page.locator('.arco-modal:visible .arco-checkbox, .arco-drawer:visible .arco-checkbox').first();
if (cbCount > 0) {
  await cb.click().catch(() => {});
  await page.waitForTimeout(300);
  const ok = page.locator('.arco-modal:visible, .arco-drawer:visible').getByRole('button', { name: /确定|确认/ }).first();
  if (await ok.count()) {
    await ok.click().catch(() => {});
    orgPicked = true;
  } else {
    const ok2 = page.getByRole('button', { name: /确定|确认/ }).last();
    if (await ok2.count()) {
      await ok2.click().catch(() => {});
      orgPicked = true;
    }
  }
  await page.waitForTimeout(800);
} else {
  await page.keyboard.press('Escape');
}
const startEnabled = !(await startBtn.isDisabled().catch(() => true));
const afterOrgSnippet = await mainSnippet(page, 40);
gates.g5_start_enabled_legal = {
  pass: orgPicked && startEnabled,
  detail: {
    modal_preview: modalText.slice(0, 400),
    checkbox_count: cbCount,
    org_picked: orgPicked,
    start_enabled: startEnabled,
    start_disabled: await startBtn.isDisabled().catch(() => null),
    snippet: afterOrgSnippet,
  },
  shot: await shot(page, 'env-gate-config.png'),
};

// —— G6 显式开始 → 过程/结果 ——
let processSeen = false;
let resultSeen = false;
let resultSnippet = [];
let charts = 0;
let timeAfterResult = { has_any: false };
if (gates.g5_start_enabled_legal.pass) {
  await startBtn.click();
  await page.waitForTimeout(3000);
  const mid = await mainSnippet(page, 80);
  processSeen = mid.some((l) => /可视化分析过程|生成中|分析中|排队|进度/.test(l));
  dump('scout-after-start.json', { url: page.url(), snippet: mid, processSeen });
  await shot(page, 'env-gate-process.png');
  for (let i = 0; i < 25; i++) {
    await page.waitForTimeout(2000);
    const t = await page.locator('main').innerText().catch(() => '');
    const lines = t
      .split('\n')
      .map((s) => s.trim())
      .filter(Boolean);
    if (/可视化分析过程|生成中|分析中/.test(t)) processSeen = true;
    if (
      (/趋势|热度|研判|明细|新增/.test(t) || /canvas|echarts/i.test(t)) &&
      !/可视化分析过程|生成中/.test(t)
    ) {
      resultSeen = true;
      resultSnippet = lines.slice(0, 100);
      charts = await page.locator('main canvas, main .echarts, main [_echarts_instance_]').count();
      timeAfterResult = await detectTimeControls(page);
      dump('scout-result.json', { url: page.url(), snippet: resultSnippet, charts, timeAfterResult });
      await shot(page, 'env-gate-result.png');
      break;
    }
    if (/失败|错误|暂无|数据长度不足/.test(t) && !/可视化分析过程|生成中/.test(t)) {
      resultSeen = true;
      resultSnippet = lines.slice(0, 100);
      dump('scout-result.json', { url: page.url(), snippet: resultSnippet, charts: 0, terminal: 'fail_or_empty' });
      await shot(page, 'env-gate-result.png');
      break;
    }
  }
} else {
  dump('scout-after-start.json', { skipped: true, reason: '开始分析未 enabled' });
}
gates.g6_process_result = {
  pass: processSeen || resultSeen,
  detail: {
    started: gates.g5_start_enabled_legal.pass,
    process_ui_seen: processSeen,
    result_reached: resultSeen,
    charts,
    time_range_on_result: timeAfterResult,
    snippet: resultSnippet.slice(0, 40),
  },
  shot: resultSeen ? 'env-gate-result.png' : processSeen ? 'env-gate-process.png' : 'env-gate-config.png',
};

// —— G7 分析记录：已完成任务 ——
await page.getByRole('tab', { name: '分析记录' }).click();
await page.waitForTimeout(1000);
const recordsText = await page.locator('main').innerText().catch(() => '');
const recordLines = recordsText
  .split('\n')
  .map((s) => s.trim())
  .filter(Boolean)
  .slice(0, 50);
const viewBtns = page.getByRole('button', { name: /查看结果|打开结果|查看/ });
const viewCount = await viewBtns.count();
let enabledView = 0;
for (let i = 0; i < Math.min(viewCount, 8); i++) {
  if (!(await viewBtns.nth(i).isDisabled().catch(() => true))) enabledView += 1;
}
const hasDone =
  /已完成|成功|完成/.test(recordsText) ||
  (enabledView > 0 && !/暂无数据|暂无记录|没有数据/.test(recordsText));
gates.g7_completed_task = {
  pass: hasDone || resultSeen,
  detail: {
    view_count: viewCount,
    enabled_view: enabledView,
    has_done_row: hasDone,
    note: resultSeen
      ? '本会话已跑出结果态，历史列表可弱依赖'
      : hasDone
        ? '分析记录有可查看结果入口'
        : '无已完成任务可供查看结果',
    snippet: recordLines,
  },
  shot: await shot(page, 'env-gate-records.png'),
};

await page.getByRole('tab', { name: '服务机构新增趋势分析' }).click().catch(() => {});

const overallPass =
  gates.g1_login_deeplink.pass &&
  gates.g2_empty_start_gate.pass &&
  gates.g4_industry_select.pass &&
  gates.g5_start_enabled_legal.pass &&
  (gates.g6_process_result.pass || gates.g7_completed_task.pass);

const tickets = [];
if (!gates.g4_industry_select.pass) tickets.push('ENV-SVC-ORG-TREND-INDUSTRY-OPTIONS');
if (!gates.g5_start_enabled_legal.pass) tickets.push('ENV-SVC-ORG-TREND-START-DISABLED');
if (!gates.g6_process_result.pass && !gates.g7_completed_task.pass) {
  tickets.push('ENV-SVC-ORG-TREND-NO-DONE-TASK');
}
if (!timeEmpty.has_any && !(timeAfterResult && timeAfterResult.has_any)) {
  tickets.push('D1-SVC-ORG-TREND-TIME-WINDOW-ASBUILT'); // 非阻塞：as-built 观测
}

dump('scout-deep.json', { gates, overallPass, tickets });
fs.writeFileSync(
  path.join(outDir, 'scout-deep.md'),
  [
    '# svc-org-trend 二次探针（env-gate）',
    '',
    `- g1 login/deeplink: ${gates.g1_login_deeplink.pass}`,
    `- g2 empty start gate: ${gates.g2_empty_start_gate.pass} (disabled=${emptyDisabled})`,
    `- g3 time config: present=${timeEmpty.has_any}`,
    `- g4 industry: ${industryOpts.length} opts, pass=${gates.g4_industry_select.pass}`,
    `- g5 start enabled: ${gates.g5_start_enabled_legal.pass}`,
    `- g6 process/result: process=${processSeen} result=${resultSeen}`,
    `- g7 records done: ${gates.g7_completed_task.pass}`,
    `- overallPass=${overallPass}`,
    '',
  ].join('\n'),
);

await browser.close();
console.log(JSON.stringify({ overallPass, tickets, gates: Object.fromEntries(Object.entries(gates).map(([k, v]) => [k, v.pass])) }, null, 2));
console.log('probe ok →', outDir);
