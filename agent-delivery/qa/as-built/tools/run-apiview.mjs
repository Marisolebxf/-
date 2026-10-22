#!/usr/bin/env node
// run-apiview.mjs — 算法库联调台 Playwright runner。
// 专题系统用 run-scripts.mjs。两边只共用 runner-core.mjs 的读册、断言、截图和结果文件。
//
// usage:
//   node run-apiview.mjs <功能目录> [--run-dir <run目录>] [--only id1,id2] [--headless false] [--check]
//
// 不关内部评审，不读专题基址。口令只来自 ALGO_LOGIN_USER / ALGO_LOGIN_PASSWORD。

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { algoFill, algoPick, algoRun, algoTab, clickPopupOption, ensureApiviewLogin } from './apiview-session.mjs';
import {
  checkAsserts, evalExpects, judgeRun, loadCasesV1, readFailText, shotStep, writeCaseRecord, yamlDump, yamlLoad,
} from './runner-core.mjs';

const args = process.argv.slice(2);
const featDirArg = args[0];
if (!featDirArg || featDirArg.startsWith('--')) {
  console.error('usage: node run-apiview.mjs <功能目录> [--run-dir <dir>] [--only id1,id2] [--headless false] [--check]');
  process.exit(2);
}
function opt(name, dflt) {
  const i = args.indexOf('--' + name);
  return i < 0 ? dflt : args[i + 1];
}
const CHECK_ONLY = args.includes('--check');
const featDir = path.resolve(featDirArg);
const only = opt('only', '') ? opt('only', '').split(',').map((s) => s.trim()) : null;
const headless = opt('headless', 'true') !== 'false';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ORCH = path.resolve(HERE, '../../../..');
const runsRoot = path.join(ORCH, 'agent-delivery/qa/as-built/runs');
const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
const scope = path.basename(featDir);
const runDir = path.resolve(opt('run-dir', path.join(runsRoot, `${today}-algovwz-${scope}`)));

const loaded = loadCasesV1(featDir);
const selected = only ? only.map((id) => loaded.byId.get(id)).filter(Boolean) : loaded.order;
const fixtures = fs.existsSync(path.join(featDir, 'fixtures/testdata.yaml')) ? yamlLoad(path.join(featDir, 'fixtures/testdata.yaml')) : {};
const baseUrl = String(fixtures.base_url || '');
if (!baseUrl.includes('/dma/algovwz/')) {
  console.error('base_url 必须包含 /dma/algovwz/');
  process.exit(2);
}

if (CHECK_ONLY) {
  const bad = checkAsserts(selected);
  console.log(`--check 完成：${selected.length} 条脚本，assert 编译错误 ${bad} 处`);
  process.exit(bad ? 1 : 0);
}
if (!process.env.ALGO_LOGIN_USER || !process.env.ALGO_LOGIN_PASSWORD) {
  console.error('需要环境变量 ALGO_LOGIN_USER 与 ALGO_LOGIN_PASSWORD');
  process.exit(2);
}

function resolveGoto(target) {
  const t = String(target || '');
  if (t.startsWith('http')) return t;
  const base = baseUrl.endsWith('/') ? baseUrl : baseUrl + '/';
  if (t.startsWith('#')) return base + t;
  if (t.startsWith('/')) return base + '#' + t;
  return base + '#' + t;
}

