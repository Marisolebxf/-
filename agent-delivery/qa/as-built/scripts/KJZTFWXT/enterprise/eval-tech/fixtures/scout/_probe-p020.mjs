#!/usr/bin/env node
/** P0-20 独立实勘：结果态「重新分析」→ 过程态 + 新 task_id */
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
  purpose: 'P0-20-reanalyze',
  CASE_ID: 'P0-20',
  FUNC_ID: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00924',
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
  out.path = 'restore';

  if (out.restore_count < 1) {
    out.error = '最近评估无「恢复结果」';
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
    } else {
      const body = await page.locator('body').innerText();
      const reBtn = page.getByRole('button', { name: '重新分析' });
      const tidMatch = page.url().match(/task_id=(EVAL-\d{8}-\d{3})/);
      const bodyTid = (body.match(/任务\s*ID[：:]\s*(EVAL-\d{8}-\d{3})/) || [])[1];
      out.before = {
        url: page.url(),
        task_id_url: tidMatch ? tidMatch[1] : null,
        task_id_body: bodyTid || null,
        reanalyze: {
          count: await reBtn.count(),
          visible: await reBtn.first().isVisible().catch(() => false),
          enabled: await reBtn.first().isEnabled().catch(() => false),
        },
        adjust_count: await page.getByRole('button', { name: '调整配置' }).count(),
        has_view_result: /view=result/.test(page.url()),
      };

      if (out.before.reanalyze.count < 1 || !out.before.reanalyze.visible) {
        out.error = '结果态无可见「重新分析」按钮';
      } else if (!out.before.reanalyze.enabled) {
        out.error = '「重新分析」disabled';
        out.ticket_hint = 'ENV-EVAL-TECH-PRECHECK-001';
      } else {
        await reBtn.first().click({ timeout: 8000 });
        const samples = [];
        const t1 = Date.now();
        while (Date.now() - t1 < 45000) {
          const u = page.url();
          const t = await page.locator('body').innerText().catch(() => '');
          const sample = {
            ms: Date.now() - t1,
            url: u,
            view_result: /view=result/.test(u),
            view_processing: /view=processing/.test(u),
            task_id: (u.match(/task_id=(EVAL-\d{8}-\d{3})/) || [])[1] || null,
            body_proc: /技术力评估生成中|可视化分析过程/.test(t),
            body_result: /技术力评估结果/.test(t) && /\d+\s*分/.test(t),
            body_precheck: /预检未返回企业明细/.test(t),
            start_btn: await page.getByRole('button', { name: '开始分析' }).count(),
            reanalyze_btn: await page.getByRole('button', { name: '重新分析' }).count(),
            slice: t.replace(/\s+/g, ' ').slice(0, 280),
          };
          samples.push(sample);
          if (
            sample.view_processing ||
            sample.body_proc ||
            (sample.task_id &&
              out.before.task_id_url &&
              sample.task_id !== out.before.task_id_url) ||
            sample.body_precheck ||
            sample.start_btn > 0
          ) {
            // keep sampling a bit more after first signal
            if (samples.length >= 3) break;
          }
          await page.waitForTimeout(1500);
        }
        out.samples = samples;
        out.after = samples[samples.length - 1] || null;
        await page.screenshot({
          path: path.join(__dirname, 'probe-p020-after-reanalyze.png'),
          fullPage: false,
        });
        out.screenshot = 'probe-p020-after-reanalyze.png';

        const last = out.after;
        if (last) {
          out.verdict = {
            left_result: !last.view_result,
            entered_processing: !!(last.view_processing || last.body_proc),
            new_task_id:
              !!(last.task_id && out.before.task_id_url && last.task_id !== out.before.task_id_url),
            hit_precheck: !!last.body_precheck,
            back_to_config: last.start_btn > 0 && !last.body_result,
          };
        }
      }
    }
  }
} catch (e) {
  out.error = String(e && e.message ? e.message : e);
  out.stack = String(e && e.stack ? e.stack : '');
} finally {
  fs.writeFileSync(path.join(__dirname, 'probe-p020.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
}
