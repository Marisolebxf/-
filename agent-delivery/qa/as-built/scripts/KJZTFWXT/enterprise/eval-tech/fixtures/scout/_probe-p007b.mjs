#!/usr/bin/env node
/** P0-07 二次实勘：定位「数据覆盖与可信度」区块容器 + 内部可点击子项结构 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
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
  const title = [...document.querySelectorAll('*')].find(
    (el) => el.children.length === 0 && (el.textContent || '').trim() === '数据覆盖与可信度'
  );
  if (!title) return { found: false };
  // 向上找一个足够大的容器（包含全部可信度文案）
  let box = title.parentElement;
  for (let i = 0; i < 8 && box; i++) {
    if ((box.innerText || '').includes('全部可信度')) break;
    box = box.parentElement;
  }
  if (!box) return { found: true, container: 'none' };
  const clickable = [...box.querySelectorAll('button, [role=tab], [role=button], .arco-btn, [class*=tab], [class*=chip], [class*=segment], [class*=filter]')]
    .slice(0, 40)
    .map((el) => ({
      tag: el.tagName.toLowerCase(),
      text: (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 30),
      cls: String(el.className || '').slice(0, 100),
      aria: el.getAttribute('aria-label') || undefined,
    }));
  return {
    found: true,
    container_cls: String(box.className || '').slice(0, 120),
    container_tag: box.tagName.toLowerCase(),
    clickable,
    box_text: (box.innerText || '').slice(0, 500),
  };
});

fs.writeFileSync(path.join(__dirname, 'scout-p007b.json'), JSON.stringify(struct, null, 2), 'utf8');
console.log(JSON.stringify(struct, null, 2));
await browser.close();
