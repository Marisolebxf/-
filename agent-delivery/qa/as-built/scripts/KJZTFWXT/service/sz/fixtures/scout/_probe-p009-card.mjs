#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-sz P0-09 补充（R5）：点开框架卡指标行 ⓘ metric-spec-card，
 * 抓弹卡（MetricSpecCard）内容——找就绪度四行区块 / aligned / draft / 已登记 / 草稿 字样。
 * 产物落同目录 scout-p009-r5-speccard.json；勿当 runner。
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
    if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { await close.first().click().catch(() => {}); await page.waitForTimeout(300); } else break;
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
if (page.url().includes('/login')) { await ensureLogin(page); await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded' }); }
await page.waitForTimeout(2500);
await closeBasket(page);

await page.getByRole('tab', { name: '分析记录' }).first().click();
await page.waitForTimeout(2000);
const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /shenzhen/ }).filter({ hasText: /已完成/ }).first();
await row.getByRole('button', { name: /查看结果/ }).first().click({ timeout: 8000 });
await page.waitForTimeout(3500);
await closeBasket(page);

const r5 = { url: page.url(), rows: [] };
try {
  const rows = page.locator('[data-testid="svc-eco-sz-metric-list"] li .metric-spec-card');
  r5.card_n = await rows.count();
  for (let i = 0; i < (await rows.count()); i++) {
    const card = rows.nth(i);
    const entry = { i, aria: await card.getAttribute('aria-label').catch(() => null) };
    try {
      await card.click({ timeout: 4000 });
      await page.waitForTimeout(1600);
      // 抓所有可见弹层容器中真正有文本的
      const cands = page.locator('.arco-popover, .arco-tooltip, .arco-modal, .arco-drawer, [class*=metric-spec], [class*=spec-card], [class*=popover]');
      const n = await cands.count();
      entry.pop_cand_n = n;
      const texts = [];
      for (let j = 0; j < n; j++) {
        const el = cands.nth(j);
        const vis = await el.isVisible().catch(() => false);
        if (!vis) continue;
        const t = ((await el.innerText().catch(() => '')) || '').trim();
        if (t) texts.push(t.replace(/\s+/g, ' ').slice(0, 900));
      }
      entry.pop_texts = texts;
      // 整页找 def_status/aligned/draft 关键词（弹卡内容兜底）
      const bodyAll = ((await page.locator('body').innerText().catch(() => '')) || '');
      entry.body_has = {
        aligned: /aligned/i.test(bodyAll), draft_word: /draft/i.test(bodyAll),
        yidengji: /已登记/.test(bodyAll), caogao: /草稿/.test(bodyAll),
        jiuxu: /就绪/.test(bodyAll), def_status: /def_status/.test(bodyAll),
      };
      await page.keyboard.press('Escape').catch(() => {});
      await page.waitForTimeout(400);
      // 点 body 关弹层
      await page.locator('main').first().click({ position: { x: 5, y: 5 } }).catch(() => {});
      await page.waitForTimeout(400);
    } catch (e2) { entry.err = String(e2).slice(0, 200); }
    r5.rows.push(entry);
  }
  await page.screenshot({ path: path.join(outDir, 'scout-p009-r5.png'), fullPage: false }).catch(() => {});
} catch (e) { r5.error = String(e).slice(0, 300); }
dump('scout-p009-r5-speccard.json', r5);
await browser.close();
console.log('probe p009-r5 done', JSON.stringify(r5, null, 2).slice(0, 1500));
