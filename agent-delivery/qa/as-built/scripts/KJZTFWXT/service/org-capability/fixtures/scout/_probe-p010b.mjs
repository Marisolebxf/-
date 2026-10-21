#!/usr/bin/env node
/** P0-10 补探针：空态文案 + Tab 往返权重（不打开结果） */
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

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 })).newPage();
const out = { surveyed_at: new Date().toISOString(), case: 'P0-10b' };

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  await closeBasket(page);

  const spins = page.locator('[role=spinbutton]');
  await spins.first().waitFor({ state: 'visible', timeout: 10000 });
  await spins.nth(0).fill('30');
  await page.keyboard.press('Tab');
  await page.waitForTimeout(500);
  const w0 = [];
  for (let i = 0; i < 5; i++) w0.push(String(await spins.nth(i).inputValue()));
  const url0 = page.url();
  out.before = { w0, url0, head: ((await page.locator('.svc-org-cap-compare__head').innerText().catch(() => '')) || '').replace(/\s+/g, ' ') };

  const tabs = page.getByRole('tab');
  const tabNames = [];
  for (let i = 0; i < await tabs.count(); i++) {
    tabNames.push({
      name: ((await tabs.nth(i).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim(),
      aria: await tabs.nth(i).getAttribute('aria-selected'),
    });
  }
  out.tabs_before = tabNames;

  await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
  await page.waitForTimeout(2000);
  const mainTxt = ((await page.locator('main').innerText().catch(() => '')) || '');
  out.records_empty = {
    url: page.url(),
    has_empty: /暂无分析记录/.test(mainTxt),
    snippet: mainTxt.replace(/\s+/g, ' ').slice(0, 400),
    tab_names: await page.getByRole('tab').allInnerTexts().catch(() => []),
    empty_nodes: await page.locator('.arco-empty, [class*=empty]').count(),
  };

  const mainTab = page.getByRole('tab', { name: '服务机构技术力评估分析', exact: true });
  out.main_tab = { count: await mainTab.count(), visible: await mainTab.first().isVisible().catch(() => null) };
  if (await mainTab.count()) {
    try {
      await mainTab.first().click({ timeout: 8000 });
      await page.waitForTimeout(1500);
      out.after_tab_click = { url: page.url(), ok: true };
    } catch (e) {
      out.after_tab_click = { ok: false, err: String(e.message || e).slice(0, 240) };
      try {
        await mainTab.first().click({ timeout: 8000, force: true });
        await page.waitForTimeout(1500);
        out.after_force_click = { url: page.url(), ok: true };
      } catch (e2) {
        out.after_force_click = { ok: false, err: String(e2.message || e2).slice(0, 240) };
      }
    }
  }

  // URL 回跳（保留 cap_w）
  await page.goto(url0, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await closeBasket(page);
  const spins2 = page.locator('[role=spinbutton]');
  const w1 = [];
  for (let i = 0; i < 5; i++) w1.push(String(await spins2.nth(i).inputValue().catch(() => '?')));
  out.after_goto = { url: page.url(), w1, weight_ok: w1.join(',') === w0.join(','), head: ((await page.locator('.svc-org-cap-compare__head').innerText().catch(() => '')) || '').replace(/\s+/g, ' ') };

  // Tab 往返（不经打开结果）：capability → records → capability，权重应保留在 URL/状态
  await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const back = page.getByRole('tab', { name: '服务机构技术力评估分析', exact: true });
  if (await back.count()) {
    await back.first().click({ timeout: 8000, force: true }).catch(() => {});
    await page.waitForTimeout(1500);
  }
  // 若仍停在 records，用 goto(url0)
  if (/tab=records/.test(page.url()) && !/tab=capability/.test(page.url())) {
    await page.goto(url0, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1500);
    out.roundtrip_via = 'goto_url0';
  } else {
    out.roundtrip_via = 'tab_click';
  }
  await closeBasket(page);
  const spins3 = page.locator('[role=spinbutton]');
  const w2 = [];
  for (let i = 0; i < 5; i++) w2.push(String(await spins3.nth(i).inputValue().catch(() => '?')));
  out.roundtrip = { url: page.url(), w2, weight_ok: w2.join(',') === w0.join(',') };

  await spins3.nth(0).fill('25');
  await page.keyboard.press('Tab');
} catch (e) {
  out.error = String(e.stack || e).slice(0, 1000);
}

fs.writeFileSync(path.join(__dirname, 'scout-p010b.json'), JSON.stringify(out, null, 2));
await browser.close();
console.log(JSON.stringify({
  empty: out.records_empty?.has_empty,
  weight_goto: out.after_goto?.weight_ok,
  weight_rt: out.roundtrip?.weight_ok,
  via: out.roundtrip_via,
  main_click: out.after_tab_click,
  err: out.error?.slice(0, 200),
}, null, 2));
