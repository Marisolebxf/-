// _probe-p021.mjs — P0-21 前探针（探针公约：独立无头，一次性；写前实证现场行为）
// 目的：FUNC-01302 备选-评审模式零泄漏——sz 工作区评审开关机制与三追溯按钮形态：
//   ① 评审模式开关机制：真源=localStorage.ent_review_mode（新 context 默认 "true"）；
//      persona 菜单 → aria-label="内部评审模式" switch 为 UI 承载（P3 路径，探针实证可操作）
//   ② 开启态三追溯按钮（用例指定：深圳服务链现状分析/横向对比分析/分析配置）可见可点、
//      点击后弹层可见且锚点命中（REQ-SVC-ECO-FRAMEWORK / REQ-SVC-ECO-COMPARE 执行时记录；
//      分析配置挂点锚=US-SVC-ECO-05 无 REQ- 前缀——_probe-p021-pop4.json 实证）
//   ③ 关闭+刷新后零泄漏基线（trace-info-icon / [data-review-metric] / .metric-spec-card / 文本字样）
//   ④ 业务态锚：选定集群回显 + URL industry= + 分析记录行数，关评审前后不变
//   ⑤ 全程任务创建 POST 计数（应 0——纯开关往返 + 只读路径）
// 弹层收场（_probe-p021-pop2/pop3/pop4 实证）：Esc 不收、再点同一按钮不 toggle、goto/reload 不清——
//   唯一可靠收场=body 空白点击（mouse.click(960,540) 后弹层 visible=0 且 select 解锁）。
// 铁律：结束时还原评审初始态（防污染后续依赖评审开的条目）；失败落盘后继续，不卡死。
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://111.198.38.90:50892';
const ROUTE = '/service/chain-analysis?workspace=shenzhen&tab=shenzhen';
const out = { probed_at: new Date().toISOString(), entry: 'svc-sz', case: 'P0-21 / FUNC-01302', path: 'review-mode zero-leak (shenzhen workspace)' };

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await ctx.newPage();

