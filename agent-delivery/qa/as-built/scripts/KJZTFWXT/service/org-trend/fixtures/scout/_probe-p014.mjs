#!/usr/bin/env node
/**
 * P0-14（FUNC-00669 研判诚实空态）一次性无头探针。产物 scout-p014-honest-empty.json；勿当 runner。
 * 目标：结果壳研判面板是否已能呈现 insufficient / no_activity 两文案，或仍停在 no_series。
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
const target = `${baseUrl.replace(/\/?$/, '')}/service/institution-judgment?workspace=trend&tab=records&view=result&demo_state=result`;
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

const MSG = {
  no_series: '暂无趋势序列，无法给出热度研判',
  insufficient: '数据长度不足，暂不给出热度研判',
  no_activity: '该领域暂无服务供给活动',
};

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
let body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
if (!(/view=result/.test(page.url()) && /服务机构新增数量趋势/.test(body))) {
  await page.goto(`${baseUrl.replace(/\/?$/, '')}/service/institution-judgment?workspace=trend&tab=trend`, {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await ensureLogin(page);
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const recTab = page.locator('[role=tab][data-tab-key="records"]');
  await recTab.waitFor({ state: 'visible', timeout: 12000 });
  await recTab.click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  const viewBtn = page.getByRole('button', { name: '查看结果' }).first();
  await viewBtn.waitFor({ state: 'visible', timeout: 12000 });
  await viewBtn.click({ timeout: 8000 });
  await page.waitForTimeout(2500);
  body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
}

out.url_result = page.url();
out.honest_empty_no_series = /当前结果快照没有年序列/.test(body);
out.legend_btn_count = await page.locator('.svc-org-trend__legend button').count();
out.zero_legend_mark = await page.locator('.svc-org-trend__legend button').filter({ hasText: '无新增' }).count();

out.heat = await page.evaluate((MSG) => {
  const panel = document.querySelector('[data-testid="svc-org-heat-panel"]');
  const txt = panel ? panel.innerText || '' : '';
  const stars = panel
    ? panel.querySelectorAll('.arco-rate, .arco-icon-star-fill, .arco-icon-star').length
    : 0;
  const rating = (panel?.querySelector('.svc-org-heat__rating')?.textContent || '').trim().slice(0, 200);
  return {
    has_panel: !!panel,
    rating_text: rating,
    star_like_count: stars,
    has_no_series: txt.includes(MSG.no_series),
    has_insufficient: txt.includes(MSG.insufficient),
    has_no_activity: txt.includes(MSG.no_activity),
    panel_slice: txt.replace(/\n/g, ' / ').slice(0, 400),
  };
}, MSG);

const shot = path.join(outDir, 'scout-p014-honest-empty.png');
await page.screenshot({ path: shot, fullPage: false });
out.empty_shot = 'scout-p014-honest-empty.png';

out.branch =
  out.heat.has_insufficient || out.heat.has_no_activity
    ? 'construct-scenarios-visible'
    : out.heat.has_no_series || out.honest_empty_no_series
      ? 'no_series-only'
      : out.legend_btn_count > 0
        ? 'series-present-need-sweep'
        : 'unknown';

out.verdict_hint =
  out.branch === 'no_series-only'
    ? 'allow_skip ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD → n/a（insufficient/no_activity 需 hasYearSeries）'
    : out.branch === 'construct-scenarios-visible'
      ? '转实跑：断言两文案 + 无星级'
      : '有图例可扫领域；扫不到两文案则 D4 构造债';

fs.writeFileSync(path.join(outDir, 'scout-p014-honest-empty.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
