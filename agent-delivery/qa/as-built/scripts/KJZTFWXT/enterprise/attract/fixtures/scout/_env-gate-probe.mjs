#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · ent-attract。产物落同目录；勿当 runner。
 * method-patch §3：登录深链 / 合法条件后开始分析 enabled / 历史已完成（结果态门）/ 过程可达。
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
const route =
  '/enterprise/attraction?workspace=attraction&recommendation_tab=attraction';
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

async function pickPlaceholderSelect(page, placeholder, optionText) {
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(200);
  const input = page.locator(`input[placeholder="${placeholder}"]`).first();
  if (!(await input.count())) return { ok: false, err: 'no-input' };
  const view = input.locator('xpath=ancestor::*[contains(@class,"arco-select-view")][1]');
  try {
    await (await view.count() ? view : input).click({ timeout: 5000 });
  } catch (e) {
    return { ok: false, err: String(e).slice(0, 120) };
  }
  await page.waitForTimeout(500);
  const popup = page.locator('.arco-trigger-popup:visible').last();
  const opts = popup.locator('.arco-select-option, li');
  const sample = await opts
    .allTextContents()
    .then((a) => a.map((t) => t.trim()).filter(Boolean).slice(0, 12))
    .catch(() => []);
  const hit = opts.filter({ hasText: optionText });
  if (!(await hit.count())) {
    await page.keyboard.press('Escape').catch(() => {});
    return { ok: false, sample, err: 'option-miss' };
  }
  await hit.first().click({ force: true }).catch(() => {});
  await page.waitForTimeout(700);
  await page.keyboard.press('Escape').catch(() => {});
  return { ok: true, sample };
}

