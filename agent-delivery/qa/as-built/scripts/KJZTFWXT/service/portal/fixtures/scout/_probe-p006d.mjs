#!/usr/bin/env node
/** 一次性探针 d：取「新一代信息技术」产业 id 编码（深链 skip 探测用）+ 深链复证环节空。产物 probe-p006d.json */
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
  await page.goto(new URL('service-portal/overview', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2200);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { await close.first().click().catch(() => {}); await page.waitForTimeout(300); }

  // 选「新一代信息技术」→ 读 URL query
  const ind = page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="全部产业"]') }).first();
  await ind.click(); await page.waitForTimeout(400);
  const opt = page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first();
  report.opt_value = await opt.getAttribute('data-value') || await opt.innerText();
  await opt.click(); await page.waitForTimeout(800);
  report.url_after_pick = page.url();

  // 深链复证：带产业 id 冷进产业分布页，环节卡 5s 探测（模拟 runner skipDetect 口径）
  const m = /[?&]industry=([^&]*)/.exec(page.url());
  const indId = m ? decodeURIComponent(m[1]) : '';
  report.industry_id = indId;
  await page.goto(new URL('service-portal/industry-distribution?industry=' + encodeURIComponent(indId), baseUrl).toString(), { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2500);
  const close2 = page.locator('[aria-label="关闭对比篮"]');
  if ((await close2.count()) && (await close2.first().isVisible().catch(() => false))) { await close2.first().click().catch(() => {}); await page.waitForTimeout(300); }
  report.deeplink_url = page.url();
  report.deeplink_stage_card_count = await page.locator('.svc-portal-stage-card').count();
  report.deeplink_stage_empty = (await page.getByText(/暂无环节分布/).count()) > 0;
  report.deeplink_industry_label_visible = (await page.getByText('新一代信息技术').count()) > 0;
  await page.screenshot({ path: path.join(outDir, 'probe-p006d-deeplink.png') });
  report.overall = 'done';
} catch (err) {
  report.overall = 'error'; report.error = String(err && err.message);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p006d.json'), JSON.stringify(report, null, 2));
  await browser.close();
}
console.log(JSON.stringify(report, null, 2));
