#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-chain-shortboard P0-06 fresh 路径（FUNC-00690 环节卡内容）。
 * 历史 3 条任务结果态全诚实空（无环节行）→ 本探针 fresh 选「新一代信息技术」起分析，
 * 轮询 120s 看结果态是否渲染环节行/环节卡（环节名/服务类型/机构数/服务深度）。
 * 产物落同目录 scout-p0-06-fresh-*.json / png；勿当 runner。
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
const baseRoute = '/service/chain-analysis?workspace=chain&tab=chain';
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
      await page.waitForTimeout(400);
    } else break;
  }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(200);
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const apiBag = [];
page.on('response', async (r) => {
  try {
    const u = r.url();
    if (/(shortboard|chain|svc)/.test(u) && r.status() < 300 && (r.headers()['content-type'] || '').includes('json')) {
      apiBag.push({ url: u.slice(0, 200), status: r.status(), body: (await r.text().catch(() => '')).slice(0, 1600) });
    }
  } catch {}
});

const out = { probed_at: new Date().toISOString(), timeline: [], error: null };
try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(baseRoute.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  const sel = page.locator('.industry-catalog-select, .arco-select').filter({ has: page.locator('input[placeholder="选择产业集群"]') }).first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(700);
  await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1000);
  await page.getByRole('button', { name: '开始分析', exact: true }).first().click({ timeout: 5000 });
  out.afterStartUrl = page.url();

  let settled = false;
  for (let t = 0; t < 40 && !settled; t++) {
    await page.waitForTimeout(3000);
    const url = page.url();
    const noSt = await page.locator('[data-testid="svc-eco-shortboard-no-stages"]').count();
    const st = await page.locator('[data-stage-id], .svc-eco-metro-station').count();
    const board = await page.locator('[data-testid="svc-eco-shortboard-board"]').count();
    out.timeline.push(`${t * 3}s ${url.replace(baseUrl, '')} board=${board} noStages=${noSt} stations=${st}`);
    if (/view=result/.test(url)) settled = true;
    if (board > 0 && (noSt > 0 || st > 0) && t > 6) settled = true;
  }
  await page.waitForTimeout(2500);
  out.finalUrl = page.url();
  out.bodySlice = ((await page.locator('main').first().innerText().catch(() => '')) || '').slice(0, 2600);
  const noStLoc = page.locator('[data-testid="svc-eco-shortboard-no-stages"]');
  out.noStagesVisible = (await noStLoc.count()) > 0 && (await noStLoc.first().isVisible().catch(() => false));
  out.stationCount = await page.locator('[data-stage-id], .svc-eco-metro-station').count();
  await page.screenshot({ path: path.join(outDir, 'scout-p0-06-fresh.png'), fullPage: false }).catch(() => {});
} catch (e) {
  out.error = String(e).slice(0, 400);
}
out.apiResponses = apiBag.slice(-6);
dump('scout-p0-06-fresh-summary.json', out);
await browser.close();
console.log('fresh probe done:', JSON.stringify({ finalUrl: out.finalUrl, noStages: out.noStagesVisible, stations: out.stationCount, error: out.error || null }));
