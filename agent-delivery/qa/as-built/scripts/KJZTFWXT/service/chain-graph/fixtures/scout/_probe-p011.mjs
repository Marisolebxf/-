#!/usr/bin/env node
/**
 * P0-11（FUNC-00717 关联主体节点侧栏摘要）写前探针：
 * 模式②结果态深链（优先历史/当日模式②种子；无则 fresh 起一次）只读勘察：
 * ① 结果壳标题在屏；图谱滤镜回显「② 机构+关联主体」
 * ② hang 空文案 / G6 svc-eco-g6-graph / 空画布 svc-eco-empty-canvas
 * ③ 关联主体侧栏 svc-eco-actor-summary 是否已开；画布框是否可点
 * 公约：独立无头；产物只进本目录。尽量 0 POST；仅无模式②种子时 fresh 1 次。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
/** P0-08 探针实测模式②当日任务（见 _probe-p008-fresh.json；可能被清理） */
const MODE2_CANDIDATES = [
  '/service/chain-analysis?workspace=graph&tab=graph&industry=INB1701&eco_filter=orgs_and_actors&view=result&demo_state=result&task_id=SVC-20261015-014',
  '/service/chain-analysis?workspace=graph&tab=graph&industry=INB1701&eco_filter=orgs_and_actors&view=result&demo_state=result&task_id=SVC-20260915-014',
];
const OUT = { probed_at: new Date().toISOString(), base: BASE, entry: 'mode2-result' };
const dump = (n, d) => { fs.writeFileSync(path.join(__dirname, n), JSON.stringify(d, null, 2), 'utf8'); };
const safe = async (fn) => { try { return await fn(); } catch (e) { return { err: String((e && e.message) || e).slice(0, 400) }; } };

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

async function scoutResult(page, deep) {
  await page.goto(BASE + deep, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2500);
  await closeBasket(page);
  const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  const titleHit = /服务生态关系图谱/.test(body);
  const hangHit = /当前 hang 无可见点边/.test(body);
  const radio = page.locator('main .arco-radio.arco-radio-checked').first();
  const radioText = ((await radio.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
  const mode2 = /②\s*机构\+关联主体/.test(radioText);
  const g6 = page.locator('[data-testid="svc-eco-g6-graph"]');
  const empty = page.locator('[data-testid="svc-eco-empty-canvas"]');
  const actor = page.locator('[data-testid="svc-eco-actor-summary"]');
  const drawer = page.locator('.arco-drawer');
  const g6Count = await g6.count();
  const emptyVisible = (await empty.count()) ? await empty.first().isVisible().catch(() => false) : false;
  const actorVisible = (await actor.count()) ? await actor.first().isVisible().catch(() => false) : false;
  const drawerVisible = (await drawer.count()) ? await drawer.first().isVisible().catch(() => false) : false;
  let aria = null;
  let canvasBox = null;
  let clickAttempt = { attempted: false };
  if (g6Count) {
    const canvas = g6.first().locator('.svc-eco-relation-graph__canvas, [role="img"]').first();
    aria = await canvas.getAttribute('aria-label').catch(() => null);
    canvasBox = await canvas.boundingBox().catch(() => null);
    if (canvasBox && canvasBox.width > 40 && canvasBox.height > 40) {
      clickAttempt.attempted = true;
      const cx = canvasBox.x + canvasBox.width / 2;
      const cy = canvasBox.y + canvasBox.height / 2;
      await page.mouse.click(cx, cy);
      await page.waitForTimeout(800);
      clickAttempt.actorAfterClick = await page.locator('[data-testid="svc-eco-actor-summary"]').first().isVisible().catch(() => false);
      clickAttempt.drawerAfterClick = await page.locator('.arco-drawer').first().isVisible().catch(() => false);
    }
  }
  return {
    deep,
    url: page.url().replace(BASE, ''),
    titleHit,
    hangHit,
    radioText,
    mode2,
    g6Count,
    emptyVisible,
    actorVisible,
    drawerVisible,
    aria,
    canvasBox,
    clickAttempt,
    body_head: body.slice(0, 420),
  };
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);

  OUT.candidates = [];
  let hit = null;
  for (const deep of MODE2_CANDIDATES) {
    const r = await safe(() => scoutResult(page, deep));
    OUT.candidates.push(r);
    if (!r.err && r.titleHit && r.mode2) {
      hit = r;
      break;
    }
  }

  if (!hit) {
    OUT.fresh = await safe(async () => {
      await page.goto(BASE + '/service/chain-analysis?workspace=graph&tab=graph', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(1500);
      await closeBasket(page);
      const sel = page.locator('.industry-catalog-select').first();
      await sel.click({ timeout: 8000 });
      await page.waitForTimeout(400);
      await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
      await page.waitForTimeout(600);
      await page.getByText('② 机构+关联主体', { exact: true }).first().click({ timeout: 8000 });
      await page.waitForTimeout(400);
      const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
      await start.click({ timeout: 8000 });
      await page.waitForTimeout(2000);
      const viewBtn = page.getByRole('button', { name: /查看结果/ }).first();
      for (let i = 0; i < 60; i++) {
        if ((await viewBtn.count()) && (await viewBtn.isVisible().catch(() => false)) && (await viewBtn.isEnabled().catch(() => false))) {
          await viewBtn.click({ timeout: 5000 });
          break;
        }
        await page.waitForTimeout(1000);
      }
      await page.waitForTimeout(2500);
      const u = page.url();
      const m = /task_id=([^&]+)/.exec(u);
      const taskId = m ? decodeURIComponent(m[1]) : null;
      const deep = u.replace(BASE, '');
      const scout = await scoutResult(page, deep);
      return { taskId, deep, scout };
    });
    if (OUT.fresh && OUT.fresh.scout && !OUT.fresh.scout.err) hit = OUT.fresh.scout;
  }

  OUT.result = hit || (OUT.candidates[0] || { err: 'no_mode2_result' });
  await page.screenshot({ path: path.join(__dirname, '_probe-p011-result.png'), fullPage: false }).catch(() => {});

  OUT.conclusion = (() => {
    const r = OUT.result || {};
    if (r.err) return 'probe_error: ' + r.err;
    if (!r.mode2) return 'P0-11 写前探针：未落到模式②结果壳（radio=' + (r.radioText || '') + '）';
    if (r.hangHit && r.g6Count === 0) {
      return 'P0-11 写前探针：模式②结果壳在 + hang 空 + g6Count=0 → 无关联主体节点可点，侧栏摘要不可达（B 档 allow_skip + ENV-SVCGRAPH-HANG-EMPTY-001）';
    }
    if (r.clickAttempt && r.clickAttempt.attempted) {
      return 'P0-11 写前探针：画布可点 actorAfterClick=' + r.clickAttempt.actorAfterClick + ' drawerAfterClick=' + r.clickAttempt.drawerAfterClick;
    }
    return 'P0-11 写前探针：模式②结果壳可达但关联主体节点不足（见 result）';
  })();

  dump('_probe-p011.json', OUT);
  console.log(JSON.stringify({ conclusion: OUT.conclusion, mode2: !!(OUT.result && OUT.result.mode2), g6Count: OUT.result && OUT.result.g6Count, hangHit: OUT.result && OUT.result.hangHit }, null, 2));
  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
