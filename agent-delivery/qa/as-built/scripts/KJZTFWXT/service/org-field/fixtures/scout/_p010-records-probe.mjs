#!/usr/bin/env node
/**
 * 一次性无头实勘 · P0-010 分析记录与当天复用（records 列表形态 / 查看结果直达 / 同条件复用 / 变更机构显式重分析）。产物落同目录；勿当 runner。
 * 只读行为勘察：不判验收，observed 记录现场事实。禁 IDE 有头。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const route = '/service/institution-judgment?workspace=field&tab=coverage';
const outDir = __dirname;
const TODAY = '20261015';

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function freshGoto(page) {
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

async function pickOrgs(page, n) {
  // 弹窗勾前 n 个可用 checkbox → 确定 → 返回已选 tag 文本数组
  const pick = page.getByRole('button', { name: '选择机构' }).first();
  await pick.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  const dialog = page.locator('.arco-modal:visible').filter({ hasText: '选择服务机构' }).first();
  if (!(await dialog.count())) throw new Error('选择服务机构弹窗未打开');
  const boxes = dialog.locator('.arco-checkbox:not(.arco-checkbox-disabled)');
  for (let i = 0; i < n; i++) { await boxes.nth(i).click({ timeout: 5000 }); await page.waitForTimeout(250); }
  await dialog.locator('.arco-modal-footer button:visible').filter({ hasText: /^确定$/ }).last().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const tags = page.locator('[data-testid="svc-org-analysis-context"] .arco-tag.svc-org-pick-tag');
  return { count: await tags.count(), tags: (await tags.allTextContents()).map((s) => s.trim()) };
}

async function clickStartAndWaitTask(page, maxMs = 18000) {
  const t0 = Date.now();
  await page.getByRole('button', { name: '开始分析' }).first().click({ timeout: 8000 });
  while (Date.now() - t0 < maxMs) {
    await page.waitForTimeout(1200);
    const m = page.url().match(/task_id=(SVC-\d+-\d+)/);
    if (m) return m[1];
  }
  return null;
}

async function waitDone(page, maxMs = 20000) {
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    const main = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    if (/查看结果|分析结果已生成/.test(main)) return true;
    await page.waitForTimeout(1000);
  }
  return false;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), today: TODAY, stages: {} };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);

  // S1 records 列表形态
  await freshGoto(page);
  await page.getByRole('tab', { name: '分析记录', exact: true }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  const recMain = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  out.stages.recordsList = {
    viewBtnCount: await page.getByRole('button', { name: '查看结果' }).count(),
    taskIds: [...new Set(recMain.match(/SVC-\d+-\d+/g) || [])],
    todayIds: [...new Set(recMain.match(/SVC-20261015-\d+/g) || [])],
    textSample: recMain.replace(/专\n创新工作台[\s\S]*?维护管理\n/, '').slice(0, 1200),
  };
  await page.screenshot({ path: path.join(outDir, 'p010-0-records.png') });

  // S2 查看结果直达性
  const viewBtns = page.getByRole('button', { name: '查看结果' });
  if (await viewBtns.count()) {
    await viewBtns.first().click({ timeout: 8000 });
    await page.waitForTimeout(2500);
    const board = page.locator('.svc-org-coverage, [data-testid="svc-org-coverage-board"]').first();
    out.stages.viewDirect = {
      url: page.url(),
      taskId: (page.url().match(/task_id=(SVC-\d+-\d+)/) || [])[1] || null,
      boardVisible: (await board.count()) > 0 && (await board.isVisible().catch(() => false)),
    };
  } else out.stages.viewDirect = { skipped: '无查看结果按钮' };

  // S3 同条件复用：构造 1 家 → 开始分析 → T1 → 回配置再点一次（同条件）观察是否复用
  await freshGoto(page);
  const s3a = await pickOrgs(page, 1);
  const t1 = await clickStartAndWaitTask(page);
  const done1 = await waitDone(page);
  out.stages.sameCond = { picked: s3a, t1, done1 };
  await page.getByRole('button', { name: '返回配置' }).click({ timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(1500);
  const keptText = ((await page.locator('main').first().innerText().catch(() => '')) || '').match(/已选机构（\d+\s*家）/);
  out.stages.sameCond.backUrl = page.url();
  out.stages.sameCond.backSelected = keptText ? keptText[0] : null;
  if (/已选机构（1\s*家）/.test(keptText ? keptText[0] : '')) {
    const t1b = await clickStartAndWaitTask(page, 12000);
    out.stages.sameCond.retry = { mode: 'kept-selection', t1b, reused: t1b === null || t1b === t1, url: page.url() };
  } else {
    await freshGoto(page);
    await pickOrgs(page, 1);
    const t1b = await clickStartAndWaitTask(page, 12000);
    out.stages.sameCond.retry = { mode: 'reconstructed', t1b, reused: t1b === null || t1b === t1, url: page.url() };
  }
  await page.screenshot({ path: path.join(outDir, 'p010-1-samecond.png') });

  // S4 变更机构显式重分析：fresh → 1 家（记 URL 干净）→ 弹窗加勾第 2 家（URL 仍无任务）→ 开始分析 → T2≠T1
  await freshGoto(page);
  await pickOrgs(page, 1);
  out.stages.changedCond = { baseUrlClean: !/task_id=|view=/.test(page.url()) };
  await pickOrgs(page, 1); // 已选 1 家后再开弹窗勾第 1 个 = 新的（当前未勾）项？不可靠 → 改为勾第 2 个
  // 修正：重开弹窗后勾「第 2 个可用 checkbox」
  await page.getByRole('button', { name: '选择机构' }).first().click({ timeout: 8000 });
  await page.waitForTimeout(800);
  const dlg2 = page.locator('.arco-modal:visible').filter({ hasText: '选择服务机构' }).first();
  await dlg2.locator('.arco-checkbox:not(.arco-checkbox-disabled)').nth(1).click({ timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(300);
  await dlg2.locator('.arco-modal-footer button:visible').filter({ hasText: /^确定$/ }).last().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const tags2 = page.locator('[data-testid="svc-org-analysis-context"] .arco-tag.svc-org-pick-tag');
  out.stages.changedCond.afterChange = {
    selectedText: (((await page.locator('main').first().innerText().catch(() => '')) || '').match(/已选机构（\d+\s*家）/) || [])[0] || null,
    tagCount: await tags2.count(),
    urlStillClean: !/task_id=|view=/.test(page.url()),
    readyHint: /切换机构或 workspace 不会自动创建任务/.test(((await page.locator('main').first().innerText().catch(() => '')) || '')),
  };
  const t2 = await clickStartAndWaitTask(page);
  out.stages.changedCond.t2 = t2;
  out.stages.changedCond.t2DiffersFromT1 = !!(t2 && t1 && t2 !== t1);
  await page.screenshot({ path: path.join(outDir, 'p010-2-changed.png') });

  // S5 收尾：records 里当天记录
  await freshGoto(page);
  await page.getByRole('tab', { name: '分析记录', exact: true }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  const recMain2 = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  out.stages.recordsAfter = { todayIds: [...new Set(recMain2.match(/SVC-20261015-\d+/g) || [])], taskIds: [...new Set(recMain2.match(/SVC-\d+-\d+/g) || [])] };

  out.overall = 'ok';
} catch (e) {
  out.overall = 'error';
  out.error = String(e).slice(0, 800);
  console.error(e);
} finally {
  fs.writeFileSync(path.join(outDir, 'scout-p010.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ overall: out.overall, stages: Object.fromEntries(Object.entries(out.stages).map(([k, v]) => [k, Array.isArray(v) ? v.length : Object.keys(v)])) }, null, 2));
  await browser.close();
}
