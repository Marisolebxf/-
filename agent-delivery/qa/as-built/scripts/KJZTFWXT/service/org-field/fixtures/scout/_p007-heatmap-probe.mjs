#!/usr/bin/env node
/**
 * 一次性无头实勘 · P0-007 热力图悬停明细与角标（分析记录→查看结果 逐条进结果态）。产物落同目录；勿当 runner。
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

const baseUrl = 'http://111.198.38.90:50892/';
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

// 结果态现场盘点：热力图渲染形态 / hover tooltip / ⓘ 与演示角标 / 广度深度数字
async function resultSnapshot(page, tag) {
  const url = page.url();
  const mainText = (await page.locator('main').first().innerText().catch(() => '')) || '';
  const dom = await page.evaluate(() => {
    const main = document.querySelector('main');
    const vis = (el) => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    };
    if (!main) return null;
    const canvases = Array.from(main.querySelectorAll('canvas')).filter(vis).map((c) => ({
      w: Math.round(c.getBoundingClientRect().width),
      h: Math.round(c.getBoundingClientRect().height),
      echarts: !!c.closest('[{_echarts_instance_}]') || !!c.closest('[_echarts_instance_]'),
    }));
    // 图表容器（echarts-for-react 或带 _echarts_instance_ 属性）
    const chartHosts = Array.from(main.querySelectorAll('[_echarts_instance_], .echarts-for-react')).map((n) => ({
      cls: String(n.className).slice(0, 80),
      w: Math.round(n.getBoundingClientRect().width),
    }));
    // tooltip 类浮层（hover 后）
    const floats = Array.from(main.querySelectorAll('div'))
      .filter((n) => vis(n) && (n.textContent || '').trim())
      .filter((n) => {
        const s = getComputedStyle(n);
        return (s.position === 'absolute' || s.position === 'fixed') && (n.className || '').toString().match(/tooltip|trigger-popup|popover/i);
      })
      .map((n) => ({ cls: String(n.className).slice(0, 100), text: (n.textContent || '').trim().slice(0, 200) }));
    // ⓘ 类图标：aria-label 或 class 含 info/metric 的可见元素
    const icons = Array.from(main.querySelectorAll('[aria-label], [class*=info], [class*=metric], [class*=badge], [class*=demo]'))
      .filter(vis)
      .map((n) => ({ aria: n.getAttribute('aria-label'), cls: String(n.className).slice(0, 100), text: (n.textContent || '').trim().slice(0, 40) }))
      .slice(0, 40);
    // 「广度&深度」标题区与「核心结论」区外层 HTML（看角标挂载形态）
    const sectionHtml = {};
    for (const key of ['服务机构产业领域服务广度', '核心结论']) {
      const label = Array.from(main.querySelectorAll('*')).find((n) => n.children.length === 0 && (n.textContent || '').includes(key));
      if (label) {
        let p = label;
        for (let i = 0; i < 3 && p.parentElement && p.parentElement.textContent.length < 3000; i++) p = p.parentElement;
        sectionHtml[key] = (p.outerHTML || '').slice(0, 3000);
      }
    }
    return { canvases, chartHosts, floats, icons, sectionHtml };
  });
  // hover 探测：有 canvas 则悬停中心，抓 tooltip 关键词
  let hover = { attempted: false };
  const canvas = page.locator('main canvas:visible').first();
  if (await canvas.count()) {
    hover.attempted = true;
    try {
      const box = await canvas.boundingBox();
      if (box && box.width > 40 && box.height > 40) {
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
        await page.waitForTimeout(300);
        await page.mouse.move(box.x + box.width / 2 + 6, box.y + box.height / 2 + 6); // 二次触发 tooltip
        await page.waitForTimeout(1200);
        hover.afterText = ((await page.locator('main').first().innerText().catch(() => '')) || '').slice(0, 400);
        const tip = await page.evaluate(() => {
          const vis = (el) => {
            const r = el.getBoundingClientRect();
            return r.width > 0 && r.height > 0;
          };
          const main = document.querySelector('main');
          const hits = [];
          for (const n of main.querySelectorAll('div, .arco-trigger-popup, .arco-tooltip')) {
            if (!vis(n)) continue;
            const t = (n.textContent || '').trim();
            if (!t || t.length > 300) continue;
            const s = getComputedStyle(n);
            const floating = s.position === 'absolute' || s.position === 'fixed';
            const tipish = /tooltip|trigger-popup|popover/i.test(String(n.className));
            if (floating && tipish) hits.push({ cls: String(n.className).slice(0, 120), text: t.slice(0, 200) });
          }
          return hits;
        });
        hover.tooltips = tip;
        hover.keywordHit = tip.some((x) => /深度|领域|广度|机构|覆盖/.test(x.text));
      }
    } catch (e) {
      hover.error = String(e).slice(0, 160);
    }
    await page.screenshot({ path: path.join(outDir, `p007-${tag}-hover.png`) });
  } else {
    await page.screenshot({ path: path.join(outDir, `p007-${tag}.png`) });
  }
  return {
    url,
    honestEmpty: /当前结果快照没有覆盖矩阵/.test(mainText),
    heatHeading: /服务机构产业领域服务广度\s*&\s*深度/.test(mainText),
    heatTabActive: /热力图/.test(mainText),
    breadthDepthNumbers: {
      top3Empty: /暂无可排名机构/.test(mainText),
      topDomainEmpty: /服务深度 TOP 领域（按机构）\s*暂无可排名机构|暂无可排名领域/.test(mainText),
    },
    demoBadgeTexts: (mainText.match(/演示口径[^\\n]{0,30}|演示\s*·[^\\n]{0,20}|🧪/g) || []).slice(0, 6),
    dom,
    hover,
  };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), stages: {} };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await freshGoto(page);

  // 阶段1：分析记录 → 枚举可「查看结果」的历史任务
  await page.getByRole('tab', { name: '分析记录', exact: true }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const recordsText = (await page.locator('main').first().innerText().catch(() => '')) || '';
  const rows = (recordsText.match(/SVC-\d+-\d+[\\s\\S]{0,120}?(?=\nSVC-\d+-\d+|$)/g) || []).slice(0, 8);
  const viewBtns = page.getByRole('button', { name: '查看结果' });
  const viewCount = Math.min(await viewBtns.count(), 4);
  out.stages.records = { sample: recordsText.slice(0, 500), rowsPreview: rows.map((r) => r.slice(0, 90)), viewCount };
  await page.screenshot({ path: path.join(outDir, 'p007-records.png') });

  // 阶段2：逐条「查看结果」→ 结果态盘点（含 hover）
  const results = [];
  for (let i = 0; i < viewCount; i++) {
    await freshGoto(page);
    await page.getByRole('tab', { name: '分析记录', exact: true }).first().click({ timeout: 8000 });
    await page.waitForTimeout(1000);
    const btn = page.getByRole('button', { name: '查看结果' }).nth(i);
    if ((await btn.count()) === 0) break;
    await btn.click({ timeout: 8000 });
    await page.waitForTimeout(2500);
    const snap = await resultSnapshot(page, `r${i}`);
    // 该行任务号：结果页 url/正文里找
    snap.taskId = (page.url().match(/task_id=(SVC-[\d-]+)/) || [])[1] || (snap.hover.afterText || '').match(/SVC-[\d-]+/)?.[0] || null;
    results.push(snap);
    // 复原到记录页供下一轮
  }
  out.stages.results = results;

  // 阶段3：评审模式开↔关对照角标（仅记录；用头部可见「评审模式」控件）
  await freshGoto(page);
  const reviewCtl = page.getByText('评审模式', { exact: true }).first();
  out.stages.reviewToggle = { found: await reviewCtl.count() > 0, tag: null, toggled: false };
  if (out.stages.reviewToggle.found) {
    out.stages.reviewToggle.tag = await reviewCtl.evaluate((n) => ({ tag: n.tagName, cls: String(n.className).slice(0, 120) })).catch(() => null);
  }

  const anyCanvas = results.some((r) => (r.dom?.canvases || []).length > 0);
  const anyHoverHit = results.some((r) => r.hover?.keywordHit);
  const anyBadge = results.some((r) => (r.demoBadgeTexts || []).length > 0);
  out.overall = anyCanvas ? (anyHoverHit ? 'pass-hover' : 'canvas-no-tooltip') : 'honest-empty';
  out.flags = { anyCanvas, anyHoverHit, anyBadge };
  fs.writeFileSync(path.join(outDir, 'scout-p007.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ overall: out.overall, flags: out.flags, viewed: results.length }, null, 2));
} catch (e) {
  out.overall = 'error';
  out.error = String(e).slice(0, 600);
  fs.writeFileSync(path.join(outDir, 'scout-p007.json'), JSON.stringify(out, null, 2));
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
