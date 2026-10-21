#!/usr/bin/env node
/** 四次：报告创建 / 评审开关 / 多对象摘要 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.resolve(__dirname, '../../../../../../tools/package.json'));
const { chromium } = require('playwright');
const base = 'http://10.50.69.111:30892/';
const outDir = __dirname;
const deep = base + 'enterprise/risk?workspace=pain-points&tab=pain-points';
const out = (n, d) => fs.writeFileSync(path.join(outDir, n), JSON.stringify(d, null, 2));

async function login(page) {
  await page.goto(base + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(500);
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const b = page.getByRole('button', { name: /登录/ });
  if (await b.count()) await b.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 25000 });
}

async function closeBasketIfVisible(page) {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if (!(await close.count())) return;
  if (!(await close.first().isVisible().catch(() => false))) return;
  await close.first().click();
  await page.waitForTimeout(400);
}

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
await login(page);

// 恢复结果 → 创建报告
await page.goto(deep + '&view=history', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await page.getByRole('button', { name: '恢复结果' }).first().click();
await page.waitForTimeout(3000);
const before = await page.locator('main.content-shell-layout').innerText();
const create = page.getByRole('button', { name: /创建报告/ });
out('scout-report-before.json', {
  hasCreate: await create.count(),
  createDisabled: await create.first().isDisabled().catch(() => null),
  slice: before.slice(0, 2000),
});
if (await create.count()) {
  await create.first().click();
  await page.waitForTimeout(4000);
  const t0 = Date.now();
  while (Date.now() - t0 < 60000) {
    const t = await page.locator('main.content-shell-layout').innerText();
    if (/问题描述|成因分析|行业最佳实践|解决方案|查看报告|生成中|生成失败/.test(t)) break;
    await page.waitForTimeout(2000);
  }
  const after = await page.locator('main.content-shell-layout').innerText();
  out('scout-report-after.json', {
    url: page.url(),
    slice: after.slice(0, 4500),
    hasFour: ['问题描述', '成因分析', '行业最佳实践', '解决方案'].map((s) => ({
      s,
      hit: after.includes(s),
    })),
  });
}

// 多对象回填 ≥6
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
await page.waitForTimeout(900);
const sels = page.locator('[aria-label^="选择 "]');
const n = Math.min(await sels.count(), 6);
for (let i = 0; i < n; i++) {
  await sels.nth(i).click();
  await page.waitForTimeout(150);
}
await page.getByRole('button', { name: '确定' }).click({ timeout: 8000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
const multi = await page.locator('main.content-shell-layout').innerText();
out('scout-multi6.json', {
  url: page.url(),
  n,
  slice: multi.slice(0, 2500),
  hasManage: /管理全部对象/.test(multi),
  hasReturn: /返回对比篮调整对象/.test(multi),
});

// 评审模式
await page.goto(deep, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);
await closeBasketIfVisible(page);
await page.locator('button.persona-switch, [class*=persona-switch]').first().click();
await page.waitForTimeout(600);
const sw = page.locator('[aria-label="内部评审模式"]');
out('scout-review-switch.json', {
  switchCount: await sw.count(),
  checked: await sw.getAttribute('aria-checked').catch(() => null),
});
if (await sw.count()) {
  const on = (await sw.getAttribute('aria-checked')) === 'true';
  if (!on) await sw.click();
  await page.waitForTimeout(800);
  // 关菜单再看主区
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(400);
  const tOn = await page.locator('main.content-shell-layout').innerText();
  out('scout-review-on.json', {
    hasRiskTrace: await page.locator('[aria-label="风险洞察需求追溯"]').count(),
    hasDimTrace: await page.locator('[aria-label="诊断范围需求追溯"]').count(),
    slice: tOn.slice(0, 1200),
  });
  await page.locator('button.persona-switch, [class*=persona-switch]').first().click();
  await page.waitForTimeout(400);
  if ((await sw.getAttribute('aria-checked')) === 'true') await sw.click();
  await page.waitForTimeout(600);
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(400);
  out('scout-review-off.json', {
    hasRiskTraceVisible: await page.locator('[aria-label="风险洞察需求追溯"]').first().isVisible().catch(() => false),
    hasDimTraceVisible: await page.locator('[aria-label="诊断范围需求追溯"]').first().isVisible().catch(() => false),
  });
}

await browser.close();
console.log('probe4 done');
