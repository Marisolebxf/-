#!/usr/bin/env node
/** P0-09 一次性无头实勘（用后可删）：tech 壳开始分析→过程态/结果态形态探测 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';

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

// 打开浮层回填 2 家（同 P0-07 既有链路）
const close = page.locator('button[aria-label="关闭对比篮"]');
if (await close.count()) {
  try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(400); } catch {}
}
await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
await page.waitForTimeout(800);
const sels = page.locator('[aria-label^="选择 "]');
const n = await sels.count();
if (n < 2) throw new Error('对比篮不足 2 家: ' + n);
await sels.nth(0).click();
await sels.nth(1).click();
await page.getByRole('button', { name: '确定' }).click();
await page.waitForTimeout(2500);

const start = page.getByRole('button', { name: '开始分析' });
const out = { surveyed_at: new Date().toISOString(), url_before: page.url(), start_disabled: await start.isDisabled() };
if (out.start_disabled) {
  out.abort = '开始分析 disabled（预检复发？）';
} else {
  await start.click();
  // ≤5s 短窗捕过程态
  let branch = null;
  const t0 = Date.now();
  while (Date.now() - t0 < 5000) {
    const procEl = page.getByText(/技术力评估生成中|可视化分析过程/).first();
    if (await procEl.isVisible().catch(() => false)) { branch = 'processing'; break; }
    if (/view=result/.test(page.url())) { branch = 'result'; break; }
    await page.waitForTimeout(300);
  }
  out.branch = branch;
  if (branch === 'processing') {
    const body = await page.locator('body').innerText();
    out.proc = {
      title_hit: body.includes('技术力评估生成中'),
      visual_hit: body.includes('可视化分析过程'),
      cancel: await page.getByRole('button', { name: /取消任务/ }).first().isVisible().catch(() => false),
      later: await page.getByRole('button', { name: /稍后查看/ }).first().isVisible().catch(() => false),
      mytasks: await page.getByRole('button', { name: /打开我的任务/ }).first().isVisible().catch(() => false),
      url_has_view_processing: /view=processing/.test(page.url()),
      url_has_workspace: /workspace=technology/.test(page.url()),
      taskid_in_url: (/EVAL-\d{8}-\d{3}/.exec(page.url()) || [])[0] || null,
      taskid_in_body: (/EVAL-\d{8}-\d{3}/.exec(body) || [])[0] || null,
      fake_percent_suspect: /百分比|%\s*进度/.test(body) && /进度/.test(body),
      body_snippet: body.slice(0, 600),
    };
    // 超窗转 30s 轮询 view=result（记录迁移时间，仅 observed）
    const t1 = Date.now();
    while (Date.now() - t1 < 30000 && !/view=result/.test(page.url())) await page.waitForTimeout(500);
    out.result_url_hit = /view=result/.test(page.url());
    out.result_url = page.url();
    if (out.result_url_hit) {
      const body2 = await page.locator('body').innerText();
      out.result = {
        title_hit: /技术力/.test(body2) && /结果/.test(body2),
        score_hit: /\d+\s*分/.test(body2),
        body_head: body2.slice(0, 300),
      };
    }
  } else if (branch === 'result') {
    out.result_url = page.url();
    out.taskid_in_url = (/EVAL-\d{8}-\d{3}/.exec(page.url()) || [])[0] || null;
    const body = await page.locator('body').innerText();
    out.result = { title_hit: /技术力/.test(body) && /结果/.test(body), score_hit: /\d+\s*分/.test(body), body_head: body.slice(0, 300) };
  } else {
    out.abort = '双分支均未命中';
    out.url_after = page.url();
    const body = await page.locator('body').innerText();
    out.body_head = body.slice(0, 400);
  }
}

await page.screenshot({ path: path.join(__dirname, 'probe-p009.png'), fullPage: true });
fs.writeFileSync(path.join(__dirname, 'probe-p009.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
