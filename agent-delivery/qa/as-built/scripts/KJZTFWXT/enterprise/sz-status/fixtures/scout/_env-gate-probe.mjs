#!/usr/bin/env node
/**
 * ent-sz-status 模块闸门二次探针（无头）。产物：env-gate.json + env-gate-*.png + scout-probe.json
 * §3：登录深链 / 无异步开始分析(N/A) / 预检N/A / 坏产业N/A / 历史N/A；
 * 另探：空态引导、区域锁定、选链结果六区块、清单空态、对标 Tab。
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

const baseUrl = 'http://10.50.69.111:30892/';
const route = '/enterprise/shenzhen-enterprise-status-analysis';
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
  for (let i = 0; i < 3; i++) {
    const close = page.locator('[aria-label="关闭对比篮"]');
    if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
      await close.first().click({ force: true }).catch(() => {});
      await page.waitForTimeout(300);
    }
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(200);
  }
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
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  gates.login = { pass: !page.url().includes('/login') };

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
  await page.waitForTimeout(3000);
  await closeBasket(page);

  const url = page.url();
  const title = await page.title();
  const h1 = await page.locator('h1').first().innerText().catch(() => '');
  const guide = await page.getByText('请先选择产业链以加载深圳现状分析').count();
  const tabPos = await page.locator('main [role=tab], main button').filter({ hasText: '产业链定位' }).count();
  const tabBench = await page.locator('main [role=tab], main button').filter({ hasText: '多城市横向对标' }).count();
  const deepOk =
    /shenzhen-enterprise-status-analysis/.test(url) &&
    /深圳企业现状分析/.test(title) &&
    /深圳企业现状分析/.test(h1) &&
    guide > 0 &&
    tabPos > 0 &&
    tabBench > 0;
  gates.deep_link = {
    pass: deepOk,
    url,
    title,
    h1,
    empty_guide: guide > 0,
    tabs: { position: tabPos > 0, benchmark: tabBench > 0 },
  };
  await shot('deep');
  probe.steps.push({ step: 'deep_link', url, title, h1, guide });

  // §3.2 本页无异步「开始分析」——选链即同步加载
  const startBtn = page.getByRole('button', { name: /开始分析/ });
  const startCount = await startBtn.count();
  gates.start_analysis = {
    pass: true,
    n_a: true,
    start_analysis_visible: startCount > 0,
    note: '深圳企业现状分析为选链同步看板，无异步「开始分析」；§3.2 N/A=pass',
  };

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

  // 区域锁定深圳
  const regionText = await page.getByText('全国热门科创城市 / 深圳 / 全部').count();
  const regionDisabled = await page.locator('main .arco-select-view-disabled, main span.sci-arco-cascader.arco-select-view-disabled').count();
  gates.region_locked = {
    pass: regionText > 0 && regionDisabled > 0,
    region_text: regionText > 0,
    disabled: regionDisabled > 0,
  };

  // 空态引导（默认未选链）
  gates.empty_guide = {
    pass: guide > 0,
    text: '请先选择产业链以加载深圳现状分析',
  };

  // 选链：人工智能 → 结果六区块
  await closeBasket(page);
  const chain = page.locator('main .arco-select-view').filter({ has: page.locator('input[placeholder="请选择产业链"]') }).first();
  let chainSelected = false;
  let chainOptions = [];
  let sawLoading = false;
  if (await chain.count()) {
    await chain.click({ timeout: 8000 });
    await page.waitForTimeout(600);
    const opts = page.locator('.arco-trigger-popup:visible .arco-select-option-content');
    const n = await opts.count();
    for (let i = 0; i < n; i++) chainOptions.push(((await opts.nth(i).textContent()) || '').trim());
    const need = ['集成电路', '生物医药', '人工智能', '新能源', '低空经济', '量子信息', '海洋经济', '智能机器人'];
    const optionsOk = need.every((t) => chainOptions.includes(t));
    gates.chain_options = { pass: optionsOk, sample: chainOptions, count: chainOptions.length };
    await page.locator('.arco-trigger-popup:visible').getByText('人工智能', { exact: true }).first().click({ timeout: 8000 });
    chainSelected = true;
    for (let i = 0; i < 20; i++) {
      if (await page.locator('.arco-spin, .arco-skeleton').count()) {
        sawLoading = true;
        break;
      }
      if (await page.getByText('深圳相关企业清单').count()) break;
      await page.waitForTimeout(100);
    }
    await page.waitForTimeout(4000);
  } else {
    gates.chain_options = { pass: false, note: '产业链下拉未找到' };
  }

  const blocks = {};
  for (const t of ['覆盖产业链环节', '重点环节企业', '产业链完整度', '产业链环节分布', '链中角色分布', '深圳相关企业清单']) {
    blocks[t] = (await page.getByText(t, { exact: true }).count()) > 0;
  }
  const blocksOk = Object.values(blocks).every(Boolean);
  const chainEcho = (await page.locator('main .arco-select-view').filter({ hasText: '人工智能' }).count()) > 0;
  const dataUpdate = (await page.getByText(/数据更新至/).count()) > 0;
  const emptyList = (await page.getByText('当前条件下暂无企业').count()) > 0;
  const zeroCount = (await page.getByText('共 0 条').count()) > 0;
  const cols = {};
  for (const c of ['企业名称', '所在区', '链中角色', '操作']) {
    cols[c] = (await page.locator('main th, main .arco-table-th').filter({ hasText: c }).count()) > 0;
  }
  const colsOk = Object.values(cols).every(Boolean);

  gates.chain_select_result = {
    pass: chainSelected && chainEcho && blocksOk,
    chain_selected: chainSelected,
    chain_echo: chainEcho,
    saw_loading_or_result: sawLoading || blocks['深圳相关企业清单'],
    saw_loading: sawLoading,
    blocks,
    data_update: dataUpdate,
  };
  await shot('result-ai');

  gates.table_empty = {
    pass: emptyList && zeroCount && colsOk,
    empty_hint: emptyList,
    zero_count: zeroCount,
    cols,
    note: emptyList
      ? '现场空数据「当前条件下暂无企业 / 共 0 条」为事实；有数据后 P0-04 硬断言需修订'
      : '未见空态文案——可能已有企业数据，P0-03/P0-04 空态断言风险',
  };
  if (emptyList && zeroCount) {
    tickets.push('ENV-SZSTATUS-ZERO-ENTERPRISE-001');
  } else if (!emptyList) {
    tickets.push('ENV-SZSTATUS-DATA-SHAPE-001');
  }

  // 对标 Tab
  await closeBasket(page);
  const benchTab = page.locator('main [role=tab], main .arco-tabs-tab, main button').filter({ hasText: '多城市横向对标' }).first();
  let benchOk = false;
  const cities = {};
  if (await benchTab.count()) {
    await benchTab.click({ timeout: 8000 });
    await page.waitForTimeout(3500);
    const benchShell =
      (await page.getByText('对标城市').count()) > 0 ||
      (await page.getByText('城市 × 指标对比表').count()) > 0 ||
      (await page.getByText('同口径多指标雷达对比').count()) > 0;
    for (const c of ['北京', '上海', '苏州', '深圳']) {
      cities[c] = (await page.locator('main').getByText(c, { exact: true }).count()) > 0;
    }
    benchOk = benchShell && cities['北京'] && cities['上海'] && cities['苏州'] && cities['深圳'];
  }
  gates.benchmark_tab = {
    pass: benchOk,
    cities,
    body_hit: (await page.locator('main').innerText().catch(() => '')).slice(0, 800),
  };
  await shot('benchmark');

  // 对比篮干扰
  const basketOpen = (await page.getByText('篮内企业').count()) > 0 && (await page.locator('[aria-label="关闭对比篮"]').count()) > 0;
  if (basketOpen) tickets.push('ENV-SZSTATUS-BASKET-OVERLAY-001');
  gates.basket_noise = {
    pass: true,
    note: basketOpen
      ? '对比篮浮层曾出现；探针已 Esc/关闭，脚本须先关篮'
      : '本轮深链后对比篮未持续挡主区（或已关闭）',
    basket_open_seen: basketOpen,
  };

  probe.steps.push({
    step: 'result',
    blocks,
    emptyList,
    zeroCount,
    cols,
    cities,
    chainOptions,
  });
  fs.writeFileSync(path.join(outDir, 'scout-probe.json'), JSON.stringify(probe, null, 2), 'utf8');

  const overallPass =
    gates.login.pass &&
    gates.deep_link.pass &&
    gates.start_analysis.pass &&
    gates.precheck_eval.pass &&
    gates.input_object_invalid.pass &&
    gates.history_completed.pass &&
    gates.region_locked.pass &&
    gates.empty_guide.pass &&
    gates.chain_options.pass &&
    gates.chain_select_result.pass &&
    gates.benchmark_tab.pass;

  // 金样建议（只建议不改 index/cases）
  const currentGold = ['P0-01', 'P0-02', 'P0-03', 'P0-04', 'P0-05'];
  const suggestKeep = ['P0-01', 'P0-02', 'P0-05'];
  const suggestKeepOrCaution = [];
  // P0-03 六区块可测；但 P0-03 同时断言空态「暂无企业」——空数据事实下可留 A
  if (gates.chain_select_result.pass && gates.table_empty.empty_hint) {
    suggestKeep.push('P0-03');
    suggestKeep.push('P0-04');
  } else {
    suggestKeepOrCaution.push('P0-03', 'P0-04');
  }
  const suggestPromote = ['P0-06', 'P0-07', 'P0-08'];
  // 若空数据稳定，P0-10 也可升；过程态 P0-09 易闪过不进 A
  if (gates.table_empty.empty_hint) suggestPromote.push('P0-10');

  const suggested_gold = [...new Set([...suggestKeep.slice(0, 5)])];
  // 凑满建议：现 gold 在空数据环境下可全留；备选补 P0-06/07/08
  const suggested_gold_final = gates.table_empty.empty_hint
    ? ['P0-01', 'P0-02', 'P0-03', 'P0-04', 'P0-05']
    : ['P0-01', 'P0-02', 'P0-05', 'P0-06', 'P0-08'];

  const forbid = {
    'P0-09': '过程态 loading 极快可能只见结果；易闪过，不进金样（B）',
    'P0-11': '对标三项指标细断言，依赖对标数据形态',
    'P0-12': '对标缺口径「暂不可用/无数据」依赖空/缺数据',
    'P0-13': '相对优势/短板依赖对标计算结果',
    'P0-14': '对标计算中过程态，易闪过',
    'P1-03': '批量栏全选依赖清单有可选企业；当前空数据不可测',
    'P1-04': 'allow_skip 报告浮层；缺正式 ticket 编号',
    'P1-05': '评审追溯显隐，非主路径金样',
  };

  const envGate = {
    surveyed_at: new Date().toISOString(),
    entry_id: 'ent-sz-status',
    base_url: baseUrl,
    route,
    headless: true,
    method: 'survey-page.mjs + _env-gate-probe.mjs (no IDE browser)',
    overall: overallPass ? 'pass' : 'fail',
    gates,
    evidence: {
      screenshots: shots,
      scout_refs: ['scout.json', 'scout.md', 'page.png', 'scout-probe.json'],
    },
    summary: {
      no_async_analysis: true,
      stable_for_gold: [
        '登录深链 /enterprise/shenzhen-enterprise-status-analysis',
        '默认空态引导「请先选择产业链…」+ 双 Tab',
        '区域锁定深圳 disabled',
        '下拉 8 链可选；选人工智能后六区块+清单壳',
        '对标 Tab 城市池北京/上海/苏州+深圳锚点',
      ],
      not_for_gold: [
        '选链 loading 过程态（极快）',
        '对标指标细项/缺口径/优势短板（数据形态）',
        '批量全选（需有企业行）',
        '报告浮层 allow_skip',
      ],
      zero_enterprise_data: !!gates.table_empty.empty_hint,
    },
    tickets: [...new Set(tickets)],
    current_index_gold: currentGold,
    suggest_keep_gold: suggested_gold_final,
    suggest_downgrade_to_B: gates.table_empty.empty_hint ? [] : ['P0-03', 'P0-04'],
    suggest_promote_to_gold: gates.table_empty.empty_hint ? [] : ['P0-06', 'P0-08'],
    suggested_gold: suggested_gold_final,
    suggest_alt_promote: ['P0-06', 'P0-07', 'P0-08', 'P0-10'],
    forbid_gold_reasons: forbid,
    conclusion: overallPass
      ? `环境闸门 overall=pass：登录深链、无异步开始分析(§3.2–3.5 N/A)、空态引导、区域锁定、选人工智能六区块+清单壳、对标 Tab 城市池可达。空企业数据=${!!gates.table_empty.empty_hint}。建议金样=${suggested_gold_final.join(',')}。tickets=${[...new Set(tickets)].join(',') || '(无)'}`
      : `环境闸门 overall=fail：见 gates 失败项。tickets=${[...new Set(tickets)].join(',') || '(无)'}`,
    suggested_gold_rationale: gates.table_empty.empty_hint
      ? '空数据事实下现 index gold P0-01~05 均可机跑：壳/选链/六区块+空态/表列+共0条/对标城市池。备选升 A：P0-06 区域锁定、P0-07 八选项、P0-08 空引导、P0-10 清单空态。禁入 A：P0-09/14 过程态、P1-03 需有行、P1-04 allow_skip。不改 cases/index（仅建议）。'
      : '若空态消失则降 B：P0-03/P0-04（硬断言空文案）；升 A：P0-06/P0-08。不改 cases/index（仅建议）。',
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2), 'utf8');
  console.log('overall', envGate.overall);
  console.log('suggested_gold', envGate.suggested_gold.join(','));
  console.log('tickets', envGate.tickets.join(','));
  console.log('gates', Object.fromEntries(Object.entries(gates).map(([k, v]) => [k, v.pass])));
} catch (e) {
  console.error('probe error', e);
  fs.writeFileSync(
    path.join(outDir, 'env-gate.json'),
    JSON.stringify(
      {
        surveyed_at: new Date().toISOString(),
        entry_id: 'ent-sz-status',
        overall: 'fail',
        error: String(e && e.stack ? e.stack : e),
        gates,
        tickets: ['ENV-SZSTATUS-PROBE-CRASH-001'],
      },
      null,
      2,
    ),
    'utf8',
  );
  process.exitCode = 1;
} finally {
  await browser.close();
}
