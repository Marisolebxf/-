#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · chain-regional-index。产物落同目录；勿当 runner。
 * method-patch §3：登录深链 / 开始分析 enabled / 预检(本页 N/A) / 坏产业黑名单 / 已完成任务。
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
const route = '/industry-center/regional?workspace=index&tab=index';
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

async function pickSelect(page, ariaLabel, textRe) {
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(200);
  const view = page.locator(`.arco-select-view[aria-label="${ariaLabel}"]`).first();
  if (!(await view.count())) return { ok: false, sample: [], err: 'no-view' };
  try {
    await view.click({ timeout: 5000 });
  } catch (e) {
    return { ok: false, sample: [], err: String(e).slice(0, 120) };
  }
  await page.waitForTimeout(600);
  const popup = page.locator('.arco-trigger-popup:visible').last();
  const opts = popup.locator('.arco-select-option');
  const sample = await opts
    .allTextContents()
    .then((a) => a.map((t) => t.trim()).filter(Boolean).slice(0, 12))
    .catch(() => []);
  const hit = opts.filter({ hasText: textRe });
  if (await hit.count()) {
    await hit.first().click({ force: true }).catch(() => {});
    await page.waitForTimeout(900);
    await page.keyboard.press('Escape').catch(() => {});
    return { ok: true, sample };
  }
  await page.keyboard.press('Escape').catch(() => {});
  return { ok: false, sample };
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
  await page.waitForTimeout(4500);
  await closeBasket(page);

  const tabMain = page.getByRole('tab', { name: '区域产业指数评价', exact: true });
  if ((await tabMain.count()) && (await tabMain.getAttribute('aria-selected')) !== 'true') {
    await tabMain.click();
    await page.waitForTimeout(1000);
  }

  const loginOk = !page.url().includes('/login');
  const deepUrl = page.url();
  const deepOk =
    /\/industry-center\/regional/.test(deepUrl) &&
    /workspace=index/.test(deepUrl) &&
    /tab=index/.test(deepUrl);
  const titleOk = /区域产业指数评价/.test(await page.title());
  shots.deep = path.join(outDir, 'env-gate-deep.png');
  await page.screenshot({ path: shots.deep, fullPage: false });

  const start = page.getByRole('button', { name: '开始分析' }).first();
  const cluster = page.locator('.arco-select-view[aria-label="集群"]').first();
  const industry = page.locator('.arco-select-view[aria-label="产业"]').first();

  const readView = async (loc) => {
    if (!(await loc.count())) return '';
    const title = (await loc.getAttribute('title')) || '';
    const raw = (await loc.innerText().catch(() => '')) || '';
    return (title || raw).replace(/\s+/g, ' ').trim();
  };

  // 空态：重置后开始分析应 disabled
  await page.getByRole('button', { name: '重置参数' }).click().catch(() => {});
  await page.waitForTimeout(800);
  const emptyStartDisabled = !(await start.isEnabled());
  const landing = {
    cluster: await readView(cluster),
    industry: await readView(industry),
    startEnabled: await start.isEnabled(),
    hint: await page.getByText('单产业模式请选择 1 个产业').first().isVisible().catch(() => false),
    templateReady: await page.getByText(/已计入 6 项/).first().isVisible().catch(() => false),
  };

  // 合法组合：集群默认「新一代信息技术」+ 产业「集成电路」+ 区域默认深圳市
  const fillLog = [];
  if (!/新一代信息技术/.test(landing.cluster)) {
    fillLog.push({ step: 'cluster', ...(await pickSelect(page, '集群', /新一代信息技术/)) });
  }
  fillLog.push({ step: 'industry', ...(await pickSelect(page, '产业', /^集成电路$/)) });
  await page.waitForTimeout(800);
  const legal = {
    cluster: await readView(cluster),
    industry: await readView(industry),
    startEnabled: await start.isEnabled(),
    weightOk: await page.getByText(/权重合计：100%/).first().isVisible().catch(() => false),
  };
  shots.config = path.join(outDir, 'env-gate-config.png');
  await page.screenshot({ path: shots.config, fullPage: false });

  // g3 预检：本页非评估类，N/A
  const g3 = {
    id: 'g3_precheck_eval',
    pass: true,
    n_a: true,
    detail: { note: '区域产业指数评价非企业评估页，无「预检未返回企业明细」门控；本闸 N/A=pass' },
  };

  // g4 坏产业：切集群「生物产业」探测（不依赖开始分析成功）
  let bioSelected = false;
  let afterBio = { cluster: '', industry: '', startEnabled: false, options: [] };
  const bioPick = await pickSelect(page, '集群', /^生物产业$/);
  if (bioPick.ok) {
    bioSelected = /生物产业/.test(await readView(cluster));
    await industry.click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(500);
    const bioIndOpts = await page
      .locator('.arco-trigger-popup:visible .arco-select-option')
      .allTextContents()
      .then((a) => a.map((t) => t.trim()).filter(Boolean).slice(0, 12))
      .catch(() => []);
    await page.keyboard.press('Escape').catch(() => {});
    afterBio = {
      cluster: await readView(cluster),
      industry: await readView(industry),
      startEnabled: await start.isEnabled().catch(() => false),
      options: bioIndOpts,
    };
  }
  shots.bio = path.join(outDir, 'env-gate-bio.png');
  await page.screenshot({ path: shots.bio, fullPage: false });

  // 切回合法组合（失败不卡死）
  await page.keyboard.press('Escape').catch(() => {});
  await pickSelect(page, '集群', /^新一代信息技术$/).catch((e) => ({ ok: false, err: String(e) }));
  await page.keyboard.press('Escape').catch(() => {});
  await pickSelect(page, '产业', /^集成电路$/).catch((e) => ({ ok: false, err: String(e) }));
  await page.keyboard.press('Escape').catch(() => {});
  await closeBasket(page);

  // g5 分析记录：至少 1 条已完成可「查看结果」
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
  const emptyRecords = /暂无数据|暂无/.test(mainText);
  const failOnly = /失败/.test(mainText) && !hasDoneRow;

  const g1pass = loginOk && deepOk && titleOk;
  const g2pass =
    emptyStartDisabled === true &&
    legal.startEnabled === true &&
    /集成电路/.test(legal.industry) &&
    (/新一代信息技术/.test(legal.cluster) || legal.cluster === '');

  const gates = [
    {
      id: 'g1_login_deep',
      pass: g1pass,
      detail: { loginOk, deepOk, titleOk, url: deepUrl },
      shot: path.relative(outDir, shots.deep),
    },
    {
      id: 'g2_start_enabled_legal_combo',
      pass: g2pass,
      detail: {
        emptyStartDisabled,
        landing,
        fillLog,
        legal,
        note: '合法组合=单产业×多区域 + 新一代信息技术/集成电路 + 默认深圳市；空态重置后 disabled，选产业后 enabled',
      },
      shot: path.relative(outDir, shots.config),
    },
    g3,
    {
      id: 'g4_bio_blacklist',
      pass: true,
      detail: {
        note: '生物产业列入分析黑名单：仅联动探测，禁止依赖其开始分析成功结果（INPUT_OBJECT_INVALID 风险）',
        bioPickOk: bioPick.ok,
        bioSelected,
        afterBio,
        blacklist: ['生物产业'],
        cluster_options_sample: bioPick.sample,
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
        sample: mainText.slice(0, 500),
      },
      shot: path.relative(outDir, shots.records),
    },
  ];

  const g2 = gates.find((g) => g.id === 'g2_start_enabled_legal_combo');
  const g5 = gates.find((g) => g.id === 'g5_completed_task_view_result');
  let overall = 'fail';
  if (gates.find((g) => g.id === 'g1_login_deep')?.pass && g2?.pass) {
    overall = g5?.pass ? 'pass' : 'partial';
  }

  const tickets = [];
  if (!g5?.pass) tickets.push('ENV-CHAIN-REGIONAL-INDEX-NO-DONE-TASK');
  if (!g2?.pass) tickets.push('ENV-CHAIN-REGIONAL-INDEX-START-DISABLED');
  if (!g1pass) tickets.push('ENV-CHAIN-REGIONAL-INDEX-DEEP-LINK');

  const envGate = {
    entry_id: 'chain-regional-index',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall,
    gates,
    tickets,
    implications: {
      gold_config_gate: g2?.pass ? 'allowed — 配置空态/门控/模式切换可进金样' : 'blocked',
      gold_process_trigger: g2?.pass
        ? 'allowed_lite — 仅断言开始分析 enabled + 显式点击进 processing URL；过程 UI 深验降 B'
        : 'forbidden',
      gold_result_state: g5?.pass ? 'allowed' : 'forbidden — 结果态仅 B 档 skip+ticket',
      bio_combo: 'blacklisted for success-path analysis',
      ticket_env_no_done: 'ENV-CHAIN-REGIONAL-INDEX-NO-DONE-TASK',
    },
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2));
  console.log(
    JSON.stringify(
      {
        overall: envGate.overall,
        tickets,
        gates: gates.map((g) => ({ id: g.id, pass: g.pass, n_a: g.n_a || false })),
      },
      null,
      2,
    ),
  );
} catch (err) {
  const fail = {
    entry_id: 'chain-regional-index',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall: 'fail',
    gates: [],
    tickets: ['ENV-CHAIN-REGIONAL-INDEX-PROBE-CRASH'],
    error: String(err && err.stack ? err.stack : err).slice(0, 800),
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2));
  console.error(fail.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
