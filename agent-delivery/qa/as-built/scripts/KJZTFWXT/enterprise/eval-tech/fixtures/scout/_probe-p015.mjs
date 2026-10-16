#!/usr/bin/env node
/** P0-15 写稿一次性无头实勘：结果态「技术力加权排名」区块标题/表序/升序入口 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);

const out = { surveyed_at: new Date().toISOString(), url_initial: page.url() };

const closeB = page.locator('button[aria-label="关闭对比篮"]');
if (await closeB.count() && await closeB.first().isVisible().catch(() => false) && await closeB.first().isEnabled().catch(() => false)) {
  try { await closeB.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
}
// 优先浮层回填；篮空则走「最近评估」打开已有结果（写稿实勘口径，脚本正式链仍先现场发起）
let branch = null;
const openBtn = page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first();
if (await openBtn.isVisible().catch(() => false)) {
  try {
    await openBtn.click({ timeout: 8000 });
    const sels = page.locator('[aria-label^="选择 "]');
    await sels.first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(800);
    const n = await sels.count();
    out.basket_count = n;
    if (n >= 2) {
      await sels.nth(0).click();
      await sels.nth(1).click();
      await page.waitForTimeout(500);
      const okBtn = page.getByRole('button', { name: '确定' }).first();
      await okBtn.scrollIntoViewIfNeeded().catch(() => {});
      await okBtn.click({ timeout: 10000 });
      await page.waitForTimeout(2500);
      const start = page.getByRole('button', { name: '开始分析' });
      out.start_disabled = await start.isDisabled();
      if (!out.start_disabled) {
        await start.click();
        const bodyRes = async () => {
          const t = await page.locator('body').innerText().catch(() => '');
          return /技术力评估结果/.test(t) && /\d+\s*分/.test(t);
        };
        const t0 = Date.now();
        while (Date.now() - t0 < 5000) {
          const procEl = page.getByText(/技术力评估生成中|可视化分析过程/).first();
          if (await procEl.isVisible().catch(() => false)) { branch = 'processing'; break; }
          if (/view=result/.test(page.url())) { branch = 'result'; break; }
          await page.waitForTimeout(300);
        }
        if (branch !== 'result') {
          const t1 = Date.now();
          while (Date.now() - t1 < 60000) {
            if (/view=result/.test(page.url())) { branch = 'result'; break; }
            if (await bodyRes()) { branch = 'inplace'; break; }
            await page.waitForTimeout(1000);
          }
        }
      } else {
        out.precheck = (await page.locator('body').innerText()).includes('预检未返回企业明细');
      }
    } else {
      // 关浮层
      const cancel = page.getByRole('button', { name: '取消' }).first();
      if (await cancel.isVisible().catch(() => false)) try { await cancel.click({ timeout: 2000 }); } catch {}
    }
  } catch (e) {
    out.open_err = String(e && e.message || e).slice(0, 120);
  }
}
if (branch !== 'result' && branch !== 'inplace') {
  const tab = page.getByRole('tab', { name: /最近评估/ }).first();
  if (await tab.isVisible().catch(() => false)) {
    try { await tab.click({ timeout: 3000 }); await page.waitForTimeout(1500); } catch {}
  }
  const tid = (/EVAL-\d{8}-\d{3}/.exec(await page.locator('body').innerText().catch(() => '')) || [])[0];
  out.fallback_tid = tid || null;
  if (!tid) {
    fs.writeFileSync(path.join(__dirname, 'probe-p015.json'), JSON.stringify(out, null, 2), 'utf8');
    console.log(JSON.stringify({ blocked: true, reason: '无结果态可达', ...out }, null, 2));
    await browser.close();
    process.exit(0);
  }
  await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology&view=result&analysis_type=technology&task_id=' + tid, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  branch = 'result_via_recent';
}
out.branch = branch;
out.url = page.url();
await page.waitForTimeout(2000);
await page.screenshot({ path: path.join(__dirname, 'result-rank.png'), fullPage: true });

const body = await page.locator('body').innerText();
out.hits = {
  rank_title_lines: (body.match(/[^\n]*排名[^\n]*/g) || []).slice(0, 8),
  score_col: body.includes('技术力综合得分'),
  enterprise_col: /\n企业\n/.test(body) || body.includes('企业\t'),
  has_asc_btn: !!(await page.getByRole('button', { name: /升序|降序|排序/ }).count()),
  has_sort_trigger: !!(await page.locator('[aria-label*="排序"], [aria-label*="升序"], [aria-label*="降序"]').count()),
};

