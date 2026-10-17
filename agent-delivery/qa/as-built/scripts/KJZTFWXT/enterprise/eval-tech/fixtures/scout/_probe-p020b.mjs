#!/usr/bin/env node
/** P0-20 复探：恢复最新结果后点重新分析，拉长采样 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const out = { surveyed_at: new Date().toISOString(), purpose: 'P0-20-reanalyze-retry' };
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
    } catch {}
  }

  await page.getByRole('tab', { name: /最近评估/ }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  await page.getByRole('button', { name: '恢复结果' }).first().click({ timeout: 8000 });
  const t0 = Date.now();
  while (Date.now() - t0 < 90000) {
    const t = await page.locator('body').innerText().catch(() => '');
    if (/技术力评估结果/.test(t) && /\d+\s*分/.test(t)) break;
    await page.waitForTimeout(1000);
  }
  out.before_url = page.url();
  out.before_tid = (page.url().match(/task_id=(EVAL-\d{8}-\d{3})/) || [])[1];
  const reBtn = page.getByRole('button', { name: '重新分析' });
  out.re = {
    count: await reBtn.count(),
    visible: await reBtn.first().isVisible().catch(() => false),
    enabled: await reBtn.first().isEnabled().catch(() => false),
  };
  // dismiss dialogs if any
  await page.waitForTimeout(1000);
  await reBtn.first().click({ timeout: 8000 });
  const samples = [];
  const t1 = Date.now();
  while (Date.now() - t1 < 90000) {
    const u = page.url();
    const t = await page.locator('body').innerText().catch(() => '');
    samples.push({
      ms: Date.now() - t1,
      view_processing: /view=processing/.test(u),
      view_result: /view=result/.test(u),
      tid: (u.match(/task_id=(EVAL-\d{8}-\d{3})/) || [])[1] || null,
      body_proc: /技术力评估生成中|可视化分析过程/.test(t),
      dialog: /确定|确认重新/.test(t) && (await page.getByRole('dialog').count().catch(() => 0)),
    });
    const last = samples[samples.length - 1];
    if (last.view_processing || (last.tid && last.tid !== out.before_tid && last.body_proc)) break;
    await page.waitForTimeout(1000);
  }
  out.samples_head = samples.slice(0, 5);
  out.samples_tail = samples.slice(-3);
  out.sample_count = samples.length;
  out.after = samples[samples.length - 1];
} catch (e) {
  out.error = String(e && e.message ? e.message : e);
} finally {
  fs.writeFileSync(path.join(__dirname, 'probe-p020b.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
}
