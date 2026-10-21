#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · ent-eval-compete。
 * 产物：env-gate.json / env-gate.png / env-gate-hist.png / scout-env-gate-probe.json
 * 勿当 runner；禁止 IDE/有头浏览器。
 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://10.50.69.111:30892/';
const pagePath = '/enterprise/evaluation?workspace=competitiveness&mode=competitiveness';
const codes = [
  '0a2b82208071ce5a0e3bd562b80e263b',
  '12ceab1a61c7d1e1e5cb61b78dd8f3aa',
];

async function closeBasket(page) {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if (!(await close.count())) return;
  const vis = await close.first().isVisible().catch(() => false);
  const en = await close.first().isEnabled().catch(() => false);
  if (!vis || !en) return;
  try {
    await close.first().click({ timeout: 1500 });
    await page.waitForTimeout(300);
  } catch {
    await page.keyboard.press('Escape').catch(() => {});
  }
}

async function closeReview(page) {
  const sw = page.locator('[aria-label="内部评审模式"]');
  if (!(await sw.count())) return { pass: true, note: '无人设开关' };
  const checked = await sw.first().getAttribute('aria-checked').catch(() => null);
  if (checked === 'true') {
    try {
      await sw.first().click({ timeout: 2000 });
      await page.waitForTimeout(400);
    } catch (e) {
      return { pass: false, note: String(e.message || e).slice(0, 120) };
    }
  }
  return { pass: true };
}

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

const gates = {
  login: { pass: false },
  deep_link: { pass: false, url: '' },
  close_review: { pass: true },
  select_objects: {
    pass: false,
    basket_count: 0,
    object_filled: false,
    overlay_openable: false,
    fill_via: '',
  },
  start_analysis_enabled: { pass: false, enabled: false },
  precheck: { pass: true, fail_text_seen: false, note: '' },
  historical_results: {
    pass: false,
    has_tab: false,
    completed_count: 0,
    restore_result_buttons: false,
    note: '',
  },
};

const evidence = {
  screenshot: 'env-gate.png',
  hist_screenshot: 'env-gate-hist.png',
  start_enabled: false,
  precheck_fail: false,
  coverage_tabs: [],
  body_hit: '',
  url_after_select: '',
  heading: '',
  template: '',
  metrics_group: '',
  metrics_hint: [],
  hist_snippet: '',
};

