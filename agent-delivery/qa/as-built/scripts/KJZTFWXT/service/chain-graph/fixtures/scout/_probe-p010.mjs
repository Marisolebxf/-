#!/usr/bin/env node
/**
 * P0-10（FUNC-00716 机构节点下钻画像抽屉）写前探针：
 * 历史种子「查看结果」深链（SVC-20260903-001，0 POST）落结果态后只读勘察：
 * ① 结果壳标题在屏；hang 空文案在否
 * ② G6 容器 svc-eco-g6-graph / 空画布 svc-eco-empty-canvas
 * ③ .arco-drawer 是否已开；画布框是否可点（无框则不可下钻）
 * 公约：独立无头；产物只进本目录。0 POST。
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
    const g6 = page.locator('[data-testid="svc-eco-g6-graph"]');
    const empty = page.locator('[data-testid="svc-eco-empty-canvas"]');
    const drawer = page.locator('.arco-drawer');
    const g6Count = await g6.count();
    const emptyVisible = (await empty.count()) ? await empty.first().isVisible().catch(() => false) : false;
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
        clickAttempt.drawerAfterClick = await page.locator('.arco-drawer').first().isVisible().catch(() => false);
      }
    }
    await page.screenshot({ path: path.join(__dirname, '_probe-p010-result.png'), fullPage: false });
    return {
      url: page.url().replace(BASE, ''),
      titleHit,
      hangHit,
      g6Count,
      emptyVisible,
      drawerVisible,
      aria,
      canvasBox,
      clickAttempt,
      body_head: body.slice(0, 420),
    };
  });

  OUT.conclusion = (() => {
    const r = OUT.result || {};
    if (r.err) return 'probe_error: ' + r.err;
    if (r.hangHit && r.g6Count === 0) {
      return 'P0-10 写前探针：结果壳在 + hang 空 + g6Count=0 → 无服务机构节点可点，画像抽屉下钻不可达（B 档 allow_skip + ENV-SVCGRAPH-HANG-EMPTY-001）';
    }
    if (r.clickAttempt && r.clickAttempt.attempted) {
      return 'P0-10 写前探针：画布可点 drawerAfterClick=' + r.clickAttempt.drawerAfterClick;
    }
    return 'P0-10 写前探针：结果壳可达但机构节点下钻对象不足（见 result）';
  })();

  dump('_probe-p010.json', OUT);
  console.log(JSON.stringify({ conclusion: OUT.conclusion, result_keys: Object.keys(OUT.result || {}) }, null, 2));
  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
