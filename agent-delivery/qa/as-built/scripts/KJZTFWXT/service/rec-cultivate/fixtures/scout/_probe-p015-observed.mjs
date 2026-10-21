#!/usr/bin/env node
/** 短探（P0-15/01274 observed 采集）：runner 轮（20261015-50892-rec-cultivate-p0-15-r3 pass=5 项机检断言）任务 ID 未跨进程落盘；
 *  本探复用记录页最新已完成 cultivate 任务（不点开始分析、不新建），采集结果态名单落局（双分支）+ 诚实性声明 + 调权草稿持久性。
 *  产出 scout-p015-observed.json + p015-observed.png。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const out = { probed_at: new Date().toISOString(), entry: 'svc-rec-cultivate', purpose: 'P0-15 / FUNC-01274 observed (score-not-recomputed, dual-branch + weight-draft persistence)' };

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
const main = async () => (await page.locator('main').first().innerText().catch(() => '')) || '';

// 主 Tab → 分析记录（走脚本同路径），reload 兜底偶发「暂无分析记录」
await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1800);
await page.locator('[role=tab][data-tab-key="records"]').first().click({ timeout: 8000 });
await page.waitForTimeout(2500);
let rows = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /已完成/ });
let n = await rows.count();
if (!n) { await page.reload({ waitUntil: 'domcontentloaded' }); await page.waitForTimeout(3000); n = await rows.count(); }
out.records_completed_rows = n;
const firstRowText = n ? ((await rows.first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim() : '';
out.newest_completed_row = firstRowText.slice(0, 160);

// 最新已完成行「查看结果」→ 结果态实况
const m = firstRowText.match(/SVC-\d{8}-\d{1,4}/);
out.task_id = m ? m[0] : null;
await rows.first().getByRole('button', { name: '查看结果', exact: true }).first().click({ timeout: 8000 });
await page.waitForURL((u) => /[?&]view=result/.test(String(u)), { timeout: 10000 });
await page.waitForTimeout(2500);
out.result_url = page.url();
const close = page.locator('[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false))) await close.first().click().catch(() => {});
const body = await main();
out.honesty_note_seen = body.includes('当前为后端签发分，页面权重仅演示配置，未改名单分数');

const ORG = /公司|大学|学院|学校|研究所|研究院|医院|中心/;
const rowsLoc = page.locator('main .arco-table-tr, main [role=row], main tr').filter({ hasText: ORG });
let cnt = 0;
for (let i = 0; i < 10; i++) { cnt = await rowsLoc.count(); if (cnt) break; await page.waitForTimeout(1000); }
out.list_rows = cnt;
if (cnt > 0) {
  out.branch = 'non-empty';
  out.first_rows = [];
  for (let i = 0; i < Math.min(cnt, 3); i++) out.first_rows.push((((await rowsLoc.nth(i).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim()).slice(0, 200));
} else {
  out.branch = 'honest-empty';
  out.empty_hit = body.includes('暂无候选') ? '暂无候选' : (body.includes('当前筛选范围内无本土机构') ? '当前筛选范围内无本土机构' : null);
}

// 调权草稿持久性 observed：返回配置（含补点主 Tab）后读现有规模 spin 初值（runner 轮曾 fill 30 → 恢复默认 25 收尾）
await page.getByRole('button', { name: '返回配置', exact: true }).first().click({ timeout: 8000 });
let spinVis = false;
for (let i = 0; i < 8; i++) {
  spinVis = await page.locator('[aria-label="现有规模权重"] [role=spinbutton]').first().isVisible().catch(() => false);
  if (spinVis) break;
  if (i === 2) { const mt = page.locator('[role=tab][data-tab-key="cultivate"]').first(); if (await mt.count()) await mt.click({ timeout: 3000 }).catch(() => {}); }
  await page.waitForTimeout(1000);
}
if (spinVis) {
  const spin = page.locator('[aria-label="现有规模权重"] [role=spinbutton]').first();
  out.weight_scale_after_restore = String((await spin.inputValue().catch(() => '')) || (await spin.getAttribute('aria-valuenow').catch(() => '')) || '');
}

await page.screenshot({ path: path.join(__dirname, 'p015-observed.png') }).catch(() => {});
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p015-observed.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify({ task_id: out.task_id, branch: out.branch, list_rows: out.list_rows, empty_hit: out.empty_hit ?? null, honesty_note_seen: out.honesty_note_seen, weight_scale_after_restore: out.weight_scale_after_restore ?? null }, null, 2));
