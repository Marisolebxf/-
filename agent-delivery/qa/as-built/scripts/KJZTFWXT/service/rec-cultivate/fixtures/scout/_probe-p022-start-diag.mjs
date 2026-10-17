// P0-22 诊断：点「开始分析」后 POST / URL / toast / 按钮态
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const target = baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate';
const out = { probed_at: new Date().toISOString(), posts: [], toasts: [], steps: [] };

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('response', async (r) => {
  if (r.request().method() === 'POST' && /analysis\/tasks|rec-list|topicAsync/.test(r.url())) {
    let body = '';
    try { body = (await r.text()).slice(0, 300); } catch {}
    out.posts.push({ status: r.status(), url: r.url().slice(0, 160), body });
  }
});
try {
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

  // 恢复默认权重（对齐 P0-18 同条件口径）
  const restore = page.getByRole('button', { name: '恢复默认权重', exact: true });
  if (await restore.count()) { await restore.first().click().catch(() => {}); await page.waitForTimeout(500); out.steps.push('restore weights'); }

  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  out.echo = ((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim();

  const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
  out.start_enabled = await start.isEnabled();
  out.start_disabled_attr = await start.getAttribute('disabled');
  out.start_class = await start.getAttribute('class');
  const mainBefore = ((await page.locator('main').first().innerText().catch(() => '')) || '').slice(0, 400);
  out.main_before_has_soft = /请先确认分析条件/.test(mainBefore);
  out.weight_sum = ((await page.locator('main').first().innerText().catch(() => '')) || '').match(/权重合计[：:]\s*[^\n]+/)?.[0] || null;

  await start.click({ timeout: 8000 });
  out.steps.push('clicked start');
  for (let i = 0; i < 10; i++) {
    await page.waitForTimeout(1000);
    out.url_t = page.url();
    const toast = ((await page.locator('.arco-message, .arco-message-list, .arco-notification').allInnerTexts().catch(() => [])) || []).join('|');
    if (toast) out.toasts.push({ t: i, toast: toast.slice(0, 200) });
    if (/view=processing|view=result/.test(out.url_t)) break;
  }
  out.url_final = page.url();
  out.main_after_head = ((await page.locator('main').first().innerText().catch(() => '')) || '').split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 20);
  out.conclusion = /view=/.test(out.url_final) ? 'navigated' : 'stayed-config';
} catch (e) {
  out.error = String(e && e.stack || e);
} finally {
  await browser.close();
}
const outPath = path.join(__dirname, 'scout-p022-start-diag.json');
fs.writeFileSync(outPath, JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
