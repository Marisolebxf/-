#!/usr/bin/env node
/** 短探（P0-14/01273 observed 采集）：复刻 P0-14 链路——发起 → 过程页引导 → 显式「查看结果」→ 结果态实况。
 *  runner 轮（20261015-50892-rec-cultivate-p0-14-r1）已 pass，但任务 ID 未跨进程落盘；本探同链路
 *  采集名单双分支落局（行数/行文本/空态文案/按钮），产出 scout-p014-result.json + p014-result.png。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const target = baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate';
const out = { probed_at: new Date().toISOString(), entry: 'svc-rec-cultivate', purpose: 'P0-14 / FUNC-01273 result-state observed (dual-branch)' };

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
await page.goto(target, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2200);
const close = page.locator('[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false))) await close.first().click().catch(() => {});

const main = async () => (await page.locator('main').first().innerText().catch(() => '')) || '';

// 选产业集群（P7 点可见容器）
const sel = page.locator('.industry-catalog-select').first();
await sel.click({ timeout: 8000 });
await page.waitForTimeout(800);
await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
await page.waitForTimeout(1200);
out.echo = ((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim();

// 点「开始分析」（exact 避开粘性提示）
const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
out.start_enabled = await start.isEnabled().catch(() => null);
await start.click({ timeout: 8000 });

// 轮询：processing（首发）或 result（当天复用直开，01279 口径）至 15s
let hit = null, directResult = false;
for (let i = 0; i < 15 && !hit; i++) {
  await page.waitForTimeout(1000);
  const u = page.url();
  const m = u.match(/[?&]task_id=(SVC-\d{8}-\d{1,4})/);
  if (/[?&]view=processing/.test(u) && m) hit = m[1];
  if (/[?&]view=result/.test(u) && m) { hit = m[1]; directResult = true; }
}
out.url_after_start = page.url();
out.task_id = hit;
out.direct_result = directResult;

if (hit && !directResult) {
  // 等过程页引导「分析结果已生成」至 15s
  for (let i = 0; i < 15; i++) {
    const b = await main();
    if (/分析结果已生成/.test(b)) break;
    await page.waitForTimeout(1000);
  }
  out.process_guide_seen = /分析结果已生成/.test(await main());
  const vr = page.getByRole('button', { name: '查看结果', exact: true }).first();
  out.view_result_btn_count = await page.getByRole('button', { name: '查看结果', exact: true }).count();
  await vr.click({ timeout: 8000 });
  await page.waitForURL((u) => /[?&]view=result/.test(String(u)), { timeout: 10000 }).catch(() => {});
}

await page.waitForTimeout(2500);
out.result_url = page.url();
out.result_body_head = ((await main()).split('\n').slice(0, 30));

// 名单双分支实况
const ORG = /公司|大学|学院|学校|研究所|研究院|医院|中心/;
const rowsLoc = page.locator('main .arco-table-tr, main [role=row], main tr').filter({ hasText: ORG });
const rows = await rowsLoc.count();
out.list_rows = rows;
if (rows > 0) {
  out.branch = 'non-empty';
  const texts = [];
  for (let i = 0; i < Math.min(rows, 5); i++) {
    const t = ((await rowsLoc.nth(i).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
    if (t) texts.push(t.slice(0, 260));
  }
  out.first_rows = texts;
} else {
  out.branch = 'honest-empty';
  out.empty_hit = (await main()).includes('暂无候选') ? '暂无候选' : ((await main()).includes('当前筛选范围内无本土机构') ? '当前筛选范围内无本土机构' : null);
}

// 结果态按钮
out.result_buttons = {};
for (const name of ['重新分析', '返回配置', '导出名单']) {
  out.result_buttons[name] = await page.getByRole('button', { name, exact: true }).count();
}

await page.screenshot({ path: path.join(__dirname, 'p014-result.png') }).catch(() => {});
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p014-result.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify({ task_id: out.task_id, direct_result: out.direct_result, branch: out.branch, list_rows: out.list_rows, empty_hit: out.empty_hit ?? null, result_buttons: out.result_buttons, result_url: out.result_url }, null, 2));
