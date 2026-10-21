#!/usr/bin/env node
/**
 * P0-08（FUNC-00662 明细表下钻画像）一次性无头探针。产物落同目录 scout-p008-detail.json；勿当 runner。
 * 目标：
 *   1) 结果壳明细表现状——诚实空（无行可点，归 ENV ticket）还是已到位（svc-org-link 可点）；
 *   2) 滚动容器结构（scrollHeight/scrollY 可设性），为「关闭后滚动位置保留」断言定口径；
 *   3) 若有机构名按钮：真点一个 → .arco-drawer 开？标题？关 → scrollY 保留？（目标态链路直接验一遍）
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
const target = `${baseUrl.replace(/\/?$/, '')}/service/institution-judgment?workspace=trend&tab=trend`;
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

await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(2000);
await closeBasket(page);

const out = { probed_at: new Date().toISOString(), url_entry: page.url() };

// —— 进结果壳（同 P0-06/07 路径）——
const recTab = page.locator('[role=tab][data-tab-key="records"]');
await recTab.waitFor({ state: 'visible', timeout: 12000 });
await recTab.click({ timeout: 8000 });
await page.waitForTimeout(1500);
const viewBtn = page.getByRole('button', { name: '查看结果' }).first();
await viewBtn.waitFor({ state: 'visible', timeout: 12000 });
await viewBtn.click({ timeout: 8000 });
await page.waitForTimeout(2500);
out.url_result = page.url();
const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
out.honest_empty = /当前结果快照没有年序列/.test(body);

// —— 明细区勘测：区块在？诚实空提示？表格行？机构名按钮？——
out.detail_zone = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const zoneTxt = main.innerText || '';
  const hasZone = /主领域年度明细/.test(zoneTxt);
  const isEmptyHint = /暂无主领域年度明细/.test(zoneTxt);
  const links = [...main.querySelectorAll('button.svc-org-link')].map((b) => ({ name: (b.textContent || '').trim().slice(0, 40), aria: b.getAttribute('aria-label') || '', visible: !!(b.offsetWidth || b.offsetHeight) }));
  const tables = main.querySelectorAll('table');
  const rows = main.querySelectorAll('table tbody tr').length;
  return { has_zone: hasZone, empty_hint: isEmptyHint, svc_org_link_count: links.length, svc_org_links: links.slice(0, 5), table_count: tables.length, tbody_rows: rows };
});

// —— 滚动容器勘测 ——
out.scroll_probe = await page.evaluate(() => {
  const de = document.documentElement;
  const main = document.querySelector('main');
  return {
    scrollHeight: de.scrollHeight, innerHeight: window.innerHeight,
    scrollable: de.scrollHeight > window.innerHeight,
    main_overflow: main ? getComputedStyle(main).overflowY : null,
    scrollY_before: window.scrollY,
  };
});

// —— 若有机构名按钮：真点一个验目标态链路（抽屉开→关→scrollY 保留）——
if (out.detail_zone.svc_org_link_count > 0) {
  const link = page.locator('main button.svc-org-link').first();
  await link.scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);
  // 稳定基准：再微滚到按钮附近并取 y0
  await page.evaluate(() => window.scrollBy(0, -40));
  await page.waitForTimeout(300);
  out.scrollY0_after_anchor = await page.evaluate(() => window.scrollY);
  await link.click({ timeout: 6000 });
  await page.waitForTimeout(1200);
  out.drawer_after_click = await page.evaluate(() => {
    const dr = document.querySelector('.arco-drawer');
    if (!dr) return { present: false };
    const cs = getComputedStyle(dr);
    const title = (dr.querySelector('.arco-drawer-title, [class*=title]')?.textContent || dr.innerText || '').trim().slice(0, 80);
    return { present: true, visible: cs.display !== 'none' && dr.offsetWidth > 0, title, scrollY_while_open: window.scrollY };
  });
  const closeBtn = page.locator('.arco-drawer .arco-drawer-close-btn').first();
  if (await closeBtn.count()) {
    await closeBtn.click({ timeout: 5000 });
    await page.waitForTimeout(800);
    out.after_close = await page.evaluate(() => ({
      drawer_visible: [...document.querySelectorAll('.arco-drawer')].some((d) => { const s = getComputedStyle(d); return s.display !== 'none' && d.offsetWidth > 0; }),
      scrollY_after_close: window.scrollY,
      detail_zone_back: /主领域年度明细/.test((document.querySelector('main')?.innerText) || ''),
    }));
  } else {
    out.after_close = { close_btn: 'absent' };
  }
  await page.screenshot({ path: path.join(outDir, 'scout-p008-drilldown.png') });
  out.drilldown_shot = 'scout-p008-drilldown.png';
} else {
  out.branch = out.detail_zone.empty_hint ? 'honest-empty-no-row' : 'zone-without-link';
  await page.locator('main').getByText('主领域年度明细').first().scrollIntoViewIfNeeded().catch(() => {});
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, 'scout-p008-detail-empty.png') });
  out.empty_shot = 'scout-p008-detail-empty.png';
}

fs.writeFileSync(path.join(outDir, 'scout-p008-detail.json'), JSON.stringify(out, null, 2));
await browser.close();
console.log(JSON.stringify({ honest_empty: out.honest_empty, detail: out.detail_zone, scroll: out.scroll_probe, branch: out.branch || 'drilldown-probed', drawer: out.drawer_after_click || null, after_close: out.after_close || null }, null, 2));
console.log('probe ok →', outDir);
