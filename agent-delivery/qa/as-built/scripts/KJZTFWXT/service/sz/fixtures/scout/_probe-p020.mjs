// _probe-p020.mjs — P0-20 前探针（探针公约：独立无头，一次性；写前实证现场行为）
// 目的：FUNC-01305 异常-分析失败态——sz 工作区 route.abort 拦截创建任务 POST
//       /topicAsync/topic/v1/analysis/tasks（精确尾段，不误伤 /tasks/list /tasks/running 轮询），
//       观察失败态形态是否与姊妹仓 chain-graph P0-29（FUNC-00731 同构）一致：
//       壳层 .arco-alert Network Error/traceId 在屏非白屏、页面壳（页头/双 Tab/配置区）+ 集群回显保留、
//       「开始分析」失败态后仍可用（重试承载）；unroute 恢复后重试 POST 200 落 view=processing
//       且 analysis_fp=svc|shenzhen| 前缀；失败态 alert 清除。
// 铁律：结束时必须 unroute（同 context 后续请求零污染）；失败落盘后继续，不卡死。
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
const ROUTE = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const out = { probed_at: new Date().toISOString(), entry: 'svc-sz', case: 'P0-20 / FUNC-01305', path: 'abort POST create-task (shenzhen workspace)' };

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await ctx.newPage();

// 全程请求记录（观察 POST 尾段 / 轮询形态）
const reqLog = [];
page.on('request', (r) => {
  const u = r.url();
  if (/topicAsync/.test(u)) reqLog.push(r.method() + ' ' + u.replace(BASE, ''));
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

await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);
const close = page.locator('button[aria-label="关闭对比篮"]');
if (await close.count() && await close.first().isVisible().catch(() => false)) { await close.first().click({ timeout: 1500 }).catch(() => {}); await page.waitForTimeout(300); }

// ---- 前置：选定产业集群（新一代信息技术）；sz 配置区只含集群下拉（无图谱滤镜/分析模式）----
const sel = page.locator('.industry-catalog-select').first();
await sel.click({ timeout: 8000 });
await page.waitForTimeout(800);
await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
await page.waitForTimeout(1500);
out.cluster_echo = (((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '')).trim();
out.sz_url_after_pick = page.url();
out.sz_has_graph_config = await page.locator('main .arco-radio').count().catch(() => 0); // sz 应无分析模式单选（与 graph 差异点）
out.sz_has_filter = /图谱滤镜/.test(((await page.locator('main').first().innerText().catch(() => '')) || '')); // sz 应无图谱滤镜

// ---- 安装拦截：仅 POST 且 URL 尾段恰为 /analysis/tasks（?参数允许；/tasks/list 不匹配）----
const GLOB = '**/topicAsync/topic/v1/analysis/tasks*';
let abortedCount = 0;
await ctx.route(GLOB, (route) => {
  const req = route.request();
  const u = req.url();
  const tailOk = /\/topicAsync\/topic\/v1\/analysis\/tasks\/?(\?|$)/.test(u);
  if (req.method() === 'POST' && tailOk) {
    abortedCount++;
    return route.abort('connectionreset'); // 断链语义（用例前置「断开分析服务（断链）」）
  }
  return route.continue();
});

// ---- 点「开始分析」（应 POST 被拒）----
const start = page.getByRole('button', { name: '开始分析', exact: true });
out.start_enabled_before = await start.first().isEnabled().catch(() => null);
await start.first().click({ timeout: 8000 });
out.url_after_abort_click = page.url();
await page.waitForTimeout(5000); // 等 alert / toast 渲染

// ---- 采集失败态形态 ----
out.aborted_posts = abortedCount;
out.url_failed_state = page.url();
out.toast_text = ((await page.locator('.arco-message, .arco-message-list, .arco-notification').allInnerTexts().catch(() => [])) || []).join(' | ').trim();
const mainText = ((await page.locator('main').first().innerText().catch(() => '')) || '');
out.main_text_head = mainText.slice(0, 600);
out.error_like_nodes = await page.evaluate(() => {
  const sels = ['.arco-result', '[class*="error" i]', '[class*="fail" i]', '.arco-alert', '[class*="retry" i]', '[class*="empty" i]'];
  const hits = [];
  for (const s of sels) {
    document.querySelectorAll(s).forEach((e) => {
      const t = (e.innerText || '').trim().slice(0, 120);
      const vis = !!(e.offsetWidth || e.offsetHeight);
      if (t) hits.push({ sel: s, text: t, visible: vis });
    });
  }
  return hits.slice(0, 20);
});
out.retry_word_hits = [/重试/, /失败/, /异常/, /错误/, /稍后再试/, /网络/].filter((re) => re.test(mainText)).map((re) => re.source);
// 页面壳与配置保留（sz 差异点：壳=页头双 Tab + 配置区只含集群下拉，无图谱滤镜/分析模式）
const tabNames = [];
{
  const tabs = page.locator('[role=tab]');
  const n = await tabs.count();
  for (let i = 0; i < n; i++) tabNames.push((((await tabs.nth(i).innerText().catch(() => '')) || '')).trim());
}
out.shell_kept = {
  title: await page.title(),
  tabs: tabNames,
  config_heading: mainText.includes('分析配置'),
  cluster_echo_after: out.cluster_echo,
  select_present: !!(await page.locator('.industry-catalog-select').first().count()),
  no_leak_task_state: !/分析结果已生成|生成中/.test(mainText),
};
out.start_button_after_abort = {
  count: await start.first().count(),
  enabled: await start.first().isEnabled().catch(() => null),
};
await page.screenshot({ path: path.join(__dirname, 'probe-p020-failed-state.png') });

// ---- unroute 恢复 → 点「开始分析」验证重试路径 ----
await ctx.unroute(GLOB);
await page.waitForTimeout(500);
await start.first().click({ timeout: 8000 });
let retryUrl = page.url();
let retryTaskId = null;
for (let i = 0; i < 15; i++) {
  await page.waitForTimeout(1000);
  retryUrl = page.url();
  const m = /[?&]task_id=(SVC-\d{8}-\d{1,4})/.exec(retryUrl);
  if (m && /view=/.test(retryUrl)) { retryTaskId = m[1]; break; }
}
out.retry = {
  url: retryUrl,
  task_id: retryTaskId,
  landed_processing_or_result: /view=processing|view=result/.test(retryUrl),
  analysis_fp_shenzhen_prefix: /analysis_fp=svc\|shenzhen\|/.test(retryUrl),
  aborted_after_unroute: abortedCount - 1, // 应 0（污染检查）
};
out.retry_main_head = (((await page.locator('main').first().innerText().catch(() => '')) || '')).slice(0, 400);
// 失败态 alert 清除检查
out.alert_cleared_after_retry = (await page.locator('.arco-alert').filter({ hasText: /Network Error/ }).count().catch(() => 0)) === 0;
await page.screenshot({ path: path.join(__dirname, 'probe-p020-after-retry.png') });

// ---- 轮询/详情 GET 形态采集（污染核查）----
out.topicasync_requests_seen = reqLog.slice(0, 40);

fs.writeFileSync(path.join(__dirname, '_probe-p020.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
