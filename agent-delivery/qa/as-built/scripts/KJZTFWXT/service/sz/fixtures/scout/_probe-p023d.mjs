#!/usr/bin/env node
/**
 * _probe-p023d — 稳登录 + 先挂 route 再进结果态 + 最小 fulfill + vue option 读「无数据」
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
const injectCities = [
  { city: '深圳', scale: 9, tech: 80, density: 0.4 },
  { city: '全国平均', scale: 5, tech: 70, density: 0.3 },
  { city: '北京' },
  { city: '上海', scale: 7, tech: 75, density: 0.35 },
  { city: '广州', scale: 6, tech: 72, density: 0.32 },
];

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await ctx.newPage();

async function ensureLogin() {
  if (!page.url().includes('/login')) return;
  const userBox = page.locator('input[placeholder*=用户名], input[type=text]').first();
  const passBox = page.locator('input[type=password]').first();
  await userBox.waitFor({ state: 'visible', timeout: 15000 });
  await passBox.waitFor({ state: 'visible', timeout: 15000 });
  await userBox.fill('admin');
  await passBox.fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin();

let hit = 0;
const reqUrls = [];
await page.context().route('**/topicAsync/topic/v1/analysis/tasks/*/result*', async (route) => {
  const req = route.request();
  reqUrls.push(req.method() + ' ' + req.url().replace(BASE, ''));
  if (req.method() !== 'GET') return route.continue();
  hit += 1;
  const body = {
    code: 0,
    msg: 'ok',
    ok: true,
    data: {
      taskId: 'SVC-20261015-085',
      userId: 'guest',
      analysisType: 'shenzhen',
      status: 'success',
      // 关键：不带 targetParams.result_payload，避免抢先于 resultData
      targetParams: JSON.stringify({
        analysis_key: 'svcan.shenzhen.v0',
        analysis_fp: 'svc|shenzhen|INB1701',
        industry: 'INB1701',
        workspace: 'shenzhen',
        viewed: true,
      }),
      resultData: JSON.stringify({ cities: injectCities }),
      resultAssetId: null,
      errorMsg: null,
    },
  };
  return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });
});

const out = { probed_at: new Date().toISOString() };

try {
  // 经历史进结果（触发 GET result → 被 fulfill）
  await page.goto(BASE + '/service/chain-analysis?workspace=shenzhen&tab=shenzhen', { waitUntil: 'domcontentloaded' });
  await ensureLogin();
  await page.waitForTimeout(1500);
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if (await close.count() && await close.first().isVisible().catch(() => false)) {
    try { await close.first().click({ timeout: 1200 }); } catch {}
  }
  const rec = page.locator('[role=tab][data-tab-key="records"]').or(page.getByRole('tab', { name: '分析记录', exact: true }));
  await rec.first().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /shenzhen/ }).filter({ hasText: /已完成/ }).filter({ has: page.getByRole('button', { name: /查看结果/ }) }).first();
  await row.getByRole('button', { name: /查看结果/ }).filter({ hasNot: page.locator('.arco-btn-disabled') }).first().click({ timeout: 8000 });
  await page.waitForTimeout(4500);

  out.url = page.url();
  out.hit = hit;
  out.reqUrls = reqUrls;
  out.hasEmpty = (await page.locator('[data-testid="svc-eco-sz-compare-empty"]').count()) > 0
    && await page.locator('[data-testid="svc-eco-sz-compare-empty"]').first().isVisible().catch(() => false);
  out.hasGrid = (await page.locator('[data-testid="svc-eco-sz-compare-grid"]').count()) > 0
    && await page.locator('[data-testid="svc-eco-sz-compare-grid"]').first().isVisible().catch(() => false);
  out.canvasN = await page.locator('[data-testid="svc-eco-sz-compare"] canvas').count();
  out.caliber = ((await page.locator('[data-testid="svc-eco-sz-compare-caliber"]').innerText().catch(() => '')) || '').trim();
  out.emptyText = out.hasEmpty ? ((await page.locator('[data-testid="svc-eco-sz-compare-empty"]').first().innerText().catch(() => '')) || '').trim() : '';

  out.vueCharts = await page.evaluate(() => {
    const cells = [...document.querySelectorAll('.svc-eco-compare-cell')];
    return cells.map((cell) => {
      const head = (cell.querySelector('.svc-eco-compare-cell__head')?.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 48);
      const chartRoot = cell.querySelector('.svc-eco-compare-cell__chart');
      if (!chartRoot) return { head, err: 'no-chart-root' };
      let comp = chartRoot.__vueParentComponent;
      let option = null;
      let how = '';
      for (let i = 0; i < 10 && comp; i++) {
        const exp = comp.exposed || {};
        const setup = comp.setupState || {};
        const ctx = comp.ctx || {};
        for (const c of [
          typeof exp.getEchartsInstance === 'function' ? exp.getEchartsInstance() : null,
          setup.chart, ctx.chart, exp.chart,
        ]) {
          if (c && typeof c.getOption === 'function') { option = c.getOption(); how = 'inst'; break; }
        }
        if (option) break;
        if (comp.props?.option) { option = comp.props.option; how = 'props'; break; }
        comp = comp.parent;
      }
      if (!option) {
        const c0 = chartRoot.__vueParentComponent;
        return { head, err: 'no-option', exposed: c0?.exposed ? Object.keys(c0.exposed) : [], setup: c0?.setupState ? Object.keys(c0.setupState) : [], props: c0?.props ? Object.keys(c0.props) : [] };
      }
      const xa = option.xAxis;
      const cats = Array.isArray(xa) ? (xa[0] && xa[0].data) : (xa && xa.data);
      const ser = (option.series || [])[0] || {};
      const raw = ser.data || [];
      const values = raw.map((d) => (d && typeof d === 'object' ? d.value : d));
      const labels = raw.map((d) => {
        try {
          if (d && d.label && typeof d.label.formatter === 'function') return String(d.label.formatter());
        } catch (e) { return 'fmt-err'; }
        return d && typeof d === 'object' && d.value == null ? '无数据' : String(d && typeof d === 'object' ? d.value : d);
      });
      const bi = Array.isArray(cats) ? cats.map(String).indexOf('北京') : -1;
      return {
        head, how,
        cities: Array.isArray(cats) ? cats.map(String) : [],
        values, labels,
        nullN: values.filter((v) => v == null).length,
        zeroN: values.filter((v) => v === 0).length,
        beijingValue: bi >= 0 ? values[bi] : undefined,
        beijingLabel: bi >= 0 ? labels[bi] : undefined,
        hasWushuju: labels.some((l) => /无数据/.test(String(l))),
      };
    });
  });

  // 悬停 tooltip
  if (out.hasGrid && out.canvasN > 0) {
    const box = await page.locator('.svc-eco-compare-cell__chart').first().boundingBox();
    if (box) {
      await page.mouse.move(box.x + box.width * 0.5, box.y + box.height * 0.55);
      await page.waitForTimeout(900);
      out.tooltip = await page.evaluate(() =>
        [...document.querySelectorAll('div')]
          .filter((el) => {
            const s = getComputedStyle(el);
            return (s.position === 'absolute' || s.position === 'fixed')
              && el.innerText && /无数据|北京/.test(el.innerText)
              && el.offsetWidth > 10 && el.offsetWidth < 360 && el.offsetHeight > 8;
          })
          .map((el) => el.innerText.trim().slice(0, 60))
          .slice(0, 6),
      );
    }
  }
  out.ok = true;
} catch (e) {
  out.ok = false;
  out.error = String(e).slice(0, 500);
}

await page.screenshot({ path: path.join(__dirname, 'probe-p023d.png'), fullPage: true }).catch(() => {});
await page.context().unroute('**/topicAsync/topic/v1/analysis/tasks/*/result*').catch(() => {});
fs.writeFileSync(path.join(__dirname, '_probe-p023d.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify({
  ok: out.ok, hit: out.hit, hasGrid: out.hasGrid, hasEmpty: out.hasEmpty, canvasN: out.canvasN,
  vueCharts: out.vueCharts, tooltip: out.tooltip, reqUrls: out.reqUrls, error: out.error,
}, null, 2));
await browser.close();
