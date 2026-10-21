#!/usr/bin/env node
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const target = baseUrl + 'industry-center/regional?workspace=index&tab=index';
const outDir = __dirname;
const dump = (n, d) => fs.writeFileSync(path.join(outDir, n), JSON.stringify(d, null, 2));

async function login(page) {
  await page.goto(baseUrl + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click(); else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
async function prep(page) {
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(3000);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && await close.first().isVisible().catch(()=>false)) await close.first().click();
  await page.locator('button.persona-switch').first().click();
  await page.waitForTimeout(400);
  const sw = page.getByRole('switch', { name: '内部评审模式' });
  if (await sw.count() && (await sw.getAttribute('aria-checked')) === 'true') await sw.click();
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
}

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 })).newPage();
await login(page);
await prep(page);

const selects = await page.evaluate(() => {
  return [...document.querySelectorAll('.arco-select-view, .arco-select')].map((el, idx) => {
    const input = el.querySelector('input');
    const rect = el.getBoundingClientRect();
    return {
      idx,
      tag: el.tagName,
      class: (el.className || '').toString().slice(0, 160),
      aria: el.getAttribute('aria-label'),
      title: el.getAttribute('title'),
      text: (el.innerText || '').trim().slice(0, 80),
      placeholder: input?.placeholder || null,
      inputClass: input?.className?.slice?.(0, 80) || null,
      multi: (el.className || '').includes('mult'),
      visible: rect.width > 0 && rect.height > 0,
      x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height),
    };
  });
});
dump('scout-select-dump.json', selects);

// click by idx helpers
async function clickSelectIdx(idx) {
  const handle = page.locator('.arco-select-view, .arco-select').nth(idx);
  await handle.click({ timeout: 8000, force: true });
  await page.waitForTimeout(800);
  return page.evaluate(() => {
    const popups = [...document.querySelectorAll('.arco-trigger-popup')].filter((el) => getComputedStyle(el).display !== 'none' && el.getBoundingClientRect().height > 0);
    const popup = popups[popups.length - 1];
    if (!popup) return { error: 'no popup', popupCount: popups.length };
    return {
      text: popup.innerText.slice(0, 1800),
      options: [...popup.querySelectorAll('.arco-select-option, [role=option], .arco-checkbox-label, .arco-checkbox')].map((el) => (el.innerText || '').trim()).filter(Boolean).slice(0, 60),
    };
  });
}

// Find likely region/industry/template/add by dump
const regionIdx = selects.find((s) => s.placeholder === '请选择区域' || (s.multi && /区域/.test(s.aria || '') || /请选择区域/.test(s.placeholder || '')))?.idx
  ?? selects.find((s) => s.multi && s.visible && s.y > 200 && s.y < 500)?.idx;
const industryIdx = selects.find((s) => s.aria === '产业' || s.placeholder === '请选择产业')?.idx;
const templateIdx = selects.find((s) => /综合指数|官方模板|未保存/.test(s.text + (s.title || '')))?.idx;
const addIdx = selects.find((s) => s.placeholder === '添加指标')?.idx;

dump('scout-select-index.json', { regionIdx, industryIdx, templateIdx, addIdx, selects });

if (regionIdx != null) {
  const r = await clickSelectIdx(regionIdx);
  dump('scout-region-options.json', { regionIdx, ...r });
  // try click 深圳市
  const opt = page.locator('.arco-trigger-popup').getByText('深圳市', { exact: true });
  if (await opt.count()) { await opt.last().click(); await page.waitForTimeout(400); }
  await page.keyboard.press('Escape'); await page.waitForTimeout(300);
}

if (industryIdx != null) {
  const r = await clickSelectIdx(industryIdx);
  dump('scout-industry-options.json', { industryIdx, ...r });
  const opt = page.locator('.arco-trigger-popup .arco-select-option').first();
  let picked = null;
  if (await opt.count()) { picked = (await opt.innerText()).trim(); await opt.click(); await page.waitForTimeout(600); }
  dump('scout-industry-picked.json', { picked });
}

if (templateIdx != null) {
  const r = await clickSelectIdx(templateIdx);
  dump('scout-template-options.json', { templateIdx, ...r });
  await page.keyboard.press('Escape'); await page.waitForTimeout(300);
}

