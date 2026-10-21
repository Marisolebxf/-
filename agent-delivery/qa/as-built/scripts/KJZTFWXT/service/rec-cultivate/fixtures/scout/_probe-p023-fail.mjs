// _probe-p023-fail.mjs — P0-23 / FUNC-01282 写前探针（独立无头，一次性）
// 口径对齐 sz P0-20 / graph P0-29 / chain-shortboard P0-17：
//   route.abort 拦截创建任务 POST（精确尾段，不误伤 list/running）
//   观察失败态 .arco-alert / 壳保留 / 「开始分析」重试承载 / unroute 后重试落点
// 铁律：结束必须 unroute；失败落盘后继续不卡死。
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
const ROUTE = '/service/institution-decision?workspace=cultivate&tab=cultivate';
const out = {
  probed_at: new Date().toISOString(),
  entry: 'svc-rec-cultivate',
  case: 'P0-23 / FUNC-01282',
  path: 'abort POST create-task (cultivate workspace)',
};

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await ctx.newPage();

const reqLog = [];
page.on('request', (r) => {
  const u = r.url();
  if (/topicAsync/.test(u)) reqLog.push(r.method() + ' ' + u.replace(BASE, ''));
});

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
if (await close.count() && await close.first().isVisible().catch(() => false)) {
  await close.first().click({ timeout: 1500 }).catch(() => {});
  await page.waitForTimeout(300);
}

const sel = page.locator('.industry-catalog-select').first();
await sel.click({ timeout: 8000 });
await page.waitForTimeout(800);
await page
  .locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
  .filter({ hasText: '新一代信息技术' })
  .first()
  .click({ timeout: 8000 });
await page.waitForTimeout(1500);
out.cluster_echo = (((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '')).trim();
out.url_after_pick = page.url();

const GLOB = '**/topicAsync/topic/v1/analysis/tasks*';
let abortedCount = 0;
await ctx.route(GLOB, (route) => {
  const req = route.request();
  const u = req.url();
  const tailOk = /\/topicAsync\/topic\/v1\/analysis\/tasks\/?(\?|$)/.test(u);
  if (req.method() === 'POST' && tailOk) {
    abortedCount++;
    return route.abort('connectionreset');
  }
  return route.continue();
});

const start = page.getByRole('button', { name: '开始分析', exact: true });
out.start_enabled_before = await start.first().isEnabled().catch(() => null);
await start.first().click({ timeout: 8000 });
await page.waitForTimeout(5000);

out.aborted_posts = abortedCount;
out.url_failed_state = page.url();
out.toast_text = ((await page.locator('.arco-message, .arco-message-list, .arco-notification').allInnerTexts().catch(() => [])) || [])
  .join(' | ')
  .trim();
const mainText = ((await page.locator('main').first().innerText().catch(() => '')) || '');
out.main_text_head = mainText.slice(0, 700).split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 28);

const alertLoc = page.locator('.arco-alert').filter({ hasText: /Network Error|失败|异常|错误/ });
out.error_alert_count = await alertLoc.count().catch(() => 0);
out.error_alert_visible = out.error_alert_count > 0 && (await alertLoc.first().isVisible().catch(() => false));
out.error_alert_text = out.error_alert_count
  ? ((await alertLoc.first().innerText().catch(() => '')) || '').trim().slice(0, 240)
  : '';

out.shell_kept = {
  title_ok: /培育服务机构推荐分析/.test(await page.title()),
  has_config: /分析配置/.test(mainText),
  has_start: /开始分析/.test(mainText),
  has_model: /培育评估模型/.test(mainText),
  tab_main: await page.locator('[role=tab][data-tab-key="cultivate"]').count(),
  tab_records: await page.locator('[role=tab][data-tab-key="records"]').count(),
  echo: (((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '')).trim(),
  url_stayed_config: !/view=processing|view=result/.test(page.url()),
  no_success_leak: !/分析结果已生成|生成中/.test(mainText),
};

out.retry_word_hits = (mainText.match(/重试/g) || []).length;
out.start_button_after_abort = {
  count: await start.count(),
  enabled: await start.first().isEnabled().catch(() => null),
  visible: await start.first().isVisible().catch(() => null),
};

await page.screenshot({ path: path.join(__dirname, 'probe-p023-failed-state.png') }).catch(() => {});

await ctx.unroute(GLOB);
abortedCount = 0;
await page.waitForTimeout(800);
out.req_log_before_retry = reqLog.slice(-12);

await start.first().click({ timeout: 8000 });
let retryUrl = page.url();
let retryTask = null;
let landed = false;
let create404 = false;
let silentConfig = false;
let localErrAgain = false;
for (let i = 0; i < 20; i++) {
  await page.waitForTimeout(1000);
  retryUrl = page.url();
  const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  const toast = ((await page.locator('.arco-message, .arco-message-list, .arco-notification').allInnerTexts().catch(() => [])) || []).join('|');
  if (/view=processing|view=result/.test(retryUrl)) {
    const m = /[?&]task_id=(SVC-\d{8}-\d{1,4})/.exec(retryUrl);
    if (m) retryTask = m[1];
    landed = true;
    break;
  }
  if (/创建下游任务失败|中间层 create 失败|404/.test(body + toast)) {
    create404 = true;
    break;
  }
  if (await page.locator('.arco-alert').filter({ hasText: /Network Error|失败|异常|错误/ }).first().isVisible().catch(() => false)) {
    localErrAgain = true;
    break;
  }
  if (i >= 8 && /分析配置/.test(body) && !/view=/.test(retryUrl) && /开始分析/.test(body)) {
    silentConfig = true;
  }
}
out.retry = {
  landed,
  create404,
  localErrAgain,
  silentConfig,
  aborted_after_unroute: abortedCount,
  retry_url: retryUrl,
  retry_task: retryTask,
  body_head: ((await page.locator('main').first().innerText().catch(() => '')) || '')
    .split('\n')
    .map((s) => s.trim())
    .filter(Boolean)
    .slice(0, 20),
};
await page.screenshot({ path: path.join(__dirname, 'probe-p023-after-retry.png') }).catch(() => {});

out.req_log_tail = reqLog.slice(-16);
out.conclusion =
  out.aborted_posts >= 1 && out.error_alert_visible && out.shell_kept.url_stayed_config
    ? 'branch1-abort-ok'
    : 'abort-or-ui-gap';

fs.writeFileSync(path.join(__dirname, 'scout-p023-fail.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify({ conclusion: out.conclusion, aborted: out.aborted_posts, alert: out.error_alert_visible, retry: out.retry }, null, 2));
await browser.close();
