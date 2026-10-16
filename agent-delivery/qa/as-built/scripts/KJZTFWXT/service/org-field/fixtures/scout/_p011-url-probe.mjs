#!/usr/bin/env node
/**
 * 一次性无头实勘 · P0-11 / FUNC-00651 URL 直达与刷新保留。
 * 产物落同目录 scout-p011.json；勿当 runner。禁 IDE 有头。
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

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  const userBox = page.locator('input[placeholder*=用户名], input[type=text]').first();
  const passBox = page.locator('input[type=password]').first();
  await userBox.waitFor({ state: 'visible', timeout: 15000 });
  await passBox.waitFor({ state: 'visible', timeout: 15000 });
  await userBox.fill('admin');
  await passBox.fill('123456');
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

async function snap(page) {
  const url = page.url();
  const u = new URL(url);
  const mainTxt = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  const tags = page.locator('[data-testid="svc-org-analysis-context"] .arco-tag.svc-org-pick-tag');
  const tagTexts = [];
  const tc = await tags.count();
  for (let i = 0; i < tc; i++) tagTexts.push(((await tags.nth(i).innerText().catch(() => '')) || '').trim());
  // 页头 Tab 用 data-tab-key（P0-01/trend 同款；getByRole 易被对比篮 Tab 污染）
  const mainTab = page.locator('[role=tab][data-tab-key="coverage"], [role=tab][data-tab-key="field"]').first();
  const recTab = page.locator('[role=tab][data-tab-key="records"]').first();
  const mainByRole = page.getByRole('tab', { name: '服务机构产业领域分析', exact: true }).first();
  const recByRole = page.getByRole('tab', { name: '分析记录', exact: true }).first();
  const mainEl = (await mainTab.count()) ? mainTab : mainByRole;
  const recEl = (await recTab.count()) ? recTab : recByRole;
  const mainSel = await mainEl.getAttribute('aria-selected').catch(() => null);
  const recSel = await recEl.getAttribute('aria-selected').catch(() => null);
  const mainCls = await mainEl.getAttribute('class').catch(() => '');
  const recCls = await recEl.getAttribute('class').catch(() => '');
  const dataKeys = await page.evaluate(() =>
    [...document.querySelectorAll('[role=tab][data-tab-key]')].map((el) => ({
      key: el.getAttribute('data-tab-key'),
      selected: el.getAttribute('aria-selected'),
      cls: (el.className || '').slice(0, 40),
      text: (el.innerText || '').trim().slice(0, 20),
    })),
  );
  return {
    url,
    workspace: u.searchParams.get('workspace'),
    tab: u.searchParams.get('tab'),
    orgIds: u.searchParams.getAll('org_ids[]').length
      ? u.searchParams.getAll('org_ids[]')
      : u.searchParams.getAll('org_ids'),
    selectedLine: (mainTxt.match(/已选机构（\d+\s*家）/) || [null])[0],
    tagTexts,
    tagCount: tagTexts.length,
    mainTabSelected: mainSel === 'true' || /active/.test(mainCls || ''),
    recTabSelected: recSel === 'true' || /active/.test(recCls || ''),
    dataKeys,
    title: await page.title(),
    hasConfig: /分析配置/.test(mainTxt),
    hasRecordsList: /任务/.test(mainTxt) && /SVC-\d+-\d+/.test(mainTxt),
  };
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  const out = { surveyed_at: new Date().toISOString(), case: 'P0-11', func: 'FUNC-00651' };
  const target = new URL(route.replace(/^\//, ''), baseUrl).toString();

  try {
    // 先显式登录再深链（survey-page / env-gate 同款）
    await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
    await ensureLogin(page);
    await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await ensureLogin(page);
    if (page.url().includes('/login')) {
      await ensureLogin(page);
      await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
    }
    await page.waitForTimeout(2000);
    await closeBasket(page);

    // 清脏：有已选则清空
    const t0 = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    if (/已选机构（[1-9]/.test(t0)) {
      const clr = page.locator('main').getByRole('button', { name: '清空' });
      if (await clr.count()) {
        await clr.first().click({ timeout: 5000 });
        await page.waitForTimeout(500);
      }
    }
    if (/org_ids|view=/.test(page.url())) {
      await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(1500);
      await closeBasket(page);
    }

    out.empty = await snap(page);

    // 选 1 家（checkbox 可能异步渲染，滚动等待同 trend P0-03）
    await page.getByRole('button', { name: '选择机构' }).first().click({ timeout: 8000 });
    await page.waitForTimeout(800);
    const dialog = page.locator('.arco-modal:visible, .arco-modal').filter({ hasText: '选择服务机构' }).first();
    await dialog.waitFor({ state: 'visible', timeout: 8000 });
    const boxes = dialog.locator('.arco-checkbox:not(.arco-checkbox-disabled) input[type=checkbox], .arco-checkbox:not(.arco-checkbox-disabled)');
    for (let i = 0; i < 20 && !(await boxes.count()); i++) {
      const body = dialog.locator('.arco-modal-body, .arco-table-body, .arco-list').first();
      if (await body.count()) {
        try {
          await body.evaluate((el) => {
            el.scrollTop = (el.scrollTop || 0) + 240;
          });
        } catch {}
      }
      await page.waitForTimeout(400);
    }
    if (!(await boxes.count())) {
      // 兜底：深链已知 org_id（env-gate / scout-p009 实证）
      await page.keyboard.press('Escape').catch(() => {});
      await page.waitForTimeout(500);
      const known =
        'http://111.198.38.90:50892/service/institution-judgment?workspace=field&tab=coverage&org_ids[]=79bbcfc0e68027808f1f4caf1b6f0469';
      await page.goto(known, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(2000);
      await closeBasket(page);
      out.selectPath = 'deeplink_known_org';
    } else {
      try {
        await boxes.first().scrollIntoViewIfNeeded();
      } catch {}
      await boxes.first().click({ timeout: 8000 });
      await page.waitForTimeout(300);
      await dialog.getByRole('button', { name: '确定', exact: true }).last().click({ timeout: 8000 });
      await page.waitForTimeout(1200);
      out.selectPath = 'modal_pick';
    }
    out.afterSelect = await snap(page);
    await page.screenshot({ path: path.join(outDir, 'p011-after-select.png'), fullPage: false });

    // 切到分析记录 Tab（非默认 tab，验 URL tab 恢复）
    const recTab = page.locator('[role=tab][data-tab-key="records"]').first();
    const recTabAlt = page.getByRole('tab', { name: '分析记录', exact: true }).first();
    if (await recTab.count()) await recTab.click({ timeout: 8000 });
    else await recTabAlt.click({ timeout: 8000 });
    await page.waitForTimeout(1500);
    await page.waitForURL(/tab=records/, { timeout: 8000 }).catch(() => {});
    out.afterRecordsTab = await snap(page);
    await page.screenshot({ path: path.join(outDir, 'p011-after-records-tab.png'), fullPage: false });

    const capturedUrl = page.url();
    out.capturedUrl = capturedUrl;

    // 步骤①：同 page 冷加载 = 新标签直达语义（graph P0-24 同款）
    await page.goto(capturedUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await ensureLogin(page);
    await page.waitForTimeout(2500);
    await closeBasket(page);
    out.afterDirect = await snap(page);
    await page.screenshot({ path: path.join(outDir, 'p011-after-direct.png'), fullPage: false });

    // 步骤②：刷新
    await page.reload({ waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2500);
    await closeBasket(page);
    out.afterReload = await snap(page);
    await page.screenshot({ path: path.join(outDir, 'p011-after-reload.png'), fullPage: false });

    // 切回 coverage 验已选机构 UI 回显（records 态可能不渲染 tag）
    await page.goto(
      page.url().replace(/tab=records/, 'tab=coverage').replace(/([?&])tab=[^&]*/, '$1tab=coverage'),
      { waitUntil: 'domcontentloaded', timeout: 60000 },
    ).catch(async () => {
      const ids = (out.afterReload?.orgIds || out.afterDirect?.orgIds || []).map((id) => `org_ids[]=${id}`).join('&');
      await page.goto(
        `http://111.198.38.90:50892/service/institution-judgment?workspace=field&tab=coverage${ids ? '&' + ids : ''}`,
        { waitUntil: 'domcontentloaded', timeout: 60000 },
      );
    });
    await page.waitForTimeout(2000);
    await closeBasket(page);
    out.afterBackCoverage = await snap(page);
    await page.screenshot({ path: path.join(outDir, 'p011-back-coverage.png'), fullPage: false });

    // 判定摘要（records 态已选以 URL org_ids 为主通道；UI 回显在 coverage 验）
    const checks = [];
    const d = out.afterDirect;
    const r = out.afterReload;
    const base = out.afterRecordsTab;
    const sel = out.afterSelect;
    if (d.workspace !== 'field') checks.push('direct workspace≠field: ' + d.workspace);
    if (d.tab !== 'records' && base.tab === 'records') checks.push('direct tab 回落: ' + d.tab + ' expect records');
    if (!(d.orgIds || []).length && (sel.orgIds || []).length) checks.push('direct 无 org_ids（选后有）');
    if ((sel.orgIds || []).length && JSON.stringify(d.orgIds) !== JSON.stringify(sel.orgIds) && d.tab === 'records') {
      // records 直达时 org_ids 应随 URL 保留
      if (!(d.orgIds || []).length) checks.push('direct records 丢 org_ids');
    }
    if (d.tab === 'records' && !d.recTabSelected && !d.hasRecordsList) {
      checks.push('direct 未落分析记录上下文（Tab/列表皆无）');
    }
    if (r.workspace !== 'field') checks.push('reload workspace≠field');
    if (r.tab !== d.tab) checks.push('reload tab 漂移: ' + r.tab + ' vs ' + d.tab);
    if ((d.orgIds || []).length && JSON.stringify(r.orgIds) !== JSON.stringify(d.orgIds)) {
      checks.push('reload org_ids 漂移');
    }
    const cov = out.afterBackCoverage;
    if ((sel.orgIds || []).length && !(cov.selectedLine || '').match(/已选机构（[1-9]/) && cov.tagCount < 1) {
      checks.push('回 coverage 已选未恢复: ' + cov.selectedLine + ' tags=' + cov.tagCount);
    }
    out.checks = checks;
    out.verdict = checks.length ? 'fail_hints' : 'probe_ok';

    fs.writeFileSync(path.join(outDir, 'scout-p011.json'), JSON.stringify(out, null, 2));
    console.log(JSON.stringify({ verdict: out.verdict, checks, capturedUrl, afterDirect: d, afterReload: r }, null, 2));
  } catch (e) {
    out.error = String(e && e.stack ? e.stack : e);
    fs.writeFileSync(path.join(outDir, 'scout-p011.json'), JSON.stringify(out, null, 2));
    console.error(out.error);
    process.exitCode = 1;
  } finally {
    await browser.close();
  }
}

main();
