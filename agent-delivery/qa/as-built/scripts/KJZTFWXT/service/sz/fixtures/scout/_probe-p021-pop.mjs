// _probe-p021-pop.mjs — 弹层收场诊断：点 trace 按钮后 Esc / goto / reload 哪个能清拦截
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://111.198.38.90:50892';
const ROUTE = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const out = {};

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await ctx.newPage();

await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(800);
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1500);
}
await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);

const popInfo = async () => {
  const pops = page.locator('.arco-trigger-popup, .arco-popover');
  const n = await pops.count();
  let visible = 0; let sample = '';
  for (let i = 0; i < n; i++) {
    const el = pops.nth(i);
    if (await el.isVisible().catch(() => false)) {
      visible++;
      if (!sample) sample = (((await el.innerText().catch(() => '')) || '')).replace(/\s+/g, ' ').slice(0, 80);
    }
  }
  return { total: n, visible: visible, sample: sample };
};

out.before = await popInfo();
const btn = page.locator('button.trace-info-icon[aria-label*="分析配置"]').first();
out.btn_count = await page.locator('button.trace-info-icon[aria-label*="分析配置"]').count();
await btn.click({ timeout: 5000 });
await page.waitForTimeout(1200);
out.after_click = await popInfo();
await page.keyboard.press('Escape').catch(() => {});
await page.waitForTimeout(600);
out.after_esc = await popInfo();
await page.goto(BASE + ROUTE + '&diag=1', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);
out.after_goto = await popInfo();
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2000);
out.after_reload = await popInfo();

// 拦截复核：reload 后 select 能否点
const selOk = await (async () => {
  try {
    await page.locator('.industry-catalog-select').first().click({ timeout: 5000 });
    return 'click-ok';
  } catch (e) {
    return 'blocked: ' + String(e).slice(0, 120);
  }
})();
out.select_click_after_reload = selOk;

fs.writeFileSync(path.join(__dirname, '_probe-p021-pop.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
