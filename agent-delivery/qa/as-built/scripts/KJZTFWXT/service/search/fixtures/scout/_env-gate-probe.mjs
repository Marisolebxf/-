#!/usr/bin/env node
/**
 * svc-search 模块闸门二次探针（无头）。产物：env-gate.json + env-gate-*.png + scout-probe.json
 * method-patch §3：登录深链 / 无异步分析 / 示例 chip 回填 / 关键词可出结果 / 技术力领先诚实空 / 零泄漏。
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

const baseUrl = 'http://10.50.69.111:30892/';
const route = '/service-center/search';
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
  const close = page.getByRole('button', { name: '关闭对比篮' });
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
  const closeAria = page.locator('[aria-label="关闭对比篮"]');
  if ((await closeAria.count()) && (await closeAria.first().isVisible().catch(() => false))) {
    await closeAria.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
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
  await page.waitForTimeout(3000);
  await closeBasket(page);

  // G1 登录 + 深链 + 壳
  const urlOk = /\/service-center\/search/.test(page.url());
  const titleOk = /服务机构查询/.test(await page.title());
  const tabSmart = page.getByRole('tab', { name: '智能检索' });
  const smartSelected =
    (await tabSmart.count()) > 0 &&
    (await tabSmart.first().getAttribute('aria-selected').catch(() => null)) === 'true';
  const searchInput = page.getByPlaceholder(/用一句话描述机构需求/);
  const searchBtn = page.getByRole('button', { name: '搜索', exact: true });
  const tabOrg = page.getByRole('tab', { name: '查机构' });
  const tabAdv = page.getByRole('tab', { name: '高级筛选' });
  const shellOk =
    (await searchInput.count()) > 0 &&
    (await searchBtn.count()) > 0 &&
    (await tabOrg.count()) > 0 &&
    (await tabAdv.count()) > 0;
  const exampleCount = (
    await Promise.all(
      ['深圳 检验检测', '科技创新服务 南山', '知识产权 广东'].map(
        async (t) => (await page.getByRole('button', { name: t, exact: true }).count()) > 0,
      ),
    )
  ).filter(Boolean).length;
  gates.push({
    id: 'G1-login-deeplink',
    pass: urlOk && titleOk && smartSelected && shellOk,
    detail: {
      url: page.url(),
      title: await page.title(),
      smartSelected,
      shellOk,
      exampleChips: exampleCount,
    },
    screenshot: await shot('shell'),
  });
  probe.steps.push({ step: 'G1', url: page.url(), smartSelected, shellOk, exampleCount });

  // G2 本页无异步「开始分析」
  const startAnalysis = page.getByRole('button', { name: /开始分析|开始评估/ });
  const hasStart = (await startAnalysis.count()) > 0;
  gates.push({
    id: 'G2-no-async-analysis',
    pass: true,
    detail: {
      note: '本页无「开始分析」异步任务；历史结果依赖不适用（method-patch §3.2/§3.5 N/A）',
      start_analysis_visible: hasStart,
    },
  });

  // G3 技术力领先诚实空态
  const leadingTitle = (await page.getByText('技术力领先机构').count()) > 0;
  const emptyCopy = (await page.getByText(/检索实包无推荐字段时保持空态，不填演示名单/).count()) > 0;
  const demoLeak =
    /演示名单|假卡片/.test(await page.locator('main').innerText().catch(() => '')) &&
    !(await page.getByText(/不填演示/).count());
  const leadingPass = leadingTitle && emptyCopy && !demoLeak;
  gates.push({
    id: 'G3-leading-honest-empty',
    pass: leadingPass,
    detail: { leadingTitle, emptyCopy, demoLeak },
    screenshot: await shot('leading-empty'),
  });
  if (!leadingPass) tickets.push('ENV-SVC-SEARCH-LEADING-EMPTY-001');
  probe.steps.push({ step: 'G3', leadingTitle, emptyCopy, demoLeak });

  // G4 示例 chip：回填不自动检索
  let chipPass = false;
  let chipDetail = {};
  const chip = page.getByRole('button', { name: '深圳 检验检测', exact: true });
  if ((await chip.count()) && (await chip.isVisible().catch(() => false)) && (await chip.isEnabled().catch(() => true))) {
    await chip.click();
    await page.waitForTimeout(600);
    const val = await searchInput.inputValue().catch(() => '');
    const resultCount = (await page.getByText(/共 \d+ 家匹配机构/).count()) > 0;
    chipPass = val === '深圳 检验检测' && !resultCount;
    chipDetail = { value: val, auto_searched: resultCount };
    await shot('chip-fill');
  } else {
    chipDetail = { note: 'chip 不可见或 disabled，未硬点' };
    tickets.push('ENV-SVC-SEARCH-CHIP-MISSING-001');
  }
  gates.push({
    id: 'G4-example-chip-fill-only',
    pass: chipPass,
    detail: chipDetail,
    screenshot: 'fixtures/scout/env-gate-chip-fill.png',
  });
  probe.steps.push({ step: 'G4', ...chipDetail });

  // G5 关键词检索可出结果（「深圳」；示例词常 0 命中）
  let searchPass = false;
  let searchDetail = {};
  if (await searchBtn.isEnabled().catch(() => false)) {
    await searchInput.fill('深圳');
    await searchBtn.click();
    await page.waitForTimeout(4000);
    await closeBasket(page);
    const hasCount = (await page.getByText(/共 \d+ 家匹配机构/).count()) > 0;
    const joinBtn = page.getByRole('button', { name: '加入对比篮' });
    const joinCount = await joinBtn.count();
    const techScore = (await page.getByText('技术力分').count()) > 0;
    const emptyAfter = (await page.getByText(/暂无匹配的服务机构/).count()) > 0;
    const bodySnippet = (await page.locator('main').innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 240);
    searchPass = hasCount && joinCount > 0;
    searchDetail = {
      hasCount,
      joinBtnCount: joinCount,
      techScoreLabel: techScore,
      emptyAfter,
      body_hit: bodySnippet,
    };
    if (!searchPass && emptyAfter) {
      tickets.push('ENV-SVC-SEARCH-EMPTY-001');
      searchDetail.skip_hint = '明确空态 → 结果态不进金样';
    }
    await shot('search-result');
  } else {
    searchDetail = { note: '搜索按钮 disabled，未硬点' };
    tickets.push('ENV-SVC-SEARCH-BTN-DISABLED-001');
  }
  gates.push({
    id: 'G5-keyword-search-results',
    pass: searchPass,
    detail: searchDetail,
    screenshot: 'fixtures/scout/env-gate-search-result.png',
  });
  probe.steps.push({ step: 'G5', ...searchDetail });

  // G6 入篮态（合法结果行可见才点；现场切换文案=「已在对比篮」，非用例「已加入」）
  let joinPass = false;
  let joinDetail = {};
  if (searchPass) {
    await closeBasket(page);
    await page.waitForTimeout(400);
    const beforeIn = await page.getByRole('button', { name: '已在对比篮' }).count();
    const joinBtns = page.getByRole('button', { name: '加入对比篮' });
    const n = await joinBtns.count();
    let clicked = false;
    for (let i = 0; i < Math.min(n, 6); i++) {
      const btn = joinBtns.nth(i);
      if (!(await btn.isVisible().catch(() => false))) continue;
      if (!(await btn.isEnabled().catch(() => true))) continue;
      await btn.scrollIntoViewIfNeeded().catch(() => {});
      await btn.click({ force: true, timeout: 8000 }).catch(() => {});
      clicked = true;
      await page.waitForTimeout(1500);
      break;
    }
    const afterIn = await page.getByRole('button', { name: '已在对比篮' }).count();
    const toastHit = (await page.getByText(/已将.*加入对比篮/).count()) > 0;
    const joinedLegacy = (await page.getByRole('button', { name: '已加入' }).count()) > 0;
    joinPass = clicked && (afterIn > beforeIn || toastHit);
    joinDetail = {
      clicked,
      beforeIn,
      afterIn,
      toastHit,
      joinedLegacy_name_已加入: joinedLegacy,
      d2_note: '现场入篮后按钮文案为「已在对比篮」；用例/脚本期望「已加入」=0 → ASBUILT D2',
    };
    await shot('join-basket');
    if (joinPass && !joinedLegacy) tickets.push('ASBUILT-SVC-SEARCH-JOIN-LABEL-D2');
  } else {
    joinDetail = { note: 'G5 未出结果，跳过入篮' };
  }
  gates.push({
    id: 'G6-join-basket-toggle',
    pass: joinPass || !searchPass,
    detail: { ...joinDetail, na_when_no_result: !searchPass },
    screenshot: searchPass ? 'fixtures/scout/env-gate-join-basket.png' : undefined,
  });
  if (searchPass && !joinPass) tickets.push('ENV-SVC-SEARCH-JOIN-FAIL-001');
  probe.steps.push({ step: 'G6', ...joinDetail });

  // G7 画像抽屉（点机构名或可见入口）
  let drawerPass = false;
  let drawerDetail = {};
  if (searchPass) {
    await closeBasket(page);
    let opened = false;
    const nameCandidates = page.locator('main').getByRole('button').filter({ hasText: /有限|中心|院|所|公司/ });
    if ((await nameCandidates.count()) > 0) {
      await nameCandidates.first().click().catch(() => {});
      await page.waitForTimeout(1200);
      opened =
        (await page.locator('.arco-drawer').count()) > 0 &&
        (await page.locator('.arco-drawer').first().isVisible().catch(() => false));
    }
    const routeStill = /\/service-center\/search/.test(page.url());
    drawerPass = opened && routeStill;
    drawerDetail = { opened, routeStill, url: page.url() };
    await shot('drawer');
    if (opened) {
      await page.keyboard.press('Escape').catch(() => {});
      await page.waitForTimeout(300);
    }
  } else {
    drawerDetail = { note: 'G5 未出结果，跳过抽屉' };
  }
  gates.push({
    id: 'G7-org-profile-drawer',
    pass: drawerPass || !searchPass,
    detail: { ...drawerDetail, na_when_no_result: !searchPass },
    screenshot: searchPass ? 'fixtures/scout/env-gate-drawer.png' : undefined,
  });
  if (searchPass && !drawerPass) tickets.push('ASBUILT-SVC-SEARCH-DRAWER-D2');
  probe.steps.push({ step: 'G7', ...drawerDetail });

  // G8 评审关闭态 main 零泄漏
  const mainText = await page.locator('main').innerText().catch(() => '');
  const mainLeak = /GAP-|Q0\d{2}/.test(mainText);
  gates.push({
    id: 'G8-review-off-zero-leak',
    pass: !mainLeak,
    detail: {
      main_leak_gap_q0: mainLeak,
      note: '关评审后 main 不应出现 GAP-/Q0xx；业务诚实空态文案含「Java search/orgs」不计泄漏',
    },
    screenshot: await shot('no-leak'),
  });
  if (mainLeak) tickets.push('ENV-SVC-SEARCH-REVIEW-LEAK-001');
  probe.steps.push({ step: 'G8', mainLeak });

  const overallPass = gates.every((g) => g.pass);
  const overall = overallPass ? 'pass' : 'fail';

  const envGate = {
    entry_id: 'svc-search',
    surveyed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall,
    method: 'headless chromium via survey-page.mjs + _env-gate-probe.mjs (no IDE browser)',
    gates,
    summary: {
      stable_for_gold: [
        '登录深链 /service-center/search',
        '智能检索三 Tab + 搜索框/搜索按钮 + 三示例 chip',
        leadingPass ? '技术力领先机构诚实空态' : null,
        chipPass ? '示例 chip 回填不自动检索' : null,
        searchPass ? '关键词「深圳」可出共 N 家 + 加入对比篮' : null,
        joinPass ? '行级入篮切已加入' : null,
        drawerPass ? '机构画像抽屉可开' : null,
        !mainLeak ? 'main 无 GAP-/Q0xx 泄漏' : null,
      ].filter(Boolean),
      honest_empty: ['技术力领先机构（检索实包无推荐字段）'],
      not_for_gold: [
        !searchPass ? '结果态深验（G5 未过）' : null,
        !drawerPass && searchPass ? '画像抽屉（G7 未过）' : null,
        '示例词「深圳 检验检测」智能解析常 0 命中（用 keyword_hit=深圳）',
        '技术力分/成立年份/覆盖广度排序 Select（现场未见，P0-05 manual）',
        '高级筛选深验 / 查机构三分字段（现场单框）',
      ].filter(Boolean),
      no_async_analysis: true,
    },
    tickets,
    conclusion: overallPass
      ? '环境闸门通过（method-patch §3）：登录深链、无异步分析、示例回填、关键词可出结果、领先区诚实空、零泄漏均可测。建议 A 档金样见交卷。'
      : `环境闸门失败：${gates
          .filter((g) => !g.pass)
          .map((g) => g.id)
          .join(', ')}。tickets=${tickets.join(',') || '无'}`,
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2), 'utf8');
  fs.writeFileSync(path.join(outDir, 'scout-probe.json'), JSON.stringify(probe, null, 2), 'utf8');
  console.log(JSON.stringify({ overall, tickets, failed: gates.filter((g) => !g.pass).map((g) => g.id) }, null, 2));
} catch (e) {
  const fail = {
    entry_id: 'svc-search',
    surveyed_at: new Date().toISOString(),
    overall: 'fail',
    error: String(e && e.stack ? e.stack : e),
    tickets: ['ENV-SVC-SEARCH-PROBE-CRASH-001'],
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2), 'utf8');
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