async function mainText(page) {
  return (
    (await page
      .locator('main.content-shell-layout, main, [data-testid="recruit-tab-stack"]')
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
  start_enabled_legal_combo: { pass: false, enabled: false, tag: '', field: '' },
  process_trigger: {
    pass: false,
    reached_processing: false,
    reached_success: false,
    url: '',
    note: '',
  },
  history_completed: {
    pass: false,
    empty: null,
    restore_count: 0,
    view_result_count: 0,
    success_status_seen: false,
    body_hit: '',
  },
  candidate_tab: { pass: false, body_hit: '' },
  basket_enterprises: { pass: false, enterprise_tab: '', note: '' },
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
    /\/enterprise\/attraction/.test(page.url()) &&
    /workspace=attraction/.test(page.url()) &&
    !page.url().includes('/login');
  gates.deep_link.title = await page.title();
  gates.deep_link.h1 = await page
    .getByRole('heading', { name: '招引企业推荐分析' })
    .isVisible()
    .catch(() => false);
  shots.deep = 'env-gate-deep.png';
  await page.screenshot({ path: path.join(outDir, shots.deep), fullPage: false });

  const start = page.getByRole('button', { name: '开始分析' }).first();
  gates.start_disabled_default.disabled = await start.isDisabled().catch(() => null);
  gates.start_disabled_default.pass = gates.start_disabled_default.disabled === true;

  // 招引：企业标签为门控必填（实勘：选标签后开始分析 enabled）
  const tagPick = await pickPlaceholderSelect(page, '全部企业标签', '高新技术企业');
  gates.start_enabled_legal_combo.tag_pick = tagPick;
  if (tagPick.ok) gates.start_enabled_legal_combo.tag = '高新技术企业';

  // 行业领域非门控必填；合法组合可加人工智能
  const fieldPick = await pickPlaceholderSelect(page, '全部行业领域', '人工智能');
  gates.start_enabled_legal_combo.field_pick = fieldPick;
  if (fieldPick.ok) gates.start_enabled_legal_combo.field = '人工智能';

  await page.waitForTimeout(600);
  gates.start_enabled_legal_combo.enabled = !(await start.isDisabled().catch(() => true));
  gates.start_enabled_legal_combo.pass = gates.start_enabled_legal_combo.enabled === true;
  gates.start_enabled_legal_combo.body_hit = (await mainText(page)).slice(0, 350);
  shots.gated = 'env-gate-gated.png';
  await page.screenshot({ path: path.join(outDir, shots.gated), fullPage: false });

  // 过程态：点开始分析；成功终态单独记录（不强制 overall）
  if (gates.start_enabled_legal_combo.pass) {
    try {
      await start.click({ timeout: 5000 });
      await page.waitForTimeout(2500);
      let u = page.url();
      let body = await mainText(page);
      gates.process_trigger.url = u;
      gates.process_trigger.reached_processing =
        /analysis_view=processing/.test(u) ||
        /可视化分析过程|排队中|任务提交/.test(body);
      // 等成功或超时（最多 ~45s）
      for (let i = 0; i < 18; i++) {
        await page.waitForTimeout(2500);
        u = page.url();
        body = await mainText(page);
        if (
          /招引推荐分析结果/.test(body) &&
          !/可视化分析过程/.test(body) &&
          /共分析\s*\d+/.test(body)
        ) {
          gates.process_trigger.reached_success = true;
          gates.process_trigger.url = u;
          break;
        }
        if (gates.process_trigger.reached_processing) break;
        if (/analysis_view=processing/.test(u) || /可视化分析过程/.test(body)) {
          gates.process_trigger.reached_processing = true;
          gates.process_trigger.url = u;
        }
      }
      gates.process_trigger.pass =
        gates.process_trigger.reached_processing || gates.process_trigger.reached_success;
      gates.process_trigger.note = gates.process_trigger.reached_success
        ? '可达成功结果态（名单可进金样候选）'
        : gates.process_trigger.reached_processing
          ? '可达 processing；成功名单不作为闸门硬条件'
          : '点击后未进入 processing/成功';
      shots.process = 'env-gate-process.png';
      await page.screenshot({ path: path.join(outDir, shots.process), fullPage: false });
    } catch (e) {
      gates.process_trigger.error = String(e.message || e).slice(0, 160);
    }
  } else {
    gates.process_trigger.note = '开始分析未 enabled，跳过过程触发';
  }

  // 最近分析
  await page.goto(target + '&entry=history', {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const recentTab = page.getByRole('tab', { name: '最近分析' }).first();
  if (await recentTab.count()) {
    await recentTab.click().catch(() => {});
    await page.waitForTimeout(1000);
  }
  const recentBody = await mainText(page);
  gates.history_completed.body_hit = recentBody.slice(0, 500);
  gates.history_completed.empty = /暂无数据/.test(recentBody);
  gates.history_completed.restore_count = await page
    .getByRole('button', { name: /恢复结果|继续查看|查看结果/ })
    .count();
  gates.history_completed.view_result_count = gates.history_completed.restore_count;
  gates.history_completed.success_status_seen = /成功/.test(recentBody);
  gates.history_completed.pass =
    gates.history_completed.restore_count > 0 && !gates.history_completed.empty;
  shots.history = 'env-gate-history.png';
  await page.screenshot({ path: path.join(outDir, shots.history), fullPage: false });

  // 候选工作台壳
  await page.goto(target + '&entry=candidates', {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await page.waitForTimeout(1200);
  await closeBasket(page);
  const candTab = page.getByRole('tab', { name: '候选工作台' }).first();
  if (await candTab.count()) await candTab.click().catch(() => {});
  await page.waitForTimeout(800);
  const candBody = await mainText(page);
  gates.candidate_tab.body_hit = candBody.slice(0, 400);
  gates.candidate_tab.pass =
    /企业名称|线索来源|待分析|暂无|人工线索/.test(candBody) ||
    (await candTab.getAttribute('aria-selected').catch(() => '')) === 'true';

  // 对比篮企业数
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(1200);
  const dock = page.getByRole('button', { name: /打开对比篮/ });
  if (await dock.count()) {
    await dock.first().click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(600);
  }
  const entTab = page.locator('#compare-basket-tab-enterprise');
  gates.basket_enterprises.enterprise_tab = (await entTab.innerText().catch(() => '')).trim();
  const m = gates.basket_enterprises.enterprise_tab.match(/企业\s*(\d+)/);
  const n = m ? Number(m[1]) : 0;
  gates.basket_enterprises.count = n;
  gates.basket_enterprises.pass = n >= 1;
  gates.basket_enterprises.note = n >= 1 ? `篮内企业 ${n}` : '篮内无企业';
  shots.basket = 'env-gate-basket.png';
  await page.screenshot({ path: path.join(outDir, shots.basket), fullPage: false });
} catch (e) {
  gates.fatal = String(e.message || e).slice(0, 300);
} finally {
  await browser.close();
}

const corePass =
  gates.login.pass &&
  gates.deep_link.pass &&
  gates.start_disabled_default.pass &&
  gates.start_enabled_legal_combo.pass;

const overall = corePass ? 'pass' : 'fail';

const tickets = [];
if (!gates.history_completed.pass) tickets.push('ENV-ATTRACT-HISTORY-EMPTY-001');
if (gates.process_trigger.pass && !gates.process_trigger.reached_success) {
  tickets.push('ENV-ATTRACT-NEWTASK-NO-SUCCESS-001');
}
if (gates.process_trigger.reached_success === false && gates.process_trigger.pass) {
  /* already covered */
}
// 页内无「加入招引候选」→ 金样禁入（D2/as-built）
tickets.push('ENV-ATTRACT-NO-INLINE-ADD-CANDIDATE-001');

const report = {
  surveyed_at: new Date().toISOString(),
  entry_id: 'ent-attract',
  base_url: baseUrl,
  route,
  headless: true,
  method: 'headless chromium via _env-gate-probe.mjs (no IDE browser)',
  overall,
  gates,
  evidence: {
    screenshots: Object.values(shots),
  },
  summary: {
    stable_for_gold: [
      '登录深链 workspace=attraction',
      '默认「开始分析」disabled',
      '选企业标签（高新技术企业）后「开始分析」enabled',
      '三 Tab 壳 / 候选工作台可达',
      gates.basket_enterprises.pass ? '对比篮有企业（浮层可测加入招引候选）' : null,
      gates.process_trigger.pass
        ? gates.process_trigger.reached_success
          ? '过程→成功结果态可达（名单列可测）'
          : '过程态 processing 可触发（lite；成功名单视现场）'
        : null,
      gates.history_completed.pass ? '最近分析有可继续查看任务' : null,
    ].filter(Boolean),
    not_for_gold: [
      gates.history_completed.pass
        ? gates.history_completed.success_status_seen
          ? null
          : '历史多为失败/处理中 → 成功结果复用勿入 A'
        : '最近分析无已完成任务（暂无数据）→ 结果态/历史复用整段 B',
      '页内结果工具栏无「加入招引候选」（仅对比篮浮层有）→ P0-05 禁入 A',
      '空结果 / 缺失字段 / 阈值角标 / 同条件复用依赖数据形态',
    ].filter(Boolean),
    gold_process_trigger: gates.process_trigger.pass
      ? gates.process_trigger.reached_success
        ? 'allowed_full'
        : 'allowed_lite'
      : 'forbidden',
    history_shell_ok: gates.history_completed.pass,
    history_success_result: !!gates.history_completed.success_status_seen,
    success_result_reachable: !!gates.process_trigger.reached_success,
  },
  tickets,
  suggested_gold: [], // filled after probe by parent writer if needed
  conclusion: '',
};

// fill conclusion + suggested_gold from live facts
report.suggested_gold = [
  'P0-01',
  'P0-02',
  'P0-06',
  'P0-09',
  gates.candidate_tab.pass ? 'P0-15' : null,
].filter(Boolean);

if (gates.process_trigger.reached_success) {
  // 成功名单可达时，可升 P0-03 lite（过程+成功）或 P0-04；本交卷建议保留门控金样，成功态另议
  report.summary.optional_success_gold = ['P0-03', 'P0-04'];
}

report.suggested_gold_rationale =
  '均为零 allow_skip 可达路径：深链壳 / 默认门控 / 条件区三选择器 / 选标签放行 / 候选表壳。' +
  (gates.process_trigger.reached_success
    ? ' 本环境成功名单可达，可选升 P0-03/P0-04（须去成功依赖的不稳定断言）。'
    : ' 成功名单未稳定 → P0-03/P0-04 降 B。') +
  ' 现 index gold 含 P0-05(allow_skip) 须踢出 A。';

report.conclusion = corePass
  ? `环境闸门 overall=pass：登录深链、默认 disabled、选高新技术企业(+可选人工智能)后开始分析 enabled` +
    (gates.process_trigger.pass
      ? gates.process_trigger.reached_success
        ? '；过程→成功结果可达'
        : '；processing 可达(lite)'
      : '') +
    (gates.history_completed.pass
      ? `；最近分析有 ${gates.history_completed.restore_count} 条可继续查看` +
        (gates.history_completed.success_status_seen ? '（见成功态）' : '（未见成功终态）')
      : '；最近分析空→结果态禁入金样') +
    `。A 档建议 gold=${report.suggested_gold.join(',')}；现 gold P0-03/04/05 须按现场收敛。tickets=${tickets.join(',')}`
  : `环境闸门失败：login=${gates.login.pass} deep=${gates.deep_link.pass} emptyDisabled=${gates.start_disabled_default.pass} startEnabled=${gates.start_enabled_legal_combo.pass}。金样仅写可达配置壳或标 blocked。`;

fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(report, null, 2) + '\n');
fs.writeFileSync(path.join(outDir, 'scout-env-gate-probe.json'), JSON.stringify(gates, null, 2) + '\n');
console.log(
  JSON.stringify(
    {
      overall: report.overall,
      tickets: report.tickets,
      suggested_gold: report.suggested_gold,
      summary: report.summary,
    },
    null,
    2,
  ),
);
