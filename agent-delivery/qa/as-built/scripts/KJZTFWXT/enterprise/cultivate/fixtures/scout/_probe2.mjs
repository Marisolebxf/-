#!/usr/bin/env node
/**
 * 二次无头探测：关篮→条件/快捷标签/门控/Tab/分析流。产物 scout-*.json
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
const deep =
  base + 'enterprise/attraction?workspace=cultivation&recommendation_tab=cultivation';
const out = (name, data) =>
  fs.writeFileSync(path.join(__dirname, name), JSON.stringify(data, null, 2));

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();

await page.goto(base + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(600);
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(3500);

// 对比篮关闭：可见再点
const closeB = page.locator('[aria-label="关闭对比篮"]');
if (await closeB.count()) {
  const vis = await closeB.first().isVisible().catch(() => false);
  if (vis) {
    await closeB.first().click();
    await page.waitForTimeout(500);
  }
}

const chips = [
  '集成电路',
  '生物医药',
  '人工智能',
  '新能源',
  '低空经济',
  '量子信息',
  '海洋经济',
  '智能机器人',
];
const chipHits = {};
for (const c of chips) {
  const loc = page.getByText(c, { exact: true });
  chipHits[c] = {
    count: await loc.count(),
    visible: await loc.first().isVisible().catch(() => false),
    tag: await loc
      .first()
      .evaluate((el) => el.tagName + '.' + (el.className || '').toString().slice(0, 80))
      .catch(() => null),
  };
}

const startBtn = page.getByRole('button', { name: '开始分析' });
const gate0 = {
  disabled: await startBtn.isDisabled(),
  text: await startBtn.innerText().catch(() => ''),
};

// 产业类别下拉
const indTrigger = page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="全部产业类别"]') }).first();
await indTrigger.click({ timeout: 8000 }).catch(() => {});
await page.waitForTimeout(600);
const indOptions = await page
  .locator('.arco-trigger-popup:visible .arco-select-option, .arco-trigger-popup:visible li')
  .allTextContents()
  .catch(() => []);
await page.keyboard.press('Escape').catch(() => {});
await page.waitForTimeout(300);

// 政策导向下拉
const polTrigger = page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="全部政策导向"]') }).first();
await polTrigger.click({ timeout: 8000 }).catch(() => {});
await page.waitForTimeout(600);
const polPopupVisible = await page.locator('.arco-trigger-popup:visible').count();
const polOptions = await page
  .locator('.arco-trigger-popup:visible .arco-select-option, .arco-trigger-popup:visible li')
  .allTextContents()
  .catch(() => []);
const polEmpty = polOptions.map((t) => t.trim()).filter(Boolean);
await page.keyboard.press('Escape').catch(() => {});
await page.waitForTimeout(300);

// 企业规模下拉
const sizeTrigger = page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="全部企业规模"]') }).first();
await sizeTrigger.click({ timeout: 8000 }).catch(() => {});
await page.waitForTimeout(600);
const sizeOptions = await page
  .locator('.arco-trigger-popup:visible .arco-select-option, .arco-trigger-popup:visible li')
  .allTextContents()
  .catch(() => []);
// 选中型
const mid = page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '中型' }).first();
if (await mid.count()) await mid.click();
await page.waitForTimeout(800);

const gate1 = {
  disabled: await startBtn.isDisabled(),
  sizeEcho: await page.locator('input[placeholder="全部企业规模"]').inputValue().catch(() => ''),
  sizeViewText: await sizeTrigger.innerText().catch(() => ''),
};

// 点快捷标签「人工智能」（若可见）
const ai = page.getByText('人工智能', { exact: true }).first();
let chipClick = null;
if (await ai.isVisible().catch(() => false)) {
  await ai.click();
  await page.waitForTimeout(600);
  chipClick = {
    afterDisabled: await startBtn.isDisabled(),
    mainSlice: (await page.getByTestId('recruit-tab-stack').innerText()).slice(0, 800),
  };
}

out('scout-gate.json', {
  chipHits,
  indOptions: indOptions.map((t) => t.trim()).filter(Boolean),
  polOptions: polEmpty,
  polPopupVisible,
  sizeOptions: sizeOptions.map((t) => t.trim()).filter(Boolean),
  gate0,
  gate1,
  chipClick,
  url: page.url(),
});

// Tab 候选工作台
await page.getByRole('tab', { name: '候选工作台' }).click();
await page.waitForTimeout(1200);
const main = () => page.getByTestId('recruit-tab-stack');
const candText = (await main().innerText()).slice(0, 1500);
out('scout-candidate.json', { url: page.url(), candText });

// Tab 最近分析
await page.getByRole('tab', { name: '最近分析' }).click();
await page.waitForTimeout(1200);
const recentText = (await main().innerText()).slice(0, 1500);
out('scout-recent.json', { url: page.url(), recentText });

// 回条件筛选推荐 → 选产业 → 开始分析
await page.getByRole('tab', { name: '条件筛选推荐' }).click();
await page.waitForTimeout(800);
await indTrigger.click({ timeout: 8000 });
await page.waitForTimeout(400);
const aiOpt = page
  .locator('.arco-trigger-popup:visible .arco-select-option')
  .filter({ hasText: '人工智能' })
  .first();
if (await aiOpt.count()) await aiOpt.click();
else {
  const opt = page.locator('.arco-trigger-popup:visible .arco-select-option').first();
  if (await opt.count()) await opt.click();
}
await page.waitForTimeout(800);
const beforeStart = {
  disabled: await startBtn.isDisabled(),
  main: (await main().innerText()).slice(0, 800),
};
if (!(await startBtn.isDisabled())) {
  await startBtn.click();
  await page.waitForTimeout(2500);
}
const afterStart = {
  url: page.url(),
  main: (await main().innerText()).slice(0, 2000),
  startDisabled: await startBtn.isDisabled().catch(() => null),
};
// 等成功（最多 60s）
let successHit = false;
const t0 = Date.now();
while (Date.now() - t0 < 60000) {
  const t = await main().innerText();
  if (/培育推荐指数|建议培育|排名/.test(t) || (/成功/.test(t) && !/分析中/.test(t))) {
    successHit = true;
    out('scout-result.json', { elapsedMs: Date.now() - t0, main: t.slice(0, 4000), url: page.url() });
    // 点首行详情（若有）
    const row = page.getByTestId('recruit-tab-stack').locator('tr, .arco-table-tr, [class*=result-row]').nth(1);
    if (await row.count()) {
      await row.click({ timeout: 5000 }).catch(() => {});
      await page.waitForTimeout(1500);
      out('scout-detail.json', {
        drawer: (await page.locator('.arco-drawer').innerText().catch(() => '')).slice(0, 2000),
        bodyExtra: (await page.locator('body').innerText()).slice(0, 500),
      });
    }
    // ⓘ
    const info = page.locator('[aria-label="指标说明：培育推荐指数"]').first();
    if (await info.count()) {
      await info.click();
      await page.waitForTimeout(800);
      out('scout-metric.json', {
        popup: (
          await page.locator('.arco-popover, .arco-trigger-popup:visible, [class*=MetricSpec]').first().innerText().catch(() => '')
        ).slice(0, 1500),
        body: (await page.locator('body').innerText()).slice(0, 800),
      });
    }
    break;
  }
  if (/空结果|无匹配企业|失败/.test(t) && !/分析中/.test(t)) {
    out('scout-result.json', {
      elapsedMs: Date.now() - t0,
      main: t.slice(0, 4000),
      url: page.url(),
      emptyOrFail: true,
    });
    break;
  }
  await page.waitForTimeout(2000);
}
if (!successHit && !fs.existsSync(path.join(__dirname, 'scout-result.json'))) {
  out('scout-result.json', {
    elapsedMs: Date.now() - t0,
    main: (await main().innerText()).slice(0, 4000),
    url: page.url(),
    timeout: true,
  });
}
out('scout-analyze.json', { beforeStart, afterStart });

await page.screenshot({ path: path.join(__dirname, 'page-after.png'), fullPage: false });
await browser.close();
console.log('probe2 ok');
