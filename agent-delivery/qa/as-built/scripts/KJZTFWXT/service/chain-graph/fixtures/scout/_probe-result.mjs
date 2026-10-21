#!/usr/bin/env node
/** 补探针：经分析记录「查看结果」看结果壳是否有图/统计。勿当 runner。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const target = `${baseUrl}service/chain-analysis?workspace=graph&tab=graph`;

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
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(2000);
const close = page.locator('[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
  await close.first().click().catch(() => {});
}
await page.getByRole('tab', { name: '分析记录' }).first().click();
await page.waitForTimeout(1500);
await page.getByRole('button', { name: /查看结果/ }).first().click();
await page.waitForTimeout(4000);
await page.screenshot({ path: path.join(__dirname, 'scout-result-deep.png'), fullPage: true });

const info = await page.evaluate(() => {
  const body = (document.body.innerText || '').replace(/\s+/g, ' ').slice(0, 2000);
  const canvas = document.querySelectorAll('canvas').length;
  const svg = document.querySelectorAll('svg').length;
  const g6 = !!document.querySelector('[class*=g6], [class*=graph], [class*=network]');
  const headings = [...document.querySelectorAll('h1,h2,h3,[role=heading]')]
    .map((el) => (el.innerText || '').trim())
    .filter(Boolean)
    .slice(0, 20);
  const dens = /密度|中心性|影响力|图例|投资|合作|竞争|人才/.test(body);
  const emptyHints = /暂无|空|失败|无法|诚实/.test(body);
  return {
    url: location.href,
    title: document.title,
    canvas,
    svg,
    g6_like: g6,
    dens_legend_hit: dens,
    empty_hint: emptyHints,
    headings,
    body_slice: body,
  };
});

fs.writeFileSync(path.join(__dirname, 'scout-result-deep.json'), JSON.stringify(info, null, 2));
await browser.close();
console.log(JSON.stringify({ url: info.url, canvas: info.canvas, svg: info.svg, dens: info.dens_legend_hit, empty: info.empty_hint }, null, 2));
