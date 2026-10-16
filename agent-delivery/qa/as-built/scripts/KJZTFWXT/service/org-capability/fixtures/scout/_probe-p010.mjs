#!/usr/bin/env node
/**
 * 一次性无头探针（P0-10 写稿用）：FUNC-00679 分析记录列表 + 打开结果 + Tab 往返配置保留。
 * 不点「开始评估」。产物落 scout-p010.json；勿当 runner。
 */
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const target = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;
const outDir = __dirname;

async function ensureLogin(page) {
  await page.waitForTimeout(600);
  if (!page.url().includes('/login')) return;
  const pw = page.locator('input[type=password]');
  await pw.first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
  if (!(await pw.count())) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await pw.first().fill('123456');
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

async function snapConfig(page) {
  const spins = page.locator('[role=spinbutton]');
  const n = await spins.count();
  const weights = [];
  for (let i = 0; i < Math.min(n, 5); i++) weights.push(String(await spins.nth(i).inputValue().catch(() => '')));
  const head = ((await page.locator('.svc-org-cap-compare__head').innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  const tags = page.locator('.svc-org-cap-compare__tags .arco-tag');
  const tagN = await tags.count();
  const tagTxt = [];
  for (let i = 0; i < Math.min(tagN, 8); i++) tagTxt.push(((await tags.nth(i).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim());
  const sumHint = ((await page.getByText(/权重合计/).first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  return { weights, head, tagN, tagTxt, sumHint, url: page.url() };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), case: 'P0-10', func: '00679' };

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  await closeBasket(page);

  // 改权重作往返探针标记（验后还原）
  const spins0 = page.locator('[role=spinbutton]');
  await spins0.first().waitFor({ state: 'visible', timeout: 10000 });
  const beforeEdit = await snapConfig(page);
  out.before_edit = beforeEdit;
  await spins0.nth(0).fill('30');
  await page.keyboard.press('Tab');
  await page.waitForTimeout(500);
  // 尝试带入对比篮（若有）
  const imp = page.locator('[data-testid="svc-org-cap-import-basket"]');
  if (await imp.count()) {
    await imp.click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(1000);
  }
  out.after_edit = await snapConfig(page);

  // 切分析记录
  await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
  await page.waitForTimeout(2000);
  const recTxt = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  const ids = [...new Set(recTxt.match(/SVC-\d+-\d+/g) || [])];
  const headers = ['任务', '类型', '状态', '创建时间', '操作'].map((h) => ({ h, ok: recTxt.includes(h) }));
  const emptyHints = ['暂无', '空', '无记录', '暂无数据', '还没有'].filter((k) => recTxt.includes(k));
  out.records = {
    url: page.url(),
    ids,
    row_hint_count: ids.length,
    headers,
    empty_hints: emptyHints,
    has_view_result: /查看结果/.test(recTxt),
    has_view_process: /查看过程/.test(recTxt),
    snippet: recTxt.replace(/\s+/g, ' ').slice(0, 500),
  };

  // 打开一条结果
  const vb = page.getByRole('button', { name: '查看结果' });
  const view = (await vb.count()) ? vb.first() : page.getByText('查看结果', { exact: true }).first();
  if (await view.count()) {
    await view.click({ timeout: 5000 });
    await page.waitForTimeout(2000);
    out.opened_result = {
      url: page.url(),
      has_view_result: /view=result/.test(page.url()),
      task_id: (page.url().match(/task_id=(SVC-\d+-\d+)/) || [])[1] || null,
      title_ok: await page.getByText('技术力横向对比结果', { exact: true }).first().isVisible().catch(() => false),
    };
  } else {
    out.opened_result = { error: 'no 查看结果' };
  }

  // 切回主 Tab
  await page.getByRole('tab', { name: '服务机构技术力评估分析', exact: true }).click({ timeout: 8000 });
  await page.waitForTimeout(2000);
  await closeBasket(page);
  out.after_roundtrip = await snapConfig(page);
  out.weight_preserved = JSON.stringify(out.after_roundtrip.weights) === JSON.stringify(out.after_edit.weights);
  out.tag_preserved = out.after_roundtrip.tagN === out.after_edit.tagN && JSON.stringify(out.after_roundtrip.tagTxt) === JSON.stringify(out.after_edit.tagTxt);
  out.head_cur_match = (out.after_roundtrip.head.match(/当前(\d+)家/) || [])[1] === (out.after_edit.head.match(/当前(\d+)家/) || [])[1];

  // 还原权重
  const spinsR = page.locator('[role=spinbutton]');
  if (await spinsR.count()) {
    await spinsR.nth(0).fill('25');
    await page.keyboard.press('Tab');
    await page.waitForTimeout(400);
  }
  out.after_restore = await snapConfig(page);
} catch (e) {
  out.error = String(e && e.stack ? e.stack : e);
} finally {
  fs.writeFileSync(path.join(outDir, 'scout-p010.json'), JSON.stringify(out, null, 2));
  await browser.close();
  console.log(JSON.stringify({ ok: !out.error, weight_preserved: out.weight_preserved, tag_preserved: out.tag_preserved, ids: out.records?.ids, opened: out.opened_result }, null, 2));
}
