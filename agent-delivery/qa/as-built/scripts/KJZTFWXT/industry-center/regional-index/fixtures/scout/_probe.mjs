#!/usr/bin/env node
/**
 * 一次性无头二次探针：区域产业指数评价。产物落同目录；勿当 runner。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const targetPath = '/industry-center/regional?workspace=index&tab=index';
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

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await gotoTarget(page);

const dump = async (name, data) => {
  fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2));
};

const base = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const radios = [...document.querySelectorAll('.arco-radio, label.arco-radio')].map((el) => ({
    text: (el.innerText || '').trim().slice(0, 80),
    checked: !!(el.querySelector('input:checked') || el.className.includes('checked')),
  })).filter((x) => x.text);
  const allTextSnips = (main.innerText || '').split('\n').map((t) => t.trim()).filter(Boolean);
  const summaryLine = allTextSnips.find((t) => /已计入|权重合计|未选产业/.test(t));
  const buttons = [...document.querySelectorAll('button')].map((b) => ({
    text: (b.innerText || b.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 80),
    disabled: b.disabled || b.className.includes('disabled'),
  })).filter((b) => /开始分析|重置参数|一键均分|保存为个人模板|查看|移除|添加/.test(b.text));
  const metricLines = allTextSnips.filter((t) => /营收|技术壁垒|高校论文|人才结构|服务机构|配套生态|商业力|技术力|学术力|支撑力/.test(t)).slice(0, 40);
  const spins = [...document.querySelectorAll('[role=spinbutton]')].map((el) => ({
    value: el.value || el.getAttribute('value') || el.getAttribute('aria-valuenow'),
    disabled: el.disabled || el.getAttribute('aria-disabled') === 'true' || !!(el.closest('.arco-input-number-disabled')),
  }));
  const tabs = [...document.querySelectorAll('[role=tab]')].map((t) => ({
    text: (t.innerText || '').trim(),
    selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
  }));
  const selectViews = [...document.querySelectorAll('.arco-select-view')].map((el) => ({
    text: (el.innerText || '').trim().slice(0, 80),
    aria: el.getAttribute('aria-label'),
    title: el.getAttribute('title'),
    placeholder: el.querySelector('input')?.placeholder,
    multi: el.className.includes('mult'),
  }));
  return {
    url: location.href,
    title: document.title,
    body_snip: main.innerText.slice(0, 2800),
    radios,
    summaryLine,
    buttons,
    metricLines,
    spins,
    tabs,
    selectViews,
    review_trace_count: document.querySelectorAll('[aria-label*=需求追溯], .trace-info-icon').length,
    gap_badge: !!document.querySelector('[aria-label*=GAP-CHAIN-REG-METRICS]'),
    qc11_badge: !!document.querySelector('[aria-label*=QC11]'),
  };
});
await dump('scout-deep.json', base);
await page.screenshot({ path: path.join(outDir, 'page-deep.png'), fullPage: true });

await setReview(page, false);
await page.waitForTimeout(600);
const reviewOff = await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  const bodyText = document.body.innerText || '';
  return {
    url: location.href,
    review_trace_count: document.querySelectorAll('[aria-label*=需求追溯], .trace-info-icon').length,
    gap_leak: /GAP-|QC11|包内 REQ|DEC-CHAIN|AC-US-/.test(mainText),
    body_has_trace_words: /需求追溯|metric_id|GAP-/.test(mainText),
    summaryLine: mainText.split('\n').map((t) => t.trim()).find((t) => /已计入|权重合计|未选产业/.test(t)),
    hint: mainText.split('\n').map((t) => t.trim()).find((t) => /请选择.*产业/.test(t)),
    start_disabled: (() => {
      const b = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
      return b ? b.disabled || b.className.includes('disabled') : null;
    })(),
    reset_exists: [...document.querySelectorAll('button')].some((x) => (x.innerText || '').includes('重置参数')),
    spins: [...document.querySelectorAll('[role=spinbutton]')].map((el) => ({
      value: el.value || el.getAttribute('aria-valuenow'),
      disabled: el.disabled || el.getAttribute('aria-disabled') === 'true' || !!(el.closest('.arco-input-number-disabled')),
    })),
    remove_disabled: [...document.querySelectorAll('button')].filter((b) => (b.innerText || '').trim() === '移除').map((b) => b.disabled || b.className.includes('disabled')),
  };
});
await dump('scout-review-off.json', reviewOff);
await page.screenshot({ path: path.join(outDir, 'page-review-off.png'), fullPage: true });

// industry options
const industryView = page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="请选择产业"]') }).first();
await industryView.click({ timeout: 8000 });
await page.waitForTimeout(800);
const industryOpts = await page.evaluate(() => {
  const popups = [...document.querySelectorAll('.arco-trigger-popup')].filter((el) => getComputedStyle(el).display !== 'none');
  const popup = popups[popups.length - 1];
  if (!popup) return { error: 'no popup' };
  return {
    options: [...popup.querySelectorAll('.arco-select-option, [role=option]')].map((el) => (el.innerText || '').trim()).filter(Boolean).slice(0, 40),
    text: popup.innerText.slice(0, 1000),
  };
});
await dump('scout-industry-options.json', industryOpts);
await page.keyboard.press('Escape');
await page.waitForTimeout(300);

// region options
const regionView = page.locator('.arco-select-view').filter({ hasText: '深圳市' }).first();
await regionView.click({ timeout: 8000 });
await page.waitForTimeout(800);
const regionOpts = await page.evaluate(() => {
  const popups = [...document.querySelectorAll('.arco-trigger-popup')].filter((el) => getComputedStyle(el).display !== 'none');
  const popup = popups[popups.length - 1];
  if (!popup) return { error: 'no popup' };
  return {
    options: [...popup.querySelectorAll('.arco-select-option, [role=option], .arco-checkbox')].map((el) => (el.innerText || '').trim()).filter(Boolean).slice(0, 40),
    text: popup.innerText.slice(0, 1000),
  };
});
await dump('scout-region-options.json', regionOpts);
await page.keyboard.press('Escape');
await page.waitForTimeout(300);

// switch mode
const multi = page.getByText('多产业 × 单区域', { exact: true });
if (await multi.count()) {
  await multi.first().click();
  await page.waitForTimeout(1000);
  const afterMulti = await page.evaluate(() => {
    const mainText = document.querySelector('main')?.innerText || '';
    return {
      selects: [...document.querySelectorAll('.arco-select-view')].map((el) => ({
        text: (el.innerText || '').trim().slice(0, 80),
        aria: el.getAttribute('aria-label'),
        placeholder: el.querySelector('input')?.placeholder,
        multi: el.className.includes('mult'),
      })),
      hints: mainText.split('\n').map((t) => t.trim()).filter((t) => /请选择|模式/.test(t)).slice(0, 20),
      body: mainText.slice(0, 1800),
      radios: [...document.querySelectorAll('.arco-radio')].map((el) => ({
        text: (el.innerText || '').trim(),
        checked: !!(el.querySelector('input:checked') || el.className.includes('checked')),
      })),
    };
  });
  await dump('scout-mode-multi.json', afterMulti);
  await page.getByText('单产业 × 多区域', { exact: true }).first().click();
  await page.waitForTimeout(600);
}

// template options + custom
const tpl = page.locator('.arco-select-view').filter({ hasText: /区域产业指数官方模板|当前未保存配置/ }).first();
await tpl.click({ timeout: 8000 });
await page.waitForTimeout(600);
const tplOpts = await page.evaluate(() => {
  const popups = [...document.querySelectorAll('.arco-trigger-popup')].filter((el) => getComputedStyle(el).display !== 'none');
  const popup = popups[popups.length - 1];
  return popup
    ? {
        text: popup.innerText.slice(0, 1200),
        options: [...popup.querySelectorAll('.arco-select-option, [role=option], .arco-select-option-group-title')].map((el) => (el.innerText || '').trim()).filter(Boolean),
      }
    : { error: 'no popup' };
});
await dump('scout-template-options.json', tplOpts);
const customOpt = page.locator('.arco-trigger-popup').getByText('当前未保存配置', { exact: true });
if (await customOpt.count()) await customOpt.first().click();
else {
  const alt = page.locator('.arco-trigger-popup').getByText(/当前未保存配置|当次自定义/);
  if (await alt.count()) await alt.last().click();
}
await page.waitForTimeout(1000);
const customState = await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  return {
    spins: [...document.querySelectorAll('[role=spinbutton]')].map((el) => ({
      value: el.value || el.getAttribute('aria-valuenow'),
      disabled: el.disabled || el.getAttribute('aria-disabled') === 'true' || !!(el.closest('.arco-input-number-disabled')),
    })),
    removeEnabled: [...document.querySelectorAll('button')].filter((b) => (b.innerText || '').trim() === '移除').map((b) => !(b.disabled || b.className.includes('disabled'))),
    checkDisabled: [...document.querySelectorAll('.arco-checkbox')].slice(0, 8).map((el) => el.className.includes('disabled')),
    summaryLine: mainText.split('\n').map((t) => t.trim()).find((t) => /已计入|权重合计/.test(t)),
    templateView: [...document.querySelectorAll('.arco-select-view')].map((el) => (el.innerText || '').trim()).find((t) => /模板|未保存|自定义/.test(t)),
  };
});
await dump('scout-custom.json', customState);
await page.screenshot({ path: path.join(outDir, 'page-custom.png'), fullPage: true });

// pick industry on fresh page
await gotoTarget(page);
await setReview(page, false);
const ind = page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="请选择产业"]') }).first();
await ind.click();
await page.waitForTimeout(700);
const opt = page.locator('.arco-trigger-popup .arco-select-option, .arco-trigger-popup [role=option]').filter({ hasNotText: /^\s*$/ }).first();
let picked = null;
if (await opt.count()) {
  picked = (await opt.innerText()).trim();
  await opt.click();
  await page.waitForTimeout(1200);
}
const afterPick = await page.evaluate(() => {
  const mainText = document.querySelector('main')?.innerText || '';
  const start = [...document.querySelectorAll('button')].find((x) => (x.innerText || '').includes('开始分析'));
  return {
    summaryLine: mainText.split('\n').map((t) => t.trim()).find((t) => /已计入|权重合计/.test(t)),
    start_text: start?.innerText?.trim(),
    start_disabled: start ? start.disabled || start.className.includes('disabled') : null,
    industry_views: [...document.querySelectorAll('.arco-select-view')].map((el) => (el.innerText || '').trim()).slice(0, 8),
  };
});
await dump('scout-after-industry.json', { picked, ...afterPick });

if (afterPick.start_disabled === false) {
  await page.getByRole('button', { name: '开始分析' }).click();
  await page.waitForTimeout(4500);
  const afterStart = await page.evaluate(() => ({
    url: location.href,
    body: (document.querySelector('main')?.innerText || '').slice(0, 2200),
  }));
  await dump('scout-after-start.json', afterStart);
  await page.screenshot({ path: path.join(outDir, 'page-after-start.png'), fullPage: true });
}

// records tab
await gotoTarget(page);
await setReview(page, false);
await page.getByRole('tab', { name: '分析记录' }).click();
await page.waitForTimeout(1500);
const records = await page.evaluate(() => ({
  url: location.href,
  body: (document.querySelector('main')?.innerText || '').slice(0, 2200),
  tabs: [...document.querySelectorAll('[role=tab]')].map((t) => ({
    text: (t.innerText || '').trim(),
    selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
  })),
}));
await dump('scout-records.json', records);
await page.screenshot({ path: path.join(outDir, 'page-records.png'), fullPage: true });

await setReview(page, true);
await page.waitForTimeout(500);
const reviewOn = await page.evaluate(() => {
  const traces = [...document.querySelectorAll('[aria-label*=需求追溯], .trace-info-icon')].map((el) => el.getAttribute('aria-label') || '');
  const badges = [...document.querySelectorAll('[aria-label*=GAP-], [aria-label*=QC11], .perm-pending-badge, .metric-spec-card')].map((el) => el.getAttribute('aria-label') || '');
  return { traces: [...new Set(traces.filter(Boolean))], badges: [...new Set(badges.filter(Boolean))], count: traces.length };
});
await dump('scout-review-on.json', reviewOn);

console.log(JSON.stringify({ picked, start_disabled: afterPick.start_disabled, review_traces: reviewOn.count, summary: base.summaryLine }, null, 2));
await browser.close();
