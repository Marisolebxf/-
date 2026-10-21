#!/usr/bin/env node
/**
 * P0-27（FUNC-00719 中心性 TOP5 统计）写前探针：
 * fresh 首发（新一代信息技术+模式②）→「查看结果」落结果态 → 只读勘察统计面板
 * 「度中心性 TOP5」区实际形态，为父单落局预判四分支（①诚实空态 ②伪排行 ③结构缺失
 * ④其他诚实形态）定证据。观察：TOP5 卡结构 / 列表行与度数 / 空态文案 / 规模行 N/E /
 * 机构名按钮（.svc-eco-org-link）/ 评审层 requirement_trace 角标。
 * 公约：独立无头；产物只进本目录（_probe-p027.json + _probe-p027-result.png）。
 * fresh 起任务属父单授权链路（env-gate g2b / P0-19b / P0-22~26 同款），POST 仅 1 次。
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
const OUT = { probed_at: new Date().toISOString(), base: BASE };
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

  // 1) fresh 首发（P0-25/26 r1 实证链路）
  OUT.fresh_start = await safe(async () => {
    await page.goto(BASE + '/service/chain-analysis?workspace=graph&tab=graph', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1500);
    await closeBasket(page);
    const sel = page.locator('.industry-catalog-select').first();
    await sel.click({ timeout: 8000 });
    await page.waitForTimeout(600);
    await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
      .filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
    await page.waitForTimeout(800);
    await page.getByText('② 机构+关联主体', { exact: true }).first().click({ timeout: 8000 });
    await page.waitForTimeout(600);
    const radio1 = page.locator('main .arco-radio.arco-radio-checked').first();
    if (!/②/.test((await radio1.innerText().catch(() => '')) || '')) throw new Error('模式②未选中');
    const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
    if (!(await start.isEnabled())) throw new Error('合法条件后开始分析不可点');
    await start.click({ timeout: 8000 });
    await page.waitForURL((u) => /view=(processing|result)/.test(String(u)), { timeout: 15000 });
    let body = '';
    for (let i = 0; i < 10; i++) {
      body = await mainText(page);
      if (/分析结果已生成|服务生态关系图谱/.test(body)) break;
      await page.waitForTimeout(1000);
    }
    const mA = /task_id=(SVC-[0-9-]+)/.exec(page.url());
    return { taskId: mA ? mA[1] : null, guided_done: /分析结果已生成/.test(body), url: page.url().replace(BASE, '') };
  });

  // 2) 查看结果落结果态
  OUT.view_result = await safe(async () => {
    if (!/view=result/.test(page.url())) {
      const vr = page.getByRole('button', { name: '查看结果', exact: true }).first();
      await vr.click({ timeout: 8000 });
      await page.waitForTimeout(2600);
    }
    await closeBasket(page);
    const u = page.url().replace(BASE, '');
    const b = await mainText(page);
    return { url: u, has_shell: /服务生态关系图谱/.test(b) };
  });

  // 3) TOP5 区形态勘察（只读）
  OUT.top5_shape = await safe(async () => {
    const panel = page.locator('section[data-testid="svc-eco-stats-panel"]').first();
    const panelVisible = await panel.isVisible().catch(() => false);
    const card = panel.locator('.svc-eco-stat').filter({ hasText: '度中心性 TOP5' }).first();
    const cardCount = await card.count();
    const cardVisible = cardCount ? await card.first().isVisible().catch(() => false) : false;
    const h3 = cardCount ? ((await card.locator('h3').first().innerText().catch(() => '')) || '') : '';
    const ul = card.locator('ul[data-testid="svc-eco-centrality-top"]').first();
    const ulCount = await ul.count();
    const rows = ul.locator('li.svc-eco-stat-row');
    const rowCount = await rows.count();
    const rowTexts = [];
    for (let i = 0; i < rowCount; i++) {
      const t = ((await rows.nth(i).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
      const btn = rows.nth(i).locator('button.svc-eco-org-link');
      const btnCount = await btn.count();
      const aria = btnCount ? ((await btn.first().getAttribute('aria-label')) || '') : '';
      rowTexts.push({ text: t, linkBtn: btnCount > 0, aria });
    }
    const emptyNote = card.locator('p.svc-eco-note').first();
    const emptyTxt = (await emptyNote.count()) ? ((await emptyNote.innerText().catch(() => '')) || '').trim() : null;
    const sizeTxt = (((await panel.locator('strong[data-testid="svc-eco-visible-size"]').first().innerText().catch(() => '')) || '')).trim();
    const cardTxt = cardCount ? ((await card.first().innerText().catch(() => '')) || '').replace(/\n/g, ' | ').slice(0, 300) : '';
    // 评审层 requirement_trace 角标（TOP5 h3 挂点，与业务列表互斥不扰）
    const traceBadge = card.locator('.metric-spec-card, [class*="requirement" i], [class*="trace" i]');
    const traceCount = await traceBadge.count();
    let branch = 'unknown';
    if (!cardCount || !cardVisible) branch = 'missing(③结构缺失)';
    else if (rowCount > 0 && /\/(\d+)/.test(sizeTxt) && RegExp.$1 === '0') branch = 'fabricated(②伪排行-子网空却有行)';
    else if (rowCount > 0) branch = 'list(有数据)';
    else if (emptyTxt && /当前子网无服务机构/.test(emptyTxt)) branch = 'honest_empty(①诚实空态)';
    else if (emptyTxt) branch = 'other_honest(④其他形态:' + emptyTxt.slice(0, 40) + ')';
    else branch = 'none_branch(无列表无空态文案)';
    return {
      panel_visible: panelVisible, card_count: cardCount, card_visible: cardVisible, h3,
      ul_count: ulCount, row_count: rowCount, rows: rowTexts.slice(0, 8),
      empty_note: emptyTxt, size_row: sizeTxt, card_text_head: cardTxt,
      trace_badge_count: traceCount, branch,
    };
  });

  // 4) 结果态整卡截图（证据）
  await safe(async () => {
    const panel = page.locator('section[data-testid="svc-eco-stats-panel"]').first();
    await panel.scrollIntoViewIfNeeded().catch(() => {});
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(__dirname, '_probe-p027-result.png'), fullPage: false });
  });

  OUT.conclusion = 'P0-27 写前探针完成：TOP5 分支=' + (OUT.top5_shape && OUT.top5_shape.branch) + '（详见 top5_shape；供 cases/P0-27.yaml 落局分支判定）';
  dump('_probe-p027.json', OUT);
  await browser.close();
  process.exit(0);
})();
