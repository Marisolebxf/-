#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-chain-shortboard P0-18（FUNC-00698 环节参数直达恢复）写前落局探查。
 * 落局判定①（任务书按序）：探 segment 参数处理链路是否独立于环节行：
 *   s1 fresh 起任务（新一代信息技术）→「查看结果」进结果态（用例前置「已进入结果态」）
 *   s2 结果态 URL 手工拼 segment=<任意值> goto 冷加载（graph P0-23/24 同款手法）→ 12s 观察窗：
 *      是否有「环节不存在」类提示 / URL 清参 / .arco-drawer 或任何面板开启
 *   s3 任务 result_data / 记录 API 探是否有任何 stages/segment 标识可用（落局②的前提）
 * 公约：独立无头一次性；产物只落本目录；失败落 json 继续不卡死；不动业务仓。
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
const OUT = { probed_at: new Date().toISOString(), entry: 'svc-chain-shortboard', case: 'P0-18 / FUNC-00698' };
const dump = () => fs.writeFileSync(path.join(__dirname, '_probe-p018.json'), JSON.stringify(OUT, null, 2), 'utf8');
const safe = async (fn) => { try { return await fn(); } catch (e) { return { err: String((e && e.message) || e).slice(0, 300) }; } };
const mainText = async (page) => ((await page.locator('main').first().innerText().catch(() => '')) || '');

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
    await close.first().click({ timeout: 1500 }).catch(() => {});
    await page.waitForTimeout(300);
  }
}

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await ctx.newPage();

// s1 —— fresh 起任务进结果态
OUT.s1_fresh_to_result = await safe(async () => {
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(800);
  await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
    .filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
  if (!(await start.isEnabled())) return { err: '开始分析不可点（前置失败）' };
  await start.click({ timeout: 8000 });
  let url = page.url(); let taskId = null;
  const pollTask = async (ms) => { for (let i = 0; i < Math.ceil(ms / 1000); i++) { await page.waitForTimeout(1000); url = page.url(); if (/view=processing|view=result/.test(url)) { const m = /[?&]task_id=(SVC-[0-9-]+)/.exec(url); if (m) return m[1]; } } return null; };
  taskId = await pollTask(10000);
  if (!taskId) {
    // 1 次诚实重试（共享账号偶发瞬时；按钮仍在配置态才复点）
    const s2btn = page.getByRole('button', { name: '开始分析', exact: true }).first();
    if ((await s2btn.count()) && (await s2btn.isVisible().catch(() => false)) && (await s2btn.isEnabled().catch(() => false)) && !/[?&]view=/.test(page.url())) {
      await s2btn.click({ timeout: 8000 });
      taskId = await pollTask(12000);
    }
  }
  if (!taskId) return { err: '未进任务态（含 1 次诚实重试）: ' + url };
  let body = '';
  for (let i = 0; i < 10; i++) { body = await mainText(page); if (/分析结果已生成/.test(body)) break; await page.waitForTimeout(1000); }
  // 「查看结果」P0-11 同款：非 disabled 按钮 + 一次 fallback 复点（首点偶发停在过程页）
  const vr = page.getByRole('button', { name: /查看结果/ }).filter({ hasNot: page.locator('.arco-btn-disabled') }).first();
  await vr.click({ timeout: 8000 });
  await page.waitForTimeout(3000);
  let u0 = page.url();
  if (/view=processing/.test(u0) && /查看结果/.test(await mainText(page))) {
    const vr2 = page.getByRole('button', { name: /查看结果/ }).filter({ hasNot: page.locator('.arco-btn-disabled') }).first();
    if (await vr2.count()) { await vr2.click({ timeout: 5000 }).catch(() => {}); await page.waitForTimeout(2500); }
    u0 = page.url();
  }
  const b0 = await mainText(page);
  await page.screenshot({ path: path.join(__dirname, 'probe-p018-s1-result.png') });
  return {
    task_id: taskId, result_url: u0, view_result: /view=result/.test(u0),
    shell_ok: /全周期服务链路/.test(b0), honest_empty: /该产业服务供给数据不足/.test(b0),
    stations: await page.locator('[data-stage-id], .svc-eco-metro-station').count(),
    drawers: await page.locator('.arco-drawer').count(),
  };
});

const taskId = OUT.s1_fresh_to_result && OUT.s1_fresh_to_result.task_id;
const resultUrl = OUT.s1_fresh_to_result && OUT.s1_fresh_to_result.result_url;