try {
  await page.goto(base + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const loginBtn = page.getByRole('button', { name: /登录/ });
  if (await loginBtn.count()) await loginBtn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
  gates.login.pass = !page.url().includes('/login');

  await page.goto(base.replace(/\/?$/, '') + pagePath, {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await page.waitForTimeout(2000);
  gates.deep_link.url = page.url();
  gates.deep_link.pass =
    /workspace=competitiveness/.test(page.url()) &&
    /mode=competitiveness/.test(page.url()) &&
    !page.url().includes('/login');

  gates.close_review = await closeReview(page);
  await closeBasket(page);

  evidence.heading = (
    await page.getByRole('heading', { name: /企业综合竞争力评估/ }).first().innerText().catch(() => '')
  ).trim();
  evidence.template = (await page.getByText(/综合竞争力标准模板/).first().innerText().catch(() => '')).slice(
    0,
    40,
  );
  evidence.metrics_group = (
    await page.getByText(/综合竞争力三域/).first().innerText().catch(() => '')
  ).slice(0, 40);
  for (const name of ['创新能力', '经营能力', '成长能力']) {
    if (await page.getByText(name, { exact: true }).count()) evidence.metrics_hint.push(name);
  }

  // Path A: overlay select
  try {
    const cta = page.getByRole('button', { name: '前往对比篮选择企业' });
    if (await cta.count()) {
      await cta.click({ timeout: 8000 });
      await page.waitForTimeout(1000);
      gates.select_objects.overlay_openable = !!(await page.getByText('选择分析企业').count());
      const sels = page.locator('[aria-label^="选择 "]');
      gates.select_objects.basket_count = await sels.count();
      if (gates.select_objects.basket_count >= 1) {
        await sels.nth(0).click();
        if (gates.select_objects.basket_count >= 2) await sels.nth(1).click();
        await page.waitForTimeout(400);
        const confirm = page.getByRole('button', { name: '确定' });
        await confirm.scrollIntoViewIfNeeded().catch(() => {});
        if (!(await confirm.isDisabled().catch(() => true))) {
          await confirm.click({ timeout: 10000 });
          await page.waitForTimeout(2500);
          gates.select_objects.fill_via = 'overlay_basket';
        }
      }
      await page.keyboard.press('Escape').catch(() => {});
    }
  } catch (e) {
    gates.select_objects.overlay_error = String(e.message || e).slice(0, 160);
  }

  // Path B: deep_link enterprise_codes if overlay did not fill
  if (!/enterprise_codes/.test(page.url())) {
    const q = codes.map((c) => `enterprise_codes[]=${c}`).join('&');
    await page.goto(
      `${base.replace(/\/?$/, '')}${pagePath}&${q}&source=compare-basket`,
      { waitUntil: 'domcontentloaded', timeout: 60000 },
    );
    await page.waitForTimeout(2500);
    gates.select_objects.fill_via = gates.select_objects.fill_via || 'deep_link_enterprise_codes';
  }

  await closeBasket(page);
  evidence.url_after_select = page.url();
  gates.select_objects.object_filled =
    !!(await page.getByText(/来自对比篮|返回对比篮调整对象/).count()) ||
    /enterprise_codes/.test(page.url());
  gates.select_objects.pass =
    gates.select_objects.object_filled || gates.select_objects.basket_count > 0;

  const start = page.getByRole('button', { name: '开始分析' });
  const startDisabled = await start.isDisabled().catch(() => null);
  gates.start_analysis_enabled.enabled = startDisabled === false;
  gates.start_analysis_enabled.pass = gates.start_analysis_enabled.enabled === true;
  evidence.start_enabled = gates.start_analysis_enabled.enabled;

  const body = await page.locator('main.content-shell-layout, main').first().innerText().catch(() => '');
  evidence.body_hit = body.slice(-280);
  if (/预检未返回企业明细/.test(body)) {
    gates.precheck.pass = false;
    gates.precheck.fail_text_seen = true;
    gates.precheck.note = '预检未返回企业明细';
    evidence.precheck_fail = true;
  } else if (gates.start_analysis_enabled.enabled) {
    gates.precheck.pass = true;
    gates.precheck.note = '未见预检失败文案且开始分析可用';
  } else {
    gates.precheck.pass = false;
    gates.precheck.note = '开始分析仍 disabled；未见标准预检文案';
  }

  for (const tab of ['全部可信度', '高可信', '中可信', '低可信', '不可生成']) {
    if (await page.getByText(tab, { exact: true }).count()) evidence.coverage_tabs.push(tab);
  }

  await page.screenshot({ path: path.join(__dirname, 'env-gate.png'), fullPage: false });

  // 最近评估
  const histTab = page.getByRole('tab', { name: /最近评估/ });
  gates.historical_results.has_tab = !!(await histTab.count());
  if (gates.historical_results.has_tab) {
    await histTab.first().click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(1500);
    await closeBasket(page);
    const histBody = await page.locator('main.content-shell-layout, main').first().innerText().catch(() => '');
    evidence.hist_snippet = histBody.replace(/\s+/g, ' ').slice(0, 400);
    const restore = page.getByRole('button', { name: '恢复结果' });
    const view = page.getByRole('button', { name: '查看结果' });
    const restoreN = await restore.count();
    const viewN = await view.count();
    gates.historical_results.restore_result_buttons = restoreN + viewN > 0;
    gates.historical_results.completed_count = (histBody.match(/已完成/g) || []).length;
    gates.historical_results.pass =
      gates.historical_results.restore_result_buttons || gates.historical_results.completed_count > 0;
    gates.historical_results.note = gates.historical_results.pass
      ? `最近评估有已完成任务；恢复结果=${restoreN} 查看结果=${viewN}`
      : '最近评估无已完成可恢复入口';
    await page.screenshot({ path: path.join(__dirname, 'env-gate-hist.png'), fullPage: false });
  } else {
    gates.historical_results.note = '无「最近评估」Tab';
  }
} catch (e) {
  evidence.probe_error = String(e.message || e).slice(0, 300);
}

const overall =
  gates.login.pass &&
  gates.deep_link.pass &&
  gates.select_objects.pass &&
  gates.start_analysis_enabled.pass &&
  gates.precheck.pass
    ? 'pass'
    : 'fail';

const ticket = 'ENV-EVAL-COMPETE-PRECHECK-001';
const conclusion =
  overall === 'pass'
    ? '环境闸门通过：合法对象回填后「开始分析」可用且无预检阻塞。过程/结果态可写机检（历史恢复另计）。'
    : `环境闸门失败：合法对象回填后「开始分析」仍 ${
        gates.start_analysis_enabled.enabled ? 'enabled' : 'disabled'
      }；预检文案「${gates.precheck.note || '无'}」。金样仅写配置/门控态，禁止过程/结果态机检。ticket=${ticket}`;

const envGate = {
  surveyed_at: new Date().toISOString(),
  entry_id: 'ent-eval-compete',
  base_url: base,
  path: pagePath,
  headless: true,
  overall,
  gates,
  evidence,
  conclusion,
  tickets: overall === 'fail' ? [ticket] : [],
};

fs.writeFileSync(path.join(__dirname, 'env-gate.json'), JSON.stringify(envGate, null, 2), 'utf8');
fs.writeFileSync(
  path.join(__dirname, 'scout-env-gate-probe.json'),
  JSON.stringify({ gates, evidence, overall }, null, 2),
  'utf8',
);
console.log(JSON.stringify({ overall, gates, tickets: envGate.tickets, conclusion }, null, 2));
await browser.close();
