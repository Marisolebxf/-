#!/usr/bin/env node
/**
 * 一次性无头探针 b（P0-06 补证：环节空属环境数据债的对照实验）。
 * 对照面：① 不选产业（默认全产业）时环节区也空？② 六类服务区同条件下有数据（证明页面接口通、仅 stages 无数据）？
 * ③ 直接打 Java 产业分布接口看 stages 字段实包。产物：probe-p006b.json + probe-p006b-*.png
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
const outDir = __dirname;

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const report = { surveyed_at: new Date().toISOString(), steps: [] };
const shot = async (n) => {
  const p = path.join(outDir, `probe-p006b-${n}.png`);
  await page.screenshot({ path: p, fullPage: false });
  return `fixtures/scout/probe-p006b-${n}.png`;
};

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);

  // B1: 直进产业分布（不选产业，默认全产业）
  await page.goto(new URL('service-portal/industry-distribution', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2500);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { await close.first().click().catch(() => {}); await page.waitForTimeout(300); }
  const b1 = {
    url: page.url(),
    h1: await page.locator('h1').allInnerTexts().catch(() => []),
    stage_card_count: await page.locator('.svc-portal-stage-card').count(),
    stage_empty_copy: (await page.getByText(/暂无环节分布/).count()) > 0,
    six_type_heading: (await page.getByRole('heading', { name: /类型分析 · 六类服务分布/ }).count()) > 0,
    six_type_kpi: (await page.getByText(/六类合计/).count()) > 0,
    six_type_chart: (await page.locator('canvas, [_echarts_instance_]').count()) > 0,
  };
  report.steps.push({ id: 'B1-no-industry-default', ...b1, screenshot: await shot('default') });
  console.log('B1:', JSON.stringify(b1));

  // B2: 页面上下文内直接打 Java 产业分布接口（默认 + 选产业两参），看 stages 实包
  const api = await page.evaluate(async () => {
    const get = async (q) => {
      const r = await fetch('/svc/topic/v1/service/portal/industry-distribution' + q, { headers: { 'Content-Type': 'application/json;charset=utf-8' } });
      const t = await r.text();
      let j = null; try { j = JSON.parse(t); } catch (e) {}
      return { status: r.status, j };
    };
    const pick = (r) => {
      const d = r.j && r.j.data !== undefined ? r.j.data : r.j;
      return {
        status: r.status,
        empty: d && d.empty,
        stage_rows: d && Array.isArray(d.stages) ? d.stages.length : null,
        stages_sample: d && Array.isArray(d.stages) ? d.stages.slice(0, 3) : null,
        type_rows: d && Array.isArray(d.by_service_type) ? d.by_service_type.length : null,
        type_sample: d && Array.isArray(d.by_service_type) ? d.by_service_type.slice(0, 2) : null,
      };
    };
    // 默认（全产业）
    const r0 = await get('');
    // 新一代信息技术（INB1701 族编码以现场 catalog 为准，先探一档）
    const r1 = await get('?industry=' + encodeURIComponent('新一代信息技术'));
    return { default: pick(r0), industry_xgdai: pick(r1) };
  });
  report.steps.push({ id: 'B2-api-envelope', ...api });
  console.log('B2:', JSON.stringify(api));

  report.overall = 'done';
} catch (err) {
  report.overall = 'error';
  report.error = String(err && err.message);
  console.error('probe error:', report.error);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p006b.json'), JSON.stringify(report, null, 2));
  await browser.close();
}
