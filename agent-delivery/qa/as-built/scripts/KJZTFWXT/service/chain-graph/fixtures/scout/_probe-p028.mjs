#!/usr/bin/env node
/**
 * P0-28（FUNC-00721 关系与节点类型过滤）写前探针：
 * fresh 首发（新一代信息技术+模式②）→「查看结果」落结果态 → 只读勘察过滤控件形态：
 * ① 结构在否（svc-eco-clip-filters / 节点类型勾选组 svc-eco-clip-node-kinds / 边类型勾选组
 *    svc-eco-clip-edge-types）——源码链 v-if="!parsed.empty" 预判 hang 空不渲染，实证定局
 * ② 若在：checkbox 清单（label 文本 + 自身 class）、默认勾选态、统计面板「统计范围」声明
 * ③ 若不在：确认 parsed.empty 空画布文案在屏（hang 空）
 * 公约：独立无头；产物只进本目录（_probe-p028.json + _probe-p028-result.png）。
 * fresh 起任务属父单授权链路（P0-19b/22~27 同款），POST 仅 1 次。
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
const OUT = { probed_at: new Date().toISOString(), base: BASE };
const dump = (n, d) => { fs.writeFileSync(path.join(__dirname, n), JSON.stringify(d, null, 2), 'utf8'); };
const safe = async (fn) => { try { return await fn(); } catch (e) { return { err: String((e && e.message) || e).slice(0, 400) }; } };

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

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);

  // 1) fresh 首发（P0-25/26/27 r1 实证链路）
  OUT.fresh_start = await safe(async () => {
    await page.goto(BASE + '/service/chain-analysis?workspace=graph&tab=graph', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1500);
    await closeBasket(page);
    const sel = page.locator('.industry-catalog-select').first();
    await sel.click({ timeout: 8000 });
    await page.waitForTimeout(600);
    await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
      .filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
    await page.waitForTimeout(800);
    await page.getByText('② 机构+关联主体', { exact: true }).first().click({ timeout: 8000 });
    await page.waitForTimeout(600);
    const radio1 = page.locator('main .arco-radio.arco-radio-checked').first();
    if (!/②/.test((await radio1.innerText().catch(() => '')) || '')) throw new Error('模式②未选中');
    const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
    if (!(await start.isEnabled())) throw new Error('合法条件后开始分析不可点');
    await start.click({ timeout: 8000 });
    await page.waitForURL((u) => /view=(processing|result)/.test(String(u)), { timeout: 15000 });
    let body = '';
    for (let i = 0; i < 10; i++) {
      body = await mainText(page);
      if (/分析结果已生成|服务生态关系图谱/.test(body)) break;
      await page.waitForTimeout(1000);
    }
    const mA = /task_id=(SVC-[0-9-]+)/.exec(page.url());
    return { taskId: mA ? mA[1] : null, guided_done: /分析结果已生成/.test(body), url: page.url().replace(BASE, '') };
  });

  // 2) 查看结果落结果态
  OUT.view_result = await safe(async () => {
    if (!/view=result/.test(page.url())) {
      const vr = page.getByRole('button', { name: '查看结果', exact: true }).first();
      await vr.click({ timeout: 8000 });
      await page.waitForTimeout(2600);
    }
    await closeBasket(page);
    const u = page.url().replace(BASE, '');
    const b = await mainText(page);
    return { url: u, has_shell: /服务生态关系图谱/.test(b) };
  });

  // 3) 过滤控件形态勘察（只读）
  OUT.filter_shape = await safe(async () => {
    const filters = page.locator('[data-testid="svc-eco-clip-filters"]').first();
    const filtersCount = await filters.count();
    const filtersVisible = filtersCount ? await filters.isVisible().catch(() => false) : false;
    const nodeGroup = page.locator('[data-testid="svc-eco-clip-node-kinds"]').first();
    const edgeGroup = page.locator('[data-testid="svc-eco-clip-edge-types"]').first();
    const nodeGroupCount = await nodeGroup.count();
    const edgeGroupCount = await edgeGroup.count();
    // checkbox 定位教训：容器内枚举 innerText + 读自身 class，勿 locator.locator 查自身
    const readChecks = async (group) => {
      const boxes = group.locator('label.arco-checkbox');
      const n = await boxes.count();
      const list = [];
      for (let i = 0; i < n; i++) {
        const el = boxes.nth(i);
        const cls = (await el.getAttribute('class')) || '';
        const txt = ((await el.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
        list.push({ text: txt, checked: /arco-checkbox-checked/.test(cls) });
      }
      return list;
    };
    const nodeChecks = nodeGroupCount ? await readChecks(nodeGroup) : null;
    const edgeChecks = edgeGroupCount ? await readChecks(edgeGroup) : null;
    const b = await mainText(page);
    const statRangeHit = /统计范围\s*=\s*当前过滤后的可见子网/.test(b);
    const hangEmptyHit = /当前 hang 无可见点边/.test(b);
    const clipEmptyHit = /当前过滤条件下无关系数据/.test(b);
    // URL 现有 clip 参数形态
    const u = page.url();
    const urlParams = {};
    for (const key of ['eco_nk', 'eco_et', 'eco_focus', 'eco_filter']) {
      const m = new RegExp('[?&]' + key + '=([^&]*)').exec(u);
      if (m) urlParams[key] = decodeURIComponent(m[1]);
    }
    // localStorage 持久化键现状（只读）
    const stored = await page.evaluate(() => window.localStorage.getItem('gkx.svc.eco.clip.v1'));
    let branch;
    if (!filtersCount || !filtersVisible) branch = 'missing(过滤控件结构性不渲染)';
    else branch = 'present(过滤控件在)';
    return {
      branch, filters_count: filtersCount, filters_visible: filtersVisible,
      node_group_count: nodeGroupCount, edge_group_count: edgeGroupCount,
      node_checks: nodeChecks, edge_checks: edgeChecks,
      stat_range_copy_hit: statRangeHit, hang_empty_copy_hit: hangEmptyHit, clip_empty_copy_hit: clipEmptyHit,
      url_clip_params: urlParams, localStorage_clip: stored,
    };
  });

  // 4) 结果态截图（证据）
  await safe(async () => {
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(__dirname, '_probe-p028-result.png'), fullPage: false });
  });

  OUT.conclusion = 'P0-28 写前探针完成：过滤控件分支=' + (OUT.filter_shape && OUT.filter_shape.branch) + '（详见 filter_shape；供 cases/P0-28.yaml 落局分支判定）';
  dump('_probe-p028.json', OUT);
  await browser.close();
  process.exit(0);
})();
