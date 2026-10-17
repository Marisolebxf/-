#!/usr/bin/env node
/**
 * svc-chain-graph 环境闸门二次探针（无头）。产物落同目录；勿当 runner。
 * method-patch §3：登录深链 / 合法条件后开始分析 enabled / 预检 N/A /
 * 生物黑名单试探 / 历史已完成+查看结果。
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
const route = '/service/chain-analysis?workspace=graph&tab=graph';
const target = `${baseUrl.replace(/\/?$/, '')}${route}`;
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
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
  await page.keyboard.press('Escape').catch(() => {});
}

async function shot(page, name) {
  const p = path.join(outDir, name);
  await page.screenshot({ path: p, fullPage: false });
  return name;
}

async function mainSnippet(page, n = 50) {
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

async function startBtnState(page) {
  const btn = page.getByRole('button', { name: '开始分析' }).first();
  const present = (await btn.count()) > 0;
  if (!present) return { present: false, enabled: false, disabled: true, class: '' };
  const disabled = await btn.isDisabled().catch(() => null);
  const cls = (await btn.getAttribute('class').catch(() => '')) || '';
  const softDisabled = /arco-btn-disabled|disabled/.test(cls);
  return {
    present: true,
    enabled: disabled === false && !softDisabled,
    disabled: disabled === true || softDisabled,
    class: cls,
    disabled_attr: disabled,
  };
}

async function openIndustrySelect(page) {
  const view = page.locator('main .industry-catalog-select.arco-select-view, main .industry-catalog-select').first();
  await view.click({ timeout: 8000 });
  await page.waitForTimeout(600);
}

async function industryOptions(page) {
  return (
    await page.locator('.arco-trigger-popup:visible .arco-select-option').allTextContents()
  )
    .map((t) => t.trim())
    .filter(Boolean);
}

async function pickIndustry(page, name) {
  await openIndustrySelect(page);
  const opts = await industryOptions(page);
  const hit = opts.find((t) => t.includes(name)) || opts[0];
  if (hit) {
    await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: hit }).first().click();
  }
  await page.waitForTimeout(400);
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(200);
  return { opts, picked: hit || '' };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const raw = { probed_at: new Date().toISOString(), route, gates: {} };

// —— G1 登录 + 深链 ——
await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(2500);
await closeBasket(page);

const urlOk =
  page.url().includes('workspace=graph') &&
  page.url().includes('tab=graph') &&
  !page.url().includes('/login');
const title = await page.title();
const tabs = await page.evaluate(() =>
  [...document.querySelectorAll('[role=tab]')]
    .filter((t) => !String(t.id || '').startsWith('compare-basket'))
    .map((t) => ({
      text: (t.innerText || '').trim().replace(/\s+/g, ' '),
      selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
    })),
);
const panelText = await page
  .locator('main .svc-eco-panel')
  .innerText()
  .then((t) => t.replace(/\s+/g, ' ').slice(0, 500))
  .catch(() => '');
raw.gates.g1_login_deep = {
  pass: urlOk && /服务链图谱分析/.test(title),
  detail: { url: page.url(), title, tabs, panel_hint: panelText },
  shot: await shot(page, 'env-gate-deep.png'),
};

// —— G2 空态门控 + 合法条件后开始分析 ——
const emptyStart = await startBtnState(page);
const emptyHint =
  /请先确认分析条件|请先选择|选择产业集群/.test(panelText) ||
  (await page
    .locator('main')
    .innerText()
    .then((t) => /请先确认分析条件|请先选择/.test(t))
    .catch(() => false));
raw.gates.g2a_empty_start = {
  pass: emptyStart.disabled === true || emptyHint === true,
  detail: {
    start: emptyStart,
    soft_gate_hint: emptyHint,
    note: emptyStart.disabled
      ? '空态开始分析 disabled'
      : '空态开始分析非 disabled，靠文案门控（as-built soft gate）',
    snippet: await mainSnippet(page, 25),
  },
  shot: await shot(page, 'env-gate-empty.png'),
};

// 产业下拉 15 + 选合法组合
await openIndustrySelect(page);
const opts = await industryOptions(page);
dump('scout-industry-options.json', { count: opts.length, options: opts });
const legalName = opts.find((t) => t.includes('新一代信息技术')) || opts[0];
if (legalName) {
  await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: legalName }).first().click();
}
await page.waitForTimeout(500);
await page.keyboard.press('Escape').catch(() => {});

// 分析模式：确保点选「① 仅机构」
const modeOnly = page.getByText('① 仅机构', { exact: false }).first();
if (await modeOnly.count()) {
  await modeOnly.click().catch(() => {});
  await page.waitForTimeout(300);
}
const afterLegalStart = await startBtnState(page);
const modeTexts = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  return [...main.querySelectorAll('.arco-radio, [role=radio], label')]
    .map((el) => (el.innerText || '').trim().replace(/\s+/g, ' '))
    .filter((t) => /仅机构|关联主体/.test(t))
    .slice(0, 8);
});
raw.gates.g2_start_enabled_legal = {
  pass: afterLegalStart.enabled === true || afterLegalStart.disabled === false,
  detail: {
    industry_count: opts.length,
    industry_options: opts,
    selected: legalName || '',
    modes: modeTexts,
    start_after_legal: afterLegalStart,
    note: '合法=选产业集群（新一代信息技术优先）+ 分析模式已呈现；选齐后「开始分析」应可点',
  },
  shot: await shot(page, 'env-gate-config.png'),
};

// —— G3 预检 N/A ——
raw.gates.g3_precheck_eval = {
  pass: true,
  n_a: true,
  detail: { note: '服务链图谱分析非企业评估页，无「预检未返回企业明细」门控；本闸 N/A=pass' },
};

// —— G4 生物黑名单试探（图谱类）——
const bioPick = await pickIndustry(page, '生物');
const afterBioStart = await startBtnState(page);
const bioBody = await page
  .locator('main')
  .innerText()
  .then((t) => t.replace(/\s+/g, ' ').slice(0, 400))
  .catch(() => '');
const bioInvalid = /INPUT_OBJECT_INVALID|无效|不可用|无法分析|暂无/.test(bioBody);
raw.gates.g4_bio_blacklist = {
  pass: true, // 记黑名单；不因可选中而 fail
  detail: {
    bio_selected: !!bioPick.picked,
    picked: bioPick.picked,
    start_after_bio: afterBioStart,
    body_hit: bioBody,
    invalid_hint: bioInvalid,
    blacklist: ['生物产业', '生物'],
    note: '图谱/诊断类：生物组合列入黑名单，禁止依赖其开始分析成功结果（INPUT_OBJECT_INVALID 风险）；金样用新一代信息技术',
  },
  shot: await shot(page, 'env-gate-bio.png'),
};

// 切回合法产业，便于后续记录探查
await pickIndustry(page, '新一代信息技术');

// —— G5 分析记录：已完成 + 查看结果 ——
const recordsTab = page.getByRole('tab', { name: '分析记录' }).first();
await recordsTab.click({ timeout: 8000 });
await page.waitForTimeout(2000);
await closeBasket(page);
const recordsShot = await shot(page, 'env-gate-records.png');
const recordsInfo = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const text = (main.innerText || '').replace(/\s+/g, ' ');
  const rows = [...main.querySelectorAll('tr, .arco-table-tr, [class*=record], [class*=task]')]
    .map((el) => (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 120))
    .filter((t) => t.length > 8)
    .slice(0, 20);
  const viewBtns = [...main.querySelectorAll('button, a, [role=button]')]
    .map((el) => (el.innerText || el.getAttribute('aria-label') || '').trim())
    .filter((t) => /查看结果|查看过程/.test(t));
  const doneHits = (text.match(/已完成/g) || []).length;
  const empty = /暂无|没有.*记录|无分析记录/.test(text) && doneHits === 0;
  return {
    snippet: text.slice(0, 800),
    rows: rows.slice(0, 12),
    view_result_labels: viewBtns.slice(0, 10),
    view_count: viewBtns.filter((t) => /查看结果/.test(t)).length,
    done_count: doneHits,
    empty,
  };
});
dump('scout-records.json', recordsInfo);

let viewResultOk = recordsInfo.view_count > 0 && recordsInfo.done_count > 0;
let viewResultDetail = { from_records: false };
if (viewResultOk) {
  const viewBtn = page.getByRole('button', { name: /查看结果/ }).first();
  if (await viewBtn.count()) {
    const enabled = !(await viewBtn.isDisabled().catch(() => true));
    if (enabled) {
      await viewBtn.click().catch(() => {});
      await page.waitForTimeout(2500);
      await closeBasket(page);
      const resultUrl = page.url();
      const resultSnippet = await mainSnippet(page, 40);
      const resultShot = await shot(page, 'env-gate-result.png');
      dump('scout-view-result.json', { url: resultUrl, snippet: resultSnippet });
      viewResultDetail = {
        from_records: true,
        url: resultUrl,
        snippet: resultSnippet,
        shot: resultShot,
        has_graph_hint: resultSnippet.some((s) => /关系|网络|图谱|节点|图例|密度|中心性/.test(s)),
      };
    } else {
      viewResultOk = false;
      viewResultDetail = { from_records: false, reason: '查看结果 disabled' };
    }
  }
}

raw.gates.g5_completed_task_view_result = {
  pass: viewResultOk,
  detail: {
    ...recordsInfo,
    view_result: viewResultDetail,
    note: viewResultOk
      ? '分析记录有已完成任务且可「查看结果」'
      : '无已完成任务或无可点「查看结果」→ 结果态金样禁写 / B+ticket',
  },
  shot: recordsShot,
};

// 可选：合法条件显式点开始（过程可达探针；失败不卡死）
await page.getByRole('tab', { name: '服务链图谱分析' }).first().click().catch(() => {});
await page.waitForTimeout(1000);
await closeBasket(page);
await pickIndustry(page, '新一代信息技术');
const modeOnly2 = page.getByText('① 仅机构', { exact: false }).first();
if (await modeOnly2.count()) await modeOnly2.click().catch(() => {});
await page.waitForTimeout(300);
const beforeClick = await startBtnState(page);
let afterStart = { attempted: false };
if (beforeClick.enabled) {
  const start = page.getByRole('button', { name: '开始分析' }).first();
  await start.click({ timeout: 5000 }).catch((e) => {
    afterStart = { attempted: true, click_error: String(e).slice(0, 200) };
  });
  if (!afterStart.click_error) {
    await page.waitForTimeout(3000);
    afterStart = {
      attempted: true,
      url: page.url(),
      snippet: await mainSnippet(page, 35),
      shot: await shot(page, 'env-gate-process.png'),
    };
  }
} else {
  afterStart = { attempted: false, reason: 'start disabled', start: beforeClick };
}
dump('scout-after-start.json', afterStart);
raw.gates.g2b_process_reachable = {
  pass: afterStart.attempted === true && !afterStart.click_error,
  detail: afterStart,
};

dump('scout-gate-raw.json', raw);
await browser.close();
console.log('env-gate probe done →', outDir);
console.log(
  JSON.stringify(
    {
      g1: raw.gates.g1_login_deep.pass,
      g2a: raw.gates.g2a_empty_start.pass,
      g2: raw.gates.g2_start_enabled_legal.pass,
      g2b: raw.gates.g2b_process_reachable.pass,
      g3: raw.gates.g3_precheck_eval.pass,
      g4: raw.gates.g4_bio_blacklist.pass,
      g5: raw.gates.g5_completed_task_view_result.pass,
    },
    null,
    2,
  ),
);
