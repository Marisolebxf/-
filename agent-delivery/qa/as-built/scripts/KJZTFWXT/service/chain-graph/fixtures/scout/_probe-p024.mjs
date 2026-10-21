#!/usr/bin/env node
/**
 * P0-24（FUNC-00724 备选-机构参数直达恢复）写前探针——找有效机构标识（org id）。
 * 落局判定（父单）：探得有效 org → goto 拼 org=<有效id> 冷加载恢复抽屉；探不得 → 诚实 skip n/a。
 * 探法（按序，探到即用）：
 *   S1 服务机构检索 POST /svc/topic/v1/service/search/orgs（keyword 多关键词轮询）→ items[].org_id
 *      （画像抽屉复用机构分析同一语义，org id 格式从其接口响应探得）
 *   S2 候选 id 逐个过 POST /svc/topic/v1/service/profile/get（抽屉真实数据源）→ isProfileCard 有卡 = 有效
 *   S3 graph 任务结果 records API / eco-graph 接口响应里 nodes 中的 org id（hang 空大概率无，兜底核）
 *   S4（若 S1/S2 探得）走真实链路冷加载验证：goto task_id 结果态 URL + &org=<有效id> → .arco-drawer 开启
 * 公约：独立无头；失败落 scout 继续；产物只进本目录。token 从登录后 localStorage 取，Authorization: Bearer。
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
const OUT = { started_at: new Date().toISOString() };
const dump = (n, d) => { fs.writeFileSync(path.join(__dirname, n), JSON.stringify(d, null, 2), 'utf8'); };
const safe = async (fn) => { try { return await fn(); } catch (e) { return { err: String((e && e.message) || e).slice(0, 300) }; } };

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();

  // 登录拿 token（页面 fetch 自带凭证；直接用 page.evaluate fetch 最省事）
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.goto(BASE + '/service/chain-analysis?workspace=graph&tab=graph', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  OUT.login_url = page.url();

  // 页内 fetch 工具：浏览器上下文里发（同源 + Authorization 由前端约定手工附加）
  OUT.token_present = await page.evaluate(() => {
    const keys = [];
    for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (/token|Token/i.test(k)) keys.push(k); }
    return { keys, has: keys.map((k) => [k, (localStorage.getItem(k) || '').slice(0, 24)]) };
  });
  const token = await page.evaluate(() => {
    // 前端 TOKEN_KEY 常量名未知，扫全部 localStorage 找 Bearer 型 token
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      const v = localStorage.getItem(k) || '';
      if (/^(ey[A-Za-z0-9_-]{10,}|[A-Za-z0-9_-]{20,})$/.test(v) && /token|access/i.test(k)) return v;
    }
    return null;
  });

  const apiPost = async (pathName, body) => page.evaluate(async ({ pathName, body, token }) => {
    const headers = { 'Content-Type': 'application/json;charset=utf-8' };
    if (token) headers.Authorization = 'Bearer ' + token;
    const resp = await fetch(pathName, { method: 'POST', headers, body: JSON.stringify(body || {}) });
    const text = await resp.text();
    let json = null;
    try { json = JSON.parse(text); } catch { /* keep raw */ }
    return { status: resp.status, json, raw: text.slice(0, 600) };
  }, { pathName, body, token });

  // ---- S1 服务机构检索：多关键词轮询 ----
  OUT.s1_search_orgs = [];
  const kws = ['深圳', '检验检测', '知识产权', '科技创新服务', '广东', '测试'];
  for (const kw of kws) {
    const r = await safe(() => apiPost('/svc/topic/v1/service/search/orgs', { keyword: kw, page: 1, size: 10 }));
    const items = r && r.json && (r.json.data || r.json).items;
    const ids = Array.isArray(items) ? items.slice(0, 6).map((it) => ({ org_id: it.org_id || null, code: it.service_org_code || null, name: it.name_cn || it.name || null })) : [];
    OUT.s1_search_orgs.push({ kw, status: r && r.status, err: r && r.err, total: r && r.json && (r.json.data || r.json).total, ids });
    if (ids.length && ids.some((x) => x.org_id || x.code)) break;
  }
  const candidates = [];
  for (const row of OUT.s1_search_orgs) for (const id of (row.ids || [])) if (id.org_id || id.code) candidates.push(id);
  OUT.s1_candidate_count = candidates.length;

  // ---- S2 候选 id 逐个过 profile/get（抽屉真实数据源，isProfileCard 口径）----
  OUT.s2_profile_get = [];
  let valid = null;
  const uniq = new Set();
  for (const c of candidates.slice(0, 12)) {
    const key = c.org_id || c.code;
    if (!key || uniq.has(key)) continue;
    uniq.add(key);
    const r = await safe(() => apiPost('/svc/topic/v1/service/profile/get', { org_id: key }));
    const d = r && r.json && (r.json.data !== undefined ? r.json.data : r.json);
    const card = !!(d && typeof d === 'object' && d.found !== false && d.empty !== true &&
      String(d.org_id ?? d.service_org_code ?? '').trim() || String(d && d.name_cn || '').trim());
    const name = d && (d.name_cn || d.name) || null;
    OUT.s2_profile_get.push({ key, status: r && r.status, has_card: card, name, found: d && d.found, empty: d && d.empty });
    if (card) { valid = { org_id: key, name }; break; }
  }
  OUT.s2_valid_org = valid;

  // ---- S3 graph 任务结果 nodes 中的 org id（hang 空兜底核）----
  OUT.s3_eco_graph = await safe(async () => {
    const r = await apiPost('/svc/topic/v1/service/eco-graph', { filter: 'orgs_and_actors', industry: 'INB1701', industry_id: 'INB1701' });
    const d = r.json && (r.json.data || r.json);
    const nodes = d && Array.isArray(d.nodes) ? d.nodes : [];
    return { status: r.status, node_count: nodes.length, sample: nodes.slice(0, 5).map((n) => ({ id: n.org_id || n.id || null, name: n.name || n.name_cn || null, kind: n.kind || n.node_type || null })) };
  });

  // ---- S4 走真实链路冷加载验证（若 S1/S2 探得）----
  if (valid) {
    OUT.s4_cold_load_verify = await safe(async () => {
      // fresh 起一条任务（P0-22/P0-23 同款链路）拿 task_id 结果态 URL
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
      await page.waitForURL((u) => String(u).includes('view=processing'), { timeout: 15000 });
      let body = '';
      for (let i = 0; i < 10; i++) { body = ((await page.locator('main').first().innerText().catch(() => '')) || ''); if (/分析结果已生成/.test(body)) break; await page.waitForTimeout(1000); }
      if (!/分析结果已生成/.test(body)) return { err: '首发未停过程页引导态: ' + page.url() };
      const mA = /task_id=(SVC-[0-9-]+)/.exec(page.url());
      if (!mA) return { err: '未捕获 task_id: ' + page.url() };
      const taskId = mA[1];
      const vr = page.getByRole('button', { name: '查看结果', exact: true }).first();
      await vr.click({ timeout: 8000 });
      await page.waitForTimeout(2000);
      const u0 = page.url();
      if (!/view=result/.test(u0)) return { err: '查看结果未落结果态: ' + u0 };
      // 拼 org=<有效id> 冷加载
      const orgUrl = /[?&]org=/.test(u0) ? u0.replace(/([?&])org=[^&]*/, '$1org=' + encodeURIComponent(valid.org_id)) : u0 + '&org=' + encodeURIComponent(valid.org_id);
      await page.goto(orgUrl, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);
      const drawer = page.locator('.arco-drawer').first();
      const drawerVisible = await drawer.isVisible().catch(() => false);
      const drawerText = drawerVisible ? ((await drawer.innerText().catch(() => '')) || '').slice(0, 300) : '';
      const uFinal = page.url();
      await page.screenshot({ path: path.join(__dirname, 'probe-p024-s4.png') });
      return {
        taskId, org: valid.org_id, org_name: valid.name,
        drawer_visible: drawerVisible, drawer_text_head: drawerText.slice(0, 160),
        url_keeps_org: /[?&]org=/.test(uFinal), url_keeps_task: uFinal.includes(taskId),
        title_seen: drawerText.includes('机构画像'), name_seen: valid.name ? drawerText.includes(valid.name) : null,
      };
    });
  } else {
    OUT.s4_cold_load_verify = { skipped: 'S1/S2 未探得有效 org（探查途径与结果见 s1/s2/s3）' };
  }

  OUT.finished_at = new Date().toISOString();
  await page.screenshot({ path: path.join(__dirname, 'probe-p024-final.png') }).catch(() => {});
  dump('_probe-p024.json', OUT);
  await browser.close();
  console.log('DONE ->', path.join(__dirname, '_probe-p024.json'));
})().catch((e) => { dump('_probe-p024.json', { fatal: String(e) }); console.error(e); process.exit(1); });
