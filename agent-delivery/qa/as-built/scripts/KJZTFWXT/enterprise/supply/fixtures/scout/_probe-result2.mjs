#!/usr/bin/env node
/** 结果态断链风险 Tab + 配置回填（篮内有企业）+ 评审追溯 */
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
  if (await close.first().isVisible().catch(() => false)) {
    await close.first().click();
    await page.waitForTimeout(400);
  }
}

async function login(page) {
  await page.goto(base + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(600);
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 25000 });
}

async function snap(page, name) {
  const data = await page.evaluate(() => {
    const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 160);
    return {
      url: location.href,
      title: document.title,
      h1: [...document.querySelectorAll('h1')].map(textOf),
      headings: [...document.querySelectorAll('h1,h2,h3,[role=heading]')].slice(0, 60).map(textOf),
      buttons: [...document.querySelectorAll('button,[role=button],.arco-btn')]
        .map((el) => ({
          text: textOf(el),
          disabled: !!el.disabled,
          aria: el.getAttribute('aria-label') || '',
          class: (el.className || '').toString().slice(0, 120),
        }))
        .filter((b) => b.text || b.aria)
        .slice(0, 80),
      mainText: (document.querySelector('main')?.innerText || '').slice(0, 8000),
      hasCanvas: !!document.querySelector('canvas, .g6-container, [class*=graph]'),
      canvasCount: document.querySelectorAll('canvas').length,
      reviewIcons: [...document.querySelectorAll('.trace-info-icon, [aria-label*=追溯], [title*=追溯]')].map((el) => ({
        aria: el.getAttribute('aria-label') || el.getAttribute('title') || textOf(el),
        class: (el.className || '').toString().slice(0, 80),
      })),
    };
  });
  fs.writeFileSync(path.join(outDir, `${name}.json`), JSON.stringify(data, null, 2));
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: true });
  console.log(name, data.url);
  console.log('  headings', data.headings);
  console.log('  reviewIcons', data.reviewIcons);
  console.log('  canvas', data.hasCanvas, data.canvasCount);
  console.log('  main slice', data.mainText.slice(0, 1200).replace(/\n/g, ' | '));
  return data;
}

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 })).newPage();
await login(page);

// 恢复结果 → 断链风险 Tab
await page.goto(deep + '&view=history', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await page.getByRole('button', { name: '恢复结果' }).first().click();
await page.waitForTimeout(3500);
await closeBasketIfVisible(page);
const riskTab = page.getByText('断链风险', { exact: true });
if (await riskTab.count()) {
  await riskTab.first().click();
  await page.waitForTimeout(1000);
}
await snap(page, 'scout-result-risk');

// 关键节点 Tab 再看
const keyTab = page.getByText('关键节点', { exact: true });
if (await keyTab.count()) {
  await keyTab.first().click();
  await page.waitForTimeout(800);
}
await snap(page, 'scout-result-key');

// 配置回填 2 家
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
console.log('basket open btn?', await page.getByRole('button', { name: /企业 \d+\/50/ }).count());
await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
await page.waitForTimeout(1200);
let sels = page.locator('[aria-label^="选择 "]');
console.log('sels', await sels.count());
if ((await sels.count()) < 1) {
  // 浮层空：关浮层，从系统篮确认是否有企业
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  const basketFab = page.locator('[aria-label="关闭对比篮"], button').filter({ hasText: /对比篮|共 \d+ 项/ });
  console.log('need reseed basket - skip fill detail');
} else {
  await sels.nth(0).click();
  if ((await sels.count()) >= 2) await sels.nth(1).click();
  await page.getByRole('button', { name: '确定' }).click();
  await page.waitForTimeout(2500);
  await closeBasketIfVisible(page);
  await snap(page, 'scout-filled2');
  console.log('start disabled', await page.getByRole('button', { name: '开始分析' }).isDisabled());
}

// 评审开
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(1500);
await closeBasketIfVisible(page);
await page.locator('button.persona-switch').click();
await page.waitForTimeout(600);
const sw = page.locator('[aria-label="内部评审模式"]');
console.log('switch count', await sw.count(), 'checked', await sw.getAttribute('aria-checked').catch(() => null));
if (await sw.count()) {
  if ((await sw.getAttribute('aria-checked')) !== 'true') {
    await sw.click();
    await page.waitForTimeout(800);
  }
}
await page.keyboard.press('Escape');
await page.waitForTimeout(500);
await closeBasketIfVisible(page);
await snap(page, 'scout-review2');

await browser.close();
