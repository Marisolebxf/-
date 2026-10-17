#!/usr/bin/env node
/** 二次深勘：配置回填（不误点开始）、超限 3 家、恢复已完成结果态、评审追溯按钮 */
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
    const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 140);
    const collect = (sel, limit = 80) =>
      [...document.querySelectorAll(sel)].slice(0, limit).map((el) => ({
        tag: el.tagName.toLowerCase(),
        text: textOf(el),
        attrs: (() => {
          const o = {};
          for (const n of ['aria-label', 'role', 'type', 'title', 'aria-disabled', 'aria-selected', 'placeholder', 'class']) {
            if (el.getAttribute(n)) o[n] = el.getAttribute(n).slice(0, 180);
          }
          if (el.disabled) o.disabled = true;
          return o;
        })(),
      }));
    return {
      url: location.href,
      title: document.title,
      h1: [...document.querySelectorAll('h1')].map(textOf),
      headings: [...document.querySelectorAll('h1,h2,h3,[role=heading]')].slice(0, 60).map(textOf),
      buttons: collect('button, [role=button], .arco-btn').filter((b) => b.text).slice(0, 60),
      checkboxes: collect('.arco-checkbox', 40),
      mainText: (document.querySelector('main')?.innerText || '').slice(0, 7000),
    };
  });
  fs.writeFileSync(path.join(outDir, `${name}.json`), JSON.stringify(data, null, 2));
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: true });
  console.log(name, data.url, 'h1=', data.h1, 'btns=', data.buttons.slice(0, 12).map((b) => b.text + (b.attrs?.disabled ? '[dis]' : '')));
  return data;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
await login(page);

// —— 1) 回填 2 家，仅点浮层「确定」，不点开始分析 ——
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
await page.waitForTimeout(800);
const sels = page.locator('[aria-label^="选择 "]');
const n = await sels.count();
console.log('selectable', n);
if (n >= 2) {
  await sels.nth(0).click();
  await sels.nth(1).click();
  await page.waitForTimeout(300);
  await page.getByRole('button', { name: '确定' }).click({ timeout: 8000 });
  await page.waitForTimeout(2500);
}
await closeBasketIfVisible(page);
await snap(page, 'scout-filled');

// 开始分析是否可用
const start = page.getByRole('button', { name: '开始分析' });
console.log('start disabled?', await start.isDisabled().catch(() => 'n/a'));

// —— 2) 超限 3 家 ——
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(1500);
await closeBasketIfVisible(page);
await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
await page.waitForTimeout(800);
const sels3 = page.locator('[aria-label^="选择 "]');
const n3 = await sels3.count();
if (n3 >= 3) {
  await sels3.nth(0).click();
  await sels3.nth(1).click();
  await sels3.nth(2).click();
  await page.getByRole('button', { name: '确定' }).click({ timeout: 8000 });
  await page.waitForTimeout(2500);
}
await closeBasketIfVisible(page);
await snap(page, 'scout-overlimit');
console.log('overlimit start disabled?', await page.getByRole('button', { name: '开始分析' }).isDisabled().catch(() => 'n/a'));

// —— 3) 最近分析 → 恢复已完成 ——
await page.goto(deep + '&view=history', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
const restore = page.getByRole('button', { name: '恢复结果' });
console.log('restore count', await restore.count());
if (await restore.count()) {
  await restore.first().click();
  await page.waitForTimeout(4000);
  await closeBasketIfVisible(page);
  await snap(page, 'scout-result');
}

// —— 4) 评审模式开：追溯按钮 ——
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(1500);
await closeBasketIfVisible(page);
const persona = page.locator('button.persona-switch, [class*=persona]').first();
if (await persona.count()) {
  await persona.click();
  await page.waitForTimeout(500);
  const sw = page.locator('[aria-label="内部评审模式"]');
  if (await sw.count()) {
    const checked = await sw.getAttribute('aria-checked');
    if (checked !== 'true') await sw.click();
    await page.waitForTimeout(800);
  }
  // 关菜单以免挡主区
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
}
await closeBasketIfVisible(page);
await snap(page, 'scout-review-on');

await browser.close();
console.log('deep done');
