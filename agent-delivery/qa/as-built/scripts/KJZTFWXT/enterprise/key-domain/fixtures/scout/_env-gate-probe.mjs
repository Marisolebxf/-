#!/usr/bin/env node
/**
 * ent-key-domain 模块闸门二次探针（无头）。
 * 产物：env-gate.json + env-gate-*.png + scout-probe.json
 * §3：登录深链 / 无异步「开始分析」(N/A) / 预检N/A / 坏产业N/A / 历史N/A；
 * 另探：空态引导、页内回填→结果四大区块、对比篮有企业、评审可关。
 * 禁止当 runner；禁止有头；disabled 不硬点。
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
const route = '/enterprise/key-enterprise-analysis?view=domain';
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
    await page.waitForTimeout(300);
  }
}

async function tryCloseReview(page) {
  const persona = page.locator('button.persona-switch').first();
  if (!(await persona.count())) return { tried: false };
  await persona.click().catch(() => {});
  await page.waitForTimeout(500);
  const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
  if (!(await sw.count())) {
    await page.keyboard.press('Escape').catch(() => {});
    return { tried: true, switchFound: false };
  }
  const checked = (await sw.getAttribute('aria-checked').catch(() => '')) || '';
  const wasOn = checked === 'true';
  if (wasOn) {
    await sw.click({ timeout: 4000 }).catch(() => {});
    await page.waitForTimeout(800);
  }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(300);
  return { tried: true, switchFound: true, wasOn, turnedOff: wasOn };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const gates = {};
const tickets = [];
const shots = [];
const shot = async (name) => {
  const file = `env-gate-${name}.png`;
  await page.screenshot({ path: path.join(outDir, file), fullPage: false });
  shots.push(file);
  return file;
};

const probe = { surveyed_at: new Date().toISOString(), steps: [] };

try {
  // 1) login
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  const loginOk = !page.url().includes('/login');
  gates.login = { pass: loginOk };
  probe.steps.push({ login: loginOk, url: page.url() });
  if (!loginOk) tickets.push('ENV-KEYDOMAIN-LOGIN-001');

  // 2) deep link
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await ensureLogin(page);
  if (page.url().includes('/login')) {
    await ensureLogin(page);
    await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), {
      waitUntil: 'domcontentloaded',
      timeout: 60000,
    });
  }
  await page.waitForTimeout(2500);
  await closeBasket(page);

  const url = page.url();
  const title = await page.title();
  const h1 = await page.locator('h1').first().innerText().catch(() => '');
  const objectBar = (await page.locator('[aria-label="领域分析对象"]').count()) > 0;
  const deepOk =
    /key-enterprise-analysis/.test(url) &&
    /view=domain/.test(url) &&
    /重点企业领域分析/.test(title) &&
    /重点企业领域分析/.test(h1);
  gates.deep_link = {
    pass: deepOk,
    url,
    title,
    h1: h1.trim(),
    object_bar: objectBar,
  };
  await shot('deep');
  probe.steps.push({ deep_link: deepOk, url, title, h1 });
  if (!deepOk) tickets.push('ENV-KEYDOMAIN-DEEPLINK-001');

  // empty state (may already have residual codes — clear by re-goto without codes)
  if (/enterprise_codes/.test(url) || (await page.getByRole('heading', { name: '领域布局概览' }).count())) {
    await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), {
      waitUntil: 'domcontentloaded',
      timeout: 60000,
    });
    await page.waitForTimeout(1500);
    await closeBasket(page);
  }
  const emptyHeading = (await page.getByRole('heading', { name: '待选择分析对象' }).count()) > 0;
  const emptyCta = (await page.getByRole('button', { name: '前往对比篮选择企业' }).count()) > 0;
  const noResultBlocks = !(await page.getByRole('heading', { name: '领域布局概览' }).count());
  gates.empty_state = {
    pass: emptyHeading && emptyCta && noResultBlocks,
    emptyHeading,
    emptyCta,
    noResultBlocks,
  };
  await shot('empty');
  if (!gates.empty_state.pass) tickets.push('ENV-KEYDOMAIN-EMPTY-001');

  // §3.2 start_analysis — 本页无异步「开始分析」工作区；结果态经页内回填/系统发起同步进
  const startBtn = page.getByRole('button', { name: /^开始分析$/ });
  const startVisible = (await startBtn.count()) > 0 && (await startBtn.first().isVisible().catch(() => false));
  gates.start_analysis = {
    pass: true,
    n_a: true,
    start_analysis_visible: startVisible,
    note: '重点企业领域分析无异步「开始分析」；对象经页内选择分析企业确定回填或系统对比篮「发起分析」进结果态；§3.2 N/A=pass',
  };

  // §3.3 / §3.4 / §3.5 N/A
  gates.precheck_eval = {
    pass: true,
    n_a: true,
    note: '非企业评估页，无「预检未返回企业明细」；§3.3 N/A=pass',
  };
  gates.input_object_invalid = {
    pass: true,
    n_a: true,
    note: '非诊断/图谱产业组合页；§3.4 N/A=pass',
  };
  gates.history_completed = {
    pass: true,
    n_a: true,
    note: '本页无异步任务历史/查看结果链；§3.5 N/A=pass',
  };

  // review close
  const review = await tryCloseReview(page);
  gates.close_review = { pass: review.tried !== false, ...review };
  await shot('review');

  // basket has selectable enterprises
  await page.getByRole('button', { name: /打开对比篮|前往对比篮选择企业/ }).first().click({ timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(1000);
  // page picker modal OR system basket
  let selectCount = await page.locator('[aria-label^="选择 "]').count();
  // if system panel opened instead, same selectors
  if (!selectCount) {
    await page.locator('button[aria-label*="打开对比篮"]').first().click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(800);
    selectCount = await page.locator('[aria-label^="选择 "]').count();
  }
  gates.basket_enterprises = {
    pass: selectCount >= 1,
    select_count: selectCount,
  };
  await shot('basket');
  if (!gates.basket_enterprises.pass) tickets.push('ENV-KEYDOMAIN-BASKET-EMPTY-001');

  // page picker → result blocks (主路径，对应 P0-03)
  let resultOk = false;
  let resultBlocks = {};
  let resultUrl = '';
  let kpiHit = false;
  if (selectCount >= 1) {
    // ensure page picker: look for 确定 in modal; if system basket, close and use 前往对比篮选择企业
    const confirmBtn = page.getByRole('button', { name: '确定' });
    let hasConfirm = (await confirmBtn.count()) > 0 && (await confirmBtn.first().isVisible().catch(() => false));
    if (!hasConfirm) {
      await closeBasket(page);
      await page.getByRole('button', { name: '前往对比篮选择企业' }).first().click({ timeout: 8000 }).catch(() => {});
      await page.waitForTimeout(1000);
      hasConfirm = (await confirmBtn.count()) > 0 && (await confirmBtn.first().isVisible().catch(() => false));
      selectCount = await page.locator('[aria-label^="选择 "]').count();
    }
    if (hasConfirm && selectCount >= 1) {
      const n = Math.min(2, selectCount);
      for (let i = 0; i < n; i++) {
        await page.locator('[aria-label^="选择 "]').nth(i).click().catch(() => {});
      }
      await page.waitForTimeout(400);
      // 确定 must be enabled — only click if not disabled
      const conf = confirmBtn.first();
      const disabled = await conf.isDisabled().catch(() => true);
      if (!disabled) {
        await conf.click({ timeout: 8000 });
        await page.waitForTimeout(3500);
        resultUrl = page.url();
        resultBlocks = {
          领域布局概览: (await page.getByRole('heading', { name: '领域布局概览' }).count()) > 0,
          企业领域覆盖: (await page.getByRole('heading', { name: '企业领域覆盖' }).count()) > 0,
          跨领域布局: (await page.getByRole('heading', { name: '跨领域布局' }).count()) > 0,
          重点领域分布: (await page.getByRole('heading', { name: '重点领域分布' }).count()) > 0,
        };
        resultOk = Object.values(resultBlocks).every(Boolean);
        const mainTxt = (await page.locator('main').innerText().catch(() => '')) || '';
        kpiHit = /已覆盖领域/.test(mainTxt) && /涉及企业/.test(mainTxt);
        await shot('result');
      } else {
        probe.steps.push({ picker_confirm_disabled: true });
      }
    } else {
      probe.steps.push({ page_picker_missing: true, selectCount });
    }
  }
  gates.result_via_picker = {
    pass: resultOk,
    resultBlocks,
    url: resultUrl,
    kpi_labels: kpiHit,
  };
  if (!resultOk) tickets.push('ENV-KEYDOMAIN-RESULT-PICKER-001');

  // business clean (review off)
  await tryCloseReview(page);
  const mainTxt2 = (await page.locator('main').innerText().catch(() => '')) || '';
  const leaks = ['Q013', 'M_ENT_DOMAIN', 'ENT-KEYENT-F', 'GAP-'].filter((t) => mainTxt2.includes(t));
  gates.business_clean = {
    pass: leaks.length === 0,
    leaks,
    note: '关评审后 main 无内部 metric/Q0 泄漏（软检）',
  };

  const critical = [
    gates.login?.pass,
    gates.deep_link?.pass,
    gates.start_analysis?.pass,
    gates.precheck_eval?.pass,
    gates.input_object_invalid?.pass,
    gates.history_completed?.pass,
  ];
  // result_via_picker is hard for gold P0-03~05 — fail overall if basket empty or result unreachable
  const overall =
    critical.every(Boolean) && gates.basket_enterprises?.pass && gates.result_via_picker?.pass ? 'pass' : 'fail';

  const suggested_gold = ['P0-01', 'P0-02', 'P0-03', 'P0-04', 'P0-05'];
  const out = {
    surveyed_at: new Date().toISOString(),
    entry_id: 'ent-key-domain',
    base_url: baseUrl,
    route,
    headless: true,
    method: 'survey-page.mjs + _env-gate-probe.mjs (no IDE browser)',
    overall,
    gates,
    evidence: {
      screenshots: shots,
      scout_refs: ['scout.json', 'scout.md', 'page.png', 'scout-probe.json'],
    },
    summary: {
      stable_for_gold: [
        '登录深链 view=domain + h1/领域分析对象',
        '空态待选择引导 + 前往对比篮 CTA',
        '页内回填≥1 家 → 结果四大区块',
        '概览 KPI 壳（已覆盖领域/涉及企业…）',
        '无异步开始分析（§3.2–3.5 N/A）',
      ],
      not_for_gold: [
        'P1-04 同名异主体造数（manual/allow_skip）→ ENV-KEYDOMAIN-SAME-NAME-SAMPLE-001',
        '评审开关联/追溯链（P1-01/P1-08）宜 B',
        '六类型弹窗系统路径（P0-06）可作备选升 A',
      ],
      no_async_analysis: true,
      result_via_picker: resultOk,
    },
    tickets: [...new Set(tickets)],
    current_index_gold: ['P0-01', 'P0-02', 'P0-03', 'P0-04', 'P0-05'],
    suggest_keep_gold: suggested_gold,
    suggest_downgrade_to_B: overall === 'fail' ? ['P0-03', 'P0-04', 'P0-05'] : [],
    suggest_promote_to_gold: [],
    suggested_gold,
    suggest_alt_promote: ['P0-06', 'P0-07', 'P0-09', 'P0-12', 'P1-06'],
    forbid_gold_reasons: {
      'P1-04': 'manual + allow_skip；无比对不同信用代码同名字号样本；ENV-KEYDOMAIN-SAME-NAME-SAMPLE-001',
      'P1-01': '评审态多源口径说明；依赖人设面板',
      'P1-08': '评审开关零泄漏；依赖人设面板',
      'P0-08': '对象联动调参，路径长于壳层金样',
      'P1-07': '刷新恢复结果态，偏稳态韧性非主路径',
    },
    conclusion:
      overall === 'pass'
        ? '环境闸门 overall=pass：登录深链 view=domain；无异步开始分析（§3.2–3.5 N/A）；页内回填可达结果四大区块。现 index gold P0-01~P0-05 可保留。tickets 见同名字号样本债。'
        : `环境闸门 overall=fail：critical/basket/result 未齐。tickets=${[...new Set(tickets)].join(',') || 'none'}。金样仅保留可达壳层，结果态降 B。`,
    suggested_gold_rationale:
      '建议金样=现 gold P0-01~P0-05（零 allow_skip；空态+页内回填结果壳可机测）。备选升 A：P0-06/07/09/12/P1-06。禁入 A：P1-04（allow_skip）、P1-01/08（评审链）。不改 cases/index（仅建议）。',
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(out, null, 2), 'utf8');
  fs.writeFileSync(path.join(outDir, 'scout-probe.json'), JSON.stringify({ ...probe, gates, tickets: out.tickets }, null, 2), 'utf8');
  console.log('overall=', overall);
  console.log('tickets=', out.tickets);
  console.log('result_via_picker=', resultOk, resultBlocks);
  console.log('wrote env-gate.json');
} catch (e) {
  console.error('probe fatal', e);
  const failOut = {
    surveyed_at: new Date().toISOString(),
    entry_id: 'ent-key-domain',
    base_url: baseUrl,
    route,
    headless: true,
    overall: 'fail',
    gates,
    tickets: [...new Set([...tickets, 'ENV-KEYDOMAIN-PROBE-FATAL-001'])],
    error: String(e && e.message ? e.message : e),
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(failOut, null, 2), 'utf8');
  process.exitCode = 1;
} finally {
  await browser.close();
}
