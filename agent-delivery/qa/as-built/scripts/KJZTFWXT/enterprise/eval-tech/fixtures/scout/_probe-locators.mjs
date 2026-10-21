#!/usr/bin/env node
/** 无头二次实勘：关闭对比篮可点性 + 空态/模板/五维/开始分析 locator */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://10.50.69.111:30892/';
const target =
  'enterprise/evaluation?workspace=technology&mode=technology';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

await page.goto(base + target, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);

const close = page.locator('button[aria-label="关闭对比篮"]');
const closeInfo = {
  count: await close.count(),
  visible: false,
  enabled: false,
  box: null,
  click_safe: 'skipped',
};
if (closeInfo.count) {
  closeInfo.visible = await close.first().isVisible().catch(() => false);
  closeInfo.enabled = await close.first().isEnabled().catch(() => false);
  closeInfo.box = await close.first().boundingBox().catch(() => null);
  try {
    await close.first().click({ timeout: 1500 });
    await page.waitForTimeout(400);
    closeInfo.click_safe = 'ok';
  } catch (e) {
    closeInfo.click_safe = 'fail:' + String(e.message || e).slice(0, 120);
    await page.keyboard.press('Escape').catch(() => {});
  }
}

const out = {
  surveyed_at: new Date().toISOString(),
  url: page.url(),
  close: closeInfo,
  close_after: {
    count: await close.count(),
    visible: await close.first().isVisible().catch(() => false),
  },
  cta: {
    count: await page.getByRole('button', { name: '前往对比篮选择企业' }).count(),
    visible: await page
      .getByRole('button', { name: '前往对比篮选择企业' })
      .isVisible()
      .catch(() => false),
  },
  start: {
    visible: await page.getByRole('button', { name: '开始分析' }).isVisible().catch(() => false),
    disabled: await page.getByRole('button', { name: '开始分析' }).isDisabled().catch(() => null),
  },
  template_select: {
    count: await page.locator('.arco-select-view').filter({ hasText: /技术力|模板|未保存/ }).count(),
    text: await page
      .locator('.arco-select-view')
      .filter({ hasText: /技术力|模板|未保存/ })
      .first()
      .innerText()
      .catch(() => ''),
  },
  metrics: {},
  empty_hint: await page.getByText(/对比篮选择企业/).first().isVisible().catch(() => false),
};

for (const n of ['技术人才', '技术创新', '技术转化', '技术合作', '技术投入']) {
  out.metrics[n] = await page.getByText(n, { exact: true }).first().isVisible().catch(() => false);
}
out.spins = await page.locator('[role=spinbutton]').count();
out.weight_sum = await page.getByText(/权重合计：100%/).first().isVisible().catch(() => false);

// 打开浮层
let overlay = { opened: false };
try {
  await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 5000 });
  await page.waitForTimeout(800);
  overlay = {
    opened: await page.getByText('选择分析企业', { exact: true }).first().isVisible().catch(() => false),
    subtitle_pick: await page.getByText(/从对比篮勾选/).first().isVisible().catch(() => false),
    subtitle_no_task: await page.getByText(/不会发起分析任务/).first().isVisible().catch(() => false),
    tab_ent: await page.getByRole('tab', { name: /企业/ }).first().isVisible().catch(() => false),
    search: await page.getByPlaceholder('按企业名称搜索').isVisible().catch(() => false),
    type_filter: await page.getByText('全部企业类型').first().isVisible().catch(() => false),
    select_n: await page.locator('[aria-label^="选择 "]').count(),
    view_profile: await page.getByRole('button', { name: '查看画像' }).first().isVisible().catch(() => false),
    remove: await page.locator('[aria-label="移除"]').first().isVisible().catch(() => false),
  };
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(300);
} catch (e) {
  overlay.error = String(e.message || e).slice(0, 200);
}

// 模板下拉
let template = { opened: false };
try {
  const close2 = page.locator('button[aria-label="关闭对比篮"]');
  if (await close2.count()) {
    try {
      await close2.first().click({ timeout: 1500 });
    } catch {}
  }
  const trg = page.locator('.arco-select-view').filter({ hasText: /技术力|模板|未保存/ }).first();
  await trg.click({ timeout: 5000 });
  await page.waitForTimeout(500);
  const pop = page.locator('.arco-trigger-popup:visible').last();
  const txt = await pop.innerText();
  template = {
    opened: true,
    groups: ['系统模板', '我的模板', '当次自定义配置'].map((g) => ({ g, ok: txt.includes(g) })),
    std: txt.includes('技术力标准模板'),
    unsaved: txt.includes('当前未保存配置'),
    sample: txt.slice(0, 300),
  };
  await page.keyboard.press('Escape');
} catch (e) {
  template.error = String(e.message || e).slice(0, 200);
}

out.overlay = overlay;
out.template = template;

const jsonPath = path.join(__dirname, 'scout-r4-locators.json');
fs.writeFileSync(jsonPath, JSON.stringify(out, null, 2), 'utf8');
await page.screenshot({ path: path.join(__dirname, 'scout-r4.png'), fullPage: true });
console.log(JSON.stringify(out, null, 2));
await browser.close();
