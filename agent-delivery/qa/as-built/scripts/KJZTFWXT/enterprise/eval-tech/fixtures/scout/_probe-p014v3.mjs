#!/usr/bin/env node
/** P0-14 诊断探针 v3（用后可删）：复刻 r3 链路，长轮询观察雷达区块 canvas/文本就绪时序 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
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
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1000);
const closeB = page.locator('button[aria-label="关闭对比篮"]');
if (await closeB.count() && await closeB.first().isVisible().catch(() => false) && await closeB.first().isEnabled().catch(() => false)) {
  try { await closeB.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
}
try {
await page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first().click({ timeout: 8000 });
await page.waitForTimeout(2000);
const sels = page.locator('[aria-label^="选择 "]');
await sels.nth(0).click();
await sels.nth(1).click();
await page.waitForTimeout(500);
const okBtn = page.getByRole('button', { name: '确定' }).first();
await okBtn.scrollIntoViewIfNeeded().catch(() => {});
await okBtn.click({ timeout: 10000 });
} catch (e) {
  const dump = await page.evaluate(() => {
    const btns = [...document.querySelectorAll('button')].filter((b) => /确定/.test(b.textContent || '')).map((b) => { const r = b.getBoundingClientRect(); return { cls: String(b.className).slice(0, 60), x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), visible: r.width > 0 && r.height > 0, inDialog: !!b.closest('[role=dialog], .arco-modal, .arco-drawer') }; });
    const dialog = document.querySelector('[role=dialog], .arco-drawer:scope, .arco-modal');
    return { ok_buttons: btns, dialog_cls: dialog ? String(dialog.className).slice(0, 80) : null, dialog_text_head: dialog ? dialog.innerText.slice(0, 300) : null };
  }).catch(() => null);
  fs.writeFileSync(path.join(__dirname, 'probe-p014v3-overlay-dump.json'), JSON.stringify({ err: String(e).split('\n')[0], dump }, null, 2), 'utf8');
  await page.screenshot({ path: path.join(__dirname, 'probe-v3-overlay-dump.png'), fullPage: true }).catch(() => {});
  throw e;
}
await page.waitForTimeout(2500);
const start = page.getByRole('button', { name: '开始分析' });
await start.click();
let branch = null;
const t0 = Date.now();
while (Date.now() - t0 < 5000) {
  const procEl = page.getByText(/技术力评估生成中|可视化分析过程/).first();
  if (await procEl.isVisible().catch(() => false)) { branch = 'processing'; break; }
  if (/view=result/.test(page.url())) { branch = 'result'; break; }
  await page.waitForTimeout(300);
}
if (branch === 'processing') { const t2 = Date.now(); while (Date.now() - t2 < 30000 && !/view=result/.test(page.url())) await page.waitForTimeout(500); }
const out = { surveyed_at: new Date().toISOString(), branch, url: page.url() };

// 长轮询 40s：每 2s 采样一次雷达区块形态
out.samples = [];
const sample = () => page.evaluate(() => {
  const owner = (word) => [...document.querySelectorAll('*')].find((e) => [...e.childNodes].some((n) => n.nodeType === 3 && new RegExp(word).test(n.textContent || '')));
  const title = owner('技术力多维雷达对比');
  const canvases = document.querySelectorAll('canvas').length;
  if (!title) return { title: false, canvases, blk_head: '' };
  let b = title;
  for (let i = 0; i < 8 && b; i++) { b = b.parentElement; if (b && b.querySelector('canvas')) break; }
  const blk = b ? b.innerText.replace(/\n+/g, ' | ').slice(0, 300) : '';
  return { title: true, canvases, blk_canvas: !!(b && b.querySelector('canvas')), blk_head: blk };
});
for (let i = 0; i < 20; i++) {
  const s = await sample();
  out.samples.push({ t: i * 2, ...s });
  if (s.blk_canvas && /对象 A/.test(s.blk_head || '')) break;
  await page.waitForTimeout(2000);
}
const last = out.samples[out.samples.length - 1];
out.final = last;
await page.screenshot({ path: path.join(__dirname, 'probe-v3-final.png'), fullPage: true });
if (!last.blk_canvas) {
  const body = await page.locator('body').innerText();
  out.body_radar_area = (body.match(/[^\n]*雷达[^\n]*/g) || []).slice(0, 5);
  out.has_obj_a = body.includes('对比对象 A');
}

fs.writeFileSync(path.join(__dirname, 'probe-p014v3.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
