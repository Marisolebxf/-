#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · chain-key-link。产物落同目录；勿当 runner。
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
const route = '/industry-center/diagnosis?workspace=key_link&tab=key-link';
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

  const tabMain = page.getByRole('tab', { name: '产业关键环节识别' });
  if ((await tabMain.getAttribute('aria-selected')) !== 'true') {
    await tabMain.click();
    await page.waitForTimeout(1000);
  }
  const loginOk = !page.url().includes('/login');
  const deepUrl = page.url();
  const deepOk =
    /\/industry-center\/diagnosis/.test(deepUrl) &&
    /workspace=key_link/.test(deepUrl);
  const title = await page.title();
  const titleOk = /产业关键环节识别/.test(title);
  shots.deep = path.join(outDir, 'env-gate-deep.png');
  await page.screenshot({ path: shots.deep, fullPage: false });

  const cluster = page.locator('.arco-select-view[aria-label="集群"]');
  const chain = page.locator('.arco-select-view[aria-label="产业"]');
  const seg = page.locator('.industry-catalog-select .arco-select-view, .industry-catalog-select').first();
  const start = page.getByRole('button', { name: '开始分析' }).first();

  const readView = async (loc) => {
    const t = (await loc.getAttribute('title')) || '';
    const value = await loc
      .locator('.arco-select-view-value, .arco-select-view-single')
      .first()
      .innerText()
      .catch(() => '');
    const raw = (await loc.innerText().catch(() => '')) || '';
    return (t || value || raw).replace(/\s+/g, ' ').trim();
  };
  const readTriple = async () => ({
    cluster: await readView(cluster),
    chain: await readView(chain),
    segment: await readView(seg),
  });

  const landing = await readTriple();
  const startEnabledLanding = await start.isEnabled();

  async function pickOption(view, textRe) {
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(200);
    await view.click({ timeout: 8000 });
    await page.waitForTimeout(600);
    const popup = page.locator('.arco-trigger-popup:visible');
    const opt = popup.locator('.arco-select-option').filter({ hasText: textRe });
    const n = await opt.count();
    const sample = await popup
      .locator('.arco-select-option')
      .allTextContents()
      .then((a) => a.slice(0, 8))
      .catch(() => []);
    if (n) {
      await opt.first().click();
      await page.waitForTimeout(900);
      return { ok: true, sample };
    }
    await page.keyboard.press('Escape').catch(() => {});
    return { ok: false, sample };
  }

  const fillLog = [];
  let legalFilled = false;
  if (!/新一代信息技术/.test(landing.cluster) || !/INB1701/.test(landing.chain) || !/半导体/.test(landing.segment)) {
    fillLog.push(await pickOption(cluster, /新一代信息技术/));
    fillLog.push(await pickOption(chain, /INB1701/));
    const segView = page.locator('.industry-catalog-select .arco-select-view').first();
    if (await segView.count()) {
      fillLog.push(await pickOption(segView, /半导体与集成电路/));
    }
    let mid = await readTriple();
    if (!/INB1701/.test(mid.chain)) {
      fillLog.push({ retry: true, ...(await pickOption(chain, /INB1701/)) });
    }
    mid = await readTriple();
    if (!/半导体/.test(mid.segment)) {
      const segView2 = page.locator('.industry-catalog-select .arco-select-view').first();
      if (await segView2.count()) fillLog.push({ retry: true, ...(await pickOption(segView2, /半导体/)) });
    }
    legalFilled = true;
  }
  const legal = await readTriple();
  const startEnabledLegal = await start.isEnabled();
  shots.config = path.join(outDir, 'env-gate-config.png');
  await page.screenshot({ path: shots.config, fullPage: false });

  await cluster.click({ timeout: 8000 });
  await page.waitForTimeout(400);
  const bioOpt = page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: /^生物产业$/ });
  let bioSelected = false;
  if (await bioOpt.count()) {
    await bioOpt.first().click();
    await page.waitForTimeout(900);
    bioSelected = /生物产业/.test((await cluster.innerText()) || '');
  }
  const afterBio = {
    ...(await readTriple()),
    startEnabled: await start.isEnabled().catch(() => false),
  };
  shots.bio = path.join(outDir, 'env-gate-bio.png');
  await page.screenshot({ path: shots.bio, fullPage: false });

  await pickOption(cluster, /^新一代信息技术$/);
  await pickOption(chain, /INB1701/);
  const segView2 = page.locator('.industry-catalog-select .arco-select-view').first();
  if (await segView2.count()) await pickOption(segView2, /半导体与集成电路/);

  await page.getByRole('tab', { name: '诊断记录' }).click();
  await page.waitForTimeout(1200);
  shots.records = path.join(outDir, 'env-gate-records.png');
  await page.screenshot({ path: shots.records, fullPage: false });
  const mainText = await page.locator('main').first().innerText();
  const viewBtns = page.getByRole('button', { name: '查看结果' });
  const viewCount = await viewBtns.count();
  let enabledView = 0;
  let disabledView = 0;
  for (let i = 0; i < viewCount; i++) {
    if (await viewBtns.nth(i).isDisabled()) disabledView++;
    else enabledView++;
  }
  const hasDoneRow = /已完成|成功/.test(mainText);
  const failOnly = /失败/.test(mainText) && !hasDoneRow;
  const emptyRecords = /暂无数据/.test(mainText);

  const g2pass =
    startEnabledLegal === true &&
    /INB1701/.test(legal.chain) &&
    /半导体/.test(legal.segment) &&
    (/新一代信息技术/.test(legal.cluster) || legal.cluster === '' || startEnabledLanding === true);

  const gates = [
    {
      id: 'g1_login_deep',
      pass: loginOk && deepOk && titleOk,
      detail: { loginOk, deepOk, titleOk, title, url: deepUrl },
      shot: path.relative(outDir, shots.deep),
    },
    {
      id: 'g2_start_enabled_legal_combo',
      pass: g2pass,
      detail: {
        landing,
        startEnabledLanding,
        legalFilled,
        fillLog,
        legal,
        startEnabledLegal,
        note: '合法组合=新一代信息技术/INB1701/半导体与集成电路；落地若空则显式选齐后再判 enabled',
      },
      shot: path.relative(outDir, shots.config),
    },
    {
      id: 'g3_precheck_eval',
      pass: true,
      n_a: true,
      detail: {
        note: '产业关键环节识别非企业评估页，无「预检未返回企业明细」门控；本闸 N/A=pass',
      },
    },
    {
      id: 'g4_bio_blacklist',
      pass: true,
      detail: {
        note: '生物产业列入分析黑名单：仅联动探测，禁止依赖其开始分析成功结果（INPUT_OBJECT_INVALID 风险）',
        bioSelected,
        afterBio,
        blacklist: ['生物产业'],
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

  const g1 = gates.find((g) => g.id === 'g1_login_deep');
  const g2 = gates.find((g) => g.id === 'g2_start_enabled_legal_combo');
  const g5 = gates.find((g) => g.id === 'g5_completed_task_view_result');
  let overall = 'fail';
  if (g1?.pass && g2?.pass) {
    overall = g5?.pass ? 'pass' : 'partial';
  }

  const tickets = [];
  if (!g5?.pass) tickets.push('ENV-CHAIN-KEY-LINK-NO-DONE-TASK');

  const envGate = {
    entry_id: 'chain-key-link',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall,
    gates,
    tickets,
    implications: {
      gold_config_gate: 'allowed — 入口/默认三级/权重只读/开始分析门控可进金样',
      gold_process_trigger:
        'allowed_lite — 仅断言开始分析 enabled + 显式点击/切对象不自动起；过程阶段文案深验降 B',
      gold_result_state: g5?.pass
        ? 'allowed — 有已完成任务可「查看结果」；结果深验可进金样或 B'
        : 'forbidden — 结果态仅 B 档 skip+ticket',
      bio_combo: 'blacklisted for success-path analysis',
      ticket_env_no_done: g5?.pass ? null : 'ENV-CHAIN-KEY-LINK-NO-DONE-TASK',
      gold_suggest_note:
        '建议金样仅配置/门控主路径；现行 gold 含 P0-05 结果态且 allow_skip，应按闸门结果保留或降 B',
    },
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2));
  console.log(
    JSON.stringify(
      {
        overall: envGate.overall,
        tickets: envGate.tickets,
        gates: gates.map((g) => ({ id: g.id, pass: g.pass, n_a: g.n_a || false })),
      },
      null,
      2,
    ),
  );
} catch (err) {
  const fail = {
    entry_id: 'chain-key-link',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall: 'fail',
    gates: [{ id: 'probe_error', pass: false, detail: { message: String(err?.message || err) } }],
    tickets: ['ENV-CHAIN-KEY-LINK-PROBE-ERROR'],
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2));
  console.error(err);
  process.exitCode = 1;
} finally {
  await browser.close();
}
