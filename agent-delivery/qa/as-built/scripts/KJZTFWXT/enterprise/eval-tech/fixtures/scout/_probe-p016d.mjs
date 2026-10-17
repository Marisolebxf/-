#!/usr/bin/env node
/** P0-16 补探 d：直达已开报告页（或复用发起链）核优势/差距文案 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

const out = { surveyed_at: new Date().toISOString() };

// 复用 c：浮层回填 → 开始分析（指纹直达）→ 点报告
await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1000);
const closeB = page.locator('button[aria-label="关闭对比篮"]');
if (await closeB.count() && await closeB.first().isVisible().catch(() => false) && await closeB.first().isEnabled().catch(() => false)) {
  try { await closeB.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
}
await page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first().click({ timeout: 8000 });
const sels = page.locator('[aria-label^="选择 "]');
await sels.first().waitFor({ state: 'visible', timeout: 15000 });
await page.waitForTimeout(600);
await sels.nth(0).click();
await sels.nth(1).click();
const okBtn = page.getByRole('button', { name: '确定' }).first();
await okBtn.scrollIntoViewIfNeeded().catch(() => {});
try { await okBtn.click({ timeout: 4000 }); } catch { await okBtn.evaluate((el) => el.click()); }
await page.waitForTimeout(2500);
const start = page.getByRole('button', { name: '开始分析' });
if (await start.isDisabled()) throw new Error('start disabled');
await start.click();
const bodyRes = async () => {
  const t = await page.locator('body').innerText().catch(() => '');
  return /技术力评估结果/.test(t) && /\d+\s*分/.test(t);
};
const t0 = Date.now();
while (Date.now() - t0 < 60000 && !(await bodyRes())) await page.waitForTimeout(1000);
out.result_ready = await bodyRes();
out.result_url = page.url();

await page.getByRole('button', { name: /查看\s*HTML\s*报告/ }).first().click({ timeout: 8000 });
await page.waitForTimeout(2500);
out.report_url = page.url();
await page.waitForURL(/view=report/, { timeout: 10000 }).catch(() => {});
await page.waitForTimeout(1500);

const body = await page.locator('body').innerText();
out.report = {
  title_readonly: body.includes('只读报告'),
  title_tech: body.includes('技术力评估报告'),
  report_id: (/REPORT-[A-Z0-9]+/.exec(body) || [])[0] || null,
  has_toc: body.includes('报告目录'),
  has_summary: body.includes('执行摘要'),
  has_findings: body.includes('关键发现'),
  advantage: /技术优势|优势|领先/.test(body),
  gap: /技术差距|差距|短板/.test(body),
  adv_lines: (body.match(/[^\n]*(优势|领先)[^\n]*/g) || []).slice(0, 12),
  gap_lines: (body.match(/[^\n]*(差距|短板|不足)[^\n]*/g) || []).slice(0, 12),
  back_btn: await page.getByRole('button', { name: /返回评估结果/ }).count(),
  sample: body.replace(/\s+/g, ' ').slice(0, 1200),
};

// 点「关键发现」目录项看是否展开优势/差距
const findLink = page.getByText('关键发现', { exact: false }).first();
if (await findLink.isVisible().catch(() => false)) {
  try { await findLink.click({ timeout: 3000 }); await page.waitForTimeout(800); } catch {}
}
const body2 = await page.locator('body').innerText();
out.after_toc_click = {
  adv_lines: (body2.match(/[^\n]*(优势|领先)[^\n]*/g) || []).slice(0, 16),
  gap_lines: (body2.match(/[^\n]*(差距|短板)[^\n]*/g) || []).slice(0, 16),
  section_heads: (body2.match(/0\d\s+[^\n]+/g) || []).slice(0, 12),
};

await page.screenshot({ path: path.join(__dirname, 'report-page.png'), fullPage: true });
fs.writeFileSync(path.join(__dirname, 'probe-p016d.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
