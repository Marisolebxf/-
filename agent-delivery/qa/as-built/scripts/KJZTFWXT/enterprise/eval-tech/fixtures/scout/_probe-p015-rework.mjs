#!/usr/bin/env node
/** P0-15 REWORK 无头实勘：指纹直达空壳时序 + 深链是否需保留 analysis_fp */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://10.50.69.111:30892/';
const out = { surveyed_at: new Date().toISOString(), purpose: 'P0-15-REWORK-empty-shell-timing' };

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);

const closeB = page.locator('button[aria-label="关闭对比篮"]');
if (await closeB.count() && await closeB.first().isVisible().catch(() => false) && await closeB.first().isEnabled().catch(() => false)) {
  try { await closeB.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
}

const bodyRes = async () => {
  const t = await page.locator('body').innerText().catch(() => '');
  return {
    ok: /技术力评估结果/.test(t) && /\d+\s*分/.test(t),
    has_title: /技术力评估结果/.test(t),
    has_score: /\d+\s*分/.test(t),
    has_rank: /技术力加权排名/.test(t),
    has_back_cfg: /返回配置/.test(t),
    slice: t.replace(/\s+/g, ' ').slice(0, 220),
  };
};

try {
  await page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first().click({ timeout: 8000 });
  const sels = page.locator('[aria-label^="选择 "]');
  await sels.first().waitFor({ state: 'visible', timeout: 10000 });
  await page.waitForTimeout(800);
  const n = await sels.count();
  out.basket_count = n;
  if (n < 2) throw new Error('可选企业不足');
  await sels.nth(0).click();
  await sels.nth(1).click();
  await page.waitForTimeout(500);
  const okBtn = page.getByRole('button', { name: '确定' }).first();
  await okBtn.scrollIntoViewIfNeeded().catch(() => {});
  await okBtn.click({ timeout: 10000 });
  await page.waitForTimeout(2500);
  const start = page.getByRole('button', { name: '开始分析' });
  out.start_disabled = await start.isDisabled();
  if (out.start_disabled) {
    out.precheck = (await page.locator('body').innerText()).includes('预检未返回企业明细');
    throw new Error('开始分析禁用');
  }
  const tClick = Date.now();
  await start.click();
  out.click_at = new Date(tClick).toISOString();

  // 等 URL 出现 view=result（指纹快路径）或 body 已有结果
  let urlAt = null;
  let branch = null;
  const samples = [];
  while (Date.now() - tClick < 120000) {
    const url = page.url();
    const br = await bodyRes();
    const ms = Date.now() - tClick;
    if (samples.length < 40 && (samples.length === 0 || ms - (samples[samples.length - 1]?.ms || 0) >= 2000)) {
      samples.push({ ms, url_has_result: /view=result/.test(url), ...br, url_short: url.replace(base, '').slice(0, 160) });
    }
    if (!urlAt && /view=result/.test(url)) {
      urlAt = ms;
      branch = branch || 'result_url';
      out.url_hit_ms = ms;
      out.url_at_hit = url;
      out.body_at_url_hit = br;
    }
    if (br.ok) {
      out.body_ok_ms = ms;
      out.body_ok = br;
      branch = branch === 'result_url' ? 'url_then_body' : 'inplace';
      break;
    }
    await page.waitForTimeout(1000);
  }
  out.branch = branch;
  out.samples = samples;
  out.url_final = page.url();

  // 若已有结果，再测冷深链 vs 保留 fp 深链
  const m = /task_id=(EVAL-\d{8}-\d{3})/.exec(page.url());
  const fp = /analysis_fp=([a-f0-9]+)/.exec(page.url());
  out.tid = m ? m[1] : null;
  out.fp = fp ? fp[1] : null;
  if (out.tid) {
    // 冷深链（当前 P0-15 fallback）
    await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology&view=result&analysis_type=technology&task_id=' + out.tid, { waitUntil: 'domcontentloaded' });
    let coldOk = false;
    let coldMs = null;
    const coldT0 = Date.now();
    while (Date.now() - coldT0 < 25000) {
      const br = await bodyRes();
      if (br.ok) { coldOk = true; coldMs = Date.now() - coldT0; break; }
      await page.waitForTimeout(1000);
    }
    out.cold_deeplink = { ok: coldOk, ms: coldMs, body: await bodyRes(), url: page.url() };

    if (out.fp) {
      await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology&view=result&analysis_type=technology&task_id=' + out.tid + '&analysis_fp=' + out.fp, { waitUntil: 'domcontentloaded' });
      let fpOk = false;
      let fpMs = null;
      const fpT0 = Date.now();
      while (Date.now() - fpT0 < 25000) {
        const br = await bodyRes();
        if (br.ok) { fpOk = true; fpMs = Date.now() - fpT0; break; }
        await page.waitForTimeout(1000);
      }
      out.fp_deeplink = { ok: fpOk, ms: fpMs, body: await bodyRes(), url: page.url() };
    }
  }

  // 回到有内容页截排名
  if (out.body_ok_ms != null || out.fp_deeplink?.ok) {
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(__dirname, 'result-rank-rework.png'), fullPage: true });
  }
} catch (e) {
  out.error = String(e && e.message || e).slice(0, 240);
  out.url = page.url();
  out.body = await bodyRes();
}

fs.writeFileSync(path.join(__dirname, 'probe-p015-rework.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify({
  branch: out.branch,
  url_hit_ms: out.url_hit_ms,
  body_ok_ms: out.body_ok_ms,
  body_at_url_hit: out.body_at_url_hit,
  cold_deeplink: out.cold_deeplink && { ok: out.cold_deeplink.ok, ms: out.cold_deeplink.ms, has_back: out.cold_deeplink.body?.has_back_cfg },
  fp_deeplink: out.fp_deeplink && { ok: out.fp_deeplink.ok, ms: out.fp_deeplink.ms },
  error: out.error || null,
}, null, 2));
await browser.close();
