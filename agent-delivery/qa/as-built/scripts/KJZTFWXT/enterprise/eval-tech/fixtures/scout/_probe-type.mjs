#!/usr/bin/env node
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
await page.getByRole('button', { name: /登录/ }).first().click();
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', {
  waitUntil: 'domcontentloaded',
});
await page.waitForTimeout(1200);
const close = page.locator('button[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
  try {
    await close.first().click({ timeout: 1500 });
  } catch {}
}
await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
await page.waitForTimeout(1000);

const out = await page.evaluate(() => {
  const hay = document.body.innerText;
  const selects = [...document.querySelectorAll('.arco-select-view, input[placeholder], [placeholder]')]
    .map((el) => ({
      text: (el.innerText || '').trim().slice(0, 80),
      ph: el.getAttribute('placeholder') || '',
      aria: el.getAttribute('aria-label') || '',
      class: (el.className || '').toString().slice(0, 100),
      vis: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length),
    }))
    .filter((s) => /类型|企业|select/i.test(s.text + s.ph + s.class));
  return {
    hasType: /企业类型/.test(hay),
    hasAllType: /全部企业类型/.test(hay),
    lines: hay
      .split('\n')
      .map((t) => t.trim())
      .filter((t) => /类型|筛选|搜索|选择分析/.test(t))
      .slice(0, 30),
    selects: selects.slice(0, 25),
  };
});

console.log(JSON.stringify(out, null, 2));
await browser.close();
