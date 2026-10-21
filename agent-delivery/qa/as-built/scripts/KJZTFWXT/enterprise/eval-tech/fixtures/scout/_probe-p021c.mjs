#!/usr/bin/env node
/** P0-21c：调权重强制新 fp → 开始分析 → 抢窗取消任务 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://10.50.69.111:30892/';
const out = { surveyed_at: new Date().toISOString(), purpose: 'P0-21c-force-new-fp', CASE_ID: 'P0-21' };

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

try {
  await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const loginBtn = page.getByRole('button', { name: /登录/ });
  if (await loginBtn.count()) await loginBtn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
  out.login = true;

  await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', {
    waitUntil: 'domcontentloaded',
  });
  await page.waitForTimeout(1000);
  const closeB = page.locator('button[aria-label="关闭对比篮"]');
  if (
    (await closeB.count()) &&
    (await closeB.first().isVisible().catch(() => false)) &&
    (await closeB.first().isEnabled().catch(() => false))
  ) {
    try {
      await closeB.first().click({ timeout: 1500 });
    } catch {}
  }

  // 若在结果态：先调整配置回配置态
  const adjust = page.getByRole('button', { name: '调整配置' });
  if (await adjust.first().isVisible().catch(() => false)) {
    await adjust.first().click({ timeout: 8000 });
    await page.waitForTimeout(1500);
    out.from_result_adjust = true;
  }

  // 无对象则选 2 家
  const open = page
    .getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象|返回对比篮/ })
    .first();
  if (await open.isVisible().catch(() => false)) {
    const body0 = await page.locator('body').innerText().catch(() => '');
    if (!/来自对比篮/.test(body0)) {
      await open.click({ timeout: 8000 });
      const sels = page.locator('[aria-label^="选择 "]');
      await sels.first().waitFor({ state: 'visible', timeout: 10000 });
      await sels.nth(0).click();
      await sels.nth(1).click();
      await page.getByRole('button', { name: '确定' }).first().click({ timeout: 8000 });
      await page.waitForTimeout(2500);
      out.selected = true;
    } else {
      out.already_filled = true;
    }
  }

  // 调第一个权重，强制新 analysis_fp（避开当天复用）
  const spins = page.locator('[role=spinbutton]');
  out.spin_count = await spins.count();
  if (out.spin_count < 1) throw new Error('无权重 spinbutton（未在配置态？）');
  const v0 = await spins.nth(0).inputValue().catch(() => '');
  out.weight_before = v0;
  await spins.nth(0).click({ timeout: 5000 });
  await spins.nth(0).fill('');
  // 改成与默认不同的合法值：21（默认首维常为 20）
  await spins.nth(0).fill('21');
  await spins.nth(0).press('Tab');
  await page.waitForTimeout(800);
  out.weight_after = await spins.nth(0).inputValue().catch(() => '');

  // 若权和校验失败，点一键均分再微调——尽量保持可开始
  const body1 = await page.locator('body').innerText().catch(() => '');
  out.sum_ok = /权重合计：100%|校验通过/.test(body1);
  if (!out.sum_ok) {
    const avg = page.getByRole('button', { name: /一键平均分配/ });
    if (await avg.count()) {
      await avg.first().click({ timeout: 5000 });
      await page.waitForTimeout(500);
      // 均分后再把第一维 +1，第二维 -1 保持 100
      const s = page.locator('[role=spinbutton]');
      await s.nth(0).fill('21');
      await s.nth(0).press('Tab');
      await page.waitForTimeout(200);
      const v1 = Number(await s.nth(1).inputValue());
      if (!Number.isNaN(v1) && v1 > 0) {
        await s.nth(1).fill(String(v1 - 1));
        await s.nth(1).press('Tab');
      }
      await page.waitForTimeout(500);
    }
    out.body_after_fix = (await page.locator('body').innerText())
      .replace(/\s+/g, ' ')
      .slice(0, 200);
    out.sum_ok2 = /权重合计：100%|校验通过/.test(out.body_after_fix || '');
  }

  const start = page.getByRole('button', { name: '开始分析' });
  out.start_disabled = await start.isDisabled().catch(() => true);
  out.precheck = /预检未返回企业明细/.test(await page.locator('body').innerText());
  if (out.start_disabled) {
    out.error = '开始分析 disabled';
    out.ticket_hint = out.precheck ? 'ENV-EVAL-TECH-PRECHECK-001' : 'ENV-EVAL-TECH-START-DISABLED';
  } else {
    // 点击后超高频轮询取消按钮
    await start.click();
    const samples = [];
    const t0 = Date.now();
    let clicked = false;
    while (Date.now() - t0 < 35000) {
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
        cancel_count: c,
        cancel_visible: c ? await cancel.first().isVisible().catch(() => false) : false,
        cancel_enabled: c ? await cancel.first().isEnabled().catch(() => false) : false,
        slice: t.replace(/\s+/g, ' ').slice(0, 180),
      };
      samples.push(sample);
      if (!clicked && sample.cancel_visible && sample.cancel_enabled) {
        await cancel.first().click({ timeout: 5000 });
        clicked = true;
        out.cancel_clicked_at_ms = sample.ms;
        await page.waitForTimeout(1500);
        break;
      }
      if (sample.view_result && /技术力评估结果/.test(t) && !sample.body_proc) {
        // 已直达结果，无取消窗
        break;
      }
      await page.waitForTimeout(120);
    }
    out.samples_before_cancel = samples;
    out.cancel_clicked = clicked;

    if (clicked) {
      const after = [];
      const t1 = Date.now();
      while (Date.now() - t1 < 15000) {
        const u = page.url();
        const t = await page.locator('body').innerText().catch(() => '');
        after.push({
          ms: Date.now() - t1,
          url: u,
          view_processing: /view=processing/.test(u),
          body_proc: /技术力评估生成中|可视化分析过程/.test(t),
          start_btn: await page.getByRole('button', { name: '开始分析' }).count(),
          spin: await page.locator('[role=spinbutton]').count(),
          object_hint: /来自对比篮|评估对象|返回对比篮/.test(t),
          weight_hint: /权重合计|技术人才|一键平均分配/.test(t),
          slice: t.replace(/\s+/g, ' ').slice(0, 240),
        });
        const last = after[after.length - 1];
        if (!last.view_processing && !last.body_proc) break;
        await page.waitForTimeout(400);
      }
      out.after = after;
      await page.screenshot({
        path: path.join(__dirname, 'probe-p021c-after-cancel.png'),
        fullPage: false,
      });
      out.screenshot = 'probe-p021c-after-cancel.png';
      const last = after[after.length - 1];
      out.verdict = {
        left_processing: last && !last.view_processing && !last.body_proc,
        config_retained: last && (last.start_btn > 0 || last.spin > 0 || last.object_hint),
      };
    } else {
      await page.screenshot({
        path: path.join(__dirname, 'probe-p021c-no-cancel.png'),
        fullPage: false,
      });
      out.screenshot = 'probe-p021c-no-cancel.png';
      out.error = '未抢到取消任务按钮（可能当天复用/瞬时完成）';
      out.ticket_hint = 'ENV-EVAL-TECH-PROCESS-WINDOW-001';
    }
  }
} catch (e) {
  out.error = String(e && e.message ? e.message : e);
  out.stack = String(e && e.stack ? e.stack : '');
} finally {
  fs.writeFileSync(path.join(__dirname, 'probe-p021c.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
}
