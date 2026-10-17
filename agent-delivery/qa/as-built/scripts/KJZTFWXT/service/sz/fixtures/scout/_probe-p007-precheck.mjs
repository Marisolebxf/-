#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-sz P0-07 补充核实：
 *  a) SVC-20261015-011 的分析对象（排除当天复用对 INB1701 主路径的干扰）
 *  b) INB1701 配置页当日干净态（无「重新分析/今天已分析」门控、开始分析 enabled）
 * 不点「开始分析」。
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
const route = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const outDir = __dirname;
const dump = (name, data) => fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2), 'utf8');

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
async function closeBasket(page) {
  for (let i = 0; i < 3; i++) {
    const close = page.locator('[aria-label="关闭对比篮"]');
    if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
      await close.first().click().catch(() => {});
      await page.waitForTimeout(300);
    } else break;
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = {};

await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
if (page.url().includes('/login')) { await ensureLogin(page); await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded' }); }
await page.waitForTimeout(2500);
await closeBasket(page);

// a) 记录页找 SVC-20261015-011 行 → 查看过程 → 分析对象
try {
  await page.getByRole('tab', { name: '分析记录', exact: true }).first().click();
  await page.waitForTimeout(2000);
  const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: 'SVC-20261015-011' }).first();
  out.row_011_found = await row.count();
  if (out.row_011_found) {
    await row.getByRole('button', { name: /查看过程/ }).first().click({ timeout: 8000 });
    await page.waitForTimeout(2500);
    const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    out.task_011 = {
      url: page.url(),
      analysis_object_line: (body.split('\n').find((l) => /分析对象/.test(l)) || '').trim(),
      status_line: (body.split('\n').find((l) => /任务状态/.test(l)) || '').trim(),
    };
  }
} catch (e) { out.a_error = String(e).slice(0, 300); }

// b) 回配置页选「新一代信息技术」（不点开始分析）
try {
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2000);
  await closeBasket(page);
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
  await page.waitForTimeout(2500);
  const cfgText = ((await page.locator('[data-testid="svc-eco-analysis-config"]').innerText().catch(() => '')) || '');
  out.inb1701_config = {
    url: page.url(),
    echo: ((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim(),
    config_snippet: cfgText.replace(/\n/g, ' | ').slice(0, 400),
    start_btn_n: await page.getByRole('button', { name: '开始分析', exact: true }).count(),
    start_enabled: await page.getByRole('button', { name: '开始分析', exact: true }).first().isEnabled().catch(() => null),
    rerun_btn_n: await page.getByRole('button', { name: '重新分析', exact: true }).count(),
    today_hint: /今天|当天|已成功|已分析/.test(cfgText),
    gate_inflight: /同条件已有进行中任务/.test(cfgText),
  };
  await page.screenshot({ path: path.join(outDir, 'scout-p007-inb1701-clean.png'), fullPage: false });
} catch (e) { out.b_error = String(e).slice(0, 300); }

dump('scout-p007-inb1701-precheck.json', out);
await browser.close();
console.log('precheck done', JSON.stringify(out, null, 2));
