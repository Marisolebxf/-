#!/usr/bin/env node
/** 一次性探针 P0-11（FUNC-01315 圆点点选联动）：区域分布页圆点形态/大小梯度/图例/点选联动/右侧列表形态 实测。产物 probe-p011.json + 2 截图 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
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

  // 直进区域分布页（P0-04 既有口径：深链 /service-portal/region-map），顺带抓 region-map 接口响应
  const respPromise = page.waitForResponse((r) => /region-map/.test(r.url()), { timeout: 15000 }).catch(() => null);
  await page.goto(new URL('service-portal/region-map', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2500);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { await close.first().click().catch(() => {}); await page.waitForTimeout(300); }
  report.url = page.url();

  // ① region-map 接口数据态（干净证据：行数/坐标字段有无）
  const resp = await respPromise;
  if (resp) {
    report.api = { url: resp.url(), status: resp.status() };
    try {
      const body = await resp.json();
      const d = body && body.data ? body.data : body;
      const cnt = (arr) => (Array.isArray(arr) ? arr.length : null);
      const sample = (arr) => (Array.isArray(arr) && arr.length ? arr[0] : null);
      report.api.china_rows = cnt(d && d.china);
      report.api.global_rows = cnt(d && d.global);
      report.api.geo_level_used = d && d.geo_level_used;
      report.api.china_first = sample(d && d.china);
      report.api.global_first = sample(d && d.global);
      report.api.empty = d && d.empty;
    } catch (e) { report.api.body_parse_error = String(e && e.message); }
  } else report.api = null;

  // ② 地图圆点形态（Leaflet circleMarker → .leaflet-overlay-pane svg path）
  await page.waitForTimeout(1200);
  const dots = page.locator('.leaflet-overlay-pane svg path');
  report.dot_count = await dots.count();
  report.map_empty_text = (await page.getByText(/Java 区域分布无坐标字段|暂无已出区域/).count()) > 0;
  report.legend_text_count = await page.getByText(/图例|梯度|机构数.*大小|大小.*机构数/).count();
  await page.screenshot({ path: path.join(outDir, 'probe-p011-region.png') });

  // ③ 圆点 bbox（半径代理）与大小梯度可断性
  if (report.dot_count > 0) {
    const sizes = [];
    const n = Math.min(report.dot_count, 12);
    for (let i = 0; i < n; i++) {
      const bb = await dots.nth(i).boundingBox().catch(() => null);
      sizes.push(bb ? { w: Math.round(bb.width * 10) / 10, h: Math.round(bb.height * 10) / 10 } : null);
    }
    report.dot_boxes = sizes;
  }

  // ④ 右侧列表形态（ECharts 条形图 vs DOM 行）
  report.right_chart_canvas = await page.locator('.svc-portal-chart--region canvas').count();
  report.right_dom_rows = await page.locator('.svc-portal-region-grid li, .svc-portal-region-grid [class*=row]').count();

  // ⑤ 点选圆点实测联动（若 ≥1 点）
  if (report.dot_count > 0) {
    const first = dots.first();
    const bb = await first.boundingBox();
    report.click_box = bb ? { x: Math.round(bb.x + bb.width / 2), y: Math.round(bb.y + bb.height / 2) } : null;
    const mainLenBefore = (await page.locator('main').innerHTML().catch(() => '')).length;
    const drawerBefore = await page.locator('.arco-drawer').count();
    await page.mouse.click(report.click_box.x, report.click_box.y);
    await page.waitForTimeout(1200);
    const mainLenAfter = (await page.locator('main').innerHTML().catch(() => '')).length;
    report.after_click = {
      url_changed: page.url() !== report.url,
      drawer_count: await page.locator('.arco-drawer').count(),
      drawer_before: drawerBefore,
      main_html_len_before: mainLenBefore,
      main_html_len_after: mainLenAfter,
      main_html_changed: mainLenBefore !== mainLenAfter,
      aria_selected_count: await page.locator('[aria-selected=true]').count(),
      highlight_class_count: await page.locator('main [class*=highlight], main [class*=active], main [class*=selected]').count(),
    };
    await page.screenshot({ path: path.join(outDir, 'probe-p011-after-click.png') });
  }
  report.overall = 'done';
} catch (err) {
  report.overall = 'error'; report.error = String(err && err.message);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p011.json'), JSON.stringify(report, null, 2));
  await browser.close();
}
console.log(JSON.stringify(report, null, 2));
