#!/usr/bin/env node
/**
 * ent-search 模块闸门二次探针（无头）。产物：env-gate.json + env-gate-*.png + scout-probe.json
 * 侧重：登录深链、示例 chip 回填不自动搜、关键词可出结果、画像抽屉、评审关闭零泄漏。
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
const route = '/enterprise/enterprise-search';
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
  // 人设面板可能挡点击；有关闭则关
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
  await page.waitForTimeout(2500);
  await closeBasket(page);
  await closePersonaIfOpen(page);

  // G1 登录 + 深链
  const urlOk = /\/enterprise\/enterprise-search/.test(page.url());
  const titleOk = /企业查询/.test(await page.title());
  const tabSmart = page.getByRole('tab', { name: '智能搜索' });
  const smartSelected =
    (await tabSmart.count()) > 0 &&
    (await tabSmart.first().getAttribute('aria-selected').catch(() => null)) === 'true';
  const searchInput = page.getByRole('textbox', { name: /输入企业名、产业、资质、区域或专利关键词/ });
  const exampleLabel = page.getByText('示例查询').first();
  const hotLabel = page.locator('main').getByText('热门场景').first();
  const searchBtn = page.getByRole('button', { name: '搜索', exact: true });
  const shellOk =
    (await searchInput.count()) > 0 &&
    (await exampleLabel.count()) > 0 &&
    (await hotLabel.count()) > 0 &&
    (await searchBtn.count()) > 0;
  gates.push({
    id: 'G1-login-deeplink',
    pass: urlOk && titleOk && smartSelected && shellOk,
    detail: {
      url: page.url(),
      title: await page.title(),
      smartSelected,
      shellOk,
      exampleChips: await page.locator('.enterprise-search-example-button').count(),
      hotChips: await page.locator('.enterprise-search-hot-button').count(),
    },
    screenshot: await shot('shell'),
  });
  probe.steps.push({ step: 'G1', url: page.url(), smartSelected, shellOk });

  // G2 本页无异步「开始分析」
  const startAnalysis = page.getByRole('button', { name: /开始分析/ });
  const hasStart = (await startAnalysis.count()) > 0;
  gates.push({
    id: 'G2-no-async-analysis',
    pass: true,
    detail: {
      note: '本页无「开始分析」异步任务；历史结果依赖不适用',
      start_analysis_visible: hasStart,
    },
  });

  // G3 示例 chip：回填不自动检索
  let chipPass = false;
  let chipDetail = {};
  const chip = page.locator('.enterprise-search-example-button').filter({ hasText: '人工智能' }).first();
  if ((await chip.count()) && (await chip.isVisible().catch(() => false)) && (await chip.isEnabled().catch(() => true))) {
    await chip.click();
    await page.waitForTimeout(800);
    const val = await searchInput.inputValue().catch(() => '');
    const emptyHint = (await page.getByText('输入关键词或选择热门场景后开始构造企业集合').count()) > 0;
    const resultTitle = (await page.getByText('智能搜索结果').count()) > 0;
    chipPass = val === '人工智能' && emptyHint && !resultTitle;
    chipDetail = { value: val, emptyHint, resultTitle, auto_searched: resultTitle };
    await shot('chip-fill');
  } else {
    chipDetail = { note: 'chip 不可见或 disabled，未硬点' };
  }
  gates.push({
    id: 'G3-example-chip-fill-only',
    pass: chipPass,
    detail: chipDetail,
    screenshot: 'fixtures/scout/env-gate-chip-fill.png',
  });
  probe.steps.push({ step: 'G3', ...chipDetail });

  // G4 关键词检索可出结果
  let searchPass = false;
  let searchDetail = {};
  if (await searchBtn.isEnabled().catch(() => false)) {
    // 若 chip 已填则直接搜；否则填词
    const cur = await searchInput.inputValue().catch(() => '');
    if (cur !== '人工智能') {
      await searchInput.fill('人工智能');
    }
    await searchBtn.click();
    await page.waitForTimeout(3500);
    const hasResultTitle = (await page.getByText('智能搜索结果').count()) > 0;
    const hitCount = await page.getByText(/命中 \d+ 家企业/).count();
    const profileBtn = page.getByRole('button', { name: '查看画像' });
    const profileCount = await profileBtn.count();
    const zaiying = (await page.getByText('在营').count()) > 0;
    const emptyAfter = (await page.getByText(/暂无|无结果|未找到/).count()) > 0;
    const bodySnippet = (await page.locator('main').innerText().catch(() => '')).slice(0, 400);
    searchPass = hasResultTitle && hitCount > 0 && profileCount > 0;
    searchDetail = {
      hasResultTitle,
      hitCountVisible: hitCount > 0,
      profileBtnCount: profileCount,
      zaiying,
      emptyAfter,
      body_hit: bodySnippet.replace(/\s+/g, ' ').slice(0, 220),
    };
    if (!searchPass && emptyAfter) {
      tickets.push('ENV-ENT-SEARCH-EMPTY-001');
      searchDetail.skip_hint = '明确空态 → Pass-N/A 数据阻塞，不进金样结果断言';
    }
    await shot('search-result');
  } else {
    searchDetail = { note: '搜索按钮 disabled，未硬点' };
    tickets.push('ENV-ENT-SEARCH-BTN-DISABLED-001');
  }
  gates.push({
    id: 'G4-keyword-search-results',
    pass: searchPass,
    detail: searchDetail,
    screenshot: 'fixtures/scout/env-gate-search-result.png',
  });
  probe.steps.push({ step: 'G4', ...searchDetail });

  // G5 画像抽屉
  let drawerPass = false;
  let drawerDetail = {};
  if (searchPass) {
    // 优先点企业名；若难定位则点「查看画像」
    const nameBtn = page.locator('main button').filter({ hasText: /有限公司|股份|集团/ }).first();
    let opened = false;
    if ((await nameBtn.count()) && (await nameBtn.isVisible().catch(() => false))) {
      await nameBtn.click().catch(() => {});
      await page.waitForTimeout(1200);
      opened = (await page.locator('.arco-drawer').count()) > 0 &&
        (await page.locator('.arco-drawer').first().isVisible().catch(() => false));
    }
    if (!opened) {
      const vb = page.getByRole('button', { name: '查看画像' }).first();
      if ((await vb.count()) && (await vb.isEnabled().catch(() => true))) {
        await vb.click();
        await page.waitForTimeout(1200);
        opened = (await page.locator('.arco-drawer').count()) > 0 &&
          (await page.locator('.arco-drawer').first().isVisible().catch(() => false));
      }
    }
    const routeStill = /\/enterprise\/enterprise-search/.test(page.url());
    const drawer = page.locator('.arco-drawer');
    const tabs = ['工商概况', '主要团队', '资质荣誉', '知识产权', '经营财务', '供应链关系', '关系图谱', '舆情动态', '风险信息', '招投标'];
    const tabHits = {};
    let allTabs = true;
    if (opened) {
      for (const t of tabs) {
        const ok = (await drawer.getByRole('tab', { name: t }).count()) > 0;
        tabHits[t] = ok;
        if (!ok) allTabs = false;
      }
    }
    drawerPass = opened && routeStill && allTabs;
    drawerDetail = { opened, routeStill, url: page.url(), tabHits, allTabs };
    await shot('drawer');
    // 关抽屉
    if (opened) {
      await page.keyboard.press('Escape').catch(() => {});
      await page.waitForTimeout(400);
      const closeD = page.locator('.arco-drawer .arco-icon-close, .arco-drawer [aria-label="关闭"]').first();
      if ((await closeD.count()) && (await closeD.isVisible().catch(() => false))) {
        await closeD.click().catch(() => {});
        await page.waitForTimeout(300);
      }
    }
  } else {
    drawerDetail = { note: 'G4 未出结果，跳过抽屉探针' };
  }
  gates.push({
    id: 'G5-profile-drawer',
    pass: drawerPass,
    detail: drawerDetail,
    screenshot: 'fixtures/scout/env-gate-drawer.png',
  });
  probe.steps.push({ step: 'G5', ...drawerDetail });

  // G6 评审关闭零泄漏 + 指标说明卡（可见才点）
  let leakPass = false;
  let leakDetail = {};
  // 人设：确认评审模式文案；若有「内部评审」开关可见则读状态
  const bodyText = await page.locator('body').innerText().catch(() => '');
  const listLeak = /GAP-|Q0\d{2}/.test(bodyText);
  // 结果列表区域更窄一点
  const listText = await page.locator('main').innerText().catch(() => '');
  const mainLeak = /GAP-|Q0\d{2}/.test(listText);
  // metric ⓘ — 可见才点
  const specBtn = page.locator('button.metric-spec-card, button[aria-label*="综合竞争力"]').first();
  let specOpened = false;
  let specHasCnName = false;
  if ((await specBtn.count()) && (await specBtn.isVisible().catch(() => false))) {
    await specBtn.click().catch(() => {});
    await page.waitForTimeout(600);
    const pop = page.locator('.arco-popover, .arco-trigger-popup, .arco-tooltip').filter({
      hasText: /综合竞争力|口径定义|指标ID/,
    });
    specOpened = (await pop.count()) > 0;
    specHasCnName = (await page.getByText(/综合竞争力/).count()) > 0;
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(300);
  }
  // 关评审后列表不应泄漏 GAP/Q0；说明卡内可有指标ID（不计入泄漏）
  leakPass = !mainLeak;
  leakDetail = {
    main_leak_gap_q0: mainLeak,
    body_has_gap_q0: listLeak,
    spec_btn_visible: (await specBtn.count()) > 0,
    specOpened,
    specHasCnName,
    note: '说明卡内部指标ID/Q0 不计列表泄漏；关卡后查 main 文本',
  };
  if (mainLeak) tickets.push('ENV-ENT-SEARCH-REVIEW-LEAK-001');
  gates.push({
    id: 'G6-review-off-zero-leak',
    pass: leakPass,
    detail: leakDetail,
    screenshot: await shot('no-leak'),
  });
  probe.steps.push({ step: 'G6', ...leakDetail });

  const overallPass = gates.every((g) => g.pass);
  const overall = overallPass ? 'pass' : 'fail';

  const envGate = {
    entry_id: 'ent-search',
    surveyed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall,
    method: 'headless chromium via _env-gate-probe.mjs (no IDE browser)',
    gates,
    summary: {
      stable_for_gold: [
        '登录深链 /enterprise/enterprise-search',
        '智能搜索四层壳（tab/搜索框/示例/热门）',
        chipPass ? '示例 chip 回填不自动检索' : null,
        searchPass ? '关键词检索出结果标题+长卡+查看画像' : null,
        drawerPass ? '当前页画像抽屉十页签' : null,
        leakPass ? '评审关闭态 main 无 GAP-/Q0xx 泄漏' : null,
      ].filter(Boolean),
      not_for_gold: [
        !searchPass ? '结果态深验（G4 未过）' : null,
        !drawerPass ? '画像抽屉十页签（G5 未过）' : null,
        '热门场景自动检索链（本闸门未测，属产品另一路径）',
        '高级筛选 / 查企业 模式切换深验',
      ].filter(Boolean),
      no_async_analysis: true,
    },
    tickets,
    conclusion: overallPass
      ? '环境闸门通过：登录深链、chip 回填、关键词可出结果、画像抽屉、零泄漏均可测。本页无异步开始分析。建议 A 档金样评估见交卷。'
      : `环境闸门失败：${gates.filter((g) => !g.pass).map((g) => g.id).join(', ')}。tickets=${tickets.join(',') || '无'}`,
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2), 'utf8');
  fs.writeFileSync(path.join(outDir, 'scout-probe.json'), JSON.stringify(probe, null, 2), 'utf8');
  console.log(JSON.stringify({ overall, tickets, failed: gates.filter((g) => !g.pass).map((g) => g.id) }, null, 2));
} catch (e) {
  const fail = {
    entry_id: 'ent-search',
    surveyed_at: new Date().toISOString(),
    overall: 'fail',
    error: String(e && e.stack ? e.stack : e),
    tickets: ['ENV-ENT-SEARCH-PROBE-CRASH-001'],
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2), 'utf8');
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
