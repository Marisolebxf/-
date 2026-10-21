#!/usr/bin/env node
/**
 * 一次性无头探针（P0-05 写稿用）：权重调节钮方向/步长 · 直改 30 · 停用「标准制定」· 重新启用回显。
 * 产物落同目录 scout-p005.json / scout-p005.png；勿当 runner。只动权重/启停，不点「开始评估」。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const target = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;
const outDir = __dirname;

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function closeBasket(page) {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

const mainLoc = (page) => page.locator('main').first();
const mainText = (page) => mainLoc(page).innerText().catch(() => '');
const sumLine = (page) => mainText(page).then((t) => (t.match(/权重合计：[^\n]*/) || [''])[0]);

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const out = { probed_at: new Date().toISOString(), path: '/service/institution-judgment?workspace=capability&tab=capability', steps: {} };
const dump = () => fs.writeFileSync(path.join(outDir, 'scout-p005.json'), JSON.stringify(out, null, 2));

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  await closeBasket(page);
  await page.waitForTimeout(500);

  const spins = page.locator('[role=spinbutton]');
  const spinCount = await spins.count();
  const stepBtns = page.locator('.arco-input-number-step-button');
  const stepCount = await stepBtns.count();
  const rows = await page.evaluate(() => {
    const names = ['专利数量', '研发投入', '核心专家', '成功案例', '标准制定'];
    return names.map((name) => {
      const label = [...document.querySelectorAll('main *')].find((el) => el.children.length === 0 && (el.innerText || '').trim() === name);
      let row = label;
      while (row && !row.querySelector('[role=spinbutton]')) row = row.parentElement;
      const cb = row?.querySelector('input[type=checkbox]');
      return {
        name,
        checkbox_found: !!cb,
        checkbox_checked: cb ? cb.checked : null,
        checkbox_class: cb ? cb.closest('.arco-checkbox')?.className : null,
        row_text: (row?.innerText || '').replace(/\n/g, ' | ').slice(0, 120),
      };
    });
  });
  out.steps.initial = { spinCount, stepCount, rows, sum: await sumLine(page), defaults: null };
  if (spinCount === 5) {
    const vals = [];
    for (let i = 0; i < 5; i++) vals.push(String(await spins.nth(i).inputValue()));
    out.steps.initial.defaults = vals;
  }
  dump();

  // 步骤1：专利数量行（nth 0）上下调节钮各一次。Arco 结构：先 up 后 down（实测方向以数值变化为准）
  const v0 = String(await spins.nth(0).inputValue());
  await stepBtns.nth(0).click();
  await page.waitForTimeout(500);
  const vUp = String(await spins.nth(0).inputValue());
  await stepBtns.nth(1).click();
  await page.waitForTimeout(500);
  const vDown = String(await spins.nth(0).inputValue());
  const btn0Class = await stepBtns.nth(0).getAttribute('class');
  const btn1Class = await stepBtns.nth(1).getAttribute('class');
  out.steps.stepper = { v0, after_first_btn: vUp, after_second_btn: vDown, btn0_class: btn0Class, btn1_class: btn1Class, sum: await sumLine(page) };
  dump();

  // 步骤2：直改 30（fill + blur）
  await spins.nth(0).fill('30');
  await page.keyboard.press('Tab');
  await page.waitForTimeout(500);
  out.steps.direct30 = { value: String(await spins.nth(0).inputValue()), sum: await sumLine(page) };
  dump();

  // 步骤3：停用「标准制定」（第 5 行 checkbox）→ 其余四维权重保留
  // P7：Arco input 本体隐藏（viewport 外），点可见 .arco-checkbox 容器；作用域收敛到模型面板，避开对比篮/机构区 checkbox
  const modelPanel = page.locator('.ent-section-panel', { hasText: '技术力评价模型' }).first();
  const cbStd = modelPanel.locator('.arco-checkbox').nth(4);
  const stdBefore = { wrapper_class: await cbStd.getAttribute('class').catch(() => null) };
  const othersBefore = [];
  for (let i = 0; i < 4; i++) othersBefore.push(String(await spins.nth(i).inputValue()));
  await cbStd.click({ timeout: 5000 });
  await page.waitForTimeout(800);
  const afterOff = {
    spinCount: await spins.count(),
    visibleSpinCount: await spins.count(),
    values: [],
    sum: await sumLine(page),
    stdRowText: null,
  };
  for (let i = 0; i < (await spins.count()); i++) {
    const s = spins.nth(i);
    afterOff.values.push({ v: String(await s.inputValue()), disabled: await s.isDisabled().catch(() => null) });
  }
  const rowInfo = await page.evaluate(() => {
    const label = [...document.querySelectorAll('main *')].find((el) => el.children.length === 0 && (el.innerText || '').trim() === '标准制定');
    let row = label;
    while (row && !row.querySelector('[role=spinbutton]')) row = row.parentElement;
    return {
      row_text: (row?.innerText || '').replace(/\n/g, ' | ').slice(0, 150),
      row_class: row?.className || null,
      checkbox_class: row?.querySelector('.arco-checkbox')?.className || null,
    };
  });
  out.steps.disable_std = { stdBefore, othersBefore, afterOff, rowInfo };
  dump();
  await page.screenshot({ path: path.join(outDir, 'scout-p005.png') });

  // 步骤4：重新启用「标准制定」→ 回显停用前取值
  await cbStd.click({ force: true });
  await page.waitForTimeout(800);
  const afterOn = { spinCount: await spins.count(), values: [], sum: await sumLine(page) };
  for (let i = 0; i < (await spins.count()); i++) afterOn.values.push(String(await spins.nth(i).inputValue()));
  out.steps.reenable_std = afterOn;
  dump();

  // 恢复默认 25（本探针把专利数量行从 30 改回 25，减少跨条污染；启停已复原）
  try {
    await spins.nth(0).fill('25');
    await page.keyboard.press('Tab');
    await page.waitForTimeout(400);
    out.steps.restore = { value: String(await spins.nth(0).inputValue()), sum: await sumLine(page) };
  } catch (e) {
    out.steps.restore = { error: String(e).slice(0, 150) };
  }
  dump();
  console.log('probe ok');
  console.log(JSON.stringify(out.steps, null, 2).slice(0, 3000));
} catch (e) {
  out.error = String(e).slice(0, 400);
  dump();
  console.error('probe fail:', out.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
