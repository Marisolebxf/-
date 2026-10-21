#!/usr/bin/env node
/** 短探（P0-15/01274 修稿定向）：复刻 expect[4] 失败上下文——结果态「返回配置」第二轮（经记录行查看结果回结果态后再点返回配置）
 *  后页面实际走向。只复用既有已完成任务（不点开始分析、不新建任务），产出 scout-p015-back-config.json + png。
 *  失败现象：runner 20261015-50892-rec-cultivate-p0-15-r1 expect[4] 第二轮点返回配置后 8s 未见分析配置区/spinbutton。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const out = { probed_at: new Date().toISOString(), entry: 'svc-rec-cultivate', purpose: 'P0-15 expect[4] round-2 back-to-config behavior' };

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
const main = async () => (await page.locator('main').first().innerText().catch(() => '')) || '';

const goResultViaRecords = async () => {
  await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1800);
  const recTab = page.locator('[role=tab][data-tab-key="records"]').first();
  await recTab.click({ timeout: 8000 });
  await page.waitForURL(/tab=records/, { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(2500);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) await close.first().click().catch(() => {});
  const rows = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /已完成/ });
  let n = 0;
  for (let i = 0; i < 8; i++) { n = await rows.count(); const b = await main(); if (n > 0 || b.includes('SVC-')) break; await page.waitForTimeout(1000); }
  out.records_completed_rows = n;
  let clicked = false;
  for (let i = 0; i < Math.min(n, 6) && !clicked; i++) {
    const vr = rows.nth(i).getByRole('button', { name: '查看结果', exact: true }).first();
    if ((await vr.count()) && (await vr.isEnabled().catch(() => false))) { await vr.click({ timeout: 8000 }); clicked = true; }
  }
  if (!clicked) {
    out.debug_records_body = ((await main()).split('\n')).slice(0, 40);
    out.debug_url = page.url();
    await page.screenshot({ path: path.join(__dirname, 'p015-back-config-debug.png') }).catch(() => {});
    await browser.close();
    fs.writeFileSync(path.join(__dirname, 'scout-p015-back-config.json'), JSON.stringify(out, null, 2));
    console.error('records 无可点查看结果行；debug 已落盘');
    process.exit(1);
  }
  await page.waitForURL((u) => /[?&]view=result/.test(String(u)), { timeout: 10000 });
  await page.waitForTimeout(2000);
  return page.url();
};

const roundTrip = async (label) => {
  const r = { label };
  r.result_url_before_back = await goResultViaRecords();
  const back = page.getByRole('button', { name: '返回配置', exact: true });
  r.back_btn_count = await back.count();
  r.back_btn_visible = r.back_btn_count ? await back.first().isVisible().catch(() => false) : false;
  await back.first().click({ timeout: 8000 });
  // 轮询 8s：分析配置 + spinbutton（与脚本同判据）
  let ok = false;
  for (let i = 0; i < 8; i++) {
    const cfgVis = await page.getByText('分析配置').first().isVisible().catch(() => false);
    const spinVis = await page.locator('[aria-label="现有规模权重"] [role=spinbutton]').first().isVisible().catch(() => false);
    if (cfgVis && spinVis) { ok = true; break; }
    await page.waitForTimeout(1000);
  }
  r.cfg_and_spin_visible_8s = ok;
  r.url_after_back = page.url();
  const b = await main();
  r.body_head = b.split('\n').slice(0, 26);
  r.has_analysis_config_text = b.includes('分析配置');
  r.has_weight_label = b.includes('现有规模');
  r.has_result_title = b.includes('本土机构培育名单');
  r.has_processing_text = /生成中|分析结果已生成/.test(b);
  return r;
};

out.round1 = await roundTrip('first back-to-config (script round1 analog)');
out.round2 = await roundTrip('second back-to-config (script expect[4] context)');

await page.screenshot({ path: path.join(__dirname, 'p015-back-config.png'), fullPage: false }).catch(() => {});
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p015-back-config.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify({ round1: { ok: out.round1.cfg_and_spin_visible_8s, url: out.round1.url_after_back }, round2: { ok: out.round2.cfg_and_spin_visible_8s, url: out.round2.url_after_back, result_title: out.round2.has_result_title, processing: out.round2.has_processing_text } }, null, 2));
