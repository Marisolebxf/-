#!/usr/bin/env node
/** P0-19 续探：集群清空后继续清产业/细分；门禁与静默写回。 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const route = '/industry-center/diagnosis?workspace=bottleneck&tab=bottleneck';

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function readView(page, ariaOrSel) {
  const loc = ariaOrSel.startsWith('.')
    ? page.locator(ariaOrSel).first()
    : page.locator(`.arco-select-view[aria-label="${ariaOrSel}"]`).first();
  if (!(await loc.count())) return { text: '', html: '', hasClear: false };
  const text = ((await loc.getAttribute('title')) || (await loc.innerText()) || '').replace(/\s+/g, ' ').trim();
  const html = (await loc.evaluate((el) => el.outerHTML)).slice(0, 500);
  await loc.hover().catch(() => {});
  await page.waitForTimeout(350);
  const parent = loc.locator('xpath=ancestor::*[contains(@class,"arco-select")][1]');
  const clearN = await page.locator(
    ariaOrSel.startsWith('.')
      ? `${ariaOrSel} .arco-select-view-clear-btn`
      : `.arco-select-view[aria-label="${ariaOrSel}"] .arco-select-view-clear-btn, .arco-select:has(.arco-select-view[aria-label="${ariaOrSel}"]) .arco-select-view-clear-btn`
  ).count();
  return { text, html, hasClear: clearN > 0, clearN };
}

async function clearByHover(page, aria) {
  const view = page.locator(`.arco-select-view[aria-label="${aria}"]`).first();
  await view.hover();
  await page.waitForTimeout(400);
  const btn = page.locator(`.arco-select-view[aria-label="${aria}"] .arco-select-view-clear-btn`).first();
  const n = await btn.count();
  if (!n) return { ok: false, reason: 'no-clear-btn' };
  await btn.click({ force: true, timeout: 4000 });
  await page.waitForTimeout(900);
  return { ok: true };
}

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
const log = [];
try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  const cb = page.locator('[aria-label="关闭对比篮"]');
  if ((await cb.count()) && (await cb.first().isVisible().catch(() => false))) await cb.first().click().catch(() => {});
  if ((await page.getByRole('tab', { name: '产业瓶颈堵点识别' }).getAttribute('aria-selected')) !== 'true') {
    await page.getByRole('tab', { name: '产业瓶颈堵点识别' }).click();
    await page.waitForTimeout(800);
  }

  const snap = async (tag) => {
    const start = page.getByRole('button', { name: '开始分析' });
    const s = {
      tag,
      cluster: await readView(page, '集群'),
      chain: await readView(page, '产业'),
      segment: await readView(page, '.industry-catalog-select .arco-select-view, .industry-catalog-select'),
      startDisabled: await start.isDisabled().catch(() => null),
      startClass: (await start.getAttribute('class').catch(() => '')) || '',
      mainHead: ((await page.locator('main').first().innerText()).slice(0, 400)),
    };
    log.push(s);
    return s;
  };

  await snap('landing');

  // clear cluster
  const c1 = await clearByHover(page, '集群');
  log.push({ action: 'clear-cluster', ...c1 });
  await snap('after-cluster-clear');

  // clear chain
  const c2 = await clearByHover(page, '产业');
  log.push({ action: 'clear-chain', ...c2 });
  await snap('after-chain-clear');

  // segment structure + try clear again
  const segHtml = await page.locator('.industry-catalog-select').first().evaluate((el) => el.outerHTML).catch(() => '');
  await page.locator('.industry-catalog-select').first().hover().catch(() => {});
  await page.waitForTimeout(500);
  const segClearN = await page.locator('.industry-catalog-select .arco-select-view-clear-btn').count();
  log.push({ action: 'seg-inspect', segClearN, segHtml: (segHtml || '').slice(0, 800) });

  // try Esc / open dropdown and pick nothing — open then click outside
  const segView = page.locator('.industry-catalog-select .arco-select-view, .industry-catalog-select').first();
  await segView.click().catch(() => {});
  await page.waitForTimeout(500);
  const popupOpts = await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-trigger-popup:visible .arco-cascader-option').count();
  log.push({ action: 'seg-open', popupOpts });
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(400);

  // wait for silent write-back
  await page.waitForTimeout(2500);
  const final = await snap('settle-2.5s');

  // click start while cluster empty — does it create task?
  const posts = [];
  page.on('request', (req) => {
    if (req.method() === 'POST' && /analysis\/tasks|topicAsync/.test(req.url())) posts.push(req.url());
  });
  const start = page.getByRole('button', { name: '开始分析' });
  const wasDisabled = await start.isDisabled();
  if (!wasDisabled) {
    await start.click().catch((e) => log.push({ action: 'start-click-err', err: String(e.message || e).slice(0, 100) }));
    await page.waitForTimeout(2000);
  }
  const afterClick = await snap('after-start-click');
  log.push({ action: 'start-gate', wasDisabled, posts, toast: await page.locator('.arco-message, .arco-notification').allInnerTexts().catch(() => []) });

  await page.screenshot({ path: path.join(__dirname, 'probe-p019b-final.png'), fullPage: false });

  const out = {
    probed_at: new Date().toISOString(),
    case_id: 'P0-19',
    steps: log,
    summary: {
      clusterClearWorks: c1.ok,
      chainClearWorks: c2.ok,
      segmentHasClear: segClearN > 0,
      finalEmpty: !final.cluster.text && (!final.chain.text || final.chain.text.length < 2),
      startDisabledWhenPartialEmpty: final.startDisabled,
      taskCreatedOnEmptyish: posts.length > 0,
    },
  };
  fs.writeFileSync(path.join(__dirname, 'probe-p019b.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out.summary, null, 2));
  console.log('cluster after clear:', log.find((x) => x.tag === 'after-cluster-clear')?.cluster?.text);
  console.log('chain after clear:', log.find((x) => x.tag === 'after-chain-clear')?.chain?.text);
  console.log('seg after chain clear:', log.find((x) => x.tag === 'after-chain-clear')?.segment?.text);
  console.log('settle:', { c: final.cluster.text, h: final.chain.text, s: final.segment.text, disabled: final.startDisabled });
  console.log('posts', posts);
} finally {
  await browser.close();
}
