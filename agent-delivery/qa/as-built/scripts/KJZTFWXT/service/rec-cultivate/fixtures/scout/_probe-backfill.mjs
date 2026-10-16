#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-rec-cultivate 脚本补齐波（P0-06~P0-23 写稿前实勘）。
 * 探测：Tag/checkbox 结构、产业清空、权重步进、起任务/单飞/当天复用、结果态名单列、
 *       评审开关零泄漏、attract 隔离、route.abort 失败态可行性。
 * 公约：独立 headless；产物落本目录；禁止硬点 disabled；结束恢复评审开启态。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const route = '/service/institution-decision?workspace=cultivate&tab=cultivate';
const target = baseUrl.replace(/\/?$/, '') + route;
const out = {};
const dump = (name) => fs.writeFileSync(path.join(__dirname, name), JSON.stringify(out[name] ?? out, null, 2));
const main = async (page) => (await page.locator('main').first().innerText().catch(() => '')) || '';

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
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
await ensureLogin(page);
await page.goto(target, { waitUntil: 'domcontentloaded' });
await ensureLogin(page);
await page.waitForTimeout(2500);
await closeBasket(page);

// ---------- 1. 机构类型 / 服务环节 DOM 结构 ----------
try {
  const cfgText = await main(page);
  const sect = page.locator('main').first();
  // 机构类型：找「机构类型」标签之后的控件群
  const checkboxes = sect.locator('.arco-checkbox');
  const cbInfo = [];
  for (let i = 0; i < Math.min(await checkboxes.count(), 8); i++) {
    const c = checkboxes.nth(i);
    cbInfo.push({
      label: (await c.innerText().catch(() => '')).trim().replace(/\s+/g, ' '),
      checked: await c.locator('input').isChecked().catch(() => null),
      visible: await c.isVisible().catch(() => false),
    });
  }
  const multSel = sect.locator('.arco-select-view-mult');
  const multInfo = [];
  for (let i = 0; i < await multSel.count(); i++) {
    const m = multSel.nth(i);
    multInfo.push({
      text: (await m.innerText().catch(() => '')).trim().replace(/\s+/g, ' ').slice(0, 200),
      tagCount: await m.locator('.arco-tag').count(),
      closeBtnCount: await m.locator('.arco-tag-close-btn').count(),
    });
  }
  // 展开服务环节多选看选项与分组
  await multSel.first().click({ timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(800);
  const popup = page.locator('.arco-trigger-popup:visible');
  const popupText = (await popup.first().innerText().catch(() => '')) || '';
  const optCount = await popup.locator('.arco-select-option').count();
  const groupTitles = await popup.locator('.arco-select-group-title, [class*=group-title]').allTextContents().catch(() => []);
  await page.keyboard.press('Escape');
  out.tag_structure = { checkboxes: cbInfo, multiselects: multInfo, popup_snippet: popupText.split('\n').slice(0, 30), option_count: optCount, group_titles: groupTitles };
} catch (e) { out.tag_structure = { err: String(e).slice(0, 200) }; }
dump('scout-tags.json');
await page.goto(target, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1800);
await closeBasket(page);

// ---------- 2. 产业选定回显 / 清空 / Tab 切换保留 ----------
try {
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 5000 });
  await page.waitForTimeout(600);
  await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 5000 });
  await page.waitForTimeout(800);
  const echo1 = (await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')).trim();
  // 改选
  await sel.click({ timeout: 5000 });
  await page.waitForTimeout(600);
  await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '新能源' }).first().click({ timeout: 5000 });
  await page.waitForTimeout(800);
  const echo2 = (await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')).trim();
  // 清空（hover 出 clear）
  await sel.hover();
  await page.waitForTimeout(300);
  const clr = sel.locator('.arco-select-view-clear-btn, .arco-select-clear-icon, [class*=clear]');
  const clrCount = await clr.count();
  let echo3 = null;
  if (clrCount) {
    await clr.first().click({ force: true, timeout: 3000 }).catch(() => {});
    await page.waitForTimeout(800);
    echo3 = (await sel.innerText().catch(() => '')).trim().replace(/\s+/g, ' ');
  }
  // 重选 + 切 Tab 返回保留
  await sel.click({ timeout: 5000 });
  await page.waitForTimeout(600);
  await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 5000 });
  await page.waitForTimeout(800);
  const rec = page.locator('[role=tab][data-tab-key="records"]');
  await rec.first().click({ timeout: 5000 });
  await page.waitForTimeout(1200);
  const recText = (await main(page)).slice(0, 400);
  const back = page.locator('[role=tab][data-tab-key="cultivate"]');
  await back.first().click({ timeout: 5000 });
  await page.waitForTimeout(1200);
  const echo4 = (await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')).trim();
  const w1 = await page.locator('[aria-label="现有规模权重"] [role=spinbutton]').first().inputValue().catch(() => null);
  out.industry_echo = { echo1, echo2, clear_btn_count: clrCount, echo_after_clear: echo3, echo_after_tab_roundtrip: echo4, weight_after_roundtrip: w1, records_snippet: recText.split('\n').slice(0, 12) };
} catch (e) { out.industry_echo = { err: String(e).slice(0, 200) }; }
dump('scout-industry-echo.json');

