#!/usr/bin/env node
/** P0-15 REWORK：强制新任务（微调权重破指纹）测 URL→body 时序 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://10.50.69.111:30892/';
const out = { surveyed_at: new Date().toISOString(), purpose: 'P0-15-REWORK-fresh-task-timing' };

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

const bodySnap = async () => {
  const t = await page.locator('body').innerText().catch(() => '');
  return {
    ok: /技术力评估结果/.test(t) && /\d+\s*分/.test(t),
    has_title: /技术力评估结果/.test(t),
    has_score: /\d+\s*分/.test(t),
    has_rank: /技术力加权排名/.test(t),
    has_proc: /技术力评估生成中|可视化分析过程/.test(t),
    has_back_cfg: /返回配置/.test(t),
    tid: (/EVAL-\d{8}-\d{3}/.exec(t) || [])[0] || null,
    slice: t.replace(/\s+/g, ' ').slice(0, 260),
  };
};

try {
  await page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first().click({ timeout: 8000 });
  const sels = page.locator('[aria-label^="选择 "]');
  await sels.first().waitFor({ state: 'visible', timeout: 10000 });
  await page.waitForTimeout(800);
  if ((await sels.count()) < 2) throw new Error('可选企业不足');
  // 换第 2/3 家，降低与历史指纹完全重合概率
  await sels.nth(1).click();
  await sels.nth(2).click().catch(async () => { await sels.nth(0).click(); });
  await page.waitForTimeout(500);
  const okBtn = page.getByRole('button', { name: '确定' }).first();
  await okBtn.scrollIntoViewIfNeeded().catch(() => {});
  await okBtn.click({ timeout: 10000 });
  await page.waitForTimeout(2500);

  // 微调权重破指纹（若有输入框）
  const weightInput = page.locator('.arco-input-number input, input[role="spinbutton"]').first();
  if (await weightInput.count()) {
    try {
      await weightInput.click({ timeout: 2000 });
      await weightInput.fill('21');
      await page.waitForTimeout(500);
      out.weight_tweaked = true;
    } catch {
      out.weight_tweaked = false;
    }
  }

  const start = page.getByRole('button', { name: '开始分析' });
  out.start_disabled = await start.isDisabled();
  if (out.start_disabled) throw new Error('开始分析禁用+预检');
  const tClick = Date.now();
  await start.click();
  out.click_at = new Date(tClick).toISOString();

  const timeline = [];
  let urlHitMs = null;
  let bodyOkMs = null;
  while (Date.now() - tClick < 180000) {
    const ms = Date.now() - tClick;
    const url = page.url();
    const br = await bodySnap();
    const row = {
      ms,
      view_result: /view=result/.test(url),
      task_id: (/task_id=(EVAL-\d{8}-\d{3})/.exec(url) || [])[1] || null,
      ...br,
    };
    if (timeline.length === 0 || ms - timeline[timeline.length - 1].ms >= 3000) timeline.push(row);
    if (urlHitMs == null && /view=result/.test(url)) {
      urlHitMs = ms;
      out.body_at_url_hit = br;
      out.url_at_hit = url;
    }
    if (bodyOkMs == null && br.ok) {
      bodyOkMs = ms;
      out.body_ok = br;
      break;
    }
    await page.waitForTimeout(1000);
  }
  out.url_hit_ms = urlHitMs;
  out.body_ok_ms = bodyOkMs;
  out.gap_url_to_body_ms = urlHitMs != null && bodyOkMs != null ? bodyOkMs - urlHitMs : null;
  out.timeline = timeline;
  out.url_final = page.url();

  // 若空壳：试 reload 当前完整 URL（含 fp）vs 冷深链
  if (bodyOkMs == null && /view=result/.test(page.url())) {
    const full = page.url();
    const tid = (/task_id=(EVAL-\d{8}-\d{3})/.exec(full) || [])[1];
    out.empty_shell_after_180s = true;
    await page.reload({ waitUntil: 'domcontentloaded' });
    let reloadOk = false;
    const r0 = Date.now();
    while (Date.now() - r0 < 60000) {
      const br = await bodySnap();
      if (br.ok) { reloadOk = true; out.reload_ok_ms = Date.now() - r0; break; }
      await page.waitForTimeout(1000);
    }
    out.reload_full_url = { ok: reloadOk, url: page.url(), body: await bodySnap() };
    if (!reloadOk && tid) {
      await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology&view=result&analysis_type=technology&task_id=' + tid, { waitUntil: 'domcontentloaded' });
      out.cold_after_empty = await bodySnap();
    }
  }
} catch (e) {
  out.error = String(e && e.message || e).slice(0, 240);
  out.url = page.url();
  out.body = await bodySnap();
}

fs.writeFileSync(path.join(__dirname, 'probe-p015-rework-fresh.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify({
  url_hit_ms: out.url_hit_ms,
  body_ok_ms: out.body_ok_ms,
  gap_url_to_body_ms: out.gap_url_to_body_ms,
  body_at_url_hit: out.body_at_url_hit && { ok: out.body_at_url_hit.ok, has_proc: out.body_at_url_hit.has_proc, has_back: out.body_at_url_hit.has_back_cfg, tid: out.body_at_url_hit.tid },
  empty_shell_after_180s: out.empty_shell_after_180s || false,
  reload_full_url: out.reload_full_url && { ok: out.reload_full_url.ok, ms: out.reload_ok_ms },
  error: out.error || null,
  tid_final: (/task_id=(EVAL-\d{8}-\d{3})/.exec(out.url_final || '') || [])[1] || null,
}, null, 2));
await browser.close();
