#!/usr/bin/env node
/** P0-07 一次性无头实勘（用后可删）：深链回填 2 家 → 数据覆盖与可信度区 + 五档 Tab 探测 */
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

const body1 = await page.locator('body').innerText();
const tabRoles = await page.getByRole('tab').allInnerTexts().catch(() => []);
const tabLike = await page.evaluate(() => {
  const out = [];
  for (const sel of ['.arco-tabs-tab', '[role=tab]']) {
    for (const el of document.querySelectorAll(sel)) out.push(sel + ' :: ' + (el.innerText || '').trim());
  }
  return out;
});

const section = page.getByText('数据覆盖与可信度', { exact: true }).first();
const out = {
  surveyed_at: new Date().toISOString(),
  url: page.url(),
  section_visible: await section.isVisible().catch(() => false),
  coverageTabs_probe: tabLike,
  tab_roles: tabRoles,
  body_hit: {
    section: body1.includes('数据覆盖与可信度'),
    all: body1.includes('全部可信度'),
    high: body1.includes('高可信'),
    mid: body1.includes('中可信'),
    low: body1.includes('低可信'),
    none: body1.includes('不可生成'),
    precheck_fail: body1.includes('预检未返回企业明细'),
  },
  body_snippet: body1.slice(body1.indexOf('数据覆盖与可信度') - 50, body1.indexOf('数据覆盖与可信度') + 260),
  from_basket: await page.getByText(/来自对比篮/).first().isVisible().catch(() => false),
  start_disabled: await page.getByRole('button', { name: '开始分析' }).isDisabled().catch(() => null),
};

await page.screenshot({ path: path.join(__dirname, 'scout-p007.png'), fullPage: true });
fs.writeFileSync(path.join(__dirname, 'scout-p007.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
