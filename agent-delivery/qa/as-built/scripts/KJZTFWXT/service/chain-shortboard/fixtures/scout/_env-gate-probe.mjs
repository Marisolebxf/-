#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · svc-chain-shortboard。产物落同目录；勿当 runner。
 * 闸门：登录深链 / 空态门控 / 选产业集群后「开始分析」enabled / 分析记录已完成。
 * async_analysis=true：合法对象选齐后须核开始分析 enabled（method-patch §3.2）。
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
const route = '/service/chain-analysis?workspace=chain&tab=chain';
const outDir = __dirname;
const pickCluster = '新一代信息技术';

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
      await page.waitForTimeout(400);
    } else break;
  }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(200);
}

async function startBtnState(page) {
  const btn = page.getByRole('button', { name: '开始分析' }).first();
  const count = await btn.count();
  if (!count) return { found: false };
  const className = (await btn.getAttribute('class').catch(() => '')) || '';
  const disabledAttr = await btn.isDisabled().catch(() => null);
  const enabled = await btn.isEnabled().catch(() => false);
  return {
    found: true,
    enabled,
    disabledAttr,
    class_has_disabled: /arco-btn-disabled|disabled/.test(className),
    class: className.slice(0, 160),
  };
}

async function mainSnippet(page, n = 60) {
  return page
    .locator('main, .svc-eco-panel, [class*=content]')
    .first()
    .innerText()
    .then((t) =>
      t
        .split('\n')
        .map((s) => s.trim())
        .filter(Boolean)
        .slice(0, n),
    )
    .catch(() => []);
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const scout = {
  surveyed_at: new Date().toISOString(),
  entry_id: 'svc-chain-shortboard',
  route,
  stages: {},
};

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  scout.stages.login = { pass: true };
} catch (e) {
  scout.stages.login = { pass: false, error: String(e).slice(0, 200) };
  dump('scout-gate-fail.json', scout);
  await browser.close();
  process.exit(1);
}

