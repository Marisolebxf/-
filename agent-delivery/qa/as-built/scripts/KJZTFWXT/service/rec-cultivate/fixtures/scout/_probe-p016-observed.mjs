#!/usr/bin/env node
/** 短探（P0-16/01277 observed 采集）：runner 轮（20261015-50892-rec-cultivate-p0-16-r3 pass=5 项机检断言）任务 ID 未跨进程落盘；
 *  本探不新建任务，从分析记录页定位本条两次任务（T1=新一代信息技术、T2=新能源，以记录行上下文区分），采集 T2 结果态名单落局
 *  （双分支）+ 产业上下文回显 + 零残留三项核对 + 会话无关的记录双任务并存证据。
 *  产出 scout-p016-observed.json + p016-observed.png。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const out = { probed_at: new Date().toISOString(), entry: 'svc-rec-cultivate', purpose: 'P0-16 / FUNC-01277 observed (re-analysis on changed industry: new task, no-residue, dual-branch)' };

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

// 记录页（先主 Tab 再点记录 Tab，走脚本同路径；reload 兜底偶发「暂无分析记录」）
await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1800);
await page.locator('[role=tab][data-tab-key="records"]').first().click({ timeout: 8000 });
await page.waitForTimeout(2500);
let rows = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /已完成/ });
let n = await rows.count();
if (!n) { await page.reload({ waitUntil: 'domcontentloaded' }); await page.waitForTimeout(3000); n = await rows.count(); }
out.records_completed_rows = n;
const texts = [];
for (let i = 0; i < Math.min(n, 12); i++) texts.push((((await rows.nth(i).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim()));
out.records_head = texts.map((t) => t.slice(0, 120));

// 记录行不含产业上下文（类型=cultivate、状态、时间、操作），T1/T2 区分靠 runner 轮时序（尾号递增）；本探取最新 2 条 SVC-20261015 任务对照
const ids = [...new Set(texts.join('\n').match(/SVC-20261015-\d{1,4}/g) || [])];
out.today_task_ids_seen = ids.slice(0, 8);
const t2 = ids[0] || null; // 最新已完成（runner 轮 T2 为最后创建）
out.probe_task_id_t2 = t2;
const t1 = ids[1] || null;
out.probe_task_id_t1 = t1;

if (t2) {
  const rowT2 = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: t2 }).first();
  await rowT2.getByRole('button', { name: '查看结果', exact: true }).first().click({ timeout: 8000 });
  await page.waitForURL((u) => /[?&]view=result/.test(String(u)), { timeout: 10000 });
  await page.waitForTimeout(2500);
  out.t2_result_url = page.url();
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) await close.first().click().catch(() => {});
  const body = await main();
  out.t2_ctx_new_energy = /重点产业方向[\s\S]*?新能源/.test(body);
  out.t2_residue_t1_id = t1 ? body.includes(t1) : null;
  out.t2_residue_old_industry = /新一代信息技术/.test(body);
  out.t2_residue_process_traits = /生成中|可视化分析过程/.test(body);
  const ORG = /公司|大学|学院|学校|研究所|研究院|医院|中心/;
  const rowsLoc = page.locator('main .arco-table-tr, main [role=row], main tr').filter({ hasText: ORG });
  let cnt = 0;
  for (let i = 0; i < 10; i++) { cnt = await rowsLoc.count(); if (cnt) break; await page.waitForTimeout(1000); }
  out.t2_list_rows = cnt;
  if (cnt > 0) {
    out.t2_branch = 'non-empty';
    out.t2_first_rows = [];
    for (let i = 0; i < Math.min(cnt, 3); i++) out.t2_first_rows.push((((await rowsLoc.nth(i).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim()).slice(0, 200));
  } else {
    out.t2_branch = 'honest-empty';
    out.t2_empty_hit = body.includes('暂无候选') ? '暂无候选' : (body.includes('当前筛选范围内无本土机构') ? '当前筛选范围内无本土机构' : null);
  }
}

await page.screenshot({ path: path.join(__dirname, 'p016-observed.png') }).catch(() => {});
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p016-observed.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify({ t2: out.probe_task_id_t2, t1: out.probe_task_id_t1, branch: out.t2_branch || null, ctx: out.t2_ctx_new_energy, rows: out.t2_list_rows ?? null }, null, 0));
