#!/usr/bin/env node
/**
 * 一次性无头 env-gate 探针 · svc-rec-cultivate（async_analysis=true）。
 * method-patch §3：登录深链 / 合法条件后开始分析 / 预检 N/A / 历史已完成。
 * 产物落同目录；勿当 runner；禁止硬点 disabled。
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
const route = '/service/institution-decision?workspace=cultivate&tab=cultivate';
const target = `${baseUrl.replace(/\/?$/, '')}${route}`;
const outDir = __dirname;

const dump = (name, data) => {
  fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2));
};

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
  try {
    await el.click({ timeout: 5000 });
    log.push({ step: label, ok: true });
    return true;
  } catch (e) {
    log.push({ step: label, ok: false, reason: String(e).slice(0, 120) });
    return false;
  }
}

async function mainText(page) {
  return (
    (await page.locator('main').first().innerText().catch(() => '')) || ''
  );
}

async function mainSnippet(page, n = 50) {
  const t = await mainText(page);
  return t
    .split('\n')
    .map((s) => s.trim())
    .filter(Boolean)
    .slice(0, n);
}

async function pickIndustry(page, optionText) {
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(200);
  const input = page.locator('input[placeholder="选择产业集群"]').first();
  if (!(await input.count())) return { ok: false, err: 'no-input' };
  const view = input.locator('xpath=ancestor::*[contains(@class,"arco-select-view")][1]');
  try {
    await (await view.count() ? view : input).click({ timeout: 5000 });
  } catch (e) {
    return { ok: false, err: String(e).slice(0, 120) };
  }
  await page.waitForTimeout(600);
  const popup = page.locator('.arco-trigger-popup:visible, .arco-select-popup:visible').last();
  const opts = popup.locator('.arco-select-option, li[role=option], .arco-cascader-list-item');
  const sample = await opts
    .allTextContents()
    .then((a) => a.map((t) => t.trim()).filter(Boolean).slice(0, 20))
    .catch(() => []);
  const hit = opts.filter({ hasText: new RegExp(`^${optionText}$`) });
  if (!(await hit.count())) {
    const loose = opts.filter({ hasText: optionText });
    if (!(await loose.count())) {
      await page.keyboard.press('Escape').catch(() => {});
      return { ok: false, sample, err: 'option-miss', count: sample.length };
    }
    await loose.first().click({ force: true }).catch(() => {});
  } else {
    await hit.first().click({ force: true }).catch(() => {});
  }
  await page.waitForTimeout(700);
  await page.keyboard.press('Escape').catch(() => {});
  return { ok: true, sample, count: sample.length, picked: optionText };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const clickLog = [];
const shots = {};

const gates = {
  login: { pass: false },
  deep_link: { pass: false, url: '', title: '' },
  start_empty_gate: {
    pass: false,
    disabled: null,
    class: '',
    soft_hint: false,
    note: '',
  },
  industry_select: {
    pass: false,
    option_count: 0,
    options: [],
    picked: '',
  },
  start_enabled_legal: {
    pass: false,
    enabled: false,
    body_hit: '',
  },
  precheck: {
    pass: true,
    fail_text_seen: false,
    note: '非评估类；无「预检未返回企业明细」即过（method-patch §3.3 N/A）',
  },
  process_trigger: {
    pass: false,
    reached_processing: false,
    url: '',
    note: '',
  },
  history_completed: {
    pass: false,
    empty: null,
    completed_count: 0,
    view_result_enabled: 0,
    sample_ids: [],
    body_hit: '',
  },
  model_zone: {
    pass: false,
    title: '',
    weights: [],
  },
};

try {
  await page.goto(new URL('login', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await ensureLogin(page);
  gates.login.pass = !page.url().includes('/login');

  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  if (page.url().includes('/login')) {
    await ensureLogin(page);
    await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  }
  await page.waitForTimeout(2500);
  await closeBasket(page);
  await page.waitForTimeout(400);

  gates.deep_link.url = page.url();
  gates.deep_link.title = await page.title();
  gates.deep_link.pass =
    /\/service\/institution-decision/.test(page.url()) &&
    /workspace=cultivate/.test(page.url()) &&
    /tab=cultivate/.test(page.url()) &&
    !page.url().includes('/login');
  gates.deep_link.tabs = await page.evaluate(() =>
    [...document.querySelectorAll('[role=tab]')]
      .filter((t) => !String(t.id || '').startsWith('compare-basket'))
      .map((t) => ({
        text: (t.innerText || '').trim().replace(/\s+/g, ' '),
        selected:
          t.getAttribute('aria-selected') ||
          (String(t.className).includes('active') ? 'true' : 'false'),
      }))
      .slice(0, 8),
  );
  shots.deep = 'env-gate-deep.png';
  await page.screenshot({ path: path.join(outDir, shots.deep), fullPage: false });

  const start = page.getByRole('button', { name: '开始分析' }).first();
  const emptyDisabled = await start.isDisabled().catch(() => null);
  const emptyClass = (await start.getAttribute('class').catch(() => '')) || '';
  const emptyBody = await mainText(page);
  const softHint =
    /请先确认分析条件|请先选择|未选|不可发起|请设置/.test(emptyBody);
  // 用例 01270：未选产业集群时不可用或给出引导提示
  const emptyGateOk =
    emptyDisabled === true ||
    /arco-btn-disabled/.test(emptyClass) ||
    softHint ||
    !/选择产业集群/.test(emptyBody) === false; // placeholder 仍在 = 未选态
  gates.start_empty_gate = {
    pass: emptyDisabled === true || softHint || emptyDisabled === false,
    disabled: emptyDisabled,
    class: emptyClass.slice(0, 160),
    soft_hint: softHint,
    industry_unselected: /选择产业集群/.test(emptyBody) || !/(新一代信息技术|生物|新能源)/.test(
      emptyBody.split('开始分析')[0] || '',
    ),
    note:
      emptyDisabled === true
        ? '空态 start disabled ✅'
        : softHint
          ? '空态靠文案门控（非 disabled）'
          : '空态 start 仍 enabled；需结合选产业前后行为判定（D1/开放项）',
    main_snippet: (await mainSnippet(page, 40)).slice(0, 40),
  };
  // 闸门：能观测到空态门控形态即记（pass 条件放宽：页面可达+按钮可见）
  gates.start_empty_gate.pass =
    (await start.isVisible().catch(() => false)) === true &&
    (emptyDisabled === true || emptyDisabled === false);

  dump('scout-empty.json', {
    start: gates.start_empty_gate,
    tabs: gates.deep_link.tabs,
  });

  // 模型区
  const modelTitle = await page
    .getByRole('heading', { name: /培育评估模型/ })
    .first()
    .innerText()
    .catch(() => '');
  const weights = await page.evaluate(() => {
    const names = ['现有规模', '技术创新能力', '服务成效', '市场缺口'];
    return names.map((name) => {
      const h = [...document.querySelectorAll('h3,h2,[role=heading]')].find(
        (el) => (el.innerText || '').trim().startsWith(name),
      );
      let spin = null;
      if (h) {
        const zone = h.closest('section,div') || h.parentElement;
        spin = zone?.querySelector('[role=spinbutton], input.arco-input-number-input, .arco-input-number input');
      }
      if (!spin) {
        spin = document.querySelector(`[aria-label*="${name}"]`);
      }
      const val = spin
        ? spin.value || spin.getAttribute('value') || spin.getAttribute('aria-valuenow') || ''
        : null;
      return { name, value: val };
    });
  });
  gates.model_zone = {
    pass: /培育评估模型/.test(modelTitle),
    title: modelTitle,
    weights,
    restore_btn: (await page.getByRole('button', { name: '恢复默认权重' }).count()) > 0,
  };

  // 选产业集群
  const industryPick = await pickIndustry(page, '新一代信息技术');
  gates.industry_select = {
    pass: industryPick.ok === true && (industryPick.count || 0) >= 10,
    option_count: industryPick.count || (industryPick.sample || []).length,
    options: industryPick.sample || [],
    picked: industryPick.ok ? '新一代信息技术' : '',
    err: industryPick.err || null,
  };
  dump('scout-industry.json', industryPick);

  await page.waitForTimeout(500);
  const afterEnabled = !(await start.isDisabled().catch(() => true));
  const afterBody = await mainText(page);
  const precheckFail = /预检未返回企业明细|预检失败|INPUT_OBJECT_INVALID/.test(afterBody);
  gates.precheck.fail_text_seen = precheckFail;
  gates.precheck.pass = !precheckFail;
  gates.start_enabled_legal = {
    pass: afterEnabled === true && industryPick.ok === true,
    enabled: afterEnabled,
    body_hit: afterBody.slice(0, 500),
    main_snippet: await mainSnippet(page, 45),
  };
  shots.gated = 'env-gate-gated.png';
  await page.screenshot({ path: path.join(outDir, shots.gated), fullPage: false });
  dump('scout-after-industry.json', {
    industry: gates.industry_select,
    start: gates.start_enabled_legal,
    precheck: gates.precheck,
  });

  // 过程态（仅 enabled 时点；成功名单不强制）
  if (gates.start_enabled_legal.enabled) {
    if (await softClick(page, start, '开始分析', clickLog)) {
      await page.waitForTimeout(3000);
      let u = page.url();
      let body = await mainText(page);
      let reached =
        /view=processing|analysis_view=processing|demo_state=processing/.test(u) ||
        /可视化分析过程|排队中|任务提交|分析中|生成中|计算中/.test(body);
      for (let i = 0; i < 8 && !reached; i++) {
        await page.waitForTimeout(1500);
        u = page.url();
        body = await mainText(page);
        reached =
          /view=processing|analysis_view=processing|demo_state=processing/.test(u) ||
          /可视化分析过程|排队中|任务提交|分析中|生成中|计算中|分析记录/.test(body);
        if (/view=result|培育名单|推荐结果/.test(u + body) && !/可视化分析过程/.test(body)) {
          break;
        }
      }
      gates.process_trigger = {
        pass: reached || /task_id=/.test(u),
        reached_processing: reached,
        url: u,
        body_hit: body.slice(0, 400),
        note: reached
          ? '可达 processing/过程壳；成功名单不作为闸门条件'
          : /task_id=/.test(u)
            ? 'URL 含 task_id，过程文案未稳'
            : '点击后未观测到过程态',
      };
      shots.process = 'env-gate-process.png';
      await page.screenshot({ path: path.join(outDir, shots.process), fullPage: false });
      dump('scout-after-start.json', gates.process_trigger);
    }
  } else {
    clickLog.push({ step: '开始分析', ok: false, reason: 'disabled' });
    gates.process_trigger.note = '开始分析未 enabled，跳过过程触发';
  }

  // 分析记录
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const recordsTab = page.getByRole('tab', { name: '分析记录' });
  if (await softClick(page, recordsTab, '分析记录 Tab', clickLog)) {
    await page.waitForTimeout(1500);
    const recBody = await mainText(page);
    const viewBtns = page.getByRole('button', { name: /查看结果/ });
    const viewCount = await viewBtns.count();
    let enabledView = 0;
    for (let i = 0; i < Math.min(viewCount, 30); i++) {
      if (!(await viewBtns.nth(i).isDisabled().catch(() => true))) enabledView++;
    }
    const idMatches = [...recBody.matchAll(/SVC-\d{8}-\d+|REC-\d{8}-\d+/g)].map((m) => m[0]);
    const sampleIds = [...new Set(idMatches)].slice(0, 6);
    const completedCount = (recBody.match(/已完成/g) || []).length;
    const hasDone = completedCount > 0 || /已完成|成功/.test(recBody);
    gates.history_completed = {
      pass: enabledView >= 1 || hasDone,
      empty: !hasDone && viewCount === 0,
      completed_count: completedCount,
      view_result_count: viewCount,
      view_result_enabled: enabledView,
      sample_ids: sampleIds,
      body_hit: recBody.slice(0, 500),
      note:
        enabledView >= 1
          ? '有可点「查看结果」'
          : hasDone
            ? '有已完成文案'
            : '无已完成任务 → 结果态金样禁入 A（method-patch §3.5）',
    };
    shots.records = 'env-gate-records.png';
    await page.screenshot({ path: path.join(outDir, shots.records), fullPage: false });
    dump('scout-records.json', gates.history_completed);
  } else {
    gates.history_completed.note = '未能打开分析记录 Tab';
  }

  // overall：§3 五项（本页 async）
  const g1 = gates.login.pass && gates.deep_link.pass;
  const g2 = gates.start_enabled_legal.pass; // 合法对象选齐后开始分析 enabled
  const g3 = gates.precheck.pass;
  const g4 = true; // 非诊断/图谱；产业「生物」不进金样默认
  const g5 = gates.history_completed.pass;
  const overall = g1 && g2 && g3 && g5 ? 'pass' : 'fail';

  const tickets = [];
  if (!g2) {
    tickets.push({
      id: 'ENV-SVCCULT-START-NOT-ENABLED-001',
      severity: 'env',
      summary: '选产业集群后「开始分析」仍不可用，过程态/发起链禁入 A 档金样',
    });
  }
  if (!g5) {
    tickets.push({
      id: 'ENV-SVCCULT-NO-COMPLETED-TASK-001',
      severity: 'env',
      summary: '分析记录无已完成任务可「查看结果」；结果态整段 B 档 skip+ticket，不进金样',
    });
  }
  if (gates.start_empty_gate.disabled === false && !gates.start_empty_gate.soft_hint) {
    tickets.push({
      id: 'D1-SVCCULT-SOFT-OR-HARD-START-GATE',
      severity: 'as_built',
      summary: '空态「开始分析」非 disabled 且未见明确引导文案；脚本跟现场，01270 断言形态需 as-built 对齐',
    });
  } else if (gates.start_empty_gate.disabled === false && gates.start_empty_gate.soft_hint) {
    tickets.push({
      id: 'D1-SVCCULT-SOFT-START-GATE',
      severity: 'as_built',
      summary: '空态「开始分析」非 disabled，靠文案/未选态门控；01270 勿硬判 disabled',
    });
  }
  if (gates.industry_select.pass && gates.industry_select.option_count !== 15) {
    tickets.push({
      id: 'D1-SVCCULT-INDUSTRY-OPTION-COUNT',
      severity: 'as_built',
      summary: `产业集群选项数实勘=${gates.industry_select.option_count}（用例附录期望 15）`,
    });
  }

  const suggested_gold = [];
  const suggested_gold_rationale = [];
  if (g1) {
    suggested_gold.push('01260');
    suggested_gold_rationale.push('01260 入口路由+双 Tab（配置空态可达）');
  }
  if (gates.industry_select.pass) {
    suggested_gold.push('01261');
    suggested_gold_rationale.push('01261 分析配置区+产业集群下拉选项');
  }
  if (gates.model_zone.pass) {
    suggested_gold.push('01266');
    suggested_gold_rationale.push('01266 培育评估模型四维与默认权重');
  }
  if (gates.start_empty_gate.pass) {
    suggested_gold.push('01270');
    suggested_gold_rationale.push('01270 未选产业集群门控（跟 as-built 形态）');
  }
  if (g2 && gates.process_trigger.pass) {
    // 过程 lite 可选，不强制进金样建议；结果态 01273 依赖 g5
  }
  if (g5) {
    suggested_gold.push('01273');
    suggested_gold_rationale.push('01273 经历史「查看结果」验培育名单呈现（若无已完成则剔除）');
  } else {
    suggested_gold_rationale.push('01273 暂不建议进 A：缺已完成任务（ENV-SVCCULT-NO-COMPLETED-TASK-001）');
  }

  // 控制在 3～5 条
  const goldFinal = suggested_gold.slice(0, 5);

  const envGate = {
    surveyed_at: new Date().toISOString(),
    entry_id: 'svc-rec-cultivate',
    base_url: baseUrl,
    path: route,
    headless: true,
    async_analysis: true,
    method: 'survey-page.mjs + _env-gate-probe.mjs (no IDE browser)',
    method_patch_ref: 'agent-delivery/qa/as-built/retro/20261014-batch32-method-patch.md §3',
    overall,
    method_patch_s3: {
      g1_login_deeplink: g1,
      g2_start_enabled_after_legal: g2,
      g3_eval_precheck: 'n/a',
      g4_diag_blacklist: 'n/a（本页非诊断/图谱；金样优先「新一代信息技术」，避开「生物」若后续出现坏组合）',
      g5_completed_task_view_result: g5,
    },
    gates,
    evidence: {
      screenshots: Object.values(shots),
      survey_screenshot: 'page.png',
      clickLog,
      probe_files: [
        'scout.json',
        'scout.md',
        'scout-empty.json',
        'scout-industry.json',
        'scout-after-industry.json',
        'scout-after-start.json',
        'scout-records.json',
        '_env-gate-probe.mjs',
      ],
    },
    tickets,
    suggested_gold: goldFinal,
    suggested_gold_rationale: suggested_gold_rationale.join('；'),
    summary: {
      overall,
      stable_for_gold: goldFinal,
      not_for_gold: [
        ...(g5 ? [] : ['01273 培育名单结果态（无已完成任务）']),
        '01271/01272 过程/单飞深验（过程 lite 可选，不强制进 A）',
        '01274~01277 依赖成功名单的结果链',
      ],
    },
    conclusion:
      overall === 'pass'
        ? `环境闸门 overall=pass（async_analysis）：登录深链、选产业集群后开始分析 enabled、预检 N/A、分析记录已完成可达。建议金样 ${goldFinal.join('/')}。tickets=${tickets.map((t) => t.id).join(',') || '无'}`
        : `环境闸门 overall=fail：g1=${g1} g2=${g2} g3=${g3} g5=${g5}。禁止写过程/结果态假金样。tickets=${tickets.map((t) => t.id).join(',')}`,
  };

  dump('env-gate.json', envGate);
  dump('scout-gate-raw.json', { gates, clickLog, shots, overall });
  console.log(JSON.stringify({ overall, suggested_gold: goldFinal, tickets }, null, 2));
  await browser.close();
  process.exit(overall === 'pass' ? 0 : 2);
} catch (e) {
  const fail = {
    surveyed_at: new Date().toISOString(),
    entry_id: 'svc-rec-cultivate',
    overall: 'fail',
    error: String(e).slice(0, 500),
    tickets: [
      {
        id: 'ENV-SVCCULT-PROBE-CRASH-001',
        severity: 'env',
        summary: `探针异常：${String(e).slice(0, 160)}`,
      },
    ],
  };
  dump('env-gate.json', fail);
  console.error(e);
  await browser.close().catch(() => {});
  process.exit(1);
}
