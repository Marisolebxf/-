#!/usr/bin/env node
/**
 * shell-compare-basket 模块闸门二次探针（无头）。
 * §3：登录深链 → 打开对比篮浮层 → 壳层控件 / 无异步「开始分析」/ 勾选→发起分析浮层。
 * 产物：env-gate.json + env-gate-*.png + scout-env-gate-probe.json
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
const route = '/enterprise/search';
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

async function openBasket(page) {
  const dock = page.getByRole('button', { name: /打开对比篮/ });
  if (await dock.count()) {
    await dock.first().click({ timeout: 8000 });
  } else {
    await page.getByRole('button', { name: /^对比篮$/ }).first().click({ timeout: 8000 });
  }
  await page.locator('.system-compare-panel').waitFor({ state: 'visible', timeout: 10000 });
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

const probe = { surveyed_at: new Date().toISOString(), steps: [] };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await ensureLogin(page);
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2500);

  const urlOk = /\/enterprise\/search/.test(page.url()) && !page.url().includes('/login');
  const title = await page.title();
  const retryBtn = page.getByRole('button', { name: /^重试$/ });
  const retryVisible = (await retryBtn.count()) > 0 && (await retryBtn.first().isVisible().catch(() => false));
  const bodySample = (await page.locator('body').innerText().catch(() => '')).slice(0, 400);
  const hostHas424 = /424|Failed to fetch|网络异常|加载失败/i.test(bodySample);
  gates.push({
    id: 'G1-login-deeplink',
    pass: urlOk,
    detail: {
      url: page.url(),
      title,
      retry_visible: retryVisible,
      host_error_hint: hostHas424,
      note: '路由入口 /enterprise/search；宿主页若见重试属宿主债，不挡篮壳闸门',
    },
    screenshot: await shot('shell'),
  });
  if (retryVisible || hostHas424) {
    tickets.push('ENV-SHELL-COMPARE-HOST-RETRY-001');
  }
  probe.steps.push({ step: 'deeplink', url: page.url(), title, retryVisible, hostHas424 });

  // G2 打开浮层
  let panelOpen = false;
  let openErr = null;
  try {
    await openBasket(page);
    panelOpen = await page.locator('.system-compare-panel').isVisible();
  } catch (e) {
    openErr = e.message;
  }
  const heading = page.getByRole('heading', { name: /对比篮 · 共\s*\d+\s*项/ });
  const headingOk = (await heading.count()) > 0;
  const stillOnSearch = /\/enterprise\/search/.test(page.url());
  gates.push({
    id: 'G2-open-basket-overlay',
    pass: panelOpen && headingOk && stillOnSearch,
    detail: {
      panelOpen,
      headingOk,
      stillOnSearch,
      url: page.url(),
      openErr,
    },
    screenshot: await shot('basket-open'),
  });
  probe.steps.push({ step: 'open', panelOpen, headingOk, stillOnSearch, openErr });

  const panel = page.locator('.system-compare-panel');
  const tabEnt = panel.locator('#compare-basket-tab-enterprise');
  const tabInd = panel.locator('#compare-basket-tab-industry');
  const tabOrg = panel.locator('#compare-basket-tab-service_org');
  const tabRegion = panel.locator('#compare-basket-tab-region');
  const tabsOk =
    (await tabEnt.count()) > 0 &&
    (await tabInd.count()) > 0 &&
    (await tabOrg.count()) > 0 &&
    (await tabRegion.count()) > 0;
  const entActive = /active/.test((await tabEnt.getAttribute('class').catch(() => '')) || '');
  const nameSearch = panel.getByPlaceholder('按企业名称搜索');
  const typeSelect = panel.getByText('全部企业类型').first();
  const launch = panel.getByRole('button', { name: '发起分析' });
  const cards = panel.locator('.ent-compare-item-card');
  const cardCount = await cards.count();
  const dock = page.getByRole('button', { name: /打开对比篮/ });
  const dockCount = await dock.count();
  gates.push({
    id: 'G3-basket-shell',
    pass: tabsOk && entActive && (await nameSearch.count()) > 0 && (await launch.count()) > 0 && cardCount >= 1,
    detail: {
      tabsOk,
      entActive,
      name_search: (await nameSearch.count()) > 0,
      type_select: (await typeSelect.count()) > 0,
      launch: (await launch.count()) > 0,
      cardCount,
      dockCount,
      note: '政策 Tab 现场缺失（as-built）；区域·开发中可见',
    },
    screenshot: await shot('basket-shell'),
  });
  if (cardCount < 1) tickets.push('ENV-SHELL-COMPARE-BASKET-EMPTY-001');
  probe.steps.push({ step: 'shell', tabsOk, entActive, cardCount, dockCount });

  // G4 本壳无异步「开始分析」；历史结果依赖不适用
  const startAnalysis = page.getByRole('button', { name: /^开始分析$/ });
  const startVisible =
    (await startAnalysis.count()) > 0 && (await startAnalysis.first().isVisible().catch(() => false));
  gates.push({
    id: 'G4-no-async-analysis',
    pass: !startVisible,
    detail: {
      start_analysis_visible: startVisible,
      note: '对比篮为分发壳：有「发起分析」任务选择，无异步工作区「开始分析」；历史结果依赖不适用',
    },
  });

  // G5 勾选 → 任务浮层（金样主路径前置）
  let modalOk = false;
  let modalText = '';
  let modalErr = null;
  try {
    const cancel = panel.getByRole('button', { name: '取消选择' });
    if ((await cancel.count()) && !(await cancel.isDisabled())) {
      await cancel.click().catch(() => {});
      await page.waitForTimeout(200);
    }
    const check = panel.locator('.ent-compare-item-card__check').first();
    if ((await check.count()) && cardCount >= 1) {
      await check.click({ timeout: 8000 });
      await page.waitForTimeout(300);
      const launchEnabled = !(await launch.isDisabled());
      if (launchEnabled) {
        await launch.click({ timeout: 8000 });
        const modal = page.locator('.arco-modal:visible').filter({ hasText: '选择分析任务' }).first();
        await modal.waitFor({ state: 'visible', timeout: 8000 });
        modalOk = true;
        modalText = (await modal.innerText()).slice(0, 500);
        const groups = {
          重点企业分析: modalText.includes('重点企业分析'),
          企业评估: modalText.includes('企业评估'),
          风险洞察: modalText.includes('风险洞察'),
          技术力评估: modalText.includes('技术力评估'),
        };
        gates.push({
          id: 'G5-launch-task-modal',
          pass: Object.values(groups).every(Boolean),
          detail: { groups, modal_snippet: modalText.slice(0, 200) },
          screenshot: await shot('task-modal'),
        });
        await modal.getByRole('button', { name: '取消' }).click({ timeout: 5000 }).catch(() => {});
      } else {
        gates.push({
          id: 'G5-launch-task-modal',
          pass: false,
          detail: { launchEnabled: false, cardCount },
        });
        tickets.push('ENV-SHELL-COMPARE-LAUNCH-DISABLED-001');
      }
    } else {
      gates.push({
        id: 'G5-launch-task-modal',
        pass: false,
        detail: { cardCount, check_missing: true },
      });
      tickets.push('ENV-SHELL-COMPARE-BASKET-EMPTY-001');
    }
  } catch (e) {
    modalErr = e.message;
    gates.push({
      id: 'G5-launch-task-modal',
      pass: false,
      detail: { modalErr },
      screenshot: await shot('task-modal-fail'),
    });
    tickets.push('ENV-SHELL-COMPARE-TASK-MODAL-001');
  }
  probe.steps.push({ step: 'modal', modalOk, modalErr });

  // G6 名称搜索控件可填（轻筛金样前置）
  let searchOk = false;
  try {
    await nameSearch.fill('___gate_probe___');
    await page.waitForTimeout(400);
    const val = await nameSearch.inputValue();
    searchOk = val.includes('gate_probe');
    await nameSearch.fill('');
    await page.waitForTimeout(200);
  } catch (e) {
    probe.steps.push({ step: 'search', err: e.message });
  }
  gates.push({
    id: 'G6-name-search-control',
    pass: searchOk,
    detail: { searchOk },
    screenshot: await shot('name-search'),
  });

  const overall = gates.every((g) => g.pass) ? 'pass' : 'fail';
  const envGate = {
    entry_id: 'shell-compare-basket',
    surveyed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall,
    method: 'headless chromium via survey-page.mjs + _env-gate-probe.mjs (no IDE browser)',
    gates,
    summary: {
      stable_for_gold: [
        '登录深链 /enterprise/search',
        '点对比篮/dock 展开 .system-compare-panel，路由不跳独立页',
        '四 Tab（企业/产业/服务机构/区域·开发中）+ 企业默认激活',
        '按企业名称搜索 + 全部企业类型',
        '篮内有企业卡片时可勾选→发起分析→选择分析任务浮层',
        '本壳无异步「开始分析」',
      ],
      not_for_gold: [
        '空篮态（P0-15）/ 清空（P1-04）破坏会话数据',
        '满员 50 / 断网 424 模拟 / 旧 basket 兼容链',
        '依赖查询页加入结果的多源去重（P0-02）',
        '分发到评估/风险/领域配置页后的下游深验（属目标页）',
        '宿主页「重试」错误态（非篮壳）',
      ],
      no_async_analysis: true,
      basket_cards_enterprise_approx: cardCount,
      host_retry_visible: retryVisible,
    },
    tickets: [...new Set(tickets)],
    scout_refs: ['scout.json', 'page.png', 'scout-env-gate-probe.json'],
    conclusion:
      overall === 'pass'
        ? '环境闸门通过：登录深链、浮层可开、壳层控件与任务浮层可达；无异步开始分析。宿主若见重试记 ticket，不挡篮壳金样。建议金样 ids 见交卷。'
        : '环境闸门未全过：见 gates fail 与 tickets；禁止写过程/结果态假金样。',
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2), 'utf8');
  fs.writeFileSync(path.join(outDir, 'scout-env-gate-probe.json'), JSON.stringify(probe, null, 2), 'utf8');
  console.log(`env-gate overall=${overall} gates=${gates.map((g) => `${g.id}:${g.pass}`).join(' ')}`);
  console.log(`tickets=${envGate.tickets.join(',') || '(none)'}`);
} catch (e) {
  const fail = {
    entry_id: 'shell-compare-basket',
    surveyed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall: 'fail',
    method: 'headless chromium via _env-gate-probe.mjs',
    gates,
    tickets: ['ENV-SHELL-COMPARE-PROBE-CRASH-001'],
    error: e.message,
    conclusion: '探针崩溃；模块 blocked',
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2), 'utf8');
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
