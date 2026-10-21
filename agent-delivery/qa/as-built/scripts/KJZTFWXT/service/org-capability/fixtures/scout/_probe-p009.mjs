#!/usr/bin/env node
/**
 * 一次性无头探针（P0-09 写稿用）：异步任务与过程态（FUNC-00678）。
 * 焦点：开始评估门控 / 分析记录态 / 查看过程壳 / 计算中文案 / 重新分析形态。
 * 禁止点「开始评估」发起（env-gate fail）。产物落 scout-p009.json；勿当 runner。
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
const out = { surveyed_at: new Date().toISOString(), case: 'P0-09', func: '00678' };

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  await closeBasket(page);

  const start = page.getByRole('button', { name: '开始评估' }).first();
  const tags = page.locator('.svc-org-cap-compare__tags .arco-tag');
  const head = ((await page.locator('.svc-org-cap-compare__head').innerText().catch(() => '')) || '').replace(/\s+/g, ' ');
  const blockers = ((await page.locator('.svc-org-cap-blockers').innerText().catch(() => '')) || '').replace(/\s+/g, ' ');
  const footerNote = ((await page.locator('.svc-org-cap-footer').innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 300);
  out.config = {
    url: page.url(),
    start_visible: await start.isVisible().catch(() => false),
    start_disabled: await start.isDisabled().catch(() => null),
    start_testid: await page.locator('[data-testid="svc-org-cap-start"]').count(),
    tag_count: await tags.count(),
    head,
    blockers: blockers.slice(0, 200),
    footer_note: footerNote,
    single_flight_hint: /同用户同条件只允许一条在跑/.test(footerNote),
    rerun_btn: await page.locator('[data-testid="svc-org-cap-rerun"]').count(),
    percent_fake: /%/.test(await page.locator('main').innerText().catch(() => '')) && /进度|完成度/.test(await page.locator('main').innerText().catch(() => '')),
  };

  // import basket once to see selected count
  const imp = page.locator('[data-testid="svc-org-cap-import-basket"]');
  if (await imp.count()) {
    await imp.click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(1000);
  }
  out.after_import = {
    tag_count: await tags.count(),
    start_disabled: await start.isDisabled().catch(() => null),
    head: ((await page.locator('.svc-org-cap-compare__head').innerText().catch(() => '')) || '').replace(/\s+/g, ' '),
    blockers: ((await page.locator('.svc-org-cap-blockers').innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 200),
  };

  // records tab
  await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
  await page.waitForTimeout(2000);
  const mainTxt = (await page.locator('main').innerText().catch(() => '')) || '';
  const viewProcess = page.getByText('查看过程', { exact: true });
  const viewResult = page.getByText('查看结果', { exact: true });
  out.records = {
    url: page.url(),
    has_computing: /计算中|运行中|排队|generating|processing/i.test(mainTxt),
    status_tokens: [...mainTxt.matchAll(/(已完成|计算中|运行中|失败|排队|取消)/g)].map((m) => m[1]),
    view_process_count: await viewProcess.count(),
    view_result_count: await viewResult.count(),
    task_ids: [...mainTxt.matchAll(/SVC-\d{8}-\d{3}/g)].map((m) => m[0]),
    snippet: mainTxt.split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 40),
  };

  // open process of first done row
  if ((await viewProcess.count()) > 0) {
    await viewProcess.first().click({ timeout: 5000 });
    await page.waitForTimeout(2000);
    const pTxt = (await page.locator('main').innerText().catch(() => '')) || '';
    out.process_view = {
      url: page.url(),
      has_percent_progress: /\d+\s*%/.test(pTxt) && /进度|完成度|percent/i.test(pTxt),
      has_rerun_label: /重新分析/.test(pTxt),
      has_computing_copy: /计算中|生成中|分析中/.test(pTxt),
      snippet: pTxt.split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 35),
    };
  }

  out.gate = {
    can_start: out.after_import.start_disabled === false && (out.after_import.tag_count || 0) >= 2,
    ticket: 'ENV-SVCCAP-BASKET-ORG-LT2-001',
    conclusion: (out.after_import.tag_count || 0) < 2
      ? '对象 <2 → 禁止过程态发起机检；本条 B+allow_skip'
      : '对象≥2 可尝试发起链',
  };
} catch (e) {
  out.error = String(e).slice(0, 400);
}

fs.writeFileSync(path.join(outDir, 'scout-p009.json'), JSON.stringify(out, null, 2));
await page.screenshot({ path: path.join(outDir, 'scout-p009.png'), fullPage: true }).catch(() => {});
await browser.close();
console.log(JSON.stringify({ ok: !out.error, gate: out.gate, config: out.config, after_import: out.after_import, records: out.records && { ...out.records, snippet: undefined }, process_view: out.process_view && { url: out.process_view.url, has_percent_progress: out.process_view.has_percent_progress, has_rerun_label: out.process_view.has_rerun_label } }, null, 2));
