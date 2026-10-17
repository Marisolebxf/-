// probe-p022-suggest.mjs — P0-22 / FUNC-01276 写稿前无头实勘
// 目的：结果态名单是否有据；有据则抓两行培育建议标签/文本；无据则记诚实空
import { chromium } from '/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration/agent-delivery/qa/as-built/tools/node_modules/playwright/index.mjs';
import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const BASE = 'http://111.198.38.90:50892';
const out = {
  probed_at: new Date().toISOString(),
  entry: 'svc-rec-cultivate',
  purpose: 'P0-22 / FUNC-01276 suggest-vs-org 1:1 observed',
  steps: [],
};

const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080, deviceScaleFactor: 1 } });
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  if (page.url().includes('/login')) {
    await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
    await page.locator('input[type=password]').first().fill('123456');
    await page.getByRole('button', { name: /登录/ }).first().click();
    await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
    out.steps.push('login ok');
  }

  await page.goto(BASE + '/service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2200);
  await page.waitForSelector('.industry-catalog-select', { timeout: 15000 });
  out.steps.push('config visible');
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if (await close.count() && await close.first().isVisible().catch(() => false)) {
    try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
  }

  // 选产业 + 开始分析
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(600);
  await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
    .filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  out.echo = ((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim();
  const start = page.getByRole('button', { name: '开始分析', exact: true });
  await start.first().click({ timeout: 8000 });
  let tid = null;
  let directResult = false;
  for (let i = 0; i < 15; i++) {
    await page.waitForTimeout(1000);
    const u = page.url();
    const m = u.match(/[?&]task_id=(SVC-\d{8}-\d{1,4})/);
    if (/[?&]view=processing/.test(u) && m) { tid = m[1]; break; }
    if (/[?&]view=result/.test(u) && m) { tid = m[1]; directResult = true; break; }
  }
  out.task_id = tid;
  out.direct_result = directResult;
  out.url_after_start = page.url();
  if (!tid) throw new Error('未进过程/结果态: ' + page.url());

  if (!directResult) {
    let pbody = '';
    for (let i = 0; i < 16; i++) {
      pbody = (await page.locator('main').first().innerText().catch(() => '')) || '';
      if (/分析结果已生成/.test(pbody)) break;
      await page.waitForTimeout(1000);
    }
    out.process_guide_seen = /分析结果已生成/.test(pbody);
    const vr = page.getByRole('button', { name: '查看结果', exact: true });
    out.view_result_btn_count = await vr.count();
    if (out.view_result_btn_count) {
      await vr.first().click({ timeout: 8000 });
      await page.waitForURL((u) => /[?&]view=result/.test(String(u)), { timeout: 12000 });
      await page.waitForTimeout(2500);
    }
  } else {
    out.process_guide_seen = false;
    out.view_result_btn_count = 0;
    await page.waitForTimeout(2500);
  }
  out.result_url = page.url();

  const body = (await page.locator('main').first().innerText().catch(() => '')) || '';
  out.result_body_head = body.split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 40);
  out.has_list_title = body.includes('本土机构培育名单');
  out.empty_hit = body.includes('暂无候选') && body.includes('当前筛选范围内无本土机构')
    ? '暂无候选+当前筛选范围内无本土机构'
    : (body.includes('暂无候选') ? '暂无候选' : (body.includes('当前筛选范围内无本土机构') ? '当前筛选范围内无本土机构' : ''));

  const LABEL_SET = ['资金支持', '市场对接', '人才引进'];
  out.label_hits_in_body = LABEL_SET.filter((t) => body.includes(t));

  const ORG = /公司|大学|学院|学校|研究所|研究院|医院|中心/;
  const rowsLoc = page.locator('main .arco-table-tr, main [role=row], main tr').filter({ hasText: ORG });
  let rows = 0;
  for (let i = 0; i < 10; i++) {
    rows = await rowsLoc.count();
    if (rows > 0) break;
    await page.waitForTimeout(800);
  }
  out.list_rows = rows;
  out.branch = rows > 0 ? 'non-empty' : (out.empty_hit ? 'honest-empty' : 'unknown');

  if (rows > 0) {
    const n = Math.min(rows, 5);
    out.rows = [];
    for (let i = 0; i < n; i++) {
      const t = ((await rowsLoc.nth(i).innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
      const cells = await rowsLoc.nth(i).locator('td, [role=cell]').allInnerTexts().catch(() => []);
      out.rows.push({
        i,
        text_head: t.slice(0, 280),
        cells: (cells || []).map((c) => String(c).replace(/\s+/g, ' ').trim().slice(0, 120)),
        label_hits: LABEL_SET.filter((lb) => t.includes(lb)),
      });
    }
    const head = ((await page.locator('main .arco-table-th, main th').allInnerTexts().catch(() => [])) || []).join('||');
    out.table_head = head;
  }

  // DOM 旁路：建议相关 class / tag
  out.suggest_dom = await page.evaluate(() => {
    const nodes = [...document.querySelectorAll('main [class*="suggest"], main [class*="advice"], main [class*="recommend"], main .arco-tag')];
    return nodes.slice(0, 30).map((el) => ({
      tag: el.tagName,
      cls: (el.className || '').toString().slice(0, 80),
      text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80),
    }));
  });

  out.conclusion = out.branch === 'non-empty'
    ? '有据：可写建议标签集合+逐行对应机检'
    : (out.branch === 'honest-empty'
      ? '诚实空：建议深验不可达，脚本走双分支无据 pass（勿假绿有据断言）'
      : '未知态：名单既无行也无诚实空文案');
} catch (e) {
  out.error = String(e && e.stack || e);
} finally {
  await browser.close();
}

const outPath = join(__dirname, 'scout-p022-suggest.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
console.log('wrote', outPath);
