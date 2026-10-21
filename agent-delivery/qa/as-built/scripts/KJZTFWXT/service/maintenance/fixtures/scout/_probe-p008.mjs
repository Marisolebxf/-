#!/usr/bin/env node
/**
 * P0-08（FUNC-01358 备选-跨目录兄弟模块隔离）写前无头探针。
 * 验证点先验：①枚举 /service/maintenance 页面全部可点元素（含全局导航 vs 页面内入口分层）；
 * ②逐一安全点击页面内可点入口（排除已知危险操作：清空/移除/发起分析/登录出）；
 * ③每点后 URL 是否仍在 /service/maintenance（含 query 子路径）；
 * ④地址栏是否出现兄弟模块路由（chain-maintenance / industry-center 等）；
 * ⑤对比篮浮层开合是否算路由漂移（P0-07 已验开合不漂移 → 预期排除）。
 * 禁止当 runner；禁止有头 MCP。
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
const route = '/service/maintenance';
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

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const probe = { probed_at: new Date().toISOString(), entry_id: 'svc-maintenance', case: 'FUNC-01358 / P0-08', steps: [] };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2000);

  // ---- ① 枚举全部可点元素（在屏 + enabled），并分层 ----
  const inventory = await page.evaluate(() => {
    const sels = 'a[href], button, [role=button], [role=tab], [role=menuitem], [role=link], [onclick], input[type=button], input[type=submit], [tabindex]:not([tabindex="-1"])';
    const nodes = Array.from(document.querySelectorAll(sels));
    const seen = new Set();
    const out = [];
    for (const el of nodes) {
      const r = el.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0) continue;
      const style = getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden' || Number(style.opacity) === 0) continue;
      const tag = el.tagName.toLowerCase();
      const aria = el.getAttribute('aria-label') || '';
      const text = ((el.innerText || el.textContent || '') + '').replace(/\s+/g, ' ').trim().slice(0, 40);
      const href = el.getAttribute('href') || '';
      const key = tag + '|' + aria + '|' + text + '|' + href;
      if (seen.has(key)) continue;
      seen.add(key);
      out.push({ tag, aria, text, href, x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) });
    }
    return out;
  });

  // 全局导航 vs 页面内分层：header/aside（侧栏、顶栏、面包屑容器）内的为全局导航
  const globalNav = await page.evaluate(() => {
    const sels = 'a[href], button, [role=menuitem], [role=tab]';
    const nodes = Array.from(document.querySelectorAll(sels));
    const seen = new Set();
    const out = [];
    for (const el of nodes) {
      // 判定是否在全局导航容器（aside/header/nav）内
      const inGlobal = !!el.closest('aside, header, nav, [class*=sidebar], [class*=menu]');
      if (!inGlobal) continue;
      const r = el.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0) continue;
      const tag = el.tagName.toLowerCase();
      const aria = el.getAttribute('aria-label') || '';
      const text = ((el.innerText || el.textContent || '') + '').replace(/\s+/g, ' ').trim().slice(0, 40);
      const href = el.getAttribute('href') || '';
      const key = tag + '|' + aria + '|' + text + '|' + href;
      if (seen.has(key)) continue;
      seen.add(key);
      out.push({ tag, aria, text, href });
    }
    return out;
  });

  // 页面内可点入口 = inventory - globalNav（按 tag+aria+text+href 匹配）
  const gKeys = new Set(globalNav.map((g) => g.tag + '|' + g.aria + '|' + g.text + '|' + g.href));
  const pageEls = inventory.filter((e) => !gKeys.has(e.tag + '|' + e.aria + '|' + e.text + '|' + e.href));

  // ---- ② 逐一安全点击页面内入口（排除危险操作） ----
  const DANGER = /清空|移除|发起分析|退出|登出|删除|重置/;
  const clickResults = [];
  const urlStart = page.url();

  for (const el of pageEls) {
    const label = el.aria || el.text || el.href || el.tag;
    if (DANGER.test(label)) { clickResults.push({ label, skipped: 'danger', urlAfter: null }); continue; }
    // href 非当前路由的锚点/链接 → 记录预期落点，不点击（兄弟路由直接跳走属真跳转入口）
    if (el.href && el.href !== '#' && !el.href.startsWith('javascript')) {
      const abs = el.href.startsWith('http') ? el.href : new URL(el.href, page.url()).toString();
      const absPath = new URL(abs).pathname;
      clickResults.push({ label, skipped: 'href-link', hrefPath: absPath, urlAfter: null });
      continue;
    }
    // 点击（用 aria/text 复合定位）
    try {
      let loc;
      if (el.aria) loc = page.locator(`${el.tag}[aria-label="${el.aria}"]`).first();
      else if (el.text) loc = page.getByText(el.text, { exact: true }).first();
      else loc = page.locator(el.tag).first();
      await loc.click({ timeout: 3000 });
      await page.waitForTimeout(600);
      const urlAfter = page.url();
      clickResults.push({
        label,
        clicked: true,
        urlAfter,
        stayedOnPage: urlAfter.includes('/service/maintenance'),
        driftedToSibling: /chain-maintenance|industry-center|industry\/|enterprise-search|\/svc\//.test(urlAfter) && !urlAfter.includes('/service/maintenance'),
      });
      // 若点出了本页 → goBack 复位
      if (!urlAfter.includes('/service/maintenance')) {
        await page.goBack({ waitUntil: 'domcontentloaded' }).catch(() => {});
        await page.waitForTimeout(600);
      }
    } catch (e) {
      clickResults.push({ label, clicked: false, err: String(e.message).split('\n')[0], urlAfter: page.url() });
    }
  }

  // ---- ③ 终态：URL + 壳保持 ----
  const urlFinal = page.url();
  const h1Kept = await page.getByRole('heading', { name: '维护管理', level: 1 }).isVisible().catch(() => false);

  probe.steps.push({
    step: 'p008_sibling_isolation',
    url_start: urlStart,
    url_final: urlFinal,
    routeKept: urlFinal.includes('/service/maintenance'),
    h1Kept,
    clickableTotal: inventory.length,
    globalNavCount: globalNav.length,
    pageElCount: pageEls.length,
    globalNav,
    pageEls,
    clickResults,
  });

  await page.screenshot({ path: path.join(outDir, 'probe-p008-final.png'), fullPage: false });
  console.log(JSON.stringify(probe, null, 2));
  fs.writeFileSync(path.join(outDir, 'probe-p008.json'), JSON.stringify(probe, null, 2));
} catch (e) {
  probe.error = String(e);
  console.error(JSON.stringify(probe, null, 2));
  fs.writeFileSync(path.join(outDir, 'probe-p008.json'), JSON.stringify(probe, null, 2));
  process.exitCode = 1;
} finally {
  await browser.close();
}
