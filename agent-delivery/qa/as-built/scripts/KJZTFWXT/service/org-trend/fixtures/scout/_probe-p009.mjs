#!/usr/bin/env node
/**
 * P0-09（FUNC-00663 研判面板与依据）一次性无头探针。产物落同目录 scout-p009-heat.json；勿当 runner。
 * 目标：
 *   1) 结果壳现状——诚实空（无年序列 payload，归 ENV ticket）还是已到位；
 *   2) 研判面板区现状——「市场热度与趋势研判」面板在否（.svc-org-heat[data-testid=svc-org-heat-panel]）；
 *      评级区形态（no_series message tag / rated 星级+文字评级 tag）；依据行数量；「演示口径」note；评审挂点数量；
 *   3) 若已到位：取证 rated 态真实形态（星级/评级/依据行/GAP 红问号），为目标态断言定口径。
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

// —— 进结果壳（同 P0-06/07/08 路径）——
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

// —— 研判面板区勘测 ——
out.heat_panel = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const panel = main.querySelector('[data-testid="svc-org-heat-panel"]');
  const txt = main.innerText || '';
  const hasTitle = /市场热度与趋势研判/.test(txt);
  const hasNote = /演示口径：评级判读算法待定义/.test(txt);
  const hasNoSeries = /暂无趋势序列，无法给出热度研判/.test(txt);
  const hasAlert = /正式评级由 Python 写入结果快照/.test(txt);
  let rating = null, stars = 0, basisLines = [], gapIcons = [];
  if (panel) {
    rating = (panel.querySelector('.svc-org-heat__rating')?.textContent || '').trim().slice(0, 120);
    stars = panel.querySelectorAll('.arco-rate, [class*=rate] svg, .arco-icon-star, .arco-icon-star-fill').length;
    basisLines = [...(panel.querySelector('.svc-org-heat__basis')?.children || [])].map((d) => (d.textContent || '').trim().slice(0, 120));
    gapIcons = [...panel.querySelectorAll('[aria-label*="GAP"], [class*=question], .arco-icon-question')].map((e) => ({ aria: e.getAttribute('aria-label') || '', cls: (e.className || '').toString().slice(0, 60), visible: !!(e.offsetWidth || e.offsetHeight) })).slice(0, 5);
  }
  const metricAria = [...main.querySelectorAll('[aria-label*="M_SVC_ORG_MARKET_HEAT"], [data-metric-id*="M_SVC_ORG_MARKET_HEAT"]')].map((e) => ({ aria: e.getAttribute('aria-label') || '', visible: !!(e.offsetWidth || e.offsetHeight) })).slice(0, 3);
  const fakeKit = /metric_id|8 件套/.test(panel ? (panel.innerText || '') : '');
  return { has_panel: !!panel, has_title: hasTitle, has_note: hasNote, has_no_series_msg: hasNoSeries, has_alert: hasAlert, rating_text: rating, star_like_count: stars, basis_lines: basisLines, gap_icons: gapIcons, market_heat_mount: metricAria, fake_kit_text: fakeKit, panel_text: (panel?.innerText || '').replace(/\n/g, ' / ').slice(0, 300) };
});

// —— 评审挂点（页面级）：红问号形态（评审模式开启态，勘察记录 in scout-view-result.json）——
out.review_mounts = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const wraps = [...main.querySelectorAll('[data-review-metric]')];
  const badges = [...main.querySelectorAll('.perm-pending-badge, [class*=pending-badge]')];
  return {
    metric_wraps: wraps.map((w) => {
      const btn = w.querySelector('button.metric-spec-card');
      return { ref: w.getAttribute('data-review-metric'), missing: btn ? btn.classList.contains('is-missing') : null, aria: btn ? btn.getAttribute('aria-label') : '', color: btn ? getComputedStyle(btn).color : '', visible: !!(w.offsetWidth || w.offsetHeight) };
    }).slice(0, 6),
    pending_badges: badges.map((b) => ({ aria: b.getAttribute('aria-label') || '', text: (b.textContent || '').trim().slice(0, 60), visible: !!(b.offsetWidth || b.offsetHeight) })).slice(0, 4),
  };
});

if (out.honest_empty) {
  out.branch = 'honest-empty';
  await page.locator('main').getByText('市场热度与趋势研判').first().scrollIntoViewIfNeeded().catch(() => {});
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(outDir, 'scout-p009-heat-empty.png') });
  out.empty_shot = 'scout-p009-heat-empty.png';
} else {
  out.branch = 'series-present';
  await page.screenshot({ path: path.join(outDir, 'scout-p009-heat-rated.png') });
  out.rated_shot = 'scout-p009-heat-rated.png';
}

fs.writeFileSync(path.join(outDir, 'scout-p009-heat.json'), JSON.stringify(out, null, 2));
await browser.close();
console.log(JSON.stringify(out, null, 2));
console.log('probe ok →', outDir);
