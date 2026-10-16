#!/usr/bin/env node
/** P0-16 补探：带 analysis_fp 深链 + 企业查询入篮 */
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

const url = base + 'enterprise/evaluation?workspace=technology&mode=technology&enterprise_codes[]=0a2b82208071ce5a0e3bd562b80e263b&enterprise_codes[]=12ceab1a61c7d1e1e5cb61b78dd8f3aa&source=compare-basket&task_id=EVAL-20261015-003&analysis_fp=ba101c92329c28be1311d7f8f2d78b60d4433305f39bbb81900c5f4779297fe7&view=result&analysis_type=technology';
await page.goto(url, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(4000);
let body = await page.locator('body').innerText();
out.deeplink = {
  url: page.url(),
  has_result: /技术力评估结果/.test(body),
  has_back: body.includes('返回配置'),
  has_report: body.includes('评估报告'),
  has_html: body.includes('查看 HTML 报告'),
  has_gap: body.includes('技术指标与差距诊断'),
  head: body.slice(0, 500).replace(/\s+/g, ' '),
};
await page.screenshot({ path: path.join(__dirname, 'p016b-deeplink.png'), fullPage: true });

if (out.deeplink.has_result) {
  // 直接勘报告入口
  const anyClick = page.locator('button, a, [role="button"]').filter({ hasText: /查看\s*HTML\s*报告|查看报告/ });
  out.entry_count = await anyClick.count();
  const popupPromise = page.waitForEvent('popup', { timeout: 10000 }).catch(() => null);
  if (out.entry_count) {
    await anyClick.first().scrollIntoViewIfNeeded().catch(() => {});
    await anyClick.first().click({ timeout: 5000 }).catch((e) => { out.click_err = String(e.message).slice(0, 120); });
    await page.waitForTimeout(2500);
    const popup = await popupPromise;
    out.popup = !!popup;
    if (popup) {
      await popup.waitForLoadState('domcontentloaded').catch(() => {});
      await popup.waitForTimeout(2000);
      const pt = await popup.locator('body').innerText().catch(() => '');
      out.popup_url = popup.url();
      out.popup_hits = { advantage: /优势|领先/.test(pt), gap: /差距|短板|不足/.test(pt), sample: pt.replace(/\s+/g, ' ').slice(0, 600) };
      await popup.screenshot({ path: path.join(__dirname, 'report-popup.png'), fullPage: true }).catch(() => {});
    }
  }
  out.result_block = {
    report: (() => { const i = body.indexOf('评估报告'); return i >= 0 ? body.slice(i, i + 300) : null; })(),
    gap: (() => { const i = body.indexOf('技术指标与差距诊断'); return i >= 0 ? body.slice(i, i + 400) : null; })(),
  };
} else {
  // 企业查询入篮
  await page.goto(base + 'enterprise/search', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  const closeB = page.locator('button[aria-label="关闭对比篮"]');
  if (await closeB.count() && await closeB.first().isVisible().catch(() => false)) {
    try { await closeB.first().click({ timeout: 1500 }); } catch {}
  }
  // 找搜索框
  const inputs = await page.evaluate(() => [...document.querySelectorAll('input')].slice(0, 12).map((i) => ({
    ph: i.placeholder, type: i.type, aria: i.getAttribute('aria-label'), visible: i.offsetParent !== null,
  })));
  out.search_inputs = inputs;
  const box = page.locator('input[placeholder*="企业"], input[placeholder*="搜索"], input[type=search]').first();
  if (await box.isVisible().catch(() => false)) {
    await box.fill('华为');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(3500);
  }
  const addBtns = page.locator('button').filter({ hasText: /加入对比|加入对比篮|添加对比/ });
  out.add_btns = await addBtns.count();
  out.search_body = (await page.locator('body').innerText()).slice(0, 500).replace(/\s+/g, ' ');
  // aria 加入对比篮
  const ariaAdd = page.locator('[aria-label*="对比"], button').filter({ hasText: /对比/ });
  out.aria_compare_count = await ariaAdd.count();
  for (let i = 0; i < Math.min(await addBtns.count(), 2); i++) {
    try { await addBtns.nth(i).click({ timeout: 2000 }); await page.waitForTimeout(600); } catch {}
  }
  // 若有 checkbox 勾选后加入
  const rowAdd = page.locator('[aria-label^="加入"], [aria-label*="对比篮"]');
  out.row_add = await rowAdd.count();
  for (let i = 0; i < Math.min(await rowAdd.count(), 2); i++) {
    try { await rowAdd.nth(i).click({ timeout: 2000 }); await page.waitForTimeout(400); } catch {}
  }
  await page.screenshot({ path: path.join(__dirname, 'p016b-search.png'), fullPage: true });

  // 回评估页看篮
  await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  const openBtn = page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first();
  if (await openBtn.isVisible().catch(() => false)) {
    await openBtn.click({ timeout: 8000 });
    await page.waitForTimeout(1500);
    const sels = page.locator('[aria-label^="选择 "]');
    out.basket_after_search = await sels.count();
    out.overlay_head = (await page.locator('body').innerText()).slice(0, 400).replace(/\s+/g, ' ');
  }
}

fs.writeFileSync(path.join(__dirname, 'probe-p016b.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
