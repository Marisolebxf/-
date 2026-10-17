#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-chain-shortboard P0-06（FUNC-00690 环节卡内容构成）。
 * 目的：查明结果态是否渲染环节卡 + 卡上字段形态（环节名/服务类型清单/机构数/服务深度）。
 * 路径：历史「查看结果」逐条看；若全空再 fresh 起一次分析看过程→结果。
 * 产物落同目录 scout-p0-06-*.json / *.png；勿当 runner。
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
const baseRoute = '/service/chain-analysis?workspace=chain&tab=chain';
const outDir = __dirname;

const dump = (name, data) => fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2), 'utf8');

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
  for (let i = 0; i < 3; i++) {
    const close = page.locator('[aria-label="关闭对比篮"]');
    if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
      await close.first().click().catch(() => {});
      await page.waitForTimeout(400);
    } else break;
  }
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(200);
}

// 捕获结果态现场：url / 诚实空 / 轨道站 / 卡文本 / 关键字段命中 / 接口 payload
async function captureResult(page, tag, responses) {
  await page.waitForTimeout(3500);
  const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  const noStagesLoc = page.locator('[data-testid="svc-eco-shortboard-no-stages"]');
  const noStagesVisible = (await noStagesLoc.count()) > 0 && (await noStagesLoc.first().isVisible().catch(() => false));
  const stLoc = page.locator('[data-testid="svc-eco-metro"] [data-stage-id], .svc-eco-metro-station, [data-stage-id]');
  const stCount = await stLoc.count();
  const stationTexts = [];
  for (let i = 0; i < Math.min(stCount, 8); i++) {
    stationTexts.push(((await stLoc.nth(i).innerText().catch(() => '')) || '').trim().replace(/\s+/g, ' ').slice(0, 300));
  }
  // 兜底：board 内任何类名含 stage/card/station 的节点文本（防 data-testid 命名漂移）
  const cardsLoc = page.locator('[data-testid="svc-eco-shortboard-board"] [class*=stage], [data-testid="svc-eco-shortboard-board"] [class*=card], [data-testid="svc-eco-shortboard-board"] [class*=station], .svc-eco-stage-card, .shortboard-stage-card');
  const cardCount = await cardsLoc.count();
  const cardTexts = [];
  for (let i = 0; i < Math.min(cardCount, 8); i++) {
    cardTexts.push(((await cardsLoc.nth(i).innerText().catch(() => '')) || '').trim().replace(/\s+/g, ' ').slice(0, 300));
  }
  const kw = {
    orgCount: /在库(服务)?机构|机构数|服务机构/.test(body),
    depth: /服务深度|平均服务深度|深度/.test(body),
    svcTypes: /服务类型|研发支持|技术转移|中试|孵化|产业化|投融资/.test(body),
    demo: /专家知识库|演示/.test(body),
  };
  const shot = `scout-p0-06-${tag}.png`;
  await page.screenshot({ path: path.join(outDir, shot), fullPage: false }).catch(() => {});
  dump(`scout-p0-06-${tag}.json`, {
    tag,
    url: page.url(),
    noStagesVisible,
    boardCount: await page.locator('[data-testid="svc-eco-shortboard-board"]').count(),
    metroCount: await page.locator('[data-testid="svc-eco-metro"]').count(),
    stationCount: stCount,
    stationTexts,
    cardCount,
    cardTexts,
    keywords: kw,
    bodySlice: body.slice(0, 2200),
    apiResponses: responses.slice(-3),
  });
  return { noStagesVisible, stationCount: stCount, cardCount };
}

// 抓 result 接口 payload（看 stages/gap 环节行是否存在于数据层）
function watchApi(page, bag) {
  page.on('response', async (r) => {
    try {
      const u = r.url();
      if (/shortboard|chain-analysis|svc/.test(u) && /result|task/.test(u) && r.status() < 300) {
        const ct = r.headers()['content-type'] || '';
        if (ct.includes('json')) {
          const txt = (await r.text().catch(() => '')).slice(0, 1200);
          bag.push({ url: u.slice(0, 160), status: r.status(), body: txt });
        }
      }
    } catch {}
  });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const apiBag = [];
watchApi(page, apiBag);
const out = { probed_at: new Date().toISOString(), histories: [], fresh: null };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(baseRoute.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  // ---- 1) 历史记录逐条查看结果 ----
  const recTab = page.getByRole('tab', { name: '分析记录', exact: true });
  await recTab.click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const viewBtns = page.getByRole('button', { name: /查看结果/ });
  const nBtn = Math.min(await viewBtns.count(), 3);
  for (let i = 0; i < nBtn; i++) {
    const btn = viewBtns.nth(i);
    if (!(await btn.isEnabled().catch(() => false))) { out.histories.push({ i, skipped: 'disabled' }); continue; }
    await btn.click({ timeout: 8000 }).catch(() => {});
    const cap = await captureResult(page, `hist${i}`, apiBag);
    out.histories.push({ i, ...cap });
    // 回分析记录，准备下一条
    await recTab.click({ timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(1500);
    await closeBasket(page);
  }

  // ---- 2) 若历史全无环节卡，fresh 起一次分析 ----
  const anyStage = out.histories.some((h) => (h.stationCount || 0) > 0 || (h.cardCount || 0) > 0);
  if (!anyStage) {
    await page.goto(new URL(baseRoute.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2000);
    await closeBasket(page);
    const sel = page.locator('.industry-catalog-select, .arco-select').filter({ has: page.locator('input[placeholder="选择产业集群"]') }).first();
    await sel.click({ timeout: 8000 });
    await page.waitForTimeout(700);
    await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
    await page.waitForTimeout(1000);
    const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
    await start.click({ timeout: 5000 }).catch(() => {});
    // 轮询最多 90s：进 result / 出 board 或诚实空
    let timeline = [];
    let done = false;
    for (let t = 0; t < 30 && !done; t++) {
      await page.waitForTimeout(3000);
      const url = page.url();
      const board = await page.locator('[data-testid="svc-eco-shortboard-board"]').count();
      const noSt = await page.locator('[data-testid="svc-eco-shortboard-no-stages"]').count();
      const st = await page.locator('[data-stage-id], .svc-eco-metro-station').count();
      timeline.push(`${t * 3}s url=${url.replace(baseUrl, '')} board=${board} noStages=${noSt} stations=${st}`);
      if (/view=result/.test(url) || board > 0 || (noSt > 0 && /view=result/.test(url))) done = true;
    }
    const cap = await captureResult(page, 'fresh', apiBag);
    out.fresh = { timeline, ...cap };
  }
} catch (e) {
  out.error = String(e).slice(0, 400);
}
dump('scout-p0-06-summary.json', out);
await browser.close();
console.log('p0-06 probe done:', JSON.stringify({ histories: out.histories.map((h) => ({ i: h.i, st: h.stationCount, card: h.cardCount, noSt: h.noStagesVisible })), fresh: out.fresh ? { st: out.fresh.stationCount, card: out.fresh.cardCount, noSt: out.fresh.noStagesVisible } : null, error: out.error || null }));
