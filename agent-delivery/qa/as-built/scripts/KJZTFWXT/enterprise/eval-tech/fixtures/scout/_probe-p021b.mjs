#!/usr/bin/env node
/** P0-21b：过程态抢窗轮询「取消任务」；失败则试开始分析链 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://10.50.69.111:30892/';
const out = {
  surveyed_at: new Date().toISOString(),
  purpose: 'P0-21b-cancel-poll',
  CASE_ID: 'P0-21',
};

async function login(page) {
  await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const loginBtn = page.getByRole('button', { name: /登录/ });
  if (await loginBtn.count()) await loginBtn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function closeBasket(page) {
  const closeB = page.locator('button[aria-label="关闭对比篮"]');
  if (
    (await closeB.count()) &&
    (await closeB.first().isVisible().catch(() => false)) &&
    (await closeB.first().isEnabled().catch(() => false))
  ) {
    try {
      await closeB.first().click({ timeout: 1500 });
      await page.waitForTimeout(300);
    } catch {}
  }
}

async function sampleCancel(page, ms) {
  const samples = [];
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    const u = page.url();
    const t = await page.locator('body').innerText().catch(() => '');
    const cancel = page.getByRole('button', { name: /取消任务/ });
    const c = await cancel.count();
    const sample = {
      ms: Date.now() - t0,
      url: u,
      tid: (u.match(/task_id=(EVAL-\d{8}-\d{3})/) || [])[1] || null,
      view_processing: /view=processing/.test(u),
      view_result: /view=result/.test(u),
      body_proc: /技术力评估生成中|可视化分析过程/.test(t),
      body_invalid: /当前评估任务不存在或已失效/.test(t),
      body_result: /技术力评估结果/.test(t) && /\d+\s*分/.test(t),
      cancel_count: c,
      cancel_visible: c ? await cancel.first().isVisible().catch(() => false) : false,
      cancel_enabled: c ? await cancel.first().isEnabled().catch(() => false) : false,
      start_btn: await page.getByRole('button', { name: '开始分析' }).count(),
      slice: t.replace(/\s+/g, ' ').slice(0, 220),
    };
    samples.push(sample);
    if (sample.cancel_visible && sample.cancel_enabled) break;
    if (sample.body_result && !sample.view_processing) break;
    await page.waitForTimeout(400);
  }
  return samples;
}

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

try {
  await login(page);
  out.login = true;
  await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', {
    waitUntil: 'domcontentloaded',
  });
  await page.waitForTimeout(1200);
  await closeBasket(page);

  // —— 路径 A：最近评估 → 恢复结果 → 重新分析 ——
  await page.getByRole('tab', { name: /最近评估/ }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const restore = page.getByRole('button', { name: '恢复结果' });
  out.path_a = { restore_count: await restore.count() };
  if (out.path_a.restore_count >= 1) {
    await restore.first().click({ timeout: 8000 });
    const t0 = Date.now();
    while (Date.now() - t0 < 45000) {
      const t = await page.locator('body').innerText().catch(() => '');
      if (/技术力评估结果/.test(t) && /\d+\s*分/.test(t)) break;
      await page.waitForTimeout(800);
    }
    const reBtn = page.getByRole('button', { name: '重新分析' });
    out.path_a.reanalyze_enabled = await reBtn.first().isEnabled().catch(() => false);
    if (out.path_a.reanalyze_enabled) {
      await reBtn.first().click({ timeout: 8000 });
      out.path_a.samples = await sampleCancel(page, 25000);
      const hit = out.path_a.samples.find((s) => s.cancel_visible && s.cancel_enabled);
      out.path_a.hit_cancel = !!hit;
      if (hit) {
        await page.getByRole('button', { name: /取消任务/ }).first().click({ timeout: 8000 });
        out.path_a.after = await sampleCancel(page, 12000);
        await page.screenshot({
          path: path.join(__dirname, 'probe-p021b-after-cancel.png'),
          fullPage: false,
        });
        out.path_a.screenshot = 'probe-p021b-after-cancel.png';
      } else {
        await page.screenshot({
          path: path.join(__dirname, 'probe-p021b-path-a.png'),
          fullPage: false,
        });
        out.path_a.screenshot = 'probe-p021b-path-a.png';
      }
    }
  }

  // —— 路径 B：当前分析 → 选企 → 开始分析（预检可能挡） ——
  await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', {
    waitUntil: 'domcontentloaded',
  });
  await page.waitForTimeout(1000);
  await closeBasket(page);
  await page.getByRole('tab', { name: /当前分析/ }).first().click({ timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(600);
  const open = page
    .getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象|返回对比篮/ })
    .first();
  out.path_b = { open_visible: await open.isVisible().catch(() => false) };
  if (out.path_b.open_visible) {
    await open.click({ timeout: 8000 });
    const sels = page.locator('[aria-label^="选择 "]');
    await sels.first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(600);
    out.path_b.sel_count = await sels.count();
    if (out.path_b.sel_count >= 2) {
      await sels.nth(0).click();
      await sels.nth(1).click();
      await page.waitForTimeout(400);
      const okBtn = page.getByRole('button', { name: '确定' }).first();
      try {
        await okBtn.click({ timeout: 5000 });
      } catch {
        await okBtn.click({ force: true, timeout: 5000 }).catch(() => {});
      }
      await page.waitForTimeout(2500);
      const start = page.getByRole('button', { name: '开始分析' });
      out.path_b.start_disabled = await start.isDisabled().catch(() => true);
      out.path_b.precheck = /预检未返回企业明细/.test(
        await page.locator('body').innerText().catch(() => ''),
      );
      if (!out.path_b.start_disabled) {
        await start.click();
        out.path_b.samples = await sampleCancel(page, 25000);
        out.path_b.hit_cancel = !!out.path_b.samples.find(
          (s) => s.cancel_visible && s.cancel_enabled,
        );
        if (out.path_b.hit_cancel) {
          await page.getByRole('button', { name: /取消任务/ }).first().click({ timeout: 8000 });
          out.path_b.after = await sampleCancel(page, 12000);
          await page.screenshot({
            path: path.join(__dirname, 'probe-p021b-path-b-after.png'),
            fullPage: false,
          });
          out.path_b.screenshot = 'probe-p021b-path-b-after.png';
        }
      }
    }
  }

  out.verdict = {
    path_a_cancel: !!out.path_a?.hit_cancel,
    path_b_cancel: !!out.path_b?.hit_cancel,
    path_b_blocked: !!(out.path_b?.start_disabled || out.path_b?.precheck),
  };
} catch (e) {
  out.error = String(e && e.message ? e.message : e);
  out.stack = String(e && e.stack ? e.stack : '');
} finally {
  fs.writeFileSync(path.join(__dirname, 'probe-p021b.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
}
