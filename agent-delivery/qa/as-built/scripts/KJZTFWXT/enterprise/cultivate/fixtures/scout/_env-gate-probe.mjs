#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · ent-cultivate。产物落同目录；勿当 runner。
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
  '/enterprise/attraction?workspace=cultivation&recommendation_tab=cultivation';
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
  const opts = popup.locator('.arco-select-option');
  const sample = await opts
    .allTextContents()
    .then((a) => a.map((t) => t.trim()).filter(Boolean).slice(0, 12))
    .catch(() => []);
  const hit = opts.filter({ hasText: new RegExp(`^${optionText}$`) });
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
    (await page.locator('main.content-shell-layout, main, [data-testid="recruit-tab-stack"]').first().innerText().catch(() => '')) ||
    ''
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
  start_enabled_legal_combo: { pass: false, enabled: false, size: '', industry: '' },
  process_trigger: {
    pass: false,
    reached_processing: false,
    url: '',
    note: '',
  },
  history_completed: {
    pass: false,
    empty: null,
    restore_count: 0,
    view_result_count: 0,
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
    /workspace=cultivation/.test(page.url()) &&
    !page.url().includes('/login');
  gates.deep_link.title = await page.title();
  gates.deep_link.h1 = await page
    .getByRole('heading', { name: '培育企业推荐分析' })
    .isVisible()
    .catch(() => false);
  shots.deep = 'env-gate-deep.png';
  await page.screenshot({ path: path.join(outDir, shots.deep), fullPage: false });

  const start = page.getByRole('button', { name: '开始分析' }).first();
  gates.start_disabled_default.disabled = await start.isDisabled().catch(() => null);
  gates.start_disabled_default.pass = gates.start_disabled_default.disabled === true;

  const sizePick = await pickPlaceholderSelect(page, '全部企业规模', '中型');
  gates.start_enabled_legal_combo.size_pick = sizePick;
  if (sizePick.ok) {
    gates.start_enabled_legal_combo.size = '中型';
  }
  // 产业非门控必填，但常用合法组合：规模+产业
  const indPick = await pickPlaceholderSelect(page, '全部产业类别', '人工智能');
  gates.start_enabled_legal_combo.industry_pick = indPick;
  if (indPick.ok) gates.start_enabled_legal_combo.industry = '人工智能';

  await page.waitForTimeout(600);
  gates.start_enabled_legal_combo.enabled = !(await start.isDisabled().catch(() => true));
  gates.start_enabled_legal_combo.pass = gates.start_enabled_legal_combo.enabled === true;
  gates.start_enabled_legal_combo.body_hit = (await mainText(page)).slice(0, 350);
  shots.gated = 'env-gate-gated.png';
  await page.screenshot({ path: path.join(outDir, shots.gated), fullPage: false });

  // 过程态：点开始分析，只断言进入 processing（成功终态不要求）
  if (gates.start_enabled_legal_combo.pass) {
    try {
      await start.click({ timeout: 5000 });
      await page.waitForTimeout(2500);
      const u = page.url();
      gates.process_trigger.url = u;
      gates.process_trigger.reached_processing =
        /analysis_view=processing/.test(u) ||
        /可视化分析过程|排队中|任务提交/.test(await mainText(page));
      gates.process_trigger.pass = gates.process_trigger.reached_processing;
      gates.process_trigger.note = gates.process_trigger.pass
        ? '可达 processing；成功名单不作为闸门条件'
        : '点击后未进入 processing';
      shots.process = 'env-gate-process.png';
      await page.screenshot({ path: path.join(outDir, shots.process), fullPage: false });
    } catch (e) {
      gates.process_trigger.error = String(e.message || e).slice(0, 160);
    }
  } else {
    gates.process_trigger.note = '开始分析未 enabled，跳过过程触发';
  }

  // 回到配置深链，查最近分析
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
  gates.history_completed.restore_count = await page.getByRole('button', { name: /恢复结果|继续查看|查看结果/ }).count();
  gates.history_completed.view_result_count = gates.history_completed.restore_count;
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
    /企业名称|线索来源|待分析|暂无/.test(candBody) ||
    (await candTab.getAttribute('aria-selected').catch(() => '')) === 'true';

  // 对比篮企业数（候选加入金样前提）
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

// 结果态历史失败不拖垮整体；过程可达记入 summary
const overall = corePass ? 'pass' : 'fail';

const report = {
  surveyed_at: new Date().toISOString(),
  entry_id: 'ent-cultivate',
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
      '登录深链 workspace=cultivation',
      '默认「开始分析」disabled',
      '选企业规模（中型）后「开始分析」enabled',
      '三 Tab 壳 / 候选工作台可达',
      gates.basket_enterprises.pass ? '对比篮有企业（可测加入培育候选）' : null,
      gates.process_trigger.pass
        ? '过程态 processing 可触发（仅 URL/过程壳；成功名单不进金样）'
        : null,
    ].filter(Boolean),
    not_for_gold: [
      gates.history_completed.pass
        ? null
        : '最近分析无已完成任务（暂无数据）→ 结果态/历史复用整段 B',
      '成功名单列构成 / 一企一策 / 空结果 / 同条件复用',
      '新发起常落推荐分析失败（终态成功不进 A）',
    ].filter(Boolean),
    gold_process_trigger: gates.process_trigger.pass ? 'allowed_lite' : 'forbidden',
    history_for_result: gates.history_completed.pass,
  },
  tickets: [
    gates.history_completed.pass ? null : 'ENV-CULTIVATE-HISTORY-EMPTY-001',
    gates.process_trigger.pass ? 'ENV-CULTIVATE-NEWTASK-OFTEN-FAIL-001' : null,
  ].filter(Boolean),
  conclusion: corePass
    ? `环境闸门通过（配置/门控）：登录深链、默认 disabled、选规模后 enabled` +
      (gates.process_trigger.pass ? '；过程 processing 可达（lite）' : '') +
      (gates.history_completed.pass
        ? '；历史有可恢复结果'
        : '；最近分析暂无数据→结果态禁入金样') +
      '。建议 A 档仅配置/门控/Tab/评审（+可选过程 URL）；成功名单与历史复用进 B。'
    : `环境闸门失败：login=${gates.login.pass} deep=${gates.deep_link.pass} emptyDisabled=${gates.start_disabled_default.pass} startEnabled=${gates.start_enabled_legal_combo.pass}。金样仅写可达配置壳或标 blocked。`,
};

fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(report, null, 2) + '\n');
fs.writeFileSync(path.join(outDir, 'scout-env-gate-probe.json'), JSON.stringify(gates, null, 2) + '\n');
console.log(JSON.stringify({ overall: report.overall, tickets: report.tickets, summary: report.summary }, null, 2));
