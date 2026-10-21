#!/usr/bin/env node
/**
 * P0-22（FUNC-00723 变更条件重析）run 后只读探针（r3）：
 * 记录 Tab 直接点本轮两条任务（SVC-20261015-037 首发 / 038 重析）的「查看过程」按钮，
 * 抓前端按任务 targetParams 自构造的落地 URL（industry / analysis_fp / task_id）与过程页
 * 分析对象文本——不猜产业 code；再点「查看结果」判 038 结果态画布分支与残留复检。
 * 公约：独立无头；只读（记录行查看按钮），任务创建 POST 必须 0 次，否则中止。
 * 产物只进本目录（_probe-p022.json）。
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
const OUT = {};
const dump = (n, d) => { fs.writeFileSync(path.join(__dirname, n), JSON.stringify(d, null, 2), 'utf8'); };
const safe = async (fn) => { try { return await fn(); } catch (e) { return { err: String(e && e.message || e).slice(0, 300) }; } };

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
async function gotoRecords(page) {
  await page.goto(BASE + '/service/chain-analysis?workspace=graph&tab=graph', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2200);
  await closeBasket(page);
  const rec = page.locator('[role=tab][data-tab-key="records"]').or(page.getByRole('tab', { name: '分析记录', exact: true }));
  await rec.first().click({ timeout: 8000 });
  await page.waitForTimeout(2500);
  await closeBasket(page);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);

  let posts = 0;
  page.on('request', (r) => { if (r.method() === 'POST' && /\/topicAsync\/topic\/v1\/analysis\/tasks\/?(\?|$)/.test(r.url())) posts++; });

  const ids = ['SVC-20261015-037', 'SVC-20261015-038'];

  // 1) 逐条「查看过程」：抓前端自构造 URL + 分析对象
  OUT.view_process = {};
  for (const id of ids) {
    OUT.view_process[id] = await safe(async () => {
      await gotoRecords(page);
      const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: id }).first();
      if (!(await row.count())) throw new Error('记录行未见 ' + id);
      const vp = row.getByRole('button', { name: '查看过程', exact: true });
      await vp.first().click({ timeout: 8000 });
      await page.waitForTimeout(2400);
      await closeBasket(page);
      const u = page.url().replace(BASE, '');
      const b = await mainText(page);
      const m = /产业领域：([^\s\t（(]+)/.exec(b);
      return {
        url: u,
        industry_param: (/[?&]industry=([^&]+)/.exec(u) || [])[1] || null,
        analysis_fp: (/[?&]analysis_fp=([^&]+)/.exec(u) || [])[1] || null,
        industry_shown: m ? m[1] : null,
        done: /已完成|分析结果已生成/.test(b),
      };
    });
  }

  // 2) 038 重析任务「查看结果」：画布分支 + 残留复检
  OUT.result_branch = await safe(async () => {
    await gotoRecords(page);
    const row = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: 'SVC-20261015-038' }).first();
    const vr = row.getByRole('button', { name: '查看结果', exact: true });
    await vr.first().click({ timeout: 8000 });
    await page.waitForTimeout(2600);
    await closeBasket(page);
    const u = page.url().replace(BASE, '');
    const b = await mainText(page);
    const legend = await page.getByText('投资', { exact: true }).first().isVisible().catch(() => false);
    const honest = /无可见点边|子网过小|不计算统计值|无服务机构|不输出影响力评分/.exec(b);
    return {
      url: u,
      has_shell: /服务生态关系图谱/.test(b),
      legend_invest_visible: legend,
      honest_copy: honest ? honest[0] : null,
      branch: legend ? 'data' : (honest ? 'honest_empty' : 'none_detected'),
      stale: {
        old_industry_INB1701: /INB1701|产业领域：新一代信息技术/.test(u + b),
        old_task_037: /SVC-20261015-037/.test(u + b),
      },
    };
  });

  OUT.posts_total = posts;
  OUT.posts_guard_ok = posts === 0;
  dump('_probe-p022.json', OUT);
  await browser.close();
  process.exit(posts === 0 ? 0 : 3);
})();
