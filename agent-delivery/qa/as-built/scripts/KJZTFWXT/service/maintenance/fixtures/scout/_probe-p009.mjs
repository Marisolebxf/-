#!/usr/bin/env node
/**
 * P0-09（FUNC-01359 权限-评审模式零泄漏）写前无头探针。
 * 验证点先验：①人设面板「内部评审模式」开关可达（P3）；
 * ②开启态本页评审增量（trace/metric 角标）observed；
 * ③关闭+刷新后附录 A 字样零泄漏；④占位文案与 H1/title 不因开关改变。
 * 禁止当 runner；禁止有头 MCP。
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
const route = '/service/maintenance';
const outDir = __dirname;

const LEAK_TERMS = ['指标说明', '指标未登记', '需求追溯', 'metric_id', 'GAP-', 'Q-'];
const LEAK_Q0XX = /Q0\d{2}/;

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
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
}

async function openPersona(page) {
  let opener = page.locator('button.persona-switch, .persona-switch').first();
  if (!(await opener.isVisible().catch(() => false))) {
    opener = page.locator('[class*="persona" i]').first();
  }
  await opener.click({ timeout: 5000 });
  await page.waitForTimeout(600);
  return opener;
}

async function readReviewChecked(page) {
  const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"], button[role=switch][aria-label="内部评审模式"]').first();
  await sw.waitFor({ state: 'visible', timeout: 8000 });
  let checked = await sw.getAttribute('aria-checked').catch(() => null);
  if (checked === null) {
    const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]');
    checked = /arco-switch-checked/.test((await holder.first().getAttribute('class').catch(() => '')) || '') ? 'true' : 'false';
  }
  return { sw, checked };
}

async function setReview(page, wantTrue) {
  await openPersona(page);
  const { sw, checked } = await readReviewChecked(page);
  const want = wantTrue ? 'true' : 'false';
  if (checked !== want) {
    await sw.click({ timeout: 5000 });
    await page.waitForTimeout(1000);
  }
  const after = await readReviewChecked(page);
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(400);
  return { before: checked, after: after.checked, want };
}

async function snapshotPage(page) {
  await closeBasket(page);
  const title = await page.title();
  const h1 = ((await page.getByRole('heading', { name: '维护管理', level: 1 }).innerText().catch(() => '')) || '').trim();
  const heading = page.locator('section.diagnosis-page-heading, .diagnosis-page-heading').first();
  const headingText = ((await heading.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  const mainText = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  const bodyText = ((await page.locator('body').innerText().catch(() => '')) || '');
  const traces = await page.locator('button.trace-info-icon, button[aria-label*="需求追溯"]').evaluateAll((els) =>
    els.map((e) => ({
      aria: e.getAttribute('aria-label') || '',
      inMain: !!e.closest('main'),
      visible: !!(e.offsetWidth || e.offsetHeight),
    })),
  );
  const metrics = await page.locator('.metric-spec-card, [data-review-metric], button[aria-label^="指标说明"], button[aria-label^="指标未登记"]').count();
  const leaksInMain = LEAK_TERMS.filter((k) => mainText.includes(k));
  if (LEAK_Q0XX.test(mainText)) leaksInMain.push('Q0xx');
  const leaksInBody = LEAK_TERMS.filter((k) => bodyText.includes(k));
  if (LEAK_Q0XX.test(bodyText)) leaksInBody.push('Q0xx');
  return {
    url: page.url(),
    title,
    h1,
    headingText,
    traces,
    metrics,
    leaksInMain,
    leaksInBody,
    mainHead: mainText.replace(/\s+/g, ' ').slice(0, 280),
  };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const probe = {
  probed_at: new Date().toISOString(),
  entry_id: 'svc-maintenance',
  case: 'FUNC-01359 / P0-09',
  route,
  steps: [],
};

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1500);

  const baseline = await snapshotPage(page);
  probe.steps.push({ id: 'baseline_default', ...baseline });

  // 读默认评审态
  await openPersona(page);
  const def = await readReviewChecked(page);
  await page.keyboard.press('Escape').catch(() => {});
  probe.steps.push({ id: 'default_review_checked', checked: def.checked });

  // 强制开评审 → observed 开启态
  const onRes = await setReview(page, true);
  await page.waitForTimeout(800);
  const onSnap = await snapshotPage(page);
  probe.steps.push({ id: 'review_on', toggle: onRes, ...onSnap });
  await page.screenshot({ path: path.join(outDir, 'probe-p009-review-on.png'), fullPage: false });

  // 关评审 + reload → 零泄漏
  const offRes = await setReview(page, false);
  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  // reload 后确认仍关（部分环境会恢复默认开）
  const offConfirm = await setReview(page, false);
  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  const offSnap = await snapshotPage(page);
  probe.steps.push({
    id: 'review_off_reload',
    toggle: offRes,
    offConfirm,
    ...offSnap,
    copyUnchanged: offSnap.headingText === baseline.headingText,
    h1Unchanged: offSnap.h1 === baseline.h1 || offSnap.h1 === '维护管理',
    titleKept: /维护管理/.test(offSnap.title),
    zeroLeakMain: offSnap.leaksInMain.length === 0 && offSnap.traces.filter((t) => t.inMain && t.visible).length === 0 && offSnap.metrics === 0,
  });
  await page.screenshot({ path: path.join(outDir, 'probe-p009-review-off.png'), fullPage: false });

  probe.conclusion = {
    personaReachable: true,
    defaultReviewOn: def.checked === 'true',
    openStateTraces: onSnap.traces,
    openStateMetrics: onSnap.metrics,
    openStateLeaksInMain: onSnap.leaksInMain,
    afterOffZeroLeak: probe.steps.find((s) => s.id === 'review_off_reload')?.zeroLeakMain,
    businessStateStable:
      probe.steps.find((s) => s.id === 'review_off_reload')?.copyUnchanged &&
      probe.steps.find((s) => s.id === 'review_off_reload')?.titleKept,
  };
  probe.ok = true;
} catch (e) {
  probe.ok = false;
  probe.error = String(e && e.stack ? e.stack : e);
  await page.screenshot({ path: path.join(outDir, 'probe-p009-error.png'), fullPage: false }).catch(() => {});
} finally {
  await browser.close();
  fs.writeFileSync(path.join(outDir, 'probe-p009.json'), JSON.stringify(probe, null, 2));
  console.log(JSON.stringify({ ok: probe.ok, conclusion: probe.conclusion, error: probe.error }, null, 2));
}
