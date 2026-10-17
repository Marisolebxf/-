#!/usr/bin/env node
/** P0-21d：恢复结果→调整配置→改权重→开始分析→抢窗取消 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const out = { surveyed_at: new Date().toISOString(), purpose: 'P0-21d-restore-adjust-cancel', CASE_ID: 'P0-21' };

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

  await page.getByRole('tab', { name: /最近评估/ }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const restore = page.getByRole('button', { name: '恢复结果' });
  if ((await restore.count()) < 1) throw new Error('无恢复结果');
  await restore.first().click({ timeout: 8000 });
  const t0 = Date.now();
  while (Date.now() - t0 < 60000) {
    const t = await page.locator('body').innerText().catch(() => '');
    if (/技术力评估结果/.test(t) && /\d+\s*分/.test(t)) break;
    await page.waitForTimeout(800);
  }
  out.after_restore_url = page.url();

  await page.getByRole('button', { name: '调整配置' }).first().click({ timeout: 8000 });
  await page.waitForTimeout(2000);
  out.after_adjust = {
    url: page.url(),
    start: await page.getByRole('button', { name: '开始分析' }).count(),
    spin: await page.locator('[role=spinbutton]').count(),
    object: /来自对比篮|评估对象/.test(await page.locator('body').innerText()),
  };

  const spins = page.locator('[role=spinbutton]');
  if ((await spins.count()) < 2) throw new Error('配置态权重不足');
  // 互换微调：维0 +1，维1 -1，保持合计 100，且 fp 变化
  const a = Number(await spins.nth(0).inputValue());
  const b = Number(await spins.nth(1).inputValue());
  out.weights_before = [a, b];
  const a2 = a >= 25 ? a - 1 : a + 1;
  const b2 = a2 > a ? b - 1 : b + 1;
  await spins.nth(0).fill(String(a2));
  await spins.nth(0).press('Tab');
  await page.waitForTimeout(200);
  await spins.nth(1).fill(String(b2));
  await spins.nth(1).press('Tab');
  await page.waitForTimeout(600);
  out.weights_after = [
    Number(await spins.nth(0).inputValue()),
    Number(await spins.nth(1).inputValue()),
  ];
  const bodyCfg = await page.locator('body').innerText();
  out.sum_ok = /权重合计：100%|校验通过/.test(bodyCfg);
  out.precheck = /预检未返回企业明细/.test(bodyCfg);

  const start = page.getByRole('button', { name: '开始分析' });
  out.start_disabled = await start.isDisabled().catch(() => true);
  if (out.start_disabled) {
    out.error = '开始分析 disabled';
    out.ticket_hint = out.precheck ? 'ENV-EVAL-TECH-PRECHECK-001' : 'ENV-EVAL-TECH-START-DISABLED';
  } else {
    await start.click();
    const samples = [];
    const t1 = Date.now();
    let clicked = false;
    while (Date.now() - t1 < 40000) {
      const u = page.url();
      const t = await page.locator('body').innerText().catch(() => '');
      const cancel = page.getByRole('button', { name: /取消任务/ });
      const c = await cancel.count();
      const sample = {
        ms: Date.now() - t1,
        url: u,
        tid: (u.match(/task_id=(EVAL-\d{8}-\d{3})/) || [])[1] || null,
        view_processing: /view=processing/.test(u),
        view_result: /view=result/.test(u),
        body_proc: /技术力评估生成中|可视化分析过程/.test(t),
        cancel_count: c,
        cancel_visible: c ? await cancel.first().isVisible().catch(() => false) : false,
        cancel_enabled: c ? await cancel.first().isEnabled().catch(() => false) : false,
        slice: t.replace(/\s+/g, ' ').slice(0, 200),
      };
      samples.push(sample);
      if (!clicked && sample.cancel_visible && sample.cancel_enabled) {
        await cancel.first().click({ timeout: 5000 });
        clicked = true;
        out.cancel_at_ms = sample.ms;
        break;
      }
      if (sample.view_result && /技术力评估结果/.test(t) && samples.length > 3) break;
      await page.waitForTimeout(100);
    }
    out.samples = samples;
    out.cancel_clicked = clicked;
    await page.screenshot({
      path: path.join(__dirname, clicked ? 'probe-p021d-after-cancel.png' : 'probe-p021d-no-cancel.png'),
      fullPage: false,
    });
    out.screenshot = clicked ? 'probe-p021d-after-cancel.png' : 'probe-p021d-no-cancel.png';

    if (clicked) {
      const after = [];
      const t2 = Date.now();
      while (Date.now() - t2 < 15000) {
        const u = page.url();
        const t = await page.locator('body').innerText().catch(() => '');
        after.push({
          ms: Date.now() - t2,
          url: u,
          view_processing: /view=processing/.test(u),
          body_proc: /技术力评估生成中|可视化分析过程/.test(t),
          start_btn: await page.getByRole('button', { name: '开始分析' }).count(),
          spin: await page.locator('[role=spinbutton]').count(),
          object_hint: /来自对比篮|评估对象|返回对比篮/.test(t),
          weight_hint: /权重合计|技术人才|一键平均分配/.test(t),
          weight0: await page.locator('[role=spinbutton]').nth(0).inputValue().catch(() => null),
          slice: t.replace(/\s+/g, ' ').slice(0, 240),
        });
        const last = after[after.length - 1];
        if (!last.view_processing && !last.body_proc) break;
        await page.waitForTimeout(400);
      }
      out.after = after;
      const last = after[after.length - 1];
      out.verdict = {
        left_processing: last && !last.view_processing && !last.body_proc,
        config_retained: last && (last.start_btn > 0 || last.spin > 0 || last.object_hint),
        weight_kept:
          last &&
          last.weight0 != null &&
          String(last.weight0) === String(out.weights_after[0]),
      };
    } else {
      out.error = '未抢到取消任务';
      out.ticket_hint = 'ENV-EVAL-TECH-PROCESS-WINDOW-001';
    }
  }
} catch (e) {
  out.error = String(e && e.message ? e.message : e);
  out.stack = String(e && e.stack ? e.stack : '');
} finally {
  fs.writeFileSync(path.join(__dirname, 'probe-p021d.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
}
