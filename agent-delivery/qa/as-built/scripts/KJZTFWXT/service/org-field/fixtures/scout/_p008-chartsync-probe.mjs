#!/usr/bin/env node
/**
 * 一次性无头实勘 · P0-008 矩阵图与图型切换（分析记录→查看结果 后切矩阵图再切回）。产物落同目录；勿当 runner。
 * 只读行为勘察：不判验收，observed 记录现场事实。禁 IDE 有头。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const route = '/service/institution-judgment?workspace=field&tab=coverage';
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

async function freshGoto(page) {
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  if (page.url().includes('/login')) {
    await ensureLogin(page);
    await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  }
  await page.waitForTimeout(2000);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

// 图表区状态盘点：switch 状态 / canvas / 矩阵区 DOM / 诚实空文案
async function chartState(page) {
  return await page.evaluate(() => {
    const board = document.querySelector('.svc-org-coverage, [data-testid="svc-org-coverage-board"]');
    if (!board) return { board: false };
    const vis = (el) => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    };
    const sw = board.querySelector('[data-testid="svc-org-coverage-chart-switch"]');
    const labels = sw ? Array.from(sw.querySelectorAll('label')).map((l) => {
      const input = l.querySelector('input');
      return { text: (l.textContent || '').trim(), value: input ? input.value : null, checked: !!(input && input.checked) };
    }) : [];
    const canvases = Array.from(board.querySelectorAll('canvas')).filter(vis).map((c) => ({
      w: Math.round(c.getBoundingClientRect().width),
      h: Math.round(c.getBoundingClientRect().height),
    }));
    // 矩阵图常见宿主：echarts 实例容器 / svg / 四象限文本
    const echartsHosts = Array.from(board.querySelectorAll('[_echarts_instance_], .echarts-for-react')).filter(vis).map((n) => ({
      cls: String(n.className).slice(0, 80),
      w: Math.round(n.getBoundingClientRect().width),
      h: Math.round(n.getBoundingClientRect().height),
    }));
    const svgCount = Array.from(board.querySelectorAll('svg')).filter((s) => vis(s) && !s.closest('button, .metric-spec-card, .perm-pending-badge, .trace-info-icon')).length;
    const alert = Array.from(board.querySelectorAll('.arco-alert')).map((a) => (a.textContent || '').trim().slice(0, 120));
    // 轴/象限类文本（矩阵图 X/Y 轴标签或四象限标注，DOM 或 echarts 内嵌均探测 DOM 可见文本）
    const boardText = (board.textContent || '');
    return {
      board: true,
      switchLabels: labels,
      canvasCount: canvases.length,
      canvases,
      echartsHosts,
      svgCount,
      alerts: alert,
      axisLikeText: {
        xCoverage: /覆盖领域数/.test(boardText),
        yDepth: /平均深度得分/.test(boardText),
        quadrant: /高深度|低深度|高覆盖|低覆盖|象限/.test(boardText),
      },
      boardHtmlTail: (board.innerHTML || '').slice(-1200),
    };
  });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), stages: {} };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await freshGoto(page);

  // 阶段1：分析记录 → 第一条已完成任务「查看结果」进结果态
  await page.getByRole('tab', { name: '分析记录', exact: true }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const viewBtns = page.getByRole('button', { name: '查看结果' });
  if (!(await viewBtns.count())) throw new Error('分析记录无查看结果按钮');
  await viewBtns.first().click({ timeout: 8000 });
  await page.waitForTimeout(2500);
  const board0 = page.locator('.svc-org-coverage, [data-testid="svc-org-coverage-board"]').first();
  if (!((await board0.count()) && (await board0.isVisible().catch(() => false)))) throw new Error('结果态热力图板不可见');
  out.stages.resultState = await chartState(page);
  out.stages.resultUrl = page.url();
  await page.screenshot({ path: path.join(outDir, 'p008-0-result-heatmap.png') });

  // 阶段2：切矩阵图 → 盘点
  const matrixLabel = page.locator('[data-testid="svc-org-coverage-chart-switch"] label:has-text("矩阵图")').first();
  await matrixLabel.click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  out.stages.matrixState = await chartState(page);
  await page.screenshot({ path: path.join(outDir, 'p008-1-result-matrix.png') });

  // 阶段3：切回热力图 → 盘点
  const heatLabel = page.locator('[data-testid="svc-org-coverage-chart-switch"] label:has-text("热力图")').first();
  await heatLabel.click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  out.stages.backState = await chartState(page);
  await page.screenshot({ path: path.join(outDir, 'p008-2-result-back-heatmap.png') });

  // 阶段4：上下文观察（已选机构/领域上下文在矩阵切换后是否保留——诚实空态下读 main 文本证据）
  out.stages.contextText = ((await page.locator('main').first().innerText().catch(() => '')) || '').slice(0, 600);

  const anyCanvas = [out.stages.resultState, out.stages.matrixState, out.stages.backState]
    .some((s) => s && s.canvasCount > 0);
  out.overall = anyCanvas ? 'canvas-present' : 'honest-empty';
  out.flags = { anyCanvas };
  fs.writeFileSync(path.join(outDir, 'scout-p008.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ overall: out.overall, flags: out.flags, stages: Object.keys(out.stages) }, null, 2));
} catch (e) {
  out.overall = 'error';
  out.error = String(e).slice(0, 600);
  fs.writeFileSync(path.join(outDir, 'scout-p008.json'), JSON.stringify(out, null, 2));
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