// s2 —— 结果态 URL 手工拼 segment=<任意值> 冷加载（观察：清参 / 提示 / 面板 / 抽屉）
OUT.s2_segment_coldload = await safe(async () => {
  if (!resultUrl || !/view=result/.test(resultUrl)) return { skipped: 's1 未落结果态' };
  const segUrl = /[?&]segment=/.test(resultUrl)
    ? resultUrl.replace(/([?&])segment=[^&]*/, '$1segment=INVALID-SEGMENT-404')
    : resultUrl + '&segment=INVALID-SEGMENT-404';
  await page.goto(segUrl, { waitUntil: 'domcontentloaded' });
  if (page.url().includes('/login')) return { err: 'goto 后落 /login（会话丢失）' };
  let msgText = ''; let cleaned = false; let drawerSeen = false; let drawerText = ''; let urlNow = '';
  const deadline = Date.now() + 12000;
  while (Date.now() < deadline) {
    const mts = await page.locator('.arco-message, .arco-message-list, .arco-notification').allInnerTexts().catch(() => []);
    const mt = ((mts || []).join(' ') || '').trim();
    if (!msgText && /环节不存在|不存在|无效/.test(mt)) msgText = mt.slice(0, 120);
    if (!cleaned && !/[?&]segment=/.test(page.url())) cleaned = true;
    if (!drawerSeen) drawerSeen = await page.locator('.arco-drawer').first().isVisible().catch(() => false);
    urlNow = page.url();
    if (msgText && cleaned && drawerSeen) break;
    await page.waitForTimeout(400);
  }
  if (drawerSeen) drawerText = ((await page.locator('.arco-drawer').first().innerText().catch(() => '')) || '').slice(0, 200);
  const body = await mainText(page);
  await page.screenshot({ path: path.join(__dirname, 'probe-p018-s2-segment-coldload.png') });
  return {
    seg_url_loaded: segUrl, final_url: urlNow, segment_cleaned: cleaned,
    stage_missing_msg: msgText || null, drawer_visible: drawerSeen, drawer_text: drawerText || null,
    any_segment_key_in_dom: /segment|环节参数/.test(body) ? body.slice(0, 0) || true : false,
    body_head: body.slice(0, 400), still_result_view: /view=result/.test(urlNow), task_kept: taskId ? urlNow.includes(taskId) : null,
  };
});

// s3 —— 任务 result_data / 记录 API 探 stages/segment 标识（落局②前提：有无有效 segment 标识源）
OUT.s3_segment_id_sources = await safe(async () => {
  if (!taskId) return { skipped: '无 taskId' };
  return await page.evaluate(async (tid) => {
    const get = async (p) => { try { const r = await fetch(p); const t = await r.text(); let j = null; try { j = JSON.parse(t) } catch (e) {} return { status: r.status, j } } catch (e) { return { status: 0, err: String(e).slice(0, 120) } } };
    const post = async (p, b) => { try { const r = await fetch(p, { method: 'POST', headers: { 'Content-Type': 'application/json;charset=utf-8' }, body: JSON.stringify(b || {}) }); const t = await r.text(); let j = null; try { j = JSON.parse(t) } catch (e) {} return { status: r.status, j } } catch (e) { return { status: 0, err: String(e).slice(0, 120) } } };
    const out = { result: null, detail: null, records: null, stage_rows: [], segment_ids: [] };
    // 结果接口（前端 analysisTaskResult：GET /tasks/{id}/result?user_id=guest）
    const r = await get('/api/topicAsync/topic/v1/analysis/tasks/' + encodeURIComponent(tid) + '/result?user_id=guest');
    if (r.j) {
      const root = r.j.data || r.j;
      out.result = { status: r.status, code: r.j.code, data_keys: root && typeof root === 'object' ? Object.keys(root).slice(0, 24) : [] };
      for (const k of ['stages', 'gap', 'links', 'segments', 'shortboard', 'items', 'rows', 'models']) {
        const v = root && typeof root === 'object' ? root[k] : null;
        if (Array.isArray(v) && v.length) out.stage_rows.push({ from: 'result', key: k, len: v.length, sample: JSON.stringify(v[0]).slice(0, 200) });
      }
    }
    // 详情接口（resultData 快照）
    const dt = await get('/api/topicAsync/topic/v1/analysis/tasks/' + encodeURIComponent(tid) + '?user_id=guest');
    if (dt.j) {
      const t = dt.j.data || dt.j;
      out.detail = { status: dt.status, code: dt.j.code, keys: t && typeof t === 'object' ? Object.keys(t).slice(0, 24) : [] };
      const rdRaw = t && typeof t === 'object' ? (t.resultData || t.result_data) : null;
      if (rdRaw && typeof rdRaw === 'string') {
        try {
          const rd = JSON.parse(rdRaw);
          const root = rd.data || rd;
          for (const k of ['stages', 'gap', 'links', 'segments', 'shortboard', 'items', 'rows', 'models']) {
            const v = root && typeof root === 'object' ? root[k] : null;
            if (Array.isArray(v) && v.length) out.stage_rows.push({ from: 'detail.resultData', key: k, len: v.length, sample: JSON.stringify(v[0]).slice(0, 200) });
          }
        } catch (e) { out.detail.rd_parse_err = String(e).slice(0, 80); }
      } else if (rdRaw && typeof rdRaw === 'object') {
        out.detail.resultData_type = 'object';
      }
    }
    // 记录列表（user_id 过滤）
    const rl = await post('/api/topicAsync/topic/v1/analysis/tasks/list', { user_id: 'guest', page: 1, size: 20 });
    if (rl.j) {
      const items = (rl.j.data && rl.j.data.items) || rl.j.items || [];
      out.records = { status: rl.status, count: items.length };
      const mine = items.filter((x) => String(x.task_id || '') === tid);
      // 深挖 result_data / models / stages / gap
      const stageBags = [];
      for (const it of mine) {
        const rd = it.result_data || it.resultData || (it.result && it.result.data);
        if (rd && typeof rd === 'object') {
          const root = rd.data || rd;
          for (const k of ['stages', 'gap', 'links', 'segments', 'shortboard', 'items', 'rows', 'models']) {
            const v = root[k];
            if (Array.isArray(v) && v.length) stageBags.push({ key: k, len: v.length, sample: JSON.stringify(v[0]).slice(0, 200) });
          }
        }
      }
      out.stage_rows = stageBags;
      if (!mine.length) out.records.note = 'task_id 不在 list 返回（可能在其他分页）';
    }
    return out;
  }, taskId);
});

dump();
console.log(JSON.stringify(OUT, null, 2));
await browser.close();
