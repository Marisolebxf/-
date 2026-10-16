#!/usr/bin/env node
/** 短探（P0-12/01271 写稿前闸门）：fresh 实测 cultivate「开始分析」POST /analysis/tasks 是否 200 恢复。
 *  旧票 D4-SVCCULT-TASK-CREATE-500 为上波前夜三次 500；今日姊妹入口已 200。本探只做一次发起，
 *  记录 POST 状态 / 过程态 URL / 完成态文案 / 记录行，产出 scout-p012-fresh.json。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const target = baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate';
const out = { probed_at: new Date().toISOString(), entry: 'svc-rec-cultivate', purpose: 'fresh POST gate for P0-12 / FUNC-01271' };

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

// 捕获任务创建 POST
const posts = [];
page.on('response', async (r) => {
  if (r.request().method() === 'POST' && r.url().includes('/api/topicAsync/topic/v1/analysis/tasks')) {
    posts.push({ status: r.status(), url: r.url() });
  }
});
page.on('response', async (r) => {
  if (r.request().method() === 'GET' && r.url().includes('/analysis/tasks') && r.url().includes('page')) {
    out.tasks_list_get = { status: r.status() };
  }
});

const main = async () => (await page.locator('main').first().innerText().catch(() => '')) || '';

// 选产业集群（P7 点可见容器）
const sel = page.locator('.industry-catalog-select').first();
await sel.click({ timeout: 8000 });
await page.waitForTimeout(800);
await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
await page.waitForTimeout(1200);
out.echo = ((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim();

// 记录行数（发起前）
await page.locator('[role=tab][data-tab-key="records"]').first().click({ timeout: 8000 });
await page.waitForTimeout(2000);
out.records_before = await page.locator('main tr, main [role="row"]').count();
out.records_body_before = ((await main()).match(/SVC-\d{8}-\d+/g) || []).slice(0, 8);
await page.locator('[role=tab][data-tab-key="cultivate"]').first().click({ timeout: 8000 });
await page.waitForTimeout(1200);
const close2 = page.locator('[aria-label="关闭对比篮"]');
if ((await close2.count()) && (await close2.first().isVisible().catch(() => false))) await close2.first().click().catch(() => {});

// 点「开始分析」（exact 避开粘性提示）
const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
out.start_enabled = await start.isEnabled().catch(() => null);
await start.click({ timeout: 8000 });

// 轮询过程态 URL 至 12s
let hit = null;
for (let i = 0; i < 12 && !hit; i++) {
  await page.waitForTimeout(1000);
  const m = page.url().match(/[?&]task_id=(SVC-\d{8}-\d{1,4})/);
  if (/[?&]view=processing/.test(page.url()) && m) hit = m[1];
}
out.url_after_start = page.url();
out.task_id = hit;
out.posts = posts;
out.body_after_start_head = ((await main()).split('\n').slice(0, 24));

// 若进过程态：等待完成/引导文案（至 15s）
if (hit) {
  let done = '';
  for (let i = 0; i < 15; i++) {
    const b = await main();
    if (/分析结果已生成|已完成|生成中/.test(b)) { done = b; if (!/生成中/.test(b) || /分析结果已生成/.test(b)) break; }
    await page.waitForTimeout(1000);
  }
  out.process_body_head = (done || (await main())).split('\n').slice(0, 30);
  // 分析记录新行
  await page.locator('[role=tab][data-tab-key="records"]').first().click({ timeout: 8000 });
  await page.waitForTimeout(2500);
  out.records_after = await page.locator('main tr, main [role="row"]').count();
  const body = await main();
  const esc = hit.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const rowRe = new RegExp(esc + '[\\s\\S]{0,200}?');
  const rowm = body.match(rowRe);
  out.new_task_row = rowm ? rowm[0].slice(0, 220) : null;
}

await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p012-fresh.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify({ posts: out.posts, task_id: out.task_id, url_after_start: out.url_after_start, echo: out.echo, records_before: out.records_before, records_after: out.records_after ?? null, new_task_row: out.new_task_row ?? null }, null, 2));
