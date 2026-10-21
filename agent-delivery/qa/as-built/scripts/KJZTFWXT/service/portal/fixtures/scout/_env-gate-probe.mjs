#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针（svc-portal 回炉）。产物：env-gate.json + env-gate-*.png
 * 禁止当 runner；禁止有头 MCP。
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

async function pickIndustry(page, name) {
  const ind = page
    .locator('.arco-select-view')
    .filter({ has: page.locator('input[placeholder="全部产业"]') })
    .first();
  if (!(await ind.count())) return false;
  await ind.click();
  await page.waitForTimeout(350);
  const opt = page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: name }).first();
  if (!(await opt.count())) {
    await page.keyboard.press('Escape');
    return false;
  }
  await opt.click();
  await page.waitForTimeout(900);
  return true;
}

const hasText = async (page, re) => (await page.getByText(re).count()) > 0;
const hasHeading = async (page, name) =>
  (await page.getByRole('heading', { name }).count()) > 0;

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const gates = [];
const shot = async (name) => {
  const p = path.join(outDir, `env-gate-${name}.png`);
  await page.screenshot({ path: p, fullPage: false });
  return `fixtures/scout/env-gate-${name}.png`;
};

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL('service-portal', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  const urlOk = /\/service-portal\/overview/.test(page.url());
  const titleOk = /专题服务/.test(await page.title());
  const tabs = ['全球服务机构概况', '服务机构产业分布', '服务机构区域分布', '服务机构技术能力', '深圳产业服务介绍'];
  let tabsOk = true;
  for (const t of tabs) {
    if (!(await page.getByRole('tab', { name: t, exact: true }).count())) tabsOk = false;
  }
  gates.push({
    id: 'G1-login-deeplink',
    pass: urlOk && titleOk && tabsOk,
    detail: { url: page.url(), title: await page.title(), tabsOk },
    screenshot: await shot('overview'),
  });

  // 概况 KPI / 三区块
  const kpi = {
    global_count: await hasText(page, /全球机构约数/),
    new_this_year: await hasText(page, /本年新增/),
    stage_sum: await hasText(page, /环节合计/),
    cover_industry_case_text: await hasText(page, /覆盖产业领域数/),
  };
  const blocks = {
    qty: await hasHeading(page, '数量分析 · 历年总量趋势'),
    type: await hasHeading(page, '类型分析 · 机构类型占比'),
    scale: await hasHeading(page, '规模分析 · 人员规模分布'),
    scale_empty: await hasText(page, /概况实包无人员规模四档|保持空态/),
    chart_visible: (await page.locator('canvas, svg, .echarts-for-react, [_echarts_instance_]').count()) > 0,
  };
  gates.push({
    id: 'G2-overview-kpi-blocks',
    pass: kpi.global_count && kpi.new_this_year && blocks.qty && blocks.type && blocks.scale,
    stable_visible: {
      kpi_labels: ['全球机构约数', '本年新增机构', '环节合计（可重复计）'],
      block_titles: true,
      qty_type_charts: blocks.chart_visible,
    },
    honest_empty: {
      scale_staff_bins: blocks.scale_empty,
      note: '规模四档本包络无字段 → 诚实空文案可见',
    },
    d1_note: '用例「覆盖产业领域数」现场为「环节合计（可重复计）」',
    detail: { kpi, blocks },
    screenshot: await shot('overview-kpi'),
  });

  // 筛选
  const indPh = await page.locator('input[placeholder="全部产业"]').count();
  const chain = page
    .locator('.arco-select-view')
    .filter({ has: page.locator('input[placeholder="全部产业链"]') })
    .first();
  const chainDisabled = (await chain.count())
    ? await chain.evaluate((el) => el.className.includes('disabled'))
    : false;
  await pickIndustry(page, '新一代信息技术');
  const chainAfter = page
    .locator('.arco-select-view')
    .filter({ has: page.locator('input[placeholder="全部产业链"]') })
    .first();
  const chainUnlocked = (await chainAfter.count())
    ? !(await chainAfter.evaluate((el) => el.className.includes('disabled')))
    : false;
  gates.push({
    id: 'G3-filter-industry-chain',
    pass: indPh === 1 && chainDisabled && chainUnlocked,
    stable_visible: { industry_select: true, chain_initial_disabled: chainDisabled, chain_unlock_after_pick: chainUnlocked },
    honest_empty: {},
    detail: { indPh, chainDisabled, chainUnlocked },
    screenshot: await shot('filter'),
  });

  // 产业分布
  await page.getByRole('tab', { name: '服务机构产业分布', exact: true }).click();
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const indDist = {
    h1: await hasHeading(page, '服务机构产业分布'),
    six_type: await hasHeading(page, /类型分析 · 六类服务分布/),
    stage: await hasHeading(page, /产业链全景|环节服务分布/),
    heat: await hasHeading(page, /领域.*环节热力|全产业总览/),
    stage_empty: await hasText(page, /暂无环节分布/),
    heat_empty: await hasText(page, /无领域.?环节矩阵|保持空态|不画演示热力/),
    six_kpi: await hasText(page, /六类合计/),
  };
  gates.push({
    id: 'G4-industry-distribution',
    pass: indDist.h1 && indDist.six_type,
    stable_visible: { page_shell: true, six_type_block: indDist.six_type, six_type_kpi: indDist.six_kpi },
    honest_empty: { stage_distribution: indDist.stage_empty, heatmap: indDist.heat_empty },
    detail: indDist,
    screenshot: await shot('industry'),
  });

  // 区域
  await page.getByRole('tab', { name: '服务机构区域分布', exact: true }).click();
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const region = {
    h1: await hasHeading(page, '服务机构区域分布'),
    global_view: await hasText(page, /^全球视图$/),
    china_view: await hasText(page, /^全国视图$/),
    rank: await hasHeading(page, /省级行政区排行/),
    no_coord: await hasText(page, /无坐标|不填 Demo|假点/),
    has_marker: (await page.locator('.leaflet-marker-icon, svg circle').count()) > 0,
    guangdong: await hasText(page, /广东/),
  };
  gates.push({
    id: 'G5-region-map',
    pass: region.h1 && region.global_view && region.china_view && region.rank,
    stable_visible: { sub_views: true, province_rank: region.rank, rank_has_rows: region.guangdong },
    honest_empty: { map_dots: region.no_coord || !region.has_marker },
    d1_note: '用例「全球分布/全国分布」现场为「全球视图/全国视图」',
    detail: region,
    screenshot: await shot('region'),
  });

  // 技术能力
  await page.getByRole('tab', { name: '服务机构技术能力', exact: true }).click();
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const cap = {
    h1: await hasHeading(page, '服务机构技术能力'),
    equal_weight: await hasText(page, /固定五维等权|五维等权|门户不可调权/),
    empty_rank: await hasText(page, /暂无技术力入榜机构|暂无覆盖机构入榜|不凑满 30/),
    has_rows: await hasText(page, /加入对比篮/),
  };
  gates.push({
    id: 'G6-capability-rank',
    pass: cap.h1 && cap.equal_weight,
    stable_visible: { page_shell: true, equal_weight_copy: cap.equal_weight, empty_copy: cap.empty_rank },
    honest_empty: { tech_rank_list: cap.empty_rank && !cap.has_rows },
    ticket_hint: 'Q060 / Q-SVCCHAIN-01 / ENV-SVC-PORTAL-TECH-RANK-EMPTY',
    detail: cap,
    screenshot: await shot('capability'),
  });

  // 深圳
  await page.getByRole('tab', { name: '深圳产业服务介绍', exact: true }).click();
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const sz = {
    h1: await hasHeading(page, /深圳产业服务介绍/),
    kpi_sz: await hasText(page, /深圳机构约数|深圳服务机构/),
    block_trend: await hasHeading(page, /产业服务机构数量|历年趋势/),
    block_type: await hasHeading(page, /产业机构类型统计/),
    block_stage: await hasHeading(page, /深圳产业链环节分布|环节分布/),
    block_region: await hasHeading(page, /产业机构区域分布/),
    key_org: await hasHeading(page, '重点产业服务机构'),
    key_empty: await hasText(page, /暂无重点机构/),
    trend_empty: await hasText(page, /暂无深圳历年|不展示折线/),
    type_empty: await hasText(page, /无类型分布矩阵|内容暂无/),
  };
  gates.push({
    id: 'G7-shenzhen',
    pass: Boolean(sz.block_trend && sz.key_org),
    stable_visible: {
      four_section_titles: sz.block_trend && sz.block_type && sz.block_stage && sz.block_region,
      key_org_heading: sz.key_org,
      kpi_shell: sz.kpi_sz,
    },
    honest_empty: {
      key_org_wall: sz.key_empty,
      trend_series: sz.trend_empty,
      type_matrix: sz.type_empty,
    },
    ticket_hint: 'ENV-SVC-PORTAL-KEY-ORG-EMPTY / Q-SVC-010',
    detail: sz,
    screenshot: await shot('shenzhen'),
  });

  // 门户无异步「开始分析」——闸门 N/A pass
  gates.push({
    id: 'G8-no-async-analysis',
    pass: true,
    detail: { note: '本页无「开始分析」异步任务；历史结果依赖不适用' },
  });

  const allPass = gates.every((g) => g.pass);
  const report = {
    entry_id: 'svc-portal',
    surveyed_at: new Date().toISOString(),
    base_url: baseUrl,
    route: '/service-portal → /service-portal/overview',
    overall: allPass ? 'pass' : 'fail',
    method: 'headless chromium via _env-gate-probe.mjs (no IDE browser)',
    gates,
    summary: {
      stable_for_gold: [
        '路由/页头/五 Tab',
        '筛选产业→链解锁',
        '概况 KPI 三标签（as-built 文案）+ 三区块标题 + 数量/类型图',
        '产业分布壳 + 六类服务区（有数）',
        '区域全球/全国视图 + 省级排行（有数）',
        '技术能力页壳 + 等权口径（榜单诚实空）',
        '深圳四区标题 + 重点机构标题（墙诚实空）',
      ],
      honest_empty: [
        '概况·人员规模四档',
        '产业分布·环节分布 / 领域×环节热力',
        '区域·地图圆点（无坐标）',
        '技术能力·入榜列表',
        '深圳·历年折线 / 类型矩阵 / 重点机构墙',
      ],
      not_for_gold: [
        '环节下钻开抽屉',
        '地图圆点点选联动',
        '金银铜配色（需非空榜）',
        '重点机构抽屉 / 带参直达',
        '无映射产业空态（十五集群均有链）',
      ],
    },
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ overall: report.overall, gates: gates.map((g) => ({ id: g.id, pass: g.pass })) }, null, 2));
} finally {
  await browser.close();
}
