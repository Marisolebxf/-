#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-sz P0-07 诊断：同日同条件（INB1701 已完成）再次点「开始分析」的现场行为。
 * 产物 scout-p007-second-inb1701.json。不产生新断言口径，只为归因。
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
const out = { steps: [] };

// 记录 POST /analysis/tasks 是否发生（判断点击是否真的发起创建）
let createPosts = 0;
page.on('request', (r) => { if (r.method() === 'POST' && /\/analysis\/tasks\/?(\?|$)/.test(r.url())) createPosts++; });

await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
if (page.url().includes('/login')) { await ensureLogin(page); await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded' }); }
await page.waitForTimeout(2500);
await closeBasket(page);

try {
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  out.url_after_pick = page.url();
  out.echo = ((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
  const cfg = ((await page.locator('[data-testid="svc-eco-analysis-config"]').innerText().catch(() => '')) || '');
  out.config_snippet = cfg.replace(/\n/g, ' | ').slice(0, 500);
  out.start_enabled = await page.getByRole('button', { name: '开始分析', exact: true }).first().isEnabled();
  const before = createPosts;
  await page.getByRole('button', { name: '开始分析', exact: true }).first().click({ timeout: 8000 });
  // 15s 观察：URL / toast / alert / DOM
  for (let i = 0; i < 15; i++) {
    await page.waitForTimeout(1000);
    const url = page.url();
    const msg = await page.locator('.arco-message, .arco-notification, .arco-alert').allInnerTexts().catch(() => []);
    const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    out.steps.push({
      t: i + 1,
      url: url.replace(baseUrl, ''),
      toast: msg.map((s) => s.trim()).filter(Boolean),
      generating: /生成中/.test(body),
      done: /分析结果已生成/.test(body),
      view_result_btn: await page.getByRole('button', { name: '查看结果', exact: true }).count(),
    });
    if (/[?&]view=/.test(url)) break;
  }
  if (out.steps.length <= 2) await page.screenshot({ path: path.join(outDir, 'scout-p007-second-inb1701.png'), fullPage: false });
  out.create_posts_after_click = createPosts - before;
} catch (e) { out.error = String(e).slice(0, 400); }

dump('scout-p007-second-inb1701.json', out);
await browser.close();
console.log('second-start diag done', JSON.stringify({ posts: out.create_posts_after_click, last: out.steps.at(-1), err: out.error || null }, null, 2));
