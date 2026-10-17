#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-sz P0-13（01295 数值角标与梯队仪表盘）现场核实。
 * 产物落同目录 scout-p013-*.json；勿当 runner。遵守探针公约（独立无头，不用 IDE/有头浏览器）。
 * 核实点：
 *  R1 逐条历史「查看结果」：城市场景 / tier 区 / 结论区构成（找有城市场景样本走有据分支）
 *  R2 对比区 checkbox + 框架清单每项角标 aria 全量（ⓘ / 待确认 / Mock 实态）
 *  R3 若存在有城市场景任务：tier gauge / tier-label / 结论一致性与 Q-SVCCHAIN-04 角标
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
const route = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const outDir = __dirname;

const dump = (name, data) => {
  fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2), 'utf8');
};

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
      await close.first().click().catch(() => {});
      await page.waitForTimeout(300);
    } else break;
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const report = { probed_at: new Date().toISOString(), stages: {} };

// ---------- 登录 + 深链 ----------
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
if (page.url().includes('/login')) { await ensureLogin(page); await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded' }); }
await page.waitForTimeout(2500);
await closeBasket(page);

// ---------- R1: 逐条历史「查看结果」----------
const r1 = { rows: [] };
try {
  await page.getByRole('tab', { name: '分析记录' }).first().click();
  await page.waitForTimeout(2000);
  const rows = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /shenzhen/ }).filter({ hasText: /已完成/ });
  const n = Math.min(await rows.count(), 4);
  r1.row_count = await rows.count();
  for (let i = 0; i < n; i++) {
    const row = rows.nth(i);
    const btn = row.getByRole('button', { name: /查看结果/ }).first();
    await btn.scrollIntoViewIfNeeded().catch(() => {});
    await btn.click({ timeout: 8000 });
    await page.waitForTimeout(3000);
    let url = page.url();
    let body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    if (/view=processing/.test(url) && /查看结果/.test(body)) {
      const vr = page.getByRole('button', { name: /查看结果/ }).first();
      if (await vr.count()) { await vr.click({ timeout: 5000 }).catch(() => {}); await page.waitForTimeout(2500); url = page.url(); }
    }
    await closeBasket(page);
    body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    const tierSec = await page.locator('[data-testid="svc-eco-sz-tier"]').count();
    const tierSecVis = tierSec ? await page.locator('[data-testid="svc-eco-sz-tier"]').first().isVisible().catch(() => false) : false;
    const tierLines = body.split('\n').filter((s) => /梯队/.test(s)).slice(0, 6);
    r1.rows.push({
      i,
      url,
      compare_grid: await page.locator('[data-testid="svc-eco-sz-compare-grid"]').count(),
      compare_empty: await page.locator('[data-testid="svc-eco-sz-compare-empty"]').count(),
      tier_section: tierSec,
      tier_section_visible: tierSecVis,
      tier_label: await page.locator('[data-testid="svc-eco-sz-tier-label"]').count(),
      conclusions_ul: await page.locator('[data-testid="svc-eco-sz-conclusions"]').count(),
      tier_text_lines: tierLines,
      task_id: (url.match(/task_id=([^&]+)/) || [])[1] || null,
    });
    await page.screenshot({ path: path.join(outDir, `scout-p013-r1-row${i}.png`), fullPage: false });
    await page.getByRole('tab', { name: '分析记录' }).first().click();
    await page.waitForTimeout(1500);
  }
} catch (e) { r1.error = String(e).slice(0, 400); }
dump('scout-p013-r1-history-rows.json', r1);
report.stages.r1 = { ok: !r1.error, rows: (r1.rows || []).length, withCity: (r1.rows || []).filter((r) => r.compare_grid > 0).length };

