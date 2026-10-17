#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-sz P0-09（01290 指标清单就绪度标注与指标集一致）现场核实。
 * 产物落同目录 scout-p009-*.json；勿当 runner。遵守探针公约（无 IDE/有头浏览器）。
 * 核实点：
 *  R1 经历史「查看结果」进结果态后，框架卡 metric-list 每项的完整 DOM/文本（找就绪度标注：已登记/草稿/aligned/draft 等）
 *  R2 metric-list 与对比指标区（compare-metrics checkbox 文本）集合对照
 *  R3 若就绪度在 ⓘ 弹卡（MetricSpecCard）内：逐项点开记录弹卡内容
 *  R4 评审模式开关前后的 metric-list 形态（就绪度是否评审门控）
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const route = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const outDir = __dirname;

const dump = (name, data) => {
  fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2), 'utf8');
};

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
  for (let i = 0; i < 3; i++) {
    const close = page.locator('[aria-label="关闭对比篮"]');
    if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
      await close.first().click().catch(() => {});
      await page.waitForTimeout(300);
    } else break;
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const report = { probed_at: new Date().toISOString(), stages: {} };

// ---------- 登录 + 深链 + 经历史进结果态 ----------
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
if (page.url().includes('/login')) { await ensureLogin(page); await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded' }); }
await page.waitForTimeout(2500);
await closeBasket(page);

await page.getByRole('tab', { name: '分析记录' }).first().click();
await page.waitForTimeout(2000);
const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /shenzhen/ }).filter({ hasText: /已完成/ }).first();
await row.getByRole('button', { name: /查看结果/ }).first().click({ timeout: 8000 });
await page.waitForTimeout(3500);
await closeBasket(page);

// ---------- R1: 框架卡 metric-list 逐项 DOM ----------
const r1 = { url: page.url(), review_on_body: /评审模式/.test(((await page.locator('main').first().innerText().catch(() => '')) || '')) };
try {
  const list = page.locator('[data-testid="svc-eco-sz-metric-list"]');
  r1.list_count = await list.count();
  const lis = list.locator('li');
  r1.li_count = await lis.count();
  r1.items = [];
  for (let i = 0; i < (await lis.count()); i++) {
    const li = lis.nth(i);
    r1.items.push({
      text: ((await li.innerText().catch(() => '')) || '').replace(/\n/g, ' | '),
      html_class: await li.getAttribute('class').catch(() => null),
      icons: await li.locator('svg, [class*=icon], [class*=badge], [class*=tag], [class*=status], [class*=dot], [aria-label]').count(),
      icon_aria: await Promise.all((await li.locator('[aria-label]').all()).map((el) => el.getAttribute('aria-label').catch(() => null))),
    });
  }
  // 整个框架卡 HTML 结构（截断）找就绪度关键词
  const fwHtml = ((await list.first().evaluate((el) => el.innerHTML).catch(() => '')) || '');
  r1.list_html_snippet = fwHtml.replace(/\s+/g, ' ').slice(0, 2000);
  r1.has_ready_words = {
    aligned: /aligned/.test(fwHtml),
    draft: /draft/.test(fwHtml),
    yidengji: /已登记/.test(fwHtml),
    caogao: /草稿/.test(fwHtml),
    missing: /missing/.test(fwHtml),
    readiness: /readiness|就绪/.test(fwHtml),
    def_status: /def_status/.test(fwHtml),
  };
  // 框架卡全文
  const fw = page.locator('[data-testid="svc-eco-sz-framework"]');
  r1.framework_text = ((await fw.first().innerText().catch(() => '')) || '').replace(/\n/g, ' | ').slice(0, 800);
  // 页面全文找就绪度字样
  const bodyText = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  r1.body_ready_words = {
    yidengji: /已登记/.test(bodyText),
    caogao: /草稿/.test(bodyText),
    jiuXudu: /就绪/.test(bodyText),
  };
} catch (e) { r1.error = String(e).slice(0, 300); }
dump('scout-p009-r1-metric-list.json', r1);
report.stages.r1 = { ok: !r1.error, li: r1.li_count, ready: r1.has_ready_words, body: r1.body_ready_words };
await page.screenshot({ path: path.join(outDir, 'scout-p009-r1.png'), fullPage: false });

// ---------- R2: metric-list vs compare-metrics 集合对照 ----------
const r2 = {};
try {
  const lis = page.locator('[data-testid="svc-eco-sz-metric-list"] li');
  const names = [];
  for (let i = 0; i < (await lis.count()); i++) {
    const t = ((await lis.nth(i).innerText().catch(() => '')) || '').split('\n').map((s) => s.trim()).filter(Boolean);
    names.push(t[0] || '');
  }
  r2.list_names = names;
  const boxes = page.locator('[data-testid="svc-eco-sz-compare-metrics"] .arco-checkbox');
  r2.checkbox_n = await boxes.count();
  r2.checkbox_labels = [];
  for (let i = 0; i < (await boxes.count()); i++) {
    r2.checkbox_labels.push(((await boxes.nth(i).innerText().catch(() => '')) || '').replace(/\n/g, ' ').trim());
  }
  r2.compare_text = ((await page.locator('[data-testid="svc-eco-sz-compare-metrics"]').first().innerText().catch(() => '')) || '').replace(/\n/g, ' | ').slice(0, 400);
} catch (e) { r2.error = String(e).slice(0, 300); }
dump('scout-p009-r2-sets.json', r2);
report.stages.r2 = { ok: !r2.error, list: r2.list_names, boxes: r2.checkbox_labels };

