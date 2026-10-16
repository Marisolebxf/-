#!/usr/bin/env node
/** 短探 4（P0-21 补充）：诊断「分析配置」「培育模型权重」两枚按钮 fresh 页面直点仍 timeout 的根因。
 *  假设：A. 按钮 offscreen（需 scrollIntoView）/ B. persona 菜单开着遮挡 / C. 元素被其他浮层覆盖 / D. 按钮本身 pointer-events 或 disabled 态。
 *  产出 scout-p021-diag.json。0 POST 只读。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const out = { probed_at: new Date().toISOString(), purpose: 'P0-21 diag why 2nd/3rd trace buttons timeout' };
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2400);
const close = page.locator('button[aria-label="关闭对比篮"]');
if ((await close.count()) && (await close.first().isVisible().catch(() => false))) { try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
const diag = async (lb) => {
  const b = page.locator('button.trace-info-icon[aria-label^="' + lb + '"]').first();
  const d = { wanted: lb };
  d.count = await b.count();
  if (!d.count) return d;
  d.visible = await b.isVisible().catch(() => false);
  d.enabled = await b.isEnabled().catch(() => false);
  const box = await b.boundingBox().catch(() => null);
  d.bbox = box ? { x: Math.round(box.x), y: Math.round(box.y), w: Math.round(box.width), h: Math.round(box.height) } : null;
  if (box) d.in_viewport = box.y >= 0 && box.y + box.height <= 1080 && box.x >= 0 && box.x + box.width <= 1920;
  // 元素中心点 elementFromPoint 命中检测
  if (box) {
    const cx = box.x + box.width / 2, cy = box.y + box.height / 2;
    d.hit_test = await page.evaluate(([x, y]) => {
      const el = document.elementFromPoint(x, y);
      if (!el) return null;
      const btn = el.closest('button');
      return { tag: el.tagName.toLowerCase(), cls: String(el.className).slice(0, 60), btn_aria: btn ? (btn.getAttribute('aria-label') || '').slice(0, 40) : null };
    }, [cx, cy]);
  }
  // scrollIntoViewIfNeeded 后再试点
  try {
    await b.scrollIntoViewIfNeeded({ timeout: 2000 });
    await page.waitForTimeout(300);
    d.after_scroll_in_viewport = true;
    await b.click({ timeout: 4000 });
    await page.waitForTimeout(800);
    const p = page.locator('.arco-trigger-popup:visible, .arco-popover:visible').first();
    d.click_after_scroll_ok = true;
    d.popup = (await p.count()) && (await p.isVisible().catch(() => false)) ? (((await p.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 160)) : null;
  } catch (e) { d.click_after_scroll_err = String(e.message).split('\n')[0]; }
  return d;
};
out.diag_1st = await diag('培育服务机构推荐分析');
// 弹层可能仍开着，先 goto 重置再诊断第 2 枚
await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2400);
out.diag_2nd = await diag('分析配置');
await page.goto(baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2400);
out.diag_3rd = await diag('培育模型权重');
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p021-diag.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify(out, null, 1));
