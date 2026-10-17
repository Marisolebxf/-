#!/usr/bin/env node
/**
 * 一次性无头探针（P0-12 写稿用）：FUNC-00682 权重边界（非负/小数/超界）与权和≠100。
 * 不点「开始评估」发起链。产物落 scout-p012.json；勿当 runner。
 */
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const target = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;
const outDir = __dirname;

async function ensureLogin(page) {
  await page.waitForTimeout(600);
  if (!page.url().includes('/login')) return;
  const pw = page.locator('input[type=password]');
  await pw.first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
  if (!(await pw.count())) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await pw.first().fill('123456');
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

async function gotoFresh(page) {
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(1500);
  await closeBasket(page);
}

async function sumHint(page) {
  const t = ((await page.locator('main').innerText().catch(() => '')) || '').replace(/\s+/g, ' ');
  const m = t.match(/权重合计：[^\n]{0,80}/);
  return m ? m[0] : '';
}

async function spinVals(page) {
  const spins = page.locator('[role=spinbutton]');
  const n = await spins.count();
  const vals = [];
  for (let i = 0; i < n; i++) vals.push(String(await spins.nth(i).inputValue()));
  return vals;
}

async function tryFill(page, idx, raw) {
  const spins = page.locator('[role=spinbutton]');
  const before = String(await spins.nth(idx).inputValue());
  await spins.nth(idx).click({ timeout: 3000 });
  await spins.nth(idx).fill(String(raw));
  await page.keyboard.press('Tab');
  await page.waitForTimeout(600);
  const after = String(await spins.nth(idx).inputValue());
  const hint = await sumHint(page);
  // aria / validity
  const ariaInvalid = await spins.nth(idx).getAttribute('aria-invalid').catch(() => null);
  const min = await spins.nth(idx).getAttribute('min').catch(() => null);
  const max = await spins.nth(idx).getAttribute('max').catch(() => null);
  const step = await spins.nth(idx).getAttribute('step').catch(() => null);
  return { raw: String(raw), before, after, accepted: after === String(raw), hint, ariaInvalid, min, max, step };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), case: 'P0-12', func: '00682' };

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await gotoFresh(page);
  out.url = page.url();

  const spins = page.locator('[role=spinbutton]');
  await spins.first().waitFor({ state: 'visible', timeout: 10000 });
  out.spin_count = await spins.count();
  out.defaults = await spinVals(page);
  out.default_hint = await sumHint(page);

  // attrs of first spin
  out.spin0_attrs = {
    min: await spins.nth(0).getAttribute('min').catch(() => null),
    max: await spins.nth(0).getAttribute('max').catch(() => null),
    step: await spins.nth(0).getAttribute('step').catch(() => null),
    aria: await spins.nth(0).getAttribute('aria-label').catch(() => null),
    type: await spins.nth(0).getAttribute('type').catch(() => null),
  };

  // 1) negative -5 on 专利数量 (idx 0)
  out.neg = await tryFill(page, 0, '-5');
  await page.screenshot({ path: path.join(outDir, 'scout-p012-neg.png'), fullPage: false });

  // reset via reload
  await gotoFresh(page);

  // 2) decimal 10.5
  out.decimal = await tryFill(page, 0, '10.5');
  await page.screenshot({ path: path.join(outDir, 'scout-p012-decimal.png'), fullPage: false });

  await gotoFresh(page);

  // 3) over-bound 101
  out.over = await tryFill(page, 0, '101');
  await page.screenshot({ path: path.join(outDir, 'scout-p012-over.png'), fullPage: false });

  await gotoFresh(page);

  // 4) sum ≠ 100: 35/25/20/20/10
  const targets = ['35', '25', '20', '20', '10'];
  const setResults = [];
  for (let i = 0; i < 5; i++) {
    const spins2 = page.locator('[role=spinbutton]');
    await spins2.nth(i).fill(targets[i]);
    await page.keyboard.press('Tab');
    await page.waitForTimeout(400);
    setResults.push(String(await spins2.nth(i).inputValue()));
  }
  out.sum_ne100 = {
    set: targets,
    actual: setResults,
    sum: setResults.reduce((a, b) => a + Number(b), 0),
    hint: await sumHint(page),
  };
  const startBtn = page.getByRole('button', { name: /开始评估/ }).first();
  out.start_after_sum = {
    disabled: await startBtn.isDisabled().catch(() => null),
    enabled: await startBtn.isEnabled().catch(() => null),
  };
  // check silent normalize: values should stay 35/25/20/20/10 not renormalized to 100
  out.silent_normalize = setResults.join(',') !== targets.join(',');
  await page.screenshot({ path: path.join(outDir, 'scout-p012-sum.png'), fullPage: false });

  // also try typing with select-all for negative via keyboard
  await gotoFresh(page);
  const s0 = page.locator('[role=spinbutton]').nth(0);
  await s0.click({ timeout: 3000 });
  await page.keyboard.press('Control+a');
  await page.keyboard.type('-5');
  await page.keyboard.press('Tab');
  await page.waitForTimeout(600);
  out.neg_keyboard = {
    after: String(await s0.inputValue()),
    hint: await sumHint(page),
  };

  // Arco InputNumber often clamps on blur — check DOM min/max via parent
  const inputNumberInfo = await page.evaluate(() => {
    const el = document.querySelector('[role=spinbutton]');
    if (!el) return null;
    const wrap = el.closest('.arco-input-number');
    return {
      wrapClass: wrap ? wrap.className : '',
      valueAttr: el.getAttribute('value'),
      inputValue: el.value,
      parentHtml: wrap ? wrap.outerHTML.slice(0, 400) : '',
    };
  });
  out.input_number_dom = inputNumberInfo;

  fs.writeFileSync(path.join(outDir, 'scout-p012.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
} catch (e) {
  out.error = String(e).slice(0, 500);
  fs.writeFileSync(path.join(outDir, 'scout-p012.json'), JSON.stringify(out, null, 2));
  console.error(out.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
