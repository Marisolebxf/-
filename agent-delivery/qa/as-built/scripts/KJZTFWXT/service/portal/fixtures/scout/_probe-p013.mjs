#!/usr/bin/env node
/** 一次性探针 P0-13（FUNC-01320 机构详情抽屉四板块）：深圳重点机构墙/卡片/抽屉。产物 probe-p013.json + 截图 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const outDir = __dirname;

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
})).newPage();
const report = { surveyed_at: new Date().toISOString(), case_id: 'P0-13', func_id: 'FUNC-01320' };
try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

  const apiPromise = page.waitForResponse(
    (r) => /key-orgs|key_orgs|keyorg/i.test(r.url()) && r.request().method() !== 'OPTIONS',
    { timeout: 20000 },
  ).catch(() => null);

  await page.goto(new URL('service-portal/shenzhen', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2800);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }

  report.url = page.url();
  report.tab_selected = await page.getByRole('tab', { name: '深圳产业服务介绍', exact: true }).getAttribute('aria-selected').catch(() => null);
  report.keyorg_heading = await page.getByRole('heading', { name: /重点产业服务机构/ }).count();
  report.empty_copy = await page.getByText(/暂无重点机构/).allTextContents().then((a) => a.slice(0, 8)).catch(() => []);
  report.empty_visible = (await page.getByText(/暂无重点机构/).count()) > 0;

  const cardSels = [
    '.svc-portal-keyorg-card',
    '[class*=keyorg-card]',
    '[class*=key-org-card]',
    'main .svc-portal-keyorg button',
    'main .svc-portal-keyorg [role=button]',
  ];
  report.card_counts = {};
  for (const s of cardSels) report.card_counts[s] = await page.locator(s).count();
  report.card_count = report.card_counts['.svc-portal-keyorg-card'] || 0;
  report.has_cards = report.card_count > 0;

  if (report.has_cards) {
    const card = page.locator('.svc-portal-keyorg-card').first();
    report.first_card_text = ((await card.innerText().catch(() => '')) || '').slice(0, 120);
    await card.click({ timeout: 8000 }).catch((e) => { report.click_err = String(e && e.message); });
    await page.waitForTimeout(1200);
    const drawer = page.locator('.arco-drawer').first();
    report.drawer_visible = await drawer.isVisible().catch(() => false);
    report.drawer_testid = await page.locator('[data-testid="svc-portal-keyorg-drawer"]').count();
    if (report.drawer_visible) {
      const dtxt = (await drawer.innerText().catch(() => '')) || '';
      report.drawer_head = dtxt.slice(0, 240).replace(/\n/g, ' | ');
      report.blocks = {
        overview: /机构概况/.test(dtxt),
        scale: /当前规模/.test(dtxt),
        field: /业务服务领域/.test(dtxt),
        region: /业务分布区域/.test(dtxt),
      };
      report.block_order_ok =
        dtxt.indexOf('机构概况') < dtxt.indexOf('当前规模') &&
        dtxt.indexOf('当前规模') < dtxt.indexOf('业务服务领域') &&
        dtxt.indexOf('业务服务领域') < dtxt.indexOf('业务分布区域');
    }
  }

  const api = await apiPromise;
  if (api) {
    report.api = { url: api.url(), status: api.status() };
    try {
      const body = await api.json();
      const d = body && body.data !== undefined ? body.data : body;
      report.api_empty = !!(d && (d.empty === true || (Array.isArray(d.items) && d.items.length === 0)));
      report.api_items_len = d && Array.isArray(d.items) ? d.items.length : null;
      report.api_section = d && d.section;
    } catch (e) {
      report.api_parse_err = String(e && e.message);
    }
  }

  await page.screenshot({ path: path.join(outDir, 'probe-p013.png'), fullPage: false });
  report.screenshot = 'fixtures/scout/probe-p013.png';
  report.verdict_hint = report.has_cards
    ? 'cards_present — can assert drawer four blocks'
    : 'key_org_wall_honest_empty — allow_skip ENV-SVC-PORTAL-KEY-ORG-EMPTY';
} catch (e) {
  report.error = String(e && e.stack ? e.stack : e);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p013.json'), JSON.stringify(report, null, 2));
  await browser.close();
  console.log(JSON.stringify(report, null, 2));
}
