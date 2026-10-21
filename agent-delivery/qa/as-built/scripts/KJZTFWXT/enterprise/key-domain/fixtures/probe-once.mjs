#!/usr/bin/env node
/** 一次性二次探测：登录后抓领域分析空态/结果态 locator。产出落 fixtures/scout/ */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.join(__dirname, 'scout');
const base = 'http://10.50.69.111:30892/';
fs.mkdirSync(outDir, { recursive: true });

async function login(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function snap(page, name) {
  const data = await page.evaluate(() => {
    const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 120);
    const collect = (sel, limit = 50) =>
      [...document.querySelectorAll(sel)].slice(0, limit).map((el) => ({
        tag: el.tagName.toLowerCase(),
        text: textOf(el),
        attrs: (() => {
          const o = {};
          for (const n of ['id', 'name', 'placeholder', 'aria-label', 'role', 'type', 'title']) {
            if (el.getAttribute(n)) o[n] = el.getAttribute(n).slice(0, 160);
          }
          if (el.className && typeof el.className === 'string') o.class = el.className.slice(0, 160);
          return o;
        })(),
      }));
    return {
      url: location.href,
      title: document.title,
      h1: [...document.querySelectorAll('h1')].map(textOf),
      headings: [...document.querySelectorAll('h1,h2,h3,[role=heading]')].slice(0, 40).map(textOf),
      buttons: collect('button, [role=button], .arco-btn'),
      textboxes: collect('input, textarea, [role=textbox], .arco-select-view, .arco-input, span.sci-arco-cascader'),
      switches: collect('[role=switch], .arco-switch'),
      menus: collect('[role=menuitem], .arco-menu-item'),
      sections: collect('section, [aria-label]', 40),
      mainText: (document.querySelector('main')?.innerText || '').slice(0, 2500),
    };
  });
  fs.writeFileSync(path.join(outDir, `${name}.json`), JSON.stringify(data, null, 2));
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: true });
  return data;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const target = `${base}enterprise/key-enterprise-analysis?view=domain`;
console.log('goto', target);
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
console.log('after goto', page.url());
await login(page);
console.log('after login', page.url());
if (!page.url().includes('key-enterprise-analysis')) {
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await login(page);
}
await page.waitForTimeout(3000);
const empty = await snap(page, 'scout-empty');
console.log('empty title', empty.title, 'h1', empty.h1);
console.log('empty headings', empty.headings);
console.log('empty buttons sample', empty.buttons.slice(0, 20).map((b) => b.text));
console.log('mainText head:\n', empty.mainText.slice(0, 800));

// 尝试对比篮发起结果态（若有残留企业）
const basketBtn = page.getByRole('button', { name: /对比篮/ }).first();
if (await basketBtn.count()) {
  try {
    await basketBtn.click({ timeout: 5000 });
    await page.waitForTimeout(1500);
    await snap(page, 'scout-basket');
    const start = page.getByRole('button', { name: /发起分析/ }).first();
    if (await start.count() && !(await start.isDisabled().catch(() => true))) {
      await start.click();
      await page.waitForTimeout(1000);
      const domainOpt = page.getByText('重点企业领域分布分析', { exact: false }).first();
      if (await domainOpt.count()) {
        await domainOpt.click();
        await page.waitForTimeout(500);
        const next = page.getByRole('button', { name: /下一步/ }).first();
        if (await next.count() && !(await next.isDisabled().catch(() => true))) {
          await next.click();
          await page.waitForTimeout(3500);
          const result = await snap(page, 'scout-result');
          console.log('result url', result.url);
          console.log('result headings', result.headings);
          console.log('result buttons', result.buttons.slice(0, 25).map((b) => b.text));
          console.log('result mainText head:\n', result.mainText.slice(0, 1200));
        } else {
          console.log('下一步不可点或缺失');
        }
      } else {
        console.log('无「重点企业领域分布分析」选项');
      }
    } else {
      console.log('发起分析不可用（可能无勾选企业）');
    }
  } catch (e) {
    console.log('basket probe err', e.message);
  }
} else {
  console.log('无对比篮按钮');
}

// 侧栏菜单探测
const menus = empty.menus.map((m) => m.text).filter(Boolean);
console.log('menus containing 重点', menus.filter((t) => /重点|领域|类型/.test(t)));

await browser.close();
console.log('probe done →', outDir);
