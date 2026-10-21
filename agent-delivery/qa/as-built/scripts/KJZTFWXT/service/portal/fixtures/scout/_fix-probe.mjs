#!/usr/bin/env node
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://10.50.69.111:30892/';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const btn = page.getByRole('button', { name: /登录/ });
if (await btn.count()) await btn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

await page.goto(base + 'service-portal/overview', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2000);
const close = page.locator('button[aria-label="关闭对比篮"]');
if (await close.count()) {
  try {
    await close.click({ timeout: 1500 });
  } catch {}
}

await page.getByRole('tab', { name: '服务机构区域分布', exact: true }).click();
await page.waitForTimeout(2000);

const dumpHeadings = async () => {
  const els = await page.locator('h1,h2,h3,h4').evaluateAll((nodes) =>
    nodes.map((e) => ({
      tag: e.tagName,
      text: (e.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 80),
      inMain: !!e.closest('main'),
      role: e.getAttribute('role') || '',
    })),
  );
  return els.filter((h) => h.text);
};

const out = {
  url: page.url(),
  regionHeadingCount: await page.getByRole('heading', { name: '服务机构区域分布' }).count(),
  regionMainFirst: await page.locator('main').getByRole('heading', { name: '服务机构区域分布', exact: true }).count(),
  rankAsHeading: await page.getByRole('heading', { name: /省级行政区排行/ }).count(),
  rankAsText: await page.getByText(/省级行政区排行/).count(),
  guangdong: await page.getByText(/广东/).count(),
  views: {
    global: await page.getByText('全球视图', { exact: true }).count(),
    china: await page.getByText('全国视图', { exact: true }).count(),
  },
  headings: await dumpHeadings(),
};

// 点全国视图
const china = page.getByText('全国视图', { exact: true }).first();
if (await china.count()) {
  await china.click();
  await page.waitForTimeout(1500);
}
out.afterChina = {
  url: page.url(),
  rankAsHeading: await page.getByRole('heading', { name: /省级行政区排行/ }).count(),
  rankAsText: await page.getByText(/省级行政区排行/).count(),
  guangdong: await page.getByText(/广东/).count(),
  headings: await dumpHeadings(),
  mainTextSample: (await page.locator('main').innerText()).split('\n').map((t) => t.trim()).filter(Boolean).slice(0, 40),
};

console.log(JSON.stringify(out, null, 2));
await browser.close();
