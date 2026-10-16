#!/usr/bin/env node
/** 二次探针：产业选中门控 / 记录 Tab / 评审零泄漏 / 兄弟隔离。勿当 runner。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const targetPath = '/industry-center/regional?workspace=competitiveness&tab=competitiveness';
const outDir = __dirname;
const dump = (name, data) => fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2));

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

async function setReview(page, on) {
  await page.locator('button.persona-switch').first().click();
  await page.waitForTimeout(500);
  const sw = page.getByRole('switch', { name: '内部评审模式' });
  if (await sw.count()) {
    const checked = await sw.getAttribute('aria-checked');
    if (on && checked !== 'true') await sw.click();
    if (!on && checked === 'true') await sw.click();
  }
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
}

async function gotoTarget(page) {
  await page.goto(new URL(targetPath.replace(/^\//, ''), baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await ensureLogin(page);
  if (page.url().includes('/login')) {
    await ensureLogin(page);
    await page.goto(new URL(targetPath.replace(/^\//, ''), baseUrl).toString(), {
      waitUntil: 'domcontentloaded',
      timeout: 60000,
    });
  }
  await page.waitForTimeout(3500);
  await closeBasket(page);
}

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();

await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await gotoTarget(page);
await setReview(page, false);
await closeBasket(page);

// --- industry pick & gate ---
const before = await page.evaluate(() => {
  const start = [...document.querySelectorAll('button')].find((b) => (b.innerText || '').includes('开始分析'));
  const ind = document.querySelector('.arco-select-view[aria-label="产业"]');
  return {
    startDisabled: start ? start.disabled || start.className.includes('disabled') : null,
    industryText: (ind?.innerText || '').trim(),
    hint: /单产业模式请选择 1 个产业/.test(document.querySelector('main')?.innerText || ''),
  };
});

await page.locator('.arco-select-view[aria-label="产业"]').click();
await page.waitForTimeout(800);
const popupInfo = await page.locator('.arco-trigger-popup:visible').last().evaluate((el) => ({
  text: (el.innerText || '').slice(0, 500),
  options: [...el.querySelectorAll('.arco-select-option')].map((o) => (o.innerText || '').trim()).filter(Boolean).slice(0, 25),
})).catch((e) => ({ error: e.message }));

let picked = null;
const visibleOpts = page.locator('.arco-trigger-popup:visible .arco-select-option');
const n = await visibleOpts.count();
for (let i = 0; i < n; i++) {
  const t = (await visibleOpts.nth(i).innerText()).trim();
  if (t === '集成电路' || t === '人工智能' || t === '传感器') {
    await visibleOpts.nth(i).click({ force: true });
    picked = t;
    break;
  }
}
if (!picked && n > 0) {
  // skip group headers; pick last leaf-like
  for (let i = n - 1; i >= 0; i--) {
    const t = (await visibleOpts.nth(i).innerText()).trim();
    if (t && t.length < 20) {
      await visibleOpts.nth(i).click({ force: true });
      picked = t;
      break;
    }
  }
}
await page.waitForTimeout(1500);
await page.keyboard.press('Escape').catch(() => {});

const afterPick = await page.evaluate(() => {
  const start = [...document.querySelectorAll('button')].find((b) => (b.innerText || '').includes('开始分析'));
  const ind = document.querySelector('.arco-select-view[aria-label="产业"]');
  const spins = [...document.querySelectorAll('[role=spinbutton]')].map((el) => el.value || '');
  return {
    startDisabled: start ? start.disabled || start.className.includes('disabled') : null,
    industryText: (ind?.innerText || '').trim(),
    hint: /单产业模式请选择 1 个产业/.test(document.querySelector('main')?.innerText || ''),
    spins,
    spinSum: spins.map(Number).reduce((a, b) => a + b, 0),
    body_snip: (document.querySelector('main')?.innerText || '').slice(0, 1800),
  };
});
dump('scout-gate.json', { before, popupInfo, picked, afterPick });

if (!afterPick.startDisabled) {
  await page.getByRole('button', { name: '开始分析' }).click();
  await page.waitForTimeout(4000);
  dump('scout-after-start2.json', {
    url: page.url(),
    title: await page.title(),
    body: await page.locator('main').innerText().then((t) => t.slice(0, 2000)).catch(() => ''),
  });
} else {
  dump('scout-after-start2.json', { skipped: true, afterPick });
}

// --- records ---
await gotoTarget(page);
await closeBasket(page);
const recTab = page.getByRole('tab', { name: '分析记录', exact: true });
await recTab.click({ timeout: 10000 });
await page.waitForTimeout(2500);
dump('scout-records.json', {
  url: page.url(),
  selected: await recTab.getAttribute('aria-selected').catch(() => null),
  body: await page.locator('main').innerText().then((t) => t.slice(0, 2500)).catch(() => ''),
});

// --- review off ---
await gotoTarget(page);
await setReview(page, false);
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3500);
await closeBasket(page);
dump('scout-review-off.json', await page.evaluate(() => {
  const t = document.body.innerText;
  const html = document.body.innerHTML;
  return {
    title: document.title,
    hasReqBtn: !!document.querySelector('[aria-label*="REQ-CHAIN-REG-03"]'),
    hasHandoffBtn: !!document.querySelector('[aria-label*="系统分析任务交接"]'),
    hasGapBtn: !!document.querySelector('[aria-label*="GAP-CHAIN-REG-METRICS"]'),
    textHasReq: /REQ-CHAIN-REG/.test(t),
    textHasHandoff: /系统分析任务交接/.test(t),
    textHasGap: /指标未登记|GAP-CHAIN-REG-METRICS/.test(t),
    htmlHasGap: /GAP-CHAIN-REG-METRICS/.test(html),
  };
}));

await setReview(page, true);
await page.waitForTimeout(600);
dump('scout-review-on.json', await page.evaluate(() => ({
  hasReqBtn: !!document.querySelector('[aria-label*="REQ-CHAIN-REG-03"]'),
  hasHandoffBtn: !!document.querySelector('[aria-label*="系统分析任务交接"]'),
  hasGapBtn: !!document.querySelector('[aria-label*="GAP-CHAIN-REG-METRICS"]'),
})));

// --- sibling index isolation ---
await page.goto(new URL('industry-center/regional?workspace=index&tab=index', baseUrl).toString(), {
  waitUntil: 'domcontentloaded',
  timeout: 60000,
});
await page.waitForTimeout(4500);
await closeBasket(page);
dump('scout-sibling-index.json', await page.evaluate(() => {
  const main = document.querySelector('main')?.innerText || '';
  return {
    title: document.title,
    hasFourForce: /商业力|技术力|学术力|支撑力/.test(main),
    hasOfficialTpl: /区域产业指数官方模板/.test(main),
    hasThreeDimSelect: /选择企业能力|选择学术生态|选择配套生态力/.test(main),
    hasCompeteTitleInMain: /区域产业竞争力评价/.test(main),
  };
}));

await page.goto(new URL(targetPath.replace(/^\//, ''), baseUrl).toString(), {
  waitUntil: 'domcontentloaded',
  timeout: 60000,
});
await page.waitForTimeout(3500);
await closeBasket(page);
dump('scout-sibling-back.json', await page.evaluate(() => {
  const main = document.querySelector('main')?.innerText || '';
  return {
    title: document.title,
    url: location.href,
    hasThreeDim: /企业能力|学术生态|配套生态力/.test(main),
    hasOfficialTpl: /区域产业指数官方模板/.test(main),
    hasFourForceGroups: /商业力[\s\S]*技术力/.test(main),
  };
}));

console.log('probe2 ok');
await browser.close();
