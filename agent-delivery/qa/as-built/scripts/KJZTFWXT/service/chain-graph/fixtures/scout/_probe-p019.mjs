#!/usr/bin/env node
/**
 * P0-19（FUNC-00725 分析记录与当天复用）写前一次性无头探针：
 * ① 记录 Tab 列表 + 与分析 Tab 互斥；② fresh 起任务（新一代信息技术 + 模式②）→ 同日同条件
 * 再次「开始分析」是否拦截复用（POST 计数 + Message 提示 + 记录新行）；③ 切记录 Tab → 切回
 * 分析 Tab 后产业/模式/页面状态是否保留（Tab 切换走 patchQuery merge，预判保留，以实测为准）。
 * 公约：独立无头；fresh ≤1 次（外加同条件复点 1 次属"复用尝试"不算新 fresh 组合）；
 * 单点失败落 json 继续；产物只进本目录。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
const ROUTE = '/service/chain-analysis?workspace=graph&tab=graph';
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
  await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  // 本页 POST 监听：任务创建端点（排除 list/running）
  const posts = [];
  page.on('request', (r) => {
    if (r.method() === 'POST' && /\/topicAsync\/topic\/v1\/analysis\/tasks\/?(\?|$)/.test(r.url())) posts.push({ t: Date.now(), url: r.url().slice(0, 120) });
  });

  // 1) 选「新一代信息技术」+ 模式② → 开始分析（fresh ≤1）
  OUT.fresh_start = await safe(async () => {
    const sel = page.locator('.industry-catalog-select').first();
    await sel.click({ timeout: 8000 });
    await page.waitForTimeout(600);
    await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
      .filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
    await page.waitForTimeout(800);
    await page.getByText('② 机构+关联主体', { exact: true }).first().click({ timeout: 8000 });
    await page.waitForTimeout(600);
    const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
    const enabled = await start.isEnabled();
    if (!enabled) return { err: '开始分析 disabled' };
    await start.click({ timeout: 8000 });
    await page.waitForURL((u) => String(u).includes('view=processing'), { timeout: 15000 });
    await page.waitForTimeout(2500);
    const body = await mainText(page);
    const m = /task_id=(SVC-[0-9-]+)/.exec(page.url());
    return { url: page.url(), task_id: m ? m[1] : null, done_hint: /分析结果已生成/.test(body), posts: posts.length };
  });
  const firstTaskId = OUT.fresh_start.task_id || null;

  // 2) 同日同条件复用尝试：返回配置（backToConfig）→ 仍选同条件（query 保留则不必重选，如实记录）→ 再点「开始分析」
  OUT.same_day_retry = await safe(async () => {
    // 过程页「返回配置重新分析」回配置态
    const back = page.getByRole('button', { name: /返回配置重新分析|返回配置/ }).first();
    if (await back.count()) { await back.click({ timeout: 8000 }); await page.waitForTimeout(1800); }
    await closeBasket(page);
    const url = page.url();
    const body = await mainText(page);
    // 条件是否保留（draft=1）
    const selVal = ((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
    const radio = ((await page.locator('main .arco-radio.arco-radio-checked').first().innerText().catch(() => '')) || '').trim();
    // 若条件丢失则重选（同条件：新一代信息技术 + 模式②）
    if (!/新一代信息技术/.test(selVal)) {
      const sel = page.locator('.industry-catalog-select').first();
      await sel.click({ timeout: 8000 });
      await page.waitForTimeout(600);
      await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
        .filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
      await page.waitForTimeout(800);
    }
    if (!/②/.test(radio)) {
      await page.getByText('② 机构+关联主体', { exact: true }).first().click({ timeout: 8000 });
      await page.waitForTimeout(600);
    }
    const postsBefore = posts.length;
    const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
    const enabled = await start.isEnabled();
    if (!enabled) return { err: '复用尝试时开始分析 disabled', back_url: url };
    await start.click({ timeout: 8000 });
    // 观察窗口：等拦截提示 / 跳转
    await page.waitForTimeout(2500);
    const toast = await toastText(page);
    const url2 = page.url();
    const m2 = /task_id=(SVC-[0-9-]+)/.exec(url2);
    const body2 = await mainText(page);
    // 若停引导态则点「查看结果」核对 task_id 是否复用既有
    let viewedTaskId = null;
    if (/分析结果已生成/.test(body2)) {
      const vr = page.getByRole('button', { name: '查看结果', exact: true }).first();
      if (await vr.count()) {
        await vr.click({ timeout: 8000 }).catch(() => {});
        await page.waitForTimeout(2000);
        const m3 = /task_id=(SVC-[0-9-]+)/.exec(page.url());
        viewedTaskId = m3 ? m3[1] : null;
      }
    }
    await page.screenshot({ path: path.join(__dirname, 'probe-p019-retry.png') });
    return {
      back_url: url, back_cluster_kept: selVal, back_radio_kept: radio,
      posts_during: posts.slice(postsBefore), posts_total: posts.length,
      after_url: url2, after_task_id: m2 ? m2[1] : null, toast,
      same_task_reused: m2 && firstTaskId ? m2[1] === firstTaskId : null,
      viewed_task_id: viewedTaskId,
      new_task_created: posts.length > postsBefore,
    };
  });

  // 3) 记录 Tab：列表 + 本条任务行；与分析 Tab 互斥
  OUT.records_tab = await safe(async () => {
    const rec = page.locator('[role=tab][data-tab-key="records"]').or(page.getByRole('tab', { name: '分析记录', exact: true }));
    await rec.first().click({ timeout: 8000 });
    await page.waitForURL(/tab=records/, { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(2000);
    await closeBasket(page);
    const url = page.url();
    const body = await mainText(page);
    const ids = [...new Set([...body.matchAll(/SVC-\d{8}-\d+/g)].map((x) => x[0]))];
    const configLeak = /请先确认分析条件/.test(body);
    await page.screenshot({ path: path.join(__dirname, 'probe-p019-records.png') });
    return {
      url, has_table_header: /任务[\s\S]*?类型[\s\S]*?状态[\s\S]*?创建时间[\s\S]*?操作/.test(body),
      has_today_row: ids.some((id) => firstTaskId && id === firstTaskId),
      latest_ids: ids.slice(0, 6), config_zone_leak_in_records: configLeak,
      rows_snippet: body.split('\n').filter((l) => /SVC-/.test(l)).slice(0, 6),
    };
  });

  // 4) 切回分析 Tab：状态保留性（产业/模式/页面状态）
  OUT.switch_back_analysis = await safe(async () => {
    const main = page.locator('[role=tab][data-tab-key="graph"]').or(page.getByRole('tab', { name: '服务链图谱分析', exact: true }));
    await main.first().click({ timeout: 8000 });
    await page.waitForURL((u) => !/tab=records/.test(String(u)), { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(2200);
    await closeBasket(page);
    const url = page.url();
    const body = await mainText(page);
    const selVal = ((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
    const radio = ((await page.locator('main .arco-radio.arco-radio-checked').first().innerText().catch(() => '')) || '').trim();
    await page.screenshot({ path: path.join(__dirname, 'probe-p019-back.png') });
    return {
      url, cluster_kept: selVal, radio_kept: radio,
      config_zone: /分析配置/.test(body),
      processing_hint: /分析结果已生成|生成中/.test(body),
      graph_result: /服务生态关系图谱/.test(body),
      has_task_in_url: /task_id=/.test(url),
    };
  });

  OUT.posts_total = posts;
  await page.screenshot({ path: path.join(__dirname, 'probe-p019-final.png') });
  dump('_probe-p019.json', OUT);
  await browser.close();
  console.log('DONE ->', path.join(__dirname, '_probe-p019.json'));
})().catch((e) => { dump('_probe-p019.json', { fatal: String(e) }); console.error(e); process.exit(1); });
