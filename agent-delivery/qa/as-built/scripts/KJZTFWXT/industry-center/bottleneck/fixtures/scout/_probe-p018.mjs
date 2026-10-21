#!/usr/bin/env node
/** 一次性探针 · P0-18(FUNC-00621) 写稿前：records 是否已有「已完成」可恢复；顺带扫恢复入口文案。
 * 产物 probe-p018.json；勿当 runner。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const recordsUrl = '/industry-center/diagnosis?workspace=bottleneck&tab=records&view=records&demo_state=records';

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
try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(recordsUrl.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  const text = await page.locator('main').first().innerText();
  const btns = page.getByRole('button', { name: '查看结果' });
  let enabledViews = 0;
  const n = await btns.count();
  for (let i = 0; i < n; i++) { if (!(await btns.nth(i).isDisabled())) enabledViews++; }
  const statusFilter = page.getByRole('combobox').filter({ hasText: /全部状态|状态/ });
  const recoverHits = {
    viewResult: n,
    enabledViews,
    hasDoneText: /已完成|成功/.test(text),
    hasFailText: /失败/.test(text),
    hasRestoreWord: /恢复/.test(text),
    hasUnselected: /未选分析对象/.test(text),
    statusFilterVisible: (await statusFilter.count()) > 0,
  };
  const out = {
    probed_at: new Date().toISOString(),
    case_id: 'P0-18',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00621',
    url: page.url(),
    rows: (text.match(/CHAIN-\d+/g) || []).slice(0, 8),
    statuses: (text.match(/已完成|失败|进行中|排队中/g) || []).slice(0, 12),
    recoverHits,
    resultReachable: enabledViews > 0,
    sample: text.slice(0, 700),
    note: '写稿前复核：无已完成行 → 恢复复用不可达；目标态断言按 FUNC-00621 写入，allow_skip 归 ENV-CHAIN-BOTTLENECK-NO-DONE-TASK',
  };
  await page.screenshot({ path: path.join(__dirname, 'probe-p018-records.png'), fullPage: false });
  fs.writeFileSync(path.join(__dirname, 'probe-p018.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
} finally {
  await browser.close();
}
