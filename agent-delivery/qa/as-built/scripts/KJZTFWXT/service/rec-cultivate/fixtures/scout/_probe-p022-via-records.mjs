// probe-p022-via-records.mjs — P0-22 备选实勘：经分析记录打开既有已完成任务结果态
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://10.50.69.111:30892/';
const target = baseUrl + 'service/institution-decision?workspace=cultivate&tab=cultivate';
const out = {
  probed_at: new Date().toISOString(),
  entry: 'svc-rec-cultivate',
  purpose: 'P0-22 / FUNC-01276 via records view-result',
  steps: [],
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
  if (page.url().includes('/login')) {
    await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
    await page.locator('input[type=password]').first().fill('123456');
    await page.getByRole('button', { name: /登录/ }).first().click();
    await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
    out.steps.push('login ok');
  }
  await page.goto(target, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2200);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) await close.first().click().catch(() => {});

  // 切分析记录
  const recTab = page.locator('[data-tab-key="records"], [role=tab]').filter({ hasText: '分析记录' }).first();
  await recTab.click({ timeout: 8000 });
  await page.waitForTimeout(2000);
  // 列表偶发空 → reload 兜底
  let body = (await page.locator('main').first().innerText().catch(() => '')) || '';
  if (/暂无分析记录/.test(body)) {
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2500);
    await recTab.click({ timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(1500);
    body = (await page.locator('main').first().innerText().catch(() => '')) || '';
  }
  out.records_body_head = body.split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 25);

  const viewBtns = page.getByRole('button', { name: '查看结果', exact: true });
  out.view_result_count = await viewBtns.count();
  if (!out.view_result_count) throw new Error('记录 Tab 无「查看结果」');

  // 跳过失败行 disabled 按钮，点首个 enabled「查看结果」
  let clicked = false;
  const n = out.view_result_count;
  for (let i = 0; i < n; i++) {
    const btn = viewBtns.nth(i);
    if (await btn.isEnabled().catch(() => false)) {
      await btn.click({ timeout: 8000 });
      clicked = true;
      out.clicked_view_result_index = i;
      break;
    }
  }
  if (!clicked) throw new Error('记录 Tab 无 enabled「查看结果」');
  await page.waitForURL((u) => /[?&]view=result/.test(String(u)), { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2500);
  out.result_url = page.url();
  const m = out.result_url.match(/[?&]task_id=(SVC-\d{8}-\d{1,4})/);
  out.task_id = m ? m[1] : null;

  const main = (await page.locator('main').first().innerText().catch(() => '')) || '';
  out.result_body_head = main.split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 40);
  out.has_list_title = main.includes('本土机构培育名单');
  out.empty_hit = main.includes('暂无候选') && main.includes('当前筛选范围内无本土机构')
    ? '暂无候选+当前筛选范围内无本土机构'
    : (main.includes('暂无候选') ? '暂无候选' : (main.includes('当前筛选范围内无本土机构') ? '当前筛选范围内无本土机构' : ''));
  const LABEL_SET = ['资金支持', '市场对接', '人才引进'];
  out.label_hits_in_body = LABEL_SET.filter((t) => main.includes(t));

  const ORG = /公司|大学|学院|学校|研究所|研究院|医院|中心/;
  const rowsLoc = page.locator('main .arco-table-tr, main [role=row], main tr').filter({ hasText: ORG });
  let rows = 0;
  for (let i = 0; i < 8; i++) {
    rows = await rowsLoc.count();
    if (rows > 0) break;
    await page.waitForTimeout(800);
  }
  out.list_rows = rows;
  out.branch = rows > 0 ? 'non-empty' : (out.empty_hit ? 'honest-empty' : 'unknown');

  if (rows > 0) {
    out.rows = [];
    const n = Math.min(rows, 3);
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
    out.table_head = ((await page.locator('main .arco-table-th, main th').allInnerTexts().catch(() => [])) || []).join('||');
  }

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
      ? '诚实空：建议深验不可达，脚本走双分支无据 pass'
      : '未知态');
} catch (e) {
  out.error = String(e && e.stack || e);
} finally {
  await browser.close();
}
const outPath = path.join(__dirname, 'scout-p022-suggest.json');
fs.writeFileSync(outPath, JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
console.log('wrote', outPath);
