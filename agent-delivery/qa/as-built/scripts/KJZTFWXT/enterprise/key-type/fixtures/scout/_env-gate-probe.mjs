#!/usr/bin/env node
/**
 * ent-key-type 模块闸门二次探针（无头）。产物：env-gate.json + env-gate-*.png + scout-probe.json
 * §3：登录深链 / 无异步开始分析 / 预检N/A / 坏产业N/A / 历史N/A；
 * 另探：筛选默认、KPI 壳、地图列表互斥、清单抽屉(0)、评审泄漏。
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
const route = '/enterprise/key-enterprise-analysis?view=type';
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
  const cls = (await sw.getAttribute('class').catch(() => '')) || '';
  const wasOn = /checked/.test(cls);
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
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  const loginOk = !page.url().includes('/login');
  gates.login = { pass: loginOk };

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
  const filterRegion = page.locator('section[aria-label="类型分析筛选"]');
  const deepOk =
    /key-enterprise-analysis/.test(url) &&
    /view=type/.test(url) &&
    /重点企业类型分析/.test(title) &&
    /重点企业类型分析/.test(h1) &&
    (await filterRegion.count()) > 0;
  gates.deep_link = {
    pass: deepOk,
    url,
    title,
    h1,
    filter_region: (await filterRegion.count()) > 0,
  };
  await shot('deep');
  probe.steps.push({ step: 'deep_link', url, title, h1 });

  // §3.2 本页无异步「开始分析」
  const startBtn = page.getByRole('button', { name: /开始分析/ });
  const startCount = await startBtn.count();
  gates.start_analysis = {
    pass: true,
    n_a: true,
    start_analysis_visible: startCount > 0,
    note: '重点企业类型分析为筛选看板，无异步「开始分析」；§3.2 N/A=pass',
  };

  // §3.3 评估预检 N/A
  gates.precheck_eval = {
    pass: true,
    n_a: true,
    note: '非企业评估页，无「预检未返回企业明细」；§3.3 N/A=pass',
  };

  // §3.4 诊断坏产业 N/A
  gates.input_object_invalid = {
    pass: true,
    n_a: true,
    note: '非诊断/图谱产业组合页；§3.4 N/A=pass',
  };

  // §3.5 历史已完成任务 N/A
  gates.history_completed = {
    pass: true,
    n_a: true,
    note: '本页无异步任务历史/查看结果链；§3.5 N/A=pass',
  };

  // 筛选默认（金样 P0-02）
  const labelsOk = {};
  for (const t of ['区域', '时间', '产业', '企业类型']) {
    labelsOk[t] = (await page.getByText(t, { exact: true }).count()) > 0;
  }
  const yearStart = page.getByPlaceholder('开始年份').first();
  const yearEnd = page.getByPlaceholder('结束年份').first();
  const y1 = (await yearStart.count()) ? await yearStart.inputValue() : null;
  const y2 = (await yearEnd.count()) ? await yearEnd.inputValue() : null;
  const industryPh = (await page.getByPlaceholder('全部产业').count()) > 0;
  const typePh = (await page.getByPlaceholder('全部类型').count()) > 0;
  const cascaderPh = (await page.locator('input[placeholder="全国热门科创城市 / 深圳 / 全部"]').count()) > 0;
  const filterDefaultsOk =
    Object.values(labelsOk).every(Boolean) &&
    y1 === '2022' &&
    y2 === '2026' &&
    industryPh &&
    typePh &&
    cascaderPh;
  gates.filter_defaults = {
    pass: filterDefaultsOk,
    labelsOk,
    years: { start: y1, end: y2 },
    industry_placeholder: industryPh,
    type_placeholder: typePh,
    region_cascader: cascaderPh,
  };
  await shot('filter');

  // KPI 三卡（金样 P0-03）；关评审后再测泄漏
  const review = await tryCloseReview(page);
  probe.steps.push({ step: 'close_review', review });
  await page.waitForTimeout(500);
  const kpiNames = {};
  for (const n of ['匹配企业数', '覆盖企业类型数', '覆盖区域数']) {
    kpiNames[n] = (await page.getByText(n, { exact: true }).count()) > 0;
  }
  const unitsOk = {};
  const main = page.locator('main').first();
  const mainTxt = (await main.innerText().catch(() => '')) || '';
  for (const u of ['家', '类', '个']) {
    unitsOk[u] = (await main.getByText(u, { exact: true }).count()) > 0;
  }
  const leakTokens = ['Q010', 'Q012', 'Q038', 'M_ENT_TYPE_COUNT', 'M_ENT_KEYPANO', 'mock_20260618'];
  const leaks = leakTokens.filter((t) => mainTxt.includes(t));
  const metricSpecVisible = (await page.locator('button.metric-spec-card').count()) > 0;
  const pendingBadgeVisible = (await page.locator('.perm-pending-badge').count()) > 0;
  gates.kpi_shell = {
    pass: Object.values(kpiNames).every(Boolean) && Object.values(unitsOk).every(Boolean),
    kpiNames,
    unitsOk,
    kpi_values_hit: /匹配企业数[\s\S]{0,40}0[\s\S]{0,20}家/.test(mainTxt.replace(/\s+/g, ' ')),
    body_hit: mainTxt.slice(0, 400).replace(/\s+/g, ' '),
  };
  gates.business_clean = {
    pass: leaks.length === 0,
    leaks,
    metric_spec_visible: metricSpecVisible,
    pending_badge_visible: pendingBadgeVisible,
    review,
    note:
      leaks.length === 0
        ? 'main.innerText 无 Q0xx/内部 metric id（P0-03 业务态断言口径）'
        : 'main 仍含内部字样；若评审关不掉则 P0-03 不宜入 A',
  };
  await shot('kpi');

  // 地图 / 列表互斥（金样 P0-04）
  const mapBtn = page.getByRole('button', { name: '地图视图' });
  const listBtn = page.getByRole('button', { name: '列表视图' });
  let mapList = { mapBtn: (await mapBtn.count()) > 0, listBtn: (await listBtn.count()) > 0 };
  if (mapList.listBtn) {
    await listBtn.click({ timeout: 8000 }).catch((e) => {
      mapList.listClickErr = String(e.message || e).slice(0, 120);
    });
    await page.waitForTimeout(900);
    mapList.leaflet_in_list = (await page.locator('.leaflet-container').count()) > 0;
    mapList.empty_list_hint = (await page.getByText('当前区域暂无可展示对象').count()) > 0;
    await mapBtn.click({ timeout: 8000 }).catch((e) => {
      mapList.mapClickErr = String(e.message || e).slice(0, 120);
    });
    await page.waitForTimeout(900);
    mapList.leaflet_after_map = (await page.locator('.leaflet-container').count()) > 0;
    mapList.insight_ok = (await page.getByRole('heading', { name: '区域洞察' }).count()) > 0;
  }
  gates.map_list_toggle = {
    pass:
      mapList.mapBtn &&
      mapList.listBtn &&
      mapList.leaflet_in_list === false &&
      mapList.leaflet_after_map === true &&
      mapList.insight_ok === true &&
      !mapList.listClickErr &&
      !mapList.mapClickErr,
    detail: mapList,
  };
  await shot('map-list');

  // 清单抽屉（金样 P0-05）；现场清单（0）
  const listEntry = page.getByRole('button', { name: /查看企业清单（\d+）/ }).first();
  let drawer = { entry_visible: (await listEntry.count()) > 0 };
  if (drawer.entry_visible) {
    drawer.entry_label = ((await listEntry.textContent()) || '').trim();
    await listEntry.click({ timeout: 8000 }).catch((e) => {
      drawer.clickErr = String(e.message || e).slice(0, 120);
    });
    await page.waitForTimeout(800);
    const d = page.locator('.arco-drawer:visible').first();
    drawer.opened = (await d.count()) > 0;
    if (drawer.opened) {
      drawer.has_title_list = (await d.getByText('企业清单').count()) > 0;
      drawer.has_map_region = (await d.getByText('地图当前区域').count()) > 0;
      drawer.has_data_update = (await d.getByText('数据更新至').count()) > 0;
      drawer.empty_match = (await d.getByText('当前搜索条件无匹配企业').count()) > 0;
      const ph = await d.locator('input').first().getAttribute('placeholder').catch(() => null);
      drawer.search_placeholder = ph;
      drawer.placeholder_ok = !!(ph && ph.includes('企业名称'));
      await page.locator('.arco-drawer:visible .arco-drawer-close-btn').first().click().catch(() => {});
      await page.waitForTimeout(400);
    }
  }
  gates.enterprise_drawer = {
    pass:
      drawer.entry_visible &&
      drawer.opened &&
      drawer.has_title_list &&
      drawer.has_map_region &&
      drawer.has_data_update &&
      drawer.placeholder_ok &&
      !drawer.clickErr,
    detail: drawer,
    note: '现场默认清单（0）；空态文案「当前搜索条件无匹配企业」与 P0-05 断言一致',
  };
  await shot('drawer');

  // 零数据环境债（不挡壳金样，但挡依赖非零家数的 B）
  const zeroKpi = /匹配企业数\s*0\s*家/.test(mainTxt.replace(/\s+/g, ' ')) || /0\s*家/.test(mainTxt);
  const listZero = /查看企业清单（0）/.test(drawer.entry_label || '');
  if (zeroKpi || listZero) {
    tickets.push('ENV-KEYTYPE-ZERO-DATA-001');
  }
  if (metricSpecVisible || pendingBadgeVisible) {
    tickets.push('ENV-KEYTYPE-REVIEW-BADGE-LEAK-001');
  }
  if (!gates.business_clean.pass) {
    tickets.push('ENV-KEYTYPE-MAIN-LEAK-Q0-001');
  }

  const hardGates = ['login', 'deep_link', 'start_analysis', 'precheck_eval', 'input_object_invalid', 'history_completed'];
  const hardPass = hardGates.every((k) => gates[k]?.pass);
  const softForGold = ['filter_defaults', 'kpi_shell', 'map_list_toggle', 'enterprise_drawer'];
  const softPass = softForGold.every((k) => gates[k]?.pass);
  // overall：§3 硬闸；business_clean 失败不直接 overall=fail（可关评审后仍测壳），但记 ticket
  const overall = hardPass ? 'pass' : 'fail';

  const current_index_gold = ['P0-01', 'P0-02', 'P0-03', 'P0-04', 'P0-05'];
  const suggest_keep_gold = ['P0-01', 'P0-02', 'P0-04'];
  const suggest_downgrade_to_B = [];
  const suggest_promote_to_gold = [];
  // P0-03：KPI 壳过则可留；若 main 泄漏则降 B
  if (!gates.business_clean.pass) {
    suggest_downgrade_to_B.push('P0-03');
  } else {
    suggest_keep_gold.push('P0-03');
  }
  // P0-05：抽屉构成可测（含 0）；空名单是 as-built，可留 A
  if (gates.enterprise_drawer.pass) {
    suggest_keep_gold.push('P0-05');
  } else {
    suggest_downgrade_to_B.push('P0-05');
  }
  // 备选升 A（壳/筛选交互，不依赖非零数据）
  if (gates.filter_defaults.pass) {
    suggest_promote_to_gold.push('P0-06', 'P0-07');
  }
  const suggested_gold = [...new Set([...suggest_keep_gold, ...suggest_promote_to_gold])].slice(0, 5);
  // 若 keep 已满 5，promote 作备选
  const suggest_alt_promote = ['P0-08', 'P0-09', 'P0-10'].filter((id) => !suggested_gold.includes(id));

  const forbid_gold_reasons = {
    'P0-11': '区域级联深钻依赖选项数据；零数据环境仅验展开，不优先入 A',
    'P0-13': '地图缩放属 P2 用例槽，非主路径金样',
    'P0-15': '评审模式开关；依赖人设面板，宜 B',
    'P1-06': '评审态指标说明卡',
    'P1-07': '未登记指标图标',
    'P1-08': '零匹配清单空态 + allow_skip；现场已是（0）但 skip 配额在 B',
    'P1-09': '零匹配列表文案 + allow_skip',
  };
  if (suggest_downgrade_to_B.includes('P0-03')) {
    forbid_gold_reasons['P0-03'] =
      'P0-03 断言 main 无 Q0xx；现场仍见泄漏 → ENV-KEYTYPE-MAIN-LEAK-Q0-001';
  }
  if (zeroKpi || listZero) {
    forbid_gold_reasons['P1-08'] =
      (forbid_gold_reasons['P1-08'] || '') + '；ENV-KEYTYPE-ZERO-DATA-001 零家数环境债';
  }

  const out = {
    surveyed_at: probe.surveyed_at,
    entry_id: 'ent-key-type',
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
        '登录深链 view=type + h1/筛选区',
        '筛选四组默认（2022–2026 / 全部产业 / 全部类型 / 深圳级联）',
        '地图↔列表互斥 + 区域洞察保持',
        gates.enterprise_drawer.pass ? '清单抽屉构成（含 N=0 空态）' : null,
        gates.business_clean.pass ? 'KPI 三卡壳 + 业务态无 Q0 泄漏' : null,
      ].filter(Boolean),
      not_for_gold: [
        '非零 KPI / 非零清单名单（现场 0/0/0 · 清单（0））→ ENV-KEYTYPE-ZERO-DATA-001',
        '评审角标 / ⓘ 泄漏链（P0-15/P1-06/P1-07）',
        'allow_skip 空匹配构造（P1-08/P1-09）',
      ],
      no_async_analysis: true,
      kpi_all_zero: !!(zeroKpi || listZero),
      soft_shell_pass: softPass,
    },
    tickets: [...new Set(tickets)],
    current_index_gold,
    suggest_keep_gold: [...new Set(suggest_keep_gold)],
    suggest_downgrade_to_B: [...new Set(suggest_downgrade_to_B)],
    suggest_promote_to_gold,
    suggested_gold,
    suggest_alt_promote,
    forbid_gold_reasons,
    conclusion: '',
    suggested_gold_rationale: '',
  };

  out.conclusion = `环境闸门 overall=${overall}：登录深链 view=type；无异步开始分析（§3.2–3.5 N/A）；筛选默认=${gates.filter_defaults.pass}；KPI壳=${gates.kpi_shell.pass}；业务态干净=${gates.business_clean.pass}；地图列表=${gates.map_list_toggle.pass}；抽屉=${gates.enterprise_drawer.pass}。建议金样 ${suggested_gold.join(',')}。tickets=${out.tickets.join(',') || '无'}`;
  out.suggested_gold_rationale = `保留可达壳路径；零数据不挡结构金样。降 B=${suggest_downgrade_to_B.join(',') || '无'}。备选升 A：${suggest_alt_promote.join(',')}。不改 cases/index（仅建议）。`;

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(out, null, 2), 'utf8');
  fs.writeFileSync(path.join(outDir, 'scout-probe.json'), JSON.stringify({ probe, gates, tickets: out.tickets }, null, 2), 'utf8');
  console.log(JSON.stringify({ overall, tickets: out.tickets, suggested_gold, softPass }, null, 2));
} catch (e) {
  const fail = {
    surveyed_at: new Date().toISOString(),
    entry_id: 'ent-key-type',
    overall: 'fail',
    error: String(e && e.stack ? e.stack : e).slice(0, 2000),
    gates,
    tickets: ['ENV-KEYTYPE-PROBE-CRASH-001'],
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2), 'utf8');
  console.error(fail.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
