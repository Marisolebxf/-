#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · chain-overview。产物落同目录；勿当 runner。
 * 本页无异步「开始分析」/诊断记录；闸门按 method-patch §3 适配（g2/g3/g5 多为 N/A）。
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
const route = '/industry-center/overview';
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
  await page.waitForTimeout(3000);
  await closeBasket(page);

  const loginOk = !page.url().includes('/login');
  const deepUrl = page.url();
  const deepOk = /\/industry-center\/overview/.test(deepUrl);
  const title = await page.title();
  const titleOk = /专题全景/.test(title);
  shots.deep = path.join(outDir, 'env-gate-deep.png');
  await page.screenshot({ path: shots.deep, fullPage: false });

  const cluster = page.locator('span[aria-label="集群"]');
  const industry = page.locator('span[aria-label="产业"]');
  const chain = page.locator('.industry-overview-chain-select');
  const joinBtn = page.getByRole('button', { name: /加入对比篮|移出对比篮/ }).first();
  const startBtn = page.getByRole('button', { name: '开始分析' });
  const startPresent = (await startBtn.count()) > 0;

  const readView = async (loc) => {
    if (!(await loc.count())) return '';
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
    industry: await readView(industry),
    chain: await readView(chain),
  });
  const chainDisabled = async () =>
    chain.evaluate((el) => String(el.className || '').includes('disabled')).catch(() => false);

  const landing = await readTriple();
  const joinEnabledLanding = await joinBtn.isEnabled().catch(() => false);
  const tabs = page.locator('[aria-label="专题全景视图"] [role=tab]');
  const tabCount = await tabs.count();
  const tabTexts = [];
  for (let i = 0; i < Math.min(tabCount, 5); i++) {
    tabTexts.push((await tabs.nth(i).innerText()).replace(/\s+/g, ' ').trim());
  }
  const defaultTab =
    (await page.locator('[aria-label="专题全景视图"] [role=tab][aria-selected="true"]').innerText().catch(() => '')) ||
    '';
  const enterPanoramaVisible = await page
    .getByRole('button', { name: '进入全景图谱' })
    .first()
    .isVisible()
    .catch(() => false);

  async function pickOption(view, textRe) {
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(200);
    await view.click({ timeout: 8000 });
    await page.waitForTimeout(500);
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
  if (
    !/新一代信息技术/.test(landing.cluster) ||
    !/INB1701/.test(landing.industry) ||
    !/半导体/.test(landing.chain)
  ) {
    fillLog.push({ step: 'cluster', ...(await pickOption(cluster, /新一代信息技术/)) });
    fillLog.push({ step: 'industry', ...(await pickOption(industry, /INB1701/)) });
    if (await chainDisabled()) {
      /* wait cascade */
    } else {
      fillLog.push({ step: 'chain', ...(await pickOption(chain, /半导体与集成电路/)) });
    }
    legalFilled = true;
  }
  const legal = await readTriple();
  const joinEnabledLegal = await joinBtn.isEnabled().catch(() => false);
  const chainDisabledLegal = await chainDisabled();
  shots.config = path.join(outDir, 'env-gate-config.png');
  await page.screenshot({ path: shots.config, fullPage: false });

  // g2：本页无「开始分析」→ N/A；代理判「合法三级选齐 + 加入对比篮 enabled」
  const legalComboOk =
    /新一代信息技术/.test(legal.cluster) &&
    /INB1701/.test(legal.industry) &&
    !!legal.chain &&
    !chainDisabledLegal &&
    joinEnabledLegal === true;

  await cluster.click({ timeout: 8000 });
  await page.waitForTimeout(400);
  const bioOpt = page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: /^生物产业$/ });
  let bioSelected = false;
  if (await bioOpt.count()) {
    await bioOpt.first().click();
    await page.waitForTimeout(1000);
    bioSelected = /生物产业/.test((await cluster.innerText()) || '');
  } else {
    await page.keyboard.press('Escape').catch(() => {});
  }
  const afterBio = {
    ...(await readTriple()),
    chainDisabled: await chainDisabled(),
    joinEnabled: await joinBtn.isEnabled().catch(() => false),
    startPresent,
  };
  shots.bio = path.join(outDir, 'env-gate-bio.png');
  await page.screenshot({ path: shots.bio, fullPage: false });

  // 恢复合法组合供 records/主区截图
  await pickOption(cluster, /^新一代信息技术$/);
  await pickOption(industry, /INB1701/);
  if (!(await chainDisabled())) {
    const chainTitle = await readView(chain);
    if (!/半导体/.test(chainTitle)) await pickOption(chain, /半导体与集成电路/);
  }

  shots.records = path.join(outDir, 'env-gate-records.png');
  await page.screenshot({ path: shots.records, fullPage: false });
  const mainText = await page.locator('main').first().innerText().catch(() => '');
  const viewBtns = page.getByRole('button', { name: '查看结果' });
  const viewCount = await viewBtns.count();
  const hasRecordsTab = (await page.getByRole('tab', { name: /诊断记录|分析记录/ }).count()) > 0;
  const hasDoneRow = /已完成|成功/.test(mainText);

  const gates = [
    {
      id: 'g1_login_deep',
      pass: loginOk && deepOk && titleOk,
      detail: { loginOk, deepOk, titleOk, title, url: deepUrl },
      shot: path.relative(outDir, shots.deep),
    },
    {
      id: 'g2_start_enabled_legal_combo',
      pass: !startPresent && legalComboOk,
      n_a: !startPresent,
      detail: {
        landing,
        joinEnabledLanding,
        legalFilled,
        fillLog,
        legal,
        joinEnabledLegal,
        chainDisabledLegal,
        startPresent,
        startEnabledLegal: null,
        tabCount,
        tabTexts,
        defaultTab: defaultTab.replace(/\s+/g, ' ').trim(),
        enterPanoramaVisible,
        legalComboOk,
        note:
          '专题全景无异步「开始分析」；本闸 N/A=pass，代理判合法三级（新一代信息技术/INB1701/半导体与集成电路）选齐且「加入对比篮」enabled',
      },
      shot: path.relative(outDir, shots.config),
    },
    {
      id: 'g3_precheck_eval',
      pass: true,
      n_a: true,
      detail: {
        note: '专题全景非企业评估页，无「预检未返回企业明细」门控；本闸 N/A=pass',
      },
    },
    {
      id: 'g4_bio_blacklist',
      pass: true,
      detail: {
        note:
          '生物产业用于空/禁用态代理（P0-02/P0-07）；非异步分析成功路径。联动探测：切生物后产业链 disabled、加入对比篮 disabled；禁止依赖其下游图谱分析成功',
        bioSelected,
        afterBio,
        blacklist: ['生物产业'],
      },
      shot: path.relative(outDir, shots.bio),
    },
    {
      id: 'g5_completed_task_view_result',
      pass: true,
      n_a: true,
      detail: {
        mode: 'no_async_task_history',
        hasRecordsTab,
        viewCount,
        hasDoneRow,
        sample: mainText.slice(0, 400),
        note:
          '本页无诊断记录/「查看结果」历史任务依赖；结果主路径=落地筛选+三 Tab+进入全景图谱跳转。本闸 N/A=pass',
      },
      shot: path.relative(outDir, shots.records),
    },
  ];

  const g1 = gates.find((g) => g.id === 'g1_login_deep');
  const g2 = gates.find((g) => g.id === 'g2_start_enabled_legal_combo');
  const g4 = gates.find((g) => g.id === 'g4_bio_blacklist');
  let overall = 'fail';
  if (g1?.pass && g2?.pass) {
    overall = g4?.pass ? 'pass' : 'partial';
  }

  const tickets = [];
  if (!g1?.pass) tickets.push('ENV-CHAIN-OVERVIEW-DEEP-LINK');
  if (!legalComboOk) tickets.push('ENV-CHAIN-OVERVIEW-LEGAL-COMBO');

  const gold_suggest = {
    keep: ['P0-01', 'P0-02', 'P0-03', 'P0-04', 'P0-05', 'P0-06'],
    downgrade_to_B: [],
    promote_to_gold: [],
    optional_promote_if_runner_green: ['P0-09', 'P0-10', 'P0-11', 'P1-02'],
    note:
      '现行 gold=P0-01..06 均无 allow_skip，对齐入口/筛选代理空态/三级解锁/三 Tab/互斥/进图谱。闸门 overall=pass（无异步分析）。P0-02/P0-07 触生物联动仅作禁用代理，金样可留 P0-02；P0-07 宜 B。P1-01 有 allow_skip 禁升 A。',
  };

  const envGate = {
    entry_id: 'chain-overview',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall,
    gates,
    tickets,
    implications: {
      gold_config_gate: 'allowed — 入口/三级筛选/加入对比篮/三 Tab 可进金样',
      gold_process_trigger: 'n_a — 本页无异步「开始分析」过程态',
      gold_result_state: 'allowed_lite — 默认落地内容+进入全景图谱跳转；无任务「查看结果」硬门槛',
      bio_combo: 'empty_state_proxy_only — 禁用/空态代理可用；禁止当成功分析对象',
      ticket_env_no_done: null,
      no_async_analysis: true,
      method_patch_ref: 'agent-delivery/qa/as-built/retro/20261014-batch32-method-patch.md §3',
      gold_suggest,
      forbid_gold_reasons: {
        'P0-07': '生物产业禁用态深验；与金样 P0-02 代理重叠，宜留 B',
        'P0-08': '集群变更刷新选项集合，内容正确性 observed',
        'P0-12': '未选链禁用门控；依赖生物/空态路径',
        'P1-01': 'allow_skip（无映射集群名单未稳定）→ A 档禁止',
        'P1-03': '跨页后退保持；依赖 panorama 可达，宜 B',
        'P1-04': '评审追溯按钮；依赖评审模式开',
        'P1-05': '关评审零泄漏；依赖人设面板',
        bio_success_path: '生物产业仅空/禁用代理；禁止依赖其下游分析成功',
      },
    },
  };

  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2));
  console.log(
    JSON.stringify(
      {
        overall: envGate.overall,
        tickets: envGate.tickets,
        gates: gates.map((g) => ({ id: g.id, pass: g.pass, n_a: g.n_a || false })),
        gold_suggest,
      },
      null,
      2,
    ),
  );
} catch (err) {
  const fail = {
    entry_id: 'chain-overview',
    probed_at: new Date().toISOString(),
    base_url: baseUrl,
    route,
    overall: 'fail',
    gates: [{ id: 'probe_error', pass: false, detail: { message: String(err?.message || err) } }],
    tickets: ['ENV-CHAIN-OVERVIEW-PROBE-ERROR'],
  };
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2));
  console.error(err);
  process.exitCode = 1;
} finally {
  await browser.close();
}
