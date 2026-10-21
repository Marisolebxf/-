/**
 * 一次性无头探针（P0-15 写稿用）：分析失败局部错误与重试（FUNC-00655）。
 * 口径对齐 org-trend P0-15 / sz P0-20 / graph P0-29：route.abort 拦截创建任务 POST，
 * 观察失败态 .arco-alert / 页面壳 / 机构回显 / 领域筛选 / 「开始分析」重试承载 / unroute 后落 processing。
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
const KNOWN_ORG = '79bbcfc0e68027808f1f4caf1b6f0469';
const ROUTE_CONFIG =
  '/service/institution-judgment?workspace=field&tab=coverage&org_ids[]=' + KNOWN_ORG;
const out = {
  probed_at: new Date().toISOString(),
  entry: 'svc-org-field',
  case: 'P0-15 / FUNC-00655',
  path: 'abort POST create-task (field config deeplink + org_ids)',
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
  if (/view=processing|view=result/.test(page.url())) {
    await page.goto(BASE + ROUTE_CONFIG, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2000);
  }
  const mainAfterPick = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  out.org_echo = (/已选机构（[1-9]\d*\s*家）/.exec(mainAfterPick) || [''])[0];
  out.url_after_org = page.url();
  const filterInput = page.getByPlaceholder('筛选领域（不改分析指纹）');
  out.filter_visible = await filterInput.first().isVisible().catch(() => false);
  if (out.filter_visible) {
    await filterInput.first().fill('新一代');
    await page.waitForTimeout(400);
  }
  out.filter_value_before = out.filter_visible
    ? ((await filterInput.first().inputValue().catch(() => '')) || '')
    : null;
  out.precondition = {
    known_org: KNOWN_ORG,
    org_echo_ok: /已选机构（[1-9]/.test(mainAfterPick),
    start_visible: await page.getByRole('button', { name: '开始分析', exact: true }).first().isVisible().catch(() => false),
    filter_visible: out.filter_visible,
    main_head: mainAfterPick.replace(/\s+/g, ' ').slice(0, 240),
  };
  if (!out.precondition.org_echo_ok) {
    throw new Error('深链 org_ids 未回显已选机构: ' + out.precondition.main_head);
  }

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
  const filterValAfter = out.filter_visible
    ? ((await filterInput.first().inputValue().catch(() => '')) || '')
    : null;
  out.shell_kept = {
    title: await page.title(),
    tabs: tabNames,
    config_heading: mainText.includes('分析配置'),
    org_echo_kept: /已选机构（[1-9]/.test(mainText),
    filter_input: !!(await page.getByPlaceholder('筛选领域（不改分析指纹）').count()),
    industry_catalog: !!(await page.locator('.industry-catalog-select').first().count()),
    filter_value_kept: filterValAfter,
    no_leak_task_state: !/分析结果已生成|生成中/.test(mainText),
    workspace_field: /workspace=field/.test(page.url()),
    no_view_drift: !/view=processing|view=result/.test(page.url()),
  };
  out.start_button_after_abort = {
    count: await start.count(),
    enabled: await start.first().isEnabled().catch(() => null),
    visible: await start.first().isVisible().catch(() => false),
  };

  await page.screenshot({ path: path.join(__dirname, 'probe-p015-failed-state.png'), fullPage: false });

  await ctx.unroute(GLOB);
  abortedCount = 0;
  await page.waitForTimeout(800);
  out.start_enabled_before_retry = await start.first().isEnabled().catch(() => null);
  await start.first().click({ timeout: 8000 });
  let retryUrl = page.url();
  let retryTask = null;
  let landed = false;
  let createFail = false;
  let localErr = false;
  let silentConfig = false;
  let main = '';
  let alertHit = '';
  const createRe = /创建下游任务失败|create 失败|中间层 create|SVC 中间层/;
  const localRe = /失败|异常|错误|404/;
  for (let i = 0; i < 20; i++) {
    await page.waitForTimeout(1000);
    retryUrl = page.url();
    if (/view=processing|view=result/.test(retryUrl)) {
      const m = /[?&]task_id=(SVC-\d{8}-\d{1,4})/.exec(retryUrl);
      if (m) retryTask = m[1];
      landed = true;
      break;
    }
    main = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    const errAlert = page.locator('.arco-alert').filter({ hasText: /Network Error|失败|异常|错误|404|创建下游|create/ });
    alertHit = '';
    for (let j = 0; j < (await errAlert.count()); j++) {
      const t = ((await errAlert.nth(j).innerText().catch(() => '')) || '').trim();
      if (!t || /评审模式|对象集只调|分析条件已就绪/.test(t)) continue;
      alertHit = t;
      break;
    }
    if (createRe.test(main) || createRe.test(alertHit) || (/404/.test(main) && /create|创建|下游|中间层/i.test(main))) {
      createFail = true;
      break;
    }
    if (localRe.test(alertHit) || /404/.test(alertHit)) {
      localErr = true;
      break;
    }
  }
  if (!landed && !createFail && !localErr) {
    retryUrl = page.url();
    main = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    const netStill = await page.locator('.arco-alert').filter({ hasText: /Network Error/ }).first().isVisible().catch(() => false);
    if (
      !netStill &&
      /分析条件已就绪/.test(main) &&
      /已选机构（[1-9]/.test(main) &&
      main.includes('分析配置') &&
      (await page.getByPlaceholder('筛选领域（不改分析指纹）').count()) > 0 &&
      !/view=processing|view=result/.test(retryUrl)
    ) {
      silentConfig = true;
    }
  }
  out.retry = {
    landed,
    createFail,
    localErr,
    silentConfig,
    branch: landed
      ? 'processing'
      : createFail
        ? 'create_404'
        : localErr
          ? 'local_error'
          : silentConfig
            ? 'silent_config'
            : 'none',
    url: retryUrl,
    task_id: retryTask,
    aborted_after_unroute: abortedCount,
    analysis_fp_field: /analysis_fp=svc\|field\|/.test(retryUrl),
    org_ids_in_url: /org_ids/.test(retryUrl),
    alert_hit: String(alertHit || '').replace(/\s+/g, ' ').slice(0, 160),
  };
  await page.screenshot({ path: path.join(__dirname, 'probe-p015-after-retry.png'), fullPage: false });

  let body = '';
  let url = page.url();
  if (landed) {
    for (let i = 0; i < 20; i++) {
      await page.waitForTimeout(2000);
      body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
      url = page.url();
      if (/分析结果已生成/.test(body) || /view=result/.test(url)) break;
    }
  } else {
    body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    url = page.url();
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
    out.aborted_posts >= 1 &&
    out.error_alert_visible &&
    out.shell_kept.org_echo_kept &&
    (out.retry.landed || out.retry.createFail || out.retry.localErr || out.retry.silentConfig)
      ? '分支①可断言：断链失败态可复现 + 壳/机构/筛选保留 + 开始分析即重试 + unroute 四分支其一'
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
