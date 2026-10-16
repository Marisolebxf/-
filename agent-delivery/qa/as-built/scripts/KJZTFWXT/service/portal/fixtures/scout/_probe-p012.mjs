#!/usr/bin/env node
/** 一次性探针 P0-12（FUNC-01317 金银铜+在库不足诚实标注）：技术能力榜行/配色/在库标注。产物 probe-p012.json + 截图 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const outDir = __dirname;

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
})).newPage();
const report = { surveyed_at: new Date().toISOString() };
try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

  const apiPromise = page.waitForResponse((r) => /capability|tech.?rank|rank/.test(r.url()) && r.request().method() !== 'OPTIONS', { timeout: 20000 }).catch(() => null);
  await page.goto(new URL('service-portal/capability-rank', baseUrl).toString(), { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2800);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
  report.url = page.url();
  report.h1 = await page.getByRole('heading', { name: /服务机构技术能力/ }).count();
  report.empty_copy = await page.getByText(/暂无技术力入榜机构|暂无覆盖机构入榜|不凑满 30|在库/).allTextContents().then((a) => a.slice(0, 12)).catch(() => []);
  report.empty_visible = (await page.getByText(/暂无技术力入榜机构|暂无覆盖机构入榜|不凑满 30/).count()) > 0;
  report.stock_label = await page.getByText(/在库|不足 30|共\s*\d+\s*家|入榜/).allTextContents().then((a) => a.slice(0, 16)).catch(() => []);
  report.equal_weight = (await page.getByText(/固定五维等权|五维等权|门户不可调权/).count()) > 0;

  // 榜单行候选
  const rowSels = [
    '.svc-portal-rank-row',
    '.svc-portal-tech-rank li',
    '.svc-portal-capability-rank li',
    'main [class*=rank] li',
    'main [class*=Rank] li',
    'main table tbody tr',
    'main .arco-list-item',
  ];
  report.row_counts = {};
  for (const s of rowSels) {
    report.row_counts[s] = await page.locator(s).count();
  }
  const bestSel = Object.entries(report.row_counts).sort((a, b) => b[1] - a[1])[0];
  report.best_row_sel = bestSel;
  report.has_rows = (bestSel && bestSel[1] > 0) || false;

  // 金银铜色 / 名次样式采样（前 4 行）
  if (report.has_rows) {
    const rows = page.locator(bestSel[0]);
    const n = Math.min(await rows.count(), 6);
    report.row_styles = [];
    for (let i = 0; i < n; i++) {
      const el = rows.nth(i);
      const info = await el.evaluate((node) => {
        const cs = getComputedStyle(node);
        const medal = node.querySelector('[class*=gold],[class*=silver],[class*=bronze],[class*=medal],[class*=rank-1],[class*=rank-2],[class*=rank-3]');
        const medalCs = medal ? getComputedStyle(medal) : null;
        return {
          text: (node.innerText || '').split('\n').slice(0, 3).join(' | ').slice(0, 80),
          className: String(node.className || '').slice(0, 120),
          color: cs.color,
          bg: cs.backgroundColor,
          medal_class: medal ? String(medal.className || '').slice(0, 80) : null,
          medal_color: medalCs ? medalCs.color : null,
          medal_bg: medalCs ? medalCs.backgroundColor : null,
        };
      }).catch((e) => ({ err: String(e && e.message) }));
      report.row_styles.push(info);
    }
  }

  // 色值字面量 / class 名扫描
  report.medal_dom = await page.evaluate(() => {
    const hits = [];
    document.querySelectorAll('[class*="gold"],[class*="silver"],[class*="bronze"],[class*="medal"],[class*="rank-1"],[class*="rank-2"],[class*="rank-3"]').forEach((n) => {
      hits.push({ tag: n.tagName, className: String(n.className || '').slice(0, 100), text: (n.innerText || '').slice(0, 40) });
    });
    return hits.slice(0, 20);
  });

  const api = await apiPromise;
  if (api) {
    report.api = { url: api.url(), status: api.status() };
    try {
      const body = await api.json();
      const d = body && body.data !== undefined ? body.data : body;
      const list = (d && (d.list || d.ranks || d.items || d.rows)) || (Array.isArray(d) ? d : null);
      report.api.list_len = Array.isArray(list) ? list.length : null;
      report.api.keys = d && typeof d === 'object' && !Array.isArray(d) ? Object.keys(d).slice(0, 20) : null;
      report.api.sample = Array.isArray(list) && list[0] ? Object.keys(list[0]).slice(0, 16) : null;
      report.api.stock = d && (d.stock_count ?? d.in_stock ?? d.total ?? d.count ?? d.org_count);
    } catch (e) {
      report.api.body_parse_error = String(e && e.message);
    }
  } else {
    report.api = null;
  }

  // 主区文本摘录（找在库/名次）
  report.main_snip = await page.locator('main').innerText().then((t) => t.slice(0, 900)).catch(() => '');
  await page.screenshot({ path: path.join(outDir, 'probe-p012-capability.png'), fullPage: false });

  // 若默认空，试选产业看是否出榜
  const ind = page.locator('.arco-select-view:has(input[placeholder="全部产业"])').first();
  if (await ind.count()) {
    await ind.click().catch(() => {});
    await page.waitForTimeout(600);
    const opt = page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-trigger-popup:visible [role="option"]').first();
    if (await opt.count()) {
      const optText = ((await opt.innerText().catch(() => '')) || '').slice(0, 40);
      await opt.click().catch(() => {});
      await page.waitForTimeout(2200);
      report.after_industry = {
        picked: optText,
        url: page.url(),
        empty_visible: (await page.getByText(/暂无技术力入榜机构|暂无覆盖机构入榜|不凑满 30/).count()) > 0,
        row_counts: {},
        stock_label: await page.getByText(/在库|不足 30|共\s*\d+\s*家|入榜/).allTextContents().then((a) => a.slice(0, 12)).catch(() => []),
      };
      for (const s of rowSels) {
        report.after_industry.row_counts[s] = await page.locator(s).count();
      }
      report.after_industry.medal_dom = await page.evaluate(() => {
        const hits = [];
        document.querySelectorAll('[class*="gold"],[class*="silver"],[class*="bronze"],[class*="medal"]').forEach((n) => {
          hits.push(String(n.className || '').slice(0, 80));
        });
        return hits.slice(0, 12);
      });
      report.after_industry.main_snip = await page.locator('main').innerText().then((t) => t.slice(0, 700)).catch(() => '');
      await page.screenshot({ path: path.join(outDir, 'probe-p012-after-industry.png'), fullPage: false });
    }
  }
} catch (e) {
  report.error = String(e && e.stack || e);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p012.json'), JSON.stringify(report, null, 2));
  await browser.close();
  console.log(JSON.stringify({ url: report.url, has_rows: report.has_rows, empty_visible: report.empty_visible, error: report.error }, null, 2));
}
