#!/usr/bin/env node
/**
 * P0-07（FUNC-01357 备选-系统级入口·对比篮浮层可达）写前无头探针。
 * 验证点先验：①系统级对比篮浮层入口（悬浮球）在本页在屏可点；
 * ②点开浮层呈现（头部「对比篮 · 共 N 项」+ 4 类型 Tab + 条目区/空态）；
 * ③关闭后浮层消失（X2：可视性断言 display/隐藏，非节点存在性）；
 * ④开合全程路由不漂移、页面壳不变（H1 + 占位说明文案不变）；
 * ⑤无机构数据写入（开合窗口内 POST 增量 = 0；GET compare-basket 属读取不判）；
 * ⑥篮内条目类型清单（8 项 = 企业7+产业4+服务机构5=16 计数与类型 Tab）与生产一致性记 observed。
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

const baseUrl = 'http://111.198.38.90:50892/';
const route = '/service/maintenance';
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

async function panelHidden(page) {
  const panel = page.locator('.system-compare-panel').first();
  if (!(await panel.count())) return 'absent';
  const vis = await panel.isVisible().catch(() => false);
  if (!vis) {
    const style = await panel.evaluate((el) => getComputedStyle(el).display + '/' + getComputedStyle(el).visibility).catch(() => '?');
    return 'hidden(' + style + ')';
  }
  return 'visible';
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

// 网络监听：开合窗口内全部请求（写判定 = POST 增量；GET 记 observed）
const reqs = [];
page.on('request', (r) => reqs.push({ m: r.method(), u: r.url().replace(baseUrl, '/') }));

const probe = { probed_at: new Date().toISOString(), entry_id: 'svc-maintenance', case: 'FUNC-01357 / P0-07', steps: [] };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  reqs.length = 0; // 登录噪声不计
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2000);

  // ---- 初始态：浮层默认开（scout 实勘面板常驻）→ 先记录再关闭，得到「入口球」态 ----
  const initPanel = await panelHidden(page);
  const headingBefore = ((await page.locator('section.diagnosis-page-heading, .diagnosis-page-heading').first().innerText().catch(() => '')) || '').replace(/\s+/g, '');
  const h1Before = await page.getByRole('heading', { name: '维护管理', level: 1 }).isVisible().catch(() => false);

  // 若默认开 → 先关（步骤 3 的关闭路径也在此先验）；若默认关 → 直接入口态
  const closeBtn = page.locator('button[aria-label="关闭对比篮"]').first();
  let closeWorked = null;
  if (initPanel === 'visible') {
    await closeBtn.click({ timeout: 5000 });
    await page.waitForTimeout(600);
    closeWorked = await panelHidden(page);
    await page.screenshot({ path: path.join(outDir, 'probe-p007-closed.png'), fullPage: false });
  }

  // ---- ① 入口悬浮球在屏可点 ----
  const entry = page.locator('button[aria-label^="打开对比篮"]').first();
  const entryCount = await page.locator('button[aria-label^="打开对比篮"]').count();
  const entryVisible = await entry.isVisible().catch(() => false);
  const entryEnabled = await entry.isEnabled().catch(() => false);
  const entryAria = await entry.getAttribute('aria-label').catch(() => null);
  const entryBox = await entry.boundingBox().catch(() => null);

  // ---- ② 点开浮层 ----
  let openOk = null, headerText = null, tabs = [], itemCountText = null, entrySectionText = '';
  if (entryVisible) {
    await entry.click({ timeout: 5000 });
    await page.waitForTimeout(800);
    openOk = await panelHidden(page);
    const panel = page.locator('.system-compare-panel').first();
    headerText = ((await panel.locator('.system-compare-panel__header').first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
    tabs = await page.locator('.system-compare-object-tabs [role=tab]').allInnerTexts().catch(() => []);
    const panelText = ((await panel.innerText().catch(() => '')) || '');
    itemCountText = (/\d+\s*\/\s*\d+/.exec(panelText.replace(/\s+/g, ' ')) || [null])[0];
    entrySectionText = panelText.replace(/\s+/g, ' ').slice(0, 300);
    await page.screenshot({ path: path.join(outDir, 'probe-p007-open.png'), fullPage: false });
    // observed：4 类型 Tab 逐个点到（只读浏览，不删不清）——类型清单与生产一致性记录
    const tabDetail = [];
    for (const t of await page.locator('.system-compare-object-tabs [role=tab]').all()) {
      const label = ((await t.innerText()) || '').replace(/\s+/g, ' ').trim();
      tabDetail.push(label);
    }
    probe.tabLabels = tabDetail;
  }

  // ---- ③ 再关闭浮层（打开→关闭完整回路） ----
  let reopenCloseState = null;
  if (openOk === 'visible') {
    await page.locator('button[aria-label="关闭对比篮"]').first().click({ timeout: 5000 });
    await page.waitForTimeout(600);
    reopenCloseState = await panelHidden(page);
    await page.screenshot({ path: path.join(outDir, 'probe-p007-reclosed.png'), fullPage: false });
  }

  // ---- ④ 页面壳不变 ----
  const urlAfter = page.url();
  const headingAfter = ((await page.locator('section.diagnosis-page-heading, .diagnosis-page-heading').first().innerText().catch(() => '')) || '').replace(/\s+/g, '');
  const h1After = await page.getByRole('heading', { name: '维护管理', level: 1 }).isVisible().catch(() => false);

  // ---- ⑤ 写请求判定（POST 增量；compare-basket GET 属读取） ----
  const posts = reqs.filter((r) => r.m === 'POST');
  const basketGets = reqs.filter((r) => /compare-basket/.test(r.u));

  probe.steps.push({
    step: 'p007_basket_cycle',
    url_start: new URL(route.replace(/^\//, ''), baseUrl).toString(),
    url_after: urlAfter,
    routeStable: urlAfter.includes('/service/maintenance'),
    initPanelState: initPanel,
    closeWorked,
    entry: { count: entryCount, visible: entryVisible, enabled: entryEnabled, aria: entryAria, box: entryBox },
    openState: openOk,
    panelHeader: headerText,
    objectTabs: tabs,
    itemCountSample: itemCountText,
    panelTextHead: entrySectionText,
    reopenCloseState,
    shellKept: {
      h1Before, h1After,
      headingBefore_head: headingBefore.slice(0, 120),
      headingAfter_head: headingAfter.slice(0, 120),
      headingUnchanged: headingBefore === headingAfter,
    },
    network: {
      totalRequests: reqs.length,
      posts: posts.map((r) => r.u),
      basketGets: basketGets.map((r) => r.u),
      noWrite: posts.length === 0,
    },
  });

  console.log(JSON.stringify(probe, null, 2));
  fs.writeFileSync(path.join(outDir, 'probe-p007.json'), JSON.stringify(probe, null, 2));
} catch (e) {
  probe.error = String(e);
  console.error(JSON.stringify(probe, null, 2));
  fs.writeFileSync(path.join(outDir, 'probe-p007.json'), JSON.stringify(probe, null, 2));
  process.exitCode = 1;
} finally {
  await browser.close();
}
