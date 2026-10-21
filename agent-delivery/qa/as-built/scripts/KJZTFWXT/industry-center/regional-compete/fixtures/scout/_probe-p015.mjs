#!/usr/bin/env node
/** P0-15 写前无头实勘：两类已完成结果壳 GIS / 待补 / 模式文案。勿当 runner。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const tasks = ['CHAIN-20260911-010', 'CHAIN-20260907-001'];
const out = { surveyed_at: new Date().toISOString(), purpose: 'P0-15-GIS-condition', tasks: {} };

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
  }
}

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();

await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);

for (const tid of tasks) {
  const url = `/industry-center/regional?view=result&task_id=${tid}&tab=competitiveness&workspace=competitiveness`;
  await page.goto(new URL(url.replace(/^\//, ''), baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  if (page.url().includes('/login')) {
    await ensureLogin(page);
    await page.goto(new URL(url.replace(/^\//, ''), baseUrl).toString(), {
      waitUntil: 'domcontentloaded',
      timeout: 60000,
    });
  }
  await page.waitForTimeout(4500);
  await closeBasket(page);
  const root = page.locator('main.diagnosis-main').first();
  const visible = await root.isVisible().catch(() => false);
  const main = visible ? await root.innerText() : await page.locator('main').first().innerText().catch(() => '');
  const leaflet = await page.locator('.leaflet-container').count();
  const mapLike = await page.locator('.leaflet-container, #map, [class*="map"]').count();
  const canvas = await page.locator('main canvas, main [_echarts_instance_]').count();
  out.tasks[tid] = {
    url: page.url(),
    rootVisible: visible,
    leaflet,
    mapLike,
    canvas,
    hasGisWord: /地图|GIS|Leaflet|天地图/.test(main),
    hasHeatWord: /热力/.test(main),
    hasPending: /待补|未返回|暂无/.test(main),
    hasModeSingle: /单产业\s*[×x]\s*多区域/.test(main),
    hasModeMulti: /多产业\s*[×x]\s*单区域/.test(main),
    hasFirstPlace: /第\s*1\s*名|第一名/.test(main),
    snip: main.replace(/\s+/g, ' ').slice(0, 900),
  };
}

fs.writeFileSync(path.join(__dirname, 'scout-p015-gis.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