out.rank_block = await page.evaluate(() => {
  const body = document.body.innerText || '';
  const own = (w) =>
    [...document.querySelectorAll('*')].find((e) => [...e.childNodes].some((c) => c.nodeType === 3 && String(c.textContent).includes(w))) ||
    [...document.querySelectorAll('*')].find((e) => e.children.length === 0 && (e.textContent || '').includes(w));
  const t = own('技术力加权排名') || own('技术力排名');
  if (!t) return { found: false, body_has_rank: /技术力加权排名|技术力排名/.test(body) };
  // 向上找含 canvas 的区块；再扩一层拿兄弟表（诊断表常紧邻排名图）
  let b = t;
  for (let i = 0; i < 12 && b; i++) {
    b = b.parentElement;
    if (b && b.querySelector('canvas')) break;
  }
  let section = b;
  for (let i = 0; i < 4 && section; i++) {
    section = section.parentElement;
    if (section && (section.querySelector('table') || section.querySelector('.arco-table'))) break;
  }
  const text = (section || b || t).innerText || '';
  const table = (section || b) && ((section || b).querySelector('table') || (section || b).querySelector('.arco-table'));
  const rows = [];
  if (table) {
    const trs = [...table.querySelectorAll('tbody tr, .arco-table-body .arco-table-tr, .arco-table-tr')];
    for (const tr of trs.slice(0, 10)) {
      if (tr.classList.contains('arco-table-header')) continue;
      const cells = [...tr.querySelectorAll('td, .arco-table-td')].map((c) => (c.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 80));
      if (cells.some((c) => c) && !cells[0]?.includes('技术力综合得分')) rows.push(cells);
    }
  }
  // 名次+得分：表首列企业名 + 综合得分列；或正文「公司\\n得分」序列
  const cosFromRows = rows
    .map((cells) => {
      const name = cells.find((c) => /公司|集团/.test(c)) || cells[0];
      const scoreCell = cells.find((c, idx) => idx > 0 && /^\d{1,3}$/.test(c));
      return name && scoreCell ? { name: name.slice(0, 40), score: Number(scoreCell) } : null;
    })
    .filter(Boolean);
  const cosFromBody = [...body.matchAll(/([\u4e00-\u9fffA-Za-z0-9]+(?:公司|集团))\n(\d{1,3})\n/g)].map((m) => ({ name: m[1], score: Number(m[2]) }));
  const cos = cosFromRows.length >= 2 ? cosFromRows : cosFromBody;
  const scores = cos.map((c) => c.score);
  const desc = scores.length >= 2 && scores.every((s, i) => i === 0 || scores[i - 1] >= s);
  const iRank = body.indexOf('技术力加权排名');
  const iGap = body.indexOf('技术指标与差距诊断');
  return {
    found: true,
    title: (t.textContent || '').trim().slice(0, 40),
    rank_slice: iRank >= 0 ? body.slice(iRank, (iGap > iRank ? iGap : iRank + 200)).slice(0, 200) : '',
    has_table: !!table,
    has_canvas: !!(b && b.querySelector('canvas')),
    rows: rows.slice(0, 6),
    company_scores: cos.slice(0, 6),
    scores_desc: desc,
    count_hint: (body.match(/\d+\s*家企业/) || [])[0] || null,
    rank_word_hits: (body.match(/[^\n]*排名[^\n]*/g) || []).slice(0, 6),
  };
});

fs.writeFileSync(path.join(__dirname, 'probe-p015.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify({ branch: out.branch, hits: out.hits, rank_block: out.rank_block }, null, 2));
await browser.close();
