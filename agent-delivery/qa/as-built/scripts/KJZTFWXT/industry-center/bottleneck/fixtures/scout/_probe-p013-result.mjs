#!/usr/bin/env node
/**
 * 一次性探针 · P0-13 结果态可达性（诊断记录恢复路径）。产物落同目录；勿当 runner。
 * 逻辑：登录 → 诊断记录找 enabled 查看结果；无则回配置合法组合点开始分析并短轮询；
 * 打开成功结果后抓顶栏 / KPI / 图谱文本样本供写断言校准。
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
const POLL_MS = 120000; // 起任务后最长轮询

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

async function gotoRecords(page) {
  await page.getByRole('tab', { name: '诊断记录' }).click();
  await page.waitForTimeout(1500);
}

// 返回第一条 enabled「查看结果」按钮；无则 null
async function findEnabledView(page) {
  const btns = page.getByRole('button', { name: '查看结果' });
  const n = await btns.count();
  for (let i = 0; i < n; i++) {
    if (!(await btns.nth(i).isDisabled())) return btns.nth(i);
  }
  return null;
}

async function openResult(page, view) {
  await view.click();
  await page.waitForTimeout(3500);
  const main = page.locator('main').first();
  const text = await main.innerText();
  await page.screenshot({ path: path.join(outDir, 'probe-p013-result.png'), fullPage: true });
  // KPI / 顶栏样本行
  const lines = text.split('\n').map((s) => s.trim()).filter(Boolean);
  const kpiLines = lines.filter((s) => /卡脖子|瓶颈环节|环节数|识别结果/.test(s)).slice(0, 20);
  return {
    url: page.url(),
    textSample: text.slice(0, 3000),
    kpiLines,
    hasResultTitle: /产业瓶颈堵点识别结果/.test(text),
    hasCardNeckWord: /卡脖子/.test(text),
    hasGraph: /健康图谱|图谱/.test(text),
  };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  const out = { probed_at: new Date().toISOString(), route, reachable: false, path: null };

  // 1) 诊断记录恢复路径
  await gotoRecords(page);
  await page.screenshot({ path: path.join(outDir, 'probe-p013-records.png'), fullPage: false });
  let view = await findEnabledView(page);
  const recordsText = await page.locator('main').first().innerText();
  out.recordsStatuses = (recordsText.match(/已完成|失败|进行中|排队中/g) || []).slice(0, 10);
  out.recordsSample = recordsText.slice(0, 800);
  if (view) {
    out.reachable = true;
    out.path = 'records-restore';
    out.result = await openResult(page, view);
  } else {
    // 2) 无已完成 → 回配置合法组合起任务，短轮询
    await page.getByRole('tab', { name: '产业瓶颈堵点识别' }).click();
    await page.waitForTimeout(1200);
    const start = page.getByRole('button', { name: '开始分析' }).first();
    if (await start.isEnabled().catch(() => false)) {
      await start.click();
      await page.waitForTimeout(3000);
      const t0 = Date.now();
      while (Date.now() - t0 < POLL_MS) {
        await gotoRecords(page);
        view = await findEnabledView(page);
        if (view) {
          out.reachable = true;
          out.path = 'fresh-start';
          out.result = await openResult(page, view);
          break;
        }
        await page.getByRole('tab', { name: '产业瓶颈堵点识别' }).click();
        await page.waitForTimeout(8000);
      }
      out.polledMs = Date.now() - t0;
    } else {
      out.startBlocked = true;
    }
  }

  fs.writeFileSync(path.join(outDir, 'probe-p013.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ reachable: out.reachable, path: out.path, hasResultTitle: out.result?.hasResultTitle, kpiLines: out.result?.kpiLines }, null, 2));
} finally {
  await browser.close();
}
