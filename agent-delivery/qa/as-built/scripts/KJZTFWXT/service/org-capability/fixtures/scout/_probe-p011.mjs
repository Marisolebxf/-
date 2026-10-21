#!/usr/bin/env node
/**
 * 一次性无头探针（P0-11 写稿用）：FUNC-00680 评审开启态追溯 + 指标说明角标 + 长提示。
 * 不点「开始评估」。产物落 scout-p011.json；勿当 runner。
 */
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const target = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;
const outDir = __dirname;

async function ensureLogin(page) {
  await page.waitForTimeout(600);
  if (!page.url().includes('/login')) return;
  const pw = page.locator('input[type=password]');
  await pw.first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
  if (!(await pw.count())) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await pw.first().fill('123456');
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

async function ensureReviewOn(page) {
  const persona = page.locator('button.persona-switch').first();
  await persona.click({ timeout: 5000 });
  await page.waitForTimeout(400);
  const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
  await sw.waitFor({ state: 'visible', timeout: 8000 });
  let checked = await sw.getAttribute('aria-checked').catch(() => null);
  if (checked === null) {
    const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]');
    checked = /arco-switch-checked/.test((await holder.first().getAttribute('class').catch(() => '')) || '')
      ? 'true'
      : 'false';
  }
  if (checked !== 'true') {
    await sw.click({ timeout: 5000 });
    await page.waitForTimeout(800);
  }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(300);
  return checked;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), case: 'P0-11', func: '00680' };

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  await closeBasket(page);

  const before = await ensureReviewOn(page);
  out.review_was = before;
  out.url = page.url();

  const main = page.locator('main').first();
  const traces = [];
  for (const lb of ['服务机构分析工作区需求追溯', '技术力评价模型需求追溯']) {
    const b = main.locator(`button[aria-label="${lb}"]`).first();
    const count = await main.locator(`button[aria-label="${lb}"]`).count();
    const vis = count ? await b.isVisible().catch(() => false) : false;
    const en = count ? await b.isEnabled().catch(() => false) : false;
    const cls = count ? (await b.getAttribute('class').catch(() => '')) || '' : '';
    traces.push({ aria: lb, count, vis, en, cls });
  }
  out.traces = traces;

  // click each trace → popup
  const popSel = '.arco-trigger-popup:visible, .arco-popover:visible';
  const dismiss = async () => {
    for (let i = 0; i < 3; i++) {
      if (!(await page.locator(popSel).count())) return;
      await page.mouse.click(1500, 600).catch(() => {});
      await page.waitForTimeout(400);
    }
  };
  await dismiss();
  const popSnips = [];
  for (const lb of ['服务机构分析工作区需求追溯', '技术力评价模型需求追溯']) {
    const b = main.locator(`button[aria-label="${lb}"]`).first();
    if (!(await b.count()) || !(await b.isVisible().catch(() => false))) {
      popSnips.push({ aria: lb, opened: false, reason: 'btn missing' });
      continue;
    }
    await b.click({ timeout: 5000 });
    await page.waitForTimeout(800);
    const pop = page.locator(popSel).first();
    const opened = (await pop.count()) && (await pop.isVisible().catch(() => false));
    const t = opened ? ((await pop.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 240) : '';
    popSnips.push({ aria: lb, opened: !!opened, text: t });
    await dismiss();
  }
  out.trace_pops = popSnips;

  // metric-spec-card + perm-pending-badge
  const specs = main.locator('button.metric-spec-card, button[aria-label="指标说明：服务机构技术力维度分"]');
  const specN = await specs.count();
  const specInfo = [];
  for (let i = 0; i < Math.min(specN, 4); i++) {
    const el = specs.nth(i);
    specInfo.push({
      aria: (await el.getAttribute('aria-label').catch(() => '')) || '',
      cls: (await el.getAttribute('class').catch(() => '')) || '',
      vis: await el.isVisible().catch(() => false),
      en: await el.isEnabled().catch(() => false),
    });
  }
  out.specs = { count: specN, items: specInfo };

  const pendings = main.locator('.perm-pending-badge, [aria-label*="待甲方确认"]');
  const pendN = await pendings.count();
  const pendInfo = [];
  for (let i = 0; i < Math.min(pendN, 4); i++) {
    const el = pendings.nth(i);
    pendInfo.push({
      tag: await el.evaluate((n) => n.tagName).catch(() => ''),
      aria: (await el.getAttribute('aria-label').catch(() => '')) || '',
      cls: (await el.getAttribute('class').catch(() => '')) || '',
      vis: await el.isVisible().catch(() => false),
    });
  }
  out.pendings = { count: pendN, items: pendInfo };

  // click first metric-spec-card → card/popup text
  await dismiss();
  if (specN) {
    await specs.first().click({ timeout: 5000 });
    await page.waitForTimeout(1000);
    const pop = page.locator(popSel).first();
    const opened = (await pop.count()) && (await pop.isVisible().catch(() => false));
    const popText = opened ? ((await pop.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 500) : '';
    // also scan drawer/modal
    const drawer = page.locator('.arco-drawer:visible, .arco-modal:visible, .arco-popover:visible').first();
    const drawerText =
      (await drawer.count()) && (await drawer.isVisible().catch(() => false))
        ? ((await drawer.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 500)
        : '';
    out.spec_click = { opened: !!opened, popText, drawerText };
    await dismiss();
    await page.keyboard.press('Escape').catch(() => {});
  }

  // click pending badge
  if (pendN) {
    await pendings.first().click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(800);
    const pop = page.locator(popSel).first();
    const opened = (await pop.count()) && (await pop.isVisible().catch(() => false));
    const t = opened ? ((await pop.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 400) : '';
    out.pending_click = { opened: !!opened, text: t };
  }

  const mainText = ((await main.innerText().catch(() => '')) || '').replace(/\s+/g, ' ');
  out.main_hits = {
    hasQ060: /Q060/.test(mainText),
    hasPending: /待甲方确认|待核验/.test(mainText),
    hasBackend: /后端签发|已算好|Java/.test(mainText),
    hasNoGreen: /禁止改绿|不改绿/.test(mainText),
    snippet: mainText.slice(0, 320),
  };

  await page.screenshot({ path: path.join(outDir, 'scout-p011.png'), fullPage: false });
  fs.writeFileSync(path.join(outDir, 'scout-p011.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
} catch (e) {
  out.error = String(e).slice(0, 400);
  fs.writeFileSync(path.join(outDir, 'scout-p011.json'), JSON.stringify(out, null, 2));
  console.error(out.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
