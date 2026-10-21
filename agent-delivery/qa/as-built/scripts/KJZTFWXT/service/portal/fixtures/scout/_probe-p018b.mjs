#!/usr/bin/env node
/** 精扫：深链 industry=INB1804（未来空间）空态形态 */
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
const page = await (
  await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  })
).newPage();
const report = { surveyed_at: new Date().toISOString(), case_id: 'P0-18b' };

try {
  await page.goto(new URL('login', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

  await page.goto(new URL('service-portal/overview?industry=INB1804', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
  });
  await page.waitForTimeout(3000);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
  await page.locator('.arco-spin-mask').first().waitFor({ state: 'hidden', timeout: 12000 }).catch(() => {});

  const filter = page.locator('[aria-label="筛选条"], .svc-portal-filter').first();
  const ind = filter.locator('.arco-select-view').nth(0);
  const chain = filter.locator('.arco-select-view').nth(1);
  report.url = page.url();
  report.indText = (await ind.innerText()).trim();
  report.chainDisabled = await chain.evaluate((el) => el.className.includes('disabled'));
  report.chainPh = await chain.locator('input').getAttribute('placeholder');
  report.chainText = (await chain.innerText()).trim();

  await chain.evaluate((el) => el.click());
  await page.waitForTimeout(800);
  const popup = page.locator('.arco-trigger-popup:visible');
  report.popupVisible = await popup.count();
  report.optCount = await popup.locator('.arco-select-option').count();
  report.optLabels = (await popup.locator('.arco-select-option').allTextContents())
    .map((t) => t.trim())
    .slice(0, 10);
  report.emptyDom = (
    await popup.locator('.arco-select-empty, .arco-empty-description, .arco-empty').allTextContents()
  ).map((t) => t.trim());
  report.pageEmptyCopy = (await page.getByText('无相关产业数据').count()) > 0;
  report.pageEmptyish = (await page.getByText(/无相关|暂无.*产业|无数据/).count()) > 0;
  report.popupHtmlSnippet = (await popup.innerHTML().catch(() => '')).replace(/\s+/g, ' ').slice(0, 400);

  await page.screenshot({
    path: path.join(outDir, 'probe-p018b-future-space.png'),
    fullPage: false,
  });
} catch (e) {
  report.error = String(e && e.stack ? e.stack : e);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p018b.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
  await browser.close();
}
