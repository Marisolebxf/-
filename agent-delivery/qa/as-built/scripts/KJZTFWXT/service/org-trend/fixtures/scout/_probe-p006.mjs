/**
 * P0-06（FUNC-00660 趋势图默认呈现）一次性无头探针。产物 scout-p006-series.json；勿当 runner。
 * 目标：结果壳可达；诚实空 / 有年序列；canvas/_echarts；图例；主领域年度明细。
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
const deeplink = `${baseUrl.replace(/\/?$/, '')}/service/institution-judgment?workspace=trend&tab=records&view=result&demo_state=result`;
const outPath = path.join(__dirname, 'scout-p006-series.json');

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
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(deeplink, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(2500);
await closeBasket(page);

const out = { probed_at: new Date().toISOString(), url_deeplink: page.url() };
let body = ((await page.locator('main').first().innerText().catch(() => '')) || '');

if (!(/view=result/.test(page.url()) && /服务机构新增数量趋势/.test(body))) {
  const recTab = page.locator('[role=tab][data-tab-key="records"]');
  if (await recTab.count()) {
    await recTab.click({ timeout: 8000 });
    await page.waitForTimeout(1200);
  }
  const vr = page.getByRole('button', { name: '查看结果' }).first();
  if (await vr.count()) {
    await vr.click({ timeout: 8000 });
    await page.waitForTimeout(2500);
  }
  body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
}

out.url_result = page.url();
out.has_trend_title = /服务机构新增数量趋势/.test(body);
out.honest_empty = /当前结果快照没有年序列/.test(body);
out.detail_empty = /暂无主领域年度明细/.test(body);
out.has_detail_label = /主领域年度明细/.test(body);
out.time_windows = ['近 3 年', '近 5 年', '近 8 年'].filter((t) => body.includes(t));
out.canvas = await page.locator('main canvas, main [_echarts_instance_]').count().catch(() => 0);
out.legend_btn = await page.locator('.svc-org-trend__legend button').count().catch(() => 0);
out.legend_visible = await page.locator('.svc-org-trend__legend button').first().isVisible().catch(() => false);
out.board = await page.locator('[data-testid=svc-org-trend-board]').count().catch(() => 0);
out.detail_rows = await page.locator('main table tbody tr, main .arco-table-tr').count().catch(() => 0);
out.body_slice = body.replace(/\s+/g, ' ').slice(0, 500);

fs.writeFileSync(outPath, JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
