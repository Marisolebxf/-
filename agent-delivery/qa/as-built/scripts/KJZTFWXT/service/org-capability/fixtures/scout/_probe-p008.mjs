#!/usr/bin/env node
/**
 * 一次性无头探针（P0-08 写稿用）：评估结果呈现。
 * ① 结果态「排名列表/雷达图」形态（图表开关/单选、同源同视图、雷达 radio 渲染条件）；
 * ② 图表容器形态（canvas/svg）与维度轴线索；③ ⓘ/指标说明入口在结果视图的存在性（不依赖数据与否）；
 * ④ 第二条已完成任务 SVC-20260824-003 交叉验证（空态一致性）。
 * 只读 GET result，不发起评估。产物落 scout-p008.json；勿当 runner。
 */
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const recordsUrl = `${baseUrl}service/institution-judgment?workspace=capability&tab=records`;
const outDir = __dirname;

async function ensureLogin(page) {
  await page.waitForTimeout(600);
  if (!page.url().includes('/login')) return;
  const pw = page.locator('input[type=password]');
  await pw.first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
  if (!(await pw.count())) return; // 已带会话跳走，无需登录
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await pw.first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function openDoneResult(page, rowIndex) {
  // P0-06 同款路径：capability 深链 → 点击「分析记录」tab（tab=records 直达深链不渲染壳，探针实测 main 空）
  const targetUrl = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2500);
  const tab = page.getByRole('tab', { name: '分析记录', exact: true });
  await tab.click({ timeout: 10000 });
  await page.waitForTimeout(2000);
  // 「查看结果」就绪轮询（冷启动兜底，15s）
  try {
    await page.getByText('查看结果', { exact: true }).first().waitFor({ state: 'visible', timeout: 15000 });
  } catch {
    out.debug = { stage: 'records-not-ready', url: page.url(), textHead: ((await page.locator('main').innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 600) };
    dump();
  }
  // 第 rowIndex 条已完成任务的「查看结果」（记录行序=创建时间倒序）
  const byRole = page.getByRole('button', { name: '查看结果' });
  const target = (await byRole.count()) ? byRole.nth(rowIndex) : page.getByText('查看结果', { exact: true }).nth(rowIndex);
  if (!(await target.count())) {
    out.debug = { url: page.url(), textHead: ((await page.locator('main').innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 500) };
    dump();
  }
  await target.click({ timeout: 8000 });
  await page.waitForTimeout(2500);
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const out = { probed_at: new Date().toISOString(), steps: {} };
const dump = () => fs.writeFileSync(path.join(outDir, 'scout-p008.json'), JSON.stringify(out, null, 2));

try {
  for (const [i, taskId] of ['SVC-20260907-003', 'SVC-20260824-003'].entries()) {
    await openDoneResult(page, i);
    const url = page.url();
    const urlMatch = url.includes('task_id=' + taskId);
    const snap = await page.evaluate(() => {
      const m = document.querySelector('main');
      const txt = ((m && m.innerText) || '').replace(/\s+/g, ' ').trim();
      const radios = [...document.querySelectorAll('.arco-radio, [role=radio]')].map((r) => ((r.innerText) || '').trim()).filter(Boolean);
      const btns = [...document.querySelectorAll('main button')].map((b) => ((b.innerText) || '').trim()).filter(Boolean);
      const chartSwitch = document.querySelector('[data-testid=svc-org-cap-chart-switch]');
      return {
        canvas: document.querySelectorAll('main canvas').length,
        svg: document.querySelectorAll('main svg').length,
        hasEmpty: txt.includes('暂无技术力评估结果'),
        hasRankWord: txt.includes('排名列表'),
        hasRadarWord: txt.includes('雷达图'),
        hasScoreHeader: txt.includes('综合得分'),
        radios,
        chartSwitchHtml: chartSwitch ? chartSwitch.outerHTML.slice(0, 300) : null,
        btnHead: btns.slice(0, 15),
        // ⓘ/说明入口线索：icon 按钮类名、aria-label、文本含「指标说明」
        infoCandidates: [...document.querySelectorAll('main [aria-label], main .arco-icon, main [class*=info], main [class*=metric], main [class*=spec]')]
          .map((e) => ({ tag: e.tagName, cls: String(e.className).slice(0, 60), aria: e.getAttribute('aria-label') }))
          .filter((x) => x.aria || /info|metric|spec/i.test(x.cls))
          .slice(0, 20),
        hasMetricWord: /指标说明/.test(txt),
        textHead: txt.slice(0, 700),
        textLen: txt.length,
      };
    });
    out.steps['task_' + taskId] = { urlMatch, url, ...snap };
    dump();
    await page.screenshot({ path: path.join(outDir, `scout-p008-result-${i + 1}.png`) });
  }
  console.log('probe ok');
  console.log(JSON.stringify(out.steps, null, 2).slice(0, 5000));
} catch (e) {
  out.error = String(e).slice(0, 400);
  dump();
  console.error('probe fail:', out.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
