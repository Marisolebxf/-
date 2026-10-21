#!/usr/bin/env node
/**
 * svc-maintenance 模块闸门二次探针（无头）。
 * 产物：env-gate.json + env-gate-*.png + scout-env-gate-probe.json
 * method-patch §3：登录深链；本页无异步「开始分析」→ g2/g3/g4/g5 N/A=pass；
 * 附加：占位壳文案 / 诚实空 / 刷新稳定 / 路由隔离。
 * 禁止当 runner；禁止有头 MCP；disabled 不硬点。
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
const route = '/service/maintenance';
const outDir = __dirname;
const PLACEHOLDER_COPY = '入口已对齐 demo 路由。业务区块由后续 US-SVC-* 叶交付';
const HONEST_EMPTY_RE = /本入口暂无业务数据|USE_MOCK=false|不填 Demo fixture/;

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
  const close = page.getByRole('button', { name: '关闭对比篮' });
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
  const closeAria = page.locator('[aria-label="关闭对比篮"]');
  if ((await closeAria.count()) && (await closeAria.first().isVisible().catch(() => false))) {
    await closeAria.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const gates = [];
const tickets = [];
const shot = async (name) => {
  const p = path.join(outDir, `env-gate-${name}.png`);
  await page.screenshot({ path: p, fullPage: false });
  return `env-gate-${name}.png`;
};

const probe = { surveyed_at: new Date().toISOString(), entry_id: 'svc-maintenance', steps: [] };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  const loginOk = !page.url().includes('/login');
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  const url = page.url();
  const title = await page.title();
  const deepOk = /\/service\/maintenance/.test(url) && !/\/login/.test(url);
  const titleOk = /维护管理/.test(title);
  const h1 = page.locator('h1');
  const h1Ok = (await h1.count()) > 0 && /维护管理/.test((await h1.first().innerText().catch(() => '')) || '');
  const g1Pass = loginOk && deepOk && titleOk && h1Ok;
  gates.push({
    id: 'g1_login_deep',
    pass: g1Pass,
    detail: { loginOk, deepOk, titleOk, h1Ok, title, url },
    shot: await shot('deep'),
  });
  if (!g1Pass) tickets.push('ENV-SVC-MAINT-LOGIN-DEEP-001');
  probe.steps.push({ step: 'g1', loginOk, deepOk, titleOk, h1Ok, url, title });

  // g2：无异步「开始分析」（主区；对比篮「发起分析」属系统浮层，不计）
  const startInMain = await page.evaluate(() => {
    const main = document.querySelector('main') || document.body;
    const texts = [...main.querySelectorAll('button, [role=button]')].map((el) =>
      (el.innerText || el.textContent || '').replace(/\s+/g, ''),
    );
    return texts.some((t) => /开始分析|开始评估/.test(t));
  });
  gates.push({
    id: 'g2_start_enabled_legal_combo',
    pass: true,
    n_a: true,
    detail: {
      startPresent: startInMain,
      note: '服务机构维护管理为占位壳，无异步「开始分析」；本闸 N/A=pass（method-patch §3.2）',
    },
  });

  gates.push({
    id: 'g3_precheck_eval',
    pass: true,
    n_a: true,
    detail: { note: '非企业评估页，无「预检未返回企业明细」门控；本闸 N/A=pass（§3.3）' },
  });

  gates.push({
    id: 'g4_bio_blacklist',
    pass: true,
    n_a: true,
    detail: { note: '本页无产业组合选择，无 INPUT_OBJECT_INVALID 风险；本闸 N/A=pass（§3.4）' },
  });

  gates.push({
    id: 'g5_completed_task_view_result',
    pass: true,
    n_a: true,
    detail: {
      mode: 'no_async_task_history',
      viewCount: 0,
      startPresent: startInMain,
      note: '本页无诊断记录/「查看结果」历史任务依赖；结果主路径=占位壳可见。本闸 N/A=pass（§3.5）',
    },
    shot: await shot('shell'),
  });

  // 占位壳结构（本页附加闸）
  const bodyText = await page.locator('main').innerText().catch(() => page.locator('body').innerText());
  const copyOk = bodyText.includes(PLACEHOLDER_COPY);
  const panel = page.locator('[aria-label="业务占位"], .svc-shell-panel');
  const panelOk = (await panel.count()) > 0;
  const honestOk = HONEST_EMPTY_RE.test(bodyText);
  const fakeWorkspace =
    /维护工作区|字段指标|模型规则|数据批次|产业链实体生命周期|门户内容（产业全景）/.test(bodyText) &&
    !bodyText.includes(PLACEHOLDER_COPY);
  const fakeList = await page.evaluate(() => {
    const main = document.querySelector('main') || document.body;
    // 主区表格/列表（排除对比篮）
    const tables = [...main.querySelectorAll('table, .arco-table, .arco-list')].filter(
      (el) => !el.closest('.system-compare-panel'),
    );
    return tables.length > 0;
  });
  const shellPass = copyOk && panelOk && honestOk && !fakeWorkspace && !fakeList;
  gates.push({
    id: 'g_placeholder_shell',
    pass: shellPass,
    detail: {
      copyOk,
      panelOk,
      honestOk,
      fakeWorkspace: !!fakeWorkspace,
      fakeList,
      placeholderCopy: PLACEHOLDER_COPY,
      note: '页头+占位说明+业务占位诚实空；无 ENT-OPS 15 分类实壳（勿与 chain-maintenance 混淆）',
    },
    shot: await shot('placeholder'),
  });
  if (!shellPass) tickets.push('ENV-SVC-MAINT-PLACEHOLDER-001');
  probe.steps.push({ step: 'g_placeholder', copyOk, panelOk, honestOk, fakeWorkspace, fakeList });

  // 刷新稳定
  await page.reload({ waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  await closeBasket(page);
  const afterUrl = page.url();
  const afterTitle = await page.title();
  const afterText = await page.locator('main').innerText().catch(() => page.locator('body').innerText());
  const refreshPass =
    /\/service\/maintenance/.test(afterUrl) &&
    /维护管理/.test(afterTitle) &&
    afterText.includes(PLACEHOLDER_COPY);
  gates.push({
    id: 'g_refresh_stable',
    pass: refreshPass,
    detail: {
      url: afterUrl,
      title: afterTitle,
      copyOk: afterText.includes(PLACEHOLDER_COPY),
      note: '刷新后路由/页标题/占位文案保持',
    },
    shot: await shot('after-refresh'),
  });
  if (!refreshPass) tickets.push('ENV-SVC-MAINT-REFRESH-001');
  probe.steps.push({ step: 'g_refresh', url: afterUrl, title: afterTitle, refreshPass });

  // 路由隔离：不落到 industry-center/maintenance
  const isolationOk = !/\/industry-center\/maintenance/.test(afterUrl) && /\/service\/maintenance/.test(afterUrl);
  gates.push({
    id: 'g_route_isolation',
    pass: isolationOk,
    detail: {
      url: afterUrl,
      forbid: '/industry-center/maintenance',
      note: '全程保持 /service/maintenance，不落到 CHAINMAINT 实壳',
    },
  });
  if (!isolationOk) tickets.push('ENV-SVC-MAINT-ISOLATION-001');
} catch (e) {
  tickets.push('ENV-SVC-MAINT-PROBE-CRASH-001');
  gates.push({ id: 'g_probe_crash', pass: false, detail: { error: String(e && e.message ? e.message : e) } });
  probe.error = String(e && e.stack ? e.stack : e);
} finally {
  await browser.close();
}

const overall = gates.every((g) => g.pass) && tickets.length === 0 ? 'pass' : 'fail';
const envGate = {
  entry_id: 'svc-maintenance',
  probed_at: new Date().toISOString(),
  base_url: baseUrl,
  route,
  overall,
  method: 'headless chromium via survey-page.mjs + _env-gate-probe.mjs (no IDE browser)',
  method_patch_ref: 'agent-delivery/qa/as-built/retro/20261014-batch32-method-patch.md §3',
  gates,
  tickets,
  implications: {
    gold_config_gate: 'allowed — 入口/页头/占位文案/诚实空/刷新可进金样',
    gold_process_trigger: 'n_a — 本页无异步「开始分析」过程态',
    gold_result_state: 'allowed_lite — 占位壳可见即结果代理；无任务「查看结果」硬门槛',
    no_async_analysis: true,
    ticket_env_no_done: tickets.length ? tickets : null,
    method_patch_ref: 'agent-delivery/qa/as-built/retro/20261014-batch32-method-patch.md §3',
    gold_suggest: {
      keep: ['01351', '01352', '01353', '01354'],
      promote_to_gold: ['01355'],
      downgrade_to_B: [],
      optional_promote_if_runner_green: ['01356', '01361'],
      note:
        '用例册金样=01351~01354（入口+构成+文案+诚实态）。闸门 overall 若 pass，建议 A 档 4～5 条：保留 01351~01354，可选升 01355 刷新稳定。01356 语义备选、01361 路由刷新可作 B→A 候补。01357 对比篮系统级 / 01358 隔离 / 01359 评审零泄漏 / 01360 网络模拟 → 不进金样。',
    },
    forbid_gold_reasons: {
      '01357': '对比篮系统浮层；专项归 COMPARE',
      '01358': '兄弟模块隔离；操作面广，非烟测核心',
      '01359': '评审模式开关；依赖人设面板',
      '01360': '网络中断模拟；环境条件常不可用',
    },
  },
};

fs.writeFileSync(path.join(outDir, 'env-gate.json'), JSON.stringify(envGate, null, 2), 'utf8');
fs.writeFileSync(path.join(outDir, 'scout-env-gate-probe.json'), JSON.stringify(probe, null, 2), 'utf8');
console.log(JSON.stringify({ overall, tickets, gates: gates.map((g) => ({ id: g.id, pass: g.pass, n_a: g.n_a })) }, null, 2));