async function clickTarget(page, target) {
  const t = String(target);
  if (/^[.#\[]/.test(t)) {
    await page.locator(t).first().click({ timeout: 8000 });
    return;
  }
  const role = t.match(/^role=(\w+)\s+(.+)$/);
  if (role) {
    await page.getByRole(role[1], { name: role[2] }).click({ timeout: 8000 });
    return;
  }
  const name = t.replace(/「|」/g, '');
  if (await page.locator('.arco-trigger-popup:visible').count()) {
    await clickPopupOption(page, name);
    return;
  }
  await page.getByText(name, { exact: true }).click({ timeout: 5000 });
}

async function runScript(page, script) {
  const caseDir = path.join(runDir, 'scripts', script.id);
  fs.mkdirSync(path.join(caseDir, 'screenshots'), { recursive: true });
  const stepLog = [], warnings = [];
  let verdicts = [];
  let shotIdx = 0;
  let aborted = null;
  const logStep = (action, label, ok, detail) => {
    stepLog.push({ n: stepLog.length + 1, action, label: label || '', ok, detail: detail || '' });
    console.log(`    ${ok ? '✓' : '✗'} ${action} ${label || ''}${detail ? ' — ' + String(detail).slice(0, 120) : ''}`);
  };
  try {
    for (const step of script.steps || []) {
      const action = step.action;
      const label = step.target || step.note || '';
      shotIdx += 1;
      try {
        if (action === 'goto') {
          const url = resolveGoto(step.target);
          if (page.url() === url) await page.reload({ waitUntil: 'domcontentloaded' });
          else await page.goto(url, { waitUntil: 'domcontentloaded' });
          await ensureApiviewLogin(page);
          logStep('goto', step.target, true);
        } else if (action === 'click') {
          await clickTarget(page, step.target);
          logStep('click', step.target, true);
        } else if (action === 'fill') {
          const t = String(step.target);
          const loc = /^[.#\[]/.test(t) ? page.locator(t).first() : page.getByLabel(t).first();
          await loc.fill(step.value ?? '', { timeout: 5000 });
          logStep('fill', `${step.target}=${step.value}`, true);
        } else if (action === 'press') {
          await page.keyboard.press(step.key || 'Enter');
          logStep('press', step.key || 'Enter', true);
        } else if (action === 'wait') {
          const ms = typeof step.timeout_ms === 'number' ? step.timeout_ms : 800;
          await page.waitForTimeout(ms);
          logStep('wait', `${ms}ms`, true);
        } else if (action === 'assert_visible') {
          const t = String(step.target);
          const loc = /^[.#\[]/.test(t) ? page.locator(t).first() : page.getByText(t.replace(/「|」/g, '')).first();
          await loc.waitFor({ state: 'visible', timeout: 6000 });
          logStep('assert_visible', step.target, true);
        } else if (action === 'assert_url') {
          const ok = page.url().includes(step.expect_contains || '');
          logStep('assert_url', step.expect_contains, ok, ok ? '' : '实际 ' + page.url());
        } else if (action === 'assert_absent') {
          const t = String(step.target);
          const cnt = /^[.#\[]/.test(t) ? await page.locator(t).count() : await page.getByText(t).count();
          logStep('assert_absent', step.target, cnt === 0, cnt ? `仍存在 ×${cnt}` : '');
        } else if (action === 'screenshot') {
          logStep('screenshot', step.note || '', true);
        } else if (action === 'algo_tab') {
          await algoTab(page, step.target);
          logStep('algo_tab', step.target, true);
        } else if (action === 'algo_pick') {
          await algoPick(page, step.target);
          logStep('algo_pick', step.target, true);
        } else if (action === 'algo_fill') {
          await algoFill(page, step);
          logStep('algo_fill', Object.keys(step.set || {}).concat(step.omit || []).join(','), true);
        } else if (action === 'algo_run') {
          await algoRun(page, caseDir);
          logStep('algo_run', '', true);
        } else {
          logStep(action, label, false, '未识别 action');
          warnings.push('未识别 action: ' + action);
        }
      } catch (e) {
        logStep(action, label, false, String(e.message).split('\n')[0]);
      }
      await shotStep(page, caseDir, shotIdx, action, label);
    }
    const judged = await evalExpects(page, script, baseUrl);
    verdicts = judged.verdicts;
    warnings.push(...judged.warnings);
    if ((script.steps || []).some((s) => s.action === 'algo_run')) {
      const file = path.join(caseDir, 'exchange.txt');
      const text = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '';
      const body = (text.split('response:\n')[1] || '').trim();
      if (!body) verdicts.push({ note: 'exchange.txt', status: 'fail', detail: '调用记录缺少真实返回' });
    }
  } catch (e) { aborted = e; }
  const judged = judgeRun({ aborted, skip: false, verdicts, warnings });
  return { ...judged, steps: stepLog, warnings, verdicts };
}

const vp = fixtures.viewport || {};
const browser = await chromium.launch({ headless });
const context = await browser.newContext({
  viewport: { width: vp.width || 1920, height: vp.height || 1080 },
  deviceScaleFactor: vp.device_scale_factor || 1,
});
const page = await context.newPage();
fs.mkdirSync(path.join(runDir, 'scripts'), { recursive: true });
const gitHead = (() => { try { return execSync('git rev-parse HEAD', { cwd: ORCH }).toString().trim(); } catch { return null; } })();
const t0 = new Date();
console.log(`▶ algovwz run ${t0.toISOString()} | headless=${headless} | 用例 ${selected.length} 条\nrun 目录: ${runDir}`);
console.log('联调台会话（不关内部评审）');

const results = [];
for (const script of selected) {
  console.log(`  ▶ ${script.id} ${script.title || ''}`);
  const r = await runScript(page, script);
  results.push({ script, ...r });
  writeCaseRecord(runDir, script, r, await readFailText(page, r.verdict));
}
await browser.close();
const t1 = new Date();
fs.writeFileSync(path.join(runDir, 'meta.yaml'), yamlDump({
  run_id: path.basename(runDir),
  feature: `${path.basename(path.dirname(featDir))}/${scope}`,
  environment: { base_url: baseUrl, env_label: 'algovwz' },
  account: { username_env: 'ALGO_LOGIN_USER' },
  git: { repo: 'gkx-orchestration', head: gitHead },
  time: { started_at: t0.toISOString(), ended_at: t1.toISOString() },
  tooling: 'run-apiview（chromium headless）',
}) + '\n');
const counts = { pass: 0, fail: 0, blocked: 0 };
for (const r of results) counts[r.verdict] = (counts[r.verdict] || 0) + 1;
fs.writeFileSync(path.join(runDir, 'SUMMARY.md'), [
  `# ${path.basename(runDir)}`,
  '',
  `- pass ${counts.pass || 0} / fail ${counts.fail || 0} / blocked ${counts.blocked || 0}`,
  '',
].join('\n'));
console.log(`■ 结束 pass=${counts.pass || 0} fail=${counts.fail || 0} blocked=${counts.blocked || 0}`);
process.exit((counts.fail || counts.blocked) ? 1 : 0);
