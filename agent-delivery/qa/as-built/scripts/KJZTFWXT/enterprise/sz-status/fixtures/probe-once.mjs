#!/usr/bin/env node
/** 一次性二次探测：深圳企业现状分析 空态/选链结果/对标 Tab。产出落 fixtures/scout/
 *  在 as-built/tools 目录执行：node ../scripts/.../sz-status/fixtures/probe-once.mjs
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const outDir = path.join(__dirname, 'scout');
const base = 'https://edu.itic-sci.com/tts/svcz/';
fs.mkdirSync(outDir, { recursive: true });

async function login(page) {
  for (let i = 0; i < 3; i++) {
    if (!page.url().includes('/login')) return;
    console.log('login attempt', i + 1, page.url());
    await page.waitForTimeout(500);
    await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
    await page.locator('input[type=password]').first().fill('123456');
    const btn = page.getByRole('button', { name: /登录/ });
    if (await btn.count()) await btn.first().click();
    else await page.keyboard.press('Enter');
    try {
      await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
      return;
    } catch (e) {
      console.log('login wait fail', page.url(), e.message);
    }
  }
  throw new Error('login failed: ' + page.url());
}

async function snap(page, name) {
  const data = await page.evaluate(() => {
    const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 120);
    const collect = (sel, limit = 60) =>
      [...document.querySelectorAll(sel)].slice(0, limit).map((el) => ({
        tag: el.tagName.toLowerCase(),
        text: textOf(el),
        attrs: (() => {
          const o = {};
          for (const n of ['id', 'name', 'placeholder', 'aria-label', 'role', 'type', 'title', 'disabled', 'aria-disabled', 'aria-selected', 'aria-checked']) {
            if (el.getAttribute(n)) o[n] = el.getAttribute(n).slice(0, 160);
          }
          if (el.disabled) o.disabled = 'true';
          if (el.className && typeof el.className === 'string') o.class = el.className.slice(0, 160);
          return o;
        })(),
      }));
    return {
      url: location.href,
      title: document.title,
      h1: [...document.querySelectorAll('h1')].map(textOf),
      headings: [...document.querySelectorAll('h1,h2,h3,[role=heading]')].slice(0, 50).map(textOf),
      buttons: collect('button, [role=button], .arco-btn, [role=tab]'),
      textboxes: collect('input, textarea, [role=textbox], .arco-select-view, .arco-input, span.sci-arco-cascader'),
      switches: collect('[role=switch], .arco-switch'),
      menus: collect('[role=menuitem], .arco-menu-item'),
      sections: collect('section, [aria-label]', 50),
      tabs: collect('[role=tab], .arco-tabs-header-title, .arco-tabs-tab'),
      mainText: (document.querySelector('main')?.innerText || document.body.innerText || '').slice(0, 4000),
    };
  });
  fs.writeFileSync(path.join(outDir, `${name}.json`), JSON.stringify(data, null, 2));
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: true });
  return data;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const target = `${base}enterprise/shenzhen-enterprise-status-analysis`;
console.log('goto', target);
await page.goto(base + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
await login(page);
console.log('after login', page.url());
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await login(page);
await page.waitForTimeout(3500);
console.log('on page', page.url(), await page.title());

async function dismissBasket() {
  for (let i = 0; i < 3; i++) {
    const closeBasket = page.getByRole('button', { name: /关闭对比篮/ }).first();
    if (await closeBasket.count()) {
      await closeBasket.click({ force: true }).catch(() => {});
      await page.waitForTimeout(500);
    }
    await page.evaluate(() => {
      document.querySelectorAll('.compare-basket-drawer, [class*=compare-basket], .arco-drawer').forEach((el) => {
        const t = el.innerText || '';
        if (t.includes('对比篮') || t.includes('篮内企业')) el.remove();
      });
      document.querySelectorAll('.arco-drawer-mask, .arco-modal-mask').forEach((el) => el.remove());
    });
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(300);
  }
}
await dismissBasket();

const empty = await snap(page, 'scout-empty');
console.log('empty h1', empty.h1);
console.log('empty headings', empty.headings);
console.log('empty tabs', empty.tabs.map((t) => t.text));
console.log('empty buttons', empty.buttons.slice(0, 40).map((b) => b.text));
console.log('empty textboxes', empty.textboxes.slice(0, 20).map((b) => b.text || b.attrs.placeholder));
console.log('mainText head:\n', empty.mainText.slice(0, 1500));

// 区域控件 disabled 态
const regionInfo = await page.evaluate(() => {
  const casc = document.querySelector('span.sci-arco-cascader, .arco-cascader-view, .arco-select-view');
  const input = document.querySelector('input[placeholder*="深圳"], input[placeholder*="全国热门"]');
  const el = casc || input;
  if (!el) return { found: false };
  const cls = el.className || '';
  return {
    found: true,
    tag: el.tagName,
    class: String(cls).slice(0, 200),
    disabled: el.getAttribute('disabled') || el.getAttribute('aria-disabled') || /disabled/.test(cls),
    text: (el.innerText || el.value || '').slice(0, 80),
  };
});
console.log('regionInfo', regionInfo);
fs.writeFileSync(path.join(outDir, 'scout-region.json'), JSON.stringify(regionInfo, null, 2));

// 快捷标签：可见 chip / button / tag
const tagSnap = await page.evaluate(() => {
  const labels = ['集成电路', '生物医药', '人工智能', '新能源', '低空经济', '量子信息', '海洋经济', '智能机器人'];
  return labels.map((name) => {
    const nodes = [...document.querySelectorAll('button, .arco-tag, .arco-btn, [role=button], span, a')].filter(
      (el) => (el.innerText || '').trim() === name,
    );
    return {
      name,
      count: nodes.length,
      visible: nodes.some((el) => {
        const r = el.getBoundingClientRect();
        const st = getComputedStyle(el);
        return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' && st.display !== 'none';
      }),
      classes: nodes.slice(0, 3).map((el) => String(el.className).slice(0, 100)),
    };
  });
});
console.log('tagSnap', tagSnap);
fs.writeFileSync(path.join(outDir, 'scout-tags.json'), JSON.stringify(tagSnap, null, 2));

// 选链：优先点可见快捷标签，否则开下拉选
await dismissBasket();
let selected = false;
const visibleAi = page.locator('main button, main .arco-tag, main .arco-btn').filter({ hasText: /^人工智能$/ }).first();
if (await visibleAi.count()) {
  try {
    await visibleAi.click({ timeout: 5000 });
    selected = true;
    console.log('selected via chip');
  } catch (e) {
    console.log('visibleAi click fail', e.message);
  }
}
if (!selected) {
  const chainTrigger = page.locator('main .arco-select-view').filter({ hasText: /请选择产业链|人工智能|生物医药/ }).first();
  console.log('chainTrigger count', await chainTrigger.count());
  if (await chainTrigger.count()) {
    await chainTrigger.click({ timeout: 8000 });
    await page.waitForTimeout(800);
    const popupOpts = page.locator('.arco-trigger-popup:visible .arco-select-option-content, .arco-trigger-popup:visible .arco-select-option');
    const optTexts = [];
    const n = await popupOpts.count();
    for (let i = 0; i < n; i++) optTexts.push((await popupOpts.nth(i).textContent()).trim());
    console.log('chain options', optTexts);
    fs.writeFileSync(path.join(outDir, 'scout-chain-options.json'), JSON.stringify(optTexts, null, 2));
    const opt = page.locator('.arco-trigger-popup:visible').getByText('人工智能', { exact: true }).first();
    await opt.click({ timeout: 8000 });
    selected = true;
    console.log('selected via dropdown');
  }
}
if (selected) {
  await page.waitForTimeout(5000);
  const result = await snap(page, 'scout-result-ai');
  console.log('result headings', result.headings);
  console.log('result mainText head:\n', result.mainText.slice(0, 2500));
} else {
  console.log('AI chain not selected');
}

// 对标 Tab
await dismissBasket();
const benchTab = page.locator('main [role=tab], main .arco-tabs-tab').filter({ hasText: '多城市横向对标' }).first();
if (await benchTab.count()) {
  await benchTab.click({ timeout: 8000 });
  console.log('clicked benchmark tab');
} else {
  console.log('benchmark tab not found');
}
await page.waitForTimeout(5000);
const bench = await snap(page, 'scout-benchmark');
console.log('bench headings', bench.headings);
console.log('bench mainText head:\n', bench.mainText.slice(0, 2500));

// 回定位 Tab 再抓
const posTab = page.locator('main [role=tab], main .arco-tabs-tab').filter({ hasText: '产业链定位' }).first();
if (await posTab.count()) await posTab.click({ timeout: 8000 });
await page.waitForTimeout(2000);
await snap(page, 'scout-back-position');

// 覆写主 scout（survey-page 同口径）
const main = await snap(page, 'scout');
fs.writeFileSync(
  path.join(outDir, 'scout.md'),
  [
    `# 无头实勘 /enterprise/shenzhen-enterprise-status-analysis`,
    '',
    `- url: ${main.url}`,
    `- title: ${main.title}`,
    `- h1: ${main.h1.join(' | ') || '(无)'}`,
    `- screenshot: scout.png`,
    '',
    '## headings',
    ...main.headings.map((t) => `- ${t}`),
    '',
    '## buttons (截断)',
    ...main.buttons.slice(0, 35).map((b) => `- ${b.text || '(无文案)'} · ${JSON.stringify(b.attrs)}`),
    '',
    '## textboxes / selects',
    ...main.textboxes.slice(0, 25).map((b) => `- ${b.text || b.attrs.placeholder || '(空)'} · ${JSON.stringify(b.attrs)}`),
    '',
    '## tabs',
    ...main.tabs.map((b) => `- ${b.text || '(tab)'} · ${JSON.stringify(b.attrs)}`),
    '',
    '## switches',
    ...main.switches.map((b) => `- ${b.text || '(switch)'} · ${JSON.stringify(b.attrs)}`),
    '',
    '## mainText (截断)',
    '```',
    main.mainText.slice(0, 2000),
    '```',
  ].join('\n'),
  'utf8',
);
await page.screenshot({ path: path.join(outDir, 'page.png'), fullPage: true });

await browser.close();
console.log('probe done →', outDir);
