#!/usr/bin/env node
/** 无头二次实勘：ent-supply 环境闸门（选企业 / 开始分析 / 最近分析恢复结果） */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const target = 'enterprise/risk?workspace=supply-chain&tab=supply-chain';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

async function closeBasketIfVisible() {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if (await close.count()) {
    const vis = await close.first().isVisible().catch(() => false);
    if (vis) {
      try {
        await close.first().click({ timeout: 1500 });
        await page.waitForTimeout(300);
      } catch {
        await page.keyboard.press('Escape').catch(() => {});
      }
    }
  }
}

const out = {
  surveyed_at: new Date().toISOString(),
  entry_id: 'ent-supply',
  base_url: base,
  path: '/' + target,
  headless: true,
  login: { pass: false },
  deep_link: { pass: false, url: '' },
  close_review: { pass: true, note: '未强制关评审；深链可达即可' },
  select_objects: { pass: false, basket_select_count: 0, object_filled: false },
  start_analysis_enabled: { pass: false, enabled: false, disabled: null },
  history_completed: {
    pass: false,
    restore_count: 0,
    continue_count: 0,
    note: '',
  },
  precheck: { pass: true, note: '供应链非评估预检文案闸；仅记回填后主区摘要' },
  body_snippets: {},
};

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
out.login.pass = !page.url().includes('/login');

await page.goto(base + target, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);
out.deep_link.url = page.url();
out.deep_link.pass =
  /\/enterprise\/risk/.test(page.url()) &&
  /workspace=supply-chain/.test(page.url()) &&
  !page.url().includes('/login');
out.body_snippets.after_deep = (
  await page.locator('main.content-shell-layout').innerText().catch(() => '')
).slice(0, 400);

await closeBasketIfVisible();

const startEmpty = page.getByRole('button', { name: '开始分析' });
out.start_analysis_enabled.before_select = {
  count: await startEmpty.count(),
  disabled: await startEmpty.isDisabled().catch(() => null),
};

try {
  await page.getByRole('button', { name: '前往对比篮选择企业' }).click({ timeout: 8000 });
  await page.waitForTimeout(1000);
  const sels = page.locator('[aria-label^="选择 "]');
  out.select_objects.basket_select_count = await sels.count();
  if (out.select_objects.basket_select_count < 1) {
    out.select_objects.note = '对比篮无可选企业';
  } else {
    await sels.nth(0).click();
    await page.waitForTimeout(400);
    const confirm = page.getByRole('button', { name: '确定' });
    out.select_objects.confirm_disabled_after_pick = await confirm.isDisabled().catch(() => null);
    if (await confirm.isDisabled()) {
      await sels.nth(0).click();
      await page.waitForTimeout(400);
      out.select_objects.confirm_disabled_after_retry = await confirm.isDisabled().catch(() => null);
    }
    // 浮层脚部位于视口外时须滚动
    await confirm.scrollIntoViewIfNeeded();
    await page.waitForTimeout(200);
    await confirm.click({ timeout: 10000 });
    await page.waitForTimeout(2000);
    await closeBasketIfVisible();
    out.select_objects.object_filled = !!(await page.getByText(/来自对比篮/).count());
    out.select_objects.pass =
      out.select_objects.object_filled ||
      /enterprise_codes|source=compare-basket/.test(page.url());
  }
} catch (e) {
  out.select_objects.error = String(e.message || e).slice(0, 200);
}

out.url_after_select = page.url();
const start = page.getByRole('button', { name: '开始分析' });
out.start_analysis_enabled.disabled = await start.isDisabled().catch(() => null);
out.start_analysis_enabled.enabled = out.start_analysis_enabled.disabled === false;
out.start_analysis_enabled.pass = out.start_analysis_enabled.enabled === true;
out.body_snippets.after_select = (
  await page.locator('main.content-shell-layout').innerText().catch(() => '')
).slice(0, 500);

if (/预检未返回企业明细/.test(out.body_snippets.after_select || '')) {
  out.precheck.pass = false;
  out.precheck.fail_text_seen = true;
  out.precheck.note = '预检未返回企业明细';
}

await page.goto(base + target + '&view=history', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);
await closeBasketIfVisible();
const restore = page.getByRole('button', { name: '恢复结果' });
const cont = page.getByRole('button', { name: '继续查看' });
out.history_completed.restore_count = await restore.count();
out.history_completed.continue_count = await cont.count();
out.history_completed.url = page.url();
out.history_completed.body = (
  await page.locator('main.content-shell-layout').innerText().catch(() => '')
).slice(0, 600);

let openedResult = false;
let sampleTask = '';
if (out.history_completed.restore_count > 0) {
  try {
    const rowText = (
      await restore.first().locator('xpath=ancestor::tr[1]').innerText().catch(() => '')
    ).slice(0, 120);
    const m = rowText.match(/RISK-\d+-\d+/);
    if (m) sampleTask = m[0];
    await restore.first().click({ timeout: 5000 });
    await page.waitForTimeout(2500);
    openedResult = /view=result/.test(page.url());
    out.history_completed.via = '恢复结果';
    out.history_completed.sample_task = sampleTask || undefined;
  } catch (e) {
    out.history_completed.restore_error = String(e.message || e).slice(0, 120);
  }
} else if (out.history_completed.continue_count > 0) {
  try {
    await cont.first().click({ timeout: 5000 });
    await page.waitForTimeout(2500);
    openedResult =
      /view=result/.test(page.url()) ||
      !!(await page.getByText(/供应链图谱|关键节点|断链风险|任务摘要/).count());
    out.history_completed.via = '继续查看';
  } catch (e) {
    out.history_completed.continue_error = String(e.message || e).slice(0, 120);
  }
} else {
  out.history_completed.note = '最近分析无「恢复结果/继续查看」';
}

out.history_completed.result_url = page.url();
out.history_completed.result_body = (
  await page.locator('main.content-shell-layout').innerText().catch(() => '')
).slice(0, 500);
out.history_completed.pass =
  openedResult ||
  out.history_completed.restore_count > 0 ||
  (out.history_completed.continue_count > 0 &&
    /供应链|RISK-|关键节点|断链风险/.test(out.history_completed.body || ''));
if (
  /view=result/.test(page.url()) ||
  (await page.getByText(/供应链图谱|关键节点与断链风险|任务摘要/).count())
) {
  out.history_completed.pass = true;
  out.history_completed.result_opened = true;
}

await page.screenshot({ path: path.join(__dirname, 'env-gate.png'), fullPage: false });
const jsonPath = path.join(__dirname, 'scout-env-gate-probe.json');
fs.writeFileSync(jsonPath, JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify(out, null, 2));
await browser.close();
