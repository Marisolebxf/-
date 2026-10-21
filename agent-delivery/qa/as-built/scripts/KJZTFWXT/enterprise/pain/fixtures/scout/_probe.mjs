#!/usr/bin/env node
/**
 * 一次性无头探针：先 /login 再深链 pain-points。产物落同目录；勿当 runner。
 * 注意：关闭对比篮仅当 aria-label=关闭对比篮 可见时再点；任务名可能是「痛点」非「痛难点」。
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
  if (!(await close.count())) return false;
  const vis = await close.first().isVisible().catch(() => false);
  if (vis) {
    await close.first().click();
    await page.waitForTimeout(400);
    return true;
  }
  return false;
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
      checkboxes: collect('.arco-checkbox, label, input[type=checkbox]', 50),
      inputs: collect(
        'input, textarea, select, [role=combobox], .arco-select-view, .arco-cascader-view, span.sci-arco-cascader',
      ),
      switches: collect('[role=switch], .arco-switch'),
      sections: collect('section, [aria-label]', 40),
      mainText: (document.querySelector('main')?.innerText || document.body.innerText || '').slice(0, 8000),
    };
  });
  fs.writeFileSync(path.join(outDir, `${name}.json`), JSON.stringify(data, null, 2));
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: true }).catch(() => {});
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

console.log('goto pain…');
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(3500);
const closed0 = await closeBasketIfVisible(page);
console.log('closed basket initially', closed0);

const empty = await snap(page, 'scout-empty');
const dims = ['技术研发', '市场拓展', '融资', '管理'];
const dimHits = {};
for (const d of dims) {
  dimHits[d] = {
    count: await page.getByText(d, { exact: true }).count(),
    visible: await page.getByText(d, { exact: true }).first().isVisible().catch(() => false),
  };
}
const startBtn = page.getByRole('button', { name: '开始分析' });
const gateEmpty = {
  disabled: await startBtn.isDisabled().catch(() => null),
  class: await startBtn.getAttribute('class').catch(() => ''),
  guide: await page.getByText('前往对比篮选择企业').count(),
  guideAlt: await page.getByText(/对比篮选择企业/).count(),
};
fs.writeFileSync(
  path.join(outDir, 'scout-gate.json'),
  JSON.stringify({ url: empty.url, title: empty.title, h1: empty.h1, dimHits, gateEmpty }, null, 2),
);
console.log('empty', empty.url, empty.h1, gateEmpty, dimHits);

// 最近分析
const recentTab = page.locator('main [role=tab], main button').filter({ hasText: '最近分析' });
if (await recentTab.count()) {
  await recentTab.first().click();
  await page.waitForTimeout(1500);
  await closeBasketIfVisible(page);
  await snap(page, 'scout-recent');
  console.log('recent snapped', page.url());
  const cur = page.locator('main [role=tab], main button').filter({ hasText: '当前分析' });
  if (await cur.count()) {
    await cur.first().click();
    await page.waitForTimeout(800);
  }
}

// 对比篮浮层：发起分析路径（用例 01073~01075）
await closeBasketIfVisible(page);
const cta = page.getByRole('button', { name: /前往对比篮选择企业/ });
if (await cta.count()) {
  await cta.first().click();
  await page.waitForTimeout(1200);
  await snap(page, 'scout-overlay');
  const launchDisabled = await page.getByRole('button', { name: '发起分析' }).isDisabled().catch(() => null);
  const sels = page.locator('[aria-label^="选择 "]');
  const n = await sels.count();
  console.log('overlay selectable', n, 'launchDisabled', launchDisabled);
  if (n >= 1) {
    await sels.nth(0).click();
    await page.waitForTimeout(400);
    const launchAfter = await page.getByRole('button', { name: '发起分析' }).isDisabled().catch(() => null);
    console.log('launchAfterSelect', launchAfter);
    await page.getByRole('button', { name: '发起分析' }).click({ timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(1200);
    await snap(page, 'scout-type-modal');
    // 六类型：企业发展痛点分析（非痛难点）
    const painOpt = page.getByText('企业发展痛点分析', { exact: true });
    const painOptAlt = page.getByText(/企业发展痛难点分析|企业发展痛点分析/);
    const types = [
      '重点企业领域分布分析',
      '技术力评估',
      '商业力评估',
      '综合竞争力评估',
      '企业供应链关系分析',
      '企业发展痛点分析',
    ];
    const typeHits = {};
    for (const t of types) {
      typeHits[t] = await page.getByText(t, { exact: true }).count();
    }
    fs.writeFileSync(path.join(outDir, 'scout-types.json'), JSON.stringify({ typeHits }, null, 2));
    console.log('typeHits', typeHits);
    if (await painOpt.count()) {
      await painOpt.first().click();
      await page.waitForTimeout(400);
    } else if (await painOptAlt.count()) {
      await painOptAlt.first().click();
      await page.waitForTimeout(400);
    }
    const submit = page.getByRole('button', { name: /下一步|确定|提交|开始/ });
    if (await submit.count()) {
      await submit.first().click();
      await page.waitForTimeout(2500);
    }
    await closeBasketIfVisible(page);
    await snap(page, 'scout-after-select');
    console.log('after-select', page.url());
  }
}

// 勾选诊断维度 + 开始分析
await closeBasketIfVisible(page);
const dimLabels = page.locator('.arco-checkbox, label').filter({ hasText: /技术研发|市场拓展|融资|管理/ });
console.log('dimLabels', await dimLabels.count());
// 确保至少一项勾选
const tech = page.getByText('技术研发', { exact: true }).first();
if (await tech.count()) {
  await tech.click().catch(() => {});
  await page.waitForTimeout(300);
}
const startEnabled = !(await startBtn.isDisabled().catch(() => true));
console.log('startEnabled', startEnabled, 'url', page.url());
fs.writeFileSync(
  path.join(outDir, 'scout-start-gate.json'),
  JSON.stringify(
    {
      url: page.url(),
      startEnabled,
      startDisabled: await startBtn.isDisabled().catch(() => null),
      mainSlice: (await page.locator('main').first().innerText().catch(() => '')).slice(0, 2500),
      hasObject: /来自对比篮|管理全部对象|返回对比篮/.test(
        await page.locator('main').first().innerText().catch(() => ''),
      ),
    },
    null,
    2,
  ),
);

if (startEnabled) {
  await startBtn.click();
  await page.waitForTimeout(2500);
  await snap(page, 'scout-processing');
  console.log('processing', page.url());
  const startTs = Date.now();
  let done = false;
  while (Date.now() - startTs < 90000) {
    const u = page.url();
    const t = await page.locator('main').first().innerText().catch(() => '');
    if (/view=result|分析结果|创建报告|痛难点识别|已识别/.test(u + t) && !/生成中|诊断中|分析中/.test(t)) {
      done = true;
      break;
    }
    if (/失败|错误编号/.test(t)) break;
    await page.waitForTimeout(3000);
  }
  await snap(page, 'scout-result');
  console.log('result done?', done, page.url());
}

// 供应链隔离探测（只记 observed）
await page.goto(base + 'enterprise/risk?workspace=supply-chain&tab=supply-chain', {
  waitUntil: 'domcontentloaded',
  timeout: 60000,
});
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await snap(page, 'scout-supply-sibling');
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await snap(page, 'scout-back-pain');

await browser.close();
console.log('done →', outDir);