const target = new URL(route.replace(/^\//, ''), baseUrl).toString();
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
if (page.url().includes('/login')) {
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
}
await page.waitForTimeout(2500);
await closeBasket(page);
await page.waitForTimeout(500);

const deepUrl = page.url();
scout.stages.deep_link = {
  pass:
    /\/service\/chain-analysis/.test(deepUrl) &&
    /workspace=chain/.test(deepUrl) &&
    !deepUrl.includes('/login'),
  url: deepUrl,
  title: await page.title(),
};
await page.screenshot({ path: path.join(outDir, 'env-gate-deep.png'), fullPage: false });

const tabs = await page.evaluate(() =>
  [...document.querySelectorAll('[role=tab]')]
    .filter((t) => !String(t.id || '').startsWith('compare-basket'))
    .map((t) => ({
      text: (t.innerText || '').trim().replace(/\s+/g, ' '),
      selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
    })),
);

const emptyStart = await startBtnState(page);
const emptyText = ((await page.locator('.svc-eco-panel').first().innerText().catch(() => '')) || '').slice(0, 800);
const emptyHint =
  /请先确认产业条件|请先选择|再点击「开始分析」|不会自动创建任务/.test(emptyText);
scout.stages.empty = {
  tabs,
  start: emptyStart,
  emptyHint,
  panelSnippet: emptyText.slice(0, 400),
  mainSnippet: await mainSnippet(page, 40),
};
dump('scout-empty.json', scout.stages.empty);
await page.screenshot({ path: path.join(outDir, 'env-gate-empty.png'), fullPage: false });

// 展开产业集群下拉
let industryOptions = [];
let pickOk = false;
let startAfterPick = { found: false };
try {
  const selectView = page.locator('.industry-catalog-select, .arco-select').filter({ has: page.locator('input[placeholder="选择产业集群"]') }).first();
  const input = page.locator('input[placeholder="选择产业集群"]').first();
  if (await selectView.count()) {
    await selectView.click({ timeout: 5000 });
  } else if (await input.count()) {
    await input.click({ timeout: 5000 });
  }
  await page.waitForTimeout(800);

  industryOptions = await page.evaluate(() => {
    const nodes = [
      ...document.querySelectorAll(
        '.arco-select-popup-visible .arco-select-option, .arco-select-dropdown .arco-select-option, [role=listbox] [role=option]',
      ),
    ];
    return nodes
      .map((el) => (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' '))
      .filter(Boolean);
  });

  dump('scout-industry-options.json', {
    count: industryOptions.length,
    options: industryOptions,
  });
  await page.screenshot({ path: path.join(outDir, 'env-gate-industry.png'), fullPage: false });

  const opt = page
    .locator('.arco-select-option, [role=option]')
    .filter({ hasText: pickCluster })
    .first();
  if ((await opt.count()) && (await opt.isVisible().catch(() => false))) {
    await opt.click({ timeout: 5000 });
    pickOk = true;
    await page.waitForTimeout(1000);
  } else {
    // fallback: 点列表第一项
    const first = page.locator('.arco-select-popup-visible .arco-select-option').first();
    if ((await first.count()) && (await first.isVisible().catch(() => false))) {
      const label = ((await first.innerText().catch(() => '')) || '').trim();
      await first.click({ timeout: 5000 });
      pickOk = true;
      scout.stages.pick_fallback = label;
      await page.waitForTimeout(1000);
    }
  }
} catch (e) {
  scout.stages.industry_error = String(e).slice(0, 200);
}

startAfterPick = await startBtnState(page);
const afterPickText = ((await page.locator('.svc-eco-panel').first().innerText().catch(() => '')) || '').slice(0, 800);
const selectValue = await page.evaluate(() => {
  const view = document.querySelector('.industry-catalog-select .arco-select-view-value, .industry-catalog-select .arco-select-view-single');
  return (view?.innerText || view?.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80);
});
scout.stages.after_pick = {
  pickOk,
  pickCluster,
  selectValue,
  industry_count: industryOptions.length,
  industry_options: industryOptions,
  start: startAfterPick,
  panelSnippet: afterPickText.slice(0, 400),
  start_enabled: startAfterPick.enabled === true && startAfterPick.class_has_disabled !== true,
};
dump('scout-after-pick.json', scout.stages.after_pick);
await page.screenshot({ path: path.join(outDir, 'env-gate-config.png'), fullPage: false });

// 分析记录：已完成任务？
await page.getByRole('tab', { name: '分析记录' }).first().click().catch(() => {});
await page.waitForTimeout(2000);
await closeBasket(page);
const recordsText = ((await page.locator('main').first().innerText().catch(() => '')) || '').slice(0, 2500);
const viewResultBtns = page.getByRole('button', { name: /查看结果/ });
const viewCount = await viewResultBtns.count();
let enabledView = 0;
for (let i = 0; i < Math.min(viewCount, 10); i++) {
  if (await viewResultBtns.nth(i).isEnabled().catch(() => false)) enabledView++;
}
const hasDone =
  /已完成/.test(recordsText) ||
  enabledView > 0 ||
  /SVC-\d{8}-\d+/.test(recordsText);
const sampleIds = [...recordsText.matchAll(/SVC-\d{8}-\d+/g)].map((m) => m[0]).slice(0, 8);
scout.stages.records = {
  has_tab: true,
  hasDone,
  enabledView,
  viewCount,
  sampleIds,
  snippet: recordsText
    .split('\n')
    .map((s) => s.trim())
    .filter(Boolean)
    .slice(0, 50),
};
dump('scout-records.json', scout.stages.records);
await page.screenshot({ path: path.join(outDir, 'env-gate-records.png'), fullPage: false });

// 切回短板 Tab，保留选中态再截一张总图
await page.getByRole('tab', { name: '服务链短板分析' }).first().click().catch(() => {});
await page.waitForTimeout(800);
await closeBasket(page);
await page.screenshot({ path: path.join(outDir, 'env-gate.png'), fullPage: false });

const g1 = scout.stages.login?.pass === true && scout.stages.deep_link?.pass === true;
const g2_empty_gate =
  emptyStart.class_has_disabled === true ||
  emptyStart.disabledAttr === true ||
  emptyHint === true;
const g3_start_enabled =
  scout.stages.after_pick?.start_enabled === true && pickOk === true;
const g5_history = hasDone === true;

scout.gate_summary = {
  G1_login_deeplink: g1,
  G2_empty_start_gate: g2_empty_gate,
  G3_start_enabled_after_cluster: g3_start_enabled,
  G4_eval_precheck: 'n/a',
  G5_completed_task: g5_history,
  industry_option_count: industryOptions.length,
};

dump('scout-env-gate-probe.json', scout);
await browser.close();
console.log('env-gate probe ok', JSON.stringify(scout.gate_summary, null, 2));