// ---------- 3. 权重步进钮 ----------
try {
  const spin = page.locator('[aria-label="现有规模权重"] [role=spinbutton]').first();
  const before = await spin.inputValue();
  const wrap = page.locator('[aria-label="现有规模权重"]').first();
  const ups = wrap.locator('.arco-input-number-step-button');
  const n = await ups.count();
  // Arco: 第一个是 down 还是 up？点第一个看变化
  await ups.first().click({ timeout: 3000 });
  await page.waitForTimeout(500);
  const afterBtn1 = await spin.inputValue();
  let afterBtn2 = afterBtn1;
  if (n > 1) { await ups.nth(1).click({ timeout: 3000 }); await page.waitForTimeout(500); afterBtn2 = await spin.inputValue(); }
  out.weight_step = { before, step_button_count: n, after_first_btn: afterBtn1, after_second_btn: afterBtn2 };
  // 复位
  await page.getByRole('button', { name: '恢复默认权重', exact: true }).click({ timeout: 4000 });
  await page.waitForTimeout(600);
} catch (e) { out.weight_step = { err: String(e).slice(0, 200) }; }
dump('scout-weight-step.json');

// ---------- 4. 起任务 / 单飞 / 记录出现 ----------
try {
  // 先数记录条数
  const rec = page.locator('[role=tab][data-tab-key="records"]');
  await rec.first().click({ timeout: 5000 });
  await page.waitForTimeout(1200);
  const rowsBefore = await page.locator('main tr, main [role="row"]').count();
  const back = page.locator('[role=tab][data-tab-key="cultivate"]');
  await back.first().click({ timeout: 5000 });
  await page.waitForTimeout(1200);
  // 开始分析
  const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
  await start.click({ timeout: 5000 });
  await page.waitForTimeout(1500);
  const url1 = page.url();
  const body1 = (await main(page)).slice(0, 600);
  // 立刻再点一次（若按钮仍在）——单飞探测
  let secondClick = 'no-button';
  const start2 = page.getByRole('button', { name: '开始分析', exact: true }).first();
  if (await start2.count()) {
    const vis = await start2.isVisible().catch(() => false);
    if (vis) { await start2.click({ timeout: 3000 }).catch(() => {}); await page.waitForTimeout(1500); secondClick = 'clicked'; }
    else secondClick = 'button-hidden';
  }
  const url2 = page.url();
  const body2 = (await main(page)).slice(0, 600);
  // 等完成
  await page.waitForTimeout(4000);
  const body3 = (await main(page)).slice(0, 600);
  // 数记录
  await page.locator('[role=tab][data-tab-key="records"]').first().click({ timeout: 5000 });
  await page.waitForTimeout(1500);
  const rowsAfter = await page.locator('main tr, main [role="row"]').count();
  const recRows = (await main(page)).slice(0, 800);
  out.start_task = { rows_before: rowsBefore, url_after_start: url1, body_after_start: body1.split('\n').slice(0, 20), second_click: secondClick, url_after_second: url2, body_after_wait: body3.split('\n').slice(0, 20), rows_after: rowsAfter, records_after: recRows.split('\n').slice(0, 20) };
} catch (e) { out.start_task = { err: String(e).slice(0, 200) }; }
dump('scout-start-task.json');

// ---------- 5. 查看结果 → 结果态名单结构 ----------
try {
  const row = page.locator('main tr, main [role="row"]').filter({ hasText: /cultivate/ }).filter({ hasText: /已完成/ }).filter({ has: page.getByRole('button', { name: /查看结果/ }) }).first();
  if (await row.count()) {
    await row.getByRole('button', { name: /查看结果/ }).first().click({ timeout: 5000 });
    await page.waitForTimeout(3000);
    // 若停在过程页须再点查看结果
    if (/view=processing/.test(page.url())) {
      const vr = page.getByRole('button', { name: /查看结果/ }).first();
      if (await vr.count()) { await vr.click({ timeout: 4000 }).catch(() => {}); await page.waitForTimeout(2500); }
    }
    const url = page.url();
    const body = await main(page);
    // 表头
    const headers = await page.locator('main .arco-table-th, main thead th, main [role="columnheader"]').allTextContents().catch(() => []);
    // 首行文本
    const firstRow = page.locator('main tbody tr, main [role="row"]').first();
    const rowText = (await firstRow.innerText().catch(() => '')).trim().replace(/\s+/g, ' ').slice(0, 400);
    // 重新分析按钮？
    const rerun = page.getByRole('button', { name: /重新分析/ });
    const rerunCount = await rerun.count();
    // 配置区是否仍可见（01274 需要）
    const cfgVisible = await page.getByText('分析配置').first().isVisible().catch(() => false);
    const modelVisible = await page.getByText(/培育评估模型/).first().isVisible().catch(() => false);
    const rowsN = await page.locator('main tbody tr, main [role="row"]').count();
    out.result_view = { url, headers, row_count: rowsN, first_row: rowText, rerun_btn_count: rerunCount, config_visible: cfgVisible, model_visible: modelVisible, body_head: body.split('\n').slice(0, 30) };
  } else {
    out.result_view = { err: '无可查看结果行' };
  }
} catch (e) { out.result_view = { err: String(e).slice(0, 200) }; }
dump('scout-result-view.json');

