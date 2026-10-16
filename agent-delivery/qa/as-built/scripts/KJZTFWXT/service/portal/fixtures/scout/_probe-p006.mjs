#!/usr/bin/env node
/**
 * 一次性无头探针（P0-06 前置：环节代表机构下钻落局探查）。产物：probe-p006.json + probe-p006-*.png
 * 探查问题：产业分布页选产业后，环节区实际形态——
 *   ① 环节卡是否渲染（stageRows 有无数据）；② 点击环节卡后发生什么（展开列表？抽屉？跳转？）
 *   ③ 若跳分析侧，分析侧落点是什么；④ 有无「代表机构列表」承载。
 * 禁止当 runner；禁止有头 MCP。探针公约：失败落 json 后继续，不卡死。
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
    await page.waitForTimeout(300);
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const report = { surveyed_at: new Date().toISOString(), steps: [] };
const shot = async (n) => {
  const p = path.join(outDir, `probe-p006-${n}.png`);
  await page.screenshot({ path: p, fullPage: false });
  return `fixtures/scout/probe-p006-${n}.png`;
};

try {
  // S1: 登录 → 门户概况
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL('service-portal/overview', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2500);
  await closeBasket(page);

  // S2: 选产业「新一代信息技术」
  const ind = page.locator('.arco-select-view').filter({ has: page.locator('input[placeholder="全部产业"]') }).first();
  await ind.click();
  await page.waitForTimeout(400);
  await page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click();
  await page.waitForTimeout(1000);

  // S3: 切产业分布 Tab
  await page.getByRole('tab', { name: '服务机构产业分布', exact: true }).click();
  await page.waitForTimeout(1800);
  await closeBasket(page);
  await page.waitForTimeout(600);

  // S4: 环节区形态盘点
  const stageCards = page.locator('.svc-portal-stage-card');
  const stageCount = await stageCards.count();
  const stageEmpty = await page.getByText(/暂无环节分布/).count();
  const stageSection = await page.getByRole('heading', { name: /产业链全景|环节服务分布/ }).count();
  const s4 = {
    stage_section_heading: stageSection > 0,
    stage_card_count: stageCount,
    stage_empty_copy: stageEmpty > 0,
    stage_aria_sample: stageCount ? await stageCards.first().getAttribute('aria-label') : null,
    stage_card_texts: stageCount ? (await stageCards.allInnerTexts()).slice(0, 8) : [],
  };
  report.steps.push({ id: 'S4-stage-area', ...s4, screenshot: await shot('stage-area') });
  console.log('S4:', JSON.stringify(s4));

  // S5: 若有环节卡，点第一张，观察行为（P2 跨 tick）
  if (stageCount > 0) {
    const urlBefore = page.url();
    const firstAria = s4.stage_aria_sample;
    await stageCards.first().click();
    await page.waitForTimeout(2500); // 等 SPA 导航/抽屉/展开任一形态
    const urlAfter = page.url();
    const drawerVisible = await page.locator('.arco-drawer').first().isVisible().catch(() => false);
    const drawerCount = await page.locator('.arco-drawer').count();
    // 展开形态探测：点击后环节卡内部或其后是否出现机构列表（li/机构名/大学/学院/公司等）
    const mainText = ((await page.locator('main').first().innerText().catch(() => '')) || '').slice(0, 600);
    const expandedList = await page.locator('.svc-portal-stage-card ul, .svc-portal-stage-card + * li').count();
    const s5 = {
      url_before: urlBefore,
      url_after: urlAfter,
      navigated: urlAfter !== urlBefore,
      drawer_count: drawerCount,
      drawer_visible: drawerVisible,
      expanded_list_li_count: expandedList,
      main_text_head: mainText.replace(/\n/g, ' | ').slice(0, 300),
      has_representative_org_copy: /代表机构|机构列表|大学|学院|研究所|公司/.test(mainText),
    };
    report.steps.push({ id: 'S5-click-first-stage', first_aria: firstAria, ...s5, screenshot: await shot('after-click') });
    console.log('S5:', JSON.stringify(s5));

    // S6: 若跳去了分析侧，看落点页形态（有无机构列表可点、有无抽屉可开）
    if (s5.navigated && /chain-analysis/.test(urlAfter)) {
      await page.waitForTimeout(2000);
      const s6text = ((await page.locator('main').first().innerText().catch(() => '')) || '');
      const orgListItems = await page.locator('main li:has-text("公司"), main li:has-text("大学"), main li:has-text("学院"), main li:has-text("所"), main [class*=org-item], main [class*=org-card]').count();
      const s6 = {
        url: page.url(),
        h1s: await page.locator('h1, h2, h3').allInnerTexts().catch(() => []),
        org_like_items: orgListItems,
        text_head: s6text.replace(/\n/g, ' | ').slice(0, 400),
      };
      report.steps.push({ id: 'S6-analysis-side-landing', ...s6, screenshot: await shot('analysis-side') });
      console.log('S6:', JSON.stringify(s6));
    }
  }

  report.overall = 'done';
} catch (err) {
  report.overall = 'error';
  report.error = String(err && err.message);
  console.error('probe error:', report.error);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p006.json'), JSON.stringify(report, null, 2));
  await browser.close();
}
