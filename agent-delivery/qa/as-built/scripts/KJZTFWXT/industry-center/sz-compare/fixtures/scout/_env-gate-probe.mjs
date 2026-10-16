#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · chain-sz-compare。产物落同目录；勿当 runner。
 * method-patch §3：登录深链 / 合法组合后开始分析 enabled / 预检 N/A / 生物黑名单 / 已完成可查看结果。
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
const route = '/industry-center/shenzhen?workspace=comparison&tab=comparison';
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

async function readSelect(page, aria) {
  const view = page.locator(`.arco-select-view[aria-label="${aria}"]`).first();
  if (!(await view.count())) return { text: '', placeholder: '', exists: false };
  const text = ((await view.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  const ph = (await view.locator('input').getAttribute('placeholder').catch(() => '')) || '';
  return { text, placeholder: ph, exists: true };
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

  const tabMain = page.getByRole('tab', { name: '深圳产业情况分析对比' });
  if ((await tabMain.count()) && (await tabMain.first().getAttribute('aria-selected')) !== 'true') {
    await tabMain.first().click();
    await page.waitForTimeout(1000);
  }

  const loginOk = !page.url().includes('/login');
  const deepUrl = page.url();
  const deepOk =
    /\/industry-center\/shenzhen/.test(deepUrl) &&
    /workspace=comparison/.test(deepUrl) &&
    /tab=comparison/.test(deepUrl);
  const title = await page.title();
  const titleOk = /深圳产业情况分析对比/.test(title);
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

  const landingCluster = await readSelect(page, '集群');
  const landingIndustry = await readSelect(page, '产业');
  const fillLog = [];

  // 标杆区域（无稳定 aria-label；用 placeholder 含 Q016 的 select）
  const allViews = page.locator('main .arco-select-view');
  let benchmarkPh = '';
  let benchmarkText = '';
  const viewN = await allViews.count();
  for (let i = 0; i < viewN; i++) {
    const el = allViews.nth(i);
    const aria = (await el.getAttribute('aria-label').catch(() => '')) || '';
    if (aria === '集群' || aria === '产业') continue;
    const ph = (await el.locator('input').getAttribute('placeholder').catch(() => '')) || '';
    const txt = ((await el.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
    if (/Q016|标杆|沪|京|苏州/.test(ph + txt) || (!aria && ph)) {
      benchmarkPh = ph;
      benchmarkText = txt;
      break;
    }
  }
  const benchmarkEmpty = /Q016|为空|未定/.test(benchmarkPh) || (!benchmarkText && /Q016|为空|未定/.test(benchmarkPh));

  // 确保集群=新一代信息技术
  await page.keyboard.press('Escape').catch(() => {});
  const clusterView = page.locator('.arco-select-view[aria-label="集群"]').first();
  await clusterView.click({ timeout: 8000 });
  await page.waitForTimeout(500);
  const clusterPopup = page.locator('.arco-trigger-popup:visible');
  const clusterOpts = await clusterPopup.locator('.arco-select-option').allTextContents().catch(() => []);
  const pickCluster = clusterPopup.locator('.arco-select-option').filter({ hasText: '新一代信息技术' });
  const clusterOk = (await pickCluster.count()) > 0;
  if (clusterOk) {
    await pickCluster.first().click();
    await page.waitForTimeout(800);
  } else {
    await page.keyboard.press('Escape').catch(() => {});
  }
  fillLog.push({ step: 'cluster', ok: clusterOk, sample: clusterOpts.slice(0, 8) });

  // 选产业（首个可用选项，优先集成电路）
  await page.keyboard.press('Escape').catch(() => {});
  const indView = page.locator('.arco-select-view[aria-label="产业"]').first();
  await indView.click({ timeout: 8000 });
  await page.waitForTimeout(600);
  const indPopup = page.locator('.arco-trigger-popup:visible');
  const indOpts = await indPopup.locator('.arco-select-option').allTextContents().catch(() => []);
  let pickedIndustry = '';
  const prefer = indPopup.locator('.arco-select-option').filter({ hasText: /集成电路|半导体/ });
  const anyInd = indPopup.locator('.arco-select-option').first();
  if ((await prefer.count()) > 0) {
    pickedIndustry = ((await prefer.first().innerText()) || '').replace(/\s+/g, ' ').trim();
    await prefer.first().click();
    await page.waitForTimeout(900);
  } else if ((await anyInd.count()) > 0) {
    pickedIndustry = ((await anyInd.innerText()) || '').replace(/\s+/g, ' ').trim();
    await anyInd.click();
    await page.waitForTimeout(900);
  }
  fillLog.push({
    step: 'industry',
    ok: !!pickedIndustry,
    picked: pickedIndustry,
    sample: indOpts.slice(0, 8),
  });

  const afterIndustry = {
    cluster: await readSelect(page, '集群'),
    industry: await readSelect(page, '产业'),
    startDisabled: await start.isDisabled(),
    startEnabled: await start.isEnabled(),
  };
  const startEnabledLegal = afterIndustry.startEnabled === true;

  shots.config = path.join(outDir, 'env-gate-config.png');
  await page.screenshot({ path: shots.config, fullPage: false });

  const g3 = {
    id: 'g3_precheck_eval',
    pass: true,
    n_a: true,
    detail: { note: '深圳产业情况分析对比非企业评估页，无「预检未返回企业明细」门控；本闸 N/A=pass' },
  };

  // g4 生物产业：仅联动探测
  if (await reset.count()) {
    await reset.click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(600);
  }
  await page.keyboard.press('Escape').catch(() => {});
  await clusterView.click({ timeout: 8000 });
  await page.waitForTimeout(500);
  const bioClusterPopup = page.locator('.arco-trigger-popup:visible');
  const bioCluster = bioClusterPopup.locator('.arco-select-option').filter({ hasText: /生物/ });
  let bioSelected = false;
  let afterBio = { cluster: '', industry: '', startEnabled: null };
  if (await bioCluster.count()) {
    await bioCluster.first().click();
    await page.waitForTimeout(800);
    bioSelected = true;
    await page.keyboard.press('Escape').catch(() => {});
    await indView.click({ timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(400);
    const bioIndPopup = page.locator('.arco-trigger-popup:visible');
    const firstBioInd = bioIndPopup.locator('.arco-select-option').first();
    if (await firstBioInd.count()) {
      await firstBioInd.click().catch(() => {});
      await page.waitForTimeout(600);
    } else {
      await page.keyboard.press('Escape').catch(() => {});
    }
    afterBio = {
      cluster: (await readSelect(page, '集群')).text,
      industry: (await readSelect(page, '产业')).text,
      startEnabled: await start.isEnabled(),
    };
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
  // §3.2：合法对象选齐后开始分析须 enabled。本页合法=集群+产业+标杆≥1；Q016 标杆恒空 → 无法 enabled → g2 fail
  const g2pass = startEnabledLegal === true && subjectValue === '深圳' && !!pickedIndustry;

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
        subjectValue,
        landing: { cluster: landingCluster, industry: landingIndustry },
        afterIndustry,
        benchmark: { placeholder: benchmarkPh, text: benchmarkText, empty: benchmarkEmpty },
        startEnabledLegal,
        fillLog,
        note:
          '合法组合=集群「新一代信息技术」+ 产业已选 + 标杆≥1 + 主体深圳；现场标杆 Q016 恒空 → 选产业后开始分析仍 disabled',
      },
      shot: path.relative(outDir, shots.config),
    },
    g3,
    {
      id: 'g4_bio_blacklist',
      pass: true,
      detail: {
        note: '生物/生物产业列入成功路径黑名单：仅联动探测，禁止依赖其开始分析成功（INPUT_OBJECT_INVALID / 标杆空叠加）',
        bioSelected,
        afterBio,
        blacklist: ['生物', '生物产业'],
        cluster_options_sample: clusterOpts.slice(0, 12),
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
  } else if (g1pass && !g2?.pass && g5?.pass) {
    // 配置门控可测、过程不可起，但历史结果可看 → overall 仍 fail（§3.2 不过禁写过程），partial 留给 g2 通 g5 不通
    overall = 'fail';
  }

  const tickets = [];
  if (!g1pass) tickets.push('ENV-CHAIN-SZ-COMPARE-DEEP-LINK');
  if (!g2?.pass) tickets.push('ENV-CHAIN-SZ-COMPARE-BENCHMARK-EMPTY-Q016');
  if (!g5?.pass) tickets.push('ENV-CHAIN-SZ-COMPARE-NO-DONE-TASK');

  const envGate = {
    entry_id: 'chain-sz-compare',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall,
    gates,
    tickets,
    implications: {
      gold_config_gate:
        g1pass
          ? 'allowed — 入口/双级对象/主体锁定/标杆诚实空/维度只读/开始分析 disabled 门控可进金样'
          : 'blocked',
      gold_process_trigger: g2?.pass
        ? 'allowed_lite — 仅断言开始分析 enabled + 显式点击；过程 UI 降 B'
        : 'forbidden — Q016 标杆空，开始分析无法 enabled',
      gold_result_state: g5?.pass
        ? 'allowed_via_history — 过程触发禁入金样，但从分析记录「查看结果」可读结果态（宜 B 或独立历史金样）'
        : 'forbidden — 结果态仅 B 档 skip+ticket',
      bio_combo: 'blacklisted for success-path analysis',
      ticket_env_benchmark: 'ENV-CHAIN-SZ-COMPARE-BENCHMARK-EMPTY-Q016',
      ticket_env_no_done: g5?.pass ? null : 'ENV-CHAIN-SZ-COMPARE-NO-DONE-TASK',
      method_patch_ref: 'agent-delivery/qa/as-built/retro/20261014-batch32-method-patch.md §3',
      gold_suggest: {
        keep: ['P0-01', 'P0-02', 'P0-03', 'P0-04'],
        demote_from_gold: ['P0-05'],
        promote_to_gold: ['P0-06', 'P0-09'],
        note:
          '现行 gold=P0-01..05。g2 fail（Q016）→ 过程触发禁入 A；P0-05 含 allow_skip 违 A 档零 skip，建议降 B。替入无 skip 的 P0-06（双 Tab）+ P0-09（对比维度构成）作第 5/可选第 6 槽；或金样缩为 4 条仅配置门控。结果链依赖历史可看（g5），但 P1-04/05 等仍挂 allow_skip，保持 B。',
      },
      forbid_gold_reasons: {
        'P0-05': 'A 档禁止 allow_skip；且依赖开始分析 enabled（环境 Q016 不通）',
        'P0-11/P0-12': '门控/禁发起 — 可作 B；与 P0-04/空态重叠',
        'P1-03/P1-04/P1-05': '过程/结果/重跑 + allow_skip',
        bio_success_path: '生物产业黑名单；禁止依赖其开始分析成功',
      },
    },
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2));
  console.log(
    JSON.stringify(
      {
        overall: envGate.overall,
        tickets,
        gates: gates.map((g) => ({ id: g.id, pass: g.pass, n_a: g.n_a || false })),
        startEnabledLegal,
        benchmarkEmpty,
        pickedIndustry,
        g5: { enabledView, hasDoneRow },
      },
      null,
      2,
    ),
  );
} catch (e) {
  const fail = {
    entry_id: 'chain-sz-compare',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall: 'fail',
    error: String(e && e.stack ? e.stack : e),
    tickets: ['ENV-CHAIN-SZ-COMPARE-PROBE-CRASH'],
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2));
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