// ---------- 6. 当天复用：结果态返回配置 → 同条件再点开始分析 ----------
try {
  // 回主 Tab（若在结果态，找返回/切 Tab 途径）
  const backCfg = page.locator('[role=tab][data-tab-key="cultivate"]');
  await backCfg.first().click({ timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(1500);
  let url = page.url();
  let body = await main(page);
  // 若仍结果态，尝试「重新分析」或再次开始分析
  const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
  const startVisible = await start.isVisible().catch(() => false);
  let reuse = 'start-not-visible';
  if (startVisible) {
    const rowsBefore = await page.locator('main [role=tab][data-tab-key="records"]').count().catch(() => 0);
    await start.click({ timeout: 5000 });
    await page.waitForTimeout(3500);
    url = page.url();
    body = await main(page);
    reuse = /view=result|培育名单|排名|综合/.test(url + body) ? 'direct-result?' : 'unknown:' + url.slice(-80);
  }
  out.same_day_reuse = { url_after: url, reuse, body_head: body.split('\n').slice(0, 22) };
} catch (e) { out.same_day_reuse = { err: String(e).slice(0, 200) }; }
dump('scout-reuse.json');

// ---------- 7. 评审模式开关 / 零泄漏 ----------
try {
  const persona = page.locator('button.persona-switch').first();
  await persona.click({ timeout: 4000 });
  await page.waitForTimeout(600);
  const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
  const checkedOn = (await sw.getAttribute('aria-checked').catch(() => null)) === 'true';
  // 关
  if (checkedOn) { await sw.click({ timeout: 4000 }); await page.waitForTimeout(800); }
  const bodyOff = await main(page);
  const leakOff = /指标未登记|Q063|Q-SVCCHAIN|需求追溯|评审模式|metric_id|GAP-/.test(bodyOff) ? bodyOff.match(/.{0,30}(指标未登记|Q063|Q-SVCCHAIN|需求追溯|GAP-).{0,40}/g) : null;
  // 开回去
  await persona.click({ timeout: 4000 }).catch(() => {});
  await page.waitForTimeout(600);
  const sw2 = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
  if (((await sw2.getAttribute('aria-checked').catch(() => null)) === 'false')) { await sw2.click({ timeout: 4000 }); await page.waitForTimeout(800); }
  await page.keyboard.press('Escape').catch(() => {});
  out.review_toggle = { was_on: checkedOn, leak_after_off: leakOff, restored: (await sw2.getAttribute('aria-checked').catch(() => null)) };
} catch (e) { out.review_toggle = { err: String(e).slice(0, 200) }; }
dump('scout-review.json');

// ---------- 8. attract 隔离 ----------
try {
  await page.goto(baseUrl.replace(/\/?$/, '') + '/service/institution-decision?workspace=attract&tab=attract', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2200);
  const title = await page.title();
  const body = (await main(page)).slice(0, 500);
  const hasCultModel = /培育评估模型/.test(body);
  const hasCultBadge = /指标未登记：培育综合分/.test(body);
  await page.goto(target, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1800);
  const backOk = /培育服务机构推荐分析/.test(await page.title()) && /培育评估模型/.test(await main(page));
  out.attract_isolation = { attract_title: title, has_cultivate_model: hasCultModel, has_cultivate_badge: hasCultBadge, cultivate_restored: backOk, attract_body_head: body.split('\n').slice(0, 14) };
} catch (e) { out.attract_isolation = { err: String(e).slice(0, 200) }; }
dump('scout-attract.json');

// ---------- 9. 失败态可行性（route.abort 起任务接口） ----------
try {
  const respSeen = [];
  page.on('request', (r) => { if (/svc|institution|task|analy/.test(r.url()) && r.method() === 'POST') respSeen.push(r.method() + ' ' + r.url().slice(0, 120)); });
  await page.route('**/svc/topic/v1/**', (r) => r.abort());
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 5000 });
  await page.waitForTimeout(600);
  await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 5000 });
  await page.waitForTimeout(800);
  await page.getByRole('button', { name: '开始分析', exact: true }).first().click({ timeout: 5000 });
  await page.waitForTimeout(5000);
  const url = page.url();
  const body = (await main(page)).slice(0, 600);
  await page.unroute('**/svc/topic/v1/**');
  out.failure_probe = { url, body_head: body.split('\n').slice(0, 24), post_seen: respSeen.slice(0, 8) };
} catch (e) { out.failure_probe = { err: String(e).slice(0, 200) }; }
dump('scout-failure.json');

await page.screenshot({ path: path.join(__dirname, 'probe-backfill-final.png') }).catch(() => {});
await browser.close();
console.log('probe done:', Object.keys(out).join(', '));
