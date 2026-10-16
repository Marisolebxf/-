/**
 * P0-13（FUNC-00668 评审模式零泄漏）一次性无头探针。产物 scout-p013-review.json；勿当 runner。
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
const target = `${baseUrl.replace(/\/?$/, '')}/service/institution-judgment?workspace=trend&tab=trend`;
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

// click both + popover
out.popovers = [];
const popSel = '.arco-trigger-popup:visible, .arco-popover:visible';
for (const lb of need) {
  await page.mouse.click(1500, 600).catch(() => {});
  await page.waitForTimeout(400);
  const b = page.locator(`button.trace-info-icon[aria-label^="${lb}"]`).first();
  await b.click({ timeout: 5000 });
  await page.waitForTimeout(800);
  const pop = page.locator(popSel).first();
  const open = (await pop.count()) && (await pop.isVisible().catch(() => false));
  const text = open ? ((await pop.innerText().catch(() => '')) || '').slice(0, 400) : '';
  out.popovers.push({ lb, open, text });
  await page.mouse.click(1500, 600).catch(() => {});
  await page.waitForTimeout(400);
}

// pick industry as fingerprint anchor
const sel = page.locator('.industry-catalog-select').first();
out.industry_visible = await sel.isVisible().catch(() => false);
if (out.industry_visible) {
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(600);
  await page
    .locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
    .filter({ hasText: '新一代信息技术' })
    .first()
    .click({ timeout: 8000 })
    .catch(() => {});
  await page.waitForTimeout(1000);
  out.industry_echo = ((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
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
// ensure still off after reload
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
const LEAKS = ['需求追溯', 'metric_id', 'GAP-', 'Q0', 'Q-', '评审模式'];
out.leak_hits = LEAKS.filter((k) => mainText.includes(k));
out.industry_echo_after = out.industry_visible
  ? ((await page.locator('.industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '')) || '').trim()
  : null;
out.url_after = page.url();
out.workspace_ok = /workspace=trend/.test(out.url_after);
out.tab_main_selected = await page.locator('[role=tab][data-tab-key="trend"]').getAttribute('aria-selected');

fs.writeFileSync(path.join(outDir, 'scout-p013-review.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
