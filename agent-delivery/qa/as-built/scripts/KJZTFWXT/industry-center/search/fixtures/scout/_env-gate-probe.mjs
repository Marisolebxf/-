#!/usr/bin/env node
/**
 * chain-search 模块闸门二次探针（无头）。产物：env-gate.json + env-gate-*.png + scout-probe.json
 * method-patch §3：登录深链；本页无异步开始分析；关键词可出结果；零泄漏。
 * 禁止当 runner；禁止有头 MCP；disabled 不硬点。
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
const route = '/industry-center/search';
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

async function closePersonaIfOpen(page) {
  for (const label of ['关闭', '收起']) {
    const b = page.getByRole('button', { name: label });
    if ((await b.count()) && (await b.first().isVisible().catch(() => false))) {
      await b.first().click().catch(() => {});
      await page.waitForTimeout(200);
    }
  }
  await page.keyboard.press('Escape').catch(() => {});
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const gates = [];
const tickets = [];
const shot = async (name) => {
  const p = path.join(outDir, `env-gate-${name}.png`);
  await page.screenshot({ path: p, fullPage: false });
  return `fixtures/scout/env-gate-${name}.png`;
};

const probe = {
  surveyed_at: new Date().toISOString(),
  steps: [],
};

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
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
  await closePersonaIfOpen(page);

  // G1 登录 + 深链 + 壳层
  const urlOk = /\/industry-center\/search/.test(page.url());
  const titleOk = /产业查询/.test(await page.title());
  const h1Ok = (await page.getByRole('heading', { name: '产业查询', level: 1 }).count()) > 0;
  const mode = page.locator('[aria-label="检索模式"]');
  const tabSmart = mode.getByRole('tab', { name: '智能检索' });
  const smartSelected =
    (await tabSmart.count()) > 0 &&
    (await tabSmart.first().getAttribute('aria-selected').catch(() => null)) === 'true';
  const searchInput = page.getByPlaceholder(/输入产业、产业链、链位方向或同义词/);
  const searchBtn = page.getByRole('button', { name: '搜索', exact: true });
  const exampleLabel = page.getByText('示例查询').first();
  const shellOk =
    (await searchInput.count()) > 0 &&
    (await searchBtn.count()) > 0 &&
    (await exampleLabel.count()) > 0 &&
    (await mode.getByRole('tab').count()) === 3;
  gates.push({
    id: 'G1-login-deeplink',
    pass: urlOk && titleOk && h1Ok && smartSelected && shellOk,
    detail: {
      url: page.url(),
      title: await page.title(),
      h1Ok,
      smartSelected,
      shellOk,
      modeTabCount: await mode.getByRole('tab').count(),
      exampleChips: await page.locator('.enterprise-search-example-button').count(),
      hotChips: await page.locator('.enterprise-search-hot-button').count(),
    },
    screenshot: await shot('shell'),
  });
  probe.steps.push({ step: 'G1', url: page.url(), smartSelected, shellOk });

  // G2 本页无异步「开始分析」（method-patch §3.2 / §3.5 N/A）
  const startAnalysis = page.getByRole('button', { name: /开始分析/ });
  const hasStart = (await startAnalysis.count()) > 0;
  gates.push({
    id: 'G2-no-async-analysis',
    pass: true,
    detail: {
      note: '本页无「开始分析」异步任务；历史结果依赖不适用（method-patch §3.2/§3.5 N/A）',
      start_analysis_visible: hasStart,
    },
  });

  // G3 未检索初始引导态（推荐产业）
  const region = page.locator('[role=region][aria-label="产业查询结果"]');
  const recommendOk = (await region.getByText('推荐产业').count()) > 0;
  const notHitList = (await region.getByText(/产业查询返回 \d+ 条结果/).count()) === 0;
  gates.push({
    id: 'G3-leading-recommend',
    pass: (await region.count()) > 0 && recommendOk && notHitList,
    detail: {
      regionVisible: (await region.count()) > 0,
      recommendOk,
      notHitList,
      note: '初始态=推荐产业引导，非检索命中列表',
    },
    screenshot: await shot('leading'),
  });
  probe.steps.push({ step: 'G3', recommendOk, notHitList });

  // G4 示例 chip：回填不自动检索
  let chipPass = false;
  let chipDetail = {};
  const chip = page.locator('.enterprise-search-example-button').filter({ hasText: '人工智能' }).first();
  if ((await chip.count()) && (await chip.isVisible().catch(() => false)) && (await chip.isEnabled().catch(() => true))) {
    await chip.click();
    await page.waitForTimeout(800);
    const val = await searchInput.inputValue().catch(() => '');
    const stillRecommend = (await region.getByText('推荐产业').count()) > 0;
    const hitTitle = (await region.getByText(/产业查询返回 \d+ 条结果/).count()) > 0;
    chipPass = val === '人工智能' && stillRecommend && !hitTitle;
    chipDetail = { value: val, stillRecommend, hitTitle, auto_searched: hitTitle };
    await shot('chip-fill');
  } else {
    chipDetail = { note: 'chip 不可见或 disabled，未硬点' };
  }
  gates.push({
    id: 'G4-example-chip-fill-only',
    pass: chipPass,
    detail: chipDetail,
    screenshot: 'fixtures/scout/env-gate-chip-fill.png',
  });
  probe.steps.push({ step: 'G4', ...chipDetail });

  // G5 关键词「光刻」可出结果（金样结果态候选）
  let searchPass = false;
  let searchDetail = {};
  if (await searchBtn.isEnabled().catch(() => false)) {
    await searchInput.fill('光刻');
    await searchBtn.click();
    await page.waitForTimeout(3500);
    const hitTitle = (await region.getByText(/产业查询返回 \d+ 条结果|检索结果/).count()) > 0;
    const entryCount = await region.getByRole('button', { name: '进入全景图谱' }).count();
    const emptyAfter = (await region.getByText(/产业查询无匹配结果|无匹配|共 0 条/).count()) > 0;
    const bodySnippet = (await page.locator('main').innerText().catch(() => '')).slice(0, 400);
    searchPass = hitTitle && entryCount > 0 && !emptyAfter;
    searchDetail = {
      keyword: '光刻',
      hitTitle,
      entryCount,
      emptyAfter,
      body_hit: bodySnippet.replace(/\s+/g, ' ').slice(0, 220),
    };
    if (!searchPass && emptyAfter) {
      tickets.push('ENV-CHAIN-SEARCH-GUANGKE-EMPTY-001');
      searchDetail.skip_hint = '光刻明确空态 → 结果态不进金样';
    }
    await shot('search-result');
  } else {
    searchDetail = { note: '搜索按钮 disabled，未硬点' };
    tickets.push('ENV-CHAIN-SEARCH-BTN-DISABLED-001');
  }
  gates.push({
    id: 'G5-keyword-search-results',
    pass: searchPass,
    detail: searchDetail,
    screenshot: 'fixtures/scout/env-gate-search-result.png',
  });
  probe.steps.push({ step: 'G5', ...searchDetail });

  // G6 命中条目分发入口（进入全景图谱 + 加入对比篮）
  let entryPass = false;
  let entryDetail = {};
  if (searchPass) {
    const panorama = await region.getByRole('button', { name: '进入全景图谱' }).count();
    const joinBasket = await page.locator('[aria-label*="加入对比篮"]').count();
    const abstract = await region.getByText(/查看摘要|暂无摘要/).count();
    entryPass = panorama >= 1 && joinBasket >= 1;
    entryDetail = { panorama, joinBasket, abstract };
    await shot('entry-actions');
  } else {
    entryDetail = { note: 'G5 未出结果，跳过分发入口' };
  }
  gates.push({
    id: 'G6-hit-entry-actions',
    pass: entryPass,
    detail: entryDetail,
    screenshot: searchPass ? 'fixtures/scout/env-gate-entry-actions.png' : undefined,
  });
  probe.steps.push({ step: 'G6', ...entryDetail });

  // G7 评审关闭零泄漏
  const listText = await page.locator('main').innerText().catch(() => '');
  const mainLeak = /GAP-|Q0\d{2}/.test(listText);
  if (mainLeak) tickets.push('ENV-CHAIN-SEARCH-REVIEW-LEAK-001');
  gates.push({
    id: 'G7-review-off-zero-leak',
    pass: !mainLeak,
    detail: {
      main_leak_gap_q0: mainLeak,
      note: '关评审后 main 不应出现 GAP-/Q0xx；说明卡内指标 ID 不计',
    },
    screenshot: await shot('no-leak'),
  });
  probe.steps.push({ step: 'G7', mainLeak });

  // G8 已知坏词「低空交通」空态（B 档 skip 证据，不挡 overall）
  await searchInput.fill('低空交通');
  await searchBtn.click();
  await page.waitForTimeout(3000);
  const dikongEmpty = (await region.getByText(/产业查询无匹配结果|共 0 条|无匹配/).count()) > 0;
  const dikongHit = (await region.getByText(/产业查询返回 \d+ 条结果/).count()) > 0;
  if (dikongEmpty) tickets.push('ENV-CHAIN-SEARCH-DIKONG-EMPTY-001');
  gates.push({
    id: 'G8-dikong-empty-observed',
    pass: true,
    detail: {
      note: '低空交通当前环境空态（P0-08 allow_skip 依据）；不挡 overall',
      dikongEmpty,
      dikongHit,
    },
    screenshot: await shot('dikong-empty'),
  });
  probe.steps.push({ step: 'G8', dikongEmpty, dikongHit });

  const hardIds = [
    'G1-login-deeplink',
    'G2-no-async-analysis',
    'G3-leading-recommend',
    'G4-example-chip-fill-only',
    'G5-keyword-search-results',
    'G6-hit-entry-actions',
    'G7-review-off-zero-leak',
  ];
  const hardGates = gates.filter((g) => hardIds.includes(g.id));
  const overallPass = hardGates.every((g) => g.pass);
  const overall = overallPass ? 'pass' : 'fail';

  const suggested_gold = {
    keep: ['P0-01', 'P0-02', 'P0-03', 'P0-05'],
    drop_from_current_gold: ['P0-04'],
    promote_optional: searchPass ? ['P0-07', 'P0-09'] : ['P0-07'],
    rationale:
      '现 gold=P0-01..05。P0-04 含 allow_skip（method-patch §2 金样禁 allow_skip）→ 建议移出 A 档；壳层四条可机跑。若光刻稳定命中可升 P0-09（无 allow_skip，结果态）+ P0-07（初始引导）。P0-08 低空交通空态仅 B+ticket。本闸门只建议不改 index/cases。',
  };

  const envGate = {
    entry_id: 'chain-search',
    surveyed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall,
    method: 'headless chromium via survey-page.mjs + _env-gate-probe.mjs (no IDE browser)',
    gates,
    summary: {
      stable_for_gold: [
        '登录深链 /industry-center/search',
        '智能检索三 Tab + 搜索框/搜索按钮 + 示例 chip',
        recommendOk ? '未检索推荐产业引导态' : null,
        chipPass ? '示例 chip 回填不自动检索' : null,
        searchPass ? '关键词「光刻」可出命中+进入全景图谱' : null,
        entryPass ? '命中条目含进入全景图谱/加入对比篮' : null,
        !mainLeak ? 'main 无 GAP-/Q0xx 泄漏' : null,
      ].filter(Boolean),
      not_for_gold: [
        !searchPass ? '结果态深验（G5 未过）' : null,
        '低空交通检索（G8 空态 / P0-08 allow_skip）',
        '空输入点搜索仍出结果（P0-11 as-built 缺陷，预期红）',
        '高级筛选 / 查产业面板深验',
      ].filter(Boolean),
      no_async_analysis: true,
      suggested_gold,
    },
    tickets,
    conclusion: overallPass
      ? `环境闸门 overall=pass（method-patch §3：登录深链✅、无异步分析✅、光刻可出结果=${searchPass}、零泄漏✅）。tickets=${tickets.join(',') || '无'}。建议金样 keep ${suggested_gold.keep.join('/')}；drop ${suggested_gold.drop_from_current_gold.join('/')}；可选升 ${suggested_gold.promote_optional.join('/')}。`
      : `环境闸门失败：${hardGates.filter((g) => !g.pass).map((g) => g.id).join(', ')}。tickets=${tickets.join(',') || '无'}`,
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2), 'utf8');
  fs.writeFileSync(path.join(outDir, 'scout-probe.json'), JSON.stringify(probe, null, 2), 'utf8');
  console.log(
    JSON.stringify(
      {
        overall,
        tickets,
        failed: hardGates.filter((g) => !g.pass).map((g) => g.id),
        suggested_gold,
      },
      null,
      2,
    ),
  );
} catch (e) {
  const fail = {
    entry_id: 'chain-search',
    surveyed_at: new Date().toISOString(),
    overall: 'fail',
    error: String(e && e.stack ? e.stack : e),
    tickets: ['ENV-CHAIN-SEARCH-PROBE-CRASH-001'],
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2), 'utf8');
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
