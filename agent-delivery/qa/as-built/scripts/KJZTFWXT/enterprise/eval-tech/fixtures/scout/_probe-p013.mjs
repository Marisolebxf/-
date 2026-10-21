#!/usr/bin/env node
/** P0-13 回炉一次性无头实勘（用后可删）：当天已成功任务指纹下，入口/回显形态探测 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://10.50.69.111:30892/';

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

const out = { surveyed_at: new Date().toISOString(), url_initial: page.url() };

// 阶段 0：裸态观察（同条件当天已成功时是否直接回显结果）
{
  const body = await page.locator('body').innerText();
  out.bare = {
    url: page.url(),
    has_result_view: /view=result/.test(page.url()),
    result_title: await page.getByText('技术力评估结果').first().isVisible().catch(() => false),
    score_hit: /\d+\s*分/.test(body),
    taskid_in_url: (/EVAL-\d{8}-\d{3}/.exec(page.url()) || [])[0] || null,
    has_recent: body.includes('最近评估'),
    body_head: body.slice(0, 300),
  };
  out.bare.screenshot = 'bare.png';
  await page.screenshot({ path: path.join(__dirname, 'bare.png'), fullPage: true });
}

// 阶段 1：走完整发起链（浮层回填 2 家 → 开始分析 → 5s 双分支窗口）
const closeB = page.locator('button[aria-label="关闭对比篮"]');
if (await closeB.count() && await closeB.first().isVisible().catch(() => false) && await closeB.first().isEnabled().catch(() => false)) {
  try { await closeB.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
}
await page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first().click({ timeout: 8000 });
await page.waitForTimeout(800);
const sels = page.locator('[aria-label^="选择 "]');
const n = await sels.count();
if (n < 2) throw new Error('可选企业不足: ' + n);
await sels.nth(0).click();
await sels.nth(1).click();
await page.getByRole('button', { name: '确定' }).click({ timeout: 8000 });
await page.waitForTimeout(2500);

const start = page.getByRole('button', { name: '开始分析' });
out.start_disabled = await start.isDisabled();
if (out.start_disabled) {
  out.abort = '开始分析 disabled（预检复发？）';
} else {
  await start.click();
  let branch = null;
  const t0 = Date.now();
  while (Date.now() - t0 < 5000) {
    const procEl = page.getByText(/技术力评估生成中|可视化分析过程/).first();
    if (await procEl.isVisible().catch(() => false)) { branch = 'processing'; break; }
    if (/view=result/.test(page.url())) { branch = 'result'; break; }
    await page.waitForTimeout(300);
  }
  out.branch5s = branch;
  out.url_5s = page.url();

  // 超 5s 继续观察 30s：URL 是否最终迁移（区分「窗口太短」与「页面不迁移」）
  const t1 = Date.now();
  while (Date.now() - t1 < 30000 && !/view=result/.test(page.url())) await page.waitForTimeout(500);
  out.migrated_within_35s = /view=result/.test(page.url());
  out.url_final = page.url();

  // 中段观察（分支未命中且未迁移时）：页面在做什么
  if (!out.migrated_within_35s) {
    const body = await page.locator('body').innerText();
    out.mid = {
      body_head: body.slice(0, 500),
      proc_visible: await page.getByText(/技术力评估生成中|可视化分析过程/).first().isVisible().catch(() => false),
      has_recent: body.includes('最近评估'),
      has_current: body.includes('当前分析'),
      recent_entries: (body.match(/EVAL-\d{8}-\d{3}/g) || []).slice(0, 5),
    };
  }

  // 阶段 2（乙分支扩展实勘）：若页面未迁移，走「最近评估」入口打开最近完成任务
  if (!out.migrated_within_35s) {
    // 先截当前形态
    await page.screenshot({ path: path.join(__dirname, 'stuck.png'), fullPage: true });
    // 找「最近评估」区里的最近条目/查看入口
    const recent = page.getByText('最近评估').first();
    out.recent_visible = await recent.isVisible().catch(() => false);
    const recentBtn = page.getByRole('button', { name: /查看|最近/ }).first();
    out.recent_btn_visible = await recentBtn.isVisible().catch(() => false);
    if (out.recent_btn_visible) {
      try { await recentBtn.click({ timeout: 3000 }); await page.waitForTimeout(1500); } catch (e) { out.recent_click_err = String(e).slice(0, 120); }
    }
    // 若仍未达 view=result，直接用已知 task_id 打开 view=result（指纹复用语义验证）
    if (!/view=result/.test(page.url())) {
      const tid = out.mid?.recent_entries?.[0];
      if (tid) {
        await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology&view=result&analysis_type=technology&task_id=' + tid, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(2000);
      }
    }
    const body2 = await page.locator('body').innerText();
    out.via_recent = {
      url: page.url(),
      url_has_view_result: /view=result/.test(page.url()),
      url_has_workspace: /workspace=technology/.test(page.url()),
      url_taskid: (/EVAL-\d{8}-\d{3}/.exec(page.url()) || [])[0] || null,
      title_hit: await page.getByText('技术力评估结果').first().isVisible().catch(() => false),
      score_hit: /\d+\s*分/.test(body2),
      body_head: body2.slice(0, 300),
    };
    await page.screenshot({ path: path.join(__dirname, 'via-recent.png'), fullPage: true });
  } else {
    const body2 = await page.locator('body').innerText();
    out.migrated = {
      title_hit: await page.getByText('技术力评估结果').first().isVisible().catch(() => false),
      score_hit: /\d+\s*分/.test(body2),
    };
  }
}

fs.writeFileSync(path.join(__dirname, 'probe-p013.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
