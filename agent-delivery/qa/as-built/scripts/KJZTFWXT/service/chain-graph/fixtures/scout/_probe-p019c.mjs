#!/usr/bin/env node
/** P0-19 修稿探针：直落过程引导态 URL，勘切回分析 Tab 后的落态与按钮全集（复用尝试前置失败根因）。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');
const BASE = 'http://10.50.69.111:30892';
const OUT = {};
const dump = (n, d) => { fs.writeFileSync(path.join(__dirname, n), JSON.stringify(d, null, 2), 'utf8'); };

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click(); else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

  // 模拟 r1 现场：首发 029（当天已成功、未点查看结果）→ 切记录 → 切回分析 Tab
  await page.goto(BASE + '/service/chain-analysis?workspace=graph&tab=graph&industry=INB1701&eco_filter=orgs_and_actors&view=processing&demo_state=processing&task_id=SVC-20261015-029&analysis_fp=' + encodeURIComponent('svc|graph|INB1701'), { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2500);
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { await close.first().click().catch(() => {}); await page.waitForTimeout(300); }

  OUT.process_url = page.url();
  OUT.process_body_head = (((await page.locator('main').first().innerText().catch(() => '')) || '')).split('\n').filter(Boolean).slice(0, 22);
  OUT.process_buttons = await page.locator('main button').evaluateAll((els) => els.map((e) => (e.innerText || '').trim() || (e.getAttribute('aria-label') || ''))).catch(() => []);
  await page.screenshot({ path: path.join(__dirname, 'probe-p019c-processing.png') });

  // 切记录 Tab → 切回分析 Tab（r1 现场）
  const rec = page.locator('[role=tab][data-tab-key="records"]').or(page.getByRole('tab', { name: '分析记录', exact: true }));
  await rec.first().click({ timeout: 8000 });
  await page.waitForTimeout(1800);
  const main = page.locator('[role=tab][data-tab-key="graph"]').or(page.getByRole('tab', { name: '服务链图谱分析', exact: true }));
  await main.first().click({ timeout: 8000 });
  await page.waitForTimeout(2200);
  const close2 = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close2.count()) && (await close2.first().isVisible().catch(() => false))) { await close2.first().click().catch(() => {}); await page.waitForTimeout(300); }

  OUT.back_url = page.url();
  OUT.back_body_head = (((await page.locator('main').first().innerText().catch(() => '')) || '')).split('\n').filter(Boolean).slice(0, 22);
  OUT.back_buttons = await page.locator('main button').evaluateAll((els) => els.map((e) => (e.innerText || '').trim() || (e.getAttribute('aria-label') || ''))).catch(() => []);
  await page.screenshot({ path: path.join(__dirname, 'probe-p019c-back.png') });

  dump('_probe-p019c.json', OUT);
  await browser.close();
  console.log('DONE ->', path.join(__dirname, '_probe-p019c.json'));
})().catch((e) => { dump('_probe-p019c.json', { fatal: String(e) }); console.error(e); process.exit(1); });
