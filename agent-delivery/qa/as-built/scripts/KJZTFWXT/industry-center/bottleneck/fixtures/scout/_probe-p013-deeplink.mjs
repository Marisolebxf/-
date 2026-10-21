#!/usr/bin/env node
/** 一次性探针 · records 深链直达性 + 「已完成」文本可见性。产物落同目录；勿当 runner。 */
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
  const out = {
    url: page.url(),
    hasRecordsTabSelected: await page.getByRole('tab', { name: '诊断记录' }).getAttribute('aria-selected').catch(() => 'n/a'),
    hasDoneText: /已完成|成功/.test(text),
    hasFailText: /失败/.test(text),
    viewResultBtns: await page.getByRole('button', { name: '查看结果' }).count(),
    sample: text.slice(0, 600),
  };
  fs.writeFileSync(path.join(__dirname, 'probe-p013-deeplink.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
} finally {
  await browser.close();
}
