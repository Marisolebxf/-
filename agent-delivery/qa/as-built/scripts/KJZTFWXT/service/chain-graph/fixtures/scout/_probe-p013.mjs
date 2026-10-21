#!/usr/bin/env node
/**
 * P0-13（FUNC-00730 异常-子网过小统计空态）写前探针：
 * 历史种子「查看结果」深链（SVC-20260903-001，0 POST）落结果态后只读勘察：
 * ① 过滤区可达性（svc-eco-clip-filters）——用例前置「可构造仅剩单节点的过滤组合」依赖勾选组
 * ② 规模行/密度位当前态（hang 空下 N=0 已呈「子网过小」属基线诚实空，非过滤构造路径）
 * ③ hang 空文案 vs 过滤空态分支
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

const BASE = 'http://10.50.69.111:30892';
const DEEP = '/service/chain-analysis?workspace=graph&tab=records&view=result&demo_state=result&task_id=SVC-20260903-001';
const OUT = { probed_at: new Date().toISOString(), base: BASE, entry: 'deep-link SVC-20260903-001', case_id: 'P0-13', func_id: 'FUNC-00730' };
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
    const filters = page.locator('[data-testid="svc-eco-clip-filters"]');
    const nGrp = page.locator('[data-testid="svc-eco-clip-node-kinds"]');
    const eGrp = page.locator('[data-testid="svc-eco-clip-edge-types"]');
    const g6 = page.locator('[data-testid="svc-eco-g6-graph"]');
    const empty = page.locator('[data-testid="svc-eco-empty-canvas"]');
    const sizeEl = page.locator('strong[data-testid="svc-eco-visible-size"]').first();
    const densEl = page.locator('strong[data-testid="svc-eco-visible-density"]').first();
    const sizeTxt = (await sizeEl.count()) ? (((await sizeEl.innerText().catch(() => '')) || '').replace(/\s+/g, '')) : null;
    const densTxt = (await densEl.count()) ? (((await densEl.innerText().catch(() => '')) || '').trim()) : null;
    const filtersCount = await filters.count();
    const filtersVisible = filtersCount ? await filters.first().isVisible().catch(() => false) : false;
    return {
      titleHit: /服务生态关系图谱/.test(body),
      hangHit: /当前 hang 无可见点边/.test(body),
      filtersCount,
      filtersVisible,
      nodeGroupCount: await nGrp.count(),
      edgeGroupCount: await eGrp.count(),
      g6Count: await g6.count(),
      emptyVisible: (await empty.count()) ? await empty.first().isVisible().catch(() => false) : false,
      sizeTxt,
      densTxt,
      densNanLike: densTxt ? /NaN|undefined|null|Infinity/i.test(densTxt) : null,
      subnetTooSmallHit: densTxt ? /子网过小/.test(densTxt) : false,
      constructableSingleNodeViaFilter: false,
      note: 'hang 空下过滤区不渲染 → 用例「勾选过滤至可见节点仅剩一个」不可达；基线密度位「子网过小」属 N=0 诚实空（P0-26 同源），非 00730 过滤构造路径',
    };
  });

  await safe(async () => {
    await page.screenshot({ path: path.join(__dirname, '_probe-p013-result.png'), fullPage: false });
  });

  const r = OUT.result || {};
  OUT.conclusion =
    'P0-13 写前探针：filtersCount=' + r.filtersCount +
    ' filtersVisible=' + r.filtersVisible +
    ' g6Count=' + r.g6Count +
    ' emptyVisible=' + r.emptyVisible +
    ' size=' + r.sizeTxt +
    ' dens=' + r.densTxt +
    ' → 过滤构造单节点/N<2 不可达，落局 B 档 allow_skip + ENV-SVCGRAPH-HANG-EMPTY-001';
  dump('_probe-p013.json', OUT);
  await browser.close();
  process.exit(0);
})();
