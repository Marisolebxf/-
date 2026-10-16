#!/usr/bin/env node
/**
 * 一次性无头二次探针：svc-org-capability。产物落同目录；勿当 runner。
 * 闸门焦点：从对比篮带入机构 / 开始评估 enabled / 预检文案 / 分析记录已完成任务。
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
const target = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;
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

const dump = (name, data) => {
  fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2));
};

const mainLoc = (page) =>
  page.locator('main.svc-org-analysis-main, [data-testid="svc-org-analysis-shell"] main, main.content-shell-layout').first();

const mainSnippet = async (page, n = 80) =>
  mainLoc(page)
    .innerText()
    .then((t) =>
      t
        .split('\n')
        .map((s) => s.trim())
        .filter(Boolean)
        .slice(0, n),
    )
    .catch(() => []);

const mainText = async (page) => mainLoc(page).innerText().catch(() => '');

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const gate = {
  surveyed_at: new Date().toISOString(),
  entry_id: 'svc-org-capability',
  path: '/service/institution-judgment?workspace=capability&tab=capability',
  steps: {},
};

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  gate.steps.login = { pass: true };
} catch (e) {
  gate.steps.login = { pass: false, error: String(e).slice(0, 200) };
  dump('scout-gate-fail.json', gate);
  await browser.close();
  process.exit(1);
}

await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(2000);
await closeBasket(page);
await page.waitForTimeout(500);

gate.steps.deep_link = {
  pass: /workspace=capability/.test(page.url()) && !page.url().includes('/login'),
  url: page.url(),
  title: await page.title(),
};

const startBtn = page.getByRole('button', { name: '开始评估' }).first();
const emptyState = {
  start_disabled: await startBtn.isDisabled().catch(() => null),
  start_class: await startBtn.getAttribute('class').catch(() => ''),
  btn_import: await page.getByRole('button', { name: '从对比篮带入' }).count(),
  btn_search: await page.getByRole('button', { name: /去检索加入对比篮/ }).count(),
  btn_manage: await page.getByRole('button', { name: /管理对比篮/ }).count(),
  tabs: await page.evaluate(() =>
    [...document.querySelectorAll('[role=tab]')]
      .filter((t) => !String(t.id || '').startsWith('compare-basket'))
      .map((t) => ({
        text: (t.innerText || '').trim().replace(/\s+/g, ' '),
        selected: t.getAttribute('aria-selected') || (t.className.includes('active') ? 'true' : 'false'),
      })),
  ),
  weights: await page.evaluate(() => {
    const labels = ['专利数量', '研发投入', '核心专家', '成功案例', '标准制定'];
    return labels.map((name) => {
      const spin = document.querySelector(`[aria-label="${name}权重"]`);
      return { name, value: spin ? spin.value || spin.getAttribute('value') || spin.textContent : null };
    });
  }),
  main_snippet: await mainSnippet(page, 50),
  precheck_text: await mainText(page).then((t) => {
    const m = t.match(/预检[^\n]{0,80}|未返回[^\n]{0,40}|INPUT_OBJECT_INVALID[^\n]{0,40}/);
    return m ? m[0] : null;
  }),
};
dump('scout-empty.json', emptyState);
gate.steps.empty_start_disabled = {
  pass: emptyState.start_disabled === true,
  enabled: emptyState.start_disabled === false,
};

// 从对比篮带入
let importOk = false;
let selectedCount = 0;
try {
  const importBtn = page.getByRole('button', { name: '从对比篮带入' }).first();
  await importBtn.click({ timeout: 8000 });
  await page.waitForTimeout(1000);

  // 切到服务机构 Tab（若有）
  const orgTab = page.getByRole('tab', { name: /服务机构/ }).first();
  if (await orgTab.count()) {
    await orgTab.click().catch(() => {});
    await page.waitForTimeout(500);
  }

  const modalInfo = {
    modal_text: await page.evaluate(() => {
      const m = document.querySelector(
        '.arco-modal:not([style*="display: none"]), .arco-drawer:not([style*="display: none"])',
      );
      return (m?.innerText || '').slice(0, 1200);
    }),
    checkboxes: await page
      .locator('.arco-modal:visible .arco-checkbox, .arco-drawer:visible .arco-checkbox')
      .count(),
  };
  dump('scout-import-modal.json', modalInfo);

  const cbs = page.locator(
    '.arco-modal:visible .arco-checkbox:not(.arco-checkbox-disabled), .arco-drawer:visible .arco-checkbox:not(.arco-checkbox-disabled)',
  );
  const n = Math.min(await cbs.count(), 3);
  for (let i = 0; i < n; i++) {
    await cbs.nth(i).click().catch(() => {});
    await page.waitForTimeout(200);
  }
  selectedCount = n;

  const ok = page.locator('.arco-modal:visible, .arco-drawer:visible').getByRole('button', { name: /确定|确认|带入/ }).first();
  if (await ok.count()) {
    await ok.click().catch(() => {});
  } else {
    const ok2 = page.getByRole('button', { name: /确定|确认|带入/ }).last();
    if (await ok2.count()) await ok2.click().catch(() => {});
  }
  await page.waitForTimeout(1200);
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(400);
  importOk = true;
} catch (e) {
  dump('scout-import-fail.json', { error: String(e).slice(0, 300) });
}

const afterImport = {
  import_ok: importOk,
  selected_attempt: selectedCount,
  start_disabled: await startBtn.isDisabled().catch(() => null),
  start_class: await startBtn.getAttribute('class').catch(() => ''),
  main_snippet: await mainSnippet(page, 60),
  precheck_text: await mainText(page).then((t) => {
    const m = t.match(/预检[^\n]{0,80}|未返回[^\n]{0,40}|请确认对象[^\n]{0,40}|数量[^\n]{0,40}/);
    return m ? m[0] : null;
  }),
  body_has_precheck_fail: await mainText(page).then((t) => /预检未返回|预检失败/.test(t)),
};
dump('scout-after-import.json', afterImport);
gate.steps.select_objects = {
  pass: importOk && selectedCount >= 1,
  selected_attempt: selectedCount,
  import_ok: importOk,
};
gate.steps.start_analysis_enabled = {
  pass: afterImport.start_disabled === false,
  enabled: afterImport.start_disabled === false,
  note: selectedCount < 2 ? '用例要求 2~5 家；篮内可勾选家数可能不足' : undefined,
};
gate.steps.precheck = {
  pass: !afterImport.body_has_precheck_fail,
  fail_text_seen: afterImport.body_has_precheck_fail,
  note: afterImport.precheck_text,
};

// 若可点则发起（观察过程/结果，不卡死）
if (afterImport.start_disabled === false) {
  try {
    await startBtn.click({ timeout: 5000 });
    await page.waitForTimeout(4000);
    const afterStart = {
      url: page.url(),
      main_snippet: await mainSnippet(page, 80),
      has_processing: await mainText(page).then((t) => /生成中|计算中|可视化分析过程/.test(t)),
      has_fail: await mainText(page).then((t) => /失败|错误|预检未返回/.test(t)),
      has_view_result: await page.getByRole('button', { name: /查看结果/ }).count(),
    };
    dump('scout-after-start.json', afterStart);
    gate.steps.start_clicked = { pass: true, ...afterStart };

    for (let i = 0; i < 15; i++) {
      await page.waitForTimeout(2000);
      const t = await mainText(page);
      if (/查看结果|排名|雷达|失败|错误|暂无过程|任务状态/.test(t) && !/正在展示分析过程/.test(t)) {
        dump('scout-result.json', {
          snippet: t
            .split('\n')
            .map((s) => s.trim())
            .filter(Boolean)
            .slice(0, 100),
        });
        break;
      }
      if (/失败|预检未返回|错误/.test(t)) {
        dump('scout-result.json', { fail: true, snippet: t.slice(0, 1500) });
        break;
      }
    }
  } catch (e) {
    dump('scout-after-start.json', { error: String(e).slice(0, 300) });
    gate.steps.start_clicked = { pass: false, error: String(e).slice(0, 200) };
  }
} else {
  dump('scout-after-start.json', { skipped: true, reason: '开始评估仍禁用' });
  gate.steps.start_clicked = { pass: false, skipped: true };
}

// 分析记录：是否有已完成任务
await page.getByRole('tab', { name: '分析记录' }).click().catch(() => {});
await page.waitForTimeout(1000);
const records = {
  url: page.url(),
  snippet: await mainSnippet(page, 50),
  row_count: await mainLoc(page).locator('table tbody tr, .arco-table-tr, [class*=record]').count(),
  has_success: await mainText(page).then((t) => /成功|已完成|success|查看结果/.test(t)),
  empty: await mainText(page).then((t) => /暂无|空|还没有/.test(t)),
};
dump('scout-records.json', records);
gate.steps.history_completed = {
  pass: records.has_success === true,
  has_success: records.has_success,
  empty_hint: records.empty,
};

await page.screenshot({ path: path.join(outDir, 'env-gate.png'), fullPage: false });
dump('scout-gate-raw.json', gate);

await browser.close();
console.log('probe ok →', outDir);
console.log(
  JSON.stringify(
    {
      start_enabled: gate.steps.start_analysis_enabled?.pass,
      precheck: gate.steps.precheck?.pass,
      history: gate.steps.history_completed?.pass,
      selected: selectedCount,
    },
    null,
    2,
  ),
);
