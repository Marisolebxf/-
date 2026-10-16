#!/usr/bin/env node
/**
 * 一次性无头探针：先 /login 再深链 supply-chain。产物落同目录；勿当 runner。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');
const base = 'http://111.198.38.90:50892/';
const outDir = __dirname;
const deep = base + 'enterprise/risk?workspace=supply-chain&tab=supply-chain';

async function closeBasketIfVisible(page) {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if (!(await close.count())) return;
  const vis = await close.first().isVisible().catch(() => false);
  if (vis) {
    await close.first().click();
    await page.waitForTimeout(400);
  }
}

async function snap(page, name) {
  const data = await page.evaluate(() => {
    const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 120);
    const collect = (sel, limit = 80) =>
      [...document.querySelectorAll(sel)].slice(0, limit).map((el) => ({
        tag: el.tagName.toLowerCase(),
        text: textOf(el),
        attrs: (() => {
          const o = {};
          for (const n of [
            'id',
            'name',
            'placeholder',
            'aria-label',
            'role',
            'type',
            'title',
            'aria-disabled',
            'aria-selected',
            'aria-checked',
            'aria-checked',
          ]) {
            if (el.getAttribute(n)) o[n] = el.getAttribute(n).slice(0, 160);
          }
          if (el.className && typeof el.className === 'string') o.class = el.className.slice(0, 160);
          if (el.disabled) o.disabled = true;
          return o;
        })(),
      }));
    return {
      url: location.href,
      title: document.title,
      h1: [...document.querySelectorAll('h1')].map(textOf),
      headings: [...document.querySelectorAll('h1,h2,h3,[role=heading]')].slice(0, 50).map(textOf),
      tabs: collect('[role=tab], .arco-tabs-header-title, .arco-tabs-tab'),
      buttons: collect('button, [role=button], .arco-btn'),
      checkboxes: collect('.arco-checkbox, label.arco-checkbox-label, input[type=checkbox]', 40),
      inputs: collect(
        'input, textarea, select, [role=combobox], .arco-select-view, .arco-cascader-view, span.sci-arco-cascader',
      ),
      switches: collect('[role=switch], .arco-switch'),
      sections: collect('section, [aria-label]', 40),
      mainText: (document.querySelector('main')?.innerText || document.body.innerText || '').slice(0, 6000),
    };
  });
  fs.writeFileSync(path.join(outDir, `${name}.json`), JSON.stringify(data, null, 2));
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: true });
  return data;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

console.log('login…');
await page.goto(base + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(800);
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 25000 });
}

console.log('goto supply…');
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(3500);
await closeBasketIfVisible(page);

const empty = await snap(page, 'scout');
fs.writeFileSync(path.join(outDir, 'scout.md'), [
  '# scout · ent-supply（空态配置页）',
  '',
  '> 先 /login 再深链；2026-10-14 headless',
  '',
  `- url: ${empty.url}`,
  `- title: ${empty.title}`,
  `- h1: ${JSON.stringify(empty.h1)}`,
  '',
  '## headings',
  ...empty.headings.map((h) => `- ${h}`),
  '',
  '## tabs',
  ...empty.tabs.map((t) => `- ${t.text || '(no)'} | ${JSON.stringify(t.attrs)}`),
  '',
  '## buttons (截断)',
  ...empty.buttons
    .filter((b) => b.text)
    .slice(0, 50)
    .map((b) => `- ${b.text} | disabled=${!!b.attrs?.disabled} | ${b.attrs?.['aria-label'] || ''}`),
  '',
  '## checkboxes',
  ...empty.checkboxes.slice(0, 30).map((c) => `- ${c.text} | ${JSON.stringify(c.attrs)}`),
  '',
  '## mainText',
  empty.mainText,
].join('\n'));
console.log('empty url', empty.url, 'h1', empty.h1);

// 最近分析 Tab
const recentTab = page.locator('main [role=tab], main .arco-tabs-tab, main button').filter({ hasText: '最近分析' });
if (await recentTab.count()) {
  await recentTab.first().click();
  await page.waitForTimeout(1500);
  await closeBasketIfVisible(page);
  await snap(page, 'scout-recent');
  console.log('recent snapped');
  // 回当前分析
  const cur = page.locator('main [role=tab], main .arco-tabs-tab, main button').filter({ hasText: '当前分析' });
  if (await cur.count()) {
    await cur.first().click();
    await page.waitForTimeout(800);
  }
}

// 尝试带入对象：优先页内 CTA，否则系统对比篮发起（用例口径）
await closeBasketIfVisible(page);
const cta = page.getByRole('button', { name: /前往对比篮|选择企业/ });
if (await cta.count()) {
  await cta.first().click();
  await page.waitForTimeout(1200);
  await snap(page, 'scout-overlay');
  const sels = page.locator('[aria-label^="选择 "]');
  const n = await sels.count();
  console.log('overlay selectable', n);
  if (n >= 1) {
    await sels.nth(0).click();
    if (n >= 2) await sels.nth(1).click();
    const ok = page.getByRole('button', { name: /确定|发起分析/ });
    if (await ok.count()) {
      await ok.first().click();
      await page.waitForTimeout(2000);
    }
    // 六类型弹窗？
    const supplyOpt = page.getByText('企业供应链关系分析', { exact: true });
    if (await supplyOpt.count()) {
      await supplyOpt.first().click();
      await page.waitForTimeout(400);
      const submit = page.getByRole('button', { name: /确定|提交|开始/ });
      if (await submit.count()) await submit.first().click();
      await page.waitForTimeout(2000);
    }
    await closeBasketIfVisible(page);
    await snap(page, 'scout-after-select');
    console.log('after-select url', page.url());
  }
} else {
  // 系统对比篮浮层
  const openBasket = page.getByRole('button', { name: /打开对比篮|对比篮/ });
  if (await openBasket.count()) {
    await openBasket.first().click();
    await page.waitForTimeout(1000);
    await snap(page, 'scout-system-basket');
  }
}

// 痛点视图隔离探测（只记 observed，不写痛点脚本）
await page.goto(base + 'enterprise/risk?workspace=pain-points&tab=pain-points', {
  waitUntil: 'domcontentloaded',
  timeout: 60000,
});
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await snap(page, 'scout-pain-sibling');
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await snap(page, 'scout-back-supply');

await browser.close();
console.log('done →', outDir);
