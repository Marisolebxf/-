#!/usr/bin/env node
/** P0-07 三次实勘：取「全部可信度」元素 outerHTML + 同级结构，确认五档 DOM 形态 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://10.50.69.111:30892/';
const target =
  "enterprise/evaluation?workspace=technology&mode=technology&enterprise_codes[]=0a2b82208071ce5a0e3bd562b80e263b&enterprise_codes[]=12ceab1a61c7d1e1e5cb61b78dd8f3aa&source=compare-basket";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

await page.goto(base + target, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);
const close = page.locator('button[aria-label="关闭对比篮"]');
if (await close.count()) {
  try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(400); } catch {}
}

const struct = await page.evaluate(() => {
  const hits = [...document.querySelectorAll('*')].filter(
    (el) => (el.textContent || '').trim() === '全部可信度' && el.children.length === 0
  );
  if (!hits.length) return { found: false };
  const el = hits[0];
  // 父层与祖父层的 outerHTML
  const p = el.parentElement;
  const gp = p ? p.parentElement : null;
  return {
    found: true,
    self: { tag: el.tagName.toLowerCase(), cls: String(el.className || ''), outer: el.outerHTML.slice(0, 300) },
    parent: p ? { tag: p.tagName.toLowerCase(), cls: String(p.className || ''), outer: p.outerHTML.slice(0, 800) } : null,
    grandparent: gp ? { tag: gp.tagName.toLowerCase(), cls: String(gp.className || '') } : null,
    sibling_texts: p ? [...p.children].map((c) => (c.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 40)) : [],
  };
});

fs.writeFileSync(path.join(__dirname, 'scout-p007c.json'), JSON.stringify(struct, null, 2), 'utf8');
console.log(JSON.stringify(struct, null, 2));
await browser.close();