// ---------- R2: 第一条结果态上角标 aria 全量 ----------
const r2 = {};
try {
  await page.getByRole('tab', { name: '分析记录' }).first().click();
  await page.waitForTimeout(1500);
  const row0 = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /shenzhen/ }).filter({ hasText: /已完成/ }).first();
  await row0.getByRole('button', { name: /查看结果/ }).first().click({ timeout: 8000 });
  await page.waitForTimeout(3000);
  await closeBasket(page);

  const badgeAudit = async (scopeSelector, itemSelector) => {
    const scope = page.locator(scopeSelector).first();
    const items = scope.locator(itemSelector);
    const out = [];
    for (let i = 0; i < (await items.count()); i++) {
      const it = items.nth(i);
      const label = (((await it.innerText().catch(() => '')) || '').split('\n')[0] || '').trim();
      const arias = await Promise.all((await it.locator('[aria-label]').all()).map((el) => el.getAttribute('aria-label').catch(() => null)));
      out.push({
        label,
        info_btn: await it.locator('button.metric-spec-card[aria-label^="指标说明："]').count(),
        info_svg_class: String(await it.locator('button.metric-spec-card svg').first().getAttribute('class').catch(() => '') || ''),
        pending_badge: await it.locator('span.perm-pending-badge').count(),
        pending_aria: await it.locator('span.perm-pending-badge').first().getAttribute('aria-label').catch(() => null),
        mock_badge: await it.locator('span[aria-label="Mock 数据"]').count(),
        review_metric_attr: await it.evaluate((el) => { const g = el.querySelector('[data-review-metric]'); return g ? g.getAttribute('data-review-metric') : null }).catch(() => null),
        all_aria: arias,
      });
    }
    return out;
  };

  r2.compare_items = await badgeAudit('[data-testid="svc-eco-sz-compare-metrics"]', '.arco-checkbox');
  r2.framework_items = await badgeAudit('[data-testid="svc-eco-sz-metric-list"]', 'li');
  // tier 头部角标（若渲染）：requirement_trace + pending_badge
  const tierHead = page.locator('[data-testid="svc-eco-sz-tier"]');
  r2.tier_present = (await tierHead.count()) > 0;
  if (r2.tier_present) {
    r2.tier_aria = await Promise.all((await tierHead.first().locator('[aria-label]').all()).map((el) => el.getAttribute('aria-label').catch(() => null)));
    r2.tier_text = ((await tierHead.first().innerText().catch(() => '')) || '').replace(/\n/g, ' | ').slice(0, 500);
  }
  await page.screenshot({ path: path.join(outDir, 'scout-p013-r2-badges.png'), fullPage: false });
} catch (e) { r2.error = String(e).slice(0, 400); }
dump('scout-p013-r2-badges.json', r2);
report.stages.r2 = { ok: !r2.error, compare: (r2.compare_items || []).length, framework: (r2.framework_items || []).length, tier: r2.tier_present };

// ---------- R3: 有城市场景任务深挖（若存在）----------
const r3 = {};
try {
  const withCity = (r1.rows || []).filter((r) => r.compare_grid > 0);
  r3.with_city_rows = withCity.map((r) => r.task_id);
  if (withCity.length) {
    const target = withCity[0];
    await page.getByRole('tab', { name: '分析记录' }).first().click();
    await page.waitForTimeout(1500);
    const rowT = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: new RegExp(target.task_id || 'shenzhen') }).filter({ hasText: /已完成/ }).first();
    await rowT.getByRole('button', { name: /查看结果/ }).first().click({ timeout: 8000 });
    await page.waitForTimeout(3500);
    await closeBasket(page);
    const tierSec = page.locator('[data-testid="svc-eco-sz-tier"]');
    r3.tier_present = (await tierSec.count()) > 0;
    if (r3.tier_present) {
      r3.tier_text = ((await tierSec.first().innerText().catch(() => '')) || '').replace(/\n/g, ' | ').slice(0, 600);
      r3.tier_label_text = ((await page.locator('[data-testid="svc-eco-sz-tier-label"]').first().innerText().catch(() => '')) || '').replace(/\n/g, ' | ');
      r3.tier_pending_aria = await Promise.all((await tierSec.first().locator('span.perm-pending-badge').all()).map((el) => el.getAttribute('aria-label').catch(() => null)));
      r3.tier_mock_badge = await tierSec.first().locator('span[aria-label="Mock 数据"]').count();
      // gauge echarts：series type + detail formatter() 求值
      r3.gauge = await page.evaluate(() => {
        const root = document.querySelector('[data-testid="svc-eco-sz-tier"]');
        if (!root) return null;
        const nodes = root.querySelectorAll('div');
        for (const nd of nodes) {
          try {
            const ec = window.echarts;
            if (!ec || !ec.getInstanceByDom) continue;
            const inst = ec.getInstanceByDom(nd);
            if (!inst) continue;
            const opt = inst.getOption() || {};
            const s = (opt.series || [])[0] || {};
            let detailText = null;
            try {
              const det = (s.detail || [])[0];
              if (det && typeof det.formatter === 'function') detailText = det.formatter({ value: ((s.data || [])[0] || {}).value });
            } catch (e) {}
            return { type: s.type, gaugeValue: ((s.data || [])[0] || {}).value ?? null, detailText, hasGaugeDom: Boolean(nd.querySelector('canvas')) };
          } catch (e) {}
        }
        return null;
      });
      const concl = page.locator('[data-testid="svc-eco-sz-conclusions"]');
      r3.conclusions_count = await concl.count();
      if (r3.conclusions_count) {
        r3.conclusion_lines = ((await concl.first().innerText().catch(() => '')) || '').split('\n').slice(0, 10);
      }
    }
    await page.screenshot({ path: path.join(outDir, 'scout-p013-r3-tier.png'), fullPage: false });
  } else {
    r3.note = '本环境 3~4 条历史任务均无城市场景：tier 区零渲染（结构性条件渲染），走无据分支（诚实空 + observed）';
  }
} catch (e) { r3.error = String(e).slice(0, 400); }
dump('scout-p013-r3-tier.json', r3);
report.stages.r3 = { ok: !r3.error, withCity: (r3.with_city_rows || []).length };

dump('scout-p013-summary.json', report);
await browser.close();
console.log('probe p013 done', JSON.stringify(report.stages, null, 2));
