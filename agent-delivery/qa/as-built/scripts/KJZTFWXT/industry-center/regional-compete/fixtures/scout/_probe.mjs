#!/usr/bin/env node
/**
 * 一次性无头二次探针：区域产业竞争力评价。产物落同目录；勿当 runner。
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
const targetPath = '/industry-center/regional?workspace=competitiveness&tab=competitiveness';
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

const dump = async (name, data) => {
  fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2));
};

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await gotoTarget(page);

const base = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const radios = [...document.querySelectorAll('.arco-radio, label.arco-radio')].map((el) => ({
    text: (el.innerText || '').trim().slice(0, 80),
    checked: !!(el.querySelector('input:checked') || el.className.includes('checked')),
  })).filter((x) => x.text);
  const allTextSnips = (main.innerText || '').split('\n').map((t) => t.trim()).filter(Boolean);
  const summaryLines = allTextSnips.filter((t) => /已计入|权重合计|模板名称|未选|企业能力|学术生态|配套生态/.test(t));
  const dimLines = allTextSnips.filter((t) => /选择企业能力|选择学术生态|选择配套生态力|一键均分|单产业模式/.test(t));
  const buttons = [...document.querySelectorAll('button')].map((b) => ({
    text: (b.innerText || b.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 100),
    disabled: b.disabled || b.className.includes('disabled'),
  })).filter((b) => /开始分析|重置参数|一键均分|查看|REQ-CHAIN|系统分析|指标未登记|选择/.test(b.text));
  const spins = [...document.querySelectorAll('[role=spinbutton], input[role=spinbutton]')].map((el) => ({
    value: el.value || el.getAttribute('value') || el.getAttribute('aria-valuenow') || '',
    aria: el.getAttribute('aria-label'),
    disabled: el.disabled || el.getAttribute('aria-disabled') === 'true' || !!(el.closest('.arco-input-number-disabled')),
  }));
  const tabs = [...document.querySelectorAll('[role=tab]')].map((t) => ({
    text: (t.innerText || '').trim(),
    selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
    id: t.id || '',
  })).filter((t) => !t.id.startsWith('compare-basket'));
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
    body_snip: main.innerText.slice(0, 3500),
    radios,
    summaryLines,
    dimLines,
    buttons,
    spins,
    tabs,
    selectViews,
    review_trace_count: document.querySelectorAll('[aria-label*=需求追溯], .trace-info-icon').length,
    gap_badge: !!document.querySelector('[aria-label*=GAP-CHAIN-REG-METRICS]'),
    has_index_title: /区域产业指数评价/.test(document.title) || /区域产业指数评价/.test(main.innerText),
    has_compete_title: /区域产业竞争力评价/.test(document.title),
  };
});
await dump('scout-deep.json', base);
await page.screenshot({ path: path.join(outDir, 'page-deep.png'), fullPage: true });

// open industry options
await page.locator('.arco-select-view[aria-label="产业"]').click();
await page.waitForTimeout(700);
const indOpts = await page.locator('.arco-trigger-popup .arco-select-option').evaluateAll((els) =>
  els.map((e) => (e.innerText || '').trim()).filter(Boolean).slice(0, 20),
);
await page.keyboard.press('Escape');
await page.waitForTimeout(300);
await dump('scout-industry-options.json', { options: indOpts });

// open region options（评价区域，避开对比篮「全部企业类型」）
let regionOpts = [];
try {
  const region = page.locator('main .arco-select-view-multiple').filter({ hasText: /深圳|请选择区域|广东/ }).first();
  if (await region.count()) {
    await region.click({ timeout: 5000 });
    await page.waitForTimeout(900);
    const pop = page.locator('.arco-trigger-popup:visible').last();
    if (await pop.count()) {
      regionOpts = await pop.evaluate((el) =>
        [...el.querySelectorAll('.arco-select-option, .arco-checkbox, li, .arco-tree-node-title, label, span')]
          .map((e) => (e.innerText || '').trim())
          .filter((t) => t && t.length < 40)
          .filter((t, i, a) => a.indexOf(t) === i)
          .slice(0, 40),
      );
    }
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
  }
} catch (e) {
  regionOpts = [`ERROR: ${e.message}`];
}
await dump('scout-region-options.json', { options: regionOpts });

// dump dimension block structure (checkbox+weight+查看; may be locked)
const dimDump = await page.evaluate(() => {
  const labels = ['选择企业能力', '选择学术生态', '选择配套生态力'];
  return labels.map((aria) => {
    const el = document.querySelector(`[aria-label="${aria}"]`);
    const weight = document.querySelector(`[aria-label="${aria.replace('选择', '')}权重"]`);
    const row = el?.closest('div,li,tr,section') || el?.parentElement;
    return {
      aria,
      tag: el?.tagName,
      className: el?.className?.slice?.(0, 120),
      checked: el?.getAttribute?.('aria-checked') || el?.className?.includes?.('checked'),
      disabled: el?.getAttribute?.('aria-disabled') || el?.className?.includes?.('disabled'),
      text: (el?.innerText || '').trim().slice(0, 80),
      weightValue: weight?.querySelector?.('input')?.value || weight?.getAttribute?.('aria-valuenow') || null,
      weightDisabled: !!(weight?.className?.includes?.('disabled') || weight?.querySelector?.('input')?.disabled),
      rowText: (row?.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 160),
    };
  });
});
await dump('scout-dim-enterprise.json', { dims: dimDump });

// switch to multi mode
await page.getByText('多产业 × 单区域', { exact: true }).first().click();
await page.waitForTimeout(1000);
const multiState = await page.evaluate(() => {
  const selectViews = [...document.querySelectorAll('.arco-select-view')].map((el) => ({
    text: (el.innerText || '').trim().slice(0, 80),
    aria: el.getAttribute('aria-label'),
    multi: el.className.includes('mult'),
    placeholder: el.querySelector('input')?.placeholder,
  }));
  const labels = (document.querySelector('main')?.innerText || '').split('\n').map((t) => t.trim()).filter((t) => /分析对象|评价区域|请选择/.test(t)).slice(0, 20);
  return { selectViews, labels, url: location.href };
});
await dump('scout-mode-multi.json', multiState);

// back to single, select industry + try start gate
await page.getByText('单产业 × 多区域', { exact: true }).first().click();
await page.waitForTimeout(800);
try {
  await page.locator('.arco-select-view[aria-label="产业"]').click({ timeout: 5000 });
  await page.waitForTimeout(600);
  const opt = page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '集成电路' }).first();
  if (await opt.count()) await opt.click({ force: true });
  else {
    const any = page.locator('.arco-trigger-popup:visible .arco-select-option').first();
    if (await any.count()) await any.click({ force: true });
  }
  await page.waitForTimeout(1000);
} catch (e) {
  await dump('scout-industry-pick-error.json', { error: e.message });
}

// 维度为固定勾选+权重；先读态，再试填权重 / 一键均分 / 开始分析门控
const dimState = await page.evaluate(() => {
  const spins = [...document.querySelectorAll('[role=spinbutton]')].map((el) => ({
    value: el.value || '',
    aria: el.getAttribute('aria-label'),
    disabled: el.disabled || !!(el.closest('.arco-input-number-disabled')),
  }));
  const checks = ['选择企业能力', '选择学术生态', '选择配套生态力'].map((aria) => {
    const el = document.querySelector(`[aria-label="${aria}"]`);
    return {
      aria,
      disabled: el?.className?.includes('disabled') || el?.getAttribute('aria-disabled') === 'true',
      checked: el?.className?.includes('checked') || el?.getAttribute('aria-checked') === 'true',
    };
  });
  const summary = (document.querySelector('main')?.innerText || '')
    .split('\n')
    .map((t) => t.trim())
    .filter((t) => /已计入|权重合计|模板|校验|单产业模式/.test(t));
  const start = [...document.querySelectorAll('button')].find((b) => (b.innerText || '').includes('开始分析'));
  return {
    checks,
    spins,
    summary,
    startDisabled: start ? start.disabled || start.className.includes('disabled') : null,
  };
});
await dump('scout-after-dims.json', { afterIndustry: dimState });

// try edit weights if enabled
const spins = page.locator('main [role=spinbutton]');
const spinCount = await spins.count();
const weightEdits = [];
for (let i = 0; i < Math.min(spinCount, 3); i++) {
  const disabled = await spins.nth(i).isDisabled().catch(async () =>
    spins.nth(i).evaluate((el) => el.disabled || !!el.closest('.arco-input-number-disabled')),
  );
  if (disabled) {
    weightEdits.push({ i, disabled: true });
    continue;
  }
  await spins.nth(i).fill(String(30 + i));
  await page.waitForTimeout(200);
  weightEdits.push({ i, disabled: false, value: await spins.nth(i).inputValue() });
}
await page.getByRole('button', { name: '一键均分' }).click().catch(() => {});
await page.waitForTimeout(800);
const afterAvg = await page.evaluate(() => {
  const spins = [...document.querySelectorAll('[role=spinbutton]')].map((el) => el.value || '');
  const start = [...document.querySelectorAll('button')].find((b) => (b.innerText || '').includes('开始分析'));
  const summary = (document.querySelector('main')?.innerText || '')
    .split('\n')
    .map((t) => t.trim())
    .filter((t) => /已计入|权重合计|模板|校验/.test(t));
  return {
    spins,
    summary,
    startDisabled: start ? start.disabled || start.className.includes('disabled') : null,
  };
});
await dump('scout-after-avg.json', { weightEdits, afterAvg });

const startBtn = page.getByRole('button', { name: '开始分析' });
const startEnabled = await startBtn.isEnabled().catch(() => false);
if (startEnabled) {
  await startBtn.click();
  await page.waitForTimeout(3500);
  await dump('scout-after-start.json', {
    url: page.url(),
    title: await page.title(),
    body: await page.locator('main').innerText().then((t) => t.slice(0, 2000)).catch(() => ''),
  });
} else {
  await dump('scout-after-start.json', { skipped: true, reason: 'start still disabled', startEnabled, afterAvg });
}

// records tab
await gotoTarget(page);
await page.getByRole('tab', { name: '分析记录', exact: true }).click();
await page.waitForTimeout(2000);
await dump('scout-records.json', {
  url: page.url(),
  body: await page.locator('main').innerText().then((t) => t.slice(0, 2500)).catch(() => ''),
});

// review off zero leak
await gotoTarget(page);
await setReview(page, false);
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);
await closeBasket(page);
const reviewOff = await page.evaluate(() => {
  const html = document.body.innerText + document.body.innerHTML;
  return {
    hasReq: /REQ-CHAIN-REG/.test(html),
    hasHandoff: /系统分析任务交接/.test(html),
    hasGap: /指标未登记|GAP-CHAIN-REG-METRICS/.test(html),
    title: document.title,
  };
});
await dump('scout-review-off.json', reviewOff);

await setReview(page, true);
await page.waitForTimeout(500);
const reviewOn = await page.evaluate(() => ({
  hasReq: !!document.querySelector('[aria-label*=REQ-CHAIN-REG-03]'),
  hasHandoff: !!document.querySelector('[aria-label*=系统分析任务交接]'),
  hasGap: !!document.querySelector('[aria-label*=GAP-CHAIN-REG-METRICS]'),
}));
await dump('scout-review-on.json', reviewOn);

// sibling isolation: go to index workspace briefly
await page.goto(new URL('industry-center/regional?workspace=index&tab=index', baseUrl).toString(), {
  waitUntil: 'domcontentloaded',
  timeout: 60000,
});
await page.waitForTimeout(4000);
await closeBasket(page);
const indexSnap = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  return {
    title: document.title,
    hasFourForce: /商业力|技术力|学术力|支撑力/.test(main.innerText),
    hasThreeDim: /选择企业能力|选择学术生态|选择配套生态力/.test(main.innerText),
    hasAvg: /一键均分/.test(main.innerText),
    hasOfficialTpl: /区域产业指数官方模板/.test(main.innerText),
  };
});
await dump('scout-sibling-index.json', indexSnap);

await page.goto(new URL(targetPath.replace(/^\//, ''), baseUrl).toString(), {
  waitUntil: 'domcontentloaded',
  timeout: 60000,
});
await page.waitForTimeout(3500);
await closeBasket(page);
const backSnap = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  return {
    title: document.title,
    hasThreeDim: /选择企业能力|选择学术生态|选择配套生态力/.test(main.innerText),
    hasFourForceTpl: /区域产业指数官方模板|商业力/.test(main.innerText),
    url: location.href,
  };
});
await dump('scout-sibling-back.json', backSnap);

console.log('probe ok →', outDir);
await browser.close();
