#!/usr/bin/env node
/**
 * 一次性无头探针：先 /login 再深链。产物落同目录 scout.*；勿当 runner。
 * 对比篮关闭钮可能不可见——可见再点。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(
  path.resolve(__dirname, '../../../../../../tools/package.json'),
);
const { chromium } = require('playwright');
const base = 'http://111.198.38.90:50892/';
const outDir = __dirname;
const deep =
  base + 'enterprise/attraction?workspace=cultivation&recommendation_tab=cultivation';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();

await page.goto(base + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(800);
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(4000);

const closeBasket = page.locator('[aria-label="关闭对比篮"]');
if (await closeBasket.count()) {
  const vis = await closeBasket.first().isVisible().catch(() => false);
  if (vis) {
    await closeBasket.first().click();
    await page.waitForTimeout(400);
  }
}

const snapshot = await page.evaluate(() => {
  const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 100);
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
          'aria-selected',
          'role',
          'type',
          'title',
          'disabled',
        ]) {
          if (el.getAttribute(n)) o[n] = el.getAttribute(n).slice(0, 160);
        }
        if (el.className && typeof el.className === 'string') o.class = el.className.slice(0, 140);
        if (el.disabled) o.disabled = true;
        return o;
      })(),
    }));
  return {
    url: location.href,
    title: document.title,
    h1: [...document.querySelectorAll('h1')].map(textOf),
    headings: [...document.querySelectorAll('h1,h2,h3,[role=heading]')].slice(0, 40).map(textOf),
    tabs: collect('[role=tab]'),
    buttons: collect('button, [role=button]'),
    inputs: collect('input, textarea, select, .arco-select-view, .sci-arco-cascader, .arco-select'),
    tags: collect('.arco-tag'),
    listitems: collect('[role=listitem], .arco-list-item, li'),
    switches: collect('[role=switch], .arco-switch'),
    mainText: (document.querySelector('main')?.innerText || '').slice(0, 2500),
  };
});

fs.writeFileSync(path.join(outDir, 'scout.json'), JSON.stringify(snapshot, null, 2));
const md = [
  '# scout · ent-cultivate',
  '',
  '> 先 /login 再深链；2026-10-14 headless',
  '',
  `- url: ${snapshot.url}`,
  `- title: ${snapshot.title}`,
  `- h1: ${JSON.stringify(snapshot.h1)}`,
  '',
  '## headings',
  ...snapshot.headings.map((h) => `- ${h}`),
  '',
  '## tabs',
  ...snapshot.tabs.map((t) => `- ${JSON.stringify(t)}`),
  '',
  '## buttons',
  ...snapshot.buttons.map((b) => `- ${JSON.stringify(b)}`),
  '',
  '## inputs',
  ...snapshot.inputs.map((i) => `- ${JSON.stringify(i)}`),
  '',
  '## tags',
  ...snapshot.tags.map((t) => `- ${JSON.stringify(t)}`),
  '',
  '## listitems',
  ...snapshot.listitems.map((t) => `- ${JSON.stringify(t)}`),
  '',
  '## switches',
  ...snapshot.switches.map((t) => `- ${JSON.stringify(t)}`),
  '',
  '## mainText (slice)',
  '```',
  snapshot.mainText,
  '```',
  '',
].join('\n');
fs.writeFileSync(path.join(outDir, 'scout.md'), md);
await page.screenshot({ path: path.join(outDir, 'page.png'), fullPage: false });
await browser.close();
console.log('scout ok →', outDir);
