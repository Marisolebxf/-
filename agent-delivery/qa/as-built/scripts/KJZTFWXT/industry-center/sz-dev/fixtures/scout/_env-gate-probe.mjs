#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · chain-sz-dev。产物落同目录；勿当 runner。
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
const route = '/industry-center/shenzhen?workspace=development&tab=development';
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

async function readSelectViews(page) {
  const views = page.locator('main .arco-select-view');
  const n = await views.count();
  const texts = [];
  for (let i = 0; i < Math.min(n, 4); i++) {
    const t = ((await views.nth(i).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
    texts.push(t);
  }
  return texts;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const shots = {};

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  const target = new URL(route.replace(/^\//, ''), baseUrl).toString();
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  if (page.url().includes('/login')) {
    await ensureLogin(page);
    await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  }
  await page.waitForTimeout(2500);
  await closeBasket(page);

  const tabMain = page.getByRole('tab', { name: '深圳产业发展分析' });
  if ((await tabMain.count()) && (await tabMain.first().getAttribute('aria-selected')) !== 'true') {
    await tabMain.first().click();
    await page.waitForTimeout(1000);
  }

  const loginOk = !page.url().includes('/login');
  const deepUrl = page.url();
  const deepOk =
    /\/industry-center\/shenzhen/.test(deepUrl) &&
    /workspace=development/.test(deepUrl) &&
    /tab=development/.test(deepUrl);
  const title = await page.title();
  const titleOk = /深圳产业发展分析/.test(title);
  shots.deep = path.join(outDir, 'env-gate-deep.png');
  await page.screenshot({ path: shots.deep, fullPage: false });

  const start = page.getByRole('button', { name: '开始分析' }).first();
  const reset = page.getByRole('button', { name: '重置参数' }).first();
  if (await reset.count()) {
    await reset.click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(800);
  }
  await closeBasket(page);

  const emptyStartDisabled = await start.isDisabled();
  const subjectInput = page.locator('main input[readonly]').filter({ hasNot: page.locator('[placeholder]') });
  let subjectValue = '';
  const inputs = page.locator('main input');
  const inCount = await inputs.count();
  for (let i = 0; i < inCount; i++) {
    const v = await inputs.nth(i).inputValue().catch(() => '');
    const ro = await inputs.nth(i).getAttribute('readonly');
    if (v === '深圳' && ro !== null) {
      subjectValue = v;
      break;
    }
  }

  const landingViews = await readSelectViews(page);
  const fillLog = [];

  // 选产业：新一代信息技术
  const ind = page.locator('main .arco-select-view').first();
  await page.keyboard.press('Escape').catch(() => {});
  await ind.click({ timeout: 8000 });
  await page.waitForTimeout(600);
  const indPopup = page.locator('.arco-trigger-popup:visible');
  const indOpts = await indPopup.locator('.arco-select-option').allTextContents().catch(() => []);
  const pickInd = indPopup.locator('.arco-select-option').filter({ hasText: '新一代信息技术' });
  const indOk = (await pickInd.count()) > 0;
  if (indOk) {
    await pickInd.first().click();
    await page.waitForTimeout(900);
  } else {
    await page.keyboard.press('Escape').catch(() => {});
  }
  fillLog.push({ step: 'industry', ok: indOk, sample: indOpts.slice(0, 8) });
  const afterIndustryDisabled = await start.isDisabled();
  const afterIndustryViews = await readSelectViews(page);

  // 绑有效对比结果
  const bind = page.locator('main .arco-select-view').nth(1);
  await page.keyboard.press('Escape').catch(() => {});
  await bind.click({ timeout: 8000 });
  await page.waitForTimeout(700);
  const bindPopup = page.locator('.arco-trigger-popup:visible');
  const bindAll = await bindPopup
    .locator('.arco-select-option')
    .evaluateAll((els) =>
      els.map((el) => ({
        text: (el.textContent || '').replace(/\s+/g, ' ').trim(),
        disabled: el.classList.contains('arco-select-option-disabled') || el.getAttribute('aria-disabled') === 'true',
      })),
    )
    .catch(() => []);
  const enabledBind = bindAll.filter((o) => !o.disabled && o.text && !/无效/.test(o.text));
  const invalidBind = bindAll.filter((o) => o.disabled || /无效/.test(o.text));
  let boundSample = '';
  let bindOk = false;
  if (enabledBind.length) {
    const opt = bindPopup.locator('.arco-select-option:not(.arco-select-option-disabled)').filter({ hasText: enabledBind[0].text });
    if (await opt.count()) {
      await opt.first().click();
      await page.waitForTimeout(900);
      boundSample = enabledBind[0].text;
      bindOk = true;
    }
  } else {
    await page.keyboard.press('Escape').catch(() => {});
  }
  fillLog.push({
    step: 'bind',
    ok: bindOk,
    enabledCount: enabledBind.length,
    invalidCount: invalidBind.length,
    sample: bindAll.slice(0, 6),
  });

  const legalViews = await readSelectViews(page);
  const startEnabledLegal = await start.isEnabled();
  const goals = [];
  for (const name of ['政策', '技术', '人才']) {
    const cb = page.getByRole('checkbox', { name });
    goals.push({
      name,
      checked: (await cb.count()) ? await cb.first().isChecked().catch(() => null) : null,
    });
  }

  shots.config = path.join(outDir, 'env-gate-config.png');
  await page.screenshot({ path: shots.config, fullPage: false });

  // g3 N/A
  const g3 = {
    id: 'g3_precheck_eval',
    pass: true,
    n_a: true,
    detail: { note: '深圳产业发展分析非企业评估页，无「预检未返回企业明细」门控；本闸 N/A=pass' },
  };

  // g4 生物：仅联动探测，不依赖成功分析
  if (await reset.count()) {
    await reset.click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(600);
  }
  await page.keyboard.press('Escape').catch(() => {});
  await ind.click({ timeout: 8000 });
  await page.waitForTimeout(500);
  const bioPopup = page.locator('.arco-trigger-popup:visible');
  const bioOpt = bioPopup.locator('.arco-select-option').filter({ hasText: /^生物$/ });
  let bioSelected = false;
  let afterBioViews = [];
  let afterBioStart = null;
  if (await bioOpt.count()) {
    await bioOpt.first().click();
    await page.waitForTimeout(800);
    bioSelected = true;
    afterBioViews = await readSelectViews(page);
    afterBioStart = await start.isEnabled();
  } else {
    await page.keyboard.press('Escape').catch(() => {});
  }
  shots.bio = path.join(outDir, 'env-gate-bio.png');
  await page.screenshot({ path: shots.bio, fullPage: false });

  // g5 分析记录
  const recordsTab = page.getByRole('tab', { name: /分析记录/ }).first();
  if (await recordsTab.count()) {
    await recordsTab.click({ timeout: 8000 }).catch(async () => {
      await page.keyboard.press('Escape').catch(() => {});
      await page.getByText('分析记录', { exact: true }).first().click({ timeout: 5000 }).catch(() => {});
    });
  }
  await page.waitForTimeout(1500);
  shots.records = path.join(outDir, 'env-gate-records.png');
  await page.screenshot({ path: shots.records, fullPage: false });
  const mainText = await page.locator('main').first().innerText();
  const viewBtns = page.getByRole('button', { name: /查看结果/ });
  const viewCount = await viewBtns.count();
  let enabledView = 0;
  let disabledView = 0;
  for (let i = 0; i < viewCount; i++) {
    if (await viewBtns.nth(i).isDisabled()) disabledView++;
    else enabledView++;
  }
  const hasDoneRow = /已完成|成功/.test(mainText);
  const emptyRecords = /暂无数据/.test(mainText);
  const failOnly = /失败/.test(mainText) && !hasDoneRow;

  const g1pass = loginOk && deepOk && titleOk;
  const g2pass =
    emptyStartDisabled === true &&
    afterIndustryDisabled === true &&
    bindOk === true &&
    startEnabledLegal === true &&
    subjectValue === '深圳';

  const gates = [
    {
      id: 'g1_login_deep',
      pass: g1pass,
      detail: { loginOk, deepOk, titleOk, title, url: deepUrl },
      shot: path.relative(outDir, shots.deep),
    },
    {
      id: 'g2_start_enabled_legal_combo',
      pass: g2pass,
      detail: {
        emptyStartDisabled,
        afterIndustryDisabled,
        subjectValue,
        landingViews,
        afterIndustryViews,
        legalViews,
        boundSample,
        startEnabledLegal,
        goals,
        fillLog,
        note: '合法组合=产业「新一代信息技术」+ 有效深圳对比结果绑定 + 主体固定深圳；仅产业仍 disabled，绑有效后 enabled',
      },
      shot: path.relative(outDir, shots.config),
    },
    g3,
    {
      id: 'g4_bio_blacklist',
      pass: true,
      detail: {
        note: '「生物」列入成功路径黑名单：仅联动探测，禁止依赖其开始分析成功结果（INPUT_OBJECT_INVALID / 无有效绑定风险）',
        bioSelected,
        afterBio: { views: afterBioViews, startEnabled: afterBioStart },
        blacklist: ['生物'],
        industry_options_sample: indOpts.slice(0, 12),
      },
      shot: path.relative(outDir, shots.bio),
    },
    {
      id: 'g5_completed_task_view_result',
      pass: enabledView >= 1 && hasDoneRow,
      detail: {
        viewCount,
        enabledView,
        disabledView,
        hasDoneRow,
        emptyRecords,
        failOnly,
        sample: mainText.slice(0, 600),
      },
      shot: path.relative(outDir, shots.records),
    },
  ];

  const g2 = gates.find((g) => g.id === 'g2_start_enabled_legal_combo');
  const g5 = gates.find((g) => g.id === 'g5_completed_task_view_result');
  let overall = 'fail';
  if (g1pass && g2?.pass) {
    overall = g5?.pass ? 'pass' : 'partial';
  }

  const tickets = [];
  if (!g5?.pass) tickets.push('ENV-CHAIN-SZ-DEV-NO-DONE-TASK');
  if (!g2?.pass) tickets.push('ENV-CHAIN-SZ-DEV-START-DISABLED');
  if (!g1pass) tickets.push('ENV-CHAIN-SZ-DEV-DEEP-LINK');

  const envGate = {
    entry_id: 'chain-sz-dev',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall,
    gates,
    tickets,
    implications: {
      gold_config_gate: g2?.pass ? 'allowed — 配置空态/门控/主体锁定/绑定可进金样' : 'blocked',
      gold_process_trigger: g2?.pass
        ? 'allowed_lite — 仅断言开始分析 enabled + 显式点击；过程 UI / 单飞 / 复用降 B'
        : 'forbidden',
      gold_result_state: g5?.pass ? 'allowed' : 'forbidden — 结果态仅 B 档 skip+ticket',
      bio_combo: 'blacklisted for success-path analysis',
      ticket_env_no_done: 'ENV-CHAIN-SZ-DEV-NO-DONE-TASK',
      gold_suggest:
        'P0-01(00754入口) · P0-02(00756产业) · P0-03(00758主体) · P0-04(00759绑定占位) · P0-05(00761门控)；剔除 P0-06 过程发起与结果链',
    },
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2));
  console.log(
    JSON.stringify(
      {
        overall: envGate.overall,
        tickets,
        gates: gates.map((g) => ({ id: g.id, pass: g.pass, n_a: g.n_a || false })),
        boundSample,
        startEnabledLegal,
      },
      null,
      2,
    ),
  );
} catch (e) {
  const fail = {
    entry_id: 'chain-sz-dev',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall: 'fail',
    error: String(e && e.stack ? e.stack : e),
    tickets: ['ENV-CHAIN-SZ-DEV-PROBE-CRASH'],
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2));
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
