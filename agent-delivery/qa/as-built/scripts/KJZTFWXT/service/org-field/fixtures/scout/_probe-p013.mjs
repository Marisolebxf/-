/**
 * P0-13（FUNC-00653 评审模式零泄漏）一次性无头探针。产物 scout-p013-review.json；勿当 runner。
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
const target = `${baseUrl.replace(/\/?$/, '')}/service/institution-judgment?workspace=field&tab=coverage`;
const outDir = __dirname;

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
    await page.waitForTimeout(400);
  }
}

async function setReview(page, wantOn) {
  const persona = page.locator('button.persona-switch').first();
  await persona.click({ timeout: 5000 });
  await page.waitForTimeout(500);
  const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
  await sw.waitFor({ state: 'visible', timeout: 8000 });
  let checked = await sw.getAttribute('aria-checked').catch(() => null);
  if (checked === null) {
    const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]');
    checked = /arco-switch-checked/.test((await holder.first().getAttribute('class').catch(() => '')) || '')
      ? 'true'
      : 'false';
  }
  const on = checked === 'true';
  if (on !== wantOn) {
    await sw.click({ timeout: 5000 });
    await page.waitForTimeout(800);
  }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(400);
  return { before: on, after: wantOn };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();

await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(2000);
await closeBasket(page);

const out = { probed_at: new Date().toISOString(), url: page.url() };
out.ls_review = await page.evaluate(() => localStorage.getItem('ent_review_mode'));

// clear residual selection
const main0 = ((await page.locator('main').first().innerText().catch(() => '')) || '');
if (/已选机构（[1-9]/.test(main0)) {
  const clr = page.locator('main').getByRole('button', { name: '清空' });
  if (await clr.count()) {
    await clr.first().click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(500);
  }
}

// pick 1 org
const pick = page.getByRole('button', { name: '选择机构' }).first();
await pick.click({ timeout: 8000 });
await page.waitForTimeout(800);
const dialog = page.locator('.arco-modal:visible, .arco-modal').filter({ hasText: '选择服务机构' }).first();
const boxes = dialog.locator('.arco-checkbox:not(.arco-checkbox-disabled)');
for (let i = 0; i < 15 && !(await boxes.count()); i++) {
  await page.waitForTimeout(400);
}
if (await boxes.count()) {
  await boxes.first().click({ timeout: 8000 });
  await page.waitForTimeout(300);
  await dialog.getByRole('button', { name: '确定', exact: true }).last().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  out.select_mode = 'modal';
} else {
  await page.keyboard.press('Escape').catch(() => {});
  await page.goto(
    `${baseUrl.replace(/\/?$/, '')}/service/institution-judgment?workspace=field&tab=coverage&org_ids[]=79bbcfc0e68027808f1f4caf1b6f0469`,
    { waitUntil: 'domcontentloaded' },
  );
  await page.waitForTimeout(2000);
  out.select_mode = 'deeplink_fallback';
}
out.selected_label = await page.getByText(/已选机构（1\s*家）/).first().isVisible().catch(() => false);
const tags = page.locator('[data-testid="svc-org-analysis-context"] .arco-tag.svc-org-pick-tag');
out.tag_text = (await tags.first().innerText().catch(() => '')).trim();
out.org_ids = (() => {
  const u = new URL(page.url());
  const a = u.searchParams.getAll('org_ids[]');
  return a.length ? a : u.searchParams.getAll('org_ids');
})();

const filterInput = page.getByPlaceholder('筛选领域（不改分析指纹）');
out.filter_visible = await filterInput.isVisible().catch(() => false);
if (out.filter_visible) {
  await filterInput.fill('新一代', { timeout: 5000 });
  await page.waitForTimeout(500);
  out.filter_val = await filterInput.inputValue().catch(() => '');
}

out.turn_on = await setReview(page, true);
await page.waitForTimeout(500);

const main = page.locator('main').first();
out.traces_on = await page.locator('button.trace-info-icon').evaluateAll((els) =>
  els.map((e) => ({
    aria: e.getAttribute('aria-label') || '',
    mount: e.getAttribute('data-review-mount-id') || '',
    visible: !!(e.offsetParent || e.getClientRects().length),
    inMain: !!e.closest('main'),
  })),
);

const need = ['服务机构分析工作区', '分析配置'];
out.need_buttons = {};
for (const lb of need) {
  const b = page.locator(`button.trace-info-icon[aria-label^="${lb}"]`).first();
  const cnt = await b.count();
  const vis = cnt ? await b.isVisible().catch(() => false) : false;
  const en = cnt ? await b.isEnabled().catch(() => false) : false;
  out.need_buttons[lb] = { count: cnt, visible: vis, enabled: en };
}

out.popovers = [];
const popSel = '.arco-trigger-popup:visible, .arco-popover:visible';
for (const lb of need) {
  await page.mouse.click(1500, 600).catch(() => {});
  await page.waitForTimeout(400);
  const b = page.locator(`button.trace-info-icon[aria-label^="${lb}"]`).first();
  if (!(await b.count())) {
    out.popovers.push({ lb, open: false, text: '', err: 'button missing' });
    continue;
  }
  await b.click({ timeout: 5000 });
  await page.waitForTimeout(800);
  const pop = page.locator(popSel).first();
  const open = (await pop.count()) && (await pop.isVisible().catch(() => false));
  const text = open ? ((await pop.innerText().catch(() => '')) || '').slice(0, 400) : '';
  out.popovers.push({ lb, open, text });
  await page.mouse.click(1500, 600).catch(() => {});
  await page.waitForTimeout(400);
}

out.url_before_off = page.url();
out.body_snip_on = ((await main.innerText().catch(() => '')) || '')
  .split('\n')
  .map((s) => s.trim())
  .filter(Boolean)
  .slice(0, 25);

out.turn_off = await setReview(page, false);
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);
await closeBasket(page);
out.after_reload_ls = await page.evaluate(() => localStorage.getItem('ent_review_mode'));
const persona = page.locator('button.persona-switch').first();
await persona.click({ timeout: 5000 });
await page.waitForTimeout(400);
const sw2 = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
let checked2 = await sw2.getAttribute('aria-checked').catch(() => null);
if (checked2 === 'true') {
  await sw2.click({ timeout: 5000 });
  await page.waitForTimeout(600);
}
await page.keyboard.press('Escape').catch(() => {});
await page.waitForTimeout(400);

out.traces_off_main = await main.locator('button.trace-info-icon, button[aria-label*="需求追溯"]').count();
out.traces_off_page = await page.locator('button.trace-info-icon').count();
out.metric_cards_off = await main.locator('.metric-spec-card, [data-review-metric]').count();
const mainText = (await main.innerText().catch(() => '')) || '';
const LEAKS = ['需求追溯', 'metric_id', 'GAP-', 'Q0', 'Q-SVCCHAIN', '指标未登记', '禁止改绿'];
out.leak_hits = LEAKS.filter((k) => mainText.includes(k));
if (/Q0\d{2}/.test(mainText)) out.leak_hits.push('Q0xx');
out.selected_after = await page.getByText(/已选机构（1\s*家）/).first().isVisible().catch(() => false);
out.tag_after = (await tags.first().innerText().catch(() => '')).trim();
out.filter_after = out.filter_visible
  ? await page.getByPlaceholder('筛选领域（不改分析指纹）').inputValue().catch(() => '')
  : null;
out.org_ids_after = (() => {
  const u = new URL(page.url());
  const a = u.searchParams.getAll('org_ids[]');
  return a.length ? a : u.searchParams.getAll('org_ids');
})();
out.url_after = page.url();
out.workspace_ok = /workspace=field/.test(out.url_after);
out.tab_coverage_selected = await page.locator('[role=tab][data-tab-key="coverage"]').getAttribute('aria-selected');
out.no_auto_task = !/view=processing|view=result|task_id=/.test(out.url_after);

fs.writeFileSync(path.join(outDir, 'scout-p013-review.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
