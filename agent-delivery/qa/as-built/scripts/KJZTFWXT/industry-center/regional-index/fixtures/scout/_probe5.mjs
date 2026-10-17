#!/usr/bin/env node
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const base = 'http://111.198.38.90:50892/';
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
async function prep(page, waitMs = 5000) {
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(waitMs);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && await close.first().isVisible().catch(() => false)) await close.first().click();
  await page.locator('button.persona-switch').first().click();
  await page.waitForTimeout(400);
  const sw = page.getByRole('switch', { name: '内部评审模式' });
  if (await sw.count() && (await sw.getAttribute('aria-checked')) === 'true') await sw.click();
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
}
const snap = async (page) => page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  const lines = mainText.split('\n').map((t) => t.trim()).filter(Boolean);
  const start = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
  return {
    url: location.href,
    title: document.title,
    summary: lines.find((t) => /已计入|权重合计|未选/.test(t)),
    hint: lines.find((t) => /请选择.*产业|请选择.*区域/.test(t)),
    template: [...document.querySelectorAll('.arco-select-view')].map((el) => (el.innerText || el.getAttribute('title') || '').trim()).find((t) => /综合指数|官方|未保存|模板/.test(t)),
    selects: [...document.querySelectorAll('.arco-select-view')].filter((el) => el.getBoundingClientRect().width > 0).map((el) => ({
      text: (el.innerText || '').trim().slice(0, 60),
      aria: el.getAttribute('aria-label'),
      title: el.getAttribute('title'),
      placeholder: el.querySelector('input')?.placeholder,
      multi: el.className.includes('mult'),
    })),
    metricLines: lines.filter((t) => /营收|技术壁垒|高校论文|人才结构|服务机构|配套生态|商业力|技术力|学术力|支撑力|16|20|权重/.test(t)).slice(0, 35),
    spins: [...document.querySelectorAll('[role=spinbutton]')].map((el) => ({
      value: el.value || el.getAttribute('aria-valuenow'),
      disabled: el.disabled || !!(el.closest('.arco-input-number-disabled')),
    })),
    checks: [...document.querySelectorAll('main .arco-checkbox')].slice(0, 10).map((el) => ({
      checked: el.className.includes('checked'),
      disabled: el.className.includes('disabled'),
    })),
    removeInMain: [...document.querySelectorAll('main button')].filter((b) => (b.innerText || '').trim() === '移除').map((b) => ({
      disabled: b.disabled || b.className.includes('disabled'),
    })),
    start_disabled: start ? start.disabled || start.className.includes('disabled') : null,
    emptyWorkset: /工作集为空/.test(mainText),
    tabs: [...document.querySelectorAll('[role=tab]')].slice(0, 2).map((t) => ({
      text: (t.innerText || '').trim(),
      selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
    })),
    body: mainText.slice(0, 3200),
  };
});

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 })).newPage();
await login(page);

await prep(page, 6000);
dump('scout-base-wait.json', await snap(page));
await page.screenshot({ path: path.join(out, 'page-base-wait.png'), fullPage: true });

// pick 集成电路
await page.locator('.arco-select-view[aria-label="产业"]').click();
await page.waitForTimeout(700);
await page.locator('.arco-trigger-popup').locator('.arco-select-option', { hasText: '集成电路' }).first().click({ force: true });
await page.waitForTimeout(2000);
dump('scout-after-industry.json', await snap(page));
await page.screenshot({ path: path.join(out, 'page-after-industry.png'), fullPage: true });

// template options
const tplView = page.locator('.arco-select-view').filter({ hasText: /综合指数|官方|未保存/ }).first();
if (await tplView.count()) {
  await tplView.click();
  await page.waitForTimeout(700);
  dump('scout-template-options.json', await page.evaluate(() => {
    const popups = [...document.querySelectorAll('.arco-trigger-popup')].filter((el) => el.getBoundingClientRect().height > 0);
    const popup = popups[popups.length - 1];
    return popup ? { text: popup.innerText.slice(0, 1500), options: [...popup.querySelectorAll('.arco-select-option, .arco-select-option-group-title')].map((el) => (el.innerText || '').trim()).filter(Boolean) } : { error: 'no' };
  }));
  const custom = page.locator('.arco-trigger-popup').getByText('当前未保存配置', { exact: true });
  if (await custom.count()) {
    await custom.last().click({ force: true });
    await page.waitForTimeout(1000);
    dump('scout-custom.json', await snap(page));
  } else {
    await page.keyboard.press('Escape');
  }
}

// region reopen after industry
await page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="请选择区域"]') }).or(page.locator('.arco-select-view-multiple')).first().click().catch(async () => {
  // may already have 深圳市 tag
  await page.locator('.arco-select-view-multiple').first().click({ force: true });
});
await page.waitForTimeout(700);
dump('scout-region-options.json', await page.evaluate(() => {
  const popups = [...document.querySelectorAll('.arco-trigger-popup')].filter((el) => el.getBoundingClientRect().height > 0);
  const popup = popups[popups.length - 1];
  return popup ? { text: popup.innerText.slice(0, 1200), options: [...popup.querySelectorAll('.arco-select-option, .arco-checkbox')].map((el) => (el.innerText || '').trim()).filter(Boolean).slice(0, 30) } : { error: 'no' };
}));
await page.keyboard.press('Escape');

// mode multi
await page.getByText('多产业 × 单区域', { exact: true }).first().click();
await page.waitForTimeout(1000);
dump('scout-mode-multi.json', await snap(page));
await page.getByText('单产业 × 多区域', { exact: true }).first().click();
await page.waitForTimeout(600);

// start analysis
const canStart = await page.evaluate(() => {
  const b = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
  return b && !(b.disabled || b.className.includes('disabled'));
});
if (canStart) {
  await page.getByRole('button', { name: '开始分析' }).click();
  await page.waitForTimeout(5000);
  dump('scout-after-start.json', await snap(page));
  await page.screenshot({ path: path.join(out, 'page-after-start.png'), fullPage: true });
}

// records
await prep(page, 4000);
await page.getByRole('tab', { name: '分析记录' }).click();
await page.waitForTimeout(1500);
dump('scout-records.json', await snap(page));
await page.screenshot({ path: path.join(out, 'page-records.png'), fullPage: true });

// review on
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

console.log('ok');
await browser.close();
