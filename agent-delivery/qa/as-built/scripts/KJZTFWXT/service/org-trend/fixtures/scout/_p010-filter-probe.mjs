#!/usr/bin/env node
/**
 * 一次性无头实勘 · P0-010 领域筛选不改指纹（trend workspace 同构性验证）。
 * 配置态筛选键入→候选收窄→清除→恢复全量；URL 无任务参数；已选机构集合不变。
 * 产物落同目录 scout-p010-filter.json + 截图；勿当 runner。只读行为勘察，不判验收。禁 IDE 有头。
 * 蓝本：org-field/fixtures/scout/_p009-filter-probe.mjs（姊妹仓零归票通过），改路由 + 加已选 tag 挂载侦查。
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
const route = '/service/institution-judgment?workspace=trend&tab=trend';
const outDir = __dirname;

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
  if (page.url().includes('/login')) {
    await ensureLogin(page);
    await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  }
  await page.waitForTimeout(2000);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

async function dropdownState(page) {
  return await page.evaluate(() => {
    const pops = Array.from(document.querySelectorAll('.arco-trigger-popup')).filter((p) => {
      const r = p.getBoundingClientRect();
      return r.width > 0 && r.height > 0 && p.querySelector('.arco-select-option, .arco-select-dropdown');
    });
    const pop = pops[pops.length - 1];
    if (!pop) return { open: false };
    const opts = Array.from(pop.querySelectorAll('.arco-select-option')).map((o) => ({
      text: (o.textContent || '').trim(),
      h: Math.round(o.getBoundingClientRect().height),
    }));
    return {
      open: true,
      total: opts.length,
      visible: opts.filter((o) => o.h > 0).map((o) => o.text).filter(Boolean),
    };
  });
}

async function configSnapshot(page) {
  return await page.evaluate(() => {
    const t = (document.querySelector('main') || document.body).textContent || '';
    return {
      selectedLine: (t.match(/已选机构（\d+\s*家）/) || [null])[0],
      hasStart: /开始分析/.test(t),
      hasProcessing: /生成中|计算中/.test(t),
      hasResultShell: /服务机构新增数量趋势/.test(t),
      tagMount: !!document.querySelector('[data-testid="svc-org-analysis-context"]'),
      pickTagCount: document.querySelectorAll('.arco-tag.svc-org-pick-tag').length,
      pickTagTexts: Array.from(document.querySelectorAll('.arco-tag.svc-org-pick-tag')).map((e) => (e.textContent || '').trim()).slice(0, 3),
      url: location.href,
    };
  });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), workspace: 'trend', stages: {} };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await freshGoto(page);
  out.stages.baseline = await configSnapshot(page);

  // 阶段1：配置空态开产业下拉，盘点全量
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  out.stages.dropdownFull = await dropdownState(page);
  await page.screenshot({ path: path.join(outDir, 'p010-0-dropdown-full.png') });

  // 阶段2：键入首条选项全文 → 收窄
  const kw = (out.stages.dropdownFull.visible || [])[0] || null;
  out.keyword = kw;
  if (kw) {
    await page.getByPlaceholder('筛选领域（不改分析指纹）').fill(kw, { timeout: 5000 });
    await page.waitForTimeout(800);
    out.stages.dropdownFiltered = await dropdownState(page);
    await page.screenshot({ path: path.join(outDir, 'p010-1-dropdown-filtered.png') });
    // 阶段3：清除 → 恢复全量
    await page.getByPlaceholder('筛选领域（不改分析指纹）').fill('', { timeout: 5000 });
    await page.waitForTimeout(800);
    out.stages.dropdownCleared = await dropdownState(page);
  }
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);
  out.stages.afterEmptyConfig = await configSnapshot(page);

  // 阶段4：自含构造已选 1 家机构（同 P0-03/P0-04 路径），复测筛选交互在有已选机构时同样成立
  const pick = page.getByRole('button', { name: '选择机构' }).first();
  await pick.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  const dialog = page.locator('.arco-modal:visible').filter({ hasText: '选择服务机构' }).first();
  await dialog.locator('.arco-checkbox:not(.arco-checkbox-disabled)').first().click({ timeout: 5000 });
  await page.waitForTimeout(300);
  await dialog.locator('.arco-modal-footer button:visible').filter({ hasText: /^确定$/ }).last().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  out.stages.afterPick = await configSnapshot(page);

  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  out.stages.pickedDropdownFull = await dropdownState(page);
  if (kw) {
    await page.getByPlaceholder('筛选领域（不改分析指纹）').fill(kw, { timeout: 5000 });
    await page.waitForTimeout(800);
    out.stages.pickedDropdownFiltered = await dropdownState(page);
    await page.getByPlaceholder('筛选领域（不改分析指纹）').fill('', { timeout: 5000 });
    await page.waitForTimeout(800);
    out.stages.pickedDropdownCleared = await dropdownState(page);
  }
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);
  out.stages.final = await configSnapshot(page);
  await page.screenshot({ path: path.join(outDir, 'p010-2-final.png') });

  // 结论标记：配置态与已选态筛选是否同构可断（收窄且恢复）；URL 稳定；已选 tag 挂载形态
  const ok = (full, filt, clr) => full && filt && clr && full.open && filt.open && clr.open
    && full.visible.length > 1 && filt.visible.length >= 1 && filt.visible.length < full.visible.length
    && clr.visible.length === full.visible.length;
  out.verdict = {
    emptyStateFilterOk: ok(out.stages.dropdownFull, out.stages.dropdownFiltered, out.stages.dropdownCleared),
    pickedStateFilterOk: ok(out.stages.pickedDropdownFull, out.stages.pickedDropdownFiltered, out.stages.pickedDropdownCleared),
    urlStable: !/view=processing|task_id=/.test(out.stages.final.url),
    noAutoRefresh: !out.stages.final.hasResultShell && !out.stages.final.hasProcessing,
    tagMountAvailable: out.stages.afterPick.tagMount || out.stages.afterPick.pickTagCount > 0,
  };
  fs.writeFileSync(path.join(outDir, 'scout-p010-filter.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ keyword: out.keyword, verdict: out.verdict, afterPick: out.stages.afterPick, full: out.stages.pickedDropdownFull, filtered: out.stages.pickedDropdownFiltered, cleared: out.stages.pickedDropdownCleared }, null, 2));
} catch (e) {
  out.overall = 'error';
  out.error = String(e).slice(0, 800);
  fs.writeFileSync(path.join(outDir, 'scout-p010-filter.json'), JSON.stringify(out, null, 2));
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
