#!/usr/bin/env node
/**
 * _probe-p023.mjs — P0-23 / FUNC-01304 写前探针（无头一次性）
 * 目的：构造「某城市某指标无数据」城市场景，核验柱位「无数据」占位且不以 0 填充。
 * 手法：经历史「查看结果」进结果态 → 捕获 GET .../tasks/{id}/result 包络 →
 *       route.fulfill 注入 cities（深圳有 scale、北京缺 scale）→ reload 重读 →
 *       读 ECharts series label/tooltip 是否出「无数据」、value===null 且 ≠0。
 * 铁律：失败落盘后继续；结束 unroute。
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
const out = { probed_at: new Date().toISOString(), entry: 'svc-sz', case: 'P0-23 / FUNC-01304' };

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
  const hasGrid = (await grid.count()) > 0 && await grid.first().isVisible().catch(() => false);
  const hasEmpty = (await empty.count()) > 0 && await empty.first().isVisible().catch(() => false);
  const caliber = ((await page.locator('[data-testid="svc-eco-sz-compare"]').first().innerText().catch(() => '')) || '');
  const echarts = hasGrid
    ? await page.evaluate(() => {
        const root = document.querySelector('[data-testid="svc-eco-sz-compare-grid"]');
        if (!root) return null;
        const nodes = root.querySelectorAll('div');
        for (const nd of nodes) {
          try {
            const ec = window.echarts;
            if (!ec || !ec.getInstanceByDom) continue;
            const inst = ec.getInstanceByDom(nd);
            if (!inst) continue;
            const opt = inst.getOption() || {};
            const xa = opt.xAxis;
            const cats = Array.isArray(xa) ? (xa[0] && xa[0].data) : (xa && xa.data);
            const ser = (opt.series || [])[0] || {};
            const data = (ser.data || []).map((d) => {
              if (d && typeof d === 'object') {
                return { value: d.value === undefined ? null : d.value, hasLabelFmt: Boolean(d.label && d.label.formatter) };
              }
              return { value: d === undefined ? null : d, hasLabelFmt: false };
            });
            // 触发 label formatter 读「无数据」文案
            const labels = (ser.data || []).map((d, i) => {
              try {
                if (d && d.label && typeof d.label.formatter === 'function') return String(d.label.formatter());
              } catch {}
              return data[i] && data[i].value == null ? '无数据?' : String(data[i]?.value);
            });
            return {
              cities: Array.isArray(cats) ? cats.map(String) : [],
              values: data.map((d) => d.value),
              labels,
              nullCount: data.filter((d) => d.value == null).length,
              zeroCount: data.filter((d) => d.value === 0).length,
            };
          } catch {}
        }
        return { err: 'no-echarts-instance', text: (root.innerText || '').slice(0, 200) };
      })
    : null;
  return {
    hasGrid,
    hasEmpty,
    emptyText: hasEmpty ? ((await empty.first().innerText().catch(() => '')) || '').trim().slice(0, 100) : '',
    caliber_has_wushuju: /缺值显示「无数据」|缺值显示『无数据』|缺值显示无数据/.test(caliber),
    echarts,
    canvasN: await page.locator('[data-testid="svc-eco-sz-compare"] canvas').count(),
  };
};

try {
  // 先挂监听捕获真实 GET result 包络
  let captured = null;
  page.on('response', async (res) => {
    try {
      const u = res.url();
      if (!/\/topicAsync\/topic\/v1\/analysis\/tasks\/[^/?]+\/result/.test(u)) return;
      if (res.request().method() !== 'GET') return;
      const json = await res.json().catch(() => null);
      if (json) captured = { url: u.replace(BASE, ''), status: res.status(), bodyKeys: Object.keys(json || {}), sample: json };
    } catch {}
  });

  await page.goto(BASE + SZ, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await closeBasket();
  const rec = page.locator('[role=tab][data-tab-key="records"]').or(page.getByRole('tab', { name: '分析记录', exact: true }));
  await rec.first().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /shenzhen/ }).filter({ hasText: /已完成/ }).filter({ has: page.getByRole('button', { name: /查看结果/ }) }).first();
  await row.getByRole('button', { name: /查看结果/ }).filter({ hasNot: page.locator('.arco-btn-disabled') }).first().click({ timeout: 8000 });
  await page.waitForTimeout(3500);
  await closeBasket();
  out.before = await snapChart();
  out.captured_result = captured
    ? {
        url: captured.url,
        status: captured.status,
        bodyKeys: captured.bodyKeys,
        code: captured.sample?.code,
        dataKeys: captured.sample?.data ? Object.keys(captured.sample.data) : null,
        hasResultData: Boolean(captured.sample?.data?.resultData),
        resultDataPreview: typeof captured.sample?.data?.resultData === 'string'
          ? captured.sample.data.resultData.slice(0, 300)
          : captured.sample?.data?.resultData,
        targetParamsPreview: typeof captured.sample?.data?.targetParams === 'string'
          ? captured.sample.data.targetParams.slice(0, 300)
          : null,
      }
    : null;

  // 构造注入：深圳 scale=9，北京无 scale（缺值→null→「无数据」）；全国/沪/穗同城有值防缺城
  const injectCities = [
    { city: '深圳', scale: 9, tech: 80, density: 0.4 },
    { city: '全国平均', scale: 5, tech: 70, density: 0.3 },
    { city: '北京' }, // 三项全缺 → 柱位「无数据」
    { city: '上海', scale: 7, tech: 75, density: 0.35 },
    { city: '广州', scale: 6, tech: 72, density: 0.32 },
  ];

  const baseEntity = captured?.sample?.data || {
    taskId: 'PROBE-P023',
    analysisType: 'shenzhen',
    status: 'success',
  };
  const injectedPayload = {
    ...(typeof baseEntity.resultData === 'string'
      ? (() => { try { return JSON.parse(baseEntity.resultData); } catch { return {}; } })()
      : {}),
    cities: injectCities,
  };
  // 清掉可能覆盖的空 compare
  delete injectedPayload.compare;
  delete injectedPayload.sz_compare;

  const fulfillBody = {
    code: captured?.sample?.code ?? 0,
    msg: captured?.sample?.msg ?? 'ok',
    data: {
      ...baseEntity,
      status: 'success',
      resultData: JSON.stringify(injectedPayload),
    },
  };
  out.inject_preview = { cities: injectCities, fulfill_code: fulfillBody.code };

  let fulfilled = 0;
  await page.context().route('**/topicAsync/topic/v1/analysis/tasks/*/result*', async (route) => {
    const req = route.request();
    if (req.method() !== 'GET') return route.continue();
    fulfilled += 1;
    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(fulfillBody),
    });
  });

  // reload 触发再次 GET result
  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(4000);
  await closeBasket();
  // 若 reload 落回 records/配置，再点查看结果
  if (!/view=result/.test(page.url())) {
    const vr = page.getByRole('button', { name: /查看结果/ }).filter({ hasNot: page.locator('.arco-btn-disabled') }).first();
    if (await vr.count()) {
      await vr.click({ timeout: 8000 }).catch(() => {});
      await page.waitForTimeout(3500);
    }
  }
  out.after_inject = await snapChart();
  out.fulfilled = fulfilled;
  out.url_after = page.url();

  // 悬停第一张图北京柱（若有）——可选
  if (out.after_inject?.hasGrid) {
    out.tooltip_probe = await page.evaluate(() => {
      const root = document.querySelector('[data-testid="svc-eco-sz-compare-grid"]');
      if (!root) return null;
      const nodes = root.querySelectorAll('div');
      for (const nd of nodes) {
        try {
          const ec = window.echarts;
          if (!ec || !ec.getInstanceByDom) continue;
          const inst = ec.getInstanceByDom(nd);
          if (!inst) continue;
          const opt = inst.getOption() || {};
          const ser = (opt.series || [])[0] || {};
          const tip = opt.tooltip;
          const fmt = tip && (Array.isArray(tip) ? tip[0]?.formatter : tip.formatter);
          const data = ser.data || [];
          const tips = data.map((d, i) => {
            const value = d && typeof d === 'object' ? d.value : d;
            if (typeof fmt === 'function') {
              try {
                return String(fmt({ name: (Array.isArray(opt.xAxis) ? opt.xAxis[0]?.data?.[i] : opt.xAxis?.data?.[i]) || '', value, data: d }));
              } catch { return null; }
            }
            return value == null ? '无数据' : String(value);
          });
          return { tips, values: data.map((d) => (d && typeof d === 'object' ? d.value : d)) };
        } catch {}
      }
      return null;
    });
  }

  await page.context().unroute('**/topicAsync/topic/v1/analysis/tasks/*/result*').catch(() => {});
  out.ok = true;
} catch (e) {
  out.ok = false;
  out.error = String(e).slice(0, 500);
  try { await page.context().unroute('**/topicAsync/topic/v1/analysis/tasks/*/result*'); } catch {}
}

fs.writeFileSync(path.join(__dirname, '_probe-p023.json'), JSON.stringify(out, null, 2), 'utf8');
await page.screenshot({ path: path.join(__dirname, 'probe-p023-after-inject.png'), fullPage: true }).catch(() => {});
await browser.close();
console.log(JSON.stringify({
  ok: out.ok,
  before_grid: out.before?.hasGrid,
  after_grid: out.after_inject?.hasGrid,
  after_echarts: out.after_inject?.echarts,
  tooltip: out.tooltip_probe,
  fulfilled: out.fulfilled,
  captured: out.captured_result,
  error: out.error,
}, null, 2));
