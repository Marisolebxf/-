#!/usr/bin/env node
/**
 * 一次性探针 · P0-13 补充：全新加载后确认开始分析 enabled→起任务→轮询成功结果。
 * 产物落同目录；勿当 runner。
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
const route = '/industry-center/diagnosis?workspace=bottleneck&tab=bottleneck';
const outDir = __dirname;

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
const out = { probed_at: new Date().toISOString() };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(3000);
  await closeBasket(page);
  if ((await page.getByRole('tab', { name: '产业瓶颈堵点识别' }).getAttribute('aria-selected')) !== 'true') {
    await page.getByRole('tab', { name: '产业瓶颈堵点识别' }).click();
    await page.waitForTimeout(1000);
  }
  const start = page.getByRole('button', { name: '开始分析' }).first();
  out.startEnabledFresh = await start.isEnabled().catch(() => false);
  out.mainText = (await page.locator('main').first().innerText()).slice(0, 1200);

  if (out.startEnabledFresh) {
    await start.click();
    await page.waitForTimeout(4000);
    // 轮询诊断记录找 enabled 查看结果，最长 150s
    const t0 = Date.now();
    let opened = false;
    while (Date.now() - t0 < 150000) {
      await page.getByRole('tab', { name: '诊断记录' }).click();
      await page.waitForTimeout(2000);
      const btns = page.getByRole('button', { name: '查看结果' });
      const n = await btns.count();
      let view = null;
      for (let i = 0; i < n; i++) if (!(await btns.nth(i).isDisabled())) { view = btns.nth(i); break; }
      const rows = (await page.locator('main').first().innerText()).match(/CHAIN-\d+-\d+\n\t\n[^\n\t]*\n\t\n[^\n\t]*/g) || [];
      out.lastRows = rows.slice(0, 3);
      if (view) {
        await view.click();
        await page.waitForTimeout(4000);
        opened = true;
        break;
      }
      await page.getByRole('tab', { name: '产业瓶颈堵点识别' }).click();
      await page.waitForTimeout(10000);
    }
    out.taskOpened = opened;
    if (opened) {
      const main = page.locator('main').first();
      const text = await main.innerText();
      out.result = {
        url: page.url(),
        hasResultTitle: /产业瓶颈堵点识别结果/.test(text),
        titleLine: (text.split('\n').find((l) => /识别结果/.test(l)) || '').trim(),
        kpiLines: text.split('\n').map((s) => s.trim()).filter((s) => /卡脖子|瓶颈环节|环节数/.test(s)).slice(0, 20),
        hasGraphWord: /图谱/.test(text),
        sample: text.slice(0, 3000),
      };
      await page.screenshot({ path: path.join(outDir, 'probe-p013-fresh-result.png'), fullPage: true });
    }
    await page.screenshot({ path: path.join(outDir, 'probe-p013-fresh-end.png'), fullPage: false });
  }
  fs.writeFileSync(path.join(outDir, 'probe-p013-fresh.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ startEnabledFresh: out.startEnabledFresh, taskOpened: out.taskOpened, hasResultTitle: out.result?.hasResultTitle, titleLine: out.result?.titleLine, kpiLines: out.result?.kpiLines }, null, 2));
} finally {
  await browser.close();
}
