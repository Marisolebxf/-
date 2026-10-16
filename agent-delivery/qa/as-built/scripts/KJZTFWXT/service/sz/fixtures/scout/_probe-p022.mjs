#!/usr/bin/env node
/**
 * _probe-p022.mjs — P0-22 / FUNC-01303 写前探针（无头一次性）
 * 目的：结果态逐项取消全部对比指标后：
 *   ① compare-none 提示文案与可见性
 *   ② 勾选=0 / URL sz_metrics=-
 *   ③ 有城市场景：grid 保留上次图形（lastRows）且不新绘空轴
 *   ④ 无城市场景：诚实空仍在 + 无 compare-grid / 无空 canvas 轴
 * 铁律：经历史「查看结果」进结果态，不 fresh 起任务；失败落盘后继续。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://111.198.38.90:50892';
const SZ = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const out = { probed_at: new Date().toISOString(), entry: 'svc-sz', case: 'P0-22 / FUNC-01303' };

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await ctx.newPage();

await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(800);
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1500);
  if (page.url().includes('/login')) {
    await page.locator('button[type=submit], button:has-text("登录")').first().click().catch(() => {});
    await page.waitForTimeout(1500);
  }
}
out.logged_in = !page.url().includes('/login');

const closeBasket = async () => {
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if (await close.count() && await close.first().isVisible().catch(() => false) && await close.first().isEnabled().catch(() => false)) {
    try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
  }
};

const snapChart = async () => {
  const grid = page.locator('[data-testid="svc-eco-sz-compare-grid"]');
  const empty = page.locator('[data-testid="svc-eco-sz-compare-empty"]');
  const none = page.locator('[data-testid="svc-eco-sz-compare-none"]');
  const hasGrid = (await grid.count()) > 0 && await grid.first().isVisible().catch(() => false);
  const hasEmpty = (await empty.count()) > 0 && await empty.first().isVisible().catch(() => false);
  const hasNone = (await none.count()) > 0 && await none.first().isVisible().catch(() => false);
  let series = '';
  if (hasGrid) {
    series = await page.evaluate(() => {
      const root = document.querySelector('[data-testid="svc-eco-sz-compare-grid"]');
      if (!root) return '';
      const nodes = root.querySelectorAll('div');
      for (const nd of nodes) {
        try {
          const ec = window.echarts;
          if (!ec || !ec.getInstanceByDom) continue;
          const inst = ec.getInstanceByDom(nd);
          if (!inst) continue;
          const opt = inst.getOption() || {};
          const sers = (opt.series || []).map((s) => String((s && s.name) || ''));
          return sers.join(',');
        } catch {}
      }
      return (root.innerText || '').slice(0, 200);
    });
  }
  const canvasN = await page.locator('[data-testid="svc-eco-sz-compare"] canvas').count();
  return {
    hasGrid, hasEmpty, hasNone,
    noneText: hasNone ? ((await none.first().innerText().catch(() => '')) || '').trim() : '',
    emptyText: hasEmpty ? ((await empty.first().innerText().catch(() => '')) || '').trim().slice(0, 80) : '',
    series, canvasN,
    checked: await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').count(),
    sz_metrics: (page.url().match(/sz_metrics=([^&]*)/) || [])[1] || null,
  };
};

try {
  await page.goto(BASE + SZ, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await closeBasket();
  const rec = page.locator('[role=tab][data-tab-key="records"]').or(page.getByRole('tab', { name: '分析记录', exact: true }));
  await rec.first().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /shenzhen/ }).filter({ hasText: /已完成/ }).filter({ has: page.getByRole('button', { name: /查看结果/ }) }).first();
  await row.getByRole('button', { name: /查看结果/ }).filter({ hasNot: page.locator('.arco-btn-disabled') }).first().click({ timeout: 8000 });
  await page.waitForTimeout(3000);
  await closeBasket();
  out.before = await snapChart();

  // 逐项取消全部
  for (let i = 0; i < 5; i++) {
    const c = await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').count();
    if (!c) break;
    await page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox-checked').first().click({ timeout: 5000 });
    await page.waitForTimeout(700);
  }
  await page.waitForTimeout(800);
  out.after_uncheck_all = await snapChart();
  out.url_after = page.url();

  // 还原全选
  const boxes = page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox');
  const n = await boxes.count();
  for (let i = 0; i < n; i++) {
    const cls = String(await boxes.nth(i).getAttribute('class') || '');
    if (!/arco-checkbox-checked/.test(cls)) {
      await boxes.nth(i).click({ timeout: 5000 });
      await page.waitForTimeout(600);
    }
  }
  out.after_restore = await snapChart();
  out.ok = true;
} catch (e) {
  out.ok = false;
  out.error = String(e).slice(0, 400);
}

fs.writeFileSync(path.join(__dirname, '_probe-p022.json'), JSON.stringify(out, null, 2), 'utf8');
await browser.close();
console.log(JSON.stringify({ ok: out.ok, before: out.before, after: out.after_uncheck_all, restore: out.after_restore, error: out.error }, null, 2));
