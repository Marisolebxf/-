#!/usr/bin/env node
/**
 * P0-30（FUNC-00729 异常-过滤后空结果提示）写前探针：
 * 历史种子「查看结果」深链（SVC-20260903-001，0 POST，P0-28 同款入口）落结果态后只读勘察：
 * ① 过滤区可达性（svc-eco-clip-filters / node-kinds / edge-types）——源码链 v-if="!parsed.empty"
 *    预判 hang 空不渲染，实证定局（预期复现 P0-28 filters_count=0）
 * ② 空态文案承载勘察：clip-empty 容器（「当前过滤条件下无关系数据」）当前态 vs
 *    hang 空文案（「当前 hang 无可见点边」）——hang 空下 clipEmpty 分支不可达应只见后者
 * ③ 统计位在场性（规模行/密度位，转实后「统计位不 NaN」检查锚点）
 * 公约：独立无头；产物只进本目录（_probe-p030.json + _probe-p030-result.png）。0 POST 不触发共享账号噪声。
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
const OUT = { probed_at: new Date().toISOString(), base: BASE, entry: 'deep-link SVC-20260903-001（P0-28 同款历史种子）' };
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
async function mainText(page) { return ((await page.locator('main').first().innerText().catch(() => '')) || ''); }

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);

  // 1) 历史种子深链落结果态（P0-28 同款 0 POST 入口）
  OUT.deep_link = await safe(async () => {
    await page.goto(BASE + '/service/chain-analysis?workspace=graph&tab=graph&view=result&demo_state=result&task_id=SVC-20260903-001', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);
    await closeBasket(page);
    const b = await mainText(page);
    return { url: page.url().replace(BASE, ''), has_shell: /服务生态关系图谱/.test(b) };
  });

  // 2) 过滤区可达性 + 空态承载勘察（只读）
  OUT.empty_hint_shape = await safe(async () => {
    const filters = page.locator('[data-testid="svc-eco-clip-filters"]').first();
    const filtersCount = await filters.count();
    const filtersVisible = filtersCount ? await filters.isVisible().catch(() => false) : false;
    const nodeGroup = await page.locator('[data-testid="svc-eco-clip-node-kinds"]').count();
    const edgeGroup = await page.locator('[data-testid="svc-eco-clip-edge-types"]').count();
    const clipEmptyEl = page.locator('[data-testid="svc-eco-clip-empty"]').first();
    const clipEmptyCount = await clipEmptyEl.count();
    const clipEmptyVisible = clipEmptyCount ? await clipEmptyEl.isVisible().catch(() => false) : false;
    const b = await mainText(page);
    const clipEmptyCopyHit = /当前过滤条件下无关系数据/.test(b);
    const hangEmptyCopyHit = /当前 hang 无可见点边/.test(b);
    return {
      branch: filtersCount && filtersVisible ? 'present(过滤控件在)' : 'missing(过滤控件结构性不渲染)',
      filters_count: filtersCount, filters_visible: filtersVisible,
      node_group_count: nodeGroup, edge_group_count: edgeGroup,
      clip_empty_el_count: clipEmptyCount, clip_empty_el_visible: clipEmptyVisible,
      clip_empty_copy_hit: clipEmptyCopyHit, hang_empty_copy_hit: hangEmptyCopyHit,
    };
  });

  // 3) 统计位在场性（规模行/密度位 + 统计范围声明——转实后「统计位不 NaN」检查锚点）
  OUT.stats_shape = await safe(async () => {
    const sizeEl = page.locator('strong[data-testid="svc-eco-visible-size"]').first();
    const sizeCount = await sizeEl.count();
    const sizeTxt = sizeCount ? (((await sizeEl.innerText().catch(() => '')) || '').replace(/\s+/g, '')) : null;
    const densEl = page.locator('strong[data-testid="svc-eco-visible-density"]').first();
    const densCount = await densEl.count();
    const densTxt = densCount ? (((await densEl.innerText().catch(() => '')) || '').trim()) : null;
    const b = await mainText(page);
    return {
      size_row_count: sizeCount, size_row_text: sizeTxt,
      density_row_count: densCount, density_row_text: densTxt,
      density_is_nan_like: densTxt ? /NaN|undefined|null|Infinity/i.test(densTxt) : null,
      stat_range_copy_hit: /统计范围\s*=\s*当前过滤后的可见子网/.test(b),
    };
  });

  // 4) 结果态截图（证据）
  await safe(async () => {
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(__dirname, '_probe-p030-result.png'), fullPage: false });
  });

  OUT.conclusion = 'P0-30 写前探针完成：过滤区分支=' + (OUT.empty_hint_shape && OUT.empty_hint_shape.branch)
    + '；clip-empty 空态承载当前 ' + (OUT.empty_hint_shape && OUT.empty_hint_shape.clip_empty_copy_hit ? '在屏' : '不在屏（hang 空下 clipEmpty 分支不可达）')
    + '（详见 empty_hint_shape；供 cases/P0-30.yaml 落局分支判定）';
  dump('_probe-p030.json', OUT);
  await browser.close();
  process.exit(0);
})();
