#!/usr/bin/env node
/**
 * P0-20（FUNC-00726 生态包三工作区隔离）写前一次性无头探针：
 * 核心场景 = graph 选定条件并【发起分析】→ 切 chain → 切 shenzhen → 切回 graph，
 * 勘：① 兄弟页是否残留 graph 结果/任务态；② 切回后产业/模式/分析状态是否保留；
 * ③ 全程是否自动产生新任务（POST 监听）。
 * 公约：独立无头；fresh ≤1 次；单点失败落 json 继续；产物只进本目录。
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
// 页面状态摘要：结果/过程/配置痕迹词
function stateWords(body) {
  return {
    graph_result: /服务生态关系图谱|双密度并排/.test(body),
    processing_hint: /分析结果已生成|生成中/.test(body),
    config_zone: /分析配置/.test(body),
    filter_radio: /图谱滤镜/.test(body),
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

  // POST 监听（全称挂载；各阶段快照清点）
  const posts = [];
  page.on('request', (r) => {
    if (r.method() === 'POST' && /\/svc\//.test(r.url())) posts.push({ t: Date.now(), url: r.url().slice(0, 120) });
  });

  // 1) graph 选「新一代信息技术」
  OUT.pick_cluster = await safe(async () => {
    const sel = page.locator('.industry-catalog-select').first();
    await sel.click({ timeout: 6000 });
    await page.waitForTimeout(600);
    await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
      .filter({ hasText: '新一代信息技术' }).first().click({ timeout: 6000 });
    await page.waitForTimeout(800);
    const val = await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '');
    return { picked: (val || '').trim() };
  });

  // 2) 开始分析 → 过程页引导态
  OUT.start_analysis = await safe(async () => {
    const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
    const enabled = await start.isEnabled();
    if (!enabled) return { err: '开始分析 disabled', picked: OUT.pick_cluster };
    await start.click({ timeout: 6000 });
    await page.waitForURL((u) => String(u).includes('view=processing'), { timeout: 15000 });
    // ~1s 完成，停引导态
    await page.waitForTimeout(2500);
    const body = await mainText(page);
    const m = /task_id=(SVC-[0-9-]+)/.exec(page.url());
    await page.screenshot({ path: path.join(__dirname, 'probe-p020-processing.png') });
    return { url: page.url(), task_id: m ? m[1] : null, done_hint: /分析结果已生成/.test(body), ...stateWords(body) };
  });

  const taskId = OUT.start_analysis.task_id || null;
  const postsBeforeSwitch = posts.length;
  OUT.posts_after_start = posts.slice(0, 6);

  // 3) 切「服务链短板分析」
  OUT.switch_chain = await safe(async () => {
    const m = page.getByRole('menuitem', { name: /服务链短板分析/ }).first();
    let ok = await m.isVisible().catch(() => false);
    if (!ok) {
      const alt = page.locator('aside, nav, .arco-menu').getByText('服务链短板分析', { exact: false }).first();
      await alt.click({ timeout: 5000 });
    } else { await m.click({ timeout: 5000 }); }
    await page.waitForTimeout(2200);
    await closeBasket(page);
    const body = await mainText(page);
    await page.screenshot({ path: path.join(__dirname, 'probe-p020-chain.png') });
    return { url: page.url(), title: body.split('\n')[0], ...stateWords(body), posts_during: posts.slice(postsBeforeSwitch) };
  });
  const postsAfterChain = posts.length;

  // 4) 切「深圳服务链现状」
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
    await page.screenshot({ path: path.join(__dirname, 'probe-p020-shenzhen.png') });
    return { url: page.url(), title: body.split('\n')[0], ...stateWords(body), posts_during: posts.slice(postsAfterChain) };
  });
  const postsAfterSz = posts.length;

  // 5) 切回「服务链图谱分析」
  OUT.switch_back = await safe(async () => {
    const m = page.getByRole('menuitem', { name: /服务链图谱分析/ }).first();
    let ok = await m.isVisible().catch(() => false);
    if (!ok) {
      const alt = page.locator('aside, nav, .arco-menu').getByText('服务链图谱分析', { exact: false }).first();
      await alt.click({ timeout: 5000 });
    } else { await m.click({ timeout: 5000 }); }
    await page.waitForTimeout(2600);
    await closeBasket(page);
    const url = page.url();
    const body = await mainText(page);
    const selVal = await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '');
    const radio = await page.locator('main .arco-radio.arco-radio-checked').first().innerText().catch(() => '');
    await page.screenshot({ path: path.join(__dirname, 'probe-p020-back.png') });
    return {
      url, cluster_kept: (selVal || '').trim(), radio_checked: (radio || '').trim(),
      ...stateWords(body), has_task_in_url: /task_id=/.test(url),
      body_head: body.split('\n').filter(Boolean).slice(0, 14),
      posts_during: posts.slice(postsAfterSz),
    };
  });

  // 6) 分析记录 Tab：本条 task 是否在列 + 最新一条 ID（新任务证据）
  OUT.records_check = await safe(async () => {
    await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
    await page.waitForTimeout(1800);
    const body = await mainText(page);
    const ids = [...body.matchAll(/SVC-\d{8}-\d+/g)].map((x) => x[0]);
    const unique = [...new Set(ids)];
    await page.screenshot({ path: path.join(__dirname, 'probe-p020-records.png') });
    return { task_in_list: taskId ? unique.includes(taskId) : null, latest_ids: unique.slice(0, 5), url: page.url() };
  });

  OUT.posts_total = posts;
  await page.screenshot({ path: path.join(__dirname, 'probe-p020-final.png') });
  dump('_probe-p020.json', OUT);
  await browser.close();
  console.log('DONE ->', path.join(__dirname, '_probe-p020.json'));
})().catch((e) => { dump('_probe-p020.json', { fatal: String(e) }); console.error(e); process.exit(1); });
