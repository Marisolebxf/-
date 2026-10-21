#!/usr/bin/env node
/** 一次性诊断 · 分段落盘：逐段 console.log + 落 JSON，卡死也知道卡哪段。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const out = {};
const flush = () => fs.writeFileSync(path.join(__dirname, 'scout-p013-r1-diagnosis.json'), JSON.stringify(out, null, 2));
const log = (tag, data) => { out[tag] = data; flush(); console.log('[' + tag + ']', typeof data === 'object' ? JSON.stringify(data).slice(0, 200) : data); };

const baseUrl = 'http://10.50.69.111:30892/';
const route = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
process.on('uncaughtException', (e) => { log('uncaught', String(e).slice(0, 300)); process.exit(1); });
process.on('unhandledRejection', (e) => { log('unhandled', String(e).slice(0, 300)); process.exit(1); });

const browser = await chromium.launch({ headless: true });
log('launched', true);
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
log('ctx', true);

// 复现 runner ensureLogin
await page.goto(baseUrl + '/', { waitUntil: 'domcontentloaded', timeout: 30000 });
log('goto_root', page.url());
await page.waitForTimeout(800);
log('after_800', page.url());
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin', { timeout: 8000 });
  await page.locator('input[type=password]').first().fill('123456', { timeout: 8000 });
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1200);
  if (page.url().includes('/login')) {
    await page.locator('button[type=submit], button:has-text("登录"), button:has-text("登 录")').first().click({ timeout: 8000 }).catch(() => {});
  }
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 10000 });
}
log('logged_in', page.url());

// goto 路由
await page.goto(baseUrl + route, { waitUntil: 'domcontentloaded', timeout: 30000 });
log('goto_route', page.url());
await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {});
log('networkidle', page.url());
await page.waitForTimeout(600);
log('settled', page.url());

// census
const cnt = async (sel) => page.locator(sel).count();
log('census_t0', {
  framework: await cnt('[data-testid="svc-eco-sz-framework"]'),
  compare: await cnt('[data-testid="svc-eco-sz-compare-metrics"]'),
  empty: await cnt('[data-testid="svc-eco-sz-compare-empty"]'),
  tier: await cnt('[data-testid="svc-eco-sz-tier"]'),
});
const body0 = ((await page.locator('main').first().innerText().catch(() => '')) || '');
log('body_t0', { len: body0.length, head: body0.replace(/\n/g, '|').slice(0, 120), has_shenzhen: /shenzhen/.test(body0) });

// 复现 expect[0]：关对比篮 → tab records → 行 → 查看结果
const close = page.locator('button[aria-label="关闭对比篮"]');
if (await close.count() && await close.first().isVisible().catch(() => false)) {
  try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
}
log('basket', 'done');
const rec = page.locator('[role=tab][data-tab-key="records"]').or(page.getByRole('tab', { name: '分析记录', exact: true }));
log('rec_count', await rec.count());
await rec.first().isVisible({ timeout: 8000 }).catch((e) => log('rec_vis_err', String(e.message).slice(0, 120)));
await rec.first().click({ timeout: 8000 });
log('rec_clicked', page.url());
await page.waitForURL(/tab=records/, { timeout: 8000 }).catch(() => log('wait_url_timeout', page.url()));
await page.waitForTimeout(1000);
const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
log('records_body', { url: page.url(), has_shenzhen: /shenzhen/.test(body), has_done: /已完成/.test(body), head: body.replace(/\n/g, '|').slice(0, 200) });

const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /shenzhen/ }).filter({ hasText: /已完成/ }).filter({ has: page.getByRole('button', { name: /查看结果/ }) }).first();
log('row_count', await row.count());
const viewBtn = row.getByRole('button', { name: /查看结果/ }).filter({ hasNot: page.locator('.arco-btn-disabled') }).first();
await viewBtn.click({ timeout: 8000 });
await page.waitForTimeout(3000);
log('after_view', { url: page.url(), framework: await cnt('[data-testid="svc-eco-sz-framework"]'), compare: await cnt('[data-testid="svc-eco-sz-compare-metrics"]') });

// 直接复现 expect[1] 首行
const cmp = page.locator('[data-testid="svc-eco-sz-compare-metrics"]');
const vis = await cmp.first().isVisible().catch(() => false);
log('cmp_vis_sync', vis);
let visPoll = false;
for (let i = 0; i < 20; i++) { if (await cmp.first().isVisible().catch(() => false)) { visPoll = true; break; } await new Promise((r) => setTimeout(r, 400)); }
log('cmp_vis_poll', visPoll);
const boxes = cmp.locator('.arco-checkbox');
log('boxes', await boxes.count());

await browser.close();
log('done', true);
console.log('ALL DONE');
