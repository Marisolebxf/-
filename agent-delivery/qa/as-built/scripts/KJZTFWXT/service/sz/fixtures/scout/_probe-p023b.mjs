#!/usr/bin/env node
/** _probe-p023b — 深验 ECharts 实例挂点 + 「无数据」label/value */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://111.198.38.90:50892';
const injectCities = [
  { city: '深圳', scale: 9, tech: 80, density: 0.4 },
  { city: '全国平均', scale: 5, tech: 70, density: 0.3 },
  { city: '北京' },
  { city: '上海', scale: 7, tech: 75, density: 0.35 },
  { city: '广州', scale: 6, tech: 72, density: 0.32 },
];

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
    await page.waitForTimeout(2000);
  }
}
if (page.url().includes('/login')) {
  console.log(JSON.stringify({ error: 'login_failed', url: page.url() }));
  await browser.close();
  process.exit(1);
}

let hit = 0;
await page.context().route('**/topicAsync/topic/v1/analysis/tasks/*/result*', async (route) => {
  if (route.request().method() !== 'GET') return route.continue();
  hit += 1;
  return route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      code: 0,
      msg: 'ok',
      data: {
        taskId: 'SVC-20261015-085',
        analysisType: 'shenzhen',
        status: 'success',
        resultData: JSON.stringify({ cities: injectCities }),
      },
    }),
  });
});

await page.goto(
  BASE + '/service/chain-analysis?workspace=shenzhen&tab=records&view=result&demo_state=result&task_id=SVC-20261015-085',
  { waitUntil: 'domcontentloaded' },
);
await page.waitForTimeout(5000);
const close = page.locator('button[aria-label="关闭对比篮"]');
if (await close.count() && await close.first().isVisible().catch(() => false)) {
  try { await close.first().click({ timeout: 1200 }); } catch {}
}

const info = await page.evaluate(() => {
  const out = {
    canvas: document.querySelectorAll('[data-testid="svc-eco-sz-compare"] canvas').length,
    grid: !!document.querySelector('[data-testid="svc-eco-sz-compare-grid"]'),
    winEcharts: typeof window.echarts,
    echartsKeys: window.echarts ? Object.keys(window.echarts).slice(0, 20) : [],
    charts: [],
  };
  const cells = [...document.querySelectorAll('.svc-eco-compare-cell')];
  for (const cell of cells) {
    const head = (cell.querySelector('.svc-eco-compare-cell__head')?.innerText || '').trim().slice(0, 40);
    const chartEl = cell.querySelector('.svc-eco-compare-cell__chart') || cell;
    const canvas = cell.querySelector('canvas');
    const candidates = [chartEl, canvas, canvas?.parentElement, cell].filter(Boolean);
    let inst = null;
    let how = '';
    const ec = window.echarts;
    if (ec && ec.getInstanceByDom) {
      for (const c of candidates) {
        try {
          const i = ec.getInstanceByDom(c);
          if (i) { inst = i; how = 'getInstanceByDom'; break; }
        } catch {}
      }
    }
    // _echarts_instance_ attribute
    if (!inst && ec) {
      for (const c of candidates) {
        const id = c.getAttribute && c.getAttribute('_echarts_instance_');
        if (id && ec.getInstanceById) {
          try { inst = ec.getInstanceById(id); how = 'getInstanceById:' + id; } catch {}
          if (inst) break;
        }
      }
    }
    // vue-echarts internal
    if (!inst) {
      for (const c of candidates) {
        if (c.__vueParentComponent?.exposed?.getEchartsInstance) {
          try { inst = c.__vueParentComponent.exposed.getEchartsInstance(); how = 'vue-exposed'; } catch {}
        }
        if (inst) break;
        const vn = c.__vueParentComponent || c.__vue_app__;
        if (vn?.ctx?.chart || vn?.setupState?.chart) {
          inst = vn.ctx?.chart || vn.setupState?.chart;
          how = 'vue-ctx';
          break;
        }
      }
    }
    if (!inst) {
      out.charts.push({
        head,
        noInst: true,
        canvasW: canvas?.width,
        attrs: chartEl.getAttributeNames?.() || [],
        html: chartEl.outerHTML?.slice(0, 180),
      });
      continue;
    }
    const opt = inst.getOption() || {};
    const xa = opt.xAxis;
    const cats = Array.isArray(xa) ? (xa[0] && xa[0].data) : (xa && xa.data);
    const ser = (opt.series || [])[0] || {};
    const data = (ser.data || []).map((d) => (d && typeof d === 'object' ? d.value : d));
    const labels = (ser.data || []).map((d) => {
      try {
        if (d && d.label && typeof d.label.formatter === 'function') return String(d.label.formatter());
      } catch {}
      return d && typeof d === 'object' && d.value == null ? '无数据' : String(d && typeof d === 'object' ? d.value : d);
    });
    out.charts.push({
      head,
      how,
      cities: Array.isArray(cats) ? cats.map(String) : [],
      values: data,
      labels,
      nullN: data.filter((v) => v == null).length,
      zeroN: data.filter((v) => v === 0).length,
      hasWushujuLabel: labels.some((l) => /无数据/.test(String(l))),
    });
  }
  // also dump all _echarts_instance_ in DOM
  out.instAttrs = [...document.querySelectorAll('[_echarts_instance_]')].map((el) => ({
    tag: el.tagName,
    cls: el.className,
    id: el.getAttribute('_echarts_instance_'),
  }));
  return out;
});

const out = { hit, info, url: page.url() };
fs.writeFileSync(path.join(__dirname, '_probe-p023b.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await page.context().unroute('**/topicAsync/topic/v1/analysis/tasks/*/result*').catch(() => {});
await browser.close();
