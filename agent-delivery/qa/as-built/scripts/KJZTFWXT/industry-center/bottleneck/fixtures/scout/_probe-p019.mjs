#!/usr/bin/env node
/** 一次性探针 · P0-19(FUNC-00625) 写稿前：清空细分/分析对象 + 开始分析门禁。
 * 产物 probe-p019.json / probe-p019-*.png；勿当 runner。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const route = '/industry-center/diagnosis?workspace=bottleneck&tab=bottleneck';

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function readSel(page, loc) {
  const el = loc.first();
  if (!(await el.count())) return '';
  return ((await el.getAttribute('title')) || (await el.innerText()) || '').replace(/\s+/g, ' ').trim();
}

async function tryClear(page, scopeSel, label) {
  const scope = page.locator(scopeSel).first();
  const before = await readSel(page, scope.locator('.arco-select-view, .arco-select-view-value').first().or(scope));
  const attempts = [];
  // hover → clear btn
  await scope.hover().catch(() => {});
  await page.waitForTimeout(400);
  const clearBtns = [
    `${scopeSel} .arco-select-view-clear-btn`,
    `${scopeSel} .arco-icon-hover`,
    `${scopeSel} .arco-select-clear-icon`,
    `${scopeSel} .arco-icon-close`,
  ];
  let cleared = false;
  let via = null;
  for (const sel of clearBtns) {
    const n = await page.locator(sel).count();
    const vis = n ? await page.locator(sel).first().isVisible().catch(() => false) : false;
    attempts.push({ sel, n, vis });
    if (n && !cleared) {
      try {
        await page.locator(sel).first().click({ force: true, timeout: 3000 });
        await page.waitForTimeout(800);
        cleared = true;
        via = sel;
        break;
      } catch (e) {
        attempts[attempts.length - 1].err = String(e.message || e).slice(0, 120);
      }
    }
  }
  // keyboard Backspace / Delete on focused view
  if (!cleared) {
    try {
      await scope.click({ timeout: 2000 });
      await page.waitForTimeout(200);
      await page.keyboard.press('Control+a');
      await page.keyboard.press('Backspace');
      await page.waitForTimeout(600);
      via = 'keyboard-backspace';
      cleared = true; // tentative; verified by after
    } catch (e) {
      attempts.push({ sel: 'keyboard', err: String(e.message || e).slice(0, 120) });
    }
  }
  const after = await readSel(page, scope.locator('.arco-select-view, .arco-select-view-value').first().or(scope));
  const emptyish = !after || /请选择|选择|筛选|placeholder/i.test(after) || after.length < 2;
  return { label, before, after, emptyish, clearedAttempt: !!via, via, attempts };
}

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2500);

  const cb = page.locator('[aria-label="关闭对比篮"]');
  if ((await cb.count()) && (await cb.first().isVisible().catch(() => false))) {
    await cb.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
  const tab = page.getByRole('tab', { name: '产业瓶颈堵点识别' });
  if ((await tab.getAttribute('aria-selected')) !== 'true') {
    await tab.click();
    await page.waitForTimeout(800);
  }

  const cluster = page.locator('.arco-select-view[aria-label="集群"]');
  const chain = page.locator('.arco-select-view[aria-label="产业"]');
  const seg = page.locator('.industry-catalog-select').first();

  const landing = {
    cluster: await readSel(page, cluster),
    chain: await readSel(page, chain),
    segment: await readSel(page, seg),
  };
  const startBtn = page.getByRole('button', { name: '开始分析' });
  const startBefore = {
    count: await startBtn.count(),
    disabled: await startBtn.first().isDisabled().catch(() => null),
    ariaDisabled: await startBtn.first().getAttribute('aria-disabled').catch(() => null),
    class: (await startBtn.first().getAttribute('class').catch(() => '')) || '',
  };

  // DOM inventory of clear affordances near analysis object
  const clearInventory = await page.evaluate(() => {
    const zone = document.querySelector('main') || document.body;
    const nodes = Array.from(zone.querySelectorAll(
      '.arco-select-view-clear-btn, .arco-select-clear-icon, .arco-icon-close, .arco-icon-hover, [aria-label*=清空], [aria-label*=清除], button'
    ));
    return nodes.slice(0, 40).map((n) => ({
      tag: n.tagName,
      cls: (n.className || '').toString().slice(0, 120),
      aria: n.getAttribute('aria-label') || '',
      text: (n.innerText || '').trim().slice(0, 40),
      visible: !!(n.offsetParent || n.getClientRects().length),
      near: (n.closest('.industry-catalog-select, [aria-label="集群"], [aria-label="产业"], .arco-select') || {}).className?.toString?.().slice(0, 80) || '',
    }));
  });

  await page.screenshot({ path: path.join(__dirname, 'probe-p019-before.png'), fullPage: false });

  // 1) try clear segment (用例：清空细分产业)
  const segClear = await tryClear(page, '.industry-catalog-select', 'segment');
  await page.waitForTimeout(1000);
  const afterSeg = {
    cluster: await readSel(page, cluster),
    chain: await readSel(page, chain),
    segment: await readSel(page, seg),
    startDisabled: await startBtn.first().isDisabled().catch(() => null),
    startClass: (await startBtn.first().getAttribute('class').catch(() => '')) || '',
    wroteBackDefault: false,
  };
  afterSeg.wroteBackDefault =
    /半导体与集成电路/.test(afterSeg.segment) && /新一代信息技术/.test(afterSeg.cluster);

  await page.screenshot({ path: path.join(__dirname, 'probe-p019-after-seg.png'), fullPage: false });

  // 2) if segment still filled, try clear cluster (cascade empty)
  let clusterClear = null;
  let afterCluster = null;
  if (!segClear.emptyish) {
    clusterClear = await tryClear(page, '.arco-select-view[aria-label="集群"]', 'cluster');
    await page.waitForTimeout(1000);
    afterCluster = {
      cluster: await readSel(page, cluster),
      chain: await readSel(page, chain),
      segment: await readSel(page, seg),
      startDisabled: await startBtn.first().isDisabled().catch(() => null),
      startClass: (await startBtn.first().getAttribute('class').catch(() => '')) || '',
    };
    await page.screenshot({ path: path.join(__dirname, 'probe-p019-after-cluster.png'), fullPage: false });
  }

  // 3) if still not empty, try chain clear
  let chainClear = null;
  let afterChain = null;
  if ((!segClear.emptyish) && (!afterCluster || !/^\s*$/.test(afterCluster.cluster || 'x') && !afterCluster.segment?.match(/^$|请选择/))) {
    chainClear = await tryClear(page, '.arco-select-view[aria-label="产业"]', 'chain');
    await page.waitForTimeout(1000);
    afterChain = {
      cluster: await readSel(page, cluster),
      chain: await readSel(page, chain),
      segment: await readSel(page, seg),
      startDisabled: await startBtn.first().isDisabled().catch(() => null),
    };
  }

  // wait 2s to detect silent write-back of defaults
  await page.waitForTimeout(2000);
  const settle = {
    cluster: await readSel(page, cluster),
    chain: await readSel(page, chain),
    segment: await readSel(page, seg),
    startDisabled: await startBtn.first().isDisabled().catch(() => null),
    wroteBackDefault:
      /新一代信息技术/.test(await readSel(page, cluster)) &&
      /INB1701/.test(await readSel(page, chain)) &&
      /半导体与集成电路/.test(await readSel(page, seg)),
  };

  const clearCtrlStable = !!(segClear.emptyish || (afterCluster && (!afterCluster.segment || !/半导体/.test(afterCluster.segment))));
  const gateOk = clearCtrlStable && (settle.startDisabled === true || /disabled/.test(settle.startDisabled + ''));

  const out = {
    probed_at: new Date().toISOString(),
    case_id: 'P0-19',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00625',
    url: page.url(),
    landing,
    startBefore,
    clearInventory,
    segClear,
    afterSeg,
    clusterClear,
    afterCluster,
    chainClear,
    afterChain,
    settle,
    clearCtrlStable,
    gateOk,
    ticket_hint: clearCtrlStable
      ? null
      : 'ENV-CHAIN-BOTTLENECK-CLEAR-CTRL',
    note: clearCtrlStable
      ? '清空可达；按空态+开始分析门禁写实跑断言'
      : '清空控件不稳定/不可达 → allow_skip 归 ENV-CHAIN-BOTTLENECK-CLEAR-CTRL；目标态断言仍按 FUNC-00625 写入',
  };

  fs.writeFileSync(path.join(__dirname, 'probe-p019.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify({
    landing,
    startBefore,
    segClear: { before: segClear.before, after: segClear.after, emptyish: segClear.emptyish, via: segClear.via, attempts: segClear.attempts },
    afterSeg,
    clusterClear: clusterClear && { before: clusterClear.before, after: clusterClear.after, emptyish: clusterClear.emptyish, via: clusterClear.via },
    afterCluster,
    settle,
    clearCtrlStable,
    gateOk,
    inventoryN: clearInventory.length,
  }, null, 2));
} finally {
  await browser.close();
}
