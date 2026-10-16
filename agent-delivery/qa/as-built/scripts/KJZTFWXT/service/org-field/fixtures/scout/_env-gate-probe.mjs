#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · svc-org-field。产物落同目录；勿当 runner。
 * 禁止硬点 disabled；失败落 scout json 后继续。
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
const route = '/service/institution-judgment?workspace=field&tab=coverage';
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

async function softClick(page, loc, label, log) {
  const n = await loc.count();
  if (!n) {
    log.push({ step: label, ok: false, reason: 'not_found' });
    return false;
  }
  const el = loc.first();
  const visible = await el.isVisible().catch(() => false);
  const enabled = await el.isEnabled().catch(() => false);
  if (!visible) {
    log.push({ step: label, ok: false, reason: 'not_visible' });
    return false;
  }
  if (!enabled) {
    log.push({ step: label, ok: false, reason: 'disabled', note: 'skip hard click' });
    return false;
  }
  await el.click({ timeout: 5000 }).catch((e) => {
    log.push({ step: label, ok: false, reason: String(e).slice(0, 120) });
    return false;
  });
  log.push({ step: label, ok: true });
  return true;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const clickLog = [];
const scout = { clickLog, stages: {} };

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

  const loginOk = !page.url().includes('/login');
  const deepUrl = page.url();
  const deepOk =
    /\/service\/institution-judgment/.test(deepUrl) &&
    /workspace=field/.test(deepUrl) &&
    /tab=coverage/.test(deepUrl);
  const title = await page.title();
  await page.screenshot({ path: path.join(outDir, 'env-gate-deep.png'), fullPage: false });

  const start = page.getByRole('button', { name: '开始分析' }).first();
  const selectBtn = page.getByRole('button', { name: '选择机构' }).first();
  const startEmpty = {
    visible: await start.isVisible().catch(() => false),
    enabled: await start.isEnabled().catch(() => false),
    class: await start.getAttribute('class').catch(() => null),
  };
  const emptyHint = /请先选择分析机构|未选择机构|已选机构（0/.test(
    (await page.locator('main').first().innerText().catch(() => '')) || '',
  );
  scout.stages.empty = { startEmpty, emptyHint };

  // 选机构：打开弹窗 → 勾选前 2 个 checkbox → 确定（禁用则跳过）
  let selectOk = false;
  let orgsSelected = 0;
  let startAfterSelect = { enabled: false };
  if (await softClick(page, selectBtn, '选择机构', clickLog)) {
    await page.waitForTimeout(800);
    const dialog = page.locator('.arco-modal, [role="dialog"]').filter({ hasText: '选择服务机构' }).first();
    const dialogVisible = await dialog.isVisible().catch(() => false);
    scout.stages.modal = { dialogVisible };
    if (dialogVisible) {
      const checks = dialog.locator('.arco-checkbox:not(.arco-checkbox-disabled) input[type=checkbox], label.arco-checkbox');
      const cn = await checks.count();
      const toPick = Math.min(2, cn);
      for (let i = 0; i < toPick; i++) {
        const c = checks.nth(i);
        const en = await c.isEnabled().catch(() => true);
        if (!en) {
          clickLog.push({ step: `checkbox[${i}]`, ok: false, reason: 'disabled' });
          continue;
        }
        await c.click({ timeout: 3000 }).catch((e) => {
          clickLog.push({ step: `checkbox[${i}]`, ok: false, reason: String(e).slice(0, 80) });
        });
        clickLog.push({ step: `checkbox[${i}]`, ok: true });
        orgsSelected++;
      }
      const confirm = dialog.getByRole('button', { name: '确定' });
      if (await softClick(page, confirm, '弹窗确定', clickLog)) {
        await page.waitForTimeout(1000);
        selectOk = orgsSelected >= 1;
      }
    }
  }
  startAfterSelect = {
    visible: await start.isVisible().catch(() => false),
    enabled: await start.isEnabled().catch(() => false),
    class: await start.getAttribute('class').catch(() => null),
  };
  const mainAfterSelect = ((await page.locator('main').first().innerText().catch(() => '')) || '').slice(0, 600);
  const selectedCountMatch = mainAfterSelect.match(/已选机构（(\d+)/);
  const selectedCount = selectedCountMatch ? Number(selectedCountMatch[1]) : orgsSelected;
  await page.screenshot({ path: path.join(outDir, 'env-gate-config.png'), fullPage: false });
  scout.stages.afterSelect = {
    selectOk,
    orgsSelected,
    selectedCount,
    startAfterSelect,
    mainSnippet: mainAfterSelect,
  };

  // 开始分析（仅 enabled 时点）
  let processOk = false;
  let resultCtaVisible = false;
  let afterStartUrl = '';
  let afterStartMain = '';
  if (startAfterSelect.enabled) {
    if (await softClick(page, start, '开始分析', clickLog)) {
      await page.waitForTimeout(3500);
      afterStartUrl = page.url();
      afterStartMain = ((await page.locator('main').first().innerText().catch(() => '')) || '').slice(0, 900);
      processOk =
        /view=processing|分析过程|生成中|任务状态|任务已创建|分析结果已生成/.test(afterStartUrl + afterStartMain);
      const viewResult = page.getByRole('button', { name: /查看结果/ });
      resultCtaVisible =
        (await viewResult.count()) > 0 &&
        (await viewResult.first().isVisible().catch(() => false)) &&
        (await viewResult.first().isEnabled().catch(() => false));
      await page.screenshot({ path: path.join(outDir, 'env-gate-process.png'), fullPage: false });

      // 尝试进结果（不硬点 disabled）
      let resultOk = false;
      let resultMain = '';
      if (resultCtaVisible && (await softClick(page, viewResult.first(), '查看结果', clickLog))) {
        await page.waitForTimeout(2500);
        resultMain = ((await page.locator('main').first().innerText().catch(() => '')) || '').slice(0, 900);
        resultOk =
          /view=result|热力|矩阵|覆盖|分析结果/.test(page.url() + resultMain) ||
          /产业领域|服务深度|暂无覆盖/.test(resultMain);
        await page.screenshot({ path: path.join(outDir, 'env-gate-result.png'), fullPage: false });
      }
      scout.stages.afterStart = {
        url: afterStartUrl,
        processOk,
        resultCtaVisible,
        resultOk,
        mainSnippet: afterStartMain,
        resultSnippet: resultMain,
      };
    }
  } else {
    clickLog.push({ step: '开始分析', ok: false, reason: 'disabled', note: 'skip hard click' });
    scout.stages.afterStart = { skipped: true, reason: 'start_disabled' };
  }

  // 分析记录：至少 1 条已完成可查看结果？
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const recordsTab = page.getByRole('tab', { name: '分析记录' });
  let historyOk = false;
  let historyDetail = {};
  if (await softClick(page, recordsTab, '分析记录 Tab', clickLog)) {
    await page.waitForTimeout(1200);
    const mainText = (await page.locator('main').first().innerText().catch(() => '')) || '';
    const viewBtns = page.getByRole('button', { name: '查看结果' });
    const viewCount = await viewBtns.count();
    let enabledView = 0;
    let disabledView = 0;
    for (let i = 0; i < Math.min(viewCount, 20); i++) {
      if (await viewBtns.nth(i).isDisabled()) disabledView++;
      else enabledView++;
    }
    const hasDoneRow = /已完成|成功|success/i.test(mainText);
    historyOk = enabledView >= 1 || hasDoneRow;
    historyDetail = {
      viewCount,
      enabledView,
      disabledView,
      hasDoneRow,
      sample: mainText.slice(0, 400),
    };
    await page.screenshot({ path: path.join(outDir, 'env-gate-records.png'), fullPage: false });
  }
  scout.stages.history = historyDetail;

  const g1 = loginOk && deepOk;
  const g2 = startAfterSelect.enabled === true && selectedCount >= 1;
  // 本页非评估预检；无「预检未返回企业明细」即过
  const precheckBlock = /预检未返回企业明细/.test(mainAfterSelect + afterStartMain);
  const g3 = !precheckBlock;
  const g4 = processOk === true || resultCtaVisible === true;
  const g5 = historyOk || scout.stages.afterStart?.resultOk === true;

  const gates = {
    login: { pass: loginOk },
    deep_link: { pass: deepOk, url: deepUrl, title },
    select_orgs: {
      pass: selectOk && selectedCount >= 1,
      selectedCount,
      orgsSelected,
    },
    start_analysis_enabled: {
      pass: g2,
      enabled: startAfterSelect.enabled,
      empty_enabled: startEmpty.enabled,
      empty_hint: emptyHint,
    },
    precheck: {
      pass: g3,
      note: '非评估类预检闸；无「预检未返回企业明细」阻塞',
      fail_text_seen: precheckBlock,
    },
    process_reachable: {
      pass: g4,
      processOk,
      resultCtaVisible,
      url: afterStartUrl || null,
    },
    history_completed: {
      pass: g5,
      ...historyDetail,
      fresh_result_ok: scout.stages.afterStart?.resultOk === true,
    },
  };

  const overall = g1 && g2 && g3 && g4 ? (g5 ? 'pass' : 'partial') : 'fail';
  const tickets = [];
  if (!g2) tickets.push('ENV-SVC-ORG-FIELD-START-DISABLED');
  if (!g4) tickets.push('ENV-SVC-ORG-FIELD-PROCESS-UNREACHABLE');
  if (!g5) tickets.push('ENV-SVC-ORG-FIELD-NO-DONE-TASK');

  const envGate = {
    surveyed_at: new Date().toISOString(),
    entry_id: 'svc-org-field',
    base_url: baseUrl,
    path: route,
    headless: true,
    overall,
    method: 'headless chromium via _env-gate-probe.mjs (no IDE browser)',
    gates,
    evidence: {
      screenshots: [
        'env-gate-deep.png',
        'env-gate-config.png',
        'env-gate-process.png',
        'env-gate-result.png',
        'env-gate-records.png',
        'page.png',
      ].filter((f) => fs.existsSync(path.join(outDir, f))),
      scout_refs: ['scout.json', 'scout-env-gate-probe.json', 'scout-deep.json'],
      start_enabled: startAfterSelect.enabled,
      body_hit: (mainAfterSelect || '').slice(0, 280),
    },
    tickets,
    conclusion:
      overall === 'pass'
        ? '环境闸门通过：登录+深链可达；选机构后「开始分析」enabled；过程/结果链可达；历史或当次有已完成可查看结果。可写过程/结果态金样。'
        : overall === 'partial'
          ? '核心闸门通过（登录/选机构/开始分析 enabled/过程可达），但历史已完成任务不足——结果态金样优先走当次「查看结果」或 B 档 skip+ticket。'
          : '环境闸门失败：过程/结果态禁止进金样；仅可写配置空态/门控断言。',
    implications: {
      gold_config_gate: 'allowed',
      gold_process_result: overall === 'pass' || overall === 'partial' ? 'allowed_if_fresh_path' : 'forbidden',
      layout: 'cases-v1',
    },
  };

  fs.writeFileSync(path.join(outDir, 'scout-env-gate-probe.json'), JSON.stringify(scout, null, 2));
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2));
  console.log(
    JSON.stringify(
      {
        overall: envGate.overall,
        gates: Object.fromEntries(Object.entries(gates).map(([k, v]) => [k, v.pass])),
        tickets,
      },
      null,
      2,
    ),
  );
} catch (e) {
  const fail = {
    surveyed_at: new Date().toISOString(),
    entry_id: 'svc-org-field',
    overall: 'fail',
    error: String(e).slice(0, 500),
    clickLog,
    tickets: ['ENV-SVC-ORG-FIELD-PROBE-CRASH'],
  };
  fs.writeFileSync(path.join(outDir, 'scout-env-gate-probe.json'), JSON.stringify({ ...scout, error: String(e) }, null, 2));
  fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(fail, null, 2));
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