// ---------- R3: ⓘ 弹卡（若指标项有可点 info 触发） ----------
const r3 = {};
try {
  const list = page.locator('[data-testid="svc-eco-sz-metric-list"]');
  // 找框架卡内的可点 icon（含 info/question 类）
  const trig = list.locator('li [class*=icon], li svg[class], li [role=button], li [aria-label]');
  r3.trig_n = await trig.count();
  r3.cards = [];
  if (r3.trig_n) {
    for (let i = 0; i < Math.min(r3.trig_n, 6); i++) {
      const el = trig.nth(i);
      const aria = await el.getAttribute('aria-label').catch(() => null);
      try {
        await el.click({ timeout: 2000 });
        await page.waitForTimeout(900);
        const pop = page.locator('.arco-popover:visible, .arco-tooltip:visible, [class*=metric-spec]:visible, .arco-drawer:visible');
        const pn = await pop.count();
        let ptext = '';
        if (pn) ptext = ((await pop.first().innerText().catch(() => '')) || '').replace(/\n/g, ' | ').slice(0, 500);
        r3.cards.push({ i, aria, pop_n: pn, pop_text: ptext });
        await page.keyboard.press('Escape').catch(() => {});
        await page.waitForTimeout(300);
      } catch (e2) {
        r3.cards.push({ i, aria, err: String(e2).slice(0, 120) });
      }
    }
  }
} catch (e) { r3.error = String(e).slice(0, 300); }
dump('scout-p009-r3-infocard.json', r3);
report.stages.r3 = { ok: !r3.error, trig: r3.trig_n, cards: (r3.cards || []).length };

// ---------- R4: 评审开关前后 metric-list 形态 ----------
const r4 = {};
try {
  // 当前默认态下 metric-list 是否含治理字样
  const before = ((await page.locator('[data-testid="svc-eco-sz-metric-list"]').first().evaluate((el) => el.innerHTML).catch(() => '')) || '');
  r4.before_has_governance = /metric_id|GAP-|Q-SVCCHAIN|aligned|draft|已登记|草稿/.test(before);
  // 关闭评审
  const pBtn = page.locator('button.persona-switch').first();
  if (await pBtn.count()) {
    await pBtn.click({ timeout: 5000 });
    await page.waitForTimeout(800);
    const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
    const ariaNow = await sw.getAttribute('aria-checked').catch(() => null);
    r4.review_initial = ariaNow;
    if (ariaNow === 'true') { await sw.click({ timeout: 5000 }); await page.waitForTimeout(1200); }
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(400);
    await page.locator('main').first().click({ position: { x: 10, y: 10 } }).catch(() => {});
    await page.waitForTimeout(800);
    const afterTxt = ((await page.locator('[data-testid="svc-eco-sz-metric-list"]').first().innerText().catch(() => '')) || '').replace(/\n/g, ' | ');
    r4.after_off_text = afterTxt;
    r4.after_off_has_ready = /已登记|草稿|aligned|draft/.test(afterTxt);
    r4.list_count_after = await page.locator('[data-testid="svc-eco-sz-metric-list"] li').count();
    // 重新打开评审（还原现场，避免污染后续脚本）
    await pBtn.click({ timeout: 5000 });
    await page.waitForTimeout(800);
    const sw2 = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
    const aria2 = await sw2.getAttribute('aria-checked').catch(() => null);
    if (aria2 === 'false') { await sw2.click({ timeout: 5000 }); await page.waitForTimeout(1000); }
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(400);
    const restoredTxt = ((await page.locator('[data-testid="svc-eco-sz-metric-list"]').first().innerText().catch(() => '')) || '').replace(/\n/g, ' | ');
    r4.restored_text = restoredTxt.slice(0, 400);
    r4.restored_li = await page.locator('[data-testid="svc-eco-sz-metric-list"] li').count();
  } else { r4.error = '未找到 persona-switch'; }
} catch (e) { r4.error = String(e).slice(0, 300); }
dump('scout-p009-r4-review-toggle.json', r4);
report.stages.r4 = { ok: !r4.error, before_gov: r4.before_has_governance, after_ready: r4.after_off_has_ready };

dump('scout-p009-summary.json', report);
await browser.close();
console.log('probe p009 done', JSON.stringify(report.stages, null, 2));
