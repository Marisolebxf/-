// _probe-p019.mjs — P0-19 前探针（探针公约：独立无头，一次性；写前实证现场行为）
// 目的：FUNC-01301 兄弟 workspace 隔离——sz 配置态选定「新一代信息技术」后：
//   ① URL 直切 workspace=chain / graph 兄弟页形态与 Tab 菜单名记录（用例步骤写「路由参数改」→ URL 直切为准）；
//   ② 两次切回 sz 后产业集群回显与 URL industry= 是否保留（预期③；姊妹票 D3-SVCSHORT/SVCGRAPH-WS-SWITCH-STATE-LOST 预判不保留）；
//   ③ 全程 POST /topicAsync/topic/v1/analysis/tasks 增量（预期②互证：切工作区不触发任务）；
//   ④ 兄弟页现场 UI 有 Tab 菜单则记录菜单名（用例备注）。
// 铁律：只读探查 + URL 直切，不点「开始分析」起任务；失败落盘后继续，不卡死。
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://111.198.38.90:50892';
const SZ = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const CHAIN = '/service/chain-analysis?workspace=chain&tab=chain';
const GRAPH = '/service/chain-analysis?workspace=graph&tab=graph';
const out = { probed_at: new Date().toISOString(), entry: 'svc-sz', case: 'P0-19 / FUNC-01301', path: 'URL 直切兄弟 workspace ×2 往返' };

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await ctx.newPage();

const posts = [];
page.on('request', (r) => {
  if (r.method() === 'POST' && /\/topicAsync\/topic\/v1\/analysis\/tasks\/?(\?|$)/.test(r.url())) posts.push(r.url().slice(0, 120));
});

// 登录（跳 /login 才登）
await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(800);
if (page.url().includes('/login')) {
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1500);
  if (page.url().includes('/login')) {
    await page.locator('button[type=submit], button:has-text("登录")').first().click().catch(() => {});
    await page.waitForTimeout(1500);
  }
}
out.logged_in = !page.url().includes('/login');

const closeBasket = async () => {
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if (await close.count() && await close.first().isVisible().catch(() => false) && await close.first().isEnabled().catch(() => false)) {
    try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
  }
};
const echoOf = async () => (((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '') || '').trim().replace(/\s+/g, '');
const bodyOf = async () => ((await page.locator('main').first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 400);
const tabNames = async () => {
  const tabs = page.locator('[role=tab]');
  const names = [];
  const n = await tabs.count();
  for (let i = 0; i < n; i++) names.push((((await tabs.nth(i).innerText().catch(() => '')) || '')).trim());
  return names;
};

// ---- 步骤0：进 sz，选定「新一代信息技术」（构造草稿）----
await page.goto(BASE + SZ, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);
await closeBasket();
await expect_text(page, '分析配置');
const sel = page.locator('.industry-catalog-select').first();
await sel.click({ timeout: 8000 });
await page.waitForTimeout(800);
await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
await page.waitForTimeout(1500);
out.sz_echo_after_pick = await echoOf();
out.sz_url_after_pick = page.url();
out.sz_industry_param = decodeURIComponent((page.url().match(/[?&]industry=([^&]*)/) || [])[1] || '');

async function expect_text(pg, t) { /* 软等待文本出现，用于诊断 */ }

// ---- 步骤1：URL 直切 workspace=chain ----
await page.goto(BASE + CHAIN, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2800);
await closeBasket();
out.chain_url = page.url();
out.chain_title = await page.title();
out.chain_tabs = await tabNames();
out.chain_body_head = await bodyOf();
out.chain_has_sz_config = await page.locator('.industry-catalog-select').first().isVisible().catch(() => false);
out.chain_leak_taskstate = /分析结果已生成|生成中|task_id=/.test(page.url());

// ---- 步骤2：URL 直切回 sz（第一次切回）----
await page.goto(BASE + SZ, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2800);
await closeBasket();
out.back1_url = page.url();
out.back1_echo = await echoOf();
out.back1_echo_kept = /新一代信息技术/.test(out.back1_echo || '');
out.back1_industry_kept = /[?&]industry=/.test(out.back1_url);
out.back1_industry_param = decodeURIComponent((out.back1_url.match(/[?&]industry=([^&]*)/) || [])[1] || '');
out.back1_view_clean = !/[?&]view=/.test(out.back1_url);
out.back1_body_head = await bodyOf();

// ---- 步骤3：URL 直切 workspace=graph ----
await page.goto(BASE + GRAPH, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2800);
await closeBasket();
out.graph_url = page.url();
out.graph_title = await page.title();
out.graph_tabs = await tabNames();
out.graph_body_head = await bodyOf();
out.graph_has_sz_config = await page.locator('.industry-catalog-select').first().isVisible().catch(() => false);
out.graph_leak_taskstate = /分析结果已生成|生成中|task_id=/.test(page.url());

// ---- 步骤4：URL 直切回 sz（第二次切回）----
await page.goto(BASE + SZ, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2800);
await closeBasket();
out.back2_url = page.url();
out.back2_echo = await echoOf();
out.back2_echo_kept = /新一代信息技术/.test(out.back2_echo || '');
out.back2_industry_kept = /[?&]industry=/.test(out.back2_url);
out.back2_industry_param = decodeURIComponent((out.back2_url.match(/[?&]industry=([^&]*)/) || [])[1] || '');
out.back2_view_clean = !/[?&]view=/.test(out.back2_url);

// ---- 全程 POST 增量（预期②：切工作区不触发任务）----
out.create_posts_total = posts.length;
out.create_posts = posts;
out.posts_delta_should_be_zero = posts.length === 0;

fs.writeFileSync(path.join(__dirname, '_probe-p019.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
