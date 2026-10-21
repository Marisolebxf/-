#!/usr/bin/env node
/**
 * P0-09（FUNC-00715 结果态画布拖拽/缩放/平移）写前探针：
 * 历史种子「查看结果」深链（SVC-20260903-001，0 POST）落结果态后只读勘察：
 * ① 结果壳标题在屏；hang 空文案在否
 * ② G6 容器 svc-eco-g6-graph / 图例 svc-eco-graph-legend / 空画布 svc-eco-empty-canvas
 * ③ canvas 节点数（aria-label「N 个节点」）与 wheel/drag 是否可改变 view transform
 * 公约：独立无头；产物只进本目录（_probe-p009.json + _probe-p009-result.png）。0 POST。
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
const DEEP = '/service/chain-analysis?workspace=graph&tab=records&view=result&demo_state=result&task_id=SVC-20260903-001';
const OUT = { probed_at: new Date().toISOString(), base: BASE, entry: 'deep-link SVC-20260903-001' };
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

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);

  OUT.result = await safe(async () => {
    await page.goto(BASE + DEEP, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2500);
    await closeBasket(page);
    const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
    const titleHit = /服务生态关系图谱/.test(body);
    const hangHit = /当前 hang 无可见点边/.test(body);
    const investVisible = await page.getByText('投资', { exact: true }).first().isVisible().catch(() => false);
    const g6 = page.locator('[data-testid="svc-eco-g6-graph"]');
    const legend = page.locator('[data-testid="svc-eco-graph-legend"]');
    const empty = page.locator('.svc-eco-empty-canvas, [data-testid="svc-eco-empty-canvas"]');
    const g6Count = await g6.count();
    const legendCount = await legend.count();
    const emptyCount = await empty.count();
    const emptyVisible = emptyCount ? await empty.first().isVisible().catch(() => false) : false;
    let aria = null;
    let canvasBox = null;
    let canvasKids = 0;
    if (g6Count) {
      const canvas = g6.first().locator('.svc-eco-relation-graph__canvas, [role="img"]').first();
      aria = await canvas.getAttribute('aria-label').catch(() => null);
      canvasBox = await canvas.boundingBox().catch(() => null);
      canvasKids = await canvas.locator('canvas, svg, canvas + *').count().catch(() => 0);
    }
    // 尝试 wheel/drag：仅当有可交互画布框；记录前后 transform 代理（g 节点 / canvas 存在）
    let interact = { attempted: false };
    if (canvasBox && canvasBox.width > 40 && canvasBox.height > 40) {
      interact.attempted = true;
      const before = await page.evaluate(() => {
        const root = document.querySelector('[data-testid="svc-eco-g6-graph"]');
        const g = root && root.querySelector('g');
        const c = root && root.querySelector('canvas');
        return {
          g_transform: g ? g.getAttribute('transform') : null,
          has_canvas: !!c,
          canvas_w: c ? c.width : 0,
          canvas_h: c ? c.height : 0,
        };
      });
      const cx = canvasBox.x + canvasBox.width / 2;
      const cy = canvasBox.y + canvasBox.height / 2;
      await page.mouse.move(cx, cy);
      await page.mouse.wheel(0, -120);
      await page.waitForTimeout(400);
      const afterWheel = await page.evaluate(() => {
        const root = document.querySelector('[data-testid="svc-eco-g6-graph"]');
        const g = root && root.querySelector('g');
        return { g_transform: g ? g.getAttribute('transform') : null };
      });
      await page.mouse.move(cx, cy);
      await page.mouse.down();
      await page.mouse.move(cx + 80, cy + 40, { steps: 8 });
      await page.mouse.up();
      await page.waitForTimeout(400);
      const afterDrag = await page.evaluate(() => {
        const root = document.querySelector('[data-testid="svc-eco-g6-graph"]');
        const g = root && root.querySelector('g');
        return { g_transform: g ? g.getAttribute('transform') : null };
      });
      interact = {
        attempted: true,
        before,
        afterWheel,
        afterDrag,
        zoom_moved: before.g_transform !== afterWheel.g_transform,
        pan_moved: afterWheel.g_transform !== afterDrag.g_transform,
      };
    }
    await page.screenshot({ path: path.join(__dirname, '_probe-p009-result.png'), fullPage: false });
    return {
      url: page.url().replace(BASE, ''),
      titleHit,
      hangHit,
      investVisible,
      g6Count,
      legendCount,
      emptyCount,
      emptyVisible,
      aria,
      canvasBox,
      canvasKids,
      interact,
      body_head: body.slice(0, 420),
    };
  });

  OUT.conclusion = (() => {
    const r = OUT.result || {};
    if (r.err) return 'probe_error: ' + r.err;
    if (r.hangHit && !r.investVisible) {
      return 'P0-09 写前探针：结果壳在 + hang 空文案在屏 + 图例「投资」不可见 → 拖拽/缩放/平移无可探索对象（B 档 allow_skip + ENV-SVCGRAPH-HANG-EMPTY-001）';
    }
    if (r.interact && r.interact.attempted) {
      return 'P0-09 写前探针：画布可交互尝试 zoom_moved=' + r.interact.zoom_moved + ' pan_moved=' + r.interact.pan_moved;
    }
    return 'P0-09 写前探针：结果壳可达但画布交互对象不足（见 result）';
  })();

  dump('_probe-p009.json', OUT);
  console.log(JSON.stringify({ conclusion: OUT.conclusion, result_keys: Object.keys(OUT.result || {}) }, null, 2));
  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
