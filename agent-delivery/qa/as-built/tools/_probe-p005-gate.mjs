#!/usr/bin/env node
// 一次性无头探针：复核 P0-05 门控现场（回填 2 家后 开始分析 enabled? / 预检文案?）
// 用法（tools/ 下）：node _probe-p005-gate.mjs
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
const open = page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first();
out.open_btn_text = (await open.innerText().catch(() => null));
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
out.body_hit = (await page.locator('body').innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 600);
await page.screenshot({ path: path.join(outDir, 'probe-p005-gate.png'), fullPage: true });

fs.writeFileSync(path.join(outDir, 'probe-p005-gate.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 1));
await browser.close();
