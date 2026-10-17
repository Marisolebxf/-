#!/usr/bin/env node
/**
 * P0-19（FUNC-00725）写前探针 v2——同日同条件复用判定 + 记录查看 + 切回保留完整链。
 * 前情（_probe-p019.json）：fresh SVC-20261015-028（INB1701+模式②，指纹 svc|graph|INB1701）当天已成功。
 * 本轮零 fresh：S1 干净配置态同条件再发起（当天复用判定：POST 计数 + task_id 是否复用 + toast）；
 * S2 查看结果；S3 返回配置重新分析（结果态按钮）→ 配置态回显；S4 记录 Tab 行「查看结果」；S5 切回分析 Tab 保留性。
 * 公约：独立无头；产物只进本目录。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://111.198.38.90:50892';
const OUT = {};
const dump = (n, d) => { fs.writeFileSync(path.join(__dirname, n), JSON.stringify(d, null, 2), 'utf8'); };
const safe = async (fn) => { try { return await fn(); } catch (e) { return { err: String(e && e.message || e).slice(0, 300) }; } };

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
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
}
async function mainText(page) { return ((await page.locator('main').first().innerText().catch(() => '')) || ''); }
async function toastText(page) {
  return ((await page.locator('.arco-message, .arco-message-list').first().innerText().catch(() => '')) || '').trim();
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.goto(BASE + '/service/chain-analysis?workspace=graph&tab=graph', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  const posts = [];
  page.on('request', (r) => {
    if (r.method() === 'POST' && /\/topicAsync\/topic\/v1\/analysis\/tasks\/?(\?|$)/.test(r.url())) posts.push({ t: Date.now(), url: r.url().slice(0, 120) });
  });

  // S1 干净配置态同条件再发起（当天复用判定）
  OUT.s1_same_day_start = await safe(async () => {
    const sel = page.locator('.industry-catalog-select').first();
    await sel.click({ timeout: 8000 });
    await page.waitForTimeout(600);
    await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
      .filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
    await page.waitForTimeout(800);
    await page.getByText('② 机构+关联主体', { exact: true }).first().click({ timeout: 8000 });
    await page.waitForTimeout(600);
    const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
    if (!(await start.isEnabled())) return { err: '开始分析 disabled' };
    await start.click({ timeout: 8000 });
    await page.waitForTimeout(3000);
    const toast = await toastText(page);
    const url = page.url();
    const m = /task_id=(SVC-[0-9-]+)/.exec(url);
    const body = await mainText(page);
    await page.screenshot({ path: path.join(__dirname, 'probe-p019b-s1.png') });
    return {
      url, landed_task_id: m ? m[1] : null, toast, posts: posts.length,
      new_post_created: posts.length > 0,
      done_hint: /分析结果已生成/.test(body), processing: /生成中/.test(body),
    };
  });

  // S2 引导态「查看结果」→ 结果态
  OUT.s2_view_result = await safe(async () => {
    const vr = page.getByRole('button', { name: '查看结果', exact: true }).first();
    if (!(await vr.count())) return { err: '未见「查看结果」按钮' };
    await vr.click({ timeout: 8000 });
    await page.waitForTimeout(2500);
    await closeBasket(page);
    const url = page.url();
    const body = await mainText(page);
    await page.screenshot({ path: path.join(__dirname, 'probe-p019b-s2.png') });
    return {
      url, view_result: /view=result/.test(url), has_shell: /服务生态关系图谱/.test(body),
      has_back_btn: /返回配置重新分析/.test(body),
      result_filter_bar: /产业领域/.test(body), radio_zone: /图谱滤镜|仅机构/.test(body),
    };
  });

  // S3 结果态「返回配置重新分析」→ 配置态回显
  OUT.s3_back_to_config = await safe(async () => {
    const back = page.getByRole('button', { name: /返回配置重新分析|返回配置/ }).first();
    if (!(await back.count())) return { err: '未见返回配置按钮' };
    await back.click({ timeout: 8000 });
    await page.waitForTimeout(2000);
    await closeBasket(page);
    const url = page.url();
    const body = await mainText(page);
    const selVal = ((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
    const radio = ((await page.locator('main .arco-radio.arco-radio-checked').first().innerText().catch(() => '')) || '').trim();
    await page.screenshot({ path: path.join(__dirname, 'probe-p019b-s3.png') });
    return {
      url, cluster_kept: selVal, radio_kept: radio, config_zone: /分析配置/.test(body),
      url_keeps_industry: /industry=/.test(url), url_keeps_eco_filter: /eco_filter=/.test(url),
    };
  });

  // S4 切记录 Tab → 当天任务行「查看结果」
  OUT.s4_records_view = await safe(async () => {
    const rec = page.locator('[role=tab][data-tab-key="records"]').or(page.getByRole('tab', { name: '分析记录', exact: true }));
    await rec.first().click({ timeout: 8000 });
    await page.waitForURL(/tab=records/, { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(2000);
    await closeBasket(page);
    const body0 = await mainText(page);
    // 找当天（20261015）已完成行点「查看结果」
    const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /SVC-20261015-\d+/ }).first();
    const rowText = ((await row.innerText().catch(() => '')) || '');
    const tid = (/SVC-20261015-\d+/.exec(rowText) || [])[0] || null;
    const vr = row.getByRole('button', { name: '查看结果', exact: true });
    const vrDisabled = (await vr.count()) ? !(await vr.first().isEnabled()) : null;
    if ((await vr.count()) && (await vr.first().isEnabled())) { await vr.first().click({ timeout: 8000 }); }
    await page.waitForTimeout(2200);
    const url = page.url();
    const body = await mainText(page);
    await page.screenshot({ path: path.join(__dirname, 'probe-p019b-s4.png') });
    return {
      records_url_before: page.url(), row_task_id: tid, row_text: rowText.slice(0, 120),
      view_btn_disabled: vrDisabled, after_url: url, after_view_result: /view=result/.test(url),
      has_shell: /服务生态关系图谱/.test(body), posts: posts.length,
      list_header: /任务[\s\S]*?类型[\s\S]*?状态/.test(body0),
    };
  });

  // S5 切回分析 Tab → 保留性
  OUT.s5_switch_back = await safe(async () => {
    const main = page.locator('[role=tab][data-tab-key="graph"]').or(page.getByRole('tab', { name: '服务链图谱分析', exact: true }));
    await main.first().click({ timeout: 8000 });
    await page.waitForTimeout(2200);
    await closeBasket(page);
    const url = page.url();
    const body = await mainText(page);
    const selVal = ((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
    const radio = ((await page.locator('main .arco-radio.arco-radio-checked').first().innerText().catch(() => '')) || '').trim();
    await page.screenshot({ path: path.join(__dirname, 'probe-p019b-s5.png') });
    return {
      url, cluster_kept: selVal, radio_kept: radio,
      url_keeps_industry: /industry=INB1701/.test(url), url_keeps_eco_filter: /eco_filter=/.test(url),
      url_keeps_task: /task_id=/.test(url),
      view_state: /view=result/.test(url) ? 'result' : (/view=processing/.test(url) ? 'processing' : 'config'),
      config_zone: /分析配置/.test(body), result_shell: /服务生态关系图谱/.test(body),
      processing_hint: /分析结果已生成|生成中/.test(body),
    };
  });

  OUT.posts_total = posts;
  await page.screenshot({ path: path.join(__dirname, 'probe-p019b-final.png') });
  dump('_probe-p019b.json', OUT);
  await browser.close();
  console.log('DONE ->', path.join(__dirname, '_probe-p019b.json'));
})().catch((e) => { dump('_probe-p019b.json', { fatal: String(e) }); console.error(e); process.exit(1); });
