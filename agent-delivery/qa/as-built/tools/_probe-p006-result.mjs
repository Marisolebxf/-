#!/usr/bin/env node
// 一次性无头探针：P0-06 结果态可达性（回填 2 家核预检门控 + 最近评估「恢复结果」直达结果态）
// 用法（tools/ 下）：node _probe-p006-result.mjs
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(__dirname, '../scripts/KJZTFWXT/enterprise/eval-business/fixtures/scout');
fs.mkdirSync(outDir, { recursive: true });

const baseUrl = 'http://111.198.38.90:50892/';
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  const userBox = page.locator('input[placeholder*=用户名], input[type=text]').first();
  const passBox = page.locator('input[type=password]').first();
  await userBox.waitFor({ state: 'visible', timeout: 15000 });
  await passBox.waitFor({ state: 'visible', timeout: 15000 });
  await userBox.fill('admin');
  await passBox.fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(new URL('/enterprise/evaluation?workspace=business&mode=business', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(2500);

const out = { probed_at: new Date().toISOString(), url: page.url() };
const closeB = page.getByRole('button', { name: '关闭对比篮' });
if (await closeB.count()) await closeB.first().click().catch(() => {});
// —— 闸门 1：回填 2 家，看预检是否恢复 ——
const open = page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first();
out.open_btn_text = await open.innerText().catch(() => null);
await open.click({ timeout: 8000 });
await page.waitForTimeout(800);
const sels = page.locator('.arco-checkbox[aria-label^="选择 "]');
out.checkbox_count = await sels.count();
for (let i = 0; i < 2; i++) await sels.nth(i).click({ force: true });
await page.getByRole('button', { name: '确定' }).click({ timeout: 8000 });
await page.waitForTimeout(2500);
out.url_after = page.url();
const start = page.getByRole('button', { name: '开始分析' });
out.start_count = await start.count();
out.start_disabled = out.start_count ? await start.first().isDisabled() : null;
const cfgBody = (await page.locator('body').innerText().catch(() => ''));
out.precheck_seen = /预检未返回企业明细/.test(cfgBody);
out.gate_precheck_pass = out.start_count > 0 && out.start_disabled === false && !out.precheck_seen;
await page.screenshot({ path: path.join(outDir, 'probe-p006-gate.png'), fullPage: true });

// —— 闸门 2：最近评估 Tab 有无已完成任务可「恢复结果」——
out.hist_tab_found = false;
out.restore_count = 0;
out.hist_snippet = null;
const histTab = page.getByText('最近评估', { exact: true }).first();
if (await histTab.count()) {
  await histTab.click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  out.hist_tab_found = true;
  const restore = page.getByRole('button', { name: '恢复结果' });
  out.restore_count = await restore.count();
  out.hist_snippet = (await page.locator('body').innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 600);
}

// —— 点击首个「恢复结果」，等结果态 ——
out.restore_clicked = false;
out.url_final = null;
out.view_result_seen = false;
out.score_seen = false;
out.result_body = null;
if (out.restore_count > 0) {
  await page.getByRole('button', { name: '恢复结果' }).first().click({ timeout: 8000 });
  out.restore_clicked = true;
  const deadline = Date.now() + 30000;
  while (Date.now() < deadline) {
    await page.waitForTimeout(2000);
    const u = page.url();
    if (/view=result/.test(u)) break;
    const t = (await page.locator('body').innerText().catch(() => ''));
    if (/得分|评分/.test(t) && !/最近评估/.test(t.slice(0, 200))) break;
  }
  await page.waitForTimeout(1500);
  out.url_final = page.url();
  out.view_result_seen = /view=result/.test(out.url_final);
  const body = (await page.locator('body').innerText().catch(() => ''));
  out.score_seen = /得分|评分/.test(body);
  out.result_body = body.replace(/\s+/g, ' ').slice(0, 900);
}
await page.screenshot({ path: path.join(outDir, 'probe-p006-result.png'), fullPage: true });

fs.writeFileSync(path.join(outDir, 'probe-p006-result.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 1));
await browser.close();
