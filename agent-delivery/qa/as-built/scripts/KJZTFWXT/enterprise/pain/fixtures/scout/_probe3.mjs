#!/usr/bin/env node
/** 三次探针：dims 全不选 / 开始分析过程 / 六类型 / 历史恢复 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.resolve(__dirname, '../../../../../../tools/package.json'));
const { chromium } = require('playwright');
const base = 'http://111.198.38.90:50892/';
const outDir = __dirname;
const deep = base + 'enterprise/risk?workspace=pain-points&tab=pain-points';
const out = (n, d) => fs.writeFileSync(path.join(outDir, n), JSON.stringify(d, null, 2));

async function closeBasketIfVisible(page) {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if (!(await close.count())) return;
  if (!(await close.first().isVisible().catch(() => false))) return;
  await close.first().click();
  await page.waitForTimeout(400);
}

async function snap(page, name) {
  const data = await page.evaluate(() => {
    const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 120);
    return {
      url: location.href,
      title: document.title,
      h1: [...document.querySelectorAll('h1')].map(textOf),
      headings: [...document.querySelectorAll('h1,h2,h3,[role=heading]')].slice(0, 40).map(textOf),
      buttons: [...document.querySelectorAll('button,[role=button]')]
        .slice(0, 90)
        .map((el) => ({
          text: textOf(el),
          disabled: !!el.disabled,
          aria: el.getAttribute('aria-label') || '',
        })),
      mainText: (document.querySelector('main.content-shell-layout')?.innerText || document.querySelector('main')?.innerText || '').slice(0, 9000),
      dialogText: [...document.querySelectorAll('.arco-modal,[role=dialog],.arco-drawer')]
        .map((el) => (el.innerText || '').slice(0, 3000))
        .join('\n---\n'),
    };
  });
  fs.writeFileSync(path.join(outDir, `${name}.json`), JSON.stringify(data, null, 2));
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: true }).catch(() => {});
  return data;
}

const mainTxt = (page) =>
  page.locator('main.content-shell-layout').first().innerText().catch(() =>
    page.locator('main').first().innerText().catch(() => ''),
  );

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();

await page.goto(base + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(500);
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const b = page.getByRole('button', { name: /登录/ });
  if (await b.count()) await b.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 25000 });
}

// 回填 1 家
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2500);
await closeBasketIfVisible(page);
await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
await page.waitForTimeout(900);
const sels = page.locator('[aria-label^="选择 "]');
await sels.nth(0).click();
await page.waitForTimeout(300);
await page.getByRole('button', { name: '确定' }).click({ timeout: 8000 });
await page.waitForTimeout(1800);
await closeBasketIfVisible(page);

// 全不选维度
for (const d of ['技术研发', '市场拓展', '融资', '管理']) {
  const box = page.locator('.arco-checkbox').filter({ hasText: d }).first();
  if (!(await box.count())) continue;
  const checked = await box.evaluate((el) => el.classList.contains('arco-checkbox-checked'));
  if (checked) {
    await box.click();
    await page.waitForTimeout(200);
  }
}
await page.waitForTimeout(400);
out('scout-dims-none.json', {
  startDisabled: await page.getByRole('button', { name: '开始分析' }).isDisabled(),
  mainSlice: (await mainTxt(page)).slice(0, 1800),
});
// 勾回技术研发
await page.locator('.arco-checkbox').filter({ hasText: '技术研发' }).first().click();
await page.waitForTimeout(400);
out('scout-dims-one.json', {
  startDisabled: await page.getByRole('button', { name: '开始分析' }).isDisabled(),
});

// 开始分析
const start = page.getByRole('button', { name: '开始分析' });
if (!(await start.isDisabled())) {
  await start.click();
  await page.waitForTimeout(2500);
  await snap(page, 'scout-processing');
  const t0 = Date.now();
  while (Date.now() - t0 < 90000) {
    const u = page.url();
    const t = await mainTxt(page);
    if (/view=result/.test(u)) break;
    if (/创建报告|已识别|分析结果|痛难点识别|问题描述/.test(t) && !/生成中|诊断中|分析中|排队/.test(t)) break;
    if (/失败|错误编号/.test(t)) break;
    await page.waitForTimeout(3000);
  }
  await snap(page, 'scout-result-live');
  console.log('live result url', page.url());
}

// 系统篮六类型
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
const openers = [
  page.locator('button[aria-label*="打开对比篮"]'),
  page.getByRole('button', { name: /对比篮/ }),
];
for (const op of openers) {
  if (await op.count()) {
    await op.first().click().catch(() => {});
    await page.waitForTimeout(800);
    break;
  }
}
await snap(page, 'scout-system-basket');
const ds = page.locator('[aria-label^="选择 "]');
if (await ds.count()) {
  await ds.nth(0).click();
  await page.waitForTimeout(400);
}
const launch = page.getByRole('button', { name: '发起分析' });
out('scout-launch-state.json', {
  count: await launch.count(),
  disabled: await launch.isDisabled().catch(() => null),
});
if ((await launch.count()) && !(await launch.isDisabled())) {
  await launch.click();
  await page.waitForTimeout(1200);
  const modal = await snap(page, 'scout-six-types');
  const types = [
    '重点企业领域分布分析',
    '技术力评估',
    '商业力评估',
    '综合竞争力评估',
    '企业供应链关系分析',
    '企业发展痛点分析',
    '企业发展痛难点分析',
  ];
  const blob = modal.dialogText + '\n' + modal.mainText;
  const hits = Object.fromEntries(types.map((t) => [t, blob.includes(t)]));
  out('scout-six-types-hits.json', { hits, dialog: modal.dialogText.slice(0, 3000) });
  console.log('six types', hits);
}

// 历史恢复
await page.goto(deep + '&view=history', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await snap(page, 'scout-history2');
const restore = page.getByRole('button', { name: '恢复结果' }).first();
if (await restore.count()) {
  await restore.click();
  await page.waitForTimeout(3500);
  const r = await snap(page, 'scout-restored-result');
  out('scout-restored-meta.json', {
    url: r.url,
    headings: r.headings,
    mainSlice: r.mainText.slice(0, 3500),
    hasCreateReport: /创建报告|查看报告|生成中/.test(r.mainText),
    hasScoreLeak: /综合评分|企业排名|推荐指数/.test(r.mainText),
  });
  console.log('restored', r.url, r.headings?.slice(0, 20));
}

await browser.close();
console.log('probe3 done');
