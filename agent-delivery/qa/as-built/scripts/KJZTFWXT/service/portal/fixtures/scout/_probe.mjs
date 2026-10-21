#!/usr/bin/env node
/**
 * 一次性无头二次探针：专题服务门户 svc-portal。产物落同目录；勿当 runner。
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

const dump = (name, data) => {
  fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2));
};

const snapMain = async (page) =>
  page.evaluate(() => {
    const main = document.querySelector('main') || document.body;
    const textLines = (main.innerText || '')
      .split('\n')
      .map((t) => t.trim())
      .filter(Boolean)
      .slice(0, 80);
    const tabs = [...document.querySelectorAll('[role=tab]')]
      .map((t) => ({
        text: (t.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 60),
        selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
        id: t.id || '',
      }))
      .filter((t) => !String(t.id).startsWith('compare-basket'));
    const selects = [...document.querySelectorAll('.arco-select-view')].map((el) => ({
      text: (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 80),
      placeholder: el.querySelector('input')?.placeholder || '',
      disabled: el.className.includes('disabled') || el.getAttribute('aria-disabled') === 'true',
      class: el.className.slice(0, 120),
    }));
    const headings = [...document.querySelectorAll('h1,h2,h3')].map((h) =>
      (h.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 80),
    );
    const reviewBtns = [...document.querySelectorAll('[aria-label]')]
      .map((el) => el.getAttribute('aria-label') || '')
      .filter((a) => /指标说明|指标未登记|需求追溯/.test(a))
      .slice(0, 30);
    const kpiHints = textLines.filter((t) =>
      /全球服务机构|本年新增|覆盖产业|深圳服务机构|技术力|在库|重点产业服务机构|口径|模拟/.test(t),
    );
    return {
      url: location.href,
      title: document.title,
      h1: [...document.querySelectorAll('h1')].map((h) => (h.innerText || '').trim()),
      headings,
      tabs,
      selects,
      reviewBtns,
      kpiHints,
      textLines,
      drawerOpen: !!document.querySelector('.arco-drawer:not([style*="display: none"])'),
      drawerText: (document.querySelector('.arco-drawer')?.innerText || '').slice(0, 500),
    };
  });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(new URL('service-portal', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(3500);
await closeBasket(page);

const overview = await snapMain(page);
dump('scout-deep-overview.json', overview);

// 产业链初始禁用探测
const chainProbe = await page.evaluate(() => {
  const views = [...document.querySelectorAll('.arco-select-view')];
  const industry = views.find((el) => (el.querySelector('input')?.placeholder || '') === '全部产业');
  const chain = views.find((el) => (el.querySelector('input')?.placeholder || '') === '全部产业链');
  return {
    industry: industry
      ? {
          disabled: industry.className.includes('disabled'),
          text: (industry.innerText || '').trim(),
          placeholder: industry.querySelector('input')?.placeholder,
        }
      : null,
    chain: chain
      ? {
          disabled: chain.className.includes('disabled'),
          text: (chain.innerText || '').trim(),
          placeholder: chain.querySelector('input')?.placeholder,
          class: chain.className.slice(0, 160),
        }
      : null,
    selectCount: views.length,
  };
});
dump('scout-filter-state.json', chainProbe);

// 展开产业下拉选项
let industryOpts = [];
try {
  const indView = page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="全部产业"]') }).first();
  await indView.click({ timeout: 5000 });
  await page.waitForTimeout(600);
  industryOpts = await page.locator('.arco-trigger-popup:visible .arco-select-option').allTextContents();
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
} catch (e) {
  industryOpts = [`ERR:${e.message}`];
}
dump('scout-industry-options.json', { count: industryOpts.length, options: industryOpts });

// 选一个产业后看产业链
let afterSelect = null;
try {
  const indView = page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="全部产业"]') }).first();
  await indView.click({ timeout: 5000 });
  await page.waitForTimeout(500);
  const opt = page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first();
  if (await opt.count()) await opt.click();
  else await page.locator('.arco-trigger-popup:visible .arco-select-option').nth(0).click();
  await page.waitForTimeout(1200);
  afterSelect = await page.evaluate(() => {
    const views = [...document.querySelectorAll('.arco-select-view')];
    const industry = views.find((el) => (el.querySelector('input')?.placeholder || el.innerText || '').includes('产业'));
    const chain = views.find((el) => (el.querySelector('input')?.placeholder || '') === '全部产业链' || (el.innerText || '').includes('产业链'));
    return {
      industryText: industry ? (industry.innerText || '').trim().slice(0, 80) : null,
      chainDisabled: chain ? chain.className.includes('disabled') : null,
      chainPlaceholder: chain?.querySelector('input')?.placeholder || null,
      chainText: chain ? (chain.innerText || '').trim().slice(0, 80) : null,
    };
  });
  // try open chain
  const chainView = page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="全部产业链"]') }).first();
  let chainOpts = [];
  if (await chainView.count()) {
    const dis = await chainView.evaluate((el) => el.className.includes('disabled'));
    if (!dis) {
      await chainView.click();
      await page.waitForTimeout(500);
      chainOpts = await page.locator('.arco-trigger-popup:visible .arco-select-option').allTextContents();
      await page.keyboard.press('Escape');
    }
    afterSelect.chainClickDisabled = dis;
    afterSelect.chainOpts = chainOpts.slice(0, 20);
  }
} catch (e) {
  afterSelect = { error: e.message };
}
dump('scout-after-industry.json', afterSelect);

// 五 Tab 深勘
const tabNames = [
  '服务机构产业分布',
  '服务机构区域分布',
  '服务机构技术能力',
  '深圳产业服务介绍',
];
const tabSnaps = {};
for (const name of tabNames) {
  await page.getByRole('tab', { name, exact: true }).click();
  await page.waitForTimeout(2500);
  await closeBasket(page);
  tabSnaps[name] = await snapMain(page);
  await page.screenshot({ path: path.join(outDir, `page-${name.replace(/\s+/g, '-')}.png`), fullPage: false });
}
dump('scout-tabs.json', tabSnaps);

// 深圳右上按钮分流
await page.getByRole('tab', { name: '全球服务机构概况', exact: true }).click();
await page.waitForTimeout(800);
await page.getByRole('button', { name: '深圳产业服务介绍', exact: true }).click();
await page.waitForTimeout(2000);
const szBtn = await snapMain(page);
dump('scout-sz-button.json', szBtn);

// 重点机构卡片 + 抽屉
let drawerSnap = null;
try {
  await page.getByRole('tab', { name: '深圳产业服务介绍', exact: true }).click();
  await page.waitForTimeout(2000);
  // scroll / find card
  const card = page.locator('text=重点产业服务机构').first();
  if (await card.count()) {
    await card.scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
  }
  // click a likely org card button/link in main
  const candidates = page.locator('main button, main a, main [role=button]').filter({ hasText: /有限|研究|中心|学院|机构/ });
  const n = await candidates.count();
  if (n > 0) {
    await candidates.first().click({ timeout: 3000 });
    await page.waitForTimeout(1500);
  } else {
    // try click any card-like
    const anyCard = page.locator('.arco-card, [class*=card]').filter({ hasText: /.+/ }).first();
    if (await anyCard.count()) await anyCard.click();
    await page.waitForTimeout(1500);
  }
  drawerSnap = await snapMain(page);
  await page.screenshot({ path: path.join(outDir, 'page-drawer.png'), fullPage: false });
} catch (e) {
  drawerSnap = { error: e.message };
}
dump('scout-drawer.json', drawerSnap);

// 评审 off 泄漏扫描
await setReview(page, false);
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);
await closeBasket(page);
const reviewOff = await page.evaluate(() => {
  const body = document.body.innerText || '';
  return {
    has指标说明: /指标说明/.test(body),
    has未登记: /指标未登记/.test(body),
    has需求追溯: /需求追溯|REQ-/.test(body),
    metricBtnCount: document.querySelectorAll('.metric-spec-card, .trace-info-icon').length,
  };
});
dump('scout-review-off.json', reviewOff);

await setReview(page, true);
await page.waitForTimeout(500);

fs.writeFileSync(
  path.join(outDir, 'scout-deep.md'),
  [
    '# svc-portal 二次无头深勘',
    '',
    `- surveyed_at: ${new Date().toISOString()}`,
    `- overview url: ${overview.url}`,
    `- industry options: ${industryOpts.length}`,
    `- chain initial: ${JSON.stringify(chainProbe.chain)}`,
    `- after industry: ${JSON.stringify(afterSelect)}`,
    `- tabs surveyed: ${tabNames.join(' / ')}`,
    `- review-off leak: ${JSON.stringify(reviewOff)}`,
    '',
  ].join('\n'),
);

await browser.close();
console.log('probe ok →', outDir);
