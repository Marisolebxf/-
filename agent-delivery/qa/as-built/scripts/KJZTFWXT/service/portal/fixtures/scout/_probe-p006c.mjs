#!/usr/bin/env node
/**
 * 一次性无头探针 c（P0-06 补证收口：POST 正确端点看 stages 实包）。
 * B2 用 GET 打错端点（424）；前端真源 = POST /svc/topic/v1/service-portal/industry-distribution。
 * 产物：probe-p006c.json
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
const report = { surveyed_at: new Date().toISOString() };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL('service-portal/industry-distribution', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2000);

  // 抓现场页面真实请求（页面自身会发 POST），同时主动 POST 两参对照
  const api = await page.evaluate(async () => {
    const post = async (body) => {
      const r = await fetch('/svc/topic/v1/service-portal/industry-distribution', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8' },
        body: JSON.stringify(body || {}),
      });
      const t = await r.text();
      let j = null; try { j = JSON.parse(t); } catch (e) {}
      const d = j && j.data !== undefined ? j.data : j;
      return {
        status: r.status,
        empty: d && d.empty,
        stage_rows: d && Array.isArray(d.stages) ? d.stages.length : null,
        stages_sample: d && Array.isArray(d.stages) ? d.stages.slice(0, 3) : null,
        type_rows: d && Array.isArray(d.by_service_type) ? d.by_service_type.length : null,
        type_sample: d && Array.isArray(d.by_service_type) ? d.by_service_type.slice(0, 2) : null,
        raw_head: (t || '').slice(0, 200),
      };
    };
    return {
      default_no_industry: await post({}),
      industry_xgdai: await post({ industry: '新一代信息技术' }),
    };
  });
  Object.assign(report, api);
  console.log(JSON.stringify(api, null, 2));
  report.overall = 'done';
} catch (err) {
  report.overall = 'error';
  report.error = String(err && err.message);
  console.error('probe error:', report.error);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p006c.json'), JSON.stringify(report, null, 2));
  await browser.close();
}
