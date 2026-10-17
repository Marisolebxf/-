#!/usr/bin/env node
/** 一次性探针 · P0-14 写稿前快速复核：records 是否已出现成功结果（enabled 查看结果）。
 * 产物落同目录 probe-p014.json；勿当 runner。不起新任务（大概率同因，沿 P0-13 探针结论）。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
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
  const out = {
    probed_at: new Date().toISOString(),
    url: page.url(),
    rows: (text.match(/CHAIN-\d+/g) || []).slice(0, 8),
    statuses: (text.match(/已完成|失败|进行中|排队中/g) || []).slice(0, 10),
    hasDoneText: /已完成|成功/.test(text),
    viewResultBtns: n,
    enabledViews,
    resultReachable: enabledViews > 0,
    sample: text.slice(0, 600),
  };
  fs.writeFileSync(path.join(__dirname, 'probe-p014.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
} finally {
  await browser.close();
}