let posts = 0;
page.on('request', (r) => {
  if (r.method() === 'POST' && /\/topicAsync\/topic\/v1\/analysis\/tasks\/?(\?|$)/.test(r.url())) posts++;
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
const closeBasket = async () => {
  const c = page.locator('button[aria-label="关闭对比篮"]');
  if (await c.count() && await c.first().isVisible().catch(() => false)) { try { await c.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {} }
};
const dismissPop = async () => { await page.mouse.click(960, 540).catch(() => {}); await page.waitForTimeout(500); };
await closeBasket();

// ---- ① 评审开关机制采集（localStorage 真源 + 菜单 UI 路径）----
out.review_ls_initial = await page.evaluate(() => localStorage.getItem('ent_review_mode'));
const readSwitch = async () => {
  const sw = page.locator('button[role=switch][aria-label="内部评审模式"], [aria-label="内部评审模式"]').first();
  const exists = (await sw.count()) > 0;
  let checked = await sw.getAttribute('aria-checked').catch(() => null);
  if (checked === null && exists) {
    const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]');
    checked = /arco-switch-checked/.test((await holder.first().getAttribute('class').catch(() => '')) || '') ? 'true' : 'false';
  }
  return { exists, checked };
};
const setReview = async (want) => {
  let opener = page.locator('.persona-switch').first();
  if (!(await opener.isVisible().catch(() => false))) opener = page.locator('[class*="persona" i]').first();
  await opener.click({ timeout: 5000 });
  await page.waitForTimeout(800);
  const st = await readSwitch();
  if (st.checked !== want) {
    const sw = page.locator('button[role=switch][aria-label="内部评审模式"], [aria-label="内部评审模式"]').first();
    await sw.click({ timeout: 5000 });
    await page.waitForTimeout(1200);
  }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(600);
  return {
    switch: (await readSwitch()).checked,
    ls: await page.evaluate(() => localStorage.getItem('ent_review_mode')),
  };
};

// ---- ② 确保评审开启态 → 三追溯按钮形态 ----
const traceCount = async () => await page.locator('button.trace-info-icon').count();
let n = await traceCount();
if (n < 3) { out.review_set_on = await setReview('true'); await page.waitForTimeout(800); n = await traceCount(); }
out.trace_count_review_on = n;
out.trace_labels_review_on = await page.locator('button.trace-info-icon').evaluateAll((els) =>
  els.map((e) => e.getAttribute('aria-label') || '(no-aria-label)')
);
out.trace_mounts = await page.locator('button.trace-info-icon').evaluateAll((els) =>
  els.map((e) => {
    let p = e.parentElement; let mount = null;
    while (p && p !== document.body) {
      if (p.getAttribute && p.getAttribute('data-testid')) { mount = p.getAttribute('data-testid'); break; }
      p = p.parentElement;
    }
    return { label: e.getAttribute('aria-label') || '', mount: mount };
  })
);

// 逐一点开三枚用例指定按钮：可见可点 + 弹层锚点；收场=body 空白点击（pop3 实证 Esc 不收）
const WANTED = ['深圳服务链现状分析', '横向对比分析', '分析配置'];
out.popovers = [];
for (const key of WANTED) {
  const b = page.locator(`button.trace-info-icon[aria-label*="${key}"]`).first();
  const cnt = await page.locator(`button.trace-info-icon[aria-label*="${key}"]`).count();
  const rec = { key: key, count: cnt };
  if (cnt > 0) {
    rec.visible = await b.isVisible().catch(() => false);
    rec.enabled = await b.isEnabled().catch(() => false);
    try {
      await b.click({ timeout: 5000 });
      await page.waitForTimeout(1500);
      const t = await page.evaluate(() => {
        const vis = Array.from(document.querySelectorAll('.arco-trigger-popup, .arco-popover')).filter((e) => !!(e.offsetWidth || e.offsetHeight));
        return vis[0] ? (vis[0].innerText || '').replace(/\s+/g, ' ') : '';
      });
      rec.pop_head = t.slice(0, 160);
      rec.anchor_framework = /REQ-SVC-ECO-FRAMEWORK/.test(t);
      rec.anchor_compare = /REQ-SVC-ECO-COMPARE/.test(t);
      rec.anchor_us05 = /US-SVC-ECO-05/.test(t);
      await dismissPop();
      rec.pop_closed_after_bodyclick = (await page.evaluate(() =>
        Array.from(document.querySelectorAll('.arco-trigger-popup, .arco-popover')).filter((e) => !!(e.offsetWidth || e.offsetHeight)).length
      )) === 0;
    } catch (e) {
      rec.click_error = String(e).slice(0, 160);
    }
  }
  out.popovers.push(rec);
}
await page.screenshot({ path: path.join(__dirname, 'probe-p021-review-on.png') });

// ---- ④ 业务态锚（开评审态）：选集群 + 记录 Tab 行数 ----
const sel = page.locator('.industry-catalog-select').first();
await sel.click({ timeout: 8000 });
await page.waitForTimeout(800);
await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
await page.waitForTimeout(1500);
out.cluster_echo_on = (((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '')).trim();
out.url_after_pick = page.url();

const recTab = page.locator('[role=tab][data-tab-key="records"]').or(page.getByRole('tab', { name: '分析记录', exact: true }));
await recTab.first().click({ timeout: 8000 });
await page.waitForTimeout(2000);
out.records_url_on = page.url();
out.records_rows_on = await page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /SVC-\d{8}-\d+/ }).count();
const mainTab = page.locator('[role=tab][data-tab-key="shenzhen"]').or(page.getByRole('tab', { name: /深圳服务链现状分析/ }));
await mainTab.first().click({ timeout: 8000 });
await page.waitForTimeout(1800);

// ---- ③ 关评审 + reload → 零泄漏 + 业务态不变 ----
out.review_set_off = await setReview('false');
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);
await closeBasket();
await dismissPop(); // reload 后弹层可能重开（pop4 实证评审开态下点开过会重开；关态按钮已卸载无弹层，兜底无害）
out.trace_count_review_off = await traceCount();
out.dom_leak_off = {
  data_review_metric: await page.locator('[data-review-metric]').count(),
  metric_spec_card: await page.locator('.metric-spec-card').count(),
};
const mainOff = ((await page.locator('main').first().innerText().catch(() => '')) || '');
out.main_leaks_off = ['需求追溯', '评审', 'Q-', 'GAP-', 'metric_id'].filter((k) => mainOff.includes(k));
out.main_head_off = mainOff.replace(/\s+/g, ' ').slice(0, 400);
out.cluster_echo_off = (((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '')).trim();
out.url_off_main = page.url();
out.config_kept_off = ['深圳服务链现状分析', '分析配置', '开始分析'].every((k) => mainOff.includes(k));
await page.screenshot({ path: path.join(__dirname, 'probe-p021-review-off.png') });

// 步骤④：切「分析记录」Tab（关评审态复查零泄漏 + 行数不变）
await recTab.first().click({ timeout: 8000 });
await page.waitForTimeout(2000);
out.records_url_off = page.url();
out.records_rows_off = await page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /SVC-\d{8}-\d+/ }).count();
const recMain = ((await page.locator('main').first().innerText().catch(() => '')) || '');
out.records_main_leaks_off = ['需求追溯', '评审', 'Q-', 'GAP-', 'metric_id'].filter((k) => recMain.includes(k));
out.trace_count_records_off = await traceCount();
await page.screenshot({ path: path.join(__dirname, 'probe-p021-records-off.png') });

// ---- 全程 POST 计数 ----
out.create_task_posts_total = posts;

// ---- 还原评审初始态（防污染）----
if (out.review_ls_initial === 'true') {
  out.review_restored = await setReview('true');
} else {
  out.review_restored = 'initial-off-kept';
}

fs.writeFileSync(path.join(__dirname, '_probe-p021.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
