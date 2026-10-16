#!/usr/bin/env node
/** P0-14 补探（用后可删）：ECharts option 可读性 + 雷达区块 DOM 结构 + 对比对象元素形态 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

// 直达结果态：最近任务深链（P0-13 已证实指纹复用语义可渲染）
const recent = JSON.parse(fs.readFileSync(path.join(__dirname, 'probe-p014.json'), 'utf8'));
const urlResult = recent.url_result;
await page.goto(urlResult, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);

const out = { surveyed_at: new Date().toISOString(), url: page.url() };
out.has_window_echarts = await page.evaluate(() => typeof window.echarts !== 'undefined' && !!window.echarts.getInstanceByDom);

out.radar_block = await page.evaluate(() => {
  const title = [...document.querySelectorAll('*')].find((e) => e.children.length === 0 && /技术力多维雷达对比/.test(e.textContent || ''));
  if (!title) return { found: false };
  let block = title;
  for (let i = 0; i < 5 && block; i++) {
    block = block.parentElement;
    if (block && block.querySelector('canvas')) break;
  }
  if (!block) return { found: false };
  const chart = block.querySelector('[class*=echarts], [_echarts_instance_]');
  const inner = block.innerText.replace(/\n+/g, ' | ').slice(0, 400);
  let option = null;
  try {
    const inst = window.echarts && window.echarts.getInstanceByDom(chart);
    if (inst) {
      const o = inst.getOption();
      option = {
        indicator_names: (o.radar || []).flatMap((r) => (r.indicator || []).map((i) => i.name)),
        legend: (o.legend || []).flatMap((l) => (l.data || []).map((d) => (d && d.name) || String(d))),
        series_names: (o.series || []).map((s) => s.name),
        series_count: (o.series || []).length,
      };
    }
  } catch (e) { option = { err: String(e).slice(0, 120) }; }
  return { found: true, chart_cls: chart ? String(chart.className) : null, block_text: inner, option };
});

// 对比对象 A 元素形态
out.obj_selector = await page.evaluate(() => {
  const el = [...document.querySelectorAll('*')].find((e) => e.children.length === 0 && /对比对象 A/.test(e.textContent || ''));
  if (!el) return { found: false };
  return { found: true, tag: el.tagName, cls: String(el.className || '').slice(0, 80), parent_cls: String(el.parentElement?.className || '').slice(0, 80) };
});

fs.writeFileSync(path.join(__dirname, 'probe-p014b.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
