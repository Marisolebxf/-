#!/usr/bin/env node
/**
 * P0-14（FUNC-00700 生态包三工作区隔离 · chain 侧）写前一次性无头探针：
 * 核心场景 = chain 选定「新一代信息技术」并【发起分析】→ 菜单切 graph → 菜单切 shenzhen → 菜单切回 chain，
 * 勘：① 兄弟页是否残留 chain 结果/任务态；② 切回 chain 后产业条件/分析状态与结果是否保留（graph 侧已知
 *    不保留→D3-SVCGRAPH-WS-SWITCH-STATE-LOST；chain 侧是否同缺陷形态待本探针实证）；
 * ③ 全程是否自动产生新任务（POST 监听）。
 * 公约：独立无头（survey-page.mjs 同族）；fresh ≤1 次；单点失败落 json 继续；产物只进本目录（chain-shortboard）。
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
const ROUTE = '/service/chain-analysis?workspace=chain&tab=chain';
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
function stateWords(body) {
  return {
    chain_result_board: /全周期服务链路/.test(body),
    processing_hint: /分析结果已生成/.test(body),
    processing_word: /生成中/.test(body),
    config_zone: /分析配置/.test(body),
  };
}
function chainSummary(url, body) {
  return {
    url,
    ...stateWords(body),
    url_view: (/[?&]view=/.exec(url) || [null])[0] || null,
    url_task_id: (/[?&]task_id=(SVC-[0-9-]+)/.exec(url) || [null, null])[1],
    url_industry: (/[?&]industry=(\w+)/.exec(url) || [null, null])[1],
    body_head: body.split('\n').filter(Boolean).slice(0, 14),
  };
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

  // POST 任务创建监听（全称挂载；精确匹配尾段，排除 tasks/list 轮询）
  const posts = [];
  page.on('request', (r) => {
    if (r.method() === 'POST' && /\/topicAsync\/topic\/v1\/analysis\/tasks\/?(\?|$)/.test(r.url())) posts.push({ t: Date.now(), url: r.url().slice(0, 120) });
  });

  // 1) chain 选「新一代信息技术」+ 开始分析 → 完成停引导态（P0-13 同款链路 + 1 次诚实重试）
  OUT.pick_cluster = await safe(async () => {
    const sel = page.locator('.industry-catalog-select').first();
    await sel.click({ timeout: 6000 });
    await page.waitForTimeout(800);
    await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
      .filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
    await page.waitForTimeout(1500);
    const val = await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '');
    return { picked: (val || '').trim() };
  });

  OUT.start_analysis = await safe(async () => {
    const pollTask = async (ms) => {
      for (let i = 0; i < Math.ceil(ms / 1000); i++) {
        await page.waitForTimeout(1000);
        const u = page.url();
        if (/[?&]view=processing/.test(u)) {
          const m = u.match(/[?&]task_id=(SVC-\d{8}-\d{1,4})/);
          if (m) return m[1];
        }
      }
      return null;
    };
    const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
    if (!(await start.isEnabled())) return { err: '开始分析 disabled', picked: OUT.pick_cluster };
    await start.click({ timeout: 8000 });
    let task = await pollTask(10000);
    if (!task) {
      const s2 = page.getByRole('button', { name: '开始分析', exact: true }).first();
      if ((await s2.count()) && (await s2.isVisible().catch(() => false)) && (await s2.isEnabled().catch(() => false)) && !/[?&]view=/.test(page.url())) {
        await s2.click({ timeout: 8000 });
        task = await pollTask(12000);
      }
    }
    if (!task) return { err: '未进过程态（含 1 次诚实重试）: ' + page.url() };
    await page.waitForTimeout(2500); // ~1s 完成，停引导态
    const body = await mainText(page);
    await page.screenshot({ path: path.join(__dirname, 'probe-p014-processing.png') });
    return { task_id: task, done_hint: /分析结果已生成/.test(body), ...stateWords(body) };
  });

  const taskId = OUT.start_analysis.task_id || null;
  const postsBeforeSwitch = posts.length;
  OUT.posts_after_start = posts.slice(0, 6);

  // 2) 菜单切「服务链图谱分析」（graph）
  OUT.switch_graph = await safe(async () => {
    const m = page.getByRole('menuitem', { name: /服务链图谱分析/ }).first();
    let ok = await m.isVisible().catch(() => false);
    if (!ok) {
      const alt = page.locator('aside, nav, .arco-menu').getByText('服务链图谱分析', { exact: false }).first();
      await alt.click({ timeout: 5000 });
    } else { await m.click({ timeout: 5000 }); }
    await page.waitForTimeout(2200);
    await closeBasket(page);
    const body = await mainText(page);
    await page.screenshot({ path: path.join(__dirname, 'probe-p014-graph.png') });
    return { ...chainSummary(page.url(), body), posts_during: posts.slice(postsBeforeSwitch) };
  });
  const postsAfterGraph = posts.length;

  // 3) 菜单切「深圳服务链现状」（shenzhen）
  OUT.switch_sz = await safe(async () => {
    const m = page.getByRole('menuitem', { name: /深圳服务链现状/ }).first();
    let ok = await m.isVisible().catch(() => false);
    if (!ok) {
      const alt = page.locator('aside, nav, .arco-menu').getByText('深圳服务链现状', { exact: false }).first();
      await alt.click({ timeout: 5000 });
    } else { await m.click({ timeout: 5000 }); }
    await page.waitForTimeout(2200);
    await closeBasket(page);
    const body = await mainText(page);
    await page.screenshot({ path: path.join(__dirname, 'probe-p014-shenzhen.png') });
    return { ...chainSummary(page.url(), body), posts_during: posts.slice(postsAfterGraph) };
  });
  const postsAfterSz = posts.length;

  // 4) 菜单切回「服务链短板分析」（chain）——核心：产业条件/分析状态与结果是否保留
  OUT.switch_back = await safe(async () => {
    const m = page.getByRole('menuitem', { name: /服务链短板分析/ }).first();
    let ok = await m.isVisible().catch(() => false);
    if (!ok) {
      const alt = page.locator('aside, nav, .arco-menu').getByText('服务链短板分析', { exact: false }).first();
      await alt.click({ timeout: 5000 });
    } else { await m.click({ timeout: 5000 }); }
    await page.waitForTimeout(2600);
    await closeBasket(page);
    const url = page.url();
    const body = await mainText(page);
    const selVal = await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '');
    await page.screenshot({ path: path.join(__dirname, 'probe-p014-back.png') });
    return {
      ...chainSummary(url, body),
      cluster_kept: (selVal || '').trim(),
      posts_during: posts.slice(postsAfterSz),
    };
  });

  // 5) 分析记录 Tab：本条 task 是否在列（服务端可找回）
  OUT.records_check = await safe(async () => {
    await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
    await page.waitForTimeout(1800);
    const body = await mainText(page);
    const ids = [...body.matchAll(/SVC-\d{8}-\d+/g)].map((x) => x[0]);
    const unique = [...new Set(ids)];
    await page.screenshot({ path: path.join(__dirname, 'probe-p014-records.png') });
    return { task_in_list: taskId ? unique.includes(taskId) : null, latest_ids: unique.slice(0, 5), url: page.url() };
  });

  OUT.posts_total = posts;
  await page.screenshot({ path: path.join(__dirname, 'probe-p014-final.png') });
  dump('_probe-p014.json', OUT);
  await browser.close();
  console.log('DONE ->', path.join(__dirname, '_probe-p014.json'));
})().catch((e) => { dump('_probe-p014.json', { fatal: String(e) }); console.error(e); process.exit(1); });
