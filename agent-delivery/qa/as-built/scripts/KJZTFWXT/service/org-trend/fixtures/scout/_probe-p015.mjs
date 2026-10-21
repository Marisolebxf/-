/**
 * 一次性无头探针（P0-15 写稿用）：分析失败局部错误与重试（FUNC-00670）。
 * 口径对齐 sz P0-20 / graph P0-29：route.abort 拦截创建任务 POST，
 * 观察失败态 .arco-alert / 页面壳 / 机构回显 / 「开始分析」重试承载 / unroute 后落 processing。
 * 产物落 scout-p015-fail.json；勿当 runner。禁止有头浏览器。
 */
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
// 已知机构 id（scout-p010 / scout-after-start）；search/orgs 空名单时用深链回填配置态，绕过弹窗
const KNOWN_ORG = '79bbcfc0e68027808f1f4caf1b6f0469';
const ROUTE_CONFIG =
  '/service/institution-judgment?workspace=trend&tab=trend&industry=INB1701&org_ids[]=' + KNOWN_ORG;
const out = {
  probed_at: new Date().toISOString(),
  entry: 'svc-org-trend',
  case: 'P0-15 / FUNC-00670',
  path: 'abort POST create-task (trend config deeplink + org_ids)',
};

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await ctx.newPage();

const reqLog = [];
page.on('request', (r) => {
  const u = r.url();
  if (/topicAsync/.test(u)) reqLog.push(r.method() + ' ' + u.replace(BASE, ''));
});

try {
  await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 60000 });
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

  // 深链配置态：产业+已知机构（search/orgs 空名单时弹窗不可用；org_ids 回填仍可点开始分析）
  await page.goto(BASE + ROUTE_CONFIG, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2500);
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if (
    (await close.count()) &&
    (await close.first().isVisible().catch(() => false)) &&
    (await close.first().isEnabled().catch(() => false))
  ) {
    await close.first().click({ timeout: 1500 }).catch(() => {});
    await page.waitForTimeout(300);
  }
  // 若深链落到 processing/result，回配置（保留 org_ids）
  if (/view=processing|view=result/.test(page.url())) {
    await page.goto(BASE + ROUTE_CONFIG, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2000);
  }
  const mainAfterPick = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  out.org_echo = (/已选机构（[1-9]\d*\s*家）/.exec(mainAfterPick) || [''])[0];
  out.url_after_org = page.url();
  out.industry_echo = (
    (await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || ''
  ).trim();
  out.precondition = {
    known_org: KNOWN_ORG,
    org_echo_ok: /已选机构（[1-9]/.test(mainAfterPick),
    start_visible: await page.getByRole('button', { name: '开始分析', exact: true }).first().isVisible().catch(() => false),
    main_head: mainAfterPick.replace(/\s+/g, ' ').slice(0, 240),
  };
  if (!out.precondition.org_echo_ok) {
    throw new Error('深链 org_ids 未回显已选机构: ' + out.precondition.main_head);
  }

  // route.abort 断链
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
  const mainText = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  out.main_text_head = mainText.slice(0, 800);
  out.toast_text = (
    (await page.locator('.arco-message, .arco-message-list, .arco-notification').allInnerTexts().catch(() => [])) || []
  )
    .join(' | ')
    .trim();

  const alerts = page.locator('.arco-alert');
  const alertTexts = [];
  for (let i = 0; i < Math.min(8, await alerts.count()); i++) {
    alertTexts.push(
      (((await alerts.nth(i).innerText().catch(() => '')) || '')).replace(/\s+/g, ' ').trim().slice(0, 160),
    );
  }
  out.alert_texts = alertTexts;
  out.error_alert_visible = await page
    .locator('.arco-alert')
    .filter({ hasText: /Network Error|失败|异常|错误/ })
    .first()
    .isVisible()
    .catch(() => false);
  out.retry_word_hits = [/重试/, /失败/, /异常/, /错误/, /Network Error/, /稍后再试/]
    .filter((re) => re.test(mainText))
    .map((re) => re.source);

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
    org_echo_kept: /已选机构（[1-9]/.test(mainText),
    industry_select: !!(await page.locator('.industry-catalog-select').first().count()),
    no_leak_task_state: !/分析结果已生成|生成中/.test(mainText),
    workspace_trend: /workspace=trend/.test(page.url()),
    no_view_drift: !/view=processing|view=result/.test(page.url()),
  };
  out.start_button_after_abort = {
    count: await start.count(),
    enabled: await start.first().isEnabled().catch(() => null),
    visible: await start.first().isVisible().catch(() => false),
  };

  await page.screenshot({ path: path.join(__dirname, 'probe-p015-failed-state.png'), fullPage: false });

  // unroute + 重试
  await ctx.unroute(GLOB);
  abortedCount = 0;
  await page.waitForTimeout(800);
  out.start_enabled_before_retry = await start.first().isEnabled().catch(() => null);
  await start.first().click({ timeout: 8000 });
  let retryUrl = page.url();
  let retryTask = null;
  let landed = false;
  for (let i = 0; i < 15; i++) {
    await page.waitForTimeout(1000);
    retryUrl = page.url();
    if (/view=processing|view=result/.test(retryUrl)) {
      const m = /[?&]task_id=(SVC-\d{8}-\d{1,4})/.exec(retryUrl);
      if (m) retryTask = m[1];
      landed = true;
      break;
    }
  }
  out.retry = {
    landed,
    url: retryUrl,
    task_id: retryTask,
    aborted_after_unroute: abortedCount,
    analysis_fp_trend: /analysis_fp=svc\|trend\|/.test(retryUrl),
    org_ids_in_url: /org_ids/.test(retryUrl),
  };
  await page.screenshot({ path: path.join(__dirname, 'probe-p015-after-retry.png'), fullPage: false });

  // 等引导/结果并看 alert 清除
  let body = '';
  let url = page.url();
  for (let i = 0; i < 20; i++) {
    await page.waitForTimeout(2000);
    body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    url = page.url();
    if (/分析结果已生成/.test(body) || /view=result/.test(url)) break;
  }
  out.after_retry_settle = {
    url,
    done: /分析结果已生成/.test(body) || /view=result/.test(url),
    network_error_alert: await page
      .locator('.arco-alert')
      .filter({ hasText: /Network Error/ })
      .count()
      .catch(() => 0),
    body_head: body.slice(0, 300),
  };

  out.req_log_tail = reqLog.slice(-20);
  out.conclusion =
    out.aborted_posts >= 1 && out.error_alert_visible && out.shell_kept.org_echo_kept && out.retry.landed
      ? '分支①全链可断言：断链失败态可复现 + 壳/机构保留 + 开始分析即重试 + unroute 落 processing'
      : '需复核：断链/alert/壳/重试有缺口——见各字段';
} catch (e) {
  out.error = String(e && e.stack ? e.stack : e).slice(0, 800);
  try {
    await page.screenshot({ path: path.join(__dirname, 'probe-p015-error.png'), fullPage: false });
  } catch {}
} finally {
  fs.writeFileSync(path.join(__dirname, 'scout-p015-fail.json'), JSON.stringify(out, null, 2));
  await browser.close();
  console.log(
    JSON.stringify(
      {
        ok: !out.error,
        aborted: out.aborted_posts,
        alert: out.error_alert_visible,
        shell: out.shell_kept,
        start_after: out.start_button_after_abort,
        retry: out.retry,
        settle: out.after_retry_settle,
        conclusion: out.conclusion || out.error,
      },
      null,
      2,
    ),
  );
}
