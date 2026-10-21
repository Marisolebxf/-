#!/usr/bin/env node
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const target = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(600);
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
await page.goto(target, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);
const close = page.locator('[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false))) await close.first().click();
const panel = page.locator('.ent-section-panel', { hasText: '技术力评价模型' }).first();
const cbs = panel.locator('.arco-checkbox');
for (let i = 4; i >= 1; i--) {
  const cls = String((await cbs.nth(i).getAttribute('class')) || '');
  if (/arco-checkbox-checked/.test(cls)) {
    await cbs.nth(i).click();
    await page.waitForTimeout(400);
  }
}
await page.waitForTimeout(500);
const info = await page.evaluate(() => {
  const nodes = [...document.querySelectorAll('*')].filter((e) => {
    const t = e.childNodes.length
      ? [...e.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent || '').join('')
      : '';
    return (e.textContent || '').includes('至少启用');
  });
  return nodes.slice(0, 20).map((e) => ({
    tag: e.tagName,
    cls: String(e.className).slice(0, 80),
    ownText: [...e.childNodes]
      .filter((n) => n.nodeType === 3)
      .map((n) => n.textContent || '')
      .join('')
      .trim()
      .slice(0, 80),
    text: (e.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120),
    childN: e.children.length,
    display: getComputedStyle(e).display,
    visibility: getComputedStyle(e).visibility,
    opacity: getComputedStyle(e).opacity,
  }));
});
const loc1 = page.getByText('至少启用 2 个评价维度', { exact: true });
const loc2 = page.getByText(/至少启用\s*2\s*个评价维度/);
const loc3 = page.locator('text=至少启用 2 个评价维度');
const out = {
  nodes: info,
  exact: { count: await loc1.count(), vis: await loc1.first().isVisible().catch(() => null) },
  regex: { count: await loc2.count(), vis: await loc2.first().isVisible().catch(() => null) },
  textSel: { count: await loc3.count(), vis: await loc3.first().isVisible().catch(() => null) },
  mainHas: ((await page.locator('.svc-org-analysis-main').innerText().catch(() => '')) || '').includes('至少启用 2'),
  bodyHas: ((await page.locator('body').innerText().catch(() => '')) || '').includes('至少启用 2'),
};
fs.writeFileSync(path.join(__dirname, 'scout-p013-tip.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
