#!/usr/bin/env node
/**
 * P0-12（FUNC-00722 聚焦机构邻域）写前探针：
 * 历史种子「查看结果」深链（SVC-20260903-001，0 POST）落结果态后只读勘察：
 * ① 结果壳标题在屏；hang 空文案在否
 * ② 过滤区 svc-eco-clip-filters / 聚焦下拉 svc-eco-clip-focus
 * ③ G6 svc-eco-g6-graph / 空画布 svc-eco-empty-canvas
 * ④ 聚焦候选 option 数（focusCandidates=isOrg）
 * 公约：独立无头；产物只进本目录。0 POST。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
const DEEP = '/service/chain-analysis?workspace=graph&tab=records&view=result&demo_state=result&task_id=SVC-20260903-001';
const OUT = { probed_at: new Date().toISOString(), base: BASE, entry: 'deep-link SVC-20260903-001' };
const dump = (n, d) => { fs.writeFileSync(path.join(__dirname, n), JSON.stringify(d, null, 2), 'utf8'); };
const safe = async (fn) => { try { return await fn(); } catch (e) { return { err: String((e && e.message) || e).slice(0, 400) }; } };

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
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);

  OUT.result = await safe(async () => {
    await page.goto(BASE + DEEP, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2500);
    await closeBasket(page);
    const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    const titleHit = /服务生态关系图谱/.test(body);
    const hangHit = /当前 hang 无可见点边/.test(body);
    const filters = page.locator('[data-testid="svc-eco-clip-filters"]');
    const focus = page.locator('[data-testid="svc-eco-clip-focus"]');
    const g6 = page.locator('[data-testid="svc-eco-g6-graph"]');
    const empty = page.locator('[data-testid="svc-eco-empty-canvas"]');
    const filtersCount = await filters.count();
    const focusCount = await focus.count();
    const focusVisible = focusCount ? await focus.first().isVisible().catch(() => false) : false;
    const g6Count = await g6.count();
    const emptyVisible = (await empty.count()) ? await empty.first().isVisible().catch(() => false) : false;
    let focusPlaceholder = null;
    let optionCount = 0;
    let optionSample = [];
    if (focusVisible) {
      focusPlaceholder = await focus.first().locator('.arco-select-view-value, .arco-select-view-placeholder').first().innerText().catch(() => null);
      await focus.first().locator('.arco-select-view').first().click({ timeout: 3000 }).catch(() => {});
      await page.waitForTimeout(500);
      const opts = page.locator('.arco-trigger-popup:visible .arco-select-option');
      optionCount = await opts.count().catch(() => 0);
      for (let i = 0; i < Math.min(optionCount, 5); i++) {
        optionSample.push(((await opts.nth(i).innerText().catch(() => '')) || '').trim().slice(0, 40));
      }
      await page.keyboard.press('Escape').catch(() => {});
    }
    let aria = null;
    if (g6Count) {
      aria = await g6.first().locator('[role="img"]').first().getAttribute('aria-label').catch(() => null);
    }
    const url = page.url().replace(BASE, '');
    const ecoFocus = (/eco_focus=([^&]+)/.exec(url) || [])[1] || null;
    await page.screenshot({ path: path.join(__dirname, '_probe-p012-result.png'), fullPage: false });
    return {
      deep: DEEP,
      url,
      titleHit,
      hangHit,
      filtersCount,
      focusCount,
      focusVisible,
      focusPlaceholder,
      optionCount,
      optionSample,
      g6Count,
      emptyVisible,
      aria,
      ecoFocus,
      body_head: body.slice(0, 420),
    };
  });

  OUT.conclusion = (() => {
    const r = OUT.result || {};
    if (r.err) return 'probe_error: ' + r.err;
    if (r.hangHit && r.focusCount === 0 && r.g6Count === 0) {
      return 'P0-12 写前探针：结果壳在 + hang 空 + focusCount=0 + g6Count=0 → 聚焦下拉挂 v-if=!parsed.empty 不渲染，无可聚焦机构（B 档 allow_skip + ENV-SVCGRAPH-HANG-EMPTY-001）';
    }
    if (r.focusVisible && r.optionCount >= 1) {
      return 'P0-12 写前探针：聚焦下拉可见且候选≥1，可继续写实跑 expect（optionCount=' + r.optionCount + '）';
    }
    return 'P0-12 写前探针：结果壳可达但聚焦不可用（见 result）';
  })();

  dump('_probe-p012.json', OUT);
  console.log(JSON.stringify({
    conclusion: OUT.conclusion,
    focusCount: OUT.result && OUT.result.focusCount,
    g6Count: OUT.result && OUT.result.g6Count,
    hangHit: OUT.result && OUT.result.hangHit,
    filtersCount: OUT.result && OUT.result.filtersCount,
  }, null, 2));
  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
