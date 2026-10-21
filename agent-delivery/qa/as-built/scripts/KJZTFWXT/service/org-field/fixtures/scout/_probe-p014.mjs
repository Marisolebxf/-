#!/usr/bin/env node
/**
 * P0-14 无头实勘 · FUNC-00654（重跑：软点查看结果 + 分析记录兜底）
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
const route = '/service/institution-judgment?workspace=field&tab=coverage';
const out = { surveyed_at: new Date().toISOString(), stages: {}, clickLog: [] };

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
    await page.waitForTimeout(400);
  }
}

async function softClick(page, loc, label) {
  const n = await loc.count();
  if (!n) { out.clickLog.push({ step: label, ok: false, reason: 'not_found' }); return false; }
  const el = loc.first();
  const visible = await el.isVisible().catch(() => false);
  const enabled = await el.isEnabled().catch(() => false);
  if (!visible || !enabled) {
    out.clickLog.push({ step: label, ok: false, reason: !visible ? 'not_visible' : 'disabled' });
    return false;
  }
  await el.click({ timeout: 5000 }).catch((e) => {
    out.clickLog.push({ step: label, ok: false, reason: String(e).slice(0, 100) });
    return false;
  });
  out.clickLog.push({ step: label, ok: true });
  return true;
}

async function snapMain(page) {
  const main = page.locator('main').first();
  const t = ((await main.innerText().catch(() => '')) || '');
  const charts = await main.locator('canvas, [_echarts_instance_], .echarts-for-react').count();
  const alerts = await page.locator('main .arco-alert').allInnerTexts().catch(() => []);
  return {
    url: page.url(),
    charts,
    hasConfigEmptyHint: /请先选择分析机构|已选机构（0\s*家）/.test(t),
    hasHeatShell: /热力图/.test(t) && /服务机构产业领域服务广度|服务深度|色阶/.test(t),
    hasHonestMatrixEmpty: /当前结果快照没有覆盖矩阵/.test(t),
    hasNoCoverTitle: /暂无覆盖数据/.test(t),
    hasNoCoverAll: /当前集合内机构均暂无覆盖数据/.test(t),
    hasNoCoverPartial: /以下机构暂无覆盖数据/.test(t),
    hasNoRank: /暂无可排名机构/.test(t),
    hasZeroFillSuspect: /(?:深度得分|覆盖深度|广度)[：:\s]*0(?:\s|$|分|家)/.test(t) && /热力|矩阵/.test(t) && !/当前结果快照没有覆盖矩阵|暂无覆盖数据/.test(t),
    alerts: (alerts || []).slice(0, 6).map((s) => String(s).replace(/\s+/g, ' ').slice(0, 160)),
    snippet: t.slice(0, 1100),
  };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(1500);
  await closeBasket(page);
  if (/org_ids|view=/.test(page.url())) {
    await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1500);
    await closeBasket(page);
  }
  out.stages.configEmpty = await snapMain(page);

  // 选机构
  let selectPath = 'modal_pick';
  const pickOk = await softClick(page, page.getByRole('button', { name: '选择机构' }).first(), 'open_picker');
  if (pickOk) {
    await page.waitForTimeout(800);
    const dialog = page.locator('.arco-modal:visible, .arco-modal').filter({ hasText: '选择服务机构' }).first();
    const dlgOk = await dialog.isVisible().catch(() => false);
    if (dlgOk) {
      const boxes = dialog.locator('.arco-checkbox:not(.arco-checkbox-disabled)');
      for (let i = 0; i < 20 && !(await boxes.count()); i++) {
        const body = dialog.locator('.arco-modal-body, .arco-table-body, .arco-list').first();
        if (await body.count()) { try { await body.evaluate((el) => { el.scrollTop = (el.scrollTop || 0) + 240 }); } catch {} }
        await page.waitForTimeout(400);
      }
      if (await boxes.count()) {
        try { await boxes.first().scrollIntoViewIfNeeded(); } catch {}
        await boxes.first().click({ timeout: 8000 });
        await page.waitForTimeout(300);
        await dialog.getByRole('button', { name: '确定', exact: true }).last().click({ timeout: 8000 });
        await page.waitForTimeout(1200);
      } else {
        selectPath = 'deeplink_fallback';
        await page.keyboard.press('Escape').catch(() => {});
        await page.goto(new URL('service/institution-judgment?workspace=field&tab=coverage&org_ids[]=79bbcfc0e68027808f1f4caf1b6f0469', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(2000);
      }
    } else {
      selectPath = 'deeplink_fallback';
      await page.goto(new URL('service/institution-judgment?workspace=field&tab=coverage&org_ids[]=79bbcfc0e68027808f1f4caf1b6f0469', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(2000);
    }
  } else {
    selectPath = 'deeplink_fallback';
    await page.goto(new URL('service/institution-judgment?workspace=field&tab=coverage&org_ids[]=79bbcfc0e68027808f1f4caf1b6f0469', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
  }
  await closeBasket(page);
  out.stages.afterSelect = { ...(await snapMain(page)), selectPath };

  // 开始分析
  await softClick(page, page.getByRole('button', { name: '开始分析', exact: true }).first(), 'start_analysis');
  await page.waitForTimeout(4000);
  out.stages.afterStart = await snapMain(page);

  let reached = /view=result/.test(page.url());
  for (let i = 0; i < 20 && !reached; i++) {
    const t = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    if (/view=result/.test(page.url()) || /当前结果快照没有覆盖矩阵|暂无覆盖数据|服务机构产业领域服务广度\s*&/.test(t)) {
      reached = true;
      break;
    }
    const viewBtn = page.getByRole('button', { name: /查看结果/ }).first();
    if ((await viewBtn.count()) && (await viewBtn.isVisible().catch(() => false)) && !(await viewBtn.isDisabled().catch(() => true))) {
      await softClick(page, viewBtn, 'view_result_process');
      await page.waitForTimeout(2500);
      reached = true;
      break;
    }
    await page.waitForTimeout(1500);
  }
  out.stages.processWait = { reached, url: page.url(), snap: await snapMain(page) };

  // 分析记录兜底
  if (!/当前结果快照没有覆盖矩阵|暂无覆盖数据/.test((out.stages.processWait.snap.snippet || ''))) {
    await softClick(page, page.locator('[role=tab][data-tab-key="records"]').first(), 'tab_records');
    await page.waitForTimeout(1200);
    const rows = page.locator('main table tbody tr, main .arco-table-body tr');
    const n = await rows.count();
    out.stages.records = { rowCount: n };
    const enabledView = page.locator('main').getByRole('button', { name: '查看结果' }).filter({ hasNot: page.locator('[disabled]') });
    // Playwright filter hasNot may not work that way — soft iterate
    const allView = page.locator('main').getByRole('button', { name: '查看结果' });
    const av = await allView.count();
    let clicked = false;
    for (let i = 0; i < av; i++) {
      const b = allView.nth(i);
      if (await b.isEnabled().catch(() => false)) {
        await b.click({ timeout: 5000 }).catch(() => {});
        await page.waitForTimeout(2500);
        clicked = true;
        out.clickLog.push({ step: 'hist_view_result', ok: true, index: i });
        break;
      }
    }
    if (!clicked) out.clickLog.push({ step: 'hist_view_result', ok: false, reason: 'no_enabled', count: av });
  }
  await closeBasket(page);
  out.stages.result = await snapMain(page);

  out.conclusion = {
    configEmpty_ok: out.stages.configEmpty.charts === 0 && out.stages.configEmpty.hasConfigEmptyHint,
    result_honestMatrixEmpty: !!out.stages.result.hasHonestMatrixEmpty,
    result_noCoverCopy: !!(out.stages.result.hasNoCoverTitle || out.stages.result.hasNoCoverAll || out.stages.result.hasNoCoverPartial),
    result_noRank: !!out.stages.result.hasNoRank,
    result_charts: out.stages.result.charts,
    gap: !(out.stages.result.hasNoCoverTitle || out.stages.result.hasNoCoverAll || out.stages.result.hasNoCoverPartial)
      ? '结果态未见「暂无覆盖数据」；现为诚实空矩阵路径（hasMatrix=false）'
      : '见「暂无覆盖数据」路径',
  };
} catch (e) {
  out.error = String(e);
  out.stack = (e && e.stack) ? String(e.stack).slice(0, 600) : '';
} finally {
  fs.writeFileSync(path.join(__dirname, 'scout-p014.json'), JSON.stringify(out, null, 2));
  await browser.close();
  console.log(JSON.stringify({ conclusion: out.conclusion, error: out.error, clickLog: out.clickLog }, null, 2));
}
