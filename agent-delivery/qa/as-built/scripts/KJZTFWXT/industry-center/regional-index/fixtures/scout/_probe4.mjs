#!/usr/bin/env node
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const base = 'http://10.50.69.111:30892/';
const target = base + 'industry-center/regional?workspace=index&tab=index';
const out = __dirname;
const dump = (n, d) => fs.writeFileSync(path.join(out, n), JSON.stringify(d, null, 2));

async function login(page) {
  await page.goto(base + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
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
  if ((await close.count()) && await close.first().isVisible().catch(() => false)) await close.first().click();
  await page.locator('button.persona-switch').first().click();
  await page.waitForTimeout(400);
  const sw = page.getByRole('switch', { name: '内部评审模式' });
  if (await sw.count() && (await sw.getAttribute('aria-checked')) === 'true') await sw.click();
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
}
async function visiblePopup(page) {
  return page.evaluate(() => {
    const popups = [...document.querySelectorAll('.arco-trigger-popup')].filter((el) => {
      const r = el.getBoundingClientRect();
      return getComputedStyle(el).display !== 'none' && r.width > 0 && r.height > 0;
    });
    const popup = popups[popups.length - 1];
    if (!popup) return null;
    return {
      text: popup.innerText.slice(0, 2000),
      options: [...popup.querySelectorAll('.arco-select-option')].filter((el) => {
        const r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
      }).map((el) => (el.innerText || '').trim()).filter(Boolean),
    };
  });
}

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 })).newPage();
await login(page);
await prep(page);

// pick industry via visible option
await page.locator('.arco-select-view[aria-label="产业"]').click();
await page.waitForTimeout(700);
let indPop = await visiblePopup(page);
dump('scout-industry-options.json', indPop);
if (indPop?.options?.length) {
  await page.locator('.arco-trigger-popup').filter({ hasText: indPop.options[0] }).getByText(indPop.options[0], { exact: true }).last().click({ force: true });
  await page.waitForTimeout(700);
}
dump('scout-after-industry.json', await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  return {
    industry: [...document.querySelectorAll('.arco-select-view[aria-label="产业"]')].map((el) => (el.innerText || el.getAttribute('title') || '').trim()),
    summary: mainText.split('\n').map((t) => t.trim()).find((t) => /已计入|未选/.test(t)),
    hint: mainText.split('\n').map((t) => t.trim()).find((t) => /请选择.*产业/.test(t)),
    start_disabled: (() => {
      const b = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
      return b ? b.disabled || b.className.includes('disabled') : null;
    })(),
  };
}));

// template popup
await page.locator('.arco-select-view').filter({ hasText: /区域产业综合指数/ }).first().click();
await page.waitForTimeout(700);
dump('scout-template-options.json', await visiblePopup(page));
await page.keyboard.press('Escape');
await page.waitForTimeout(300);

// add metrics
const added = [];
for (let i = 0; i < 6; i++) {
  await page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="添加指标"]') }).first().click();
  await page.waitForTimeout(600);
  const pop = await visiblePopup(page);
  if (!pop?.options?.length) { dump('scout-add-metric-options.json', pop); break; }
  if (i === 0) dump('scout-add-metric-options.json', pop);
  const name = pop.options[0];
  added.push(name);
  await page.locator('.arco-trigger-popup').filter({ hasText: name }).locator('.arco-select-option').filter({ hasText: new RegExp('^' + name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')) }).first().click({ force: true });
  await page.waitForTimeout(600);
}
await page.keyboard.press('Escape');
await page.waitForTimeout(800);
const afterAdd = await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  const lines = mainText.split('\n').map((t) => t.trim()).filter(Boolean);
  const start = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
  return {
    summary: lines.find((t) => /已计入|权重合计|未选/.test(t)),
    metricRows: lines.filter((t) => /营收|技术壁垒|高校论文|人才结构|服务机构|配套生态|商业力|技术力|学术力|支撑力|\d+/.test(t)).slice(0, 40),
    spins: [...document.querySelectorAll('[role=spinbutton]')].map((el) => ({
      value: el.value || el.getAttribute('aria-valuenow'),
      disabled: el.disabled || !!(el.closest('.arco-input-number-disabled')),
    })),
    checks: [...document.querySelectorAll('main .arco-checkbox')].slice(0, 10).map((el) => ({
      checked: el.className.includes('checked'),
      disabled: el.className.includes('disabled'),
    })),
    removeEnabled: [...document.querySelectorAll('button')].filter((b) => (b.innerText || '').trim() === '移除' && !(b.closest('[aria-label="对比篮"], [class*=compare]'))).slice(0, 8).map((b) => !(b.disabled || b.className.includes('disabled'))),
    start_disabled: start ? start.disabled || start.className.includes('disabled') : null,
    body: mainText.slice(0, 3000),
  };
});
dump('scout-after-add.json', { added, ...afterAdd });
await page.screenshot({ path: path.join(out, 'page-after-add.png'), fullPage: true });

if (await page.getByRole('button', { name: '一键均分' }).count()) {
  await page.getByRole('button', { name: '一键均分' }).click();
  await page.waitForTimeout(600);
}
dump('scout-after-avg.json', await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  const start = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
  return {
    summary: mainText.split('\n').map((t) => t.trim()).find((t) => /已计入|权重合计|未选/.test(t)),
    spins: [...document.querySelectorAll('[role=spinbutton]')].map((el) => el.value || el.getAttribute('aria-valuenow')),
    start_disabled: start ? start.disabled || start.className.includes('disabled') : null,
  };
}));

// mode
await page.getByText('多产业 × 单区域', { exact: true }).first().click();
await page.waitForTimeout(900);
dump('scout-mode-multi.json', await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  return {
    selects: [...document.querySelectorAll('.arco-select-view')].filter((el) => el.getBoundingClientRect().width > 0).map((el) => ({
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
    body: mainText.slice(0, 1600),
  };
}));
await page.getByText('单产业 × 多区域', { exact: true }).first().click();
await page.waitForTimeout(500);

// records
await prep(page);
await page.getByRole('tab', { name: '分析记录' }).click();
await page.waitForTimeout(1500);
dump('scout-records.json', await page.evaluate(() => ({
  url: location.href,
  body: (document.querySelector('main')?.innerText || '').slice(0, 2500),
  tabs: [...document.querySelectorAll('[role=tab]')].slice(0, 4).map((t) => ({
    text: (t.innerText || '').trim(),
    selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
  })),
})));
await page.screenshot({ path: path.join(out, 'page-records.png'), fullPage: true });

// review on (config tab)
await page.getByRole('tab', { name: '区域产业指数评价' }).click();
await page.waitForTimeout(800);
await page.locator('button.persona-switch').first().click();
await page.waitForTimeout(400);
const sw = page.getByRole('switch', { name: '内部评审模式' });
if (await sw.count() && (await sw.getAttribute('aria-checked')) !== 'true') await sw.click();
await page.keyboard.press('Escape');
await page.waitForTimeout(500);
dump('scout-review-on.json', await page.evaluate(() => {
  const traces = [...document.querySelectorAll('[aria-label*=需求追溯]')].map((el) => el.getAttribute('aria-label') || '');
  const badges = [...document.querySelectorAll('[aria-label*=GAP-], [aria-label*=QC11]')].map((el) => el.getAttribute('aria-label') || '');
  return { traces: [...new Set(traces)], badges: [...new Set(badges)], count: traces.length };
}));

console.log(JSON.stringify({ added, summary: afterAdd.summary, start: afterAdd.start_disabled, spins: afterAdd.spins }, null, 2));
await browser.close();