if (addIdx != null) {
  const r = await clickSelectIdx(addIdx);
  dump('scout-add-metric-options.json', { addIdx, ...r });
  const opts = page.locator('.arco-trigger-popup .arco-select-option');
  const n = Math.min(await opts.count(), 6);
  const added = [];
  for (let i = 0; i < n; i++) {
    // reopen each time
    if (i > 0) {
      await page.keyboard.press('Escape');
      await page.waitForTimeout(200);
      await clickSelectIdx(addIdx);
    }
    const cur = page.locator('.arco-trigger-popup .arco-select-option');
    if (!(await cur.count())) break;
    const t = (await cur.nth(0).innerText()).trim(); // after previous add, list shrinks; always take first remaining
    added.push(t);
    await cur.nth(0).click();
    await page.waitForTimeout(500);
  }
  await page.keyboard.press('Escape');
  await page.waitForTimeout(800);
  const state = await page.evaluate(() => {
    const mainText = document.querySelector('main')?.innerText || '';
    const lines = mainText.split('\n').map((t) => t.trim()).filter(Boolean);
    const start = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
    return {
      summary: lines.find((t) => /已计入|权重合计|未选/.test(t)),
      metricRows: lines.filter((t) => /营收|技术壁垒|高校论文|人才结构|服务机构|配套生态|商业力|技术力|学术力|支撑力/.test(t)).slice(0, 30),
      spins: [...document.querySelectorAll('[role=spinbutton]')].map((el) => ({
        value: el.value || el.getAttribute('aria-valuenow'),
        disabled: el.disabled || !!(el.closest('.arco-input-number-disabled')),
      })),
      start_disabled: start ? start.disabled || start.className.includes('disabled') : null,
      removeEnabled: [...document.querySelectorAll('button')].filter((b) => (b.innerText || '').trim() === '移除').slice(0, 8).map((b) => !(b.disabled || b.className.includes('disabled'))),
      body: mainText.slice(0, 2800),
    };
  });
  dump('scout-after-add.json', { added, ...state });
  await page.screenshot({ path: path.join(outDir, 'page-after-add.png'), fullPage: true });

  // 一键均分
  const avg = page.getByRole('button', { name: '一键均分' });
  if (await avg.count()) { await avg.click(); await page.waitForTimeout(600); }
  const afterAvg = await page.evaluate(() => {
    const mainText = document.querySelector('main')?.innerText || '';
    const start = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
    return {
      summary: mainText.split('\n').map((t) => t.trim()).find((t) => /已计入|权重合计|未选/.test(t)),
      spins: [...document.querySelectorAll('[role=spinbutton]')].map((el) => el.value || el.getAttribute('aria-valuenow')),
      start_disabled: start ? start.disabled || start.className.includes('disabled') : null,
    };
  });
  dump('scout-after-avg.json', afterAvg);

  if (afterAvg.start_disabled === false) {
    await page.getByRole('button', { name: '开始分析' }).click();
    await page.waitForTimeout(5000);
    dump('scout-after-start.json', await page.evaluate(() => ({
      url: location.href,
      body: (document.querySelector('main')?.innerText || '').slice(0, 2800),
    })));
    await page.screenshot({ path: path.join(outDir, 'page-after-start.png'), fullPage: true });
  }
}

// mode multi
await prep(page);
await page.getByText('多产业 × 单区域', { exact: true }).first().click();
await page.waitForTimeout(900);
dump('scout-mode-multi.json', await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  return {
    selects: [...document.querySelectorAll('.arco-select-view')].map((el) => ({
      text: (el.innerText || '').trim().slice(0, 80),
      aria: el.getAttribute('aria-label'),
      placeholder: el.querySelector('input')?.placeholder,
      multi: el.className.includes('mult'),
    })),
    hints: mainText.split('\n').map((t) => t.trim()).filter((t) => /请选择|模式/.test(t)).slice(0, 20),
    radios: [...document.querySelectorAll('.arco-radio')].map((el) => ({
      text: (el.innerText || '').trim(),
      checked: !!(el.querySelector('input:checked') || el.className.includes('checked')),
    })),
    body: mainText.slice(0, 1800),
  };
}));

// records + review
await prep(page);
await page.getByRole('tab', { name: '分析记录' }).click();
await page.waitForTimeout(1500);
dump('scout-records.json', await page.evaluate(() => ({
  url: location.href,
  body: (document.querySelector('main')?.innerText || '').slice(0, 2500),
})));
await page.screenshot({ path: path.join(outDir, 'page-records.png'), fullPage: true });

await page.locator('button.persona-switch').first().click();
await page.waitForTimeout(400);
const sw2 = page.getByRole('switch', { name: '内部评审模式' });
if (await sw2.count() && (await sw2.getAttribute('aria-checked')) !== 'true') await sw2.click();
await page.keyboard.press('Escape');
await page.waitForTimeout(500);
dump('scout-review-on.json', await page.evaluate(() => {
  const traces = [...document.querySelectorAll('[aria-label*=需求追溯], .trace-info-icon')].map((el) => el.getAttribute('aria-label') || '');
  const badges = [...document.querySelectorAll('[aria-label*=GAP-], [aria-label*=QC11], .perm-pending-badge, .metric-spec-card')].map((el) => el.getAttribute('aria-label') || '');
  return { traces: [...new Set(traces.filter(Boolean))], badges: [...new Set(badges.filter(Boolean))], count: traces.length };
}));

console.log('done', { regionIdx, industryIdx, templateIdx, addIdx });
await browser.close();
