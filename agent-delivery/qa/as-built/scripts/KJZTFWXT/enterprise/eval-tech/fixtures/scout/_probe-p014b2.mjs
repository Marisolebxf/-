#!/usr/bin/env node
/** P0-14 补探 v2（用后可删）：深链渲染等待 + 失败现场 dump + ECharts option 再试 */
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

const recent = JSON.parse(fs.readFileSync(path.join(__dirname, 'probe-p014.json'), 'utf8'));
await page.goto(recent.url_result, { waitUntil: 'domcontentloaded' });

const out = { surveyed_at: new Date().toISOString(), url: page.url() };
// 等雷达标题最长 20s
let titleVisible = false;
const t0 = Date.now();
while (Date.now() - t0 < 20000) {
  if (await page.getByText('技术力多维雷达对比').first().isVisible().catch(() => false)) { titleVisible = true; break; }
  await page.waitForTimeout(500);
}
out.title_visible = titleVisible;
out.wait_ms = Date.now() - t0;
if (!titleVisible) {
  const body = await page.locator('body').innerText().catch(() => '');
  out.body_head = body.slice(0, 600);
  out.url_now = page.url();
  await page.screenshot({ path: path.join(__dirname, 'probe-b2-fail.png'), fullPage: true });
} else {
  await page.waitForTimeout(2000); // 图表渲染缓冲
  out.radar_block = await page.evaluate(() => {
    const title = [...document.querySelectorAll('*')].find((e) => e.children.length === 0 && /技术力多维雷达对比/.test(e.textContent || ''));
    if (!title) return { found: false };
    let block = title;
    for (let i = 0; i < 6 && block; i++) {
      block = block.parentElement;
      if (block && block.querySelector('canvas')) break;
    }
    if (!block) return { found: false, reason: 'no canvas ancestor' };
    const chart = block.querySelector('[class*=echarts], [_echarts_instance_]');
    let option = null;
    try {
      if (window.echarts && window.echarts.getInstanceByDom) {
        const inst = window.echarts.getInstanceByDom(chart);
        if (inst) {
          const o = inst.getOption();
          option = {
            indicator_names: (o.radar || []).flatMap((r) => (r.indicator || []).map((i) => i.name)),
            legend: (o.legend || []).flatMap((l) => (l.data || []).map((d) => (d && d.name) || String(d))),
            series_count: (o.series || []).length,
          };
        } else option = { err: 'getInstanceByDom null（生产构建未暴露 window.echarts）' };
      } else option = { err: 'window.echarts 未暴露（生产构建常态）' };
    } catch (e) { option = { err: String(e).slice(0, 120) }; }
    return {
      found: true,
      chart_cls: chart ? String(chart.className) : null,
      has_canvas: !!block.querySelector('canvas'),
      block_text: block.innerText.replace(/\n+/g, ' | ').slice(0, 500),
      option,
    };
  });
  // 图例/维度文本是否以 DOM 文本存在于雷达区块内（X3 代理）
  out.block_dom_dims = await page.evaluate(() => {
    const els = [...document.querySelectorAll('*')].filter((e) => e.children.length === 0);
    const names = ['技术人才', '技术创新', '技术转化', '技术合作', '技术投入', '对比对象 A', '对象 B'];
    const hits = {};
    for (const nm of names) {
      const hit = els.find((e) => new RegExp('^' + nm + '$').test((e.textContent || '').trim()));
      if (hit) hits[nm] = { tag: hit.tagName, cls: String(hit.className || '').slice(0, 60) };
    }
    return hits;
  });
  await page.screenshot({ path: path.join(__dirname, 'probe-b2-ok.png'), fullPage: true });
}

fs.writeFileSync(path.join(__dirname, 'probe-p014b2.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
