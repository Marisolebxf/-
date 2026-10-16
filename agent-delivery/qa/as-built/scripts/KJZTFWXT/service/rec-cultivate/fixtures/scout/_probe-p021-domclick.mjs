#!/usr/bin/env node
/** 短探 5（P0-21 补充）：X4 路径验证——DOM 事件点击（evaluate e.click()）点开第 2/3 枚追溯弹层。
 *  根因（scout-p021-diag）：评审开态常驻 trace-info-popover DOM 层覆盖 2/3 枚按钮，原生 click actionability 拦截 timeout。
 *  本验：每枚 fresh goto 后 e.click() → 弹层文本锚点各自正确（标题词 = 按钮名）。
 *  产出 scout-p021-domclick.json。0 POST 只读。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const out = { probed_at: new Date().toISOString(), purpose: 'P0-21 X4 DOM-event click for 2nd/3rd trace buttons under persistent popover overlay' };
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
const labels = ['培育服务机构推荐分析', '分析配置', '培育模型权重'];
out.per_button_domclick = [];
for (const lb of labels) {
  await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2200);
  const b = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  const entry = { wanted: lb };
  try {
    await b.evaluate((e) => e.click());
    await page.waitForTimeout(1000);
    // 弹层文本锚点：标题词应含按钮名（各自弹层各自锚点）
    const p = page.locator('.trace-info-popover, .arco-trigger-popup, .arco-popover').filter({ hasText: lb }).first();
    const any = page.locator('.trace-info-popover').first();
    entry.domclick_ok = true;
    entry.popup_all_count = await page.locator('.trace-info-popover').count();
    const txt = (await any.count()) && (await any.isVisible().catch(() => false)) ? ((await any.innerText().catch(() => '')) || '').replace(/\s+/g, ' ') : '';
    entry.popup_head = txt.slice(0, 120);
    entry.popup_anchor_match = txt.includes(lb);
  } catch (e) { entry.domclick_ok = false; entry.err = String(e.message).split('\n')[0]; }
  out.per_button_domclick.push(entry);
}
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-domclick.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify(out.per_button_domclick.map((e) => ({ w: e.wanted, ok: e.domclick_ok, anchor: e.popup_anchor_match, head: (e.popup_head || e.err || '').slice(0, 70) })), null, 1));
