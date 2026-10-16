#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-chain-shortboard P0-22（FUNC-00705 无效环节参数）。
 * 探：结果态 URL 拼 segment=INVALID-SEGMENT-404 冷加载 → 是否开 Drawer / 「环节不存在」提示 / 清参。
 * 公约：独立无头；产物只落本目录；失败落 json 继续；不动业务仓。
 * 对照：同日 _probe-p018.json s2；graph P0-23 无效 org 同构。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://111.198.38.90:50892';
const ROUTE = '/service/chain-analysis?workspace=chain&tab=chain';
const DEEP =
  'http://111.198.38.90:50892/service/chain-analysis?workspace=chain&tab=chain&industry=INB1701&view=result&demo_state=result&task_id=SVC-20261015-066';
const OUT = {
  probed_at: new Date().toISOString(),
  entry: 'svc-chain-shortboard',
  case: 'P0-22 / FUNC-00705',
  invalid_segment: 'INVALID-SEGMENT-404',
  result_base: null,
  coldload: null,
};
const dump = () =>
  fs.writeFileSync(path.join(__dirname, '_probe-p022.json'), JSON.stringify(OUT, null, 2), 'utf8');

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
    await close.first().click({ timeout: 1500 }).catch(() => {});
    await page.waitForTimeout(300);
  }
}
async function pickViewResult(page) {
  const btns = page.getByRole('button', { name: /查看结果/ });
  const n = await btns.count();
  for (let i = 0; i < n; i++) {
    const b = btns.nth(i);
    const dis = await b.isDisabled().catch(() => true);
    const cls = ((await b.getAttribute('class').catch(() => '')) || '');
    if (!dis && !/arco-btn-disabled/.test(cls) && (await b.isVisible().catch(() => false))) {
      await b.click({ timeout: 8000 });
      return true;
    }
  }
  return false;
}

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await ctx.newPage();
try {
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  await closeBasket(page);

  // 进结果态：hist → 深链回落（P0-21 同款）
  let resultUrl = '';
  try {
    const rec = page.getByRole('tab', { name: '分析记录', exact: true });
    await rec.click({ timeout: 8000 });
    await page.waitForTimeout(2000);
    let clicked = await pickViewResult(page);
    if (!clicked) {
      await page.waitForTimeout(2500);
      clicked = await pickViewResult(page);
    }
    if (!clicked) {
      await page.goto(DEEP, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3500);
      OUT.result_base = { path: 'deep', url: page.url() };
    } else {
      await page.waitForTimeout(3000);
      if (/view=processing/.test(page.url())) {
        await pickViewResult(page);
        await page.waitForTimeout(2500);
      }
      OUT.result_base = { path: 'hist', url: page.url() };
    }
    resultUrl = page.url();
    if (!/view=result/.test(resultUrl)) {
      OUT.result_base = { ...(OUT.result_base || {}), err: '未落结果态', url: resultUrl };
      dump();
    } else {
      OUT.result_base = {
        ...(OUT.result_base || {}),
        view_result: true,
        shell: /全周期服务链路/.test(
          ((await page.locator('main').first().innerText().catch(() => '')) || ''),
        ),
        stations: await page.locator('[data-stage-id], .svc-eco-metro-station').count().catch(() => 0),
        drawers: await page.locator('.arco-drawer').count().catch(() => 0),
      };
    }
  } catch (e) {
    OUT.result_base = { err: String(e).slice(0, 400) };
  }
  dump();

  if (!resultUrl || !/view=result/.test(resultUrl)) {
    resultUrl = DEEP;
  }

  const segUrl = /[?&]segment=/.test(resultUrl)
    ? resultUrl.replace(/([?&])segment=[^&]*/, '$1segment=INVALID-SEGMENT-404')
    : resultUrl + (resultUrl.includes('?') ? '&' : '?') + 'segment=INVALID-SEGMENT-404';

  try {
    await page.goto(segUrl, { waitUntil: 'domcontentloaded' });
    await ensureLogin(page);
    let msgSeen = false;
    let msgText = '';
    let cleaned = false;
    let drawerSeen = false;
    const deadline = Date.now() + 12000;
    while (Date.now() < deadline) {
      const mts = await page.locator('.arco-message, .arco-message-list, .arco-notification').allInnerTexts().catch(() => []);
      const mt = ((mts || []).join(' ') || '').trim();
      if (!msgSeen && /环节不存在|不存在|无效/.test(mt)) {
        msgSeen = true;
        msgText = mt.slice(0, 120);
      }
      const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
      if (!msgSeen && /环节不存在/.test(body)) {
        msgSeen = true;
        msgText = 'body:' + body.slice(0, 80);
      }
      if (!cleaned && !/[?&]segment=/.test(page.url())) cleaned = true;
      const dVis = await page.locator('.arco-drawer').first().isVisible().catch(() => false);
      if (dVis) drawerSeen = true;
      if (msgSeen && cleaned) break;
      await page.waitForTimeout(400);
    }
    const urlNow = page.url();
    const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    await page.screenshot({ path: path.join(__dirname, 'probe-p022-segment-coldload.png') }).catch(() => {});
    OUT.coldload = {
      seg_url_loaded: segUrl,
      final_url: urlNow,
      segment_cleaned: cleaned,
      segment_still_in_url: /[?&]segment=/.test(urlNow),
      segment_value: ((/[?&]segment=([^&]*)/.exec(urlNow) || [])[1] || null),
      msgSeen,
      msgText: msgText || null,
      drawerSeen,
      drawerCount: await page.locator('.arco-drawer').count().catch(() => 0),
      still_result_view: /view=result/.test(urlNow),
      still_chain_route: /\/service\/chain-analysis/.test(urlNow),
      body_head: body.slice(0, 360).replace(/\n+/g, ' | '),
    };
  } catch (e) {
    OUT.coldload = { err: String(e).slice(0, 400) };
  }

  const c = OUT.coldload || {};
  OUT.verdict = {
    constructable_00705: !!(c.seg_url_loaded && c.still_result_view),
    expect1_no_drawer: c.drawerSeen === false,
    expect2_tip: !!c.msgSeen,
    expect2_clear: !!c.segment_cleaned,
    unhandled:
      c.segment_still_in_url === true && !c.msgSeen && c.drawerSeen === false,
    recommendation: c.segment_still_in_url && !c.msgSeen
      ? 'B档实跑无 allow_skip；预期①终态无 Drawer 可绿；预期②清参+提示未承载→设计红挂 D3-SVCSHORT-INVALID-SEGMENT-UNHANDLED（与 STAGE-DRAWER-MISSING 同根）'
      : '按实勘写 expect；禁止用「无面板」单独伪绿预期②',
  };
  dump();
} finally {
  await browser.close();
}
console.log(JSON.stringify(OUT.verdict || OUT, null, 2));
