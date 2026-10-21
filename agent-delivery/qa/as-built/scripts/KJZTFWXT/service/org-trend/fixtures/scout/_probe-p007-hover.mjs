#!/usr/bin/env node
/**
 * P0-07（FUNC-00661 悬停明细）一次性无头探针。产物落同目录 scout-p007-hover.json；勿当 runner。
 * 目标：确认结果态现状——诚实空（无点可悬）还是已到位（可 hover）；顺带勘 ⓘ 角标渲染态。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const target = `${baseUrl.replace(/\/?$/, '')}/service/institution-judgment?workspace=trend&tab=trend`;
const outDir = __dirname;

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function closeBasket(page) {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(2000);
await closeBasket(page);

const out = { probed_at: new Date().toISOString(), url_entry: page.url() };

// —— 进结果壳（同 P0-06 expect-1 路径）——
const recTab = page.locator('[role=tab][data-tab-key="records"]');
await recTab.waitFor({ state: 'visible', timeout: 12000 });
await recTab.click({ timeout: 8000 });
await page.waitForTimeout(1500);
const viewBtn = page.getByRole('button', { name: '查看结果' }).first();
await viewBtn.waitFor({ state: 'visible', timeout: 12000 });
await viewBtn.click({ timeout: 8000 });
await page.waitForTimeout(2500);
out.url_result = page.url();
const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
out.body_slice = body.slice(0, 1600);
out.honest_empty = /当前结果快照没有年序列/.test(body);

// —— 图表容器 ——
out.chart_containers = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const canvases = [...main.querySelectorAll('canvas')].map((c) => ({ w: c.width, h: c.height, cls: (c.className || '').toString().slice(0, 60) }));
  const echarts = [...main.querySelectorAll('[_echarts_instance_]')].map((el) => ({ tag: el.tagName, w: el.clientWidth, h: el.clientHeight }));
  return { canvas: canvases, echarts_instance: echarts };
});

// —— ⓘ 角标：metric_id / info icon / 演示角标 探测（业务态 DOM，不切评审）——
out.badge_probe_biz = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const hits = [];
  for (const el of main.querySelectorAll('[aria-label], [title], [data-metric-id]')) {
    const a = el.getAttribute('aria-label') || '';
    const t = el.getAttribute('title') || '';
    const m = el.getAttribute('data-metric-id') || '';
    if (/M_SVC_ORG_NEW_COUNT|metric|ⓘ|演示/i.test(`${a} ${t} ${m}`)) {
      hits.push({ tag: el.tagName, aria: a.slice(0, 80), title: t.slice(0, 80), metric: m.slice(0, 60), visible: !!(el.offsetWidth || el.offsetHeight) });
    }
  }
  const infoIcons = [...main.querySelectorAll('.arco-icon-info-circle, .arco-icon-info')].map((el) => ({ visible: !!(el.offsetWidth || el.offsetHeight) }));
  return { metric_hits: hits.slice(0, 10), info_icon_count: infoIcons.length, info_icon_visible: infoIcons.filter((x) => x.visible).length };
});

// —— hover 探测：诚实空则跳过；有 canvas 则悬停中心找 tooltip ——
if (!out.honest_empty && out.chart_containers.canvas.length > 0) {
  const canvas = page.locator('main canvas').first();
  const box = await canvas.boundingBox();
  out.hover_box = box;
  if (box) {
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 8 });
    await page.waitForTimeout(1200);
    out.tooltip_after_hover = await page.evaluate(() => {
      const main = document.querySelector('main') || document.body;
      const cand = [...main.querySelectorAll('div')]
        .filter((d) => {
          const s = getComputedStyle(d);
          return s.position === 'absolute' && (s.pointerEvents === 'none' || +s.zIndex > 0) && (d.innerText || '').trim().length > 0 && !d.querySelector('canvas');
        })
        .map((d) => ({ text: (d.innerText || '').trim().slice(0, 200), cls: (d.className || '').toString().slice(0, 80), visible: !!(d.offsetWidth || d.offsetHeight) }))
        .filter((x) => x.visible);
      return cand.slice(0, 8);
    });
    await page.screenshot({ path: path.join(outDir, 'scout-p007-hover.png') });
    out.hover_shot = 'scout-p007-hover.png';
  }
} else {
  out.hover = out.honest_empty ? 'skipped: honest empty, no point to hover' : 'skipped: no canvas';
  await page.screenshot({ path: path.join(outDir, 'scout-p007-result-empty.png') });
  out.empty_shot = 'scout-p007-result-empty.png';
}

fs.writeFileSync(path.join(outDir, 'scout-p007-hover.json'), JSON.stringify(out, null, 2));
await browser.close();
console.log(JSON.stringify({ honest_empty: out.honest_empty, canvas: (out.chart_containers?.canvas || []).length, tooltip: out.tooltip_after_hover?.length ?? null, badge_biz: out.badge_probe_biz }, null, 2));
console.log('probe ok →', outDir);
