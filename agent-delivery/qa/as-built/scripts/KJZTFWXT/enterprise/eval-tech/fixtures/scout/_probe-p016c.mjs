#!/usr/bin/env node
/** P0-16 补探 c：篮已有货 → 全链结果态 → 点击查看 HTML 报告 */
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
const bodyRes = async () => {
  const t = await page.locator('body').innerText().catch(() => '');
  return /技术力评估结果/.test(t) && /\d+\s*分/.test(t);
};

await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1200);
const closeB = page.locator('button[aria-label="关闭对比篮"]');
if (await closeB.count() && await closeB.first().isVisible().catch(() => false) && await closeB.first().isEnabled().catch(() => false)) {
  try { await closeB.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
}

await page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first().click({ timeout: 8000 });
const sels = page.locator('[aria-label^="选择 "]');
await sels.first().waitFor({ state: 'visible', timeout: 15000 }).catch(() => {});
await page.waitForTimeout(800);
out.basket_count = await sels.count();
if (out.basket_count < 2) {
  // 最近评估兜底
  const cancel = page.getByRole('button', { name: '取消' }).first();
  if (await cancel.isVisible().catch(() => false)) try { await cancel.click({ timeout: 2000 }); } catch {}
  await page.getByRole('tab', { name: /最近评估/ }).first().click({ timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(2000);
  out.recent = (await page.locator('body').innerText()).replace(/\s+/g, ' ').slice(0, 500);
  const restore = page.getByRole('button', { name: /恢复结果/ }).first();
  out.has_restore = await restore.isVisible().catch(() => false);
  if (out.has_restore) {
    await restore.click({ timeout: 8000 });
    await page.waitForTimeout(3000);
  }
} else {
  await sels.nth(0).click();
  await sels.nth(1).click();
  await page.waitForTimeout(400);
  const okBtn = page.getByRole('button', { name: '确定' }).first();
  await okBtn.scrollIntoViewIfNeeded().catch(() => {});
  try {
    await okBtn.click({ timeout: 5000 });
  } catch {
    await okBtn.click({ force: true, timeout: 5000 }).catch(async () => {
      await okBtn.evaluate((el) => el.click());
    });
  }
  await page.waitForTimeout(2500);
  const start = page.getByRole('button', { name: '开始分析' });
  out.start_disabled = await start.isDisabled();
  out.precheck = (await page.locator('body').innerText()).includes('预检未返回企业明细');
  if (out.start_disabled) {
    fs.writeFileSync(path.join(__dirname, 'probe-p016c.json'), JSON.stringify(out, null, 2), 'utf8');
    console.log(JSON.stringify({ blocked: 'precheck', ...out }, null, 2));
    await browser.close();
    process.exit(0);
  }
  await start.click();
  let branch = null;
  const t0 = Date.now();
  while (Date.now() - t0 < 5000) {
    if (await page.getByText(/技术力评估生成中|可视化分析过程/).first().isVisible().catch(() => false)) { branch = 'processing'; break; }
    if (/view=result/.test(page.url())) { branch = 'result'; break; }
    await page.waitForTimeout(300);
  }
  if (branch !== 'result') {
    const t1 = Date.now();
    while (Date.now() - t1 < 90000) {
      if (/view=result/.test(page.url())) { branch = 'result'; break; }
      if (await bodyRes()) { branch = 'inplace'; break; }
      await page.waitForTimeout(1000);
    }
  }
  const tw = Date.now();
  while (Date.now() - tw < 30000 && !(await bodyRes())) await page.waitForTimeout(1000);
  out.branch = branch;
}

out.url = page.url();
out.body_ready = await bodyRes();
await page.screenshot({ path: path.join(__dirname, 'result-before-report.png'), fullPage: true });

if (!(await bodyRes())) {
  // 再试最近评估
  await page.getByRole('tab', { name: /最近评估/ }).first().click({ timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(2000);
  out.recent2 = (await page.locator('body').innerText()).replace(/\s+/g, ' ').slice(0, 600);
  const restore = page.getByRole('button', { name: /恢复结果/ }).first();
  if (await restore.isVisible().catch(() => false)) {
    await restore.click({ timeout: 8000 });
    await page.waitForTimeout(4000);
    out.body_ready = await bodyRes();
    out.branch = 'restore';
  }
}

if (!(await bodyRes())) {
  fs.writeFileSync(path.join(__dirname, 'probe-p016c.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify({ blocked: true, ...out }, null, 2));
  await browser.close();
  process.exit(0);
}

const body = await page.locator('body').innerText();
out.hits = {
  report_section: body.includes('评估报告'),
  view_html: body.includes('查看 HTML 报告'),
  gap_diag: body.includes('技术指标与差距诊断'),
  adv_col: body.includes('领先差距与优势短板'),
  report_block: (() => { const i = body.indexOf('评估报告'); return i >= 0 ? body.slice(i, i + 280) : null; })(),
  gap_block: (() => { const i = body.indexOf('技术指标与差距诊断'); return i >= 0 ? body.slice(i, i + 450) : null; })(),
};

const anyClick = page.locator('button, a, [role="button"]').filter({ hasText: /查看\s*HTML\s*报告/ });
out.entry_count = await anyClick.count();
out.entry = [];
for (let i = 0; i < Math.min(out.entry_count, 4); i++) {
  const el = anyClick.nth(i);
  out.entry.push({
    text: (await el.innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 60),
    visible: await el.isVisible().catch(() => false),
    enabled: await el.isEnabled().catch(() => false),
    tag: await el.evaluate((e) => e.tagName).catch(() => '?'),
  });
}

const popupPromise = page.waitForEvent('popup', { timeout: 12000 }).catch(() => null);
const btn = page.getByRole('button', { name: /查看\s*HTML\s*报告/ }).first();
try {
  if (await btn.isVisible().catch(() => false)) {
    await btn.scrollIntoViewIfNeeded();
    await btn.click({ timeout: 8000 });
    out.click_via = 'role=button';
  } else if (out.entry_count) {
    await anyClick.first().scrollIntoViewIfNeeded();
    await anyClick.first().click({ timeout: 8000 });
    out.click_via = 'filter';
  }
} catch (e) {
  out.click_err = String(e.message).slice(0, 160);
}
await page.waitForTimeout(2500);
const popup = await popupPromise;
out.popup = !!popup;
if (popup) {
  await popup.waitForLoadState('domcontentloaded').catch(() => {});
  await popup.waitForTimeout(2500);
  const pt = await popup.locator('body').innerText().catch(() => '');
  out.popup_url = popup.url();
  out.popup_title = await popup.title().catch(() => '');
  out.popup_hits = {
    advantage: /优势|领先/.test(pt),
    gap: /差距|短板|不足/.test(pt),
    tech: /技术/.test(pt),
    readonly: /只读报告|报告身份|执行摘要/.test(pt),
    sample: pt.replace(/\s+/g, ' ').slice(0, 700),
  };
  await popup.screenshot({ path: path.join(__dirname, 'report-popup.png'), fullPage: true }).catch(() => {});
} else {
  // 同页导航？
  out.after_url = page.url();
  out.after_hits = {
    readonly: await page.getByText(/只读报告|报告身份|执行摘要/).count(),
    drawer: await page.locator('.arco-drawer:visible').count(),
    iframe: await page.locator('iframe').count(),
  };
  const ab = await page.locator('body').innerText();
  out.after_sample = ab.replace(/\s+/g, ' ').slice(0, 500);
}
await page.screenshot({ path: path.join(__dirname, 'result-after-report-click.png'), fullPage: true });

fs.writeFileSync(path.join(__dirname, 'probe-p016c.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
