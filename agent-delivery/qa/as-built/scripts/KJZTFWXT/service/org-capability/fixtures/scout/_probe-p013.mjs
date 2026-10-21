#!/usr/bin/env node
/**
 * 一次性无头探针（P0-13 写稿用）：FUNC-00683 无可用维度（仅剩1维 / 全部停用）。
 * 不点「开始评估」发起链（env-gate basket&lt;2）。产物落 scout-p013.json；勿当 runner。
 */
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const target = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;
const outDir = __dirname;

async function ensureLogin(page) {
  await page.waitForTimeout(600);
  if (!page.url().includes('/login')) return;
  const pw = page.locator('input[type=password]');
  await pw.first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
  if (!(await pw.count())) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await pw.first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function closeBasket(page) {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

async function gotoFresh(page) {
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(1500);
  await closeBasket(page);
}

async function panelSnapshot(page) {
  const panel = page.locator('.ent-section-panel', { hasText: '技术力评价模型' }).first();
  const text = ((await panel.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  const rows = page.locator('.svc-org-cap-dim');
  const n = await rows.count();
  const dims = [];
  for (let i = 0; i < n; i++) {
    const row = rows.nth(i);
    const cls = String((await row.getAttribute('class')) || '');
    const label = ((await row.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim().slice(0, 40);
    const cb = panel.locator('.arco-checkbox').nth(i);
    const cbCls = String((await cb.getAttribute('class').catch(() => '')) || '');
    const checked = /arco-checkbox-checked/.test(cbCls);
    dims.push({ i, label, cls, isDisabled: cls.includes('is-disabled'), checked, cbCls: cbCls.slice(0, 80) });
  }
  const spins = page.locator('[role=spinbutton]');
  const spinStates = [];
  for (let i = 0; i < (await spins.count()); i++) {
    spinStates.push({
      i,
      val: String(await spins.nth(i).inputValue().catch(() => '')),
      disabled: await spins.nth(i).isDisabled().catch(() => null),
    });
  }
  const startBtn = page.getByRole('button', { name: /开始评估/ }).first();
  const hint = page.locator('span', { hasText: /权重合计：/ }).first();
  const hintText = ((await hint.innerText().catch(() => '')) || '').replace(/\s+/g, ' ');
  const mainHit = ((await page.locator('main').innerText().catch(() => '')) || '')
    .replace(/\s+/g, ' ')
    .match(/(无可用|至少|启用维度|维度不足|须至少|权重合计：[^\n]{0,60})/g);
  return {
    panelTextSlice: text.slice(0, 500),
    dims,
    spinStates,
    hintText,
    start: {
      disabled: await startBtn.isDisabled().catch(() => null),
      enabled: await startBtn.isEnabled().catch(() => null),
    },
    mainHits: mainHit,
  };
}

async function uncheckN(page, count) {
  const panel = page.locator('.ent-section-panel', { hasText: '技术力评价模型' }).first();
  // uncheck from last to first so we leave earliest dims
  for (let i = 4; i >= 5 - count; i--) {
    const cb = panel.locator('.arco-checkbox').nth(i);
    const cbCls = String((await cb.getAttribute('class').catch(() => '')) || '');
    if (/arco-checkbox-checked/.test(cbCls)) {
      await cb.click({ timeout: 4000 });
      await page.waitForTimeout(500);
    }
  }
}

async function uncheckAll(page) {
  const panel = page.locator('.ent-section-panel', { hasText: '技术力评价模型' }).first();
  for (let i = 0; i < 5; i++) {
    const cb = panel.locator('.arco-checkbox').nth(i);
    const cbCls = String((await cb.getAttribute('class').catch(() => '')) || '');
    if (/arco-checkbox-checked/.test(cbCls)) {
      await cb.click({ timeout: 4000 });
      await page.waitForTimeout(450);
    }
  }
}

async function restoreDefaults(page) {
  // reload is cleanest
  await gotoFresh(page);
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), case: 'P0-13', func: '00683' };

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await gotoFresh(page);
  out.url = page.url();
  out.baseline = await panelSnapshot(page);
  await page.screenshot({ path: path.join(outDir, 'scout-p013-baseline.png'), fullPage: false });

  // disable 4 dims → leave 1 (专利数量)
  await uncheckN(page, 4);
  out.one_left = await panelSnapshot(page);
  await page.screenshot({ path: path.join(outDir, 'scout-p013-one-left.png'), fullPage: false });

  await gotoFresh(page);

  // disable all 5
  await uncheckAll(page);
  out.all_off = await panelSnapshot(page);
  await page.screenshot({ path: path.join(outDir, 'scout-p013-all-off.png'), fullPage: false });

  // try clicking any remaining checked? none
  // also look for toast / message / alert text in body
  out.all_off_body_snip = ((await page.locator('main').innerText().catch(() => '')) || '')
    .replace(/\s+/g, ' ')
    .slice(0, 800);

  // restore defaults via reload
  await restoreDefaults(page);
  out.restored = await panelSnapshot(page);
  await page.screenshot({ path: path.join(outDir, 'scout-p013-restored.png'), fullPage: false });

  // secondary: leave exactly 1 then check whether last checkbox can be unchecked
  await gotoFresh(page);
  await uncheckN(page, 4);
  const panel = page.locator('.ent-section-panel', { hasText: '技术力评价模型' }).first();
  const lastCb = panel.locator('.arco-checkbox').nth(0);
  const beforeLast = String((await lastCb.getAttribute('class').catch(() => '')) || '');
  await lastCb.click({ timeout: 4000 }).catch((e) => {
    out.last_uncheck_error = String(e).slice(0, 200);
  });
  await page.waitForTimeout(600);
  out.after_last_uncheck = await panelSnapshot(page);
  out.last_cb_before = beforeLast.slice(0, 80);

  fs.writeFileSync(path.join(outDir, 'scout-p013.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
} catch (e) {
  out.error = String(e).slice(0, 500);
  fs.writeFileSync(path.join(outDir, 'scout-p013.json'), JSON.stringify(out, null, 2));
  console.error(out.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
