#!/usr/bin/env node
/** _probe-p023c — 登录稳 + inject cities + 从 vue-echarts / tooltip DOM 读「无数据」 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
const SZ = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const injectCities = [
  { city: '深圳', scale: 9, tech: 80, density: 0.4 },
  { city: '全国平均', scale: 5, tech: 70, density: 0.3 },
  { city: '北京' }, // 缺值 → null → 「无数据」
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
const logged_in = !page.url().includes('/login');

const closeBasket = async () => {
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if (await close.count() && await close.first().isVisible().catch(() => false) && await close.first().isEnabled().catch(() => false)) {
    try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
  }
};

let hit = 0;
let capturedKeys = null;
await page.context().route('**/topicAsync/topic/v1/analysis/tasks/*/result*', async (route) => {
  const req = route.request();
  if (req.method() !== 'GET') return route.continue();
  hit += 1;
  // 透传一次拿包络再改？直接 fulfill 最小包即可（_probe-p023 已证 grid 出）
  return route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      code: 0,
      msg: 'ok',
      data: {
        taskId: 'SVC-INJECT-P023',
        analysisType: 'shenzhen',
        status: 'success',
        resultData: JSON.stringify({ cities: injectCities }),
      },
    }),
  });
});

const out = { probed_at: new Date().toISOString(), logged_in, injectCities };

try {
  if (!logged_in) throw new Error('login failed');
  await page.goto(BASE + SZ, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await closeBasket();
  const rec = page.locator('[role=tab][data-tab-key="records"]').or(page.getByRole('tab', { name: '分析记录', exact: true }));
  await rec.first().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /shenzhen/ }).filter({ hasText: /已完成/ }).filter({ has: page.getByRole('button', { name: /查看结果/ }) }).first();
  await row.getByRole('button', { name: /查看结果/ }).filter({ hasNot: page.locator('.arco-btn-disabled') }).first().click({ timeout: 8000 });
  await page.waitForTimeout(4000);
  await closeBasket();
  out.url = page.url();
  out.hit = hit;
  out.before_empty = (await page.locator('[data-testid="svc-eco-sz-compare-empty"]').count()) > 0;
  out.after_grid = (await page.locator('[data-testid="svc-eco-sz-compare-grid"]').count()) > 0
    && await page.locator('[data-testid="svc-eco-sz-compare-grid"]').first().isVisible().catch(() => false);
  out.canvasN = await page.locator('[data-testid="svc-eco-sz-compare"] canvas').count();
  out.caliber = ((await page.locator('[data-testid="svc-eco-sz-compare-caliber"]').innerText().catch(() => '')) || '').trim();

  // 从 vue-echarts 组件读 option
  out.vueCharts = await page.evaluate(() => {
    const cells = [...document.querySelectorAll('.svc-eco-compare-cell')];
    return cells.map((cell) => {
      const head = (cell.querySelector('.svc-eco-compare-cell__head')?.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 40);
      const chartRoot = cell.querySelector('.svc-eco-compare-cell__chart');
      if (!chartRoot) return { head, err: 'no-chart-root' };
      // walk vue fiber
      let comp = chartRoot.__vueParentComponent;
      let option = null;
      let how = '';
      for (let i = 0; i < 8 && comp; i++) {
        const exp = comp.exposed || {};
        const setup = comp.setupState || {};
        const ctx = comp.ctx || {};
        const candidates = [
          typeof exp.getEchartsInstance === 'function' ? exp.getEchartsInstance() : null,
          setup.chart,
          ctx.chart,
          exp.chart,
        ];
        for (const c of candidates) {
          if (c && typeof c.getOption === 'function') {
            option = c.getOption();
            how = 'vue-instance';
            break;
          }
        }
        if (option) break;
        // props.option 直接是我们传入的 EChartsOption（含 label.formatter 闭包）
        if (comp.props && comp.props.option) {
          option = comp.props.option;
          how = 'vue-props-option';
          break;
        }
        comp = comp.parent;
      }
      if (!option) {
        // dump keys for diagnosis
        const c0 = chartRoot.__vueParentComponent;
        return {
          head,
          err: 'no-option',
          vueKeys: c0 ? Object.keys(c0) : [],
          exposed: c0?.exposed ? Object.keys(c0.exposed) : [],
          setupKeys: c0?.setupState ? Object.keys(c0.setupState) : [],
          propKeys: c0?.props ? Object.keys(c0.props) : [],
        };
      }
      const xa = option.xAxis;
      const cats = Array.isArray(xa) ? (xa[0] && xa[0].data) : (xa && xa.data);
      const ser = (option.series || [])[0] || {};
      const raw = ser.data || [];
      const values = raw.map((d) => (d && typeof d === 'object' ? d.value : d));
      const labels = raw.map((d) => {
        try {
          if (d && d.label && typeof d.label.formatter === 'function') return String(d.label.formatter());
        } catch (e) {
          return 'fmt-err:' + String(e).slice(0, 40);
        }
        if (d && typeof d === 'object' && d.value == null) return '无数据';
        return String(d && typeof d === 'object' ? d.value : d);
      });
      return {
        head,
        how,
        cities: Array.isArray(cats) ? cats.map(String) : [],
        values,
        labels,
        nullN: values.filter((v) => v == null).length,
        zeroN: values.filter((v) => v === 0).length,
        beijingIdx: Array.isArray(cats) ? cats.map(String).indexOf('北京') : -1,
        beijingValue: (() => {
          const i = Array.isArray(cats) ? cats.map(String).indexOf('北京') : -1;
          return i >= 0 ? values[i] : undefined;
        })(),
        beijingLabel: (() => {
          const i = Array.isArray(cats) ? cats.map(String).indexOf('北京') : -1;
          return i >= 0 ? labels[i] : undefined;
        })(),
      };
    });
  });

  // 悬停第一张图约北京柱位（第 3 列，五城均分）
  if (out.after_grid && out.canvasN > 0) {
    const box = await page.locator('.svc-eco-compare-cell__chart').first().boundingBox();
    if (box) {
      // 北京是第 3 城（0-index 2），五城均分 x：约 left + width*(2.5/5)
      const x = box.x + box.width * (2.5 / 5);
      const y = box.y + box.height * 0.55;
      await page.mouse.move(x, y);
      await page.waitForTimeout(800);
      out.tooltip_text = await page.evaluate(() => {
        const tips = [...document.querySelectorAll('div')].filter((el) => {
          const s = getComputedStyle(el);
          return (s.position === 'absolute' || s.position === 'fixed')
            && el.innerText && /无数据|北京|深圳/.test(el.innerText)
            && el.offsetWidth > 20 && el.offsetHeight > 10
            && el.offsetWidth < 400;
        }).map((el) => el.innerText.trim().slice(0, 80));
        return tips.slice(0, 8);
      });
    }
  }

  out.ok = true;
} catch (e) {
  out.ok = false;
  out.error = String(e).slice(0, 500);
}

await page.screenshot({ path: path.join(__dirname, 'probe-p023c.png'), fullPage: true }).catch(() => {});
await page.context().unroute('**/topicAsync/topic/v1/analysis/tasks/*/result*').catch(() => {});
fs.writeFileSync(path.join(__dirname, '_probe-p023c.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify({
  ok: out.ok,
  hit: out.hit,
  grid: out.after_grid,
  canvasN: out.canvasN,
  vueCharts: out.vueCharts,
  tooltip: out.tooltip_text,
  error: out.error,
}, null, 2));
await browser.close();
