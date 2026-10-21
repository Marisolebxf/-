#!/usr/bin/env node
/** 微探针：服务环节多选 Select 的 popup 结构（01264 写稿用）+ 机构类型 checkbox 取消/重选。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const target = baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate';
const out = {};
const main = async (page) => (await page.locator('main').first().innerText().catch(() => '')) || '';

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

// 服务环节多选：定位含「上游·研发」回显的 select-view
try {
  const mult = page.locator('.arco-select-view-has-tag, .arco-select-view').filter({ hasText: '上游·研发' }).first();
  const cls = await mult.getAttribute('class');
  const tagTexts = await mult.locator('.arco-tag').allTextContents();
  await mult.click({ timeout: 5000 });
  await page.waitForTimeout(900);
  const popup = page.locator('.arco-trigger-popup:visible').first();
  const popupText = (await popup.innerText().catch(() => '')) || '';
  const opts = await popup.locator('.arco-select-option').allTextContents();
  const groups = await popup.locator('.arco-select-group-title, [class*=group]').allTextContents().catch(() => []);
  out.stage_select = { view_class: cls, visible_tags: tagTexts.map((t) => t.trim()), option_count: opts.length, options: opts.map((t) => t.trim()).slice(0, 20), group_nodes: groups.slice(0, 10), popup_head: popupText.split('\n').slice(0, 26) };
  // 取消一个选项（中游·中试）再断言
  const optMid = popup.locator('.arco-select-option').filter({ hasText: '中试' }).first();
  if (await optMid.count()) { await optMid.click({ timeout: 3000 }); await page.waitForTimeout(600); }
  const after1 = (await page.locator('.arco-select-view-has-tag, .arco-select-view').filter({ hasText: '上游·研发' }).first().innerText()).replace(/\s+/g, ' ');
  // 重新勾回
  const popup2 = page.locator('.arco-trigger-popup:visible').first();
  const optMid2 = popup2.locator('.arco-select-option').filter({ hasText: '中试' }).first();
  if (await optMid2.count()) { await optMid2.click({ timeout: 3000 }); await page.waitForTimeout(600); }
  const after2 = (await page.locator('.arco-select-view-has-tag, .arco-select-view').filter({ hasText: '上游·研发' }).first().innerText()).replace(/\s+/g, ' ');
  await page.keyboard.press('Escape');
  out.stage_toggle = { after_deselect: after1.slice(0, 160), after_reselect: after2.slice(0, 160) };
} catch (e) { out.stage_select = { err: String(e).slice(0, 200) }; }

// 机构类型 checkbox：取消高校 → 重选
try {
  const gx = page.locator('.arco-checkbox').filter({ hasText: '高校' }).first();
  const before = await gx.locator('input').isChecked();
  await gx.click({ timeout: 3000 });
  await page.waitForTimeout(500);
  const mid = await page.locator('.arco-checkbox').filter({ hasText: '高校' }).first().locator('input').isChecked();
  await page.locator('.arco-checkbox').filter({ hasText: '高校' }).first().click({ timeout: 3000 });
  await page.waitForTimeout(500);
  const after = await page.locator('.arco-checkbox').filter({ hasText: '高校' }).first().locator('input').isChecked();
  // 全取消（3 个都点掉）
  for (const name of ['高校', '科研院所', '企业']) {
    const c = page.locator('.arco-checkbox').filter({ hasText: name }).first();
    if (await c.locator('input').isChecked().catch(() => false)) { await c.click({ timeout: 3000 }); await page.waitForTimeout(300); }
  }
  const allOff = [];
  for (const name of ['高校', '科研院所', '企业']) allOff.push(await page.locator('.arco-checkbox').filter({ hasText: name }).first().locator('input').isChecked().catch(() => null));
  // 恢复全选
  for (const name of ['高校', '科研院所', '企业']) {
    const c = page.locator('.arco-checkbox').filter({ hasText: name }).first();
    if (!(await c.locator('input').isChecked().catch(() => true))) { await c.click({ timeout: 3000 }); await page.waitForTimeout(300); }
  }
  out.org_checkbox = { before, after_deselect: mid, after_reselect: after, all_unchecked: allOff };
} catch (e) { out.org_checkbox = { err: String(e).slice(0, 200) }; }

fs.writeFileSync(path.join(__dirname, 'scout-stage-popup.json'), JSON.stringify(out, null, 2));
await browser.close();
console.log('done');
