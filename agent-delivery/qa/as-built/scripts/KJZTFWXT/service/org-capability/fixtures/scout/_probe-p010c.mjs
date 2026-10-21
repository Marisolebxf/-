#!/usr/bin/env node
/** P0-10c：分析记录页回切主 Tab 的真实 locator + 列表/空态稳态 */
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
const out = { surveyed_at: new Date().toISOString(), case: 'P0-10c' };

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  const spins = page.locator('[role=spinbutton]');
  await spins.first().waitFor({ state: 'visible', timeout: 10000 });
  await spins.nth(0).fill('30');
  await page.keyboard.press('Tab');
  await page.waitForTimeout(500);
  const w0 = [];
  for (let i = 0; i < 5; i++) w0.push(String(await spins.nth(i).inputValue()));
  const url0 = page.url();

  await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
  // 等空态或列表出现
  let settled = null;
  for (let i = 0; i < 20; i++) {
    await page.waitForTimeout(500);
    const t = ((await page.locator('main').innerText().catch(() => '')) || '');
    if (/暂无分析记录|查看结果|SVC-\d+/.test(t)) { settled = t; break; }
  }
  const recTxt = settled || ((await page.locator('main').innerText().catch(() => '')) || '');
  out.records = {
    url: page.url(),
    empty: /暂无分析记录/.test(recTxt),
    has_svc: /SVC-\d+/.test(recTxt),
    has_view: /查看结果/.test(recTxt),
    headers: ['任务', '类型', '状态', '创建时间', '操作'].filter((h) => recTxt.includes(h)),
    snippet: recTxt.replace(/\s+/g, ' ').slice(0, 500),
  };

  // 枚举可点回主区的候选
  const candidates = [];
  const sels = [
    { k: 'role_tab_exact', loc: () => page.getByRole('tab', { name: '服务机构技术力评估分析', exact: true }) },
    { k: 'role_tab_re', loc: () => page.getByRole('tab', { name: /服务机构技术力评估分析/ }) },
    { k: 'text_exact', loc: () => page.getByText('服务机构技术力评估分析', { exact: true }) },
    { k: 'arco_tabs_title', loc: () => page.locator('.arco-tabs-tab').filter({ hasText: '服务机构技术力评估分析' }) },
    { k: 'arco_tabs_title_nav', loc: () => page.locator('.arco-tabs-header-title, .arco-tabs-tab-title').filter({ hasText: '服务机构技术力评估分析' }) },
  ];
  for (const s of sels) {
    const loc = s.loc();
    const n = await loc.count();
    const info = { k: s.k, n };
    if (n) {
      info.visible = await loc.first().isVisible().catch(() => null);
      info.box = await loc.first().boundingBox().catch(() => null);
      info.tag = await loc.first().evaluate((el) => ({ tag: el.tagName, role: el.getAttribute('role'), cls: el.className, pe: getComputedStyle(el).pointerEvents })).catch(() => null);
    }
    candidates.push(info);
  }
  out.candidates = candidates;

  // 试点 arco-tabs-tab
  const arco = page.locator('.arco-tabs-tab').filter({ hasText: '服务机构技术力评估分析' });
  if (await arco.count()) {
    await arco.first().click({ timeout: 5000 });
    await page.waitForTimeout(1500);
    out.after_arco_click = { url: page.url(), has_spin: await page.locator('[role=spinbutton]').count() };
  } else {
    // text click first visible
    const tx = page.getByText('服务机构技术力评估分析', { exact: true });
    const n = await tx.count();
    out.text_count = n;
    for (let i = 0; i < Math.min(n, 4); i++) {
      const vis = await tx.nth(i).isVisible().catch(() => false);
      if (!vis) continue;
      await tx.nth(i).click({ timeout: 5000 }).catch((e) => { out.text_click_err = String(e.message || e).slice(0, 160); });
      await page.waitForTimeout(1200);
      out.after_text_click = { i, url: page.url(), has_spin: await page.locator('[role=spinbutton]').count() };
      if (/tab=capability/.test(page.url()) || (await page.locator('[role=spinbutton]').count()) >= 5) break;
    }
  }

  // 最终用 goto 验证权重
  await page.goto(url0, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const w1 = [];
  for (let i = 0; i < 5; i++) w1.push(String(await page.locator('[role=spinbutton]').nth(i).inputValue().catch(() => '?')));
  out.weight_via_url = { w0, w1, ok: w0.join(',') === w1.join(',') };

  // 若有查看结果则打开再回切
  await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
  await page.waitForTimeout(2500);
  const vr = page.getByText('查看结果', { exact: true });
  if (await vr.count()) {
    await vr.first().click();
    await page.waitForTimeout(2000);
    out.opened = { url: page.url() };
    const arco2 = page.locator('.arco-tabs-tab').filter({ hasText: '服务机构技术力评估分析' });
    if (await arco2.count()) {
      await arco2.first().click({ timeout: 5000 });
      await page.waitForTimeout(1500);
    } else {
      await page.goto(url0, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(1500);
    }
    await closeBasket(page);
    const w2 = [];
    for (let i = 0; i < 5; i++) w2.push(String(await page.locator('[role=spinbutton]').nth(i).inputValue().catch(() => '?')));
    out.after_open_rt = { url: page.url(), w2, ok: w0.join(',') === w2.join(',') };
  } else {
    out.opened = { skip: 'no 查看结果 — empty list' };
  }

  await page.locator('[role=spinbutton]').nth(0).fill('25').catch(() => {});
  await page.keyboard.press('Tab');
} catch (e) {
  out.error = String(e.stack || e).slice(0, 1200);
}

fs.writeFileSync(path.join(__dirname, 'scout-p010c.json'), JSON.stringify(out, null, 2));
await browser.close();
console.log(JSON.stringify({
  empty: out.records?.empty,
  has_svc: out.records?.has_svc,
  candidates: out.candidates,
  after_arco: out.after_arco_click,
  weight: out.weight_via_url?.ok,
  opened: out.opened,
  after_open_rt: out.after_open_rt,
  err: out.error?.slice(0, 200),
}, null, 2));
