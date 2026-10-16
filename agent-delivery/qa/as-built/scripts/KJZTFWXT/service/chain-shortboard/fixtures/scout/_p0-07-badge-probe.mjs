#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-chain-shortboard P0-07（FUNC-00691 环节卡角标与演示声明）。
 * 目的：结果态（诚实空分支）下查明——
 *   a) 「环节机构数」「平均服务深度」声明词旁是否挂 ⓘ 角标（svg/class/aria-label 形态）
 *   b) 演示角标（experiment/mock/demo badge）是否存在
 *   c) 演示态可读声明的字面形态（「演示规则判定」/「专家知识库」）
 *   d) 评审模式开关位置与关闭后：ⓘ 是否保留、评审字样是否泄漏、业务演示声明是否保留
 * 产物落同目录 scout-p0-07-*.json / *.png；勿当 runner。
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
const baseRoute = '/service/chain-analysis?workspace=chain&tab=chain';
const outDir = __dirname;
const dump = (name, data) => fs.writeFileSync(path.join(outDir, name), JSON.stringify(data, null, 2), 'utf8');

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
    await page.waitForTimeout(300);
  }
}

// 现场横切：正文 / 指标词周边 DOM / 角标候选 / 评审痕迹
async function capture(page, tag) {
  await page.waitForTimeout(3000);
  const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');

  // 1) 「环节机构数」「平均服务深度」声明词所在节点的父级 innerHTML（截断）——看词旁是否挂角标
  const wordHosts = [];
  for (const word of ['环节机构数', '平均服务深度']) {
    try {
      const hosts = await page.locator(`text=${word}`).all();
      for (let i = 0; i < Math.min(hosts.length, 2); i++) {
        const parentHtml = await hosts[i].evaluate((el) => {
          let p = el.parentElement;
          for (let up = 0; up < 3 && p && p.innerHTML.length < 1600; up++) p = p.parentElement;
          return p ? p.outerHTML.slice(0, 1600) : '(no parent)';
        }).catch(() => '(eval fail)');
        wordHosts.push({ word, i, parentHtml });
      }
    } catch {}
  }

  // 2) 角标候选盘点（board 全区）
  const badgeSelectors = [
    '.arco-icon-info-circle', '[class*=info-circle]', '[class*=infoCircle]',
    '[class*=experiment]', '.arco-icon-experiment',
    '[class*=mock]', '[class*=Mock]',
    '[class*=demo-badge]', '[class*=demoBadge]', '[class*=demo_badge]',
    '[aria-label*=指标]', '[aria-label*=口径]', '[data-testid*=metric]', '[data-testid*=badge]',
    '[class*=question-circle]', '[class*=questionCircle]',
  ];
  const badgeCounts = {};
  for (const sel of badgeSelectors) {
    try { badgeCounts[sel] = await page.locator(sel).count(); } catch { badgeCounts[sel] = -1; }
  }

  // 3) 命中角标的具体形态（前几个的 outerHTML + aria）
  const badgeSamples = [];
  for (const sel of ['.arco-icon-info-circle', '[class*=experiment]', '[class*=question-circle]']) {
    try {
      const loc = page.locator(sel);
      const n = Math.min(await loc.count(), 3);
      for (let i = 0; i < n; i++) {
        badgeSamples.push({ sel, i, html: (await loc.nth(i).evaluate((el) => el.outerHTML.slice(0, 300)).catch(() => '')) });
      }
    } catch {}
  }

  // 4) 评审痕迹与演示声明
  const reviewTraces = {
    hasReviewText: /评审模式/.test(body),
    hasMetricIdLeak: /M_SVC_CHAIN[A-Z_]*|metric_id/.test(body),
    hasGapLeak: /GAP-|Q-SVCCHAIN/.test(body),
    demoDecl: {
      expertKB: /专家知识库/.test(body),
      demoRule: /演示规则判定/.test(body),
      anyDemo: /演示/.test(body),
    },
    payloadDecl: /只认 payload/.test(body),
    honestEmpty: /没有环节行|不补固定六卡|不补六张空卡/.test(body),
  };

  // 5) 评审开关本体形态（页面内「评审模式」文本旁的 switch/checkbox）
  let reviewSwitch = null;
  try {
    const sw = page.locator('[aria-label="内部评审模式"], [role=switch][aria-label*=评审], .arco-switch').first();
    if (await sw.count()) {
      reviewSwitch = {
        found: true,
        ariaLabel: await sw.getAttribute('aria-label').catch(() => null),
        ariaChecked: await sw.getAttribute('aria-checked').catch(() => null),
        cls: await sw.getAttribute('class').catch(() => null),
        html: await sw.evaluate((el) => el.outerHTML.slice(0, 400)).catch(() => ''),
      };
    } else reviewSwitch = { found: false };
  } catch { reviewSwitch = { found: false, err: true }; }

  const shot = `scout-p0-07-${tag}.png`;
  await page.screenshot({ path: path.join(outDir, shot), fullPage: false }).catch(() => {});
  const out = {
    tag, url: page.url(),
    noStagesVisible: (await page.locator('[data-testid="svc-eco-shortboard-no-stages"]').count()) > 0,
    stationCount: await page.locator('[data-stage-id], .svc-eco-metro-station').count().catch(() => 0),
    wordHosts, badgeCounts, badgeSamples, reviewTraces, reviewSwitch,
    bodySlice: body.slice(0, 2400),
  };
  dump(`scout-p0-07-${tag}.json`, out);
  return out;
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { probed_at: new Date().toISOString(), steps: [] };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(baseRoute.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  // 历史查看结果 → 结果态
  const recTab = page.getByRole('tab', { name: '分析记录', exact: true });
  await recTab.click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  await closeBasket(page);
  const viewBtn = page.getByRole('button', { name: /查看结果/ }).filter({ hasNot: page.locator('.arco-btn-disabled') }).first();
  if (!(await viewBtn.count())) throw new Error('无可用查看结果按钮');
  await viewBtn.click({ timeout: 8000 });
  await page.waitForTimeout(3000);
  // 过程页兜底：再点一次查看结果
  if (/view=processing/.test(page.url())) {
    const vr = page.getByRole('button', { name: /查看结果/ }).filter({ hasNot: page.locator('.arco-btn-disabled') }).first();
    if (await vr.count()) { await vr.click({ timeout: 5000 }).catch(() => {}); await page.waitForTimeout(2500); }
  }
  if (!/view=result/.test(page.url())) throw new Error('未进入结果态: ' + page.url());
  out.steps.push('entered result via history view_result');

  // ---- 1) 评审开着（现场默认态）抓一次 ----
  out.reviewOn = await capture(page, 'review-on');

  // ---- 2) 关闭评审模式再抓（P3 口径）----
  // 开关若在 header persona 菜单内，先开菜单；若页内直接可见则直点
  let switched = false;
  try {
    // 先尝试页内直接可见的「内部评审模式」switch（不动菜单，避免菜单拦截）
    const sw = page.locator('[aria-label="内部评审模式"]').first();
    if ((await sw.count()) && (await sw.isVisible().catch(() => false))) {
      await sw.click({ timeout: 3000 }); switched = true;
    } else {
      // persona 菜单路径：右上头像/人设按钮
      const menuBtn = page.locator('header button, [class*=persona] button, [class*=avatar] button').first();
      if (await menuBtn.count()) {
        await menuBtn.click({ timeout: 3000 }).catch(() => {});
        await page.waitForTimeout(800);
        const sw2 = page.locator('[aria-label="内部评审模式"]').first();
        if ((await sw2.count())) { await sw2.click({ timeout: 3000 }); switched = true; }
        await page.keyboard.press('Escape').catch(() => {});
        await page.waitForTimeout(400);
      }
    }
  } catch {}
  out.steps.push('review switch toggled: ' + switched);
  if (switched) {
    await page.waitForTimeout(1500);
    out.reviewOff = await capture(page, 'review-off');
  }
} catch (e) {
  out.error = String(e).slice(0, 500);
}
dump('scout-p0-07-summary.json', out);
await browser.close();
console.log('p0-07 probe done:', JSON.stringify({
  err: out.error || null,
  reviewOn: { noStages: out.reviewOn?.noStagesVisible, stations: out.reviewOn?.stationCount, badges: out.reviewOn?.badgeCounts, demo: out.reviewOn?.reviewTraces?.demoDecl, payload: out.reviewOn?.reviewTraces?.payloadDecl },
  reviewOff: out.reviewOff ? { badges: out.reviewOff.badgeCounts, demo: out.reviewOff.reviewTraces.demoDecl, leak: { metricId: out.reviewOff.reviewTraces.hasMetricIdLeak, gap: out.reviewOff.reviewTraces.hasGapLeak, reviewText: out.reviewOff.reviewTraces.hasReviewText } } : null,
}));
