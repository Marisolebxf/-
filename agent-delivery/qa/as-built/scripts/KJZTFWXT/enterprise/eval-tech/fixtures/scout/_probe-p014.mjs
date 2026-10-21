#!/usr/bin/env node
/** P0-14 写稿一次性无头实勘（用后可删）：结果态雷达区块 DOM/canvas 形态与图例/维度标签可取性 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://10.50.69.111:30892/';
const DIMS = ['技术人才', '技术创新', '技术转化', '技术合作', '技术投入'];

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
await page.waitForTimeout(1500);

const out = { surveyed_at: new Date().toISOString(), url_initial: page.url() };

// 复用 P0-13 链：关对比篮 → 浮层回填 2 家 → 开始分析 → 三分支
const closeB = page.locator('button[aria-label="关闭对比篮"]');
if (await closeB.count() && await closeB.first().isVisible().catch(() => false) && await closeB.first().isEnabled().catch(() => false)) {
  try { await closeB.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
}
await page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first().click({ timeout: 8000 });
await page.waitForTimeout(800);
const sels = page.locator('[aria-label^="选择 "]');
const n = await sels.count();
if (n < 2) throw new Error('可选企业不足: ' + n);
await sels.nth(0).click();
await sels.nth(1).click();
await page.getByRole('button', { name: '确定' }).click({ timeout: 8000 });
await page.waitForTimeout(2500);
const start = page.getByRole('button', { name: '开始分析' });
out.start_disabled = await start.isDisabled();
if (out.start_disabled) throw new Error('开始分析 disabled（预检复发？ticket=ENV-EVAL-TECH-PRECHECK-001）');
await start.click();
let branch = null;
const t0 = Date.now();
while (Date.now() - t0 < 5000) {
  const procEl = page.getByText(/技术力评估生成中|可视化分析过程/).first();
  if (await procEl.isVisible().catch(() => false)) { branch = 'processing'; break; }
  if (/view=result/.test(page.url())) { branch = 'result'; break; }
  await page.waitForTimeout(300);
}
out.branch5s = branch;
if (branch === 'processing') {
  const t2 = Date.now();
  while (Date.now() - t2 < 30000 && !/view=result/.test(page.url())) await page.waitForTimeout(500);
}
if (!/view=result/.test(page.url())) throw new Error('未达结果态: ' + page.url());
out.url_result = page.url();

// 等图表渲染
await page.waitForTimeout(2500);
await page.screenshot({ path: path.join(__dirname, 'result-radar.png'), fullPage: true });

// 结果区全文（找雷达区块标题 / 维度名 / 企业名 / 模式切换）
const body = await page.locator('body').innerText();
out.body_full = body;
out.hits = {
  radar_word: (body.match(/[^\n]*雷达[^\n]*/g) || []).slice(0, 10),
  dims_in_body: DIMS.filter((d) => body.includes(d)),
  company_lines: [...new Set((body.match(/[^\n]*(公司|集团)[^\n]*/g) || []).map((s) => s.trim()))].slice(0, 15),
  mode_words: (body.match(/[^\n]*(单企|双企|对比模式|对比对象)[^\n]*/g) || []).slice(0, 8),
  obj_count: (body.match(/对象[:：]\s*\d+\s*家/g) || [])[0] || null,
};

// canvas/svg 图表清单（类名 + 尺寸 + 相对位置）
out.charts = await page.evaluate(() => {
  const pick = (sel) => [...document.querySelectorAll(sel)].map((c) => {
    const r = c.getBoundingClientRect();
    let head = '';
    let p = c.parentElement;
    for (let i = 0; i < 4 && p; i++) {
      const t = (p.querySelector('h1,h2,h3,h4,[class*=title],[class*=header]') || {}).textContent || '';
      if (t.trim()) { head = t.trim().slice(0, 40); break; }
      p = p.parentElement;
    }
    return { cls: String(c.className || '').slice(0, 80), w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top), near_title: head };
  }).filter((c) => c.w > 50 && c.h > 50);
  return { canvas: pick('canvas'), svg: pick('svg'), echarts_div: [...document.querySelectorAll('[class*=echarts], [_echarts_instance_]')].map((c) => String(c.className).slice(0, 60)) };
});

fs.writeFileSync(path.join(__dirname, 'probe-p014.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify({ url_result: out.url_result, hits: out.hits, charts: out.charts }, null, 2));
await browser.close();
