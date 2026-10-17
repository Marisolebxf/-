#!/usr/bin/env node
/**
 * 一次性无头实勘 · P0-010 补充轮：同条件复用的两条路径（保留选区重按 vs 重建同条件重按）+ records 新任务即时入列。勿当 runner。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const route = '/service/institution-judgment?workspace=field&tab=coverage';
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

async function freshGoto(page) {
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

async function pickFirst(page) {
  const pick = page.getByRole('button', { name: '选择机构' }).first();
  await pick.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  const dialog = page.locator('.arco-modal:visible').filter({ hasText: '选择服务机构' }).first();
  await dialog.locator('.arco-checkbox:not(.arco-checkbox-disabled)').first().click({ timeout: 5000 });
  await page.waitForTimeout(300);
  await dialog.locator('.arco-modal-footer button:visible').filter({ hasText: /^确定$/ }).last().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const tags = page.locator('[data-testid="svc-org-analysis-context"] .arco-tag.svc-org-pick-tag');
  return (await tags.allTextContents()).map((s) => s.trim());
}

async function clickStartTrack(page, maxMs = 15000) {
  const before = (page.url().match(/task_id=(SVC-\d+-\d+)/) || [])[1] || null;
  await page.getByRole('button', { name: '开始分析' }).first().click({ timeout: 8000 });
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    await page.waitForTimeout(1000);
    const m = page.url().match(/task_id=(SVC-\d+-\d+)/);
    if (m && m[1] !== before) return { newTask: m[1], url: page.url() };
    if (/view=result/.test(page.url())) return { newTask: null, reused: true, url: page.url() };
  }
  return { newTask: null, url: page.url(), noTaskObserved: true };
}

async function waitDone(page, maxMs = 20000) {
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    const main = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    if (/查看结果|分析结果已生成/.test(main)) return true;
    await page.waitForTimeout(1000);
  }
  return false;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), stages: {} };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);

  // R1 保留选区路径：构造 → T_a → 完成 → 返回配置（保留 task/org 上下文）→ 再点开始
  await freshGoto(page);
  out.stages.r1 = {};
  out.stages.r1.picked = await pickFirst(page);
  const ta = await clickStartTrack(page);
  out.stages.r1.taskA = ta;
  out.stages.r1.doneA = await waitDone(page);
  // 回配置
  const backBtn = page.getByRole('button', { name: '返回配置' }).first();
  if (await backBtn.count()) { await backBtn.click({ timeout: 8000 }).catch(() => {}); } else {
    await page.getByRole('tab', { name: '服务机构产业领域分析', exact: true }).first().click({ timeout: 8000 });
  }
  await page.waitForTimeout(1500);
  const mainTxt = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  out.stages.r1.backState = {
    url: page.url(),
    selected: (mainTxt.match(/已选机构（\d+\s*家）/) || [])[0] || null,
    readyHint: /分析条件已就绪/.test(mainTxt),
    startVisible: await page.getByRole('button', { name: '开始分析' }).first().isVisible().catch(() => false),
  };
  const rb = await clickStartTrack(page, 12000);
  out.stages.r1.reclick = rb;
  await page.screenshot({ path: path.join(outDir, 'p010-3-reclick-kept.png') });

  // R2 records 即时入列核对
  await freshGoto(page);
  await page.getByRole('tab', { name: '分析记录', exact: true }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  const rec = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  out.stages.r2 = { todayTop: (rec.match(/SVC-\d+-\d+/g) || []).slice(0, 3), hasTaskA: !!(ta.newTask && rec.includes(ta.newTask)) };
  await page.screenshot({ path: path.join(outDir, 'p010-4-records-after.png') });

  out.overall = 'ok';
} catch (e) {
  out.overall = 'error';
  out.error = String(e).slice(0, 800);
  console.error(e);
} finally {
  fs.writeFileSync(path.join(outDir, 'scout-p010b.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ overall: out.overall }, null, 2));
  await browser.close();
}
