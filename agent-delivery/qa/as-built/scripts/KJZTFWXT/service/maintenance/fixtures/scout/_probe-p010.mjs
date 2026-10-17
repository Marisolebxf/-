#!/usr/bin/env node
/**
 * P0-10（FUNC-01360 异常-远端异常·网络异常反馈）写前无头探针。
 * 先验：BrowserContext.setOffline(true) + reload 是否可构造「明确异常反馈」；
 * 壳页缓存命中仍显正常占位 = 模拟条件不可用（D4）→ B 档 allow_skip + ticket。
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
const FEEDBACK_RE = /错误|失败|不可用|网络|重试|异常|加载失败|服务不可用|offline|ERR_|timed?\s*out|无法访问|连接/i;
const PLACEHOLDER_RE = /入口已对齐 demo 路由/;

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

async function snap(page) {
  const url = page.url();
  const title = await page.title().catch(() => '');
  const body = ((await page.locator('body').innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  const main = ((await page.locator('main').first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  const h1 = ((await page.getByRole('heading', { name: '维护管理', level: 1 }).first().innerText().catch(() => '')) || '').trim();
  const alertCount = await page.locator('.arco-alert, [role=alert], .arco-result').count();
  const alertTexts = await page.locator('.arco-alert, [role=alert], .arco-result').evaluateAll((els) =>
    els.map((e) => (e.innerText || '').replace(/\s+/g, ' ').trim()).filter(Boolean).slice(0, 8),
  );
  return {
    url,
    title,
    h1,
    bodyHead: body.slice(0, 400),
    mainHead: main.slice(0, 400),
    bodyLen: body.length,
    hasPlaceholder: PLACEHOLDER_RE.test(body) || PLACEHOLDER_RE.test(main),
    hasFeedback: FEEDBACK_RE.test(body) || FEEDBACK_RE.test(title),
    feedbackHits: (body.match(FEEDBACK_RE) || []).slice(0, 12),
    alertCount,
    alertTexts,
  };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const result = {
  at: new Date().toISOString(),
  baseUrl,
  route,
  method: 'setOffline(true) + reload（Playwright BrowserContext；用例步骤「中断网络连接；刷新页面」合法模拟）',
  baseline: null,
  offline: null,
  offlineReloadError: null,
  afterRestore: null,
  constructable: false,
  recommendation: '',
};

try {
  await page.goto(new URL('/login', baseUrl).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await ensureLogin(page);
  await page.goto(new URL(route, baseUrl).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(1500);
  await closeBasket(page);
  result.baseline = await snap(page);
  await page.screenshot({ path: path.join(outDir, 'probe-p010-baseline.png'), fullPage: true });

  await context.setOffline(true);
  let reloadErr = null;
  try {
    await page.reload({ waitUntil: 'domcontentloaded', timeout: 20000 });
  } catch (e) {
    reloadErr = String(e && e.message ? e.message : e).slice(0, 300);
  }
  await page.waitForTimeout(2500);
  result.offlineReloadError = reloadErr;
  result.offline = await snap(page);
  await page.screenshot({ path: path.join(outDir, 'probe-p010-offline.png'), fullPage: true }).catch(() => {});

  await context.setOffline(false);
  await page.waitForTimeout(400);
  try {
    await page.goto(new URL(route, baseUrl).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(1200);
    await closeBasket(page);
  } catch (e) {
    result.restoreError = String(e && e.message ? e.message : e).slice(0, 300);
  }
  result.afterRestore = await snap(page);
  await page.screenshot({ path: path.join(outDir, 'probe-p010-restored.png'), fullPage: true }).catch(() => {});

  const off = result.offline || {};
  const hasFeedback = !!off.hasFeedback || !!reloadErr || (off.alertCount > 0 && off.alertTexts.some((t) => FEEDBACK_RE.test(t)));
  const silentOk = !!off.hasPlaceholder && !hasFeedback && /\/service\/maintenance/.test(off.url || '');
  result.constructable = hasFeedback && !silentOk;
  result.silentCacheHit = silentOk;
  result.recommendation = result.constructable
    ? 'B档实跑零 allow_skip：setOffline+reload 可采到明确异常反馈；expect 双层写全；不进 gold'
    : 'B档 allow_skip+ticket：setOffline+reload 壳页缓存命中/无明确异常反馈（或仅导航超时无 UI 反馈）——用例前置「具备网络中断模拟条件」不可达；禁止用正常占位绿冒充异常反馈。ticket=ENV-SVCMAINT-NET-SIM-UNAVAILABLE';
} catch (e) {
  result.fatal = String(e && e.stack ? e.stack : e).slice(0, 800);
  try {
    await context.setOffline(false);
  } catch {}
  result.recommendation =
    '探针异常；默认 B 档 allow_skip+ticket=ENV-SVCMAINT-NET-SIM-UNAVAILABLE；禁止假绿';
} finally {
  await browser.close().catch(() => {});
}

const outPath = path.join(outDir, 'probe-p010.json');
fs.writeFileSync(outPath, JSON.stringify(result, null, 2));
console.log(JSON.stringify({ outPath, constructable: result.constructable, silentCacheHit: result.silentCacheHit, recommendation: result.recommendation, offlineReloadError: result.offlineReloadError }, null, 2));
