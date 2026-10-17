#!/usr/bin/env node
/**
 * 一次性无头实勘 · P0-12 / FUNC-00652 三兄弟 workspace 隔离。
 * 产物落同目录 scout-p012.json；勿当 runner。禁 IDE 有头。
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
const fieldRoute = '/service/institution-judgment?workspace=field&tab=coverage';
const knownOrg = '79bbcfc0e68027808f1f4caf1b6f0469';
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

async function snap(page, label) {
  const url = page.url();
  const u = new URL(url);
  const mainTxt = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  const tags = page.locator('[data-testid="svc-org-analysis-context"] .arco-tag.svc-org-pick-tag');
  const tagTexts = [];
  const tc = await tags.count();
  for (let i = 0; i < tc; i++) tagTexts.push(((await tags.nth(i).innerText().catch(() => '')) || '').trim());
  const filterVal = await page.getByPlaceholder('筛选领域（不改分析指纹）').inputValue().catch(() => null);
  const title = await page.title();
  const dataKeys = await page.evaluate(() =>
    [...document.querySelectorAll('[role=tab][data-tab-key]')].map((el) => ({
      key: el.getAttribute('data-tab-key'),
      selected: el.getAttribute('aria-selected'),
      text: (el.innerText || '').trim().slice(0, 24),
    })),
  );
  const menuItems = await page.evaluate(() =>
    [...document.querySelectorAll('.arco-menu-item, [role=menuitem]')]
      .map((el) => (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 40))
      .filter((t) => /服务机构|产业领域|新增趋势|技术力/.test(t)),
  );
  return {
    label,
    url,
    workspace: u.searchParams.get('workspace'),
    tab: u.searchParams.get('tab'),
    view: u.searchParams.get('view'),
    taskId: u.searchParams.get('task_id'),
    orgIds: u.searchParams.getAll('org_ids[]').length
      ? u.searchParams.getAll('org_ids[]')
      : u.searchParams.getAll('org_ids'),
    selectedLine: (mainTxt.match(/已选机构（\d+\s*家）/) || [null])[0],
    tagTexts,
    tagCount: tagTexts.length,
    filterVal,
    title,
    dataKeys,
    menuItems,
    hasConfig: /分析配置/.test(mainTxt),
    hasFieldTitle: /服务机构产业领域分析/.test(mainTxt) || /服务机构产业领域分析/.test(title),
    hasTrendTitle: /服务机构新增趋势分析/.test(mainTxt) || /服务机构新增趋势分析/.test(title),
    hasCapTitle: /服务机构技术力评估分析/.test(mainTxt) || /服务机构技术力评估分析/.test(title),
    hasFieldResultLeak: /覆盖矩阵|覆盖热力|当前结果快照没有覆盖矩阵/.test(mainTxt),
    hasTaskLeak: /生成中|计算中|分析结果已生成|view=processing/.test(mainTxt) || !!u.searchParams.get('view'),
    bodyHit: mainTxt.slice(0, 400).replace(/\s+/g, ' '),
  };
}

async function clickMenu(page, nameRe) {
  const m = page.getByRole('menuitem', { name: nameRe }).first();
  if (await m.isVisible().catch(() => false)) {
    await m.click({ timeout: 8000 });
    return 'menuitem';
  }
  const alt = page.locator('aside, nav, .arco-menu').getByText(nameRe).first();
  await alt.click({ timeout: 8000 });
  return 'text';
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  const posts = [];
  page.on('request', (r) => {
    if (r.method() === 'POST' && /\/topicAsync\/topic\/v1\/analysis\/tasks\/?(\?|$)/.test(r.url())) {
      posts.push(r.url().slice(0, 140));
    }
  });
  const out = {
    surveyed_at: new Date().toISOString(),
    case: 'P0-12',
    func: 'FUNC-00652',
    posts,
  };

  try {
    await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
    await ensureLogin(page);
    await page.goto(new URL(fieldRoute.replace(/^\//, ''), baseUrl).toString(), {
      waitUntil: 'domcontentloaded',
      timeout: 60000,
    });
    await ensureLogin(page);
    await page.waitForTimeout(2000);
    await closeBasket(page);

    // 清脏
    const t0 = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    if (/已选机构（[1-9]/.test(t0)) {
      const clr = page.locator('main').getByRole('button', { name: '清空' });
      if (await clr.count()) {
        await clr.first().click({ timeout: 5000 });
        await page.waitForTimeout(500);
      }
    }
    if (/org_ids|view=/.test(page.url())) {
      await page.goto(new URL(fieldRoute.replace(/^\//, ''), baseUrl).toString(), {
        waitUntil: 'domcontentloaded',
        timeout: 60000,
      });
      await page.waitForTimeout(1500);
      await closeBasket(page);
    }

    // 选 1 家（弹窗 / 深链兜底）
    await page.getByRole('button', { name: '选择机构' }).first().click({ timeout: 8000 });
    await page.waitForTimeout(800);
    const dialog = page.locator('.arco-modal:visible, .arco-modal').filter({ hasText: '选择服务机构' }).first();
    await dialog.waitFor({ state: 'visible', timeout: 8000 });
    const boxes = dialog.locator(
      '.arco-checkbox:not(.arco-checkbox-disabled) input[type=checkbox], .arco-checkbox:not(.arco-checkbox-disabled)',
    );
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
      await page.keyboard.press('Escape').catch(() => {});
      await page.waitForTimeout(400);
      await page.goto(
        `http://111.198.38.90:50892/service/institution-judgment?workspace=field&tab=coverage&org_ids[]=${knownOrg}`,
        { waitUntil: 'domcontentloaded', timeout: 60000 },
      );
      await page.waitForTimeout(2000);
      await closeBasket(page);
      out.selectPath = 'deeplink_known_org';
    } else {
      await boxes.first().click({ timeout: 8000 });
      await page.waitForTimeout(300);
      await dialog.getByRole('button', { name: '确定', exact: true }).last().click({ timeout: 8000 });
      await page.waitForTimeout(1200);
      out.selectPath = 'modal_pick';
    }

    // 领域筛选键入（便于验切回保留）
    const filterInput = page.getByPlaceholder('筛选领域（不改分析指纹）');
    if (await filterInput.count()) {
      await filterInput.fill('新一代', { timeout: 5000 });
      await page.waitForTimeout(500);
      out.filterSeed = '新一代';
    }
    out.afterFieldSelect = await snap(page, 'field+org+filter');
    await page.screenshot({ path: path.join(outDir, 'p012-field.png'), fullPage: false });
    const postsAfterSetup = posts.length;

    // 切 trend（侧栏优先；失败则 URL goto）
    let switchMode = {};
    try {
      switchMode.trend = await clickMenu(page, /服务机构新增趋势分析/);
      await page.waitForTimeout(2200);
      await closeBasket(page);
    } catch (e) {
      switchMode.trend = 'goto_fallback:' + String(e.message || e).slice(0, 80);
      await page.goto(
        'http://111.198.38.90:50892/service/institution-judgment?workspace=trend&tab=trend',
        { waitUntil: 'domcontentloaded', timeout: 60000 },
      );
      await page.waitForTimeout(2000);
      await closeBasket(page);
    }
    out.afterTrend = await snap(page, 'trend');
    await page.screenshot({ path: path.join(outDir, 'p012-trend.png'), fullPage: false });

    // 切 capability
    try {
      switchMode.capability = await clickMenu(page, /服务机构技术力评估分析/);
      await page.waitForTimeout(2200);
      await closeBasket(page);
    } catch (e) {
      switchMode.capability = 'goto_fallback:' + String(e.message || e).slice(0, 80);
      await page.goto(
        'http://111.198.38.90:50892/service/institution-judgment?workspace=capability&tab=capability',
        { waitUntil: 'domcontentloaded', timeout: 60000 },
      );
      await page.waitForTimeout(2000);
      await closeBasket(page);
    }
    out.afterCapability = await snap(page, 'capability');
    await page.screenshot({ path: path.join(outDir, 'p012-capability.png'), fullPage: false });

    // 切回 field
    try {
      switchMode.fieldBack = await clickMenu(page, /服务机构产业领域分析/);
      await page.waitForTimeout(2600);
      await closeBasket(page);
    } catch (e) {
      switchMode.fieldBack = 'goto_fallback:' + String(e.message || e).slice(0, 80);
      await page.goto(
        'http://111.198.38.90:50892/service/institution-judgment?workspace=field&tab=coverage',
        { waitUntil: 'domcontentloaded', timeout: 60000 },
      );
      await page.waitForTimeout(2000);
      await closeBasket(page);
    }
    out.afterBackField = await snap(page, 'back-field');
    await page.screenshot({ path: path.join(outDir, 'p012-back-field.png'), fullPage: false });

    out.switchMode = switchMode;
    out.postsAfterSetup = postsAfterSetup;
    out.postsAfterSwitch = posts.length;
    out.postsDuringSwitch = posts.slice(postsAfterSetup);

    // 判定摘要
    const f0 = out.afterFieldSelect;
    const t = out.afterTrend;
    const c = out.afterCapability;
    const b = out.afterBackField;
    const checks = [];
    if (t.workspace !== 'trend') checks.push('trend workspace≠trend: ' + t.workspace);
    if (t.hasFieldResultLeak) checks.push('trend 泄漏 field 结果文案');
    if (t.hasTaskLeak && t.view) checks.push('trend 带 view/任务态: ' + t.view);
    if (!t.hasTrendTitle) checks.push('trend 页标题/主区未落趋势工作区');
    if (c.workspace !== 'capability') checks.push('cap workspace≠capability: ' + c.workspace);
    if (c.hasFieldResultLeak) checks.push('cap 泄漏 field 结果文案');
    if (c.hasTaskLeak && c.view) checks.push('cap 带 view/任务态: ' + c.view);
    if (!c.hasCapTitle) checks.push('cap 页标题/主区未落技术力工作区');
    if (b.workspace !== 'field') checks.push('切回 workspace≠field: ' + b.workspace);
    if (!(b.selectedLine || '').match(/已选机构（[1-9]/) && b.tagCount < 1 && !(b.orgIds || []).length) {
      checks.push('切回已选机构未保留: line=' + b.selectedLine + ' tags=' + b.tagCount + ' orgs=' + JSON.stringify(b.orgIds));
    }
    if (out.filterSeed && b.filterVal !== out.filterSeed && b.filterVal !== null) {
      // filter 可能不跨 workspace 保留——记 hint，不强制 fail
      out.filterKept = false;
      out.filterNote = `filter seed=${out.filterSeed} back=${b.filterVal}`;
    } else if (out.filterSeed) {
      out.filterKept = b.filterVal === out.filterSeed;
    }
    if (out.postsDuringSwitch.length) {
      checks.push('切换段自动 POST 任务: ' + JSON.stringify(out.postsDuringSwitch));
    }
    if (b.view || b.taskId) checks.push('切回带任务态: view=' + b.view + ' task=' + b.taskId);

    out.checks = checks;
    out.verdict = checks.length ? 'fail_hints' : 'probe_ok';
    fs.writeFileSync(path.join(outDir, 'scout-p012.json'), JSON.stringify(out, null, 2));
    console.log(
      JSON.stringify(
        {
          verdict: out.verdict,
          checks,
          switchMode,
          filterKept: out.filterKept,
          filterNote: out.filterNote,
          postsDuringSwitch: out.postsDuringSwitch,
          afterField: { ws: f0.workspace, orgs: f0.orgIds, selected: f0.selectedLine, filter: f0.filterVal },
          afterTrend: { ws: t.workspace, orgs: t.orgIds, title: t.hasTrendTitle, leak: t.hasFieldResultLeak, view: t.view },
          afterCap: { ws: c.workspace, orgs: c.orgIds, title: c.hasCapTitle, leak: c.hasFieldResultLeak, view: c.view },
          afterBack: { ws: b.workspace, orgs: b.orgIds, selected: b.selectedLine, filter: b.filterVal, view: b.view },
        },
        null,
        2,
      ),
    );
  } catch (e) {
    out.error = String(e && e.stack ? e.stack : e);
    fs.writeFileSync(path.join(outDir, 'scout-p012.json'), JSON.stringify(out, null, 2));
    console.error(out.error);
    process.exitCode = 1;
  } finally {
    await browser.close();
  }
}

main();
