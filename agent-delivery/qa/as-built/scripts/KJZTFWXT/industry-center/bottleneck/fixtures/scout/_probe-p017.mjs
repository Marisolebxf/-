#!/usr/bin/env node
/** 一次性探针 · P0-17(FUNC-00616) 写稿前：records 是否已有成功结果；顺带扫图例/禁词相关文案。
 * 产物 probe-p017.json；勿当 runner。 */
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
  const legendHits = {
    healthBand: /健康分档/.test(text),
    judgeBadge: /判定角标/.test(text),
    duanlian: /断链/.test(text),
    weakBottleneckMerged: /薄弱\s*[\/／|]\s*瓶颈|薄弱\/瓶颈|薄弱瓶颈/.test(text),
    jianquan: /稳健/.test(text),
    guanzhu: /关注/.test(text),
    boruo: /薄弱/.test(text),
  };
  const out = {
    probed_at: new Date().toISOString(),
    case_id: 'P0-17',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00616',
    url: page.url(),
    rows: (text.match(/CHAIN-\d+/g) || []).slice(0, 8),
    statuses: (text.match(/已完成|失败|进行中|排队中/g) || []).slice(0, 10),
    hasDoneText: /已完成|成功/.test(text),
    viewResultBtns: n,
    enabledViews,
    resultReachable: enabledViews > 0,
    legendHitsOnRecords: legendHits,
    sample: text.slice(0, 600),
    note: '写稿前复核：无已完成行 → 结果态图例不可达；目标态断言按 FUNC-00616 写入，allow_skip 归 ENV-CHAIN-BOTTLENECK-NO-RESULT',
  };
  await page.screenshot({ path: path.join(__dirname, 'probe-p017-records.png'), fullPage: false });
  fs.writeFileSync(path.join(__dirname, 'probe-p017.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
} finally {
  await browser.close();
}
