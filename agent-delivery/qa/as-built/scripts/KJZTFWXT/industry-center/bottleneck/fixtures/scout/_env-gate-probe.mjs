#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · chain-bottleneck。产物落同目录；勿当 runner。
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
const route = '/industry-center/diagnosis?workspace=bottleneck&tab=bottleneck';
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

  // 若落在诊断记录 Tab，先切回配置
  const tabMain = page.getByRole('tab', { name: '产业瓶颈堵点识别' });
  if ((await tabMain.getAttribute('aria-selected')) !== 'true') {
    await tabMain.click();
    await page.waitForTimeout(1000);
  }
  const loginOk = !page.url().includes('/login');
  const deepUrl = page.url();
  const deepOk =
    /\/industry-center\/diagnosis/.test(deepUrl) &&
    /workspace=bottleneck/.test(deepUrl);
  shots.deep = path.join(outDir, 'env-gate-deep.png');
  await page.screenshot({ path: shots.deep, fullPage: false });

  const cluster = page.locator('.arco-select-view[aria-label="集群"]');
  const chain = page.locator('.arco-select-view[aria-label="产业"]');
  const seg = page.locator('.industry-catalog-select .arco-select-view, .industry-catalog-select').first();
  const start = page.getByRole('button', { name: '开始分析' }).first();

  const readView = async (loc) => {
    const title = (await loc.getAttribute('title')) || '';
    const value = await loc
      .locator('.arco-select-view-value, .arco-select-view-single')
      .first()
      .innerText()
      .catch(() => '');
    const raw = (await loc.innerText().catch(() => '')) || '';
    return (title || value || raw).replace(/\s+/g, ' ').trim();
  };
  const readTriple = async () => ({
    cluster: await readView(cluster),
    chain: await readView(chain),
    segment: await readView(seg),
  });

  const landing = await readTriple();
  const startEnabledLanding = await start.isEnabled();

  // 显式选合法组合：新一代信息技术 / INB1701 / 半导体与集成电路
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
    // 若链仍空再试一次（联动延迟）
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

  // 生物组合：列入黑名单探测（只切对象，不点开始分析依赖成功）
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

  // 切回合法组合（供后续脚本假设）
  await pickOption(cluster, /^新一代信息技术$/);
  await pickOption(chain, /INB1701/);
  const segView2 = page.locator('.industry-catalog-select .arco-select-view').first();
  if (await segView2.count()) await pickOption(segView2, /半导体与集成电路/);

  // 诊断记录：已完成可查看结果？
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

  // 核心：合法组合选齐后「开始分析」enabled；集群文案偶发 title 空则用链+细分+enabled 判定
  const g2pass =
    startEnabledLegal === true &&
    /INB1701/.test(legal.chain) &&
    /半导体/.test(legal.segment) &&
    (/新一代信息技术/.test(legal.cluster) || legal.cluster === '' || startEnabledLanding === true);

  const gates = [
    {
      id: 'g1_login_deep',
      pass: loginOk && deepOk,
      detail: { loginOk, deepOk, url: deepUrl },
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
      detail: { viewCount, enabledView, disabledView, hasDoneRow, failOnly, sample: mainText.slice(0, 400) },
      shot: path.relative(outDir, shots.records),
    },
  ];

  const g2 = gates.find((g) => g.id === 'g2_start_enabled_legal_combo');
  const g5 = gates.find((g) => g.id === 'g5_completed_task_view_result');
  let overall = 'fail';
  if (gates.find((g) => g.id === 'g1_login_deep')?.pass && g2?.pass) {
    overall = g5?.pass ? 'pass' : 'partial';
  }

  const envGate = {
    entry_id: 'chain-bottleneck',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall,
    gates,
    implications: {
      gold_result_state: g5?.pass ? 'allowed' : 'forbidden — 结果态仅 B 档 skip+ticket',
      process_ui: '过程 UI 深验不进金样；开始分析仅断言 enabled/显式触发/切对象不自动起',
      bio_combo: 'blacklisted for success-path analysis',
      ticket_env_no_done: 'ENV-CHAIN-BOTTLENECK-NO-DONE-TASK',
    },
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2));
  console.log(JSON.stringify({ overall: envGate.overall, gates: gates.map((g) => ({ id: g.id, pass: g.pass })) }, null, 2));
} finally {
  await browser.close();
}
