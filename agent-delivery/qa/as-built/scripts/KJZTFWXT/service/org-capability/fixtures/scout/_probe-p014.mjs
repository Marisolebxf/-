#!/usr/bin/env node
/**
 * 一次性无头探针（P0-14 写稿用）：评估失败局部错误与重试（FUNC-00684）。
 * 焦点：页面壳/模型区/开始评估门控 / 分析记录失败行 / 过程壳失败文案 / 重试入口。
 * 禁止点「开始评估」发起（env-gate fail）。产物落 scout-p014.json；勿当 runner。
 */
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const target = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;
const outDir = __dirname;

async function ensureLogin(page) {
  await page.waitForTimeout(600);
  if (!page.url().includes('/login')) return;
  const pw = page.locator('input[type=password]');
  await pw.first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
  if (!(await pw.count())) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await pw.first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function closeBasket(page) {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), case: 'P0-14', func: '00684' };

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(1500);
  await closeBasket(page);

  const board = page.locator('[data-testid="svc-org-capability-board"]');
  const panel = page.locator('.ent-section-panel', { hasText: '技术力评价模型' }).first();
  const start = page.getByRole('button', { name: /开始评估/ }).first();
  const spins = page.locator('[role=spinbutton]');
  const mainTab = page.getByRole('tab', { name: /服务机构技术力评估分析/ });
  const recTab = page.getByRole('tab', { name: '分析记录', exact: true });

  out.config = {
    board: await board.count(),
    model_panel: await panel.count(),
    start_visible: await start.isVisible().catch(() => false),
    start_disabled: await start.isDisabled().catch(() => null),
    spin_count: await spins.count(),
    spin_vals: [],
    main_tab: await mainTab.count(),
    records_tab: await recTab.count(),
    url: page.url(),
    title: await page.title(),
    blockers: ((await page.locator('.svc-org-cap-blockers').innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim(),
    compare_head: ((await page.locator('.svc-org-cap-compare__head').innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim(),
  };
  for (let i = 0; i < Math.min(5, out.config.spin_count); i++) {
    out.config.spin_vals.push(String(await spins.nth(i).inputValue().catch(() => '')));
  }

  // 分析记录：扫失败/重试词
  await recTab.first().click({ timeout: 8000 });
  await page.waitForTimeout(2000);
  const mainTxt = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  out.records = {
    url: page.url(),
    status_tokens: [...mainTxt.matchAll(/(已完成|失败|进行中|计算中|排队|取消|重试)/g)].map((m) => m[1]),
    fail_rows: (mainTxt.match(/失败/g) || []).length,
    retry_hits: (mainTxt.match(/重试/g) || []).length,
    view_process: await page.getByText('查看过程', { exact: true }).count(),
    view_result: await page.getByText('查看结果', { exact: true }).count(),
    snippet: mainTxt
      .split('\n')
      .map((s) => s.trim())
      .filter(Boolean)
      .slice(0, 40),
  };

  // 若有查看过程，打开看过程壳是否含失败/重试
  const vp = page.getByText('查看过程', { exact: true });
  if ((await vp.count()) > 0) {
    await vp.first().click({ timeout: 5000 });
    await page.waitForTimeout(2000);
    const shell = page.locator('[data-testid="svc-org-analysis-process"]');
    const shellTxt = ((await shell.innerText().catch(() => '')) || '');
    const alerts = page.locator('.arco-alert');
    const alertTexts = [];
    for (let i = 0; i < Math.min(5, await alerts.count()); i++) {
      alertTexts.push(((await alerts.nth(i).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim().slice(0, 120));
    }
    out.process_view = {
      url: page.url(),
      shell_visible: await shell.isVisible().catch(() => false),
      shell_head: shellTxt.replace(/\s+/g, ' ').trim().slice(0, 240),
      has_fail_word: /失败|异常|错误|Network Error/.test(shellTxt),
      has_retry_word: /重试/.test(shellTxt),
      alert_texts: alertTexts,
      retry_btn: await page.getByRole('button', { name: /重试/ }).count(),
      start_on_process: await page.getByRole('button', { name: /开始评估/ }).count(),
    };
  }

  // 回配置态确认壳仍在
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(1200);
  await closeBasket(page);
  out.shell_after_reload = {
    board: await page.locator('[data-testid="svc-org-capability-board"]').count(),
    model: await page.locator('.ent-section-panel', { hasText: '技术力评价模型' }).count(),
    start: await page.getByRole('button', { name: /开始评估/ }).count(),
    spins: await page.locator('[role=spinbutton]').count(),
  };

  out.gate = {
    overall: 'fail',
    ticket: 'ENV-SVCCAP-BASKET-ORG-LT2-001',
    note: '篮机构不足 → 无法合法开始评估 → 无法 route.abort 断链触发失败态；本探针只读壳/记录',
  };
  out.conclusion =
    '失败态构造需发起链（篮≥2）+ 断链/route.abort；当前 env-gate fail → 写稿走 skip+ticket 或只断言配置壳；历史记录未见独立失败行可只读失败 UI';
} catch (e) {
  out.error = String(e).slice(0, 500);
}

fs.writeFileSync(path.join(outDir, 'scout-p014.json'), JSON.stringify(out, null, 2));
console.log(
  JSON.stringify(
    {
      ok: !out.error,
      config: out.config,
      records: out.records && { ...out.records, snippet: out.records.snippet?.slice(0, 12) },
      process_view: out.process_view,
      shell_after_reload: out.shell_after_reload,
      error: out.error,
    },
    null,
    2,
  ),
);
await browser.close();
process.exit(out.error ? 1 : 0);
