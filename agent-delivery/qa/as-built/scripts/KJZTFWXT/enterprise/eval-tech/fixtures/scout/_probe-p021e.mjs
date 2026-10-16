#!/usr/bin/env node
/** P0-21e：选 2 企→改权重→开始分析→抢窗取消（force 点确定） */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const out = { surveyed_at: new Date().toISOString(), purpose: 'P0-21e-select-weight-cancel', CASE_ID: 'P0-21' };

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

async function clickOk(page) {
  const okBtn = page.getByRole('button', { name: '确定' }).first();
  await okBtn.scrollIntoViewIfNeeded().catch(() => {});
  try {
    await okBtn.click({ timeout: 5000 });
  } catch {
    try {
      await okBtn.click({ force: true, timeout: 5000 });
    } catch {
      await okBtn.evaluate((el) => el.click());
    }
  }
}

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
  await page.waitForTimeout(1200);
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

  // 若已在结果态，先调整配置
  if (await page.getByRole('button', { name: '调整配置' }).first().isVisible().catch(() => false)) {
    await page.getByRole('button', { name: '调整配置' }).first().click({ timeout: 8000 });
    await page.waitForTimeout(1500);
  }

  await page.getByRole('tab', { name: /当前分析/ }).first().click({ timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(500);

  const open = page
    .getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象|返回对比篮/ })
    .first();
  await open.click({ timeout: 8000 });
  const sels = page.locator('[aria-label^="选择 "]');
  await sels.first().waitFor({ state: 'visible', timeout: 10000 });
  await page.waitForTimeout(600);
  out.sel_count = await sels.count();
  if (out.sel_count < 2) throw new Error('可选企业不足');
  // 换后两家，尽量避开与历史完全相同的对象组合
  const i0 = Math.min(2, out.sel_count - 2);
  await sels.nth(i0).click();
  await sels.nth(i0 + 1).click();
  await page.waitForTimeout(400);
  await clickOk(page);
  await page.waitForTimeout(2500);
  out.after_select = {
    url: page.url(),
    object: /来自对比篮/.test(await page.locator('body').innerText()),
    precheck: /预检未返回企业明细/.test(await page.locator('body').innerText()),
  };

  const spins = page.locator('[role=spinbutton]');
  out.spin_count = await spins.count();
  if (out.spin_count >= 2) {
    const a = Number(await spins.nth(0).inputValue());
    const b = Number(await spins.nth(1).inputValue());
    const a2 = a >= 25 ? a - 1 : a + 1;
    const b2 = a2 > a ? b - 1 : b + 1;
    await spins.nth(0).fill(String(a2));
    await spins.nth(0).press('Tab');
    await page.waitForTimeout(150);
    await spins.nth(1).fill(String(b2));
    await spins.nth(1).press('Tab');
    await page.waitForTimeout(500);
    out.weights = { before: [a, b], after: [a2, b2] };
  }

  const start = page.getByRole('button', { name: '开始分析' });
  out.start_disabled = await start.isDisabled().catch(() => true);
  out.body_cfg = (await page.locator('body').innerText()).replace(/\s+/g, ' ').slice(0, 280);
  if (out.start_disabled) {
    out.error = '开始分析 disabled';
    out.ticket_hint = out.after_select.precheck
      ? 'ENV-EVAL-TECH-PRECHECK-001'
      : 'ENV-EVAL-TECH-START-DISABLED';
  } else {
    await start.click();
    const samples = [];
    const t1 = Date.now();
    let clicked = false;
    while (Date.now() - t1 < 45000) {
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
      if (sample.view_result && /技术力评估结果/.test(t) && samples.length > 5) break;
      await page.waitForTimeout(80);
    }
    out.samples = samples;
    out.cancel_clicked = clicked;
    const shot = clicked ? 'probe-p021e-after-cancel.png' : 'probe-p021e-no-cancel.png';
    await page.screenshot({ path: path.join(__dirname, shot), fullPage: false });
    out.screenshot = shot;

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
      };
    } else {
      out.error = '未抢到取消任务';
      out.ticket_hint = 'ENV-EVAL-TECH-PROCESS-WINDOW-001';
      const procHits = samples.filter((s) => s.view_processing || s.body_proc || s.cancel_count > 0);
      out.proc_hit_count = procHits.length;
      out.proc_hits_head = procHits.slice(0, 5);
    }
  }
} catch (e) {
  out.error = String(e && e.message ? e.message : e);
  out.stack = String(e && e.stack ? e.stack : '');
} finally {
  fs.writeFileSync(path.join(__dirname, 'probe-p021e.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
}
