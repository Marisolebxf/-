#!/usr/bin/env node
/** 探针 c：P0-11 深勘——诚实空文案 / leaflet 圆点 / 全国视图 / in-page POST region-map。产物 probe-p011c.json + probe-p011c-region.png */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const outDir = __dirname;

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
const report = {};
try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

  await page.goto(new URL('service-portal/region-map', baseUrl).toString(), { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  await page.waitForTimeout(3000);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { await close.first().click().catch(() => {}); await page.waitForTimeout(300); }

  report.url = page.url();
  report.h1 = await page.locator('main').getByRole('heading').allTextContents().catch(() => []);
  report.views = {
    global: await page.getByText('全球视图', { exact: true }).count(),
    china: await page.getByText('全国视图', { exact: true }).count(),
  };
  const emptyCandidates = ['Java 区域分布无坐标字段', '暂无已出区域', '无坐标', '暂无区域', '地图暂无'];
  report.empty_hits = {};
  for (const t of emptyCandidates) {
    report.empty_hits[t] = await page.getByText(new RegExp(t)).count();
  }
  const mainText = await page.locator('main').innerText().catch(() => '');
  report.main_snip = mainText.slice(0, 800).replace(/\n+/g, ' | ');
  report.dot_path = await page.locator('.leaflet-overlay-pane svg path').count();
  report.dot_circle = await page.locator('.leaflet-overlay-pane svg circle, .leaflet-marker-icon').count();
  report.leaflet_pane = await page.locator('.leaflet-container').count();
  report.rank_h3 = await page.locator('main').getByRole('heading', { name: /省级行政区排行/ }).count();
  report.guangdong = await page.locator('main').getByText(/广东省|广东/).count();
  report.legend = await page.getByText(/图例|梯度|机构数/).allTextContents().catch(() => []);
  report.canvas = await page.locator('main canvas').count();

  const chinaBtn = page.getByText('全国视图', { exact: true }).first();
  if (await chinaBtn.isVisible().catch(() => false)) {
    await chinaBtn.click();
    await page.waitForTimeout(2000);
    report.after_china = {
      url: page.url(),
      dot_path: await page.locator('.leaflet-overlay-pane svg path').count(),
      empty_coord: await page.getByText(/无坐标|暂无已出区域|Java 区域分布/).count(),
      main_snip: ((await page.locator('main').innerText().catch(() => '')) || '').slice(0, 500).replace(/\n+/g, ' | '),
    };
  }

  report.api = await page.evaluate(async () => {
    const r = await fetch('/svc/topic/v1/service-portal/region-map', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
    const j = await r.json();
    const d = j.data || j;
    const first = (d.china && d.china[0]) || null;
    return {
      status: r.status,
      empty: d.empty,
      china_n: Array.isArray(d.china) ? d.china.length : null,
      global_n: Array.isArray(d.global) ? d.global.length : null,
      china_first_keys: first ? Object.keys(first) : null,
      china_first: first,
      gap: d.gap,
    };
  });

  await page.screenshot({ path: path.join(outDir, 'probe-p011c-region.png') });
  report.overall = 'done';
} catch (err) {
  report.overall = 'error'; report.error = String(err && err.message);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p011c.json'), JSON.stringify(report, null, 2));
  await browser.close();
}
console.log(JSON.stringify(report, null, 2));
