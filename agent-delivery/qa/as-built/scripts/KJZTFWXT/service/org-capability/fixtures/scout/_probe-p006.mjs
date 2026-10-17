#!/usr/bin/env node
/**
 * 一次性无头探针（P0-06 写稿用）：算分口径诚实性。
 * ① 配置态 main 全文/图表节点（canvas|svg）形态；② 改权重 25→40 前后「模型区外」文本等值性（验证无重算断言可行性）；
 * ③ 分析记录 tab 条目形态（有无已完成结果）。产物落 scout-p006.json；勿当 runner。只动权重，不点「开始评估」。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const target = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;
const outDir = __dirname;

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
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

// 模型区外文本（等值比对面）+ 图表节点计数 + 结果态关键词行
const bizSnap = (page) => page.evaluate(() => {
  const m = document.querySelector('main');
  if (!m) return { text: '', canvases: 0, svgs: 0, kw: [] };
  const c = m.cloneNode(true);
  c.querySelectorAll('.ent-section-panel').forEach((e) => e.remove());
  const text = (c.innerText || '').replace(/\s+/g, ' ').trim();
  const kw = text.split(/(?<=。)|\n/) || [];
  const lines = (c.innerText || '').split('\n').filter((l) => /得分|名次|排名|最近评估|分数|图表|雷达/.test(l));
  return {
    text,
    canvases: m.querySelectorAll('canvas').length,
    svgs: m.querySelectorAll('svg').length,
    kwLines: lines.slice(0, 20),
    kwJoined: kw.length,
  };
});

const spinVal = (page) => page.locator('[role=spinbutton]').nth(0).inputValue();

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const out = { probed_at: new Date().toISOString(), path: '/service/institution-judgment?workspace=capability&tab=capability', steps: {} };
const dump = () => fs.writeFileSync(path.join(outDir, 'scout-p006.json'), JSON.stringify(out, null, 2));

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  await closeBasket(page);
  await page.waitForTimeout(800);

  // ① 配置态基线
  const snapA = await bizSnap(page);
  out.steps.baseline = {
    spin0: await spinVal(page),
    canvases: snapA.canvases,
    svgs: snapA.svgs,
    kwLines: snapA.kwLines,
    bizTextHead: snapA.text.slice(0, 600),
    bizTextLen: snapA.text.length,
  };
  dump();

  // ② 改权重 25→40 → 等值比对（模型区外）
  await page.locator('[role=spinbutton]').nth(0).fill('40');
  await page.keyboard.press('Tab');
  await page.waitForTimeout(1000);
  const snapB = await bizSnap(page);
  out.steps.after40 = {
    spin0: await spinVal(page),
    equal: snapA.text === snapB.text,
    canvases: snapB.canvases,
    bizTextLen: snapB.text.length,
    headA: snapA.text.slice(0, 200),
    headB: snapB.text.slice(0, 200),
  };
  if (!out.steps.after40.equal) {
    // 找出第一处差异位置辅助归因
    let i = 0;
    while (i < Math.min(snapA.text.length, snapB.text.length) && snapA.text[i] === snapB.text[i]) i++;
    out.steps.after40.firstDiffAt = i;
    out.steps.after40.ctxA = snapA.text.slice(Math.max(0, i - 60), i + 60);
    out.steps.after40.ctxB = snapB.text.slice(Math.max(0, i - 60), i + 60);
  }
  dump();

  // ③ 恢复 25 → 再次等值 + 合计行
  await page.locator('[role=spinbutton]').nth(0).fill('25');
  await page.keyboard.press('Tab');
  await page.waitForTimeout(800);
  const snapC = await bizSnap(page);
  const mainText = await page.locator('main').first().innerText();
  out.steps.restore25 = {
    spin0: await spinVal(page),
    equalVsBaseline: snapA.text === snapC.text,
    sumLine: (mainText.match(/权重合计：[^\n]*/) || [''])[0],
  };
  dump();

  // ④ 分析记录 tab 形态
  const recTab = page.getByRole('tab', { name: '分析记录', exact: true });
  await recTab.click({ timeout: 5000 });
  await page.waitForTimeout(1500);
  const recText = await page.locator('main').first().innerText();
  out.steps.records = {
    textHead: recText.replace(/\s+/g, ' ').slice(0, 800),
    hasDone: /已完成|成功|计算完成/.test(recText),
    canvases: await page.locator('main canvas').count(),
  };
  dump();

  // ⑤ 打开第一条已完成任务的「查看结果」→ 结果视图形态（只读 GET，不发起评估）
  const viewBtn = page.getByRole('button', { name: '查看结果' }).first();
  const viewText = page.getByText('查看结果', { exact: true }).first();
  const target5 = (await viewBtn.count()) ? viewBtn : viewText;
  await target5.click({ timeout: 5000 });
  await page.waitForTimeout(2000);
  const afterView = await page.evaluate(() => {
    const m = document.querySelector('main');
    const overlay = document.querySelector('.arco-drawer, .arco-modal, [role=dialog]');
    const scope = overlay || m;
    const txt = ((scope && scope.innerText) || '').replace(/\s+/g, ' ').trim();
    return {
      overlayKind: overlay ? overlay.className.toString().slice(0, 80) : null,
      url: location.href,
      canvas: document.querySelectorAll('main canvas').length,
      svg: document.querySelectorAll('main svg').length,
      textHead: txt.slice(0, 1200),
      textLen: txt.length,
    };
  });
  out.steps.resultView = afterView;
  dump();
  await page.screenshot({ path: path.join(outDir, 'scout-p006-result.png') });
  // 关浮层（ESC + 关闭钮兜底），结束（runner 每条 expect 自带 goto，不需要还原 tab）
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(400);
  out.steps.close = { url: page.url() };
  dump();
  console.log('probe ok');
  console.log(JSON.stringify(out.steps, null, 2).slice(0, 4000));
} catch (e) {
  out.error = String(e).slice(0, 400);
  dump();
  console.error('probe fail:', out.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
