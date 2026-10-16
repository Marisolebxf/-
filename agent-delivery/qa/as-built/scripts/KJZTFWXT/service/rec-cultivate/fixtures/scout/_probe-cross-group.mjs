#!/usr/bin/env node
/** 微探针：01265 跨组并存写稿用——确认「机构类型全取消」真实行为 + 链位多选能否全空（P0-09 fail 诊断）。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const target = baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate';
const out = {};

const orgState = async (page) => {
  const r = {};
  for (const n of ['高校', '科研院所', '企业']) {
    r[n] = await page.locator('main .arco-checkbox').filter({ hasText: n }).first().locator('input').isChecked().catch(() => null);
  }
  return r;
};

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
const close = page.locator('button[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false))) await close.first().click().catch(() => {});

// ---- 场景 A：复现 runner 序列——取消高校+企业（剩科研院所），再点科研院所 ----
try {
  out.scenario_A = { step0: await orgState(page) };
  for (const n of ['高校', '企业']) {
    const c = page.locator('main .arco-checkbox').filter({ hasText: n }).first();
    if (await c.locator('input').isChecked().catch(() => false)) { await c.click({ timeout: 5000 }); await page.waitForTimeout(500); }
  }
  out.scenario_A.step1_after_deselect_gx_qy = await orgState(page);
  const ky = page.locator('main .arco-checkbox').filter({ hasText: '科研院所' }).first();
  const kyClassBefore = await ky.getAttribute('class');
  await ky.click({ timeout: 5000 });
  await page.waitForTimeout(300);
  out.scenario_A.step2_right_after_ky_click = await orgState(page);
  await page.waitForTimeout(1200);
  out.scenario_A.step3_after_1200ms = await orgState(page);
  out.scenario_A.ky_class_before = kyClassBefore;
  out.scenario_A.ky_class_after = await ky.getAttribute('class');
  // 若被重置回全选，则再试一次点击科研院所（确认二次点击行为）
  const ky2 = page.locator('main .arco-checkbox').filter({ hasText: '科研院所' }).first();
  await ky2.click({ timeout: 5000 });
  await page.waitForTimeout(800);
  out.scenario_A.step4_second_ky_click = await orgState(page);
} catch (e) { out.scenario_A = { err: String(e).slice(0, 300) }; }

// ---- 场景 B：链位多选能否全空（重开页面，从默认全选 11 项逐项取消） ----
try {
  await page.goto(target, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  const close2 = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close2.count()) && (await close2.first().isVisible().catch(() => false))) await close2.first().click().catch(() => {});
  const selAny = page.locator('main .arco-select-view-multiple').first();
  const readSel = async () => ((await selAny.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  out.scenario_B = { step0: await readSel() };
  await selAny.click({ timeout: 8000 });
  await page.waitForTimeout(900);
  // 循环取消所有 selected 项，最多 3 轮（防重置回填需要多轮）
  for (let round = 0; round < 3; round++) {
    const allOpts = page.locator('.arco-trigger-popup:visible .arco-select-option');
    const n = await allOpts.count();
    let clicked = 0;
    for (let i = 0; i < n; i++) {
      const cls = await allOpts.nth(i).getAttribute('class');
      if ((cls || '').includes('selected')) { await allOpts.nth(i).click({ timeout: 3000 }); await page.waitForTimeout(250); clicked++; }
    }
    await page.waitForTimeout(600);
    const v = await readSel();
    out.scenario_B['round' + (round + 1)] = { clicked, view: v.slice(0, 120) };
    if (!/\+\d+|上游|中游|下游/.test(v)) break; // 已空
  }
  // popup 里剩余 selected 数
  const remainSel = await page.locator('.arco-trigger-popup:visible .arco-select-option.selected').count().catch(() => -1);
  out.scenario_B.remaining_selected_opts = remainSel;
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  out.scenario_B.final_view = (await readSel()).slice(0, 120);
  // 同时看目标组是否被影响
  out.scenario_B.org_after_stage_clear = await orgState(page);
} catch (e) { out.scenario_B = { err: String(e).slice(0, 300) }; }

fs.writeFileSync(path.join(__dirname, 'scout-cross-group.json'), JSON.stringify(out, null, 2));
await browser.close();
console.log('done');
