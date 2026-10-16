#!/usr/bin/env node
/** P0-21 独立实勘：过程态「取消任务」→ 离开 processing + 配置保留 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const out = {
  surveyed_at: new Date().toISOString(),
  purpose: 'P0-21-cancel-task',
  CASE_ID: 'P0-21',
  FUNC_ID: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00925',
};

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
  await page.waitForTimeout(1500);

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

  await page.getByRole('tab', { name: /最近评估/ }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  const restore = page.getByRole('button', { name: '恢复结果' });
  out.restore_count = await restore.count();

  if (out.restore_count < 1) {
    out.error = '最近评估无「恢复结果」';
    out.ticket_hint = 'ENV-EVAL-TECH-RESULT-SHELL-001';
  } else {
    await restore.first().click({ timeout: 8000 });
    const t0 = Date.now();
    let ok = false;
    while (Date.now() - t0 < 60000) {
      const t = await page.locator('body').innerText().catch(() => '');
      if (/技术力评估结果/.test(t) && /\d+\s*分/.test(t)) {
        ok = true;
        break;
      }
      await page.waitForTimeout(1000);
    }
    out.after_restore = { ok, ms: Date.now() - t0, url: page.url() };
    if (!ok) {
      out.error = '恢复结果后无结果正文';
      out.ticket_hint = 'ENV-EVAL-TECH-RESULT-SHELL-001';
    } else {
      const prevTid = (page.url().match(/task_id=(EVAL-\d{8}-\d{3})/) || [])[1];
      out.prev_tid = prevTid;
      const reBtn = page.getByRole('button', { name: '重新分析' });
      out.reanalyze = {
        count: await reBtn.count(),
        visible: await reBtn.first().isVisible().catch(() => false),
        enabled: await reBtn.first().isEnabled().catch(() => false),
      };
      if (out.reanalyze.count < 1 || !out.reanalyze.visible || !out.reanalyze.enabled) {
        out.error = '结果态无可用「重新分析」';
        out.ticket_hint = 'ENV-EVAL-TECH-PRECHECK-001';
      } else {
        await reBtn.first().click({ timeout: 8000 });
        // 尽快等到过程态再点取消（完成迁移约 15~20s，需抢窗）
        let hitProc = false;
        const t1 = Date.now();
        while (Date.now() - t1 < 30000) {
          const u = page.url();
          const t = await page.locator('body').innerText().catch(() => '');
          if (/view=processing/.test(u) || /技术力评估生成中|可视化分析过程/.test(t)) {
            hitProc = true;
            break;
          }
          if (/预检未返回企业明细/.test(t)) {
            out.error = '重新分析后预检阻塞';
            out.ticket_hint = 'ENV-EVAL-TECH-PRECHECK-001';
            break;
          }
          await page.waitForTimeout(300);
        }
        out.processing = {
          hit: hitProc,
          ms: Date.now() - t1,
          url: page.url(),
        };
        if (hitProc) {
          const cancel = page.getByRole('button', { name: /取消任务/ });
          out.cancel_before = {
            count: await cancel.count(),
            visible: await cancel.first().isVisible().catch(() => false),
            enabled: await cancel.first().isEnabled().catch(() => false),
          };
          await page.screenshot({
            path: path.join(__dirname, 'probe-p021-processing.png'),
            fullPage: false,
          });
          out.screenshot_processing = 'probe-p021-processing.png';

          if (out.cancel_before.count < 1 || !out.cancel_before.visible) {
            out.error = '过程态无可见「取消任务」';
            const body = await page.locator('body').innerText().catch(() => '');
            out.body_slice = body.replace(/\s+/g, ' ').slice(0, 400);
          } else {
            await cancel.first().click({ timeout: 8000 });
            const samples = [];
            const t2 = Date.now();
            while (Date.now() - t2 < 20000) {
              const u = page.url();
              const t = await page.locator('body').innerText().catch(() => '');
              const sample = {
                ms: Date.now() - t2,
                url: u,
                view_processing: /view=processing/.test(u),
                view_result: /view=result/.test(u),
                body_proc: /技术力评估生成中|可视化分析过程/.test(t),
                cancel_btn: await page.getByRole('button', { name: /取消任务/ }).count(),
                start_btn: await page.getByRole('button', { name: '开始分析' }).count(),
                spin: await page.locator('[role=spinbutton]').count(),
                object_hint: /来自对比篮|评估对象|返回对比篮/.test(t),
                weight_hint: /权重合计|技术人才|一键平均分配/.test(t),
                slice: t.replace(/\s+/g, ' ').slice(0, 320),
              };
              samples.push(sample);
              if (!sample.view_processing && !sample.body_proc) break;
              await page.waitForTimeout(500);
            }
            out.after_cancel = samples;
            const last = samples[samples.length - 1] || null;
            out.after = last;
            await page.screenshot({
              path: path.join(__dirname, 'probe-p021-after-cancel.png'),
              fullPage: false,
            });
            out.screenshot_after = 'probe-p021-after-cancel.png';
            if (last) {
              out.verdict = {
                left_processing: !last.view_processing && !last.body_proc,
                config_retained: last.start_btn > 0 || last.spin > 0 || last.object_hint,
                object_or_weight: !!(last.object_hint || last.weight_hint || last.spin > 0),
              };
            }
          }
        } else if (!out.error) {
          out.error = '30s 未达过程态（可能瞬时完成或环境不可达）';
          out.ticket_hint = 'ENV-EVAL-TECH-PROCESS-WINDOW-001';
          out.final_url = page.url();
          const t = await page.locator('body').innerText().catch(() => '');
          out.body_slice = t.replace(/\s+/g, ' ').slice(0, 400);
        }
      }
    }
  }
} catch (e) {
  out.error = String(e && e.message ? e.message : e);
  out.stack = String(e && e.stack ? e.stack : '');
} finally {
  fs.writeFileSync(path.join(__dirname, 'probe-p021.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
}
