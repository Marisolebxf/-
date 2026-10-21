#!/usr/bin/env node
/**
 * 一次性无头实勘 · P0-009 领域筛选不改指纹（配置态筛选框键入→领域展示收窄→清除→恢复全量）。
 * 产物落同目录 scout-p009.json + 截图；勿当 runner。只读行为勘察，不判验收。禁 IDE 有头。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const route = '/service/institution-judgment?workspace=field&tab=coverage';
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

// 下拉选项盘点：可见 trigger-popup 内 .arco-select-option 全量/可见文本/空态
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
    const empty = pop.querySelector('.arco-empty');
    return {
      open: true,
      total: opts.length,
      visible: opts.filter((o) => o.h > 0).map((o) => o.text).filter(Boolean),
      emptyText: empty ? (empty.textContent || '').trim().slice(0, 30) : null,
    };
  });
}

async function configSnapshot(page) {
  return await page.evaluate(() => {
    const t = (document.querySelector('main') || document.body).textContent || '';
    const sel = document.querySelector('.industry-catalog-select');
    return {
      selectedLine: (t.match(/已选机构（\d+\s*家）/) || [null])[0],
      hasStart: /开始分析/.test(t),
      hasProcessing: /生成中|分析中|loading|任务状态/.test(t),
      catalogSelValue: sel ? (sel.textContent || '').trim().slice(0, 30) : null,
      filterPh: !!document.querySelector('input[placeholder="筛选领域（不改分析指纹）"]'),
      url: location.href,
    };
  });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), stages: {} };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await freshGoto(page);
  out.stages.baseline = await configSnapshot(page);

  // 阶段1（配置空态）：打开产业领域下拉，盘点全量选项
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  out.stages.dropdownFull = await dropdownState(page);
  await page.screenshot({ path: path.join(outDir, 'p009-0-dropdown-full.png') });

  // 阶段2：键入首条选项全文 → 盘点收窄
  const kw = (out.stages.dropdownFull.visible || [])[0] || null;
  out.keyword = kw;
  if (kw) {
    const filterInput = page.getByPlaceholder('筛选领域（不改分析指纹）');
    await filterInput.fill(kw, { timeout: 5000 });
    await page.waitForTimeout(800);
    out.stages.dropdownFiltered = await dropdownState(page);
    await page.screenshot({ path: path.join(outDir, 'p009-1-dropdown-filtered.png') });

    // 阶段3：清除 → 恢复全量
    await filterInput.fill('', { timeout: 5000 });
    await page.waitForTimeout(800);
    out.stages.dropdownCleared = await dropdownState(page);
  }
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);
  out.stages.afterEmptyConfig = await configSnapshot(page);

  // 阶段4：自含构造已选 1 家机构（同 P0-06 路径），复测筛选交互在有已选机构时同样成立
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
  await page.screenshot({ path: path.join(outDir, 'p009-2-final.png') });

  // 结论标记：配置态与已选态筛选是否都可真实断言（收窄且恢复）
  const ok = (full, filt, clr) => full && filt && clr && full.open && filt.open && clr.open
    && full.visible.length > 1 && filt.visible.length >= 1 && filt.visible.length < full.visible.length
    && clr.visible.length === full.visible.length;
  out.verdict = {
    emptyStateFilterOk: ok(out.stages.dropdownFull, out.stages.dropdownFiltered, out.stages.dropdownCleared),
    pickedStateFilterOk: ok(out.stages.pickedDropdownFull, out.stages.pickedDropdownFiltered, out.stages.pickedDropdownCleared),
    urlStable: !/view=processing|task_id=/.test(out.stages.final.url),
  };
  fs.writeFileSync(path.join(outDir, 'scout-p009.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ keyword: out.keyword, verdict: out.verdict, dropdownFull: out.stages.dropdownFull, dropdownFiltered: out.stages.dropdownFiltered, dropdownCleared: out.stages.dropdownCleared }, null, 2));
} catch (e) {
  out.overall = 'error';
  out.error = String(e).slice(0, 800);
  fs.writeFileSync(path.join(outDir, 'scout-p009.json'), JSON.stringify(out, null, 2));
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
