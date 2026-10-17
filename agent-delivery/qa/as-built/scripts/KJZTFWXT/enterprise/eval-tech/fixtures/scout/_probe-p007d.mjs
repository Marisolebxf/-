#!/usr/bin/env node
/** P0-07 四次实勘：打开可信度筛选下拉，枚举选项文本与 DOM；顺带验证切换行为 */
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

// 打开下拉（点可见触发器容器，P7）
const trigger = page.locator('.arco-select-view[aria-label="筛选数据可信度"]');
await trigger.click({ timeout: 8000 });
await page.waitForTimeout(600);
const popup = page.locator('.arco-trigger-popup:visible').last();
const options = await popup.evaluate((el) =>
  [...el.querySelectorAll('.arco-select-option, [role=option], li')].map((o) => ({
    text: (o.innerText || '').trim(),
    cls: String(o.className || '').slice(0, 80),
  }))
);
const popupText = await popup.innerText().catch(() => '');

// 选「高可信」看过滤行为（observed 记录，不进 expect）
let after = null;
try {
  await popup.getByText('高可信', { exact: true }).click();
  await page.waitForTimeout(800);
  const body = await page.locator('body').innerText();
  after = {
    trigger_title: await trigger.getAttribute('title'),
    still_shows_2: body.includes('东莞华为服务有限公司') && body.includes('深圳市小飞鱼移动科技有限公司'),
    current_visible_hit: (body.match(/当前可见 (\d+ \/ \d+) 家/) || [])[1] || null,
  };
} catch (e) {
  after = { error: String(e.message || e).slice(0, 150) };
}

const out = { surveyed_at: new Date().toISOString(), options, popup_text: popupText.slice(0, 300), after };
await page.screenshot({ path: path.join(__dirname, 'scout-p007d.png'), fullPage: false });
fs.writeFileSync(path.join(__dirname, 'scout-p007d.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
