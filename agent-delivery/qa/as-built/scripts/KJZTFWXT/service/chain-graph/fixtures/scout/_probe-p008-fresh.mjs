#!/usr/bin/env node
/**
 * P0-08（FUNC-00714 模式①/②节点构成差异）写前一次性无头短探：
 *  A) 3 条历史任务逐条结果深链 → 图谱滤镜 radio 选中态（找模式②任务）+ 三类主体图例可见性
 *  B) fresh 起一次模式②分析（新一代信息技术 + ② 机构+关联主体 → 开始分析 → 查看结果）
 *     → 结果壳 hang 空？「企业/高校/资本」图例是否渲染？（ENV-SVCGRAPH-HANG-EMPTY-001 当日证据）
 * 公约：独立无头；fresh ≤1 次；单点失败落 json 继续；产物只进本目录。
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
const ROUTE = '/service/chain-analysis?workspace=graph&tab=graph';
const DEEP = (id) => `/service/chain-analysis?workspace=graph&tab=records&view=result&demo_state=result&task_id=${id}`;
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

// 结果壳采集：radio 选中态 + 图例词可见性 + hang 空文案
async function shellFacts(page) {
  const radio = await safe(async () =>
    ((await page.locator('main .arco-radio.arco-radio-checked').first().innerText().catch(() => '')) || '').trim());
  const legend = {};
  for (const k of ['机构', '企业', '高校', '资本', '投资', '合作', '竞争', '人才流动']) {
    legend[k] = await safe(async () =>
      await page.locator('main').getByText(k, { exact: true }).first().isVisible().catch(() => false));
  }
  const body = await mainText(page);
  return {
    radio_checked: radio,
    legend,
    has_shell_title: body.includes('服务生态关系图谱'),
    hang_empty_note: /当前 hang 无可见点边|无可见点边/.test(body),
    node_edge_zero: /节点数 \/ 关系边数\s*0 \/ 0/.test(body.replace(/\u00a0/g, ' ')),
  };
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);

  // A) 历史任务 radio 模式普查（3 条深链）
  OUT.history_radio = {};
  for (const id of ['SVC-20260903-001', 'SVC-20260902-001', 'SVC-20260823-001']) {
    OUT.history_radio[id] = await safe(async () => {
      await page.goto(BASE + DEEP(id), { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);
      await closeBasket(page);
      return { ...(await shellFacts(page)), url: page.url() };
    });
  }

  // B) fresh 模式②（≤1 次）：新一代信息技术 + ② 机构+关联主体
  OUT.fresh_mode2 = await safe(async () => {
    await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
    await ensureLogin(page);
    await page.waitForTimeout(2500);
    await closeBasket(page);
    // 选产业（P7：点可见 view 容器，选项在 .arco-trigger-popup:visible）
    const sel = page.locator('.industry-catalog-select').first();
    await sel.click({ timeout: 6000 });
    await page.waitForTimeout(600);
    await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
      .filter({ hasText: '新一代信息技术' }).first().click({ timeout: 6000 });
    await page.waitForTimeout(600);
    // 切模式②（跨 tick 断言 P2）
    await page.getByText('② 机构+关联主体', { exact: true }).first().click({ timeout: 6000 });
    await page.waitForTimeout(600);
    const radioBefore = await page.locator('main .arco-radio.arco-radio-checked').first().innerText();
    // 开始分析（g2 证实合法条件后 enabled）
    const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
    const enabled = await start.isEnabled();
    if (!enabled) return { err: '开始分析 disabled（合法条件后仍不可点）', radio_before: radioBefore.trim() };
    await start.click({ timeout: 6000 });
    // 过程页：等「分析结果已生成」+「查看结果」
    await page.waitForURL((u) => String(u).includes('view=processing'), { timeout: 15000 });
    await page.getByRole('button', { name: '查看结果', exact: true }).first().click({ timeout: 20000 });
    await page.waitForURL((u) => String(u).includes('view=result'), { timeout: 15000 });
    await page.waitForTimeout(3500);
    await closeBasket(page);
    const facts = await shellFacts(page);
    const m = /task_id=(SVC-[0-9-]+)/.exec(page.url());
    await page.screenshot({ path: path.join(__dirname, 'probe-p008-mode2-result.png'), fullPage: false });
    return { task_id: m ? m[1] : null, url: page.url(), radio_before: radioBefore.trim(), enabled, ...facts };
  });

  await page.screenshot({ path: path.join(__dirname, 'probe-p008-final.png'), fullPage: false });
  dump('_probe-p008-fresh.json', OUT);
  await browser.close();
  console.log('DONE ->', path.join(__dirname, '_probe-p008-fresh.json'));
})().catch((e) => { dump('_probe-p008-fresh.json', { fatal: String(e) }); console.error(e); process.exit(1); });
