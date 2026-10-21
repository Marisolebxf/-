#!/usr/bin/env node
/**
 * 二次探针：页内确定回填 / 系统篮六类型 / 开始分析 / 历史恢复。勿当 runner。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');
const base = 'http://10.50.69.111:30892/';
const outDir = __dirname;
const deep = base + 'enterprise/risk?workspace=pain-points&tab=pain-points';

async function closeBasketIfVisible(page) {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if (!(await close.count())) return { tried: false, closed: false };
  const vis = await close.first().isVisible().catch(() => false);
  if (!vis) return { tried: false, closed: false, reason: 'not-visible' };
  await close.first().click();
  await page.waitForTimeout(500);
  return { tried: true, closed: true };
}

async function snap(page, name) {
  const data = await page.evaluate(() => {
    const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 120);
    return {
      url: location.href,
      title: document.title,
      h1: [...document.querySelectorAll('h1')].map(textOf),
      headings: [...document.querySelectorAll('h1,h2,h3,[role=heading]')].slice(0, 40).map(textOf),
      buttons: [...document.querySelectorAll('button, [role=button]')]
        .slice(0, 80)
        .map((el) => ({
          text: textOf(el),
          disabled: !!el.disabled,
          aria: el.getAttribute('aria-label') || '',
          class: (el.className || '').toString().slice(0, 100),
        })),
      mainText: (document.querySelector('main')?.innerText || '').slice(0, 8000),
      dialogText: [...document.querySelectorAll('.arco-modal, [role=dialog], .arco-drawer')]
        .map((el) => (el.innerText || '').slice(0, 2000))
        .join('\n---\n'),
    };
  });
  fs.writeFileSync(path.join(outDir, `${name}.json`), JSON.stringify(data, null, 2));
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: true }).catch(() => {});
  return data;
}

const out = (name, data) => fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2));

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

await page.goto(base + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(600);
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 25000 });
}

await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(3000);
const closeInfo = await closeBasketIfVisible(page);
out('scout-close-info.json', closeInfo);

// —— A. 页内「选择分析企业」确定回填 ——
await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
await page.waitForTimeout(1000);
const overlay = await snap(page, 'scout-select-overlay');
const sels = page.locator('[aria-label^="选择 "]');
const n = await sels.count();
if (n < 1) throw new Error('no selectable enterprises');
await sels.nth(0).click();
await page.waitForTimeout(300);
const confirm = page.getByRole('button', { name: '确定' });
await expectEnabledClick(page, confirm);
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
const after = await snap(page, 'scout-after-confirm');
out('scout-after-confirm-meta.json', {
  url: after.url,
  hasSource: /source=compare-basket|enterprise_codes/.test(after.url),
  mainSlice: after.mainText.slice(0, 2000),
  startDisabled: after.buttons.find((b) => b.text === '开始分析')?.disabled,
  dimChecked: ['技术研发', '市场拓展', '融资', '管理'].map((d) => ({
    d,
    inText: after.mainText.includes(d),
  })),
});

// 诊断范围勾选态
const checks = await page.evaluate(() =>
  [...document.querySelectorAll('.arco-checkbox')].map((el) => ({
    text: (el.innerText || el.textContent || '').trim().slice(0, 40),
    checked: el.classList.contains('arco-checkbox-checked') || !!el.querySelector('.arco-checkbox-checked'),
    aria: el.getAttribute('aria-checked'),
  })),
);
out('scout-dims-state.json', checks);

// 全不选探测
for (const d of ['技术研发', '市场拓展', '融资', '管理']) {
  const box = page.locator('.arco-checkbox').filter({ hasText: d }).first();
  if (await box.count()) {
    const checked = await box.evaluate(
      (el) => el.classList.contains('arco-checkbox-checked') || !!el.querySelector('input:checked'),
    );
    if (checked) {
      await box.click();
      await page.waitForTimeout(200);
    }
  }
}
await page.waitForTimeout(400);
const mainText = async () =>
  page.locator('main.content-shell-layout, main').first().innerText().catch(() => '');
out('scout-dims-none.json', {
  startDisabled: await page.getByRole('button', { name: '开始分析' }).isDisabled(),
  mainSlice: (await mainText()).slice(0, 1500),
});
// 恢复勾选 技术研发
const tech = page.locator('.arco-checkbox').filter({ hasText: '技术研发' }).first();
if (await tech.count()) await tech.click();
await page.waitForTimeout(400);

const startBtn = page.getByRole('button', { name: '开始分析' });
const canStart = !(await startBtn.isDisabled());
out('scout-can-start.json', { canStart, url: page.url() });

if (canStart) {
  await startBtn.click();
  await page.waitForTimeout(2500);
  await snap(page, 'scout-processing');
  const t0 = Date.now();
  while (Date.now() - t0 < 90000) {
    const u = page.url();
    const t = await mainText();
    if (/view=result/.test(u)) break;
    if (/创建报告|痛点|已识别|分析结果/.test(t) && !/生成中|诊断中|分析中|排队/.test(t)) break;
    if (/失败|错误编号/.test(t) && /view=/.test(u)) break;
    await page.waitForTimeout(3000);
  }
  await snap(page, 'scout-result-live');
}

// —— B. 系统对比篮 → 发起分析 → 六类型 ——
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
const openDock = page.locator('button[aria-label*="打开对比篮"], button[aria-label*="对比篮"]');
if (await openDock.count()) {
  await openDock.first().click();
  await page.waitForTimeout(1000);
} else {
  // 若浮层已在，继续
}
await snap(page, 'scout-system-basket');
const dockSels = page.locator('[aria-label^="选择 "]');
if (await dockSels.count()) {
  await dockSels.nth(0).click();
  await page.waitForTimeout(400);
}
const launch = page.getByRole('button', { name: '发起分析' });
out('scout-launch-state.json', {
  disabled: await launch.isDisabled().catch(() => null),
  count: await launch.count(),
});
if (await launch.count() && !(await launch.isDisabled())) {
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
  const hits = {};
  for (const t of types) hits[t] = (modal.dialogText + modal.mainText).includes(t);
  out('scout-six-types-hits.json', { hits, dialog: modal.dialogText.slice(0, 2500) });
  const pain = page.getByText('企业发展痛点分析', { exact: true });
  if (await pain.count()) {
    await pain.first().click();
    await page.waitForTimeout(400);
    const next = page.getByRole('button', { name: /下一步|确定/ });
    if (await next.count() && !(await next.first().isDisabled())) {
      await next.first().click();
      await page.waitForTimeout(2500);
    }
  }
  await snap(page, 'scout-after-six-type');
}

// —— C. 最近分析恢复已完成任务（结果态） ——
await page.goto(deep + '&view=history', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await snap(page, 'scout-history');
const restore = page.getByRole('button', { name: '恢复结果' }).first();
if (await restore.count()) {
  await restore.click();
  await page.waitForTimeout(3000);
  await snap(page, 'scout-restored-result');
}

await browser.close();
console.log('probe2 done');

async function expectEnabledClick(page, loc) {
  await page.waitForTimeout(200);
  if (await loc.isDisabled()) {
    // 再点一次选择
    const sels = page.locator('[aria-label^="选择 "]');
    if (await sels.count()) await sels.nth(0).click();
    await page.waitForTimeout(400);
  }
  await loc.click({ timeout: 10000 });
}
