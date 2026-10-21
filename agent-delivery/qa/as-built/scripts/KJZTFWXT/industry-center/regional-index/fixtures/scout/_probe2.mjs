#!/usr/bin/env node
/** 二次无头：补区域/模板/添加指标/选产业/开始分析/分析记录 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const targetPath = '/industry-center/regional?workspace=index&tab=index';
const outDir = __dirname;
const dump = (n, d) => fs.writeFileSync(path.join(outDir, n), JSON.stringify(d, null, 2));

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
    await close.first().click();
    await page.waitForTimeout(400);
  }
}
async function setReview(page, on) {
  await page.locator('button.persona-switch').first().click();
  await page.waitForTimeout(400);
  const sw = page.getByRole('switch', { name: '内部评审模式' });
  if (await sw.count()) {
    const checked = await sw.getAttribute('aria-checked');
    if (on && checked !== 'true') await sw.click();
    if (!on && checked === 'true') await sw.click();
  }
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
}
async function gotoTarget(page) {
  await page.goto(new URL(targetPath.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  if (page.url().includes('/login')) {
    await ensureLogin(page);
    await page.goto(new URL(targetPath.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  }
  await page.waitForTimeout(2800);
  await closeBasket(page);
}
async function openSelectByAriaOrPh(page, { aria, placeholder, hasText }) {
  let loc;
  if (aria) loc = page.locator(`.arco-select-view[aria-label="${aria}"]`).first();
  else if (placeholder) loc = page.locator('.arco-select-view').filter({ has: page.locator(`input[placeholder="${placeholder}"]`) }).first();
  else loc = page.locator('.arco-select-view').filter({ hasText }).first();
  await loc.click({ timeout: 8000 });
  await page.waitForTimeout(700);
  return loc;
}
async function readPopup(page) {
  return page.evaluate(() => {
    const popups = [...document.querySelectorAll('.arco-trigger-popup')].filter((el) => getComputedStyle(el).display !== 'none');
    const popup = popups[popups.length - 1];
    if (!popup) return { error: 'no popup' };
    return {
      text: popup.innerText.slice(0, 1500),
      options: [...popup.querySelectorAll('.arco-select-option, [role=option], .arco-checkbox, .arco-select-option-group-title')].map((el) => (el.innerText || '').trim()).filter(Boolean).slice(0, 50),
    };
  });
}

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 })).newPage();
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await gotoTarget(page);
await setReview(page, false);

// region options (placeholder 请选择区域)
await openSelectByAriaOrPh(page, { placeholder: '请选择区域' });
const regionOpts = await readPopup(page);
dump('scout-region-options.json', regionOpts);
// select 深圳市 if present
const sz = page.locator('.arco-trigger-popup').getByText('深圳市', { exact: true });
if (await sz.count()) {
  await sz.first().click();
  await page.waitForTimeout(500);
}
await page.keyboard.press('Escape');
await page.waitForTimeout(300);

// industry options
await openSelectByAriaOrPh(page, { aria: '产业' });
const industryOpts = await readPopup(page);
dump('scout-industry-options.json', industryOpts);
const firstInd = page.locator('.arco-trigger-popup .arco-select-option, .arco-trigger-popup [role=option]').first();
let pickedIndustry = null;
if (await firstInd.count()) {
  pickedIndustry = (await firstInd.innerText()).trim();
  await firstInd.click();
  await page.waitForTimeout(800);
}

// template options
await openSelectByAriaOrPh(page, { hasText: /区域产业综合指数|区域产业指数官方|当前未保存/ });
const tplOpts = await readPopup(page);
dump('scout-template-options.json', tplOpts);
await page.keyboard.press('Escape');
await page.waitForTimeout(300);

// add metrics from library
await openSelectByAriaOrPh(page, { placeholder: '添加指标' });
const addOpts = await readPopup(page);
dump('scout-add-metric-options.json', addOpts);
// click first few options
const addChoices = page.locator('.arco-trigger-popup .arco-select-option, .arco-trigger-popup [role=option]');
const nAdd = Math.min(await addChoices.count(), 6);
const added = [];
for (let i = 0; i < nAdd; i++) {
  const t = (await addChoices.nth(i).innerText()).trim();
  added.push(t);
  await addChoices.nth(i).click();
  await page.waitForTimeout(500);
  // reopen if closed
  if (i < nAdd - 1) {
    const still = await page.locator('.arco-trigger-popup').filter({ hasText: /营收|技术|论文|人才|服务|配套/ }).count();
    if (!still) {
      await openSelectByAriaOrPh(page, { placeholder: '添加指标' });
    }
  }
}
await page.keyboard.press('Escape');
await page.waitForTimeout(800);

const afterAdd = await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  const lines = mainText.split('\n').map((t) => t.trim()).filter(Boolean);
  return {
    summaryLine: lines.find((t) => /已计入|权重合计|未选/.test(t)),
    metricLines: lines.filter((t) => /营收|技术壁垒|高校论文|人才结构|服务机构|配套生态|商业力|技术力|学术力|支撑力|\d+%|\d+\./.test(t)).slice(0, 40),
    spins: [...document.querySelectorAll('[role=spinbutton]')].map((el) => ({
      value: el.value || el.getAttribute('aria-valuenow'),
      disabled: el.disabled || el.getAttribute('aria-disabled') === 'true' || !!(el.closest('.arco-input-number-disabled')),
    })),
    start_disabled: (() => {
      const b = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
      return b ? b.disabled || b.className.includes('disabled') : null;
    })(),
    remove_states: [...document.querySelectorAll('button')].filter((b) => (b.innerText || '').trim() === '移除').slice(0, 8).map((b) => !(b.disabled || b.className.includes('disabled'))),
    check_states: [...document.querySelectorAll('main .arco-checkbox')].slice(0, 8).map((el) => ({
      checked: el.className.includes('checked') || el.getAttribute('aria-checked') === 'true',
      disabled: el.className.includes('disabled'),
    })),
    body: mainText.slice(0, 2500),
  };
});
dump('scout-after-add.json', { pickedIndustry, added, ...afterAdd });
await page.screenshot({ path: path.join(outDir, 'page-after-add.png'), fullPage: true });

// mode switch
await page.getByText('多产业 × 单区域', { exact: true }).first().click();
await page.waitForTimeout(900);
const multi = await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  return {
    selects: [...document.querySelectorAll('.arco-select-view')].map((el) => ({
      text: (el.innerText || '').trim().slice(0, 80),
      aria: el.getAttribute('aria-label'),
      placeholder: el.querySelector('input')?.placeholder,
      multi: el.className.includes('mult'),
    })),
    hints: mainText.split('\n').map((t) => t.trim()).filter((t) => /请选择|模式|产业|区域/.test(t)).slice(0, 25),
    radios: [...document.querySelectorAll('.arco-radio')].map((el) => ({
      text: (el.innerText || '').trim(),
      checked: !!(el.querySelector('input:checked') || el.className.includes('checked')),
    })),
  };
});
dump('scout-mode-multi.json', multi);
await page.getByText('单产业 × 多区域', { exact: true }).first().click();
await page.waitForTimeout(600);

// if start enabled, click
if (afterAdd.start_disabled === false) {
  await page.getByRole('button', { name: '开始分析' }).click();
  await page.waitForTimeout(5000);
  dump('scout-after-start.json', await page.evaluate(() => ({
    url: location.href,
    body: (document.querySelector('main')?.innerText || '').slice(0, 2500),
  })));
  await page.screenshot({ path: path.join(outDir, 'page-after-start.png'), fullPage: true });
} else {
  // try ensure industry+region+metrics then start
  await gotoTarget(page);
  await setReview(page, false);
  // region
  await openSelectByAriaOrPh(page, { placeholder: '请选择区域' });
  const sz2 = page.locator('.arco-trigger-popup').getByText('深圳市', { exact: true });
  if (await sz2.count()) await sz2.first().click();
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  // industry
  await openSelectByAriaOrPh(page, { aria: '产业' });
  const ind2 = page.locator('.arco-trigger-popup .arco-select-option').first();
  if (await ind2.count()) await ind2.click();
  await page.waitForTimeout(500);
  // add one metric at least
  await openSelectByAriaOrPh(page, { placeholder: '添加指标' });
  const m1 = page.locator('.arco-trigger-popup .arco-select-option').first();
  if (await m1.count()) await m1.click();
  await page.keyboard.press('Escape');
  await page.waitForTimeout(800);
  // maybe need weight sum 100 - click 一键均分
  const avg = page.getByRole('button', { name: '一键均分' });
  if (await avg.count()) await avg.click();
  await page.waitForTimeout(600);
  const gate = await page.evaluate(() => {
    const mainText = document.querySelector('main')?.innerText || '';
    const start = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
    return {
      summary: mainText.split('\n').map((t) => t.trim()).find((t) => /已计入|权重合计|未选/.test(t)),
      start_disabled: start ? start.disabled || start.className.includes('disabled') : null,
      spins: [...document.querySelectorAll('[role=spinbutton]')].map((el) => el.value || el.getAttribute('aria-valuenow')),
      body: mainText.slice(0, 2000),
    };
  });
  dump('scout-gate.json', gate);
  if (gate.start_disabled === false) {
    await page.getByRole('button', { name: '开始分析' }).click();
    await page.waitForTimeout(5000);
    dump('scout-after-start.json', await page.evaluate(() => ({
      url: location.href,
      body: (document.querySelector('main')?.innerText || '').slice(0, 2500),
    })));
    await page.screenshot({ path: path.join(outDir, 'page-after-start.png'), fullPage: true });
  }
}

// records
await gotoTarget(page);
await setReview(page, false);
await page.getByRole('tab', { name: '分析记录' }).click();
await page.waitForTimeout(1500);
dump('scout-records.json', await page.evaluate(() => ({
  url: location.href,
  body: (document.querySelector('main')?.innerText || '').slice(0, 2500),
  tabs: [...document.querySelectorAll('[role=tab]')].map((t) => ({
    text: (t.innerText || '').trim(),
    selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
  })),
})));
await page.screenshot({ path: path.join(outDir, 'page-records.png'), fullPage: true });

// review on traces
await setReview(page, true);
await page.waitForTimeout(500);
dump('scout-review-on.json', await page.evaluate(() => {
  const traces = [...document.querySelectorAll('[aria-label*=需求追溯], .trace-info-icon')].map((el) => el.getAttribute('aria-label') || '');
  const badges = [...document.querySelectorAll('[aria-label*=GAP-], [aria-label*=QC11], .perm-pending-badge, .metric-spec-card')].map((el) => el.getAttribute('aria-label') || '');
  return { traces: [...new Set(traces.filter(Boolean))], badges: [...new Set(badges.filter(Boolean))], count: traces.length };
}));

// custom template unlock: switch to 当前未保存配置 if exists, else adjust after add
await gotoTarget(page);
await setReview(page, false);
await openSelectByAriaOrPh(page, { hasText: /区域产业综合指数|当前未保存/ });
const custom = page.locator('.arco-trigger-popup').getByText('当前未保存配置', { exact: true });
if (await custom.count()) await custom.first().click();
else await page.keyboard.press('Escape');
await page.waitForTimeout(600);
await openSelectByAriaOrPh(page, { placeholder: '添加指标' });
const opts = page.locator('.arco-trigger-popup .arco-select-option');
for (let i = 0; i < Math.min(await opts.count(), 3); i++) {
  await opts.nth(i).click();
  await page.waitForTimeout(400);
  if (!(await page.locator('.arco-trigger-popup .arco-select-option').count())) {
    await openSelectByAriaOrPh(page, { placeholder: '添加指标' });
  }
}
await page.keyboard.press('Escape');
await page.waitForTimeout(500);
dump('scout-custom.json', await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  return {
    summary: mainText.split('\n').map((t) => t.trim()).find((t) => /已计入|权重合计/.test(t)),
    spins: [...document.querySelectorAll('[role=spinbutton]')].map((el) => ({
      value: el.value || el.getAttribute('aria-valuenow'),
      disabled: el.disabled || !!(el.closest('.arco-input-number-disabled')),
    })),
    removeEnabled: [...document.querySelectorAll('button')].filter((b) => (b.innerText || '').trim() === '移除').slice(0, 6).map((b) => !(b.disabled || b.className.includes('disabled'))),
    template: [...document.querySelectorAll('.arco-select-view')].map((el) => (el.innerText || '').trim()).find((t) => /模板|未保存|综合指数/.test(t)),
  };
}));

console.log(JSON.stringify({
  pickedIndustry,
  added,
  start_disabled: afterAdd.start_disabled,
  summary: afterAdd.summaryLine,
  region_opts: regionOpts.options?.slice?.(0, 10),
  industry_opts: industryOpts.options?.slice?.(0, 10),
}, null, 2));
await browser.close();
