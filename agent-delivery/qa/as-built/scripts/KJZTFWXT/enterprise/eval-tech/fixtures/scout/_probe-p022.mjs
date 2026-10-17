#!/usr/bin/env node
/** P0-22 独立实勘：过程态「稍后查看」→ 离开 processing + 任务不被取消 + 我的任务入口计数 */
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
  purpose: 'P0-22-view-later',
  CASE_ID: 'P0-22',
  FUNC_ID: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00926',
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

function parseMyTasksCount(text) {
  const m = String(text || '').match(/打开我的任务[，,]\s*(\d+)\s*个进行中/);
  return m ? Number(m[1]) : null;
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
        let hitProc = false;
        const samples = [];
        const t1 = Date.now();
        while (Date.now() - t1 < 30000) {
          const u = page.url();
          const t = await page.locator('body').innerText().catch(() => '');
          const later = page.getByRole('button', { name: /稍后查看/ });
          const myTasks = page.getByRole('button', { name: /打开我的任务/ });
          const cancel = page.getByRole('button', { name: /取消任务/ });
          const sample = {
            ms: Date.now() - t1,
            url: u,
            tid: (u.match(/task_id=(EVAL-\d{8}-\d{3})/) || [])[1] || null,
            view_processing: /view=processing/.test(u),
            view_result: /view=result/.test(u),
            body_proc: /技术力评估生成中|可视化分析过程/.test(t),
            body_invalid: /当前评估任务不存在或已失效/.test(t),
            later_count: await later.count(),
            later_visible: (await later.count())
              ? await later.first().isVisible().catch(() => false)
              : false,
            later_enabled: (await later.count())
              ? await later.first().isEnabled().catch(() => false)
              : false,
            my_tasks_count: await myTasks.count(),
            my_tasks_text: (await myTasks.count())
              ? (await myTasks.first().innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 80)
              : null,
            my_tasks_n: parseMyTasksCount(t),
            cancel_count: await cancel.count(),
            slice: t.replace(/\s+/g, ' ').slice(0, 280),
          };
          samples.push(sample);
          if (sample.view_processing || sample.body_proc || sample.body_invalid) {
            hitProc = true;
            break;
          }
          if (/预检未返回企业明细/.test(t)) {
            out.error = '重新分析后预检阻塞';
            out.ticket_hint = 'ENV-EVAL-TECH-PRECHECK-001';
            break;
          }
          await page.waitForTimeout(120);
        }
        out.proc_samples_head = samples.slice(0, 8);
        out.processing = {
          hit: hitProc,
          ms: Date.now() - t1,
          url: page.url(),
          last: samples[samples.length - 1] || null,
        };
        if (hitProc) {
          const later = page.getByRole('button', { name: /稍后查看/ });
          const myTasks = page.getByRole('button', { name: /打开我的任务/ });
          const body = await page.locator('body').innerText().catch(() => '');
          out.later_before = {
            count: await later.count(),
            visible: (await later.count())
              ? await later.first().isVisible().catch(() => false)
              : false,
            enabled: (await later.count())
              ? await later.first().isEnabled().catch(() => false)
              : false,
          };
          out.my_tasks_before = {
            count: await myTasks.count(),
            text: (await myTasks.count())
              ? (await myTasks.first().innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 80)
              : null,
            n: parseMyTasksCount(body),
          };
          out.body_invalid = /当前评估任务不存在或已失效/.test(body);
          out.body_slice = body.replace(/\s+/g, ' ').slice(0, 400);
          await page.screenshot({
            path: path.join(__dirname, 'probe-p022-processing.png'),
            fullPage: false,
          });
          out.screenshot_processing = 'probe-p022-processing.png';

          if (out.later_before.count < 1 || !out.later_before.visible || !out.later_before.enabled) {
            out.error = '过程态无可见可点「稍后查看」';
            out.ticket_hint = 'ENV-EVAL-TECH-PROCESS-WINDOW-001';
          } else {
            const nBefore = out.my_tasks_before.n;
            await later.first().click({ timeout: 8000 });
            const after = [];
            const t2 = Date.now();
            while (Date.now() - t2 < 15000) {
              const u = page.url();
              const t = await page.locator('body').innerText().catch(() => '');
              const sample = {
                ms: Date.now() - t2,
                url: u,
                view_processing: /view=processing/.test(u),
                view_result: /view=result/.test(u),
                body_proc: /技术力评估生成中|可视化分析过程/.test(t),
                later_btn: await page.getByRole('button', { name: /稍后查看/ }).count(),
                cancel_btn: await page.getByRole('button', { name: /取消任务/ }).count(),
                my_tasks_n: parseMyTasksCount(t),
                start_btn: await page.getByRole('button', { name: '开始分析' }).count(),
                object_hint: /来自对比篮|评估对象|返回对比篮/.test(t),
                slice: t.replace(/\s+/g, ' ').slice(0, 280),
              };
              after.push(sample);
              if (!sample.view_processing && !sample.body_proc) break;
              await page.waitForTimeout(400);
            }
            out.after_later = after;
            const last = after[after.length - 1] || null;
            out.after = last;
            await page.screenshot({
              path: path.join(__dirname, 'probe-p022-after-later.png'),
              fullPage: false,
            });
            out.screenshot_after = 'probe-p022-after-later.png';
            if (last) {
              out.verdict = {
                left_processing: !last.view_processing && !last.body_proc,
                my_tasks_n_before: nBefore,
                my_tasks_n_after: last.my_tasks_n,
                count_not_decreased:
                  nBefore == null || last.my_tasks_n == null
                    ? null
                    : last.my_tasks_n >= nBefore,
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
  fs.writeFileSync(path.join(__dirname, 'probe-p022.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
}
